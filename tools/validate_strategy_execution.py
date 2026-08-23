#!/usr/bin/env python3
"""Validate that generated strategy choices have executable PER rule paths."""

from __future__ import annotations

import json
import re
from pathlib import Path

from sync_civ_strategies import (
    AI_ROOT,
    CONFIG_PATH,
    ENEMY_CIV_SYMBOLS,
    HISTORICAL_CONFIG_PATH,
    RUSH_GOALS,
    TRAIN_GOALS,
    historical_profile,
    matchup_adjustments,
)


ROLE_GOALS = ["primary", "secondary", "tertiary", "quaternary"]
DIFFICULTIES = [
    "DIFFICULTY-EASIEST",
    "DIFFICULTY-EASY",
    "DIFFICULTY-MODERATE",
    "DIFFICULTY-HARD",
    "DIFFICULTY-HARDEST",
    "DIFFICULTY-EXTREME",
]


def code_only(text: str) -> str:
    lines = []
    for raw_line in text.splitlines():
        line = raw_line.split(";", 1)[0]
        line = re.sub(r'"(?:\\.|[^"\\])*"', '""', line)
        lines.append(line)
    return "\n".join(lines)


def defrule_blocks(text: str) -> list[str]:
    code = code_only(text)
    blocks: list[str] = []
    start = 0
    while True:
        match = re.search(r"\(defrule\b", code[start:])
        if not match:
            break
        block_start = start + match.start()
        depth = 0
        for index in range(block_start, len(code)):
            if code[index] == "(":
                depth += 1
            elif code[index] == ")":
                depth -= 1
                if depth == 0:
                    blocks.append(code[block_start : index + 1])
                    start = index + 1
                    break
        else:
            break
    return blocks


def required_roles(profiles: dict[str, dict[str, object]]) -> set[tuple[str, str]]:
    required: set[tuple[str, str]] = set()
    for profile in profiles.values():
        for field in ("early", "late"):
            units = profile[field]
            assert isinstance(units, list)
            required.update((ROLE_GOALS[index], str(unit)) for index, unit in enumerate(units))
        support = profile["support"]
        assert isinstance(support, list)
        required.update(
            (
                "primary-support" if index == 0 else "secondary-support",
                str(unit),
            )
            for index, unit in enumerate(support)
        )
    return required


def validate_executor(
    path: Path,
    profiles: dict[str, dict[str, object]],
) -> list[str]:
    errors: list[str] = []
    text = code_only(path.read_text(encoding="utf-8-sig"))
    for role, unit in sorted(required_roles(profiles)):
        if not re.search(rf"\(goal\s+{re.escape(role)}-unit\s+{re.escape(unit)}\s*\)", text):
            errors.append(f"{path.name}: missing {role}-unit executor for {unit}")

    for block_number, block in enumerate(defrule_blocks(text), 1):
        can_train = re.findall(r"\(up-can-train\s+\S+\s+c:\s*([^\s)]+)", block)
        trains = re.findall(r"\(up-train\s+\S+\s+c:\s*([^\s)]+)", block)
        if can_train and trains and can_train != trains:
            errors.append(
                f"{path.name}: rule {block_number} checks {can_train} but trains {trains}"
            )
    return errors


def preprocess(text: str, difficulty: str) -> str:
    active = True
    stack: list[bool] = []
    output: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#load-if-defined "):
            stack.append(active)
            symbol = stripped.split(maxsplit=1)[1].split(";", 1)[0].strip()
            active = active and symbol == difficulty
        elif stripped.startswith("#load-if-not-defined "):
            stack.append(active)
            symbol = stripped.split(maxsplit=1)[1].split(";", 1)[0].strip()
            active = active and symbol != difficulty
        elif stripped == "#end-if":
            active = stack.pop()
        elif active:
            output.append(line)
    if stack:
        raise ValueError("unbalanced preprocessor input")
    return "\n".join(output)


def validate_difficulty_matrix() -> list[str]:
    errors: list[str] = []
    difficulty_text = (AI_ROOT / "rawai-difficulty.per").read_text(encoding="utf-8-sig")
    cheat_text = (AI_ROOT / "rawai-cheats.per").read_text(encoding="utf-8-sig")
    expected_intervals = {
        "DIFFICULTY-EASIEST": 2700,
        "DIFFICULTY-EASY": 2700,
        "DIFFICULTY-MODERATE": 1800,
        "DIFFICULTY-HARD": 600,
        "DIFFICULTY-HARDEST": 600,
        "DIFFICULTY-EXTREME": 600,
    }
    expected_refunds = {
        "DIFFICULTY-EASIEST": None,
        "DIFFICULTY-EASY": None,
        "DIFFICULTY-MODERATE": 6,
        "DIFFICULTY-HARD": 6,
        "DIFFICULTY-HARDEST": 12,
        "DIFFICULTY-EXTREME": 37,
    }
    for difficulty in DIFFICULTIES:
        active_difficulty = preprocess(difficulty_text, difficulty)
        intervals = [
            int(value)
            for value in re.findall(
                r"periodic-attack-interval\s+c:=\s*(\d+)", active_difficulty
            )
        ]
        expected_interval = expected_intervals[difficulty]
        if intervals.count(expected_interval) != 1:
            errors.append(
                f"{difficulty}: expected one attack interval {expected_interval}, got {intervals}"
            )

        active_cheats = preprocess(cheat_text, difficulty)
        refunds = [
            int(value)
            for value in re.findall(r"gl-refund-food\s+c:=\s*(\d+)", active_cheats)
            if int(value) > 0
        ]
        expected_refund = expected_refunds[difficulty]
        if expected_refund is None:
            if refunds:
                errors.append(f"{difficulty}: unexpected villager refunds {refunds}")
        elif expected_refund not in refunds:
            errors.append(
                f"{difficulty}: expected villager refund {expected_refund}, got {refunds}"
            )
    return errors


