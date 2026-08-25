#!/usr/bin/env python3
"""Synchronize the maintained ODS workbook with generated evaluations.

The primary spreadsheet authoring workflow produces and renders XLSX through
@oai/artifact-tool.  That tool does not export ODS, so this narrow fallback
updates cell values and adds the naval evidence sheet without changing the
existing OpenDocument styles, settings, or embedded resources.
"""

from __future__ import annotations

import argparse
import copy
import io
import json
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from validate_good_units import EXPECTED_CATEGORIES
from validate_good_units_workbook import HEADERS, NAVAL_HEADERS, STATS_HEADERS


ROOT = Path(__file__).resolve().parents[1]
NS = {
    "office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
    "table": "urn:oasis:names:tc:opendocument:xmlns:table:1.0",
    "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
    "meta": "urn:oasis:names:tc:opendocument:xmlns:meta:1.0",
}
def attr(namespace: str, name: str) -> str:
    return f"{{{NS[namespace]}}}{name}"


def register_namespaces(xml: bytes) -> None:
    seen: set[str] = set()
    for _, (prefix, uri) in ET.iterparse(io.BytesIO(xml), events=("start-ns",)):
        if prefix in seen:
            continue
        seen.add(prefix)
        ET.register_namespace(prefix, uri)


def cell_text(cell: ET.Element) -> str:
    return "\n".join("".join(paragraph.itertext()) for paragraph in cell.findall("text:p", NS))


def expanded_cells(row: ET.Element, required: int) -> list[ET.Element]:
    """Expand repeated cells only through the requested logical column count."""
    cell_tags = {attr("table", "table-cell"), attr("table", "covered-table-cell")}
    logical = 0
    for child in list(row):
        if child.tag not in cell_tags:
            continue
        repeat = int(child.get(attr("table", "number-columns-repeated"), "1"))
        if repeat <= 1 or logical >= required:
            logical += repeat
            continue
        expand = min(repeat, required - logical)
        if expand <= 1:
            logical += repeat
            continue
        position = list(row).index(child)
        row.remove(child)
        for offset in range(expand):
            clone = copy.deepcopy(child)
            clone.attrib.pop(attr("table", "number-columns-repeated"), None)
            row.insert(position + offset, clone)
        remainder = repeat - expand
        if remainder:
            trailing = copy.deepcopy(child)
            if remainder == 1:
                trailing.attrib.pop(attr("table", "number-columns-repeated"), None)
            else:
                trailing.set(attr("table", "number-columns-repeated"), str(remainder))
            row.insert(position + expand, trailing)
        logical += repeat
    return [child for child in row if child.tag in cell_tags][:required]


def set_cell(row: ET.Element, column: int, value: object) -> None:
    cells = expanded_cells(row, column + 1)
    if len(cells) <= column:
        while len(cells) <= column:
            cell = ET.Element(attr("table", "table-cell"))
            row.append(cell)
            cells.append(cell)
    cell = cells[column]
    for child in list(cell):
        cell.remove(child)
    for key in list(cell.attrib):
        if key in {
            attr("office", "value"),
            attr("office", "string-value"),
            attr("office", "boolean-value"),
            attr("office", "date-value"),
            attr("office", "time-value"),
            attr("table", "formula"),
        }:
            del cell.attrib[key]
    if value is None:
        text = ""
    elif isinstance(value, bool):
        text = str(value).lower()
    elif isinstance(value, float) and value.is_integer():
        text = str(int(value))
    else:
        text = str(value)
    cell.set(attr("office", "value-type"), "string")
    paragraph = ET.SubElement(cell, attr("text", "p"))
    paragraph.text = text


def expected_stats_row(civ: dict[str, object], category: str) -> list[object]:
    record = civ["ratings"][category]  # type: ignore[index]
    stat = record.get("statistics", {})
    return [
        civ["civilization"], civ["host_civilization"], category, record["rating"],
        record.get("unit_name", ""), record.get("unit_id", ""), stat.get("hp", ""),
        stat.get("attack", ""), stat.get("bonus_damage_total", ""), stat.get("melee_armor", ""),
        stat.get("pierce_armor", ""), stat.get("range", ""), stat.get("minimum_range", ""),
        stat.get("speed", ""), stat.get("reload_time", ""), stat.get("accuracy", ""),
        stat.get("food_cost", ""), stat.get("wood_cost", ""), stat.get("gold_cost", ""),
        stat.get("stone_cost", ""), stat.get("population", ""), stat.get("train_time", ""),
        record.get("combat_ratio", ""), record.get("number_multiplier", ""),
        record.get("number_adjusted_ratio", ""),
        ", ".join(map(str, record.get("missing_standard_tech_ids", []))),
        record.get("full_standard_upgrades", ""), record.get("has_parthian_tactics", ""),
        record.get("compatible_package_count", ""), stat.get("blast_width", ""),
        stat.get("attack_delay_frames", ""), stat.get("friendly_fire_damage", ""), record["reason"],
    ]


