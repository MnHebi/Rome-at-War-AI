#!/usr/bin/env python3
"""Semantic invariants for match-relative naval capability and production."""

from __future__ import annotations

import json
import re
from pathlib import Path

from sync_naval_capabilities import (
    RUNTIME_SCORE_SCALE,
    compact_scores,
    competitive_enemy_ceiling,
    render,
    runtime_score,
)


ROOT = Path(__file__).resolve().parents[1]


def rule_blocks(text: str) -> list[tuple[int, int, str, str, str]]:
    """Return balanced defrules with their facts/actions and source offsets."""
    def uncommented(line: str) -> str:
        quoted = False
        escaped = False
        for index, character in enumerate(line):
            if character == '"' and not escaped:
                quoted = not quoted
            elif character == ";" and not quoted:
                return line[:index]
            escaped = character == "\\" and not escaped
            if character != "\\":
                escaped = False
        return line

    blocks: list[tuple[int, int, str, str, str]] = []
    offset = 0
    start = -1
    depth = 0
    lines: list[str] = []
    code_lines: list[str] = []
    for raw_line in text.splitlines(keepends=True):
        code = uncommented(raw_line)
        if start < 0 and code.strip() == "(defrule":
            start = offset
            depth = 0
            lines = []
            code_lines = []
        if start >= 0:
            lines.append(raw_line)
            code_lines.append(code)
            depth += code.count("(") - code.count(")")
            if depth == 0:
                block = "".join(lines)
                code_block = "".join(code_lines)
                if "=>" not in code_block:
                    raise ValueError(f"defrule at offset {start} has no action separator")
                facts, actions = code_block.split("=>", 1)
                blocks.append((start, offset + len(raw_line), block, facts, actions))
                start = -1
                lines = []
                code_lines = []
        offset += len(raw_line)
    if start >= 0:
        raise ValueError(f"unterminated defrule at offset {start}")
    return blocks


def matching_rules(
    text: str,
    *,
    facts: tuple[str, ...] = (),
    actions: tuple[str, ...] = (),
) -> list[tuple[int, int, str, str, str]]:
    return [
        block
        for block in rule_blocks(text)
        if all(token in block[3] for token in facts)
        and all(token in block[4] for token in actions)
    ]


