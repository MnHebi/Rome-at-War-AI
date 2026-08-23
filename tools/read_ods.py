#!/usr/bin/env python3
"""Print compact JSON summaries of OpenDocument spreadsheets.

This is deliberately read-only. It expands repeated ODS rows and columns so the
two planning workbooks can be audited without depending on a desktop office
suite.
"""

from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


NS = {
    "office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
    "table": "urn:oasis:names:tc:opendocument:xmlns:table:1.0",
    "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
}


def attr(namespace: str, name: str) -> str:
    return f"{{{NS[namespace]}}}{name}"


def cell_text(cell: ET.Element) -> str:
    paragraphs = []
    for paragraph in cell.findall("text:p", NS):
        paragraphs.append("".join(paragraph.itertext()))
    text = "\n".join(paragraphs)
    if text:
        return text

    value_type = cell.get(attr("office", "value-type"))
    value_attrs = {
        "float": "value",
        "percentage": "value",
        "currency": "value",
        "boolean": "boolean-value",
        "date": "date-value",
        "time": "time-value",
        "string": "string-value",
    }
    value_attr = value_attrs.get(value_type or "")
    return cell.get(attr("office", value_attr), "") if value_attr else ""


def read_sheets(path: Path) -> list[dict[str, object]]:
    with zipfile.ZipFile(path) as archive:
        root = ET.fromstring(archive.read("content.xml"))

    sheets: list[dict[str, object]] = []
    for table in root.findall(".//table:table", NS):
        rows: list[list[str]] = []
        for row in table.findall("table:table-row", NS):
            row_repeat = int(row.get(attr("table", "number-rows-repeated"), "1"))
            values: list[str] = []
            for cell in row:
                if cell.tag not in {
                    attr("table", "table-cell"),
                    attr("table", "covered-table-cell"),
                }:
                    continue
                col_repeat = int(
                    cell.get(attr("table", "number-columns-repeated"), "1")
                )
                value = cell_text(cell)
                # ODS files often encode thousands of trailing blank cells as a
                # repeated cell. Preserve meaningful repeats, cap blank padding.
                if not value and col_repeat > 256:
                    col_repeat = 1
                values.extend([value] * col_repeat)

            while values and values[-1] == "":
                values.pop()
            if not values and row_repeat > 256:
                row_repeat = 1
            rows.extend([values.copy() for _ in range(row_repeat)])

        while rows and not rows[-1]:
            rows.pop()
        sheets.append(
            {
                "name": table.get(attr("table", "name"), ""),
                "row_count": len(rows),
                "column_count": max((len(row) for row in rows), default=0),
                "rows": rows,
            }
        )
    return sheets


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--max-rows", type=int, default=200)
    args = parser.parse_args()

    result = []
    for path in args.paths:
        sheets = read_sheets(path)
        for sheet in sheets:
            sheet["rows"] = sheet["rows"][: args.max_rows]
        result.append({"path": str(path), "sheets": sheets})
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
