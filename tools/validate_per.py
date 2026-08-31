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

# The AoE II AI runtime exposes timer slots 1 through 50. Defining a symbolic
# timer outside this range parses, but its controller cannot be trusted at
# runtime; sharing one slot between two owners creates the same class of race.
MIN_TIMER_ID = 1
MAX_TIMER_ID = 50

# DE extends the UserPatch table to 0..19 (AIRef GroupId and
# up-modify-group-flag parameter table, archived 2026-08-30).
MIN_DUC_GROUP_ID = 0
MAX_DUC_GROUP_ID = 19

# These DUC commands mutate search state and are only valid on the action side
# of a rule. AoE reports ERR2005 when one is accidentally used as a fact.
ACTION_ONLY_RULE_COMMANDS = {
    "up-add-object-by-id",
    "up-full-reset-search",
}

# PER logical operators have fixed arity. In particular, `or` and `and` are
# binary; additional alternatives must be expressed with nested operators.
LOGICAL_OPERATOR_ARITY = {
    "and": 2,
    "nor": 2,
    "not": 1,
    "or": 2,
}


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


def constants_with_prefix(prefix: str) -> frozenset[str]:
    """Collect engine-domain constants from the project's audited table."""
    path = ROOT / "rawai-constants.per"
    if not path.is_file():
        return frozenset()
    text = "\n".join(
        code_without_comments_or_strings(line)
        for line in path.read_text(encoding="utf-8-sig").splitlines()
    )
    return frozenset(
        name.casefold()
        for name in re.findall(
            rf"\(defconst\s+({re.escape(prefix)}[a-z0-9-]+)\s+[-0-9]+\s*\)",
            text,
            re.IGNORECASE,
        )
    )


def constant_values_with_prefix(prefix: str) -> frozenset[int]:
    """Collect the numeric values in one audited engine-constant domain."""
    path = ROOT / "rawai-constants.per"
    if not path.is_file():
        return frozenset()
    text = "\n".join(
        code_without_comments_or_strings(line)
        for line in path.read_text(encoding="utf-8-sig").splitlines()
    )
    return frozenset(
        int(value)
        for value in re.findall(
            rf"\(defconst\s+{re.escape(prefix)}[a-z0-9-]+\s+(-?\d+)\s*\)",
            text,
            re.IGNORECASE,
        )
    )


def project_defconsts() -> frozenset[str]:
    """Collect every goal/domain identifier declared by the AI payload."""
    names: set[str] = set()
    for path in ROOT.glob("*.per"):
        text = "\n".join(
            code_without_comments_or_strings(line)
            for line in path.read_text(encoding="utf-8-sig").splitlines()
        )
        names.update(
            name.casefold()
            for name in re.findall(r"\(defconst\s+([^\s()]+)", text)
        )
    return frozenset(names)


def project_defconst_values() -> dict[str, int]:
    """Collect numeric project constants for cross-file operand validation."""
    values: dict[str, int] = {}
    for path in ROOT.glob("*.per"):
        text = "\n".join(
            code_without_comments_or_strings(line)
            for line in path.read_text(encoding="utf-8-sig").splitlines()
        )
        for name, value in re.findall(
            r"\(defconst\s+([^\s()]+)\s+(-?\d+)\s*\)", text
        ):
            values.setdefault(name.casefold(), int(value))
    return values


