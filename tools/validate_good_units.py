#!/usr/bin/env python3
"""Validate completeness and schema invariants of good-unit-evaluations.json."""

from __future__ import annotations

import argparse
import hashlib
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
EXPECTED_NAVAL_CLASSES = {
    "Polyreme",
    "Fire Ship",
    "Demolition Ship",
    "Scout Ship",
    "Hemiolia",
    "Boarding Ship",
    "Juggernaut",
    "Quadrireme/Quinquereme",
    "Octeres",
    "Naval unique unit",
}
EXPECTED_NAVAL_UPGRADE_CHAINS = {
    "Polyreme": {"34": [[539, 21]], "35": [[539, 442], [21, 442]]},
    "Fire Ship": {"34": [[1103, 529]], "246": [[529, 532], [1103, 532]]},
    "Demolition Ship": {
        "34": [[1104, 527]],
        "1033": [[1104, 527]],
        "244": [[527, 528], [1104, 528]],
    },
    "Scout Ship": {"1007": [[1877, 1878]], "1008": [[1877, 1879], [1878, 1879]]},
    "Hemiolia": {
        "1005": [[1881, 1882], [1950, 1951]],
        "1006": [[1882, 1883], [1881, 1883], [1950, 1952], [1951, 1952]],
    },
    "Boarding Ship": {},
    "Juggernaut": {"376": [[420, 691], [1885, 1886]]},
    "Quadrireme/Quinquereme": {"1003": [[1870, 1750]]},
    "Octeres": {},
    "Naval unique unit": {"1174": [[2008, 2009]]},
}


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_ROOT = ROOT.parent.parent / "RaW data fix"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_provenance_sources(
    document: dict[str, Any], provenance_paths: dict[str, Path]
) -> list[str]:
    issues: list[str] = []
    provenance = document.get("source_provenance", {})
    for key, source_path in provenance_paths.items():
        if not source_path.exists():
            issues.append(f"source_provenance/{key}: authoritative source is missing: {source_path}")
            continue
        actual_hash = sha256(source_path)
        if provenance.get(key) != actual_hash:
            issues.append(f"source_provenance/{key}: recorded hash does not match {source_path}")
    return issues


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
    if document.get("schema_version") != 2:
        issues.append("schema_version must be 2 for data-derived naval capability")
    if document.get("naval_upgrade_chains") != EXPECTED_NAVAL_UPGRADE_CHAINS:
        issues.append("naval upgrade-chain metadata does not match the audited DAT mapping")

    for key in order:
        civ = civilizations.get(key)
        if not isinstance(civ, dict):
            issues.append(f"{key}: missing civilization record")
            continue
        if not civ.get("civilization") or not civ.get("host_civilization"):
            issues.append(f"{key}: missing display or host civilization name")
        if not str(civ.get("host_civilization_constant", "")).endswith("-CIV"):
            issues.append(f"{key}: missing host civilization preprocessor constant")
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
        navy = ratings.get("Navy", {})
        if navy.get("rating") != "No":
            score = navy.get("capability_score")
            components = [
                navy.get("lineup_completeness_score"),
                navy.get("ship_class_quality_score"),
                navy.get("support_upgrade_score"),
            ]
            steady_state = navy.get("steady_state_capability_score")
            throughput_adjustment = navy.get("production_throughput_adjustment")
            if not isinstance(score, (int, float)) or not 0 <= score <= 100:
                issues.append(f"{key}/Navy: capability_score must be within 0..100")
            if not all(isinstance(value, (int, float)) for value in components):
                issues.append(f"{key}/Navy: capability components are incomplete")
            elif not isinstance(steady_state, (int, float)) or abs(sum(components) - steady_state) > 0.03:
                issues.append(f"{key}/Navy: steady-state components do not sum correctly")
            if not isinstance(throughput_adjustment, (int, float)) or not -5 <= throughput_adjustment <= 5:
                issues.append(f"{key}/Navy: production-throughput adjustment must be within -5..5")
            elif isinstance(score, (int, float)) and isinstance(steady_state, (int, float)):
                expected_score = min(100.0, max(0.0, steady_state + throughput_adjustment))
                if abs(expected_score - score) > 0.03:
                    issues.append(f"{key}/Navy: competitive score does not include its signed throughput adjustment")
            if set(navy.get("ship_classes", {})) != EXPECTED_NAVAL_CLASSES:
                issues.append(f"{key}/Navy: ship-class breakdown is incomplete")
            for class_name, class_record in navy.get("ship_classes", {}).items():
                if "upgrade_tech_ids" not in class_record or "applied_upgrade_tech_ids" not in class_record:
                    issues.append(f"{key}/Navy/{class_name}: upgrade evidence is incomplete")
                if class_record.get("available") and "forced_upgrade_from_unit_ids" not in class_record:
                    issues.append(f"{key}/Navy/{class_name}: forced-upgrade closure evidence is missing")
                if class_record.get("available") and "throughput_multiplier" not in class_record:
                    issues.append(f"{key}/Navy/{class_name}: production-throughput evidence is missing")
                if class_record.get("available"):
                    for field in (
                        "production_source",
                        "production_work_rate",
                        "production_batch_size",
                        "production_resource_cost_per_ship",
                    ):
                        if field not in class_record:
                            issues.append(f"{key}/Navy/{class_name}: missing {field}")
                    statistics = class_record.get("statistics", {})
                    if any(
                        field not in statistics
                        for field in (
                            "projectile_count",
                            "max_projectile_count",
                            "operational_projectile_factor",
                            "garrison_capacity",
                            "blast_width",
                        )
                    ):
                        issues.append(f"{key}/Navy/{class_name}: projectile/blast evidence is missing")
                applied = set(class_record.get("applied_upgrade_tech_ids", []))
                upgrade_ids = set(class_record.get("upgrade_tech_ids", []))
                if not applied <= upgrade_ids:
                    issues.append(f"{key}/Navy/{class_name}: applied upgrades exceed the audited chain")
            expected_specialist = bool(
                navy.get("has_quadrireme_or_quinquereme") and navy.get("has_octeres")
            )
            if navy.get("specialist_support_detachment") is not expected_specialist:
                issues.append(f"{key}/Navy: specialist support flag disagrees with hull access")
            expected_rating = (
                "Excellent" if score >= 80 else "Good" if score >= 70 else "Mediocre" if score >= 60 else "Bad"
            ) if isinstance(score, (int, float)) else None
            if expected_rating and navy.get("rating") != expected_rating:
                issues.append(f"{key}/Navy: rating disagrees with capability thresholds")

    def naval_class(civ_key: str, class_name: str) -> dict[str, Any]:
        return civilizations[civ_key]["ratings"]["Navy"]["ship_classes"][class_name]

    applied_expectations = {
        ("britons", "Polyreme"): [34],
        ("athenians", "Polyreme"): [34, 35],
        ("athenians", "Juggernaut"): [376],
        ("athenians", "Quadrireme/Quinquereme"): [1003],
        ("illyrians", "Naval unique unit"): [1174],
    }
    calibration_civs = {civ_key for civ_key, _ in applied_expectations} | {
        "britons",
        "armenia",
        "carthagians",
    }
    # Unit tests intentionally use reduced fixtures; authoritative calibration
    # assertions apply when the real 34-civilization document is present.
    if calibration_civs <= set(civilizations):
        for (civ_key, class_name), expected in applied_expectations.items():
            actual = naval_class(civ_key, class_name).get("applied_upgrade_tech_ids")
            if actual != expected:
                issues.append(
                    f"{civ_key}/Navy/{class_name}: expected applied upgrade evidence {expected}, found {actual}"
                )

        britons_hemiolia = naval_class("britons", "Hemiolia")
        if britons_hemiolia.get("statistics", {}).get("projectile_count") != 5:
            issues.append("britons/Navy/Hemiolia: elite five-projectile lethality is not represented")
        armenian_demo = naval_class("armenia", "Demolition Ship")
        if armenian_demo.get("statistics", {}).get("blast_width") != 3.5:
            issues.append("armenia/Navy/Demolition Ship: heavy 3.5 blast width is not represented")
        carthage_scout = naval_class("carthagians", "Scout Ship")
        if carthage_scout.get("production_source") != "Shipyard":
            issues.append("carthagians/Navy/Scout Ship: unrealized Cothon output inflates runtime production")
        if not str(carthage_scout.get("potential_production_source", "")).startswith(
            "Cothon potential"
        ):
            issues.append("carthagians/Navy/Scout Ship: validated Cothon potential is not recorded")
        if carthage_scout.get("potential_production_batch_size") != 5:
            issues.append("carthagians/Navy/Scout Ship: Expanded Docking Bays five-ship potential is missing")
        if not 0 < carthage_scout.get("potential_production_resource_cost_per_ship", 9999) < 90:
            issues.append("carthagians/Navy/Scout Ship: Cothon potential per-ship discount is missing")
        persian_demo = naval_class("persians", "Demolition Ship")
        if persian_demo.get("unit_id") != 527:
            issues.append("persians/Navy/Demolition Ship: tech 34 forced upgrade to unit 527 is missing")
        if persian_demo.get("forced_upgrade_from_unit_ids") != [1104]:
            issues.append("persians/Navy/Demolition Ship: forced source unit 1104 is not recorded")
        tess = naval_class("macedonians", "Naval unique unit").get("statistics", {})
        if tess.get("projectile_count") != 1 or tess.get("max_projectile_count") != 20:
            issues.append("macedonians/Navy/Naval unique unit: Tessarakonteres 1/20 projectile bounds are missing")
        if tess.get("garrison_capacity") != 60:
            issues.append("macedonians/Navy/Naval unique unit: fully upgraded Tessarakonteres capacity must be 60")
        if not 2.7 < tess.get("operational_projectile_factor", 0) < 2.8:
            issues.append("macedonians/Navy/Naval unique unit: garrison firepower is not population-discounted")

    provenance = document.get("source_provenance", {})
    for name, value in provenance.items():
        if name.endswith("_sha256") and (not isinstance(value, str) or len(value) != 64):
            issues.append(f"source_provenance/{name}: invalid SHA-256")
    return issues


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", type=Path, default=Path("good-unit-evaluations.json"))
    parser.add_argument("--manifest", type=Path, default=Path("unique-unit-production.json"))
    parser.add_argument("--data-root", type=Path, default=DEFAULT_DATA_ROOT)
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
    provenance_paths = {
        "empires2_x2_p1.dat_sha256": args.data_root / "resources" / "_common" / "dat" / "empires2_x2_p1.dat",
        "civTechTrees.json_sha256": args.data_root / "resources" / "_common" / "dat" / "civTechTrees.json",
        "civilizations.json_sha256": args.data_root / "resources" / "_common" / "dat" / "civilizations.json",
        "AI RAW.per_sha256": ROOT / "AI RAW.per",
        "unique-unit-production.json_sha256": args.manifest,
    }
    issues.extend(validate_provenance_sources(document, provenance_paths))
    if issues:
        for issue in issues:
            print(f"ERROR: {issue}")
        raise SystemExit(1)
    print(f"Validated {EXPECTED_CIVS} civilizations x {len(EXPECTED_CATEGORIES)} rating categories: {args.path}")


if __name__ == "__main__":
    main()
