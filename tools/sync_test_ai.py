#!/usr/bin/env python3
"""Check or synchronize the repository's runtime AI files to a local test mod."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest().upper()


def runtime_files() -> list[Path]:
    return sorted((*ROOT.glob("*.ai"), *ROOT.glob("*.per")), key=lambda path: path.name)


def manifest_digest(paths: list[Path]) -> str:
    """Hash runtime names and contents so one value identifies the full payload."""
    value = hashlib.sha256()
    for path in sorted(paths, key=lambda item: item.name):
        value.update(path.name.encode("utf-8"))
        value.update(b"\0")
        value.update(bytes.fromhex(digest(path)))
    return value.hexdigest().upper()


def payload_digest(payload: dict[str, bytes]) -> str:
    value = hashlib.sha256()
    for name, data in sorted(payload.items()):
        value.update(name.encode('utf-8'))
        value.update(b'\0')
        value.update(hashlib.sha256(data).digest())
    return value.hexdigest().upper()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check or copy top-level .ai/.per runtime files to a test-mod AI directory."
    )
    parser.add_argument("target", type=Path, help="Existing resources/_common/ai directory")
    parser.add_argument('--writer-trace', action='store_true',
                        help='Compile bounded T10 writer telemetry in memory from this checkout')
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Copy missing or different files. Without this flag the command is read-only.",
    )
    args = parser.parse_args()

    target = args.target.expanduser().resolve()
    if not target.is_dir():
        parser.error(f"target is not an existing directory: {target}")
    if args.target.is_symlink():
        parser.error("target must not be a symbolic link")

    suffix = tuple(part.lower() for part in target.parts[-3:])
    if suffix != ("resources", "_common", "ai"):
        parser.error("target must end in resources/_common/ai")

    source_root = ROOT.resolve()
    if target == source_root or source_root in target.parents:
        parser.error("target must be an external test-mod AI directory")

    files = runtime_files()
    payload = {path.name: path.read_bytes() for path in files}
    source_hash = payload_digest(payload)
    if args.writer_trace:
        from writer_trace import compile_payload
        payload, trace_manifest = compile_payload(payload)
        saved = ROOT / 'writer-trace-sites.json'
        if not saved.exists() or json.loads(saved.read_text(encoding='utf-8')) != trace_manifest:
            parser.error('writer-trace-sites.json is missing/stale; generate it with tools/writer_trace.py --manifest writer-trace-sites.json')
    expected_names = {path.name for path in files}
    unexpected = sorted(
        path.name
        for pattern in ("*.ai", "*.per")
        for path in target.glob(pattern)
        if path.name not in expected_names
    )
    missing: list[str] = []
    different: list[str] = []
    copied: list[str] = []

    for source in files:
        destination = target / source.name
        if not destination.exists():
            missing.append(source.name)
            needs_copy = True
        else:
            needs_copy = hashlib.sha256(payload[source.name]).hexdigest().upper() != digest(destination)
            if needs_copy:
                different.append(source.name)

        if args.apply and needs_copy:
            temporary_name: str | None = None
            try:
                with tempfile.NamedTemporaryFile(
                    dir=target,
                    prefix=f".{source.name}.",
                    suffix=".tmp",
                    delete=False,
                ) as temporary:
                    temporary_name = temporary.name
                temporary_path = Path(temporary_name)
                temporary_path.write_bytes(payload[source.name])
                expected = hashlib.sha256(payload[source.name]).hexdigest().upper()
                if expected != digest(temporary_path):
                    raise RuntimeError(f"temporary hash mismatch: {source.name}")
                temporary_path.replace(destination)
            finally:
                if temporary_name is not None:
                    Path(temporary_name).unlink(missing_ok=True)
            if hashlib.sha256(payload[source.name]).hexdigest().upper() != digest(destination):
                raise RuntimeError(f"post-replace hash mismatch: {source.name}")
            copied.append(source.name)

    remaining = [
        source.name
        for source in files
        if not (target / source.name).exists()
        or hashlib.sha256(payload[source.name]).hexdigest().upper() != digest(target / source.name)
    ]
    report = {
        "mode": "apply" if args.apply else "check",
        "source": str(source_root),
        "target": str(target),
        "runtime_files": len(files),
        "source_runtime_sha256": payload_digest(payload),
        "checkout_runtime_sha256": source_hash,
        "writer_trace": args.writer_trace,
        "target_runtime_sha256": (
            manifest_digest([target / source.name for source in files])
            if not remaining
            else None
        ),
        "unexpected_runtime_files": unexpected,
        "missing_before": missing,
        "different_before": different,
        "copied": copied,
        "remaining_mismatches": remaining,
    }
    print(json.dumps(report, indent=2))
    return 1 if remaining or unexpected else 0


if __name__ == "__main__":
    sys.exit(main())