def validate_timer_sources(
    sources: dict[str, str],
) -> dict[str, list[dict[str, object]]]:
    """Require timer constants in named PER sources to use unique valid slots."""
    report: dict[str, list[dict[str, object]]] = {}
    timer_slots: dict[int, tuple[str, str, int]] = {}
    timer_pattern = re.compile(
        r"^\s*\(defconst\s+(?P<name>t-[^\s()]+)\s+(?P<value>-?\d+)\s*\)",
        re.IGNORECASE,
    )
    for filename, source in sources.items():
        for line_number, raw_line in enumerate(source.splitlines(), 1):
            line = code_without_comments_or_strings(raw_line)
            match = timer_pattern.match(line)
            if match is None:
                continue
            name = match.group("name")
            value = int(match.group("value"))
            if not MIN_TIMER_ID <= value <= MAX_TIMER_ID:
                report.setdefault(filename, []).append(
                    {
                        "kind": "timer_id_out_of_range",
                        "name": name,
                        "value": value,
                        "line": line_number,
                        "minimum": MIN_TIMER_ID,
                        "maximum": MAX_TIMER_ID,
                    }
                )
            if value in timer_slots:
                first_name, first_file, first_line = timer_slots[value]
                report.setdefault(filename, []).append(
                    {
                        "kind": "duplicate_timer_id",
                        "name": name,
                        "value": value,
                        "line": line_number,
                        "first_name": first_name,
                        "first_file": first_file,
                        "first_line": first_line,
                    }
                )
            else:
                timer_slots[value] = (name, filename, line_number)
    return report


def validate_timer_definitions(
    paths: list[Path],
) -> dict[str, list[dict[str, object]]]:
    """Read project PER files and validate their engine timer definitions."""
    return validate_timer_sources(
        {
            path.name: path.read_text(encoding="utf-8-sig")
            for path in paths
        }
    )


TARGET_ACTION_CONSTANTS = constants_with_prefix("action-")
TARGET_ACTION_VALUES = constant_values_with_prefix("action-")
POSITION_SOURCE_CONSTANTS = constants_with_prefix("position-")
ACTION_ID_CONSTANTS = constants_with_prefix("actionid-")
ORDER_ID_CONSTANTS = constants_with_prefix("orderid-")
PROJECT_DEFCONSTS = project_defconsts()
PROJECT_DEFCONST_VALUES = project_defconst_values()


def defrule_blocks(lines: list[str]) -> list[tuple[int, str]]:
    """Return balanced, comment-free defrule blocks with start line numbers."""
    text = "\n".join(code_without_comments_or_strings(line) for line in lines)
    blocks: list[tuple[int, str]] = []
    search_from = 0
    while match := re.search(r"\(defrule\b", text[search_from:]):
        start = search_from + match.start()
        depth = 0
        end = start
        for end in range(start, len(text)):
            if text[end] == "(":
                depth += 1
            elif text[end] == ")":
                depth -= 1
                if depth == 0:
                    end += 1
                    break
        else:
            break
        start_line = text.count("\n", 0, start) + 1
        blocks.append((start_line, text[start:end]))
        search_from = end
    return blocks