def main() -> None:
    evaluations = json.loads((ROOT / "good-unit-evaluations.json").read_text(encoding="utf-8-sig"))
    scores = json.loads((ROOT / "naval-capability-scores.json").read_text(encoding="utf-8-sig"))
    doctrine = (ROOT / "rawai-naval-doctrine.per").read_text(encoding="utf-8-sig")
    issues: list[str] = []

    if scores != compact_scores(evaluations):
        issues.append("naval-capability-scores.json is stale")
    if doctrine != render(evaluations):
        issues.append("rawai-naval-doctrine.per is stale")
    if len(scores.get("civilizations", {})) != 34:
        issues.append("compact naval score table must contain 34 civilizations")

    civs = scores.get("civilizations", {})
    rome = civs.get("romeemp", {})
    britons = civs.get("britons", {})
    if not (rome.get("capability_score", 0) > britons.get("capability_score", 100)):
        issues.append("Roman Empire must data-score above Britons in the validated DAT")
    if rome.get("primary_navy_doctrine") or britons.get("primary_navy_doctrine"):
        issues.append("Rome-vs-Britons all-No calibration no longer matches AI RAW.per")
    if sum(bool(record.get("primary_navy_doctrine")) for record in civs.values()) != 10:
        issues.append("expected ten current Naval Yes doctrine civilizations")
    for key, record in civs.items():
        if record.get("runtime_score") != runtime_score(record.get("capability_score", 0.0)):
            issues.append(f"{key}: runtime score does not preserve the two-decimal capability")
        expected_ceiling = competitive_enemy_ceiling(record.get("capability_score", 0.0))
        if record.get("competitive_enemy_ceiling") != expected_ceiling:
            issues.append(f"{key}: competitive ceiling does not apply the exact 85% threshold")
        expected_specialist = bool(
            record.get("has_quadrireme_or_quinquereme") and record.get("has_octeres")
        )
        if record.get("specialist_support_detachment") is not expected_specialist:
            issues.append(f"{key}: specialist support flag disagrees with heavy-hull access")

    ai = (ROOT / "AI RAW.per").read_text(encoding="utf-8-sig")
    if scores.get("score_model", {}).get("runtime_score_scale") != RUNTIME_SCORE_SCALE:
        issues.append("compact score table does not declare the PER runtime score scale")
    if ai.count('(load "rawai-naval-doctrine")') != 1:
        issues.append("AI RAW.per must load generated naval doctrine exactly once")
    doctrine_load = ai.find('(load "rawai-naval-doctrine")')
    common_loads = [
        ai.find('(load "rawai-military-units-common")'),
        ai.find('(load "rawai-military-units-common-hard")'),
    ]
    if doctrine_load < 0 or any(position < doctrine_load for position in common_loads):
        issues.append("generated naval doctrine must load before both common production files")

    military = (ROOT / "rawai-military.per").read_text(encoding="utf-8-sig")
    warship_searches = re.findall(
        r"\(up-find-(local|remote) c: warship-class c: 40\)", military
    )
    class_aware_searches = re.findall(
        r"\(up-find-(local|remote) c: warship-class c: 40\)\s*"
        r"\(up-find-\1 c: boarding-ship c: 10\)",
        military,
    )
    if len(class_aware_searches) != len(warship_searches):
        issues.append(
            "every DUC warship search must include the DAT class-53 Boarding Ship"
        )
    if "(unit-type-count boarding-ship >= 1)" not in military:
        issues.append("Boarding-only fleets cannot activate transport escort ownership")
    if military.count("(up-object-data object-data-type == boarding-ship)") != 2:
        issues.append("enemy Boarding Ships are not classified as water threats in both response paths")
    if military.count("(up-object-data object-data-type != boarding-ship)") != 2:
        issues.append("enemy Boarding Ships can still fall through into a coastal land-threat path")

    constants = (ROOT / "rawai-customconstants.per").read_text(encoding="utf-8-sig")
    numeric_constants = re.findall(r"\(defconst\s+([^\s()]+)\s+(-?\d+)\)", constants)
    constants_by_name = {name: int(value) for name, value in numeric_constants}
    names_by_value: dict[int, list[str]] = {}
    for name, value in numeric_constants:
        names_by_value.setdefault(int(value), []).append(name)
    expected_goals = {
        "gl-own-naval-capability": 512,
        "gl-enemy-max-naval-capability": 897,
        "gl-enemy-primary-navy": 898,
        "gl-naval-role": 899,
        "gl-naval-capability-ready": 900,
        "gl-naval-fleet-cap": 901,
        "gl-naval-specialist-support": 902,
        "gl-naval-theater": 903,
        "gl-naval-specialist-fleet-cap": 904,
        "gl-naval-fleet-count-total": 905,
        "gl-naval-boarding-count-total": 906,
    }
    for name, expected_value in expected_goals.items():
        actual_value = constants_by_name.get(name)
        if actual_value != expected_value:
            issues.append(f"{name} must remain at audited goal {expected_value}, found {actual_value}")
        occupants = names_by_value.get(expected_value, [])
        if occupants != [name]:
            issues.append(
                f"goal {expected_value} must be owned only by {name}, found {occupants or 'no owner'}"
            )

    selector_start = military.find(";Keep one choice stable")
    selector_end = military.find("#load-if-not-defined DIFFICULTY-EASIEST", selector_start)
    selector = military[selector_start:selector_end]
    if selector_start < 0 or selector_end < 0:
        issues.append("cannot locate stable naval selector")
    else:
        if "good-navy" in selector:
            issues.append("stable selector still branches directly on good-navy")
        for role in ("NAVAL-ROLE-PRIMARY", "NAVAL-ROLE-COMPETITIVE", "NAVAL-ROLE-SUPPORT"):
            if role not in selector:
                issues.append(f"stable selector does not implement {role}")
    if military.count("gl-naval-role c:<= NAVAL-ROLE-COMPETITIVE") < 2:
        issues.append("support navies are not excluded from both independent naval attack executors")
    military_rules = rule_blocks(military)
    periodic_attack = military.find(";periodic attacks")
    support_zero_rules = matching_rules(
        military,
        facts=("(goal gl-naval-role NAVAL-ROLE-SUPPORT)",),
        actions=("(set-goal naval-attack-percentage 0)",),
    )
    nonzero_writers = [
        block
        for block in military_rules
        if re.search(r"\(set-goal\s+naval-attack-percentage\s+(?!0\b)[^\s()]+\)", block[4])
        and (periodic_attack < 0 or block[0] < periodic_attack)
    ]
    if len(support_zero_rules) != 1 or periodic_attack < 0 or not nonzero_writers:
        issues.append(
            "expected one SUPPORT naval-percentage suppression and identifiable superiority/periodic rules"
        )
    else:
        support_rule = support_zero_rules[0]
        if not (max(block[1] for block in nonzero_writers) <= support_rule[0] < periodic_attack):
            issues.append(
                "SUPPORT naval-percentage suppression must run after every nonzero writer and before periodic attack-now"
            )

    for filename in ("rawai-military-units-common.per", "rawai-military-units-common-hard.per"):
        text = (ROOT / filename).read_text(encoding="utf-8-sig")
        if "(warboat-count g:< gl-naval" in text:
            issues.append(f"{filename}: completed-only warboat-count remains in a fleet ceiling")
        queue_cap = "(up-compare-goal gl-naval-fleet-count-total g:< gl-naval-fleet-cap)"
        specialist_cap = "(up-compare-goal gl-naval-fleet-count-total g:< gl-naval-specialist-fleet-cap)"
        if text.count(queue_cap) < 13:
            issues.append(f"{filename}: naval production is not consistently queue/role-capped")
        if text.count("(goal gl-naval-specialist-support YES)") < 2:
            issues.append(f"{filename}: bounded heavy support detachment is incomplete")
        if text.count(specialist_cap) < 3:
            issues.append(f"{filename}: reserved heavy-detachment ceiling is not queue-safe")

        naval_targets = (
            "scout-galley-line",
            "polyreme-line",
            "fire-ship-line",
            "demolition-ship-line",
            "hemiolia-line",
            "boarding-ship",
            "quadrireme-line",
            "octeres",
            "juggernaut-line",
        )
        production_rules = [
            block
            for block in rule_blocks(text)
            if any(re.search(rf"\(up-train\s+[^\n]*\b{re.escape(target)}\)", block[4]) for target in naval_targets)
        ]
        if len(production_rules) != 16:
            issues.append(f"{filename}: expected 16 common warship production rules, found {len(production_rules)}")
        for block in production_rules:
            if queue_cap not in block[3] and specialist_cap not in block[3]:
                issues.append(
                    f"{filename}: warship production rule at offset {block[0]} lacks a queue-aware total cap"
                )
            if "(up-modify-goal gl-naval-fleet-count-total c:+ 1)" not in block[4]:
                issues.append(
                    f"{filename}: warship production rule at offset {block[0]} does not reserve queued capacity"
                )

        pre_imperial_q = matching_rules(
            text,
            facts=(
                "(current-age < imperial-age)",
                "(goal gl-naval-role NAVAL-ROLE-SUPPORT)",
                "(goal gl-naval-specialist-support YES)",
                specialist_cap,
                "(unit-type-count-total quadrireme-line < 1)",
            ),
            actions=("quadrireme-line",),
        )
        imperial_octeres = matching_rules(
            text,
            facts=(
                "(current-age >= imperial-age)",
                "(goal gl-naval-role NAVAL-ROLE-SUPPORT)",
                "(goal gl-naval-specialist-support YES)",
                specialist_cap,
                "(unit-type-count-total octeres < 1)",
            ),
            actions=("octeres",),
        )
        second_imperial_q = matching_rules(
            text,
            facts=(
                "(current-age >= imperial-age)",
                "(goal gl-naval-role NAVAL-ROLE-SUPPORT)",
                "(goal gl-naval-specialist-support YES)",
                specialist_cap,
                "(unit-type-count-total quadrireme-line < 2)",
            ),
            actions=("quadrireme-line",),
        )
        if len(pre_imperial_q) != 1:
            issues.append(f"{filename}: pre-Imperial support Quadrireme must be bounded to one")
        if len(imperial_octeres) != 1 or len(second_imperial_q) != 1:
            issues.append(f"{filename}: Imperial Octeres/second-Quadrireme specialist rules are incomplete")
        elif imperial_octeres[0][0] >= second_imperial_q[0][0]:
            issues.append(f"{filename}: Octeres must be evaluated before the second Imperial heavy reme")

    for filename, unit_line in (
        ("rawai-civ-egyptians.per", "tessarakonteres"),
        ("rawai-civ-macedonians.per", "tessarakonteres"),
        ("rawai-civ-illyrians.per", "liburna-line"),
    ):
        text = (ROOT / filename).read_text(encoding="utf-8-sig")
        rules = matching_rules(
            text,
            facts=(
                "(up-compare-goal gl-naval-fleet-count-total g:< gl-naval-specialist-fleet-cap)",
            ),
            actions=(
                f"(train {unit_line})",
                "(up-modify-goal gl-naval-fleet-count-total c:+ 1)",
            ),
        )
        if len(rules) != 1 or f"(unit-type-count-total {unit_line}" not in rules[0][3]:
            issues.append(f"{filename}: naval unique production bypasses its queue-aware role cap")

    research = (ROOT / "rawai-research.per").read_text(encoding="utf-8-sig")
    if "ri-reinforced-prow" in research:
        issues.append("no-effect Reinforced Prow technology is still queued")
    if "(goal gl-naval-specialist-support YES)" not in research:
        issues.append("support heavy-hull upgrade path is missing")

    required_doctrine_tokens = (
        "(up-allied-goal any-ally good-navy == YES)",
        "(up-allied-goal any-ally gl-own-naval-capability >",
        "(set-goal naval-attack-percentage 0)",
        "(up-modify-goal gl-naval-fleet-cap g:= gl-three-percent)",
        "(up-modify-goal gl-naval-fleet-cap g:= gl-eight-percent)",
        "(up-modify-goal gl-naval-fleet-cap g:= gl-ten-percent)",
        "(up-modify-goal gl-naval-specialist-fleet-cap g:= gl-five-percent)",
    )
    doctrine_code = "\n".join(
        facts + "\n=>\n" + actions for _, _, _, facts, actions in rule_blocks(doctrine)
    )
    for token in required_doctrine_tokens:
        if token not in doctrine_code:
            issues.append(f"generated doctrine is missing semantic token: {token}")

    doctrine_support_zero = matching_rules(
        doctrine,
        facts=("(goal gl-naval-role NAVAL-ROLE-SUPPORT)",),
        actions=("(set-goal naval-attack-percentage 0)",),
    )
    if len(doctrine_support_zero) != 1:
        issues.append("generated doctrine must give SUPPORT exactly one independent-attack zero rule")

    doctrine_queue_sum = matching_rules(
        doctrine,
        facts=("(goal gl-naval-capability-ready YES)",),
        actions=(
            "(up-get-fact unit-type-count-total warship-class gl-naval-fleet-count-total)",
            "(up-get-fact unit-type-count-total boarding-ship gl-naval-boarding-count-total)",
            "(up-modify-goal gl-naval-fleet-count-total g:+ gl-naval-boarding-count-total)",
        ),
    )
    if len(doctrine_queue_sum) != 1:
        issues.append("generated doctrine must publish the queue-aware class-22 plus Boarding total")

    if issues:
        for issue in issues:
            print(f"ERROR: {issue}")
        raise SystemExit(1)
    print(
        "Validated naval doctrine: 34 scores, all-No relative election, Yes/No team roles, "
        "queue-safe role caps, specialist support, research, and attack ownership"
    )


if __name__ == "__main__":
    main()
