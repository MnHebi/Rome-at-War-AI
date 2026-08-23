#!/usr/bin/env python3
"""Synchronize civilization doctrine blocks into the Rome at War PER files."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

from read_ods import read_sheets


ROOT = Path(__file__).resolve().parents[1]
AI_ROOT = ROOT / "Rome-at-War-AI-main"
if not AI_ROOT.is_dir():
    AI_ROOT = ROOT
CONFIG_PATH = AI_ROOT / "civ-strategy-data.json"
HISTORICAL_CONFIG_PATH = AI_ROOT / "civ-strategy-historical-overrides.json"
FOCUS_PATH = ROOT / "RAW AI unit focus spreadsheet.ods"
RUSH_GOALS = [
    "drush",
    "fcast",
    "trush",
    "hrush",
    "krush",
    "mush",
    "sprush",
    "scush",
    "skrush",
    "sgush",
    "cush",
    "lush",
    "ilush",
    "fc",
]
UNIT_SLOTS = ["primary", "secondary", "tertiary", "quaternary"]
TRAIN_GOALS = {
    "CHAMPION": "train-champion",
    "SPEARMAN": "train-spearman",
    "HORUS": "train-horus",
    "ARCHER": "train-bowman",
    "SKIRMISHER": "train-skirmisher",
    "CAVARCHER": "train-cavarcher",
    "CMLARCHER": "train-cmlarcher",
    "ELEARCHER": "train-elearcher",
    "CHRARCHER": "train-chrarcher",
    "SCAVALRY": "train-scoutcav",
    "CAVALRY": "train-cavalry",
    "RATHA": "train-ratha",
    "CAMEL": "train-camel",
    "ELEPHANT": "train-elephant",
    "CHARIOT": "train-chariot",
    "PRIEST": "train-priest",
}
CIV_SHEET_NAMES = {
    "armenia": "Armenians",
    "athenians": "Athenians",
    "britons": "Britons",
    "carthagians": "Carthagians",
    "cretans": "Cretans",
    "dacians": "Dacians",
    "egyptians": "Egyptians",
    "gauls": "Gauls",
    "germani": "Germani",
    "goths": "Goths",
    "gupta": "Gupta",
    "han": "Han",
    "huns": "Huns",
    "iberians": "Iberians",
    "illyrians": "Illyrians",
    "judeans": "Judeans",
    "kushans": "Kushan",
    "macedonians": "Macedonians",
    "mauryans": "Mauryans",
    "nanda": "Nanda",
    "nubians": "Nubians",
    "numidians": "Numidians",
    "parthians": "Parthians",
    "persians": "Persian",
    "phoenicians": "Phoenicians",
    "picts": "Picts",
    "pontus": "Pontus",
    "romeemp": "Roman Empire",
    "romerep": "Roman Republic",
    "scythians": "Scythians",
    "seleucids": "Seleucids",
    "spartans": "Spartans",
    "syracusans": "Syracusans",
    "thracians": "Thracians",
}
ENEMY_CIV_SYMBOLS = {
    "armenia": "UP-BERBERS-CIV-ENEMY",
    "athenians": "UP-LITHUANIANS-CIV-ENEMY",
    "britons": "UP-BRITON-CIV-ENEMY",
    "carthagians": "UP-PORTUGUESE-CIV-ENEMY",
    "cretans": "UP-VIETNAMESE-CIV-ENEMY",
    "dacians": "UP-ETHIOPIANS-CIV-ENEMY",
    "egyptians": "UP-AZTEC-CIV-ENEMY",
    "gauls": "UP-FRANKISH-CIV-ENEMY",
    "germani": "UP-TEUTONIC-CIV-ENEMY",
    "goths": "UP-GOTHIC-CIV-ENEMY",
    "gupta": "UP-GURJARAS-CIV-ENEMY",
    "han": "UP-CHINESE-CIV-ENEMY",
    "huns": "UP-HUN-CIV-ENEMY",
    "iberians": "UP-SPANISH-CIV-ENEMY",
    "illyrians": "UP-BULGARIANS-CIV-ENEMY",
    "judeans": "UP-SARACEN-CIV-ENEMY",
    "kushans": "UP-INDIAN-CIV-ENEMY",
    "macedonians": "UP-KOREAN-CIV-ENEMY",
    "mauryans": "UP-BENGALIS-CIV-ENEMY",
    "nanda": "UP-DRAVIDIANS-CIV-ENEMY",
    "nubians": "UP-MAYAN-CIV-ENEMY",
    "numidians": "UP-INCAN-CIV-ENEMY",
    "parthians": "UP-TURKISH-CIV-ENEMY",
    "persians": "UP-PERSIAN-CIV-ENEMY",
    "phoenicians": "UP-MONGOL-CIV-ENEMY",
    "picts": "UP-CELTIC-CIV-ENEMY",
    "pontus": "UP-KHMER-CIV-ENEMY",
    "romeemp": "UP-BYZANTINE-CIV-ENEMY",
    "romerep": "UP-ITALIAN-CIV-ENEMY",
    "scythians": "UP-CUMANS-CIV-ENEMY",
    "seleucids": "UP-BURMESE-CIV-ENEMY",
    "spartans": "UP-JAPANESE-CIV-ENEMY",
    "syracusans": "UP-MALAY-CIV-ENEMY",
    "thracians": "UP-MALIAN-CIV-ENEMY",
}
UNIT_FOCUS_COLUMNS = {
    "CHAMPION": "Infantry",
    "SPEARMAN": "Infantry",
    "HORUS": "Infantry",
    "ARCHER": "Archers",
    "SKIRMISHER": "Archers",
    "CAVARCHER": "Cavalry Archers",
    "CMLARCHER": "Cavalry Archers",
    "ELEARCHER": "Cavalry Archers",
    "CHRARCHER": "Cavalry Archers",
    "SCAVALRY": "Cavalry",
    "CAVALRY": "Cavalry",
    "RATHA": "Cavalry",
    "CAMEL": "Cavalry",
    "CHARIOT": "Cavalry",
    "ELEPHANT": "Cavalry",
    "PRIEST": "Priests",
}
SPECIALTY_FOCUS_COLUMNS = {
    "SPE-INFANTRY": ("Infantry",),
    "SPE-ARCHER": ("Archers",),
    "SPE-SKIRMISHER": ("Archers",),
    "SPE-CAVARCHER": ("Cavalry Archers",),
    "SPE-CAVALRY": ("Cavalry",),
    "SPE-CAMEL": ("Cavalry",),
    "SPE-ELEPHANT": ("Cavalry", "Cavalry Archers"),
    "SPE-PRIEST": ("Priests",),
    "SPE-SIEGE": ("Siege",),
    "SPE-NAVAL": ("Naval",),
}
RUSH_FOCUS_UNITS = {
    "drush": "CHAMPION",
    "hrush": "HORUS",
    "krush": "CAVALRY",
    "mush": "PRIEST",
    "sprush": "SPEARMAN",
    "scush": "SCAVALRY",
    "skrush": "SKIRMISHER",
    "sgush": "SIEGE",
    "cush": "CHAMPION",
    "lush": "CHAMPION",
    "ilush": "CHAMPION",
}
FOCUS_VALUE_UNIT_ALLOWLISTS = {
    ("Infantry", "yes(spears)"): {"SPEARMAN"},
    ("Infantry", "yes(eagle warrior)"): {"HORUS"},
    ("Infantry", "taxiarch, spear"): {"CHAMPION", "SPEARMAN"},
    ("Infantry", "imitation legionary, spear"): {"CHAMPION", "SPEARMAN"},
    ("Infantry", "legionary, spear"): {"CHAMPION", "SPEARMAN"},
    ("Infantry", "praetorian guard, legionary, spear"): {"CHAMPION", "SPEARMAN"},
    ("Infantry", "hippeus"): {"CHAMPION", "SPEARMAN"},
    ("Cavalry", "yes(scout)"): {"SCAVALRY"},
    ("Cavalry", "yes(scouts)"): {"SCAVALRY"},
    ("Cavalry", "yes(no scouts)"): {"CAVALRY", "RATHA", "CAMEL", "CHARIOT", "ELEPHANT"},
    ("Cavalry", "yes(chariot, camel)"): {"CAMEL", "CHARIOT"},
    ("Cavalry", "yes(camel,chariot)"): {"CAMEL", "CHARIOT"},
    ("Archers", "crossbowmen"): {"ARCHER"},
    ("Cavalry Archers", "yes(chariot)"): {"CHRARCHER"},
    ("Cavalry Archers", "yes(elephant)"): {"ELEARCHER"},
    ("Cavalry Archers", "yes(camel archers)"): {"CMLARCHER"},
}

# Matchups use broad battlefield roles rather than claiming exact historical
# pairings between every faction. Early units receive more weight because these
# modifiers choose openings, not the final Imperial-age army.
UNIT_THREAT_TAGS = {
    "CHAMPION": {"infantry"},
    "SPEARMAN": {"infantry", "spearman"},
    "HORUS": {"infantry", "raider"},
    "ARCHER": {"archer"},
    "SKIRMISHER": {"skirmisher"},
    "CAVARCHER": {"cavarcher"},
    "CMLARCHER": {"camel", "cavarcher"},
    "ELEARCHER": {"elephant", "cavarcher"},
    "CHRARCHER": {"chariot", "cavarcher"},
    "SCAVALRY": {"cavalry", "light-cavalry", "raider"},
    "CAVALRY": {"cavalry", "heavy-cavalry"},
    "RATHA": {"cavalry", "heavy-cavalry"},
    "CAMEL": {"cavalry", "camel"},
    "ELEPHANT": {"cavalry", "elephant"},
    "CHARIOT": {"cavalry", "chariot"},
    "PRIEST": {"priest"},
}
SPECIALTY_THREAT_TAGS = {
    "SPE-INFANTRY": {"infantry"},
    "SPE-ARCHER": {"archer"},
    "SPE-SKIRMISHER": {"skirmisher"},
    "SPE-CAVARCHER": {"cavarcher"},
    "SPE-CAVALRY": {"cavalry"},
    "SPE-CAMEL": {"camel"},
    "SPE-ELEPHANT": {"elephant"},
    "SPE-PRIEST": {"priest"},
    "SPE-SIEGE": {"siege"},
    "SPE-NAVAL": {"naval"},
    "SPE-DEFENSIVE": {"defensive"},
    "SPE-ADVWEAP": {"siege", "archer"},
}
RUSH_MATCHUPS = {
    "drush": (
        {"spearman", "skirmisher", "siege", "priest"},
        {"archer", "cavarcher", "cavalry", "elephant"},
    ),
    "fcast": (
        {"defensive", "elephant", "priest", "siege"},
        {"raider", "light-cavalry", "infantry"},
    ),
    "trush": (
        {"defensive", "archer", "priest"},
        {"siege", "cavalry"},
    ),
    "hrush": (
        {"archer", "skirmisher", "priest", "siege"},
        {"infantry", "spearman", "heavy-cavalry"},
    ),
    "krush": (
        {"archer", "skirmisher", "priest", "siege"},
        {"spearman", "camel", "elephant"},
    ),
    "mush": (
        {"heavy-cavalry", "elephant", "chariot"},
        {"light-cavalry", "archer", "cavarcher", "infantry"},
    ),
    "sprush": (
        {"cavalry", "cavarcher", "camel", "elephant", "chariot"},
        {"archer", "skirmisher", "infantry"},
    ),
    "scush": (
        {"archer", "skirmisher", "priest", "siege"},
        {"spearman", "camel", "heavy-cavalry"},
    ),
    "skrush": (
        {"archer", "cavarcher"},
        {"infantry", "cavalry", "chariot"},
    ),
    "sgush": (
        {"infantry", "spearman", "archer", "skirmisher"},
        {"cavalry", "cavarcher"},
    ),
    "cush": (
        {"spearman", "skirmisher", "siege", "priest"},
        {"archer", "cavarcher", "cavalry", "elephant"},
    ),
    "lush": (
        {"spearman", "skirmisher", "siege", "priest"},
        {"archer", "cavarcher", "cavalry", "elephant"},
    ),
    "ilush": (
        {"spearman", "skirmisher", "siege", "priest"},
        {"archer", "cavarcher", "cavalry", "elephant"},
    ),
    "fc": (
        {"defensive", "elephant", "priest", "siege"},
        {"raider", "light-cavalry", "infantry"},
    ),
}


def per_rule(goal: str, value: str, phase: str) -> str:
    return f"""(defrule
\t(up-compare-goal current-phase {phase} 4)
\t(not
\t\t(goal {goal} {value})
\t)
=>
\t(set-goal {goal} {value})
)
"""


def unique_in_order(values: list[object]) -> list[str]:
    result: list[str] = []
    for value in values:
        unit = str(value)
        if unit not in result:
            result.append(unit)
    return result


def training_enable_rule(unit: str, phase: str) -> str:
    train_goal = TRAIN_GOALS[unit]
    return f"""(defrule
	(up-compare-goal current-phase {phase} 4)
	(goal {train_goal} NO)
=>
	(set-goal {train_goal} YES)
)
"""


def unit_preference_rules(strategy: dict[str, object]) -> str:
    doctrine = strategy["doctrine"]
    early = strategy["early"]
    late = strategy["late"]
    support = strategy["support"]
    assert isinstance(doctrine, str)
    assert isinstance(early, list)
    assert isinstance(late, list)
    assert isinstance(support, list)

    rules = [f";Doctrine: {doctrine}.", ""]
    for slot, unit in zip(UNIT_SLOTS, early, strict=True):
        rules.append(per_rule(f"{slot}-unit", str(unit), "<").rstrip())
        rules.append("")
    for slot, unit in zip(UNIT_SLOTS, late, strict=True):
        rules.append(per_rule(f"{slot}-unit", str(unit), ">=").rstrip())
        rules.append("")
    for index, unit in enumerate(support[:2]):
        goal = "primary-support-unit" if index == 0 else "secondary-support-unit"
        rules.append(per_rule(goal, str(unit), ">=").rstrip())
        rules.append("")
    rules.extend([";Keep every configured composition line enabled for training.", ""])
    for unit in unique_in_order(early):
        rules.append(training_enable_rule(unit, "<").rstrip())
        rules.append("")
    for unit in unique_in_order(late + support):
        rules.append(training_enable_rule(unit, ">=").rstrip())
        rules.append("")
    return "\n".join(rules).rstrip() + "\n\n"


def gated_block(
    heading: str,
    historical_body: str,
    extreme_body: str,
) -> str:
    return "\n".join(
        [
            heading,
            ";Below Extreme: historical and broad combined-arms profile.",
            "#load-if-not-defined DIFFICULTY-EXTREME",
            "",
            historical_body.rstrip(),
            "",
            "#end-if",
            "",
            ";Extreme: max-return profile constrained by RAW AI unit focus spreadsheet.ods.",
            "#load-if-defined DIFFICULTY-EXTREME",
            "",
            extreme_body.rstrip(),
            "",
            "#end-if",
            "",
        ]
    )


def unit_preference_block(
    historical: dict[str, object],
    extreme: dict[str, object],
) -> str:
    return gated_block(
        ";civ specific unit preferences",
        unit_preference_rules(historical),
        unit_preference_rules(extreme),
    )


def rush_rules(strategy: dict[str, object]) -> str:
    rush = strategy["rush"]
    doctrine = strategy["doctrine"]
    assert isinstance(rush, dict)
    assert isinstance(doctrine, str)
    lines = [
        f";Opening priorities derived from doctrine: {doctrine}.",
        "(defrule",
        "\t(true)",
        "=>",
    ]
    for name in RUSH_GOALS:
        lines.append(f"\t(set-goal {name}-affinity {int(rush.get(name, 0))})")
    lines.extend(
        ["\t(set-goal rush-affinities-ready YES)", "", "\t(disable-self)", ")", ""]
    )
    return "\n".join(lines) + "\n"


def rush_block(
    historical: dict[str, object],
    extreme: dict[str, object],
) -> str:
    return gated_block(
        ";difficulty-specific rush affinities",
        rush_rules(historical),
        rush_rules(extreme),
    )


def specialty_rules(strategy: dict[str, object]) -> str:
    specialties = strategy["specialties"]
    assert isinstance(specialties, list)
    lines = ["(defrule", "\t(true)", "=>"]
    for index, value in enumerate(specialties, 1):
        lines.append(f"\t(set-goal civ-specialty{index} {value})")
    lines.extend(["", "\t(disable-self)", ")", ""])
    return "\n".join(lines)


def specialty_block(
    historical: dict[str, object],
    extreme: dict[str, object],
) -> str:
    return gated_block(
        ";define difficulty-specific civ specialties",
        specialty_rules(historical),
        specialty_rules(extreme),
    )


def threat_weights(strategy: dict[str, object]) -> Counter[str]:
    weights: Counter[str] = Counter()
    for field, weight in (("early", 2), ("late", 1)):
        units = strategy[field]
        assert isinstance(units, list)
        for unit in units:
            for tag in UNIT_THREAT_TAGS[str(unit)]:
                weights[tag] += weight
    specialties = strategy["specialties"]
    assert isinstance(specialties, list)
    for specialty in specialties:
        for tag in SPECIALTY_THREAT_TAGS.get(str(specialty), set()):
            weights[tag] += 2
    return weights


def matchup_adjustments(
    own_civ: str,
    enemy_civ: str,
    own: dict[str, object],
    enemy: dict[str, object],
) -> dict[str, int]:
    enemy_weights = threat_weights(enemy)
    own_rush = own["rush"]
    enemy_rush = enemy["rush"]
    assert isinstance(own_rush, dict)
    assert isinstance(enemy_rush, dict)
    enemy_max = max((int(value) for value in enemy_rush.values()), default=0)
    enemy_primary = {
        name for name, value in enemy_rush.items() if int(value) == enemy_max and enemy_max > 0
    }

    adjustments: dict[str, int] = {}
    for name in RUSH_GOALS:
        base = int(own_rush.get(name, 0))
        if base <= 0:
            continue
        strong, weak = RUSH_MATCHUPS[name]
        score = sum(enemy_weights[tag] for tag in strong) - sum(
            enemy_weights[tag] for tag in weak
        )
        if score >= 4:
            delta = 2
        elif score >= 1:
            delta = 1
        elif score <= -4:
            delta = -2
        elif score <= -1:
            delta = -1
        else:
            delta = 0

        # A mirror commitment gives neither side an opening advantage. Prefer a
        # configured alternative when one exists instead of blindly mirroring.
        if own_civ == enemy_civ and name in enemy_primary:
            delta -= 1

        delta = max(-2, min(2, delta))
        delta = max(-base, min(4 - base, delta))
        if delta:
            adjustments[name] = delta
    return adjustments


def matchup_rule(adjustments: dict[str, int], enemy: dict[str, object]) -> str:
    if not adjustments:
        return ";Base opening retained; no configured rush has a decisive matchup edge.\n"
    doctrine = enemy["doctrine"]
    assert isinstance(doctrine, str)
    lines = [f";Respond to enemy doctrine: {doctrine}.", "(defrule", "\t(true)", "=>"]
    for name in RUSH_GOALS:
        delta = adjustments.get(name)
        if delta is None:
            continue
        operator = "+" if delta > 0 else "-"
        lines.append(f"\t(up-modify-goal {name}-affinity c:{operator} {abs(delta)})")
    lines.extend(["", "\t(disable-self)", ")", ""])
    return "\n".join(lines) + "\n"


def matchup_block(
    own_civ: str,
    historical: dict[str, object],
    extreme: dict[str, object],
    historical_profiles: dict[str, dict[str, object]],
    extreme_profiles: dict[str, dict[str, object]],
) -> str:
    lines = [
        ";enemy-specific opening adjustments",
        ";Only rushes configured for the active difficulty profile are adjusted.",
        ";Positive values exploit the enemy doctrine; negative values avoid its counters.",
        "",
    ]
    for enemy_civ, enemy_extreme in extreme_profiles.items():
        symbol = ENEMY_CIV_SYMBOLS[enemy_civ]
        display_name = CIV_SHEET_NAMES[enemy_civ]
        enemy_historical = historical_profiles[enemy_civ]
        historical_rule = matchup_rule(
            matchup_adjustments(own_civ, enemy_civ, historical, enemy_historical),
            enemy_historical,
        ).rstrip()
        extreme_rule = matchup_rule(
            matchup_adjustments(own_civ, enemy_civ, extreme, enemy_extreme),
            enemy_extreme,
        ).rstrip()
        lines.extend([f"#load-if-defined {symbol} ; {display_name}", ""])
        if historical_rule == extreme_rule:
            lines.extend([historical_rule, ""])
        else:
            lines.extend(
                [
                    "#load-if-not-defined DIFFICULTY-EXTREME",
                    historical_rule,
                    "#end-if",
                    "",
                    "#load-if-defined DIFFICULTY-EXTREME",
                    extreme_rule,
                    "#end-if",
                    "",
                ]
            )
        lines.extend(["#end-if", ""])
    return "\n".join(lines).rstrip() + "\n\n"


def available_constants() -> set[str]:
    constants: set[str] = set()
    pattern = re.compile(r"^\s*\(defconst\s+([^\s)]+)", re.MULTILINE)
    for path in AI_ROOT.glob("*.per"):
        constants.update(pattern.findall(path.read_text(encoding="utf-8-sig")))
    return constants


def read_focus_rows() -> dict[str, dict[str, str]]:
    sheets = read_sheets(FOCUS_PATH)
    if len(sheets) != 1:
        raise ValueError("unit-focus workbook must contain exactly one sheet")
    rows = sheets[0]["rows"]
    if not isinstance(rows, list) or not rows:
        raise ValueError("unit-focus workbook is empty")
    header = rows[0]
    if not isinstance(header, list):
        raise ValueError("unit-focus workbook has no header")
    focus: dict[str, dict[str, str]] = {}
    for row in rows[1:]:
        if not isinstance(row, list) or not row:
            continue
        padded = row + [""] * (len(header) - len(row))
        focus[str(padded[0])] = {
            str(column): str(value) for column, value in zip(header, padded, strict=True)
        }
    return focus


def is_focused(value: str) -> bool:
    return bool(value.strip()) and value.strip().lower() != "no"


def unit_is_focused(unit: str, column: str, value: str) -> bool:
    if not is_focused(value):
        return False
    allowlist = FOCUS_VALUE_UNIT_ALLOWLISTS.get((column, value.strip().lower()))
    return allowlist is None or unit in allowlist


def validate_profile(
    civ: str,
    strategy: dict[str, object],
    constants: set[str],
) -> None:
    for key, count in (("specialties", 3), ("early", 4), ("late", 4)):
        values = strategy.get(key)
        if not isinstance(values, list) or len(values) != count:
            raise ValueError(f"{civ}.{key} must contain exactly {count} values")
        unknown = [value for value in values if value not in constants]
        if unknown:
            raise ValueError(f"{civ}.{key} has unknown constants: {unknown}")
    support = strategy.get("support")
    if not isinstance(support, list) or len(support) > 2:
        raise ValueError(f"{civ}.support must contain zero to two values")
    unknown_support = [value for value in support if value not in constants]
    if unknown_support:
        raise ValueError(f"{civ}.support has unknown constants: {unknown_support}")
    rush = strategy.get("rush")
    if not isinstance(rush, dict) or not set(rush).issubset(RUSH_GOALS):
        raise ValueError(f"{civ}.rush has unsupported keys")
    if any(not isinstance(value, int) or value < 0 or value > 4 for value in rush.values()):
        raise ValueError(f"{civ}.rush values must be integers from 0 through 4")


def historical_profile(
    strategy: dict[str, object],
    override: dict[str, object],
) -> dict[str, object]:
    profile = dict(strategy)
    profile.update(override)
    return profile


def validate_config(
    config: dict[str, dict[str, object]],
    historical_overrides: dict[str, dict[str, object]],
) -> None:
    expected = {path.stem.removeprefix("rawai-civ-") for path in AI_ROOT.glob("rawai-civ-*.per")}
    actual = set(config)
    if expected != actual:
        raise ValueError(
            f"strategy/file mismatch: missing={sorted(expected - actual)}, "
            f"extra={sorted(actual - expected)}"
        )
    unknown_overrides = set(historical_overrides) - actual
    if unknown_overrides:
        raise ValueError(f"historical overrides have unknown civilizations: {sorted(unknown_overrides)}")
    if set(ENEMY_CIV_SYMBOLS) != actual:
        raise ValueError(
            "strategy/enemy-symbol mismatch: "
            f"missing={sorted(actual - set(ENEMY_CIV_SYMBOLS))}, "
            f"extra={sorted(set(ENEMY_CIV_SYMBOLS) - actual)}"
        )

    constants = available_constants()
    focus_rows = read_focus_rows()
    expected_sheet_rows = set(CIV_SHEET_NAMES.values())
    if set(focus_rows) != expected_sheet_rows:
        raise ValueError(
            "strategy/focus-sheet mismatch: "
            f"missing={sorted(expected_sheet_rows - set(focus_rows))}, "
            f"extra={sorted(set(focus_rows) - expected_sheet_rows)}"
        )
    for civ, strategy in config.items():
        validate_profile(civ, strategy, constants)
        historical = historical_profile(strategy, historical_overrides.get(civ, {}))
        validate_profile(f"{civ}.historical", historical, constants)
        for profile_name, profile in (("extreme", strategy), ("historical", historical)):
            for key in ("early", "late", "support"):
                values = profile[key]
                assert isinstance(values, list)
                unknown_trainers = [value for value in values if value not in TRAIN_GOALS]
                if unknown_trainers:
                    raise ValueError(
                        f"{civ}.{profile_name}.{key} has no training-goal mapping: "
                        f"{unknown_trainers}"
                    )
        civ_focus = focus_rows[CIV_SHEET_NAMES[civ]]
        for key in ("early", "late", "support"):
            values = strategy[key]
            assert isinstance(values, list)
            for unit in values:
                column = UNIT_FOCUS_COLUMNS.get(str(unit))
                if column is None:
                    raise ValueError(f"{civ}.{key} has an unmapped unit category: {unit}")
                if not unit_is_focused(str(unit), column, civ_focus[column]):
                    raise ValueError(
                        f"{civ}.{key} uses {unit}, but {column} is "
                        f"'{civ_focus[column]}' in the unit-focus workbook"
                    )
        specialties = strategy["specialties"]
        assert isinstance(specialties, list)
        for specialty in specialties:
            columns = SPECIALTY_FOCUS_COLUMNS.get(str(specialty))
            # Unique, defensive, and advanced-weapon specialties have no direct
            # column in the agreed workbook and are allowed as tactical tags.
            if columns is not None and not any(
                is_focused(civ_focus[column]) for column in columns
            ):
                raise ValueError(
                    f"{civ}.specialties uses {specialty}, but its focus columns "
                    f"are not enabled in the unit-focus workbook"
                )
        rush = strategy["rush"]
        assert isinstance(rush, dict)
        for name, affinity in rush.items():
            if int(affinity) <= 0:
                continue
            unit = RUSH_FOCUS_UNITS.get(name)
            # Fast-age and tower openings are timing/structure strategies and
            # do not select a focus-sheet unit category directly.
            if unit is None:
                continue
            if unit == "SIEGE":
                if not is_focused(civ_focus["Siege"]):
                    raise ValueError(
                        f"{civ}.rush uses {name}, but Siege is "
                        f"'{civ_focus['Siege']}' in the unit-focus workbook"
                    )
                continue
            column = UNIT_FOCUS_COLUMNS[unit]
            if not unit_is_focused(unit, column, civ_focus[column]):
                raise ValueError(
                    f"{civ}.rush uses {name} ({unit}), but {column} is "
                    f"'{civ_focus[column]}' in the unit-focus workbook"
                )


def replace_once(pattern: str, replacement: str, text: str, label: str) -> str:
    updated, count = re.subn(pattern, replacement, text, count=1, flags=re.DOTALL)
    if count != 1:
        raise ValueError(f"expected one {label} block, found {count}")
    return updated


def update_civ_file(
    path: Path,
    civ: str,
    historical: dict[str, object],
    extreme: dict[str, object],
    historical_profiles: dict[str, dict[str, object]],
    extreme_profiles: dict[str, dict[str, object]],
    write: bool,
) -> bool:
    raw = path.read_bytes().decode("utf-8-sig")
    newline = "\r\n" if "\r\n" in raw else "\n"
    text = raw.replace("\r\n", "\n")

    specialties = specialty_block(historical, extreme)
    text = replace_once(
        r";define (?:difficulty-specific )?civ specialties.*?(?=;Define unique unit properties)",
        specialties,
        text,
        f"{path.name} specialties",
    )

    rush = rush_block(historical, extreme)
    if ";default rush affinities" in text or ";difficulty-specific rush affinities" in text:
        text = replace_once(
            r";(?:default|difficulty-specific) rush affinities.*?(?=;(?:enemy civs will alter rush affinities|enemy-specific opening adjustments))",
            rush,
            text,
            f"{path.name} rush",
        )
    else:
        marker = ";enemy civs will alter rush affinities"
        if marker not in text:
            raise ValueError(f"{path.name}: missing enemy-affinity marker")
        text = text.replace(marker, rush + marker, 1)

    matchups = matchup_block(
        civ,
        historical,
        extreme,
        historical_profiles,
        extreme_profiles,
    )
    text = replace_once(
        r";(?:enemy civs will alter rush affinities|enemy-specific opening adjustments).*?(?=;civ specific unit preferences)",
        matchups,
        text,
        f"{path.name} enemy matchups",
    )

    preferences = unit_preference_block(historical, extreme)
    if ";civ specific unit preferences" in text:
        text = replace_once(
            r";civ specific unit preferences.*?(?=;civ specific structure preferences)",
            preferences,
            text,
            f"{path.name} unit preferences",
        )
    else:
        marker = ";civ specific structure preferences"
        if marker not in text:
            raise ValueError(f"{path.name}: missing structure-preference marker")
        text = text.replace(marker, preferences + marker, 1)

    output = text.replace("\n", newline)
    changed = output != raw
    if changed and write:
        path.write_bytes(output.encode("utf-8"))
    return changed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="Apply validated updates")
    args = parser.parse_args()

    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    historical_overrides = json.loads(HISTORICAL_CONFIG_PATH.read_text(encoding="utf-8"))
    validate_config(config, historical_overrides)
    historical_profiles = {
        civ: historical_profile(strategy, historical_overrides.get(civ, {}))
        for civ, strategy in config.items()
    }
    changed = []
    for civ, strategy in config.items():
        path = AI_ROOT / f"rawai-civ-{civ}.per"
        historical = historical_profiles[civ]
        if update_civ_file(
            path,
            civ,
            historical,
            strategy,
            historical_profiles,
            config,
            args.write,
        ):
            changed.append(path.name)
    mode = "updated" if args.write else "would update"
    print(json.dumps({"mode": mode, "count": len(changed), "files": changed}, indent=2))


if __name__ == "__main__":
    main()