def validate_command_domains(lines: list[str]) -> list[dict[str, object]]:
    """Catch technology/unit operand swaps and guarded research mismatches."""
    issues: list[dict[str, object]] = []
    code = "\n".join(code_without_comments_or_strings(line) for line in lines)

    # Resolve both repository-wide constants and constants declared by an
    # isolated test fixture, then enforce the engine's 0..9 DUC group domain.
    constant_values = dict(PROJECT_DEFCONST_VALUES)
    constant_values.update(
        {
            name.casefold(): int(value)
            for name, value in re.findall(
                r"\(defconst\s+([^\s()]+)\s+(-?\d+)\s*\)", code
            )
        }
    )
    group_operand_patterns = (
        re.compile(
            r"\(up-create-group\s+\S+\s+\S+\s+c:\s*(?P<group>[^\s)]+)",
            re.IGNORECASE,
        ),
        re.compile(
            r"\(up-set-group\s+\S+\s+c:\s*(?P<group>[^\s)]+)",
            re.IGNORECASE,
        ),
        re.compile(
            r"\(up-reset-group\s+c:\s*(?P<group>[^\s)]+)",
            re.IGNORECASE,
        ),
        re.compile(
            r"\(up-modify-group-flag\s+\S+\s+c:\s*(?P<group>[^\s)]+)",
            re.IGNORECASE,
        ),
        re.compile(
            r"\(up-group-size\s+c:\s*(?P<group>[^\s)]+)",
            re.IGNORECASE,
        ),
    )
    for pattern in group_operand_patterns:
        for match in pattern.finditer(code):
            operand = match.group("group")
            value = (
                int(operand)
                if re.fullmatch(r"-?\d+", operand)
                else constant_values.get(operand.casefold())
            )
            line = code.count("\n", 0, match.start("group")) + 1
            if value is None:
                issues.append(
                    {
                        "kind": "unknown_duc_group_identifier",
                        "identifier": operand,
                        "line": line,
                    }
                )
            elif not MIN_DUC_GROUP_ID <= value <= MAX_DUC_GROUP_ID:
                issues.append(
                    {
                        "kind": "duc_group_id_out_of_range",
                        "identifier": operand,
                        "value": value,
                        "line": line,
                        "minimum": MIN_DUC_GROUP_ID,
                        "maximum": MAX_DUC_GROUP_ID,
                    }
                )

    # ActionId and OrderId are separate engine domains from TargetAction. A
    # plausible invented name (for example actionid-guard) produces ERR2005
    # even though the corresponding TargetAction action-guard is valid.
    for prefix, known, kind in (
        ("actionid-", ACTION_ID_CONSTANTS, "undefined_action_id_constant"),
        ("orderid-", ORDER_ID_CONSTANTS, "undefined_order_id_constant"),
    ):
        for match in re.finditer(
            rf"\b(?P<identifier>{re.escape(prefix)}[a-z0-9-]+)\b",
            code,
            re.IGNORECASE,
        ):
            identifier = match.group("identifier")
            if identifier.casefold() not in known:
                issues.append(
                    {
                        "kind": kind,
                        "identifier": identifier,
                        "line": code.count("\n", 0, match.start()) + 1,
                    }
                )
    invalid_compare_assignment = re.compile(
        r"\((?P<command>up-compare-goal|up-compare-sn)\s+[^\s)]+\s+"
        r"(?P<operator>[cgs]:=)(?=\s)",
        re.IGNORECASE,
    )
    for match in invalid_compare_assignment.finditer(code):
        issues.append(
            {
                "kind": "assignment_operator_in_comparison",
                "command": match.group("command"),
                "operator": match.group("operator"),
                "line": code.count("\n", 0, match.start()) + 1,
            }
        )

    invalid_goal_comparison = re.compile(
        r"\(goal\s+[^\s)]+\s+(?P<operator><=|>=|==|!=|<|>)\s+",
        re.IGNORECASE,
    )
    for match in invalid_goal_comparison.finditer(code):
        issues.append(
            {
                "kind": "comparison_operator_in_goal_fact",
                "operator": match.group("operator"),
                "line": code.count("\n", 0, match.start()) + 1,
            }
        )

    # up-get-search-state writes four consecutive outputs beginning at its
    # operand: local total, local last-added, remote total, remote last-added.
    # The project's audited four-goal block begins at local-total. Passing
    # remote-total instead shifts every value and overwrites the following goal.
    search_state_operand = re.compile(
        r"\(up-get-search-state\s+(?P<operand>[^\s)]+)\s*\)",
        re.IGNORECASE,
    )
    for match in search_state_operand.finditer(code):
        if match.group("operand").casefold() != "local-total":
            issues.append(
                {
                    "kind": "invalid_search_state_output_base",
                    "operand": match.group("operand"),
                    "expected": "local-total",
                    "line": code.count("\n", 0, match.start()) + 1,
                }
            )

    # set-goal treats its second operand as a literal. A gl-* token is the
    # numeric identifier of another goal, not that goal's stored value; use
    # up-modify-goal with a g:= operand when copying between goals.
    literal_goal_copy = re.compile(
        r"\(set-goal\s+(?P<destination>[^\s)]+)\s+"
        r"(?P<source>gl-[^\s)]+)\s*\)",
        re.IGNORECASE,
    )
    for match in literal_goal_copy.finditer(code):
        issues.append(
            {
                "kind": "goal_identifier_stored_as_value",
                "destination": match.group("destination"),
                "source": match.group("source"),
                "line": code.count("\n", 0, match.start()) + 1,
            }
        )

    # position-focus and position-object are point *sources*. They never expose
    # synthetic -x/-y goal aliases, regardless of the command consuming them.
    invalid_position_alias = re.compile(
        r"\b(?P<identifier>position-(?:focus|object)-[xy])\b",
        re.IGNORECASE,
    )
    for match in invalid_position_alias.finditer(code):
        issues.append(
            {
                "kind": "invalid_position_point_identifier",
                "identifier": match.group("identifier"),
                "line": code.count("\n", 0, match.start()) + 1,
            }
        )

    # up-target-* takes a TargetAction as its second operand. Unknown action-*
    # names parse as ERR2005; validate only this operand rather than rejecting
    # similarly named state constants elsewhere in the AI.
    target_command = re.compile(
        r"\((?P<command>up-target-(?:point|objects))\s+"
        r"(?P<target>[^\s()]+)\s+(?P<action>[^\s()]+)",
        re.IGNORECASE,
    )
    for match in target_command.finditer(code):
        action = match.group("action")
        numeric_action = re.fullmatch(r"-?\d+", action)
        if (
            numeric_action is not None
            and int(action) not in TARGET_ACTION_VALUES
        ) or (
            numeric_action is None
            and action.casefold() not in TARGET_ACTION_CONSTANTS
        ):
            issues.append(
                {
                    "kind": "invalid_target_action_identifier",
                    "command": match.group("command"),
                    "identifier": action,
                    "line": code.count("\n", 0, match.start("action")) + 1,
                }
            )
        target = match.group("target")
        if (
            match.group("command").casefold() == "up-target-point"
            and target.casefold() in POSITION_SOURCE_CONSTANTS
        ):
            issues.append(
                {
                    "kind": "position_source_used_as_target_point",
                    "command": match.group("command"),
                    "identifier": target,
                    "line": code.count("\n", 0, match.start("target")) + 1,
                }
            )
        elif (
            match.group("command").casefold() == "up-target-point"
            and not re.fullmatch(r"-?\d+", target)
            and target.casefold() not in PROJECT_DEFCONSTS
        ):
            issues.append(
                {
                    "kind": "invalid_target_point_identifier",
                    "command": match.group("command"),
                    "identifier": target,
                    "line": code.count("\n", 0, match.start("target")) + 1,
                }
            )

    technology_training_patterns = (
        re.compile(
            r"\((?P<command>can-train(?:-with-escrow)?|train)\s+"
            r"(?P<name>(?:ut|ri)-[^\s)]+)",
            re.IGNORECASE,
        ),
        re.compile(
            r"\((?P<command>up-can-train|up-train)\s+\S+\s+c:\s*"
            r"(?P<name>(?:ut|ri)-[^\s)]+)",
            re.IGNORECASE,
        ),
    )
    for pattern in technology_training_patterns:
        for match in pattern.finditer(code):
            issues.append(
                {
                    "kind": "technology_used_as_training_operand",
                    "command": match.group("command"),
                    "name": match.group("name"),
                    "line": code.count("\n", 0, match.start()) + 1,
                }
            )

    guard_patterns = (
        re.compile(
            r"\(can-research(?:-with-escrow)?\s+(?P<name>[^\s)]+)",
            re.IGNORECASE,
        ),
        re.compile(
            r"\(up-can-research\s+\S+\s+c:\s*(?P<name>[^\s)]+)",
            re.IGNORECASE,
        ),
    )
    action_patterns = (
        re.compile(r"\(research\s+(?P<name>[^\s)]+)", re.IGNORECASE),
        re.compile(
            r"\(up-research\s+\S+\s+c:\s*(?P<name>[^\s)]+)",
            re.IGNORECASE,
        ),
    )
    for start_line, block in defrule_blocks(lines):
        facts, separator, actions = block.partition("=>")
        if not separator:
            continue
        guard_matches = [
            match for pattern in guard_patterns for match in pattern.finditer(facts)
        ]
        guards = {
            match.group("name").casefold(): match.group("name")
            for match in guard_matches
        }
        if not guards:
            continue
        action_matches = [
            match for pattern in action_patterns for match in pattern.finditer(actions)
        ]
        action_names = {
            match.group("name").casefold(): match.group("name")
            for match in action_matches
        }
        if len(guards) > 1:
            first_action = action_matches[0] if action_matches else None
            action_line = start_line + facts.count("\n")
            if first_action:
                action_line += actions.count("\n", 0, first_action.start())
            issues.append(
                {
                    "kind": "ambiguous_multiple_research_guards",
                    "guards": sorted(guards.values(), key=str.casefold),
                    "actions": sorted(action_names.values(), key=str.casefold),
                    "line": action_line,
                }
            )
        for action in action_matches:
            technology = action.group("name")
            if technology.casefold() not in guards:
                action_line = (
                    start_line
                    + facts.count("\n")
                    + actions.count("\n", 0, action.start())
                )
                issues.append(
                    {
                        "kind": "research_guard_action_mismatch",
                        "guards": sorted(guards.values(), key=str.casefold),
                        "action": technology,
                        "line": action_line,
                    }
                )
    return issues


