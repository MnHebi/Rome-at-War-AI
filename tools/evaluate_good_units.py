#!/usr/bin/env python3
"""Build the data-backed civilization unit evaluation used by the AI workbook.

The Rome at War data mod is deliberately an external input.  This script emits
AI-side knowledge only: availability, fully upgraded combat statistics, and a
documented rating.  It does not copy the DAT or tech-tree payload into the AI
repository.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = REPO_ROOT.parent.parent


CIV_KEYS = {
    1: "armenia",
    2: "athenians",
    3: "britons",
    4: "carthagians",
    5: "cretans",
    6: "dacians",
    7: "egyptians",
    8: "gauls",
    9: "germani",
    10: "goths",
    11: "huns",
    12: "iberians",
    13: "illyrians",
    14: "judeans",
    15: "macedonians",
    16: "nubians",
    17: "numidians",
    18: "parthians",
    19: "persians",
    20: "phoenicians",
    21: "picts",
    22: "pontus",
    23: "romeemp",
    24: "romerep",
    25: "scythians",
    26: "seleucids",
    27: "spartans",
    28: "syracusans",
    29: "thracians",
    30: "nanda",
    31: "mauryans",
    32: "kushans",
    33: "gupta",
    34: "han",
}


DISPLAY_ORDER = [
    "armenia",
    "athenians",
    "britons",
    "carthagians",
    "cretans",
    "dacians",
    "egyptians",
    "gauls",
    "germani",
    "goths",
    "gupta",
    "han",
    "huns",
    "iberians",
    "illyrians",
    "judeans",
    "kushans",
    "macedonians",
    "mauryans",
    "nanda",
    "nubians",
    "numidians",
    "parthians",
    "persians",
    "phoenicians",
    "picts",
    "pontus",
    "romeemp",
    "romerep",
    "scythians",
    "seleucids",
    "spartans",
    "syracusans",
    "thracians",
]


DISPLAY_NAMES = {
    "armenia": "Armenians",
    "athenians": "Athenians",
    "britons": "Britons",
    "carthagians": "Carthaginians",
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
    "persians": "Persians",
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


TREE_ID_TO_KEY = {
    "ARMENIANS": "armenia",
    "ATHENIANS": "athenians",
    "BRITONS": "britons",
    "CARTHAGINIANS": "carthagians",
    "CRETANS": "cretans",
    "DACIANS": "dacians",
    "EGYPTIANS": "egyptians",
    "GAULS": "gauls",
    "GERMANI": "germani",
    "GOTHS": "goths",
    "GUPTA": "gupta",
    "HAN EMPIRE": "han",
    "HUNS": "huns",
    "IBERIANS": "iberians",
    "ILLYRIANS": "illyrians",
    "JUDEANS": "judeans",
    "KUSHAN": "kushans",
    "MACEDONIANS": "macedonians",
    "MAURYANS": "mauryans",
    "NANDA": "nanda",
    "NUBIANS": "nubians",
    "NUMIDIANS": "numidians",
    "PARTHIANS": "parthians",
    "PERSIANS": "persians",
    "PHOENICIANS": "phoenicians",
    "PICTS": "picts",
    "PONTUS": "pontus",
    "ROMAN EMPIRE": "romeemp",
    "ROMAN REPUBLIC": "romerep",
    "SCYTHIANS": "scythians",
    "SELEUCIDS": "seleucids",
    "SPARTANS": "spartans",
    "SYRACUSANS": "syracusans",
    "THRACIANS": "thracians",
}


HOST_NAMES = {
    "armenia": "Berbers",
    "athenians": "Lithuanians",
    "britons": "Britons",
    "carthagians": "Portuguese",
    "cretans": "Vietnamese",
    "dacians": "Ethiopians",
    "egyptians": "Aztecs",
    "gauls": "Franks",
    "germani": "Teutons",
    "goths": "Goths",
    "gupta": "Gurjaras",
    "han": "Chinese",
    "huns": "Huns",
    "iberians": "Spanish",
    "illyrians": "Bulgarians",
    "judeans": "Saracens",
    "kushans": "Indians",
    "macedonians": "Koreans",
    "mauryans": "Bengalis",
    "nanda": "Dravidians",
    "nubians": "Mayans",
    "numidians": "Incas",
    "parthians": "Turks",
    "persians": "Persians",
    "phoenicians": "Mongols",
    "picts": "Celts",
    "pontus": "Khmer",
    "romeemp": "Byzantines",
    "romerep": "Italians",
    "scythians": "Cumans",
    "seleucids": "Burmese",
    "spartans": "Japanese",
    "syracusans": "Malay",
    "thracians": "Malians",
}


# Standard research used to define a fully upgraded reference unit.  Unit-line
# upgrades are represented by each category's final_unit_ids.
INFANTRY_TECHS = (67, 68, 75, 74, 76, 77, 215)
ARCHER_TECHS = (199, 200, 201, 211, 212, 219, 47, 93, 437)
MOUNTED_ARCHER_TECHS = ARCHER_TECHS + (39, 435, 436)
CAVALRY_TECHS = (67, 68, 75, 81, 82, 80, 39, 435)
SIEGE_TECHS = (377,)


@dataclass(frozen=True)
class Category:
    name: str
    unit_ids: tuple[int, ...]
    reference_unit_id: int
    final_unit_ids: tuple[int, ...]
    required_techs: tuple[int, ...]
    damage_class: int
    profile: str
    parthian_sensitive: bool = False


CATEGORIES = (
    Category("Militia", (567, 1809, 473, 1808, 77, 1807, 75, 1806, 74, 1805), 567, (567, 1809), INFANTRY_TECHS, 4, "melee"),
    Category("Spearmen", (359, 1812, 2446, 2040, 358, 1811, 93, 1810), 359, (359, 1812, 2446, 2040), INFANTRY_TECHS, 4, "melee"),
    Category("Archer", (492, 24, 4), 492, (492,), ARCHER_TECHS, 3, "ranged"),
    Category("Skirmisher", (6, 7), 6, (6,), ARCHER_TECHS, 3, "ranged"),
    # Seleucid Aphraktos (2017) is a manifest-listed unique family and belongs
    # in UU Type, not in the generic cavalry-archer score.
    Category("Cavalry Archer", (474, 39), 474, (474,), MOUNTED_ARCHER_TECHS, 3, "mounted_ranged", True),
    Category("Camel Archer", (1836, 1835), 1836, (1836,), MOUNTED_ARCHER_TECHS, 3, "mounted_ranged", True),
    Category("Elephant Archer", (875, 873), 875, (875,), MOUNTED_ARCHER_TECHS, 3, "mounted_ranged", True),
    Category("Chariot Archer", (2042,), 2042, (2042,), MOUNTED_ARCHER_TECHS, 3, "mounted_ranged", True),
    Category("Light Cavalry", (441, 546, 448), 441, (441,), CAVALRY_TECHS, 4, "melee"),
    # Ratha is the regional cavalry replacement for Mauryans and Nanda.  It is
    # eligible for category scoring, but does not receive the generic line's
    # automatic "complete final unit" qualification.
    Category("Cavalry", (569, 283, 38, 1740, 1738), 569, (569,), CAVALRY_TECHS, 4, "melee"),
    Category("Camel Rider", (330, 329), 330, (330,), CAVALRY_TECHS, 4, "melee"),
    Category("Battle Elephant", (1134, 1132), 1134, (1134,), CAVALRY_TECHS, 4, "melee"),
    Category("Chariot", (1372, 1370), 1372, (1372,), CAVALRY_TECHS, 4, "melee"),
    Category("Battering Ram", (548, 422, 35, 1258), 548, (548,), SIEGE_TECHS, 11, "ram"),
    Category("Armored Elephant", (1746, 1744), 1746, (1746,), SIEGE_TECHS, 11, "ram"),
    Category("Mangonel", (588, 550, 280), 588, (588,), SIEGE_TECHS, 4, "siege_ranged"),
    Category("Scorpion", (542, 279), 542, (542,), SIEGE_TECHS, 3, "siege_ranged"),
    Category("Catapult", (36,), 36, (36,), SIEGE_TECHS, 4, "siege_ranged"),
)


RATING_ORDER = {"No": 0, "Bad": 1, "Mediocre": 2, "Good": 3, "Excellent": 4}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-root",
        type=Path,
        default=WORKSPACE_ROOT / "RaW data fix",
        help="Path to the external Rome at War data mod",
    )
    parser.add_argument(
        "--genieutils",
        type=Path,
        default=WORKSPACE_ROOT / "tools" / "vendor",
        help="Path containing the vendored genieutils package",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=REPO_ROOT / "good-unit-evaluations.json",
    )
    return parser.parse_args()


def load_affinities(path: Path) -> dict[str, dict[str, bool]]:
    text = path.read_text(encoding="utf-8-sig")
    blocks = re.split(r"(?=^#load-if-defined\s+)", text, flags=re.MULTILINE)
    by_host: dict[str, dict[str, bool]] = {}
    for block in blocks:
        match = re.match(r"#load-if-defined\s+([^\s]+)", block)
        if not match:
            continue
        host = match.group(1)
        priest = re.search(r"\(set-goal\s+good-priests\s+(YES|NO)\)", block)
        navy = re.search(r"\(set-goal\s+good-navy\s+(YES|NO)\)", block)
        if priest and navy:
            by_host[host] = {
                "good_priests": priest.group(1) == "YES",
                "good_navy": navy.group(1) == "YES",
            }
    return by_host


def packed_value(raw: float) -> tuple[int, float]:
    sign = -1 if raw < 0 else 1
    packed = int(round(abs(raw)))
    class_id = packed >> 8
    amount = packed & 0xFF
    return class_id, float(sign * amount)


def apply_numeric(current: float, command_type: int, value: float) -> float:
    if command_type == 0:
        return value
    if command_type == 4:
        return current + value
    if command_type == 5:
        return current * value
    return current


def base_state(unit: Any) -> dict[str, Any]:
    type50 = unit.type_50
    costs = {
        item.type: float(item.amount)
        for item in (unit.creatable.resource_costs if unit.creatable else ())
        if item.type >= 0 and item.flag
    }
    pop = 1.0
    # Population use is stored as resource-storage type 4 (normally -1), not
    # as a charged creation cost.  Later effect attribute 110 can change it.
    for item in unit.resource_storages:
        if item.type == 4:
            pop = abs(float(item.amount))
            break
    return {
        "hp": float(unit.hit_points),
        "speed": float(unit.speed or 0.0),
        "range": float(type50.max_range if type50 else 0.0),
        "minimum_range": float(type50.min_range if type50 else 0.0),
        "reload": float(type50.reload_time if type50 else 1.0),
        "accuracy": float(type50.accuracy_percent if type50 else 100.0),
        "attacks": {item.class_: float(item.amount) for item in (type50.attacks if type50 else ())},
        "armors": {item.class_: float(item.amount) for item in (type50.armours if type50 else ())},
        "costs": costs,
        "population": pop,
        "train_time": float(unit.creatable.train_locations[0].train_time) if unit.creatable and unit.creatable.train_locations else 0.0,
        "bonus_damage_resistance": float(type50.bonus_damage_resistance if type50 else 0.0),
        "blast_width": float(type50.blast_width if type50 else 0.0),
        "attack_delay_frames": int(type50.frame_delay if type50 else 0),
        "friendly_fire_damage": float(type50.friendly_fire_damage if type50 else 0.0),
    }


def command_targets(command: Any, unit_id: int, unit_class: int) -> bool:
    return command.a == unit_id or (command.a == -1 and command.b == unit_class)


def apply_effect(state: dict[str, Any], effect: Any, unit_id: int, unit_class: int) -> None:
    for command in effect.effect_commands:
        if command.type not in {0, 4, 5} or not command_targets(command, unit_id, unit_class):
            continue
        attribute = command.c
        if attribute == 0:
            state["hp"] = apply_numeric(state["hp"], command.type, command.d)
        elif attribute == 5:
            state["speed"] = apply_numeric(state["speed"], command.type, command.d)
        elif attribute == 8:
            class_id, amount = packed_value(command.d)
            state["armors"][class_id] = apply_numeric(
                state["armors"].get(class_id, 0.0), command.type, amount
            )
        elif attribute == 9:
            class_id, amount = packed_value(command.d)
            if command.type == 5:
                # Multiplicative attack effects encode the multiplier as an
                # integer percentage in the low byte (e.g. 0x0B78 = 120%).
                amount = abs(amount) / 100.0
                if command.d < 0:
                    amount = 1.0 / amount if amount else 1.0
            state["attacks"][class_id] = apply_numeric(
                state["attacks"].get(class_id, 0.0), command.type, amount
            )
        elif attribute == 10:
            state["reload"] = apply_numeric(state["reload"], command.type, command.d)
        elif attribute == 11:
            state["accuracy"] = apply_numeric(state["accuracy"], command.type, command.d)
        elif attribute == 12:
            state["range"] = apply_numeric(state["range"], command.type, command.d)
        elif attribute == 20:
            state["minimum_range"] = apply_numeric(state["minimum_range"], command.type, command.d)
        elif attribute == 24:
            state["bonus_damage_resistance"] = apply_numeric(
                state["bonus_damage_resistance"], command.type, command.d
            )
        elif attribute == 100:
            for resource in tuple(state["costs"]):
                if resource != 4:
                    state["costs"][resource] = apply_numeric(
                        state["costs"][resource], command.type, command.d
                    )
        elif attribute == 101:
            state["train_time"] = apply_numeric(state["train_time"], command.type, command.d)
        elif attribute in {103, 104, 105, 106}:
            resource = {103: 0, 104: 1, 105: 3, 106: 2}[attribute]
            state["costs"][resource] = apply_numeric(
                state["costs"].get(resource, 0.0), command.type, command.d
            )
        elif attribute == 110:
            # Negative values are the DAT convention for fractional population
            # use: -0.75 means the unit occupies 0.75 population.
            state["population"] = abs(float(command.d))


def disabled_techs(effect: Any) -> set[int]:
    return {
        int(round(command.d))
        for command in effect.effect_commands
        if command.type == 102 and command.d >= 0
    }


def available_nodes(tree: dict[str, Any], technology_count: int) -> tuple[set[int], set[int], dict[int, str]]:
    units: set[int] = set()
    techs: set[int] = set()
    names: dict[int, str] = {}
    for group in (tree.get("civ_techs_units", []), tree.get("civ_techs_buildings", [])):
        for node in group:
            node_id = int(node.get("Node ID", -1))
            if node_id < 0:
                continue
            if node.get("Node Status") == "NotAvailable":
                continue
            if node.get("Use Type") == "Unit":
                units.add(node_id)
                names[node_id] = node.get("Name", "")
            elif node.get("Use Type") == "Tech":
                # Some exported tree nodes are virtual UI technologies (for
                # example Poisoned Arrows 31101) and have no DAT technology.
                # They cannot be applied as research effects here.
                if node_id < technology_count:
                    techs.add(node_id)
    return units, techs, names


def compatible_tech_packages(data: Any, visible: set[int], disabled: set[int]) -> list[set[int]]:
    """Return strongest legal visible-tech packages without combining exclusions."""
    active = {tech_id for tech_id in visible if 0 <= tech_id < len(data.techs) and tech_id not in disabled}
    conflicts: dict[int, set[int]] = {tech_id: set() for tech_id in active}
    for tech_id in active:
        effect_id = data.techs[tech_id].effect_id
        if not 0 <= effect_id < len(data.effects):
            continue
        for command in data.effects[effect_id].effect_commands:
            if command.type != 102 or command.d < 0:
                continue
            other = int(round(command.d))
            if other in active and other != tech_id:
                conflicts[tech_id].add(other)
                conflicts[other].add(tech_id)

    contested = {tech_id for tech_id, peers in conflicts.items() if peers}
    base = active - contested
    components: list[set[int]] = []
    unseen = set(contested)
    while unseen:
        seed = unseen.pop()
        component = {seed}
        frontier = [seed]
        while frontier:
            current = frontier.pop()
            for peer in conflicts[current]:
                if peer not in component:
                    component.add(peer)
                    unseen.discard(peer)
                    frontier.append(peer)
        components.append(component)

    choices: list[list[set[int]]] = []
    for component in components:
        members = sorted(component)
        if len(members) > 16:
            # No current Rome at War choice group approaches this size.  Keep
            # a safe deterministic fallback rather than exploding 2^n.
            choices.append([{member} for member in members])
            continue
        independent: list[set[int]] = []
        for mask in range(1, 1 << len(members)):
            selection = {members[index] for index in range(len(members)) if mask & (1 << index)}
            if any(conflicts[item] & selection for item in selection):
                continue
            if any(not (conflicts[item] & selection) for item in component - selection):
                continue
            independent.append(selection)
        choices.append(independent or [set()])

    if not choices:
        return [base]
    return [base | set().union(*selection) for selection in itertools.product(*choices)]


def auto_tech_closure(data: Any, civ_id: int, researched: set[int], disabled: set[int]) -> set[int]:
    result = set(researched)
    changed = True
    while changed:
        changed = False
        for tech_id, tech in enumerate(data.techs):
            if tech_id in result or tech_id in disabled or tech.effect_id < 0:
                continue
            if tech.civ not in {-1, civ_id}:
                continue
            if not any(location.location_id == -1 for location in tech.research_locations):
                continue
            prerequisites = [value for value in tech.required_techs if value >= 0]
            required_count = max(0, int(tech.required_tech_count))
            if required_count == 0:
                # Location -1 also marks effects that are enabled explicitly
                # by other effects.  A zero-prerequisite hidden technology is
                # not an automatic research trigger by itself.
                continue
            if sum(value in result for value in prerequisites) >= required_count:
                result.add(tech_id)
                changed = True
    return result


def state_for_unit(data: Any, civ_id: int, unit_id: int, tech_ids: set[int]) -> dict[str, Any]:
    unit = data.civs[civ_id].units[unit_id]
    if unit is None:
        raise ValueError(f"{data.civs[civ_id].name}: missing unit {unit_id}")
    state = base_state(unit)
    civ = data.civs[civ_id]
    apply_effect(state, data.effects[civ.tech_tree_id], unit_id, unit.class_)
    if 0 <= civ.team_bonus_id < len(data.effects):
        apply_effect(state, data.effects[civ.team_bonus_id], unit_id, unit.class_)
    for tech_id in sorted(tech_ids):
        if not 0 <= tech_id < len(data.techs):
            continue
        tech = data.techs[tech_id]
        if 0 <= tech.effect_id < len(data.effects):
            apply_effect(state, data.effects[tech.effect_id], unit_id, unit.class_)
    return state


def reference_state(data: Any, category: Category) -> dict[str, Any]:
    unit = data.civs[0].units[category.reference_unit_id]
    if unit is None:
        raise ValueError(f"Gaia reference missing unit {category.reference_unit_id}")
    state = base_state(unit)
    for tech_id in category.required_techs:
        tech = data.techs[tech_id]
        if 0 <= tech.effect_id < len(data.effects):
            apply_effect(state, data.effects[tech.effect_id], category.reference_unit_id, unit.class_)
    return state


def resource_cost(state: dict[str, Any]) -> float:
    weights = {0: 1.0, 1: 1.0, 2: 1.2, 3: 1.1}
    return sum(max(0.0, amount) * weights.get(resource, 1.0) for resource, amount in state["costs"].items())


def durability(state: dict[str, Any]) -> float:
    melee = state["armors"].get(4, 0.0)
    pierce = state["armors"].get(3, 0.0)
    melee_factor = 15.0 / max(1.0, 15.0 - melee)
    pierce_factor = 10.0 / max(1.0, 10.0 - pierce)
    resistance = max(-0.75, min(0.75, state.get("bonus_damage_resistance", 0.0)))
    return state["hp"] * ((melee_factor + pierce_factor) / 2.0) * max(0.25, 1.0 + resistance)


def dps(state: dict[str, Any], category: Category) -> float:
    damage_class = category.damage_class
    damage = max(0.1, state["attacks"].get(damage_class, 0.0))
    bonus = sum(
        max(0.0, amount)
        for class_id, amount in state["attacks"].items()
        if class_id != damage_class
    )
    bonus_weight = {
        "Spearmen": 0.55,
        "Skirmisher": 0.55,
        "Battering Ram": 0.40,
        "Armored Elephant": 0.40,
        "Scorpion": 0.25,
        "Mangonel": 0.20,
        "Catapult": 0.20,
    }.get(category.name, 0.10)
    accuracy = max(0.1, min(1.0, state["accuracy"] / 100.0)) if state["range"] > 0 else 1.0
    return (damage + bonus_weight * bonus) * accuracy / max(0.1, state["reload"])


def combat_ratio(state: dict[str, Any], reference: dict[str, Any], category: Category, has_parthian: bool) -> float:
    weights = {
        "melee": (0.50, 0.40, 0.00, 0.10),
        "ranged": (0.30, 0.35, 0.30, 0.05),
        "mounted_ranged": (0.25, 0.30, 0.30, 0.15),
        "ram": (0.35, 0.45, 0.00, 0.20),
        "siege_ranged": (0.25, 0.35, 0.35, 0.05),
    }[category.profile]
    durability_weight, dps_weight, range_weight, speed_weight = weights
    range_ratio = max(0.5, state["range"]) / max(0.5, reference["range"])
    range_deficit = max(0.0, reference["range"] - state["range"])
    if range_deficit >= 0.75:
        range_ratio *= max(0.55, 1.0 - 0.10 * math.ceil(range_deficit))
    minimum_range_penalty = max(0.70, 1.0 - 0.05 * max(0.0, state["minimum_range"] - reference["minimum_range"]))
    result = (
        (durability(state) / max(0.1, durability(reference))) ** durability_weight
        * (dps(state, category) / max(0.1, dps(reference, category))) ** dps_weight
        * ((range_ratio * minimum_range_penalty) ** range_weight)
        * ((max(0.1, state["speed"]) / max(0.1, reference["speed"])) ** speed_weight)
    )
    if category.parthian_sensitive and not has_parthian:
        result *= 0.82
    return result


def serialize_state(state: dict[str, Any], category: Category) -> dict[str, Any]:
    return {
        "hp": round(state["hp"], 2),
        "attack": round(state["attacks"].get(category.damage_class, 0.0), 2),
        "bonus_damage_total": round(
            sum(max(0.0, amount) for class_id, amount in state["attacks"].items() if class_id != category.damage_class),
            2,
        ),
        "damage_class": category.damage_class,
        "melee_armor": round(state["armors"].get(4, 0.0), 2),
        "pierce_armor": round(state["armors"].get(3, 0.0), 2),
        "range": round(state["range"], 2),
        "minimum_range": round(state["minimum_range"], 2),
        "speed": round(state["speed"], 3),
        "reload_time": round(state["reload"], 3),
        "accuracy": round(state["accuracy"], 2),
        "food_cost": round(state["costs"].get(0, 0.0), 2),
        "wood_cost": round(state["costs"].get(1, 0.0), 2),
        "gold_cost": round(state["costs"].get(3, 0.0), 2),
        "stone_cost": round(state["costs"].get(2, 0.0), 2),
        "population": round(state["population"], 3),
        "train_time": round(state["train_time"], 2),
        "blast_width": round(state["blast_width"], 2),
        "attack_delay_frames": state["attack_delay_frames"],
        "friendly_fire_damage": round(state["friendly_fire_damage"], 2),
    }


def rate_category(
    data: Any,
    civ_id: int,
    category: Category,
    available_units: set[int],
    research_packages: list[set[int]],
    names: dict[int, str],
    reference: dict[str, Any],
) -> dict[str, Any]:
    candidates = [unit_id for unit_id in category.unit_ids if unit_id in available_units]
    if not candidates:
        return {"rating": "No", "reason": "The unit family is not available in this civilization's validated tech tree."}

    evaluated = []
    for package_index, package in enumerate(research_packages):
        has_parthian = 436 in package
        for unit_id in candidates:
            state = state_for_unit(data, civ_id, unit_id, package)
            ratio = combat_ratio(state, reference, category, has_parthian)
            missing = [tech_id for tech_id in category.required_techs if tech_id not in package]
            full = unit_id in category.final_unit_ids and not missing
            ref_cost = resource_cost(reference)
            actual_cost = resource_cost(state)
            cost_multiplier = ref_cost / max(1.0, actual_cost)
            pop_multiplier = reference["population"] / max(0.05, state["population"])
            number_multiplier = max(cost_multiplier, pop_multiplier)
            number_adjusted = ratio * number_multiplier
            if full or ratio >= 1.0:
                rating = "Excellent"
            elif ratio < 0.72 and number_adjusted < 0.95:
                rating = "Bad"
            elif ratio >= 0.90 or number_adjusted >= 1.0:
                rating = "Good"
            else:
                rating = "Mediocre"
            evaluated.append(
                (
                    RATING_ORDER[rating],
                    number_adjusted,
                    ratio,
                    unit_id,
                    state,
                    package,
                    package_index,
                    missing,
                    full,
                    rating,
                    has_parthian,
                    number_multiplier,
                )
            )

    (
        _, number_adjusted, ratio, unit_id, state, researched, package_index, missing, full,
        rating, has_parthian, number_multiplier,
    ) = max(evaluated, key=lambda item: item[:3])

    reasons = []
    if full:
        reasons.append("Complete final unit and standard attack, armor, life, speed, and accuracy/range upgrade suite.")
    elif ratio >= 1.0:
        reasons.append("Missing standard upgrades are offset by final statistics at or above the fully upgraded reference threshold.")
    if category.parthian_sensitive and not has_parthian:
        reasons.append("Parthian Tactics is missing; the mounted-archer combat score receives the documented 18% penalty.")
    if number_multiplier >= 1.20:
        reasons.append("At least a 20% cost or population advantage materially improves attainable numbers.")
    if rating == "Bad":
        reasons.append("Even-number combat is below 72% of reference and cost/population advantages do not recover 95% reference efficiency.")
    elif rating == "Mediocre":
        reasons.append("The family is usable but remains below the Good combat and number-efficiency thresholds.")
    elif rating == "Good" and not reasons:
        reasons.append("The family reaches at least 90% even-number combat or full reference efficiency after cost/population advantages.")

    unit = data.civs[civ_id].units[unit_id]
    return {
        "rating": rating,
        "unit_id": unit_id,
        "unit_name": names.get(unit_id) or unit.name,
        "full_standard_upgrades": full,
        "missing_standard_tech_ids": missing,
        "has_parthian_tactics": has_parthian if category.parthian_sensitive else None,
        "selected_package_index": package_index,
        "applied_standard_tech_ids": sorted(set(category.required_techs) & researched),
        "compatible_package_count": len(research_packages),
        "combat_ratio": round(ratio, 4),
        "number_multiplier": round(number_multiplier, 4),
        "number_adjusted_ratio": round(number_adjusted, 4),
        "statistics": serialize_state(state, category),
        "reference_statistics": serialize_state(reference, category),
        "reason": " ".join(reasons),
    }


def classify_unique_types(data: Any, civ_key: str, manifest: dict[str, Any]) -> str:
    labels: set[str] = set()
    for family in manifest["civs"][civ_key]["families"]:
        family_name = family["name"].lower()
        if "elephant" in family_name:
            labels.add("Elephant")
        for unit_id in family.get("source_unit_ids", []):
            unit = data.civs[0].units[unit_id]
            if unit is None:
                continue
            if unit.class_ == 6:
                labels.add("Infantry")
            elif unit.class_ == 0:
                labels.add("Archer")
            elif unit.class_ == 36:
                labels.add("Cavalry Archer")
            elif unit.class_ in {12, 47} and "elephant" not in family_name:
                labels.add("Cavalry")
            elif unit.class_ in {13, 55}:
                labels.add("Siege")
            elif unit.class_ in {2, 20, 21, 22, 53}:
                labels.add("Navy")
    order = ["Infantry", "Archer", "Cavalry Archer", "Cavalry", "Elephant", "Siege", "Navy"]
    return "/".join(label for label in order if label in labels) or "Other"


def main() -> None:
    args = parse_args()
    sys.path.insert(0, str(args.genieutils.resolve()))
    from genieutils.datfile import DatFile  # type: ignore  # noqa: PLC0415

    dat_dir = args.data_root / "resources" / "_common" / "dat"
    dat_path = dat_dir / "empires2_x2_p1.dat"
    tree_path = dat_dir / "civTechTrees.json"
    civs_path = dat_dir / "civilizations.json"
    manifest_path = REPO_ROOT / "unique-unit-production.json"
    ai_path = REPO_ROOT / "AI RAW.per"

    for required in (dat_path, tree_path, civs_path, manifest_path, ai_path):
        if not required.exists():
            raise FileNotFoundError(required)

    data = DatFile.parse(str(dat_path))
    tree_doc = json.loads(tree_path.read_text(encoding="utf-8-sig"))
    civ_doc = json.loads(civs_path.read_text(encoding="utf-8-sig"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    affinities = load_affinities(ai_path)

    trees = tree_doc["civs"]
    trees_by_key = {TREE_ID_TO_KEY[tree["civ_id"]]: tree for tree in trees}
    civ_records = civ_doc["civilization_list"]
    if len(trees) != 34 or len(data.civs) < 35 or len(civ_records) < 35:
        raise ValueError("Expected 34 playable Rome at War civilizations")

    references = {category.name: reference_state(data, category) for category in CATEGORIES}
    civ_output: dict[str, Any] = {}
    for civ_id in range(1, 35):
        key = CIV_KEYS[civ_id]
        tree = trees_by_key[key]
        available_units, visible_techs, names = available_nodes(tree, len(data.techs))
        tree_effect = data.effects[data.civs[civ_id].tech_tree_id]
        disabled = disabled_techs(tree_effect)
        visible_packages = compatible_tech_packages(data, visible_techs | {101, 102, 103, 104}, disabled)
        research_packages = [
            auto_tech_closure(data, civ_id, package, disabled | (visible_techs - package))
            for package in visible_packages
        ]
        host_constant = civ_records[civ_id].get("data_name", "")
        host_constant = {"ETHIOPIAN-CIV": "ETHIOPIANS-CIV"}.get(host_constant, host_constant)
        affinity = affinities.get(host_constant)
        if affinity is None:
            raise ValueError(f"Missing AI affinity block for {key} ({host_constant})")

        ratings = {
            category.name: rate_category(
                data,
                civ_id,
                category,
                available_units,
                research_packages,
                names,
                references[category.name],
            )
            for category in CATEGORIES
        }
        priest_available = 125 in available_units
        shipyard_available = any(
            node.get("Building ID") == 1251 and node.get("Node Status") != "NotAvailable"
            for node in tree.get("civ_techs_buildings", [])
        )
        priest_tech_weights = {231: 1.0, 252: 1.0, 230: 1.0, 233: 1.0, 316: 1.0, 319: 1.0, 438: 0.5, 439: 0.5, 45: 0.5}
        priest_capability = max(
            (sum(weight for tech_id, weight in priest_tech_weights.items() if tech_id in package) for package in research_packages),
            default=0.0,
        )
        if not priest_available:
            priest_rating = "No"
        elif affinity["good_priests"]:
            priest_rating = "Excellent"
        elif priest_capability >= 5.0:
            priest_rating = "Good"
        elif priest_capability >= 3.5:
            priest_rating = "Mediocre"
        else:
            priest_rating = "Bad"
        ratings["Priest"] = {
            "rating": priest_rating,
            "capability_score": priest_capability,
            "reason": (
                "Priest is unavailable."
                if not priest_available
                else "Excellent follows the civilization-template good-priests affinity."
                if affinity["good_priests"]
                else f"Priest capability score {priest_capability:g}/7.5 determines the non-affinity rating."
            ),
            "source": "AI RAW.per good-priests",
        }
        ratings["Navy"] = {
            "rating": "No" if not shipyard_available else ("Excellent" if affinity["good_navy"] else "Mediocre"),
            "reason": (
                "Shipyard is unavailable."
                if not shipyard_available
                else "Excellent follows the civilization-template good-navy affinity; boarding effectiveness is not reduced to ordinary damage/armor statistics."
                if affinity["good_navy"]
                else "Naval production is available, but the civilization-template affinity does not classify it as a primary strength."
            ),
            "source": "AI RAW.per good-navy and validated Shipyard availability",
        }

        common_techs = set.intersection(*(set(package) for package in research_packages))
        civ_output[key] = {
            "civilization": DISPLAY_NAMES[key],
            "host_civilization": HOST_NAMES[key],
            "dat_civilization_id": civ_id,
            "tech_tree_id": tree["civ_id"],
            "good_priests": affinity["good_priests"],
            "good_navy": affinity["good_navy"],
            "common_researched_technology_ids": sorted(common_techs),
            "branch_technology_ids": [sorted(set(package) - common_techs) for package in research_packages],
            "unique_unit_type": classify_unique_types(data, key, manifest),
            "ratings": ratings,
        }

    output = {
        "schema_version": 1,
        "display_order": DISPLAY_ORDER,
        "source_provenance": {
            "data_mod": "External authoritative Rome at War data; payload intentionally excluded from the AI repository.",
            "empires2_x2_p1.dat_sha256": sha256(dat_path),
            "civTechTrees.json_sha256": sha256(tree_path),
            "civilizations.json_sha256": sha256(civs_path),
            "AI RAW.per_sha256": sha256(ai_path),
            "unique-unit-production.json_sha256": sha256(manifest_path),
        },
        "rubric": {
            "No": "The unit family is unavailable in the validated civilization tech tree.",
            "Excellent": "The final unit and complete standard upgrade suite are available, or fully upgraded final combat statistics reach the complete-upgrade reference threshold despite missing standard technologies.",
            "Good": "At least 90% of the reference even-number combat score, or at least 100% reference efficiency after cost/population advantages.",
            "Mediocre": "Usable, but below the Good thresholds and not weak enough to be Bad.",
            "Bad": "Below 72% of reference even-number combat and below 95% reference efficiency after the best cost or population advantage.",
            "mounted_archer_rule": "Missing Parthian Tactics applies an 18% combat-score penalty in addition to the lost armor/bonus damage represented by final statistics.",
            "priests_and_navy": "Priest affinity automatically gives Excellent; other priests use a 7.5-point capability score. Navy Excellent comes from good-navy affinity because boarding/fleet utility is not reduced to ordinary damage/armor statistics.",
        },
        "score_model": {
            "durability": "HP adjusted against representative 15 melee and 10 pierce attacks using final melee/pierce armor.",
            "damage": "Final primary and role-weighted bonus damage divided by reload time and adjusted for ranged accuracy; counter families therefore retain their defining bonus damage.",
            "range": "30-35% of ranged/siege profiles with an additional whole-tile breakpoint and minimum-range penalty; archers therefore cannot hide a serious range deficit behind one strong stat.",
            "mobility": "5-20% by profile; slower cavalry can still qualify through damage and durability.",
            "numbers": "The better of weighted resource-cost advantage and population-use advantage.",
            "doctrine_packages": "Each category records its own strongest legal mutually exclusive technology package. Cells are unit-family potential ratings, not a claim that all best branches coexist in one match.",
        },
        "category_order": [category.name for category in CATEGORIES] + ["Priest", "Navy"],
        "civilizations": civ_output,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    counts: dict[str, int] = {rating: 0 for rating in RATING_ORDER}
    for civ in civ_output.values():
        for record in civ["ratings"].values():
            counts[record["rating"]] += 1
    print(json.dumps({"output": str(args.output), "rating_counts": counts}, indent=2))


if __name__ == "__main__":
    main()
