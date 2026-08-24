#!/usr/bin/env python3
"""Compare the generated ODS matrix with good-unit-evaluations.json."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from read_ods import read_sheets
from validate_good_units import EXPECTED_CATEGORIES


HEADERS = ("Civ name", "Host civ") + EXPECTED_CATEGORIES + ("UU Type",)
STATS_HEADERS = (
    "Civ", "Host civ", "Category", "Rating", "Selected unit", "Unit ID", "HP", "Attack",
    "Bonus damage", "Melee armor", "Pierce armor", "Range", "Minimum range", "Speed", "Reload",
    "Accuracy", "Food", "Wood", "Gold", "Stone", "Population", "Train time", "Combat ratio",
    "Number multiplier", "Efficiency", "Missing standard tech IDs", "Full standard suite",
    "Parthian Tactics", "Legal packages", "Blast width", "Attack delay frames", "Friendly fire", "Reason",
)
NAVAL_HEADERS = (
    "Civ", "Doctrine", "Overall score", "Steady-state score", "Rating", "Lineup /30",
    "Class quality /50", "Upgrades /20", "Throughput adjustment ±5", "Fleet throughput",
    "Shipyard work rate", "Ship class", "Available", "Selected unit", "Unit ID", "Tier",
    "Lineup points", "Quality points", "Combat ratio", "Number multiplier", "Efficiency",
    "Class throughput", "Production source", "Production work rate", "Batch size", "Per-ship cost",
    "Potential production source", "Potential throughput", "Potential work rate",
    "Potential batch size", "Potential per-ship cost",
    "Empty projectiles", "Max projectiles", "Operational projectile factor", "Garrison capacity",
    "Blast width", "Upgrade tech IDs", "Applied upgrade tech IDs",
    "Forced upgrade from unit IDs", "Q/Quin", "Octeres", "Specialist support",
)


def normalize(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def normalize_stat(value: object, column: int) -> str:
    normalized = normalize(value)
    if column in {26, 27}:
        return {"0": "false", "1": "true"}.get(normalized, normalized)
    return normalized


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("workbook", nargs="?", type=Path, default=Path("RAW AI good units per civ.ods"))
    parser.add_argument("--evaluations", type=Path, default=Path("good-unit-evaluations.json"))
    args = parser.parse_args()
    document = json.loads(args.evaluations.read_text(encoding="utf-8-sig"))
    sheets = read_sheets(args.workbook)
    if not sheets:
        raise SystemExit("ERROR: workbook has no sheets")
    sheets_by_name = {sheet["name"]: sheet for sheet in sheets}
    if {"Sheet1", "Methodology", "Final stats", "Naval capability"} - set(sheets_by_name):
        raise SystemExit("ERROR: workbook must contain Sheet1, Methodology, Final stats, and Naval capability")
    rows = sheets_by_name["Sheet1"]["rows"]
    issues: list[str] = []
    if tuple(rows[0][: len(HEADERS)]) != HEADERS:
        issues.append("Sheet1 headers do not match the evaluation schema")
    if len(rows) < 35:
        issues.append("Sheet1 has fewer than 34 civilization rows")
    else:
        for row_index, key in enumerate(document["display_order"], start=1):
            expected = document["civilizations"][key]
            expected_row = [
                expected["civilization"],
                expected["host_civilization"],
                *[expected["ratings"][category]["rating"] for category in EXPECTED_CATEGORIES],
                expected["unique_unit_type"],
            ]
            actual = rows[row_index][: len(HEADERS)]
            if actual != expected_row:
                issues.append(f"row {row_index + 1} ({key}) differs from generated evaluations")

    stats_rows = sheets_by_name["Final stats"]["rows"]
    if not stats_rows or tuple(stats_rows[0][: len(STATS_HEADERS)]) != STATS_HEADERS:
        issues.append("Final stats headers do not match the evidence schema")
    elif len(stats_rows) != 681:
        issues.append("Final stats must contain one header plus 34 x 20 evidence rows")
    else:
        row_index = 1
        for key in document["display_order"]:
            civ = document["civilizations"][key]
            for category in EXPECTED_CATEGORIES:
                record = civ["ratings"][category]
                stat = record.get("statistics", {})
                expected_stats = [
                    civ["civilization"], civ["host_civilization"], category, record["rating"],
                    record.get("unit_name", ""), record.get("unit_id", ""), stat.get("hp", ""),
                    stat.get("attack", ""), stat.get("bonus_damage_total", ""), stat.get("melee_armor", ""),
                    stat.get("pierce_armor", ""), stat.get("range", ""), stat.get("minimum_range", ""),
                    stat.get("speed", ""), stat.get("reload_time", ""), stat.get("accuracy", ""),
                    stat.get("food_cost", ""), stat.get("wood_cost", ""), stat.get("gold_cost", ""),
                    stat.get("stone_cost", ""), stat.get("population", ""), stat.get("train_time", ""),
                    record.get("combat_ratio", ""), record.get("number_multiplier", ""),
                    record.get("number_adjusted_ratio", ""), ", ".join(map(str, record.get("missing_standard_tech_ids", []))),
                    record.get("full_standard_upgrades", ""), record.get("has_parthian_tactics", ""),
                    record.get("compatible_package_count", ""), stat.get("blast_width", ""),
                    stat.get("attack_delay_frames", ""), stat.get("friendly_fire_damage", ""), record["reason"],
                ]
                actual_stats = stats_rows[row_index][: len(STATS_HEADERS)]
                if [normalize_stat(value, column) for column, value in enumerate(actual_stats)] != [
                    normalize_stat(value, column) for column, value in enumerate(expected_stats)
                ]:
                    issues.append(f"Final stats row {row_index + 1} ({key}/{category}) differs from evaluations")
                row_index += 1

    naval_rows = sheets_by_name["Naval capability"]["rows"]
    if not naval_rows or tuple(naval_rows[0][: len(NAVAL_HEADERS)]) != NAVAL_HEADERS:
        issues.append("Naval capability headers do not match the evidence schema")
    elif len(naval_rows) != 341:
        issues.append("Naval capability must contain one header plus 34 x 10 ship-class rows")
    else:
        row_index = 1
        for key in document["display_order"]:
            civ = document["civilizations"][key]
            navy = civ["ratings"]["Navy"]
            for class_name, record in navy["ship_classes"].items():
                expected_naval = [
                    civ["civilization"], "Yes" if navy["primary_navy_doctrine"] else "No",
                    navy["capability_score"], navy["steady_state_capability_score"], navy["rating"],
                    navy["lineup_completeness_score"], navy["ship_class_quality_score"],
                    navy["support_upgrade_score"], navy["production_throughput_adjustment"],
                    navy["fleet_throughput_multiplier"], navy["shipyard_work_rate"], class_name,
                    record["available"], record.get("unit_name", ""), record.get("unit_id", ""),
                    record.get("tier_multiplier", ""), record.get("lineup_points", ""),
                    record.get("quality_points", ""), record.get("combat_ratio", ""),
                    record.get("number_multiplier", ""), record.get("number_adjusted_ratio", ""),
                    record.get("throughput_multiplier", ""), record.get("production_source", ""),
                    record.get("production_work_rate", ""), record.get("production_batch_size", ""),
                    record.get("production_resource_cost_per_ship", ""),
                    record.get("potential_production_source", ""),
                    record.get("potential_throughput_multiplier", ""),
                    record.get("potential_production_work_rate", ""),
                    record.get("potential_production_batch_size", ""),
                    record.get("potential_production_resource_cost_per_ship", ""),
                    record.get("statistics", {}).get("projectile_count", ""),
                    record.get("statistics", {}).get("max_projectile_count", ""),
                    record.get("statistics", {}).get("operational_projectile_factor", ""),
                    record.get("statistics", {}).get("garrison_capacity", ""),
                    record.get("statistics", {}).get("blast_width", ""),
                    ", ".join(map(str, record.get("upgrade_tech_ids", []))),
                    ", ".join(map(str, record.get("applied_upgrade_tech_ids", []))),
                    ", ".join(map(str, record.get("forced_upgrade_from_unit_ids", []))),
                    navy["has_quadrireme_or_quinquereme"], navy["has_octeres"],
                    navy["specialist_support_detachment"],
                ]
                actual_naval = naval_rows[row_index][: len(NAVAL_HEADERS)]
                if [normalize(value) for value in actual_naval] != [normalize(value) for value in expected_naval]:
                    issues.append(f"Naval capability row {row_index + 1} ({key}/{class_name}) differs from evaluations")
                row_index += 1
    if issues:
        for issue in issues:
            print(f"ERROR: {issue}")
        raise SystemExit(1)
    print(
        "Validated workbook round trip: 34 civilizations x 20 ratings, "
        f"UU Type, 680 unit evidence rows, and 340 naval class rows ({args.workbook})"
    )


if __name__ == "__main__":
    main()
