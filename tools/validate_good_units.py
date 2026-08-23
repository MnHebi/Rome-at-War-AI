#!/usr/bin/env python3
"""Validate completeness and schema invariants of good-unit-evaluations.json."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


EXPECTED_CIVS = 34
EXPECTED_CATEGORIES = (
    "Militia",
    "Spearmen",
    "Archer",
    "Skirmisher",
    "Cavalry Archer",
    "Camel Archer",
    "Elephant Archer",
    "Chariot Archer",
    "Light Cavalry",
    "Cavalry",
    "Camel Rider",
    "Battle Elephant",
    "Chariot",
    "Battering Ram",
    "Armored Elephant",
    "Mangonel",
    "Scorpion",
    "Catapult",
    "Priest",
    "Navy",
)
VALID_RATINGS = {"No", "Bad", "Mediocre", "Good", "Excellent"}


def validate_document(document: dict[str, Any], unique_unit_ids: set[int] | None = None) -> list[str]:
    issues: list[str] = []
    order = document.get("display_order", [])
    categories = tuple(document.get("category_order", []))
    civilizations = document.get("civilizations", {})
    if len(order) != EXPECTED_CIVS or len(set(order)) != EXPECTED_CIVS:
        issues.append(f"display_order must contain {EXPECTED_CIVS} unique civilizations")
    if categories != EXPECTED_CATEGORIES:
        issues.append("category_order does not match the workbook's 20 rating columns")
    if set(order) != set(civilizations):
        issues.append("civilization keys do not match display_order")

    for key in order:
        civ = civilizations.get(key)
        if not isinstance(civ, dict):
            issues.append(f"{key}: missing civilization record")
            continue
        if not civ.get("civilization") or not civ.get("host_civilization"):
            issues.append(f"{key}: missing display or host civilization name")
        if not civ.get("unique_unit_type"):
            issues.append(f"{key}: missing unique-unit type")
        ratings = civ.get("ratings", {})
        if set(ratings) != set(EXPECTED_CATEGORIES):
            issues.append(f"{key}: rating columns are incomplete or unexpected")
        for category in EXPECTED_CATEGORIES:
            record = ratings.get(category)
            if not isinstance(record, dict):
                issues.append(f"{key}/{category}: missing rating record")
                continue
            if record.get("rating") not in VALID_RATINGS:
                issues.append(f"{key}/{category}: invalid or blank rating")
            if not record.get("reason"):
                issues.append(f"{key}/{category}: missing explanation")
            if category not in {"Priest", "Navy"} and record.get("rating") != "No":
                for field in ("unit_id", "unit_name", "statistics", "combat_ratio"):
                    if field not in record:
                        issues.append(f"{key}/{category}: missing {field}")
                if unique_unit_ids and record.get("unit_id") in unique_unit_ids:
                    issues.append(f"{key}/{category}: manifest-listed unique unit leaked into generic rating")

    provenance = document.get("source_provenance", {})
    for name, value in provenance.items():
        if name.endswith("_sha256") and (not isinstance(value, str) or len(value) != 64):
            issues.append(f"source_provenance/{name}: invalid SHA-256")
    return issues


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", type=Path, default=Path("good-unit-evaluations.json"))
    parser.add_argument("--manifest", type=Path, default=Path("unique-unit-production.json"))
    args = parser.parse_args()
    document = json.loads(args.path.read_text(encoding="utf-8-sig"))
    unique_ids: set[int] = set()
    if args.manifest.exists():
        manifest = json.loads(args.manifest.read_text(encoding="utf-8-sig"))
        unique_ids = {
            int(unit_id)
            for civ in manifest.get("civs", {}).values()
            for family in civ.get("families", [])
            for unit_id in family.get("source_unit_ids", [])
        }
    issues = validate_document(document, unique_ids)
    if issues:
        for issue in issues:
            print(f"ERROR: {issue}")
        raise SystemExit(1)
    print(f"Validated {EXPECTED_CIVS} civilizations x {len(EXPECTED_CATEGORIES)} rating categories: {args.path}")


if __name__ == "__main__":
    main()
