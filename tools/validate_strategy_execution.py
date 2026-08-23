#!/usr/bin/env python3
"""Validate that generated strategy choices have executable PER rule paths."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from sync_civ_strategies import (
    AI_ROOT,
    CIV_SHEET_NAMES,
    CONFIG_PATH,
    ENEMY_CIV_SYMBOLS,
    HISTORICAL_CONFIG_PATH,
    RUSH_GOALS,
    TRAIN_GOALS,
    UNIT_FOCUS_COLUMNS,
    UNIQUE_MANIFEST_PATH,
    historical_profile,
    matchup_adjustments,
    read_focus_rows,
    unit_is_focused,
    validate_config,
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

# Resource domains verified against the current Rome at War DAT during the
# Roman/Briton calibration pass. The mod data remains authoritative when this
# table and the DAT differ.
CALIBRATED_UNIQUE_TECH_ESCROW = {
    "rawai-civ-britons.per": {
        "ut-ovates": {"food", "gold"},
        "ut-warrior-druids": {"food", "gold"},
        "ut-carnyx": {"food", "gold"},
        "ut-exmoor-covines": {"food", "gold"},
    },
    "rawai-civ-romeemp.per": {
        "ut-siege-ballistae": {"wood", "gold"},
        "ut-castra-network": {"wood", "stone"},
        "ut-pax-romana": {"food", "gold"},
        "ut-diocletian-reforms": {"food", "gold"},
    },
    "rawai-civ-numidians.per": {
        "ri-range-elite-mounted-skirmisher": {"wood", "gold"},
    },
    "rawai-civ-seleucids.per": {
        "ri-aphraktos": {"food", "gold"},
    },
}


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


def preprocess_symbols(text: str, defined_symbols: set[str]) -> str:
    active = True
    stack: list[bool] = []
    output: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#load-if-defined "):
            stack.append(active)
            symbol = stripped.split(maxsplit=1)[1].split(";", 1)[0].strip()
            active = active and symbol in defined_symbols
        elif stripped.startswith("#load-if-not-defined "):
            stack.append(active)
            symbol = stripped.split(maxsplit=1)[1].split(";", 1)[0].strip()
            active = active and symbol not in defined_symbols
        elif stripped == "#end-if":
            active = stack.pop()
        elif active:
            output.append(line)
    if stack:
        raise ValueError("unbalanced preprocessor input")
    return "\n".join(output)


def preprocess(text: str, difficulty: str) -> str:
    return preprocess_symbols(text, {difficulty})


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


ROLE_FACT = re.compile(
    r"\(goal\s+(?:primary|secondary|tertiary|quaternary|"
    r"primary-support|secondary-support)-unit\s+",
)


def trained_units(block: str) -> set[str]:
    return set(re.findall(r"\(train\s+([^\s)]+)\s*\)", block)) | set(
        re.findall(r"\(up-train\s+\S+\s+c:\s*([^\s)]+)\s*\)", block)
    )


def can_train_unit(block: str, unit: str) -> bool:
    return bool(
        re.search(
            rf"\(can-train(?:-with-escrow)?\s+{re.escape(unit)}\s*\)",
            block,
        )
        or re.search(
            rf"\(up-can-train\s+\S+\s+c:\s*{re.escape(unit)}\s*\)",
            block,
        )
    )


def has_finite_bound(block: str, bound_units: set[str]) -> bool:
    positive_limit = r"(?:gl-(?:one|two|five|ten)-percent|[1-9]\d*)"
    bounded_units: set[str] = set()
    for unit in bound_units:
        escaped = re.escape(unit)
        if re.search(
            rf"\(unit-type-count-total\s+{escaped}\s+"
            rf"(?:(?:g:|c:)?<\s*{positive_limit}|==\s*0)\s*\)",
            block,
        ):
            bounded_units.add(unit)
            continue
        if re.search(
            rf"\(up-object-type-count-total\s+c:\s*{escaped}\s+"
            rf"(?:g:|c:)?<\s*{positive_limit}\s*\)",
            block,
        ):
            bounded_units.add(unit)
    return bounded_units == bound_units


def phase_gate_persists(block: str) -> bool:
    exact_phases = {
        int(value) for value in re.findall(r"\(goal\s+current-phase\s+(\d+)\s*\)", block)
    }
    if exact_phases:
        first_phase = min(exact_phases)
        if not set(range(first_phase, 8)).issubset(exact_phases):
            return False

    comparisons = re.findall(
        r"\(up-compare-goal\s+current-phase\s+(<=|>=|==|!=|<|>)\s+(\d+)\s*\)",
        block,
    )
    allowed = set(range(1, 8))
    for operator, raw_value in comparisons:
        value = int(raw_value)
        predicates = {
            "<": lambda phase: phase < value,
            "<=": lambda phase: phase <= value,
            ">": lambda phase: phase > value,
            ">=": lambda phase: phase >= value,
            "==": lambda phase: phase == value,
            "!=": lambda phase: phase != value,
        }
        allowed = {phase for phase in allowed if predicates[operator](phase)}
    if comparisons and (not allowed or 7 not in allowed):
        return False
    if comparisons:
        first_phase = min(allowed)
        if not set(range(first_phase, 8)).issubset(allowed):
            return False
    return True


def bounded_direct_train_blocks(
    text: str,
    unit: str,
    bound_units: set[str] | None = None,
) -> list[str]:
    """Return bounded, role-independent, persistent production paths."""
    expected_bounds = bound_units or {unit}
    return [
        block
        for block in defrule_blocks(text)
        if unit in trained_units(block)
        and can_train_unit(block, unit)
        and not ROLE_FACT.search(block)
        and has_finite_bound(block, expected_bounds)
        and phase_gate_persists(block)
    ]


def bounded_direct_train_units(text: str) -> set[str]:
    """Find all civ-local bounded production independent of generic roles."""
    units = {
        unit
        for block in defrule_blocks(text)
        if not ROLE_FACT.search(block) and phase_gate_persists(block)
        for unit in trained_units(block)
        if can_train_unit(block, unit) and has_finite_bound(block, {unit})
    }
    return units


def validate_focus_exemptions(
    extreme: dict[str, dict[str, object]],
    overrides: dict[str, dict[str, object]],
) -> list[str]:
    """Keep generic focus constraints and direct bounded exceptions distinct."""
    errors: list[str] = []
    try:
        validate_config(extreme, overrides)
    except ValueError as error:
        errors.append(f"generic Extreme focus validation failed: {error}")

    # Recheck the generic role boundary here so a future generator refactor
    # cannot accidentally make this semantic validator rely only on comments.
    focus_rows = read_focus_rows()
    unique_manifest = json.loads(UNIQUE_MANIFEST_PATH.read_text(encoding="utf-8"))
    manifest_civs = unique_manifest.get("civs", {})
    if set(manifest_civs) != set(extreme):
        errors.append(
            "unique-unit manifest civilization set differs from strategy data: "
            f"missing={sorted(set(extreme) - set(manifest_civs))} "
            f"extra={sorted(set(manifest_civs) - set(extreme))}"
        )
    for civ, profile in extreme.items():
        civ_focus = focus_rows[CIV_SHEET_NAMES[civ]]
        for field in ("early", "late", "support"):
            values = profile[field]
            assert isinstance(values, list)
            for value in values:
                unit = str(value)
                column = UNIT_FOCUS_COLUMNS[unit]
                if not unit_is_focused(unit, column, civ_focus[column]):
                    errors.append(
                        f"{civ}.{field}: generic Extreme role {unit} escapes "
                        f"the {column} focus category"
                    )

        civ_path = AI_ROOT / f"rawai-civ-{civ}.per"
        civ_text = civ_path.read_text(encoding="utf-8-sig")
        expected_units: dict[str, tuple[str, set[str]]] = {}
        civ_manifest = manifest_civs.get(civ, {})
        for family in civ_manifest.get("families", []):
            family_name = str(family["name"])
            bounds = {str(value) for value in family.get("bound_units", [])}
            for value in family.get("train_units", []):
                unit = str(value)
                expected_units[unit] = (family_name, bounds or {unit})

        active_by_difficulty = {
            name: preprocess(civ_text, name)
            for name in DIFFICULTIES
        }
        for unit, (family_name, bound_units) in expected_units.items():
            for difficulty, active_text in active_by_difficulty.items():
                if not bounded_direct_train_blocks(active_text, unit, bound_units):
                    errors.append(
                        f"{civ_path.name}: {family_name} ({unit}) has no bounded, "
                        f"role-independent persistent path on {difficulty}"
                    )

        allowed_non_composition = {
            str(unit)
            for node in unique_manifest.get("non_composition_nodes", [])
            if node.get("civ") == civ
            for unit in node.get("train_units", [])
        }
        for block_number, block in enumerate(defrule_blocks(civ_text), 1):
            if ROLE_FACT.search(block):
                continue
            for unit in trained_units(block):
                if unit in allowed_non_composition:
                    continue
                if unit not in expected_units:
                    errors.append(
                        f"{civ_path.name}: rule {block_number} directly trains "
                        f"unmanifested composition unit {unit}"
                    )
                    continue
                _, bound_units = expected_units[unit]
                if not has_finite_bound(block, bound_units):
                    errors.append(
                        f"{civ_path.name}: rule {block_number} directly trains {unit} "
                        "without a positive finite manifest bound"
                    )
        for block_number, block in enumerate(defrule_blocks(civ_text), 1):
            disabled = re.search(
                r"\(unit-type-count-total\s+([^\s)]+)\s+g:<\s+"
                r"gl-no-percent\s*\)",
                block,
            )
            if disabled and re.search(
                rf"\(can-train\s+{re.escape(disabled.group(1))}\s*\)", block
            ):
                errors.append(
                    f"{civ_path.name}: rule {block_number} disables direct production "
                    f"of {disabled.group(1)} with a zero quota"
                )

    for filename in (
        "rawai-military-units-common.per",
        "rawai-military-units-common-hard.per",
    ):
        path = AI_ROOT / filename
        generic_text = preprocess_symbols(
            path.read_text(encoding="utf-8-sig"),
            set(),
        )
        blocks = defrule_blocks(generic_text)
        reactive_skirmisher = any(
            all(
                token in block
                for token in (
                    "(players-unit-type-count any-enemy archery-class >= 3)",
                    "(players-unit-type-count any-enemy cavalry-archer-class >= 3)",
                    "(unit-type-count-total skirmisher-line g:< gl-five-percent)",
                    "(up-can-train gl-unitescrow-state c: skirmisher-line)",
                    "(up-train gl-unitescrow-state c: skirmisher-line)",
                )
            )
            and not ROLE_FACT.search(block)
            and len(re.findall(r"\(or\b", block)) == 1
            for block in blocks
        )
        if not reactive_skirmisher:
            errors.append(f"{filename}: missing bounded threat-triggered Skirmisher exception")

    return errors


def validate_calibrated_unique_tech_escrow() -> list[str]:
    errors: list[str] = []
    for filename, expected_technologies in CALIBRATED_UNIQUE_TECH_ESCROW.items():
        blocks = defrule_blocks((AI_ROOT / filename).read_text(encoding="utf-8-sig"))
        for technology, expected_resources in expected_technologies.items():
            matching = [
                block
                for block in blocks
                if re.search(rf"\(research\s+{re.escape(technology)}\s*\)", block)
            ]
            if not matching:
                errors.append(f"{filename}: no research action for calibrated {technology}")
                continue
            for block in matching:
                released = set(re.findall(r"\(release-escrow\s+([^\s)]+)\s*\)", block))
                if released != expected_resources:
                    errors.append(
                        f"{filename}: {technology} releases {sorted(released)}, "
                        f"expected {sorted(expected_resources)} from current DAT"
                    )
    return errors


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_unique_manifest_sources() -> list[str]:
    """Verify recorded mod provenance when the sibling data mod is available."""
    manifest = json.loads(UNIQUE_MANIFEST_PATH.read_text(encoding="utf-8"))
    provenance = manifest["source_provenance"]
    errors: list[str] = []
    constants_hash = sha256(AI_ROOT / "rawai-unitconstants.per")
    if constants_hash != provenance["rawai-unitconstants.per_sha256_at_audit"]:
        errors.append(
            "unique-unit-production.json: rawai-unitconstants.per changed since "
            "the manifest audit; refresh the mapping and provenance"
        )

    candidates = [
        AI_ROOT.parent / "RaW data fix" / "resources" / "_common" / "dat",
        AI_ROOT.parents[1] / "RaW data fix" / "resources" / "_common" / "dat",
    ]
    data_root = next((path for path in candidates if path.is_dir()), None)
    if data_root is None:
        return errors

    core_sources = {
        "empires2_x2_p1.dat_sha256": data_root / "empires2_x2_p1.dat",
        "unitlines.json_sha256": data_root / "unitlines.json",
    }
    for key, path in core_sources.items():
        if not path.is_file() or sha256(path) != provenance[key]:
            errors.append(
                f"unique-unit-production.json: authoritative source drift for {path.name}"
            )

    tree_root = data_root / "CivTechTrees"
    for civ, record in manifest["civs"].items():
        path = tree_root / record["source_tree"]
        if not path.is_file() or sha256(path) != record["source_sha256"]:
            errors.append(
                f"unique-unit-production.json: tech-tree source drift for {civ} "
                f"({record['source_tree']})"
            )
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
    errors.extend(validate_focus_exemptions(extreme, overrides))
    errors.extend(validate_calibrated_unique_tech_escrow())
    errors.extend(validate_unique_manifest_sources())
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
