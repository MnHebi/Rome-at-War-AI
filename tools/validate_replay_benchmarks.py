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
    "decoded-selected-color-and-resolved-team",
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

    pending_setups = payload.get("pending_match_setups", [])
    if not isinstance(pending_setups, list):
        errors.append("pending_match_setups must be a list")
    else:
        pending_ids: set[str] = set()
        for setup in pending_setups:
            if not isinstance(setup, dict):
                errors.append("every pending match setup must be an object")
                continue
            setup_id = setup.get("id")
            if not isinstance(setup_id, str) or not setup_id.strip():
                errors.append("every pending match setup requires a non-empty id")
            elif setup_id in pending_ids:
                errors.append(f"duplicate pending match setup id: {setup_id}")
            else:
                pending_ids.add(setup_id)
            if setup.get("status") != "awaiting-replay":
                errors.append(f"{setup_id}: pending setup status must be awaiting-replay")

            setup_source = setup.get("source")
            if not isinstance(setup_source, dict):
                errors.append(f"{setup_id}: pending setup source must be an object")
            else:
                basename = setup_source.get("image_basename")
                if (
                    not isinstance(basename, str)
                    or "/" in basename
                    or "\\" in basename
                    or Path(basename).name != basename
                ):
                    errors.append(f"{setup_id}: image_basename must not contain a path")
                digest = setup_source.get("sha256")
                if not isinstance(digest, str) or not SHA256.fullmatch(digest):
                    errors.append(
                        f"{setup_id}: setup sha256 must be 64 uppercase hexadecimal digits"
                    )

            settings = setup.get("settings")
            if not isinstance(settings, dict) or not settings:
                errors.append(f"{setup_id}: pending setup settings must be an object")

            players = setup.get("players")
            if not isinstance(players, list) or len(players) < 2:
                errors.append(f"{setup_id}: pending setup requires at least two players")
            else:
                color_ids: set[int] = set()
                colors: set[str] = set()
                for index, player in enumerate(players):
                    if not isinstance(player, dict):
                        errors.append(f"{setup_id}: players[{index}] must be an object")
                        continue
                    color_id = player.get("color_id")
                    color = player.get("color")
                    civilization = player.get("civilization")
                    team = player.get("team")
                    if not isinstance(color_id, int) or color_id <= 0:
                        errors.append(f"{setup_id}: players[{index}] has invalid color_id")
                    elif color_id in color_ids:
                        errors.append(f"{setup_id}: duplicate color_id {color_id}")
                    else:
                        color_ids.add(color_id)
                    if not isinstance(color, str) or not color.strip():
                        errors.append(f"{setup_id}: players[{index}] has invalid color")
                    elif color in colors:
                        errors.append(f"{setup_id}: duplicate color {color}")
                    else:
                        colors.add(color)
                    if not isinstance(civilization, str) or not civilization.strip():
                        errors.append(
                            f"{setup_id}: players[{index}] has invalid civilization"
                        )
                    if not isinstance(team, int) or team <= 0:
                        errors.append(f"{setup_id}: players[{index}] has invalid team")

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
                    "decoded-selected-color-and-resolved-team",
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
