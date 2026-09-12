#!/usr/bin/env python3
"""Correlate T53 Ctrl Villager retasks with exact order-706 actor streams."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from audit_task_ownership import economic_retask_correlation, read_stream


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("replay", type=Path)
    parser.add_argument("--parser-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--window-seconds", type=int, default=30)
    args = parser.parse_args()
    if args.window_seconds <= 0:
        parser.error("--window-seconds must be positive")
    events, counts, failures = read_stream(args.replay, args.parser_root)
    report = economic_retask_correlation(events, args.window_seconds * 1000)
    with args.replay.open("rb") as source:
        report["source_sha256"] = hashlib.file_digest(source, "sha256").hexdigest()
    report["action_counts"] = counts
    report["decoder_failures"] = failures
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