def validate_file(path: Path) -> list[dict[str, object]]:
    issues: list[dict[str, object]] = []
    parenthesis_stack: list[tuple[int, int]] = []
    expression_stack: list[dict[str, object]] = []
    preprocessor_stack: list[tuple[int, str, bool]] = []
    defconst_lines: dict[str, int] = {}
    rule_depth: int | None = None
    rule_start_line = 0
    rule_element_count = 0
    rule_in_actions = False

    raw_lines = path.read_text(encoding="utf-8-sig").splitlines()
    for line_number, raw_line in enumerate(raw_lines, 1):
        line = code_without_comments_or_strings(raw_line)
        for column, char in enumerate(line, 1):
            if char == "(":
                keyword_match = re.match(r"\s*([^\s()]+)", line[column:])
                keyword = keyword_match.group(1) if keyword_match else ""
                if expression_stack:
                    parent = expression_stack[-1]
                    if parent["keyword"] in LOGICAL_OPERATOR_ARITY:
                        parent["children"] = int(parent["children"]) + 1
                expression_stack.append(
                    {
                        "keyword": keyword,
                        "children": 0,
                        "line": line_number,
                    }
                )
                parenthesis_stack.append((line_number, column))
                current_depth = len(parenthesis_stack)
                if rule_depth is None and keyword == "defrule":
                    rule_depth = current_depth
                    rule_start_line = line_number
                    rule_element_count = 0
                    rule_in_actions = False
                elif rule_depth is not None and current_depth > rule_depth:
                    rule_element_count += 1
                    if not rule_in_actions and keyword in ACTION_ONLY_RULE_COMMANDS:
                        issues.append(
                            {
                                "kind": "action_used_as_fact",
                                "name": keyword,
                                "line": line_number,
                            }
                        )
            elif char == ")":
                if parenthesis_stack:
                    expression = expression_stack.pop()
                    logical_keyword = str(expression["keyword"])
                    expected_arity = LOGICAL_OPERATOR_ARITY.get(logical_keyword)
                    if (
                        expected_arity is not None
                        and int(expression["children"]) != expected_arity
                    ):
                        issues.append(
                            {
                                "kind": "logical_operator_arity",
                                "name": logical_keyword,
                                "line": int(expression["line"]),
                                "operands": int(expression["children"]),
                                "expected": expected_arity,
                            }
                        )
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
                        rule_in_actions = False
                    parenthesis_stack.pop()
                else:
                    issues.append(
                        {
                            "kind": "unmatched_closing_parenthesis",
                            "line": line_number,
                            "column": column,
                        }
                    )

        if rule_depth is not None and "=>" in line:
            rule_in_actions = True

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
    issues.extend(validate_command_domains(raw_lines))
    return issues


def main() -> None:
    report: dict[str, list[dict[str, object]]] = {}
    paths = sorted(ROOT.glob("*.per"))
    for path in paths:
        issues = validate_file(path)
        if issues:
            report[path.name] = issues

    for filename, issues in validate_timer_definitions(paths).items():
        report.setdefault(filename, []).extend(issues)

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
