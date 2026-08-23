#!/usr/bin/env python3
"""Lightweight structural validator for AoE II PER scripts."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NESTED_AI_ROOT = ROOT / "Rome-at-War-AI-main"
if NESTED_AI_ROOT.is_dir():
    ROOT = NESTED_AI_ROOT

# Research constants supplied by the AoE II AI scripting runtime rather than by
# this project. Keeping the allow-list explicit lets the validator still catch
# typos in Rome at War's custom technology constants.
ENGINE_RESEARCH_CONSTANTS = {
    "ri-architecture",
    "ri-bow-saw",
    "ri-deck-guns",
    "ri-dry-dock",
    "ri-elite-armored-elephant",
    "ri-elite-eagle-warrior",
    "ri-man-at-arms",
    "ri-pikeman",
    "ri-stonecutting",
    "ri-wheel-barrow",
}

# Definitive Edition accepts at most 32 facts, actions, and logical operators
# inside one defrule. Each parenthesized expression below the defrule itself is
# one element for this limit.
MAX_RULE_ELEMENTS = 32


def code_without_comments_or_strings(line: str) -> str:
    result = []
    in_string = False
    escaped = False
    for char in line:
        if escaped:
            escaped = False
            if not in_string:
                result.append(" ")
            continue
        if char == "\\" and in_string:
            escaped = True
            continue
        if char == '"':
            in_string = not in_string
            result.append(" ")
            continue
        if char == ";" and not in_string:
            break
        result.append(" " if in_string else char)
    return "".join(result)


def validate_file(path: Path) -> list[dict[str, object]]:
    issues: list[dict[str, object]] = []
    parenthesis_stack: list[tuple[int, int]] = []
    preprocessor_stack: list[tuple[int, str, bool]] = []
    defconst_lines: dict[str, int] = {}
    rule_depth: int | None = None
    rule_start_line = 0
    rule_element_count = 0

    for line_number, raw_line in enumerate(
        path.read_text(encoding="utf-8-sig").splitlines(), 1
    ):
        line = code_without_comments_or_strings(raw_line)
        for column, char in enumerate(line, 1):
            if char == "(":
                parenthesis_stack.append((line_number, column))
                keyword_match = re.match(r"\s*([^\s()]+)", line[column:])
                keyword = keyword_match.group(1) if keyword_match else ""
                current_depth = len(parenthesis_stack)
                if rule_depth is None and keyword == "defrule":
                    rule_depth = current_depth
                    rule_start_line = line_number
                    rule_element_count = 0
                elif rule_depth is not None and current_depth > rule_depth:
                    rule_element_count += 1
            elif char == ")":
                if parenthesis_stack:
                    if rule_depth is not None and len(parenthesis_stack) == rule_depth:
                        if rule_element_count > MAX_RULE_ELEMENTS:
                            issues.append(
                                {
                                    "kind": "rule_too_long",
                                    "line": rule_start_line,
                                    "elements": rule_element_count,
                                    "maximum": MAX_RULE_ELEMENTS,
                                }
                            )
                        rule_depth = None
                        rule_start_line = 0
                        rule_element_count = 0
                    parenthesis_stack.pop()
                else:
                    issues.append(
                        {
                            "kind": "unmatched_closing_parenthesis",
                            "line": line_number,
                            "column": column,
                        }
                    )

        directive_parts = line.strip().split(maxsplit=1) if line.strip() else []
        directive = directive_parts[0] if directive_parts else ""
        if directive in {"#load-if-defined", "#load-if-not-defined"}:
            symbol = directive_parts[1].strip() if len(directive_parts) == 2 else ""
            is_defined = directive == "#load-if-defined"
            if is_defined and symbol.startswith("DIFFICULTY-"):
                for previous_line, previous_symbol, previous_defined in preprocessor_stack:
                    if (
                        previous_defined
                        and previous_symbol.startswith("DIFFICULTY-")
                        and previous_symbol != symbol
                    ):
                        issues.append(
                            {
                                "kind": "mutually_exclusive_difficulty_conditions",
                                "line": line_number,
                                "symbol": symbol,
                                "outer_line": previous_line,
                                "outer_symbol": previous_symbol,
                            }
                        )
            preprocessor_stack.append((line_number, symbol, is_defined))
        elif directive == "#end-if":
            if preprocessor_stack:
                preprocessor_stack.pop()
            else:
                issues.append({"kind": "unmatched_end_if", "line": line_number})

        match = re.match(r"^\s*\(defconst\s+([^\s)]+)", line)
        if match:
            name = match.group(1)
            if name in defconst_lines:
                issues.append(
                    {
                        "kind": "duplicate_defconst",
                        "name": name,
                        "line": line_number,
                        "first_line": defconst_lines[name],
                    }
                )
            else:
                defconst_lines[name] = line_number

    for line_number, column in parenthesis_stack:
        issues.append(
            {
                "kind": "unclosed_parenthesis",
                "line": line_number,
                "column": column,
            }
        )
    for line_number, _symbol, _is_defined in preprocessor_stack:
        issues.append({"kind": "unclosed_load_if", "line": line_number})
    return issues


def main() -> None:
    report: dict[str, list[dict[str, object]]] = {}
    paths = sorted(ROOT.glob("*.per"))
    for path in paths:
        issues = validate_file(path)
        if issues:
            report[path.name] = issues

    all_defconsts: set[str] = set()
    for path in paths:
        text = "\n".join(
            code_without_comments_or_strings(line)
            for line in path.read_text(encoding="utf-8-sig").splitlines()
        )
        all_defconsts.update(re.findall(r"\(defconst\s+([^\s)]+)", text))

    prefixed_reference = re.compile(r"\b(?:ri|ut)-[a-z0-9-]+\b", re.IGNORECASE)
    for path in paths:
        for line_number, raw_line in enumerate(
            path.read_text(encoding="utf-8-sig").splitlines(), 1
        ):
            line = code_without_comments_or_strings(raw_line)
            for name in prefixed_reference.findall(line):
                if name not in all_defconsts and name not in ENGINE_RESEARCH_CONSTANTS:
                    report.setdefault(path.name, []).append(
                        {
                            "kind": "undefined_research_constant",
                            "name": name,
                            "line": line_number,
                        }
                    )
            load_match = re.match(r'^\s*\(load\s+"([^"]+)"\s*\)', line)
            if load_match:
                loaded_path = ROOT / f"{load_match.group(1)}.per"
                if not loaded_path.is_file():
                    report.setdefault(path.name, []).append(
                        {
                            "kind": "missing_loaded_file",
                            "name": load_match.group(1),
                            "line": line_number,
                        }
                    )
    print(json.dumps(report, indent=2))
    if report:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
