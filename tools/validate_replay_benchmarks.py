#!/usr/bin/env python3
"""Validate the AI-side replay benchmark knowledge artifact."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BENCHMARKS = ROOT / "replay-benchmarks.json"
SHA256 = re.compile(r"^[0-9A-F]{64}$")
VALID_STATUSES = {"fresh-replay-required", "runtime-confirmed", "superseded"}
VALID_TEAM_MAPPING_BASES = {
    "decoded-diplomacy-matrix",
    "unresolved",
    "user-verified-match-setup",
}


def require_text_list(entry: dict, key: str, errors: list[str]) -> None:
    value = entry.get(key)
    if not isinstance(value, list) or not value:
        errors.append(f"{entry.get('id', '<unknown>')}: {key} must be a non-empty list")
        return
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            errors.append(f"{entry.get('id', '<unknown>')}: {key}[{index}] must be text")


def validate() -> list[str]:
    errors: list[str] = []
    try:
        payload = json.loads(BENCHMARKS.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot read {BENCHMARKS.name}: {exc}"]

    if payload.get("schema_version") != 1:
        errors.append("schema_version must be 1")

    benchmarks = payload.get("benchmarks")
    if not isinstance(benchmarks, list) or not benchmarks:
        return errors + ["benchmarks must be a non-empty list"]

    seen_ids: set[str] = set()
    for entry in benchmarks:
        if not isinstance(entry, dict):
            errors.append("every benchmark must be an object")
            continue

        benchmark_id = entry.get("id")
        if not isinstance(benchmark_id, str) or not benchmark_id.strip():
            errors.append("every benchmark requires a non-empty id")
        elif benchmark_id in seen_ids:
            errors.append(f"duplicate benchmark id: {benchmark_id}")
        else:
            seen_ids.add(benchmark_id)

        source = entry.get("source")
        if not isinstance(source, dict):
            errors.append(f"{benchmark_id}: source must be an object")
        else:
            basename = source.get("file_basename")
            if (
                not isinstance(basename, str)
                or "/" in basename
                or "\\" in basename
                or Path(basename).name != basename
            ):
                errors.append(f"{benchmark_id}: file_basename must not contain a path")
            digest = source.get("sha256")
            if not isinstance(digest, str) or not SHA256.fullmatch(digest):
                errors.append(f"{benchmark_id}: sha256 must be 64 uppercase hexadecimal digits")
            duration = source.get("duration_seconds")
            if not isinstance(duration, int) or duration <= 0:
                errors.append(f"{benchmark_id}: duration_seconds must be a positive integer")

            players = source.get("players")
            if isinstance(players, list) and len(players) > 2:
                basis = source.get("team_mapping_basis")
                note = source.get("team_mapping_note")
                if basis not in VALID_TEAM_MAPPING_BASES:
                    errors.append(
                        f"{benchmark_id}: multiplayer team_mapping_basis must be one of "
                        f"{sorted(VALID_TEAM_MAPPING_BASES)}"
                    )
                if not isinstance(note, str) or not note.strip():
                    errors.append(
                        f"{benchmark_id}: multiplayer team_mapping_note must explain provenance"
                    )

                team_labels = [
                    player
                    for player in players
                    if isinstance(player, str) and re.search(r"\(team\s+\d+\)$", player)
                ]
                if basis == "unresolved" and team_labels:
                    errors.append(
                        f"{benchmark_id}: unresolved team mapping must not label player teams"
                    )
                if basis in {
                    "decoded-diplomacy-matrix",
                    "user-verified-match-setup",
                } and len(team_labels) != len(players):
                    errors.append(
                        f"{benchmark_id}: authoritative team mapping must label every player"
                    )

        for key in (
            "direct_replay_observations",
            "implementation_inferences",
            "changes_under_test",
            "fresh_replay_acceptance",
            "known_limits",
        ):
            require_text_list(entry, key, errors)

        status = entry.get("validation_status")
        if status not in VALID_STATUSES:
            errors.append(f"{benchmark_id}: invalid validation_status {status!r}")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print(json.dumps({"errors": errors}, indent=2))
        return 1

    payload = json.loads(BENCHMARKS.read_text(encoding="utf-8"))
    print(f"Validated {len(payload['benchmarks'])} replay benchmark(s): {BENCHMARKS.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