def validate_age_timing() -> list[str]:
    errors: list[str] = []
    main_text = (AI_ROOT / "AI RAW.per").read_text(encoding="utf-8-sig")
    if not re.search(r'\(load\s+"rawai-escrow"\s*\)', main_text):
        errors.append("AI RAW.per: research escrow policy is not loaded")

    exemptions = (
        "(goal rush-rushing NO)",
        "strategy c:!= BOOMER-STRATEGY",
        "boomer-affinity c:<= 0",
        "fishboom-affinity c:<= 0",
    )
    age_blocks = defrule_blocks(
        (AI_ROOT / "rawai-age-advancement.per").read_text(encoding="utf-8-sig")
    )
    for technology, deadline in (
        ("ri-middle-antiquity-age", 570),
        ("ri-imperial-age", 990),
    ):
        matching = [
            block
            for block in age_blocks
            if f"(game-time >= {deadline})" in block
            and f"(up-research gl-researchescrow-state c: {technology})" in block
        ]
        if len(matching) != 1 or any(token not in matching[0] for token in exemptions):
            errors.append(
                f"rawai-age-advancement.per: invalid normal deadline for {technology}"
            )

    rush_blocks = defrule_blocks(
        (AI_ROOT / "rawai-rush.per").read_text(encoding="utf-8-sig")
    )
    if not any(
        "(attack-now)" in block and "(set-goal rush-rushing NO)" in block
        for block in rush_blocks
    ):
        errors.append("rawai-rush.per: opening commitment never releases age exemption")
    return errors


def main() -> None:
    errors: list[str] = []
    extreme = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    overrides = json.loads(HISTORICAL_CONFIG_PATH.read_text(encoding="utf-8"))
    historical = {
        civ: historical_profile(profile, overrides.get(civ, {}))
        for civ, profile in extreme.items()
    }

    errors.extend(
        validate_executor(AI_ROOT / "rawai-military-units-common.per", historical)
    )
    errors.extend(
        validate_executor(
            AI_ROOT / "rawai-military-units-common-hard.per",
            {
                **{f"historical:{civ}": profile for civ, profile in historical.items()},
                **{f"extreme:{civ}": profile for civ, profile in extreme.items()},
            },
        )
    )

    rush_text = code_only((AI_ROOT / "rawai-rush.per").read_text(encoding="utf-8-sig"))
    for name in RUSH_GOALS:
        if not re.search(rf"\(set-goal\s+rush-{re.escape(name)}\s+YES\s*\)", rush_text):
            errors.append(f"rawai-rush.per: {name} has no activation path")
        if not re.search(rf"\(goal\s+rush-{re.escape(name)}\s+YES\s*\)", rush_text):
            errors.append(f"rawai-rush.per: {name} has no execution path")

    expected_symbols = set(ENEMY_CIV_SYMBOLS.values())
    historical_non_neutral = 0
    extreme_non_neutral = 0
    for own_civ in extreme:
        civ_path = AI_ROOT / f"rawai-civ-{own_civ}.per"
        civ_text = civ_path.read_text(encoding="utf-8-sig")
        symbols = set(
            re.findall(r"#load-if-defined\s+(UP-[A-Z-]+-CIV-ENEMY)", civ_text)
        )
        if symbols != expected_symbols:
            errors.append(
                f"{civ_path.name}: enemy symbol mismatch "
                f"missing={sorted(expected_symbols - symbols)} extra={sorted(symbols - expected_symbols)}"
            )
        if re.search(r"up-modify-goal\s+\S+-affinity\s+c:[+-]\s+0\b", civ_text):
            errors.append(f"{civ_path.name}: contains a zero-value matchup modifier")
        for enemy_civ in extreme:
            historical_non_neutral += bool(
                matchup_adjustments(
                    own_civ,
                    enemy_civ,
                    historical[own_civ],
                    historical[enemy_civ],
                )
            )
            extreme_non_neutral += bool(
                matchup_adjustments(
                    own_civ,
                    enemy_civ,
                    extreme[own_civ],
                    extreme[enemy_civ],
                )
            )

        for profile in (historical[own_civ], extreme[own_civ]):
            selected_units = {
                str(unit)
                for field in ("early", "late", "support")
                for unit in profile[field]
            }
            for unit in selected_units:
                train_goal = TRAIN_GOALS[unit]
                if not re.search(
                    rf"\(goal\s+{re.escape(train_goal)}\s+NO\s*\)", civ_text
                ):
                    errors.append(
                        f"{civ_path.name}: configured {unit} does not enforce {train_goal}"
                    )

    matchup_total = len(extreme) ** 2
    if historical_non_neutral < int(matchup_total * 0.9):
        errors.append(
            f"historical matchup coverage is too sparse: {historical_non_neutral}/{matchup_total}"
        )
    if extreme_non_neutral < int(matchup_total * 0.9):
        errors.append(
            f"Extreme matchup coverage is too sparse: {extreme_non_neutral}/{matchup_total}"
        )

    errors.extend(validate_difficulty_matrix())
    errors.extend(validate_age_timing())
    report = {
        "errors": errors,
        "historical_matchups_with_adjustments": historical_non_neutral,
        "extreme_matchups_with_adjustments": extreme_non_neutral,
        "matchup_total": matchup_total,
    }
    print(json.dumps(report, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