def sync_content(content: bytes, document: dict[str, object]) -> bytes:
    register_namespaces(content)
    root = ET.fromstring(content)
    tables = {
        table.get(attr("table", "name"), ""): table
        for table in root.findall(".//table:table", NS)
    }
    for required in ("Sheet1", "Methodology", "Final stats"):
        if required not in tables:
            raise ValueError(f"Workbook is missing {required}")

    order = document["display_order"]  # type: ignore[index]
    civilizations = document["civilizations"]  # type: ignore[index]
    matrix = [list(HEADERS)]
    for key in order:
        civ = civilizations[key]
        matrix.append(
            [
                civ["civilization"],
                civ["host_civilization"],
                *[civ["ratings"][category]["rating"] for category in EXPECTED_CATEGORIES],
                civ["unique_unit_type"],
            ]
        )
    sheet_rows = tables["Sheet1"].findall("table:table-row", NS)
    for row, values in zip(sheet_rows[: len(matrix)], matrix, strict=True):
        for column, value in enumerate(values):
            set_cell(row, column, value)

    method_rows = tables["Methodology"].findall("table:table-row", NS)
    for row in method_rows:
        cells = expanded_cells(row, 2)
        if cells and cell_text(cells[0]) == "Priests / Navy":
            set_cell(row, 1, document["rubric"]["priests_and_navy"])  # type: ignore[index]
        if cells and cell_text(cells[0]) == "Technology branches":
            set_cell(
                row,
                1,
                document["score_model"]["doctrine_packages"]  # type: ignore[index]
                + " "
                + document["score_model"]["naval_package"],  # type: ignore[index]
            )

    stats_matrix = [list(STATS_HEADERS)]
    for key in order:
        civ = civilizations[key]
        for category in EXPECTED_CATEGORIES:
            stats_matrix.append(expected_stats_row(civ, category))
    stats_rows = tables["Final stats"].findall("table:table-row", NS)
    for row, values in zip(stats_rows[: len(stats_matrix)], stats_matrix, strict=True):
        for column, value in enumerate(values):
            set_cell(row, column, value)

    # Rebuild a dedicated, exact-mapping naval sheet from the existing styled
    # Final stats table so every class score and role flag remains auditable.
    template = tables["Final stats"]
    header_template = copy.deepcopy(stats_rows[0])
    data_template = copy.deepcopy(stats_rows[1])
    naval_table = copy.deepcopy(template)
    naval_table.set(attr("table", "name"), "Naval capability")
    for row in naval_table.findall("table:table-row", NS):
        naval_table.remove(row)

    naval_rows: list[list[object]] = [list(NAVAL_HEADERS)]
    for key in order:
        civ = civilizations[key]
        navy = civ["ratings"]["Navy"]
        for class_name, record in navy["ship_classes"].items():
            naval_rows.append(
                [
                    civ["civilization"],
                    "Yes" if navy["primary_navy_doctrine"] else "No",
                    navy["capability_score"],
                    navy["steady_state_capability_score"],
                    navy["rating"],
                    navy["lineup_completeness_score"],
                    navy["ship_class_quality_score"],
                    navy["support_upgrade_score"],
                    navy["production_throughput_adjustment"],
                    navy["fleet_throughput_multiplier"],
                    navy["shipyard_work_rate"],
                    class_name,
                    record["available"],
                    record.get("unit_name", ""),
                    record.get("unit_id", ""),
                    record.get("tier_multiplier", ""),
                    record.get("lineup_points", ""),
                    record.get("quality_points", ""),
                    record.get("combat_ratio", ""),
                    record.get("number_multiplier", ""),
                    record.get("number_adjusted_ratio", ""),
                    record.get("throughput_multiplier", ""),
                    record.get("production_source", ""),
                    record.get("production_work_rate", ""),
                    record.get("production_batch_size", ""),
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
                    navy["has_quadrireme_or_quinquereme"],
                    navy["has_octeres"],
                    navy["specialist_support_detachment"],
                ]
            )
    for index, values in enumerate(naval_rows):
        row = copy.deepcopy(header_template if index == 0 else data_template)
        for column, value in enumerate(values):
            set_cell(row, column, value)
        naval_table.append(row)

    spreadsheet = root.find(".//office:spreadsheet", NS)
    if spreadsheet is None:
        raise ValueError("Workbook has no spreadsheet body")
    existing_naval = tables.get("Naval capability")
    if existing_naval is not None:
        spreadsheet.remove(existing_naval)
    spreadsheet.append(naval_table)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def sync_meta(meta: bytes) -> bytes:
    register_namespaces(meta)
    root = ET.fromstring(meta)
    statistic = root.find(".//meta:document-statistic", NS)
    if statistic is not None:
        statistic.set(attr("meta", "table-count"), "4")
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def write_ods(path: Path, content: bytes, meta: bytes) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    with zipfile.ZipFile(path, "r") as source, zipfile.ZipFile(temporary, "w") as target:
        for info in source.infolist():
            payload = source.read(info.filename)
            if info.filename == "content.xml":
                payload = content
            elif info.filename == "meta.xml":
                payload = meta
            target.writestr(info, payload)
    temporary.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("workbook", nargs="?", type=Path, default=ROOT / "RAW AI good units per civ.ods")
    parser.add_argument("--evaluations", type=Path, default=ROOT / "good-unit-evaluations.json")
    args = parser.parse_args()
    document = json.loads(args.evaluations.read_text(encoding="utf-8-sig"))
    with zipfile.ZipFile(args.workbook, "r") as archive:
        content = sync_content(archive.read("content.xml"), document)
        meta = sync_meta(archive.read("meta.xml"))
    write_ods(args.workbook, content, meta)
    print(f"Synchronized ODS ratings, final statistics, and naval capability evidence: {args.workbook}")


if __name__ == "__main__":
    main()
