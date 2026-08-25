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

# Naval capability is deliberately independent from the historical/template
# ``good-navy`` preference. The former answers whether a civilization can
# compete in this DAT; the latter is a strategic doctrine override: Naval Yes
# owns primary team fleets, and Naval No fields support rather than attempting
# one-for-one competition against a Naval Yes enemy, as specified by design.
NAVAL_SUPPORT_TECH_WEIGHTS = {
    374: 3.0,   # Careening
    375: 3.0,   # Dry Dock / Improved Rowing Banks
    373: 3.0,   # Shipwright
    199: 1.0,   # Fletching
    200: 1.5,   # Bodkin Arrow
    201: 2.0,   # Bracer
    93: 1.5,    # Ballistics
    47: 2.0,    # Advanced Weaponry (host Chemistry technology)
    377: 1.5,   # Siege Engineers
    1123: 1.0,  # Artillery Platforms
    45: 0.5,    # Faith (conversion resistance for boarding engagements)
}


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


@dataclass(frozen=True)
class NavalCategory:
    name: str
    # (unit id, lineup-tier multiplier).  A final Imperial hull is 1.0,
    # Middle Antiquity is normally 0.7, and an early hull is normally 0.4.
    units: tuple[tuple[int, float], ...]
    reference_unit_id: int
    weight: float
    damage_class: int
    profile: str
    upgrade_tech_ids: tuple[int, ...] = ()
    # Naval unique families share one optional eight-point lineup slot, but
    # each family must be compared with its own fully upgraded reference.
    reference_by_unit: tuple[tuple[int, int], ...] = ()


CATEGORIES = (
    Category("Militia", (567, 1809, 473, 1808, 77, 1807, 75, 1806, 74, 1805), 567, (567, 1809), INFANTRY_TECHS, 4, "melee"),
    Category("Spearmen", (359, 1812, 2446, 2040, 358, 1811, 93, 1810), 359, (359, 1812, 2446, 2040), INFANTRY_TECHS, 4, "melee"),
    # Crossbowman 5 is a separate Advanced Weaponry-era branch used by Roman
    # Imperial doctrine, not an Improved Bowman upgrade. Include it as a final
    # generic archer candidate and derive its actually applicable upgrades from
    # DAT effect targets (Marksmanship 437 does not target this unit/class).
    Category("Archer", (5, 492, 24, 4), 492, (5, 492), ARCHER_TECHS, 3, "ranged"),
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


NAVAL_CATEGORIES = (
    NavalCategory("Polyreme", ((539, 0.4), (21, 0.7), (442, 1.0)), 442, 12.0, 3, "ranged", (34, 35)),
    NavalCategory("Fire Ship", ((1103, 0.4), (529, 0.7), (532, 1.0)), 532, 10.0, 4, "fire", (34, 246)),
    NavalCategory("Demolition Ship", ((1104, 0.4), (527, 0.7), (528, 1.0)), 528, 6.0, 4, "demolition", (34, 1033, 244)),
    NavalCategory("Scout Ship", ((1877, 0.4), (1878, 0.7), (1879, 1.0)), 1879, 8.0, 3, "scout", (1007, 1008)),
    NavalCategory("Hemiolia", ((1881, 0.4), (1882, 0.7), (1883, 1.0)), 1883, 8.0, 3, "ranged", (1005, 1006)),
    NavalCategory("Boarding Ship", ((1880, 1.0),), 1880, 4.0, 3, "boarding"),
    NavalCategory("Juggernaut", ((420, 0.7), (691, 1.0)), 691, 9.0, 4, "naval_siege", (376,)),
    NavalCategory("Quadrireme/Quinquereme", ((1870, 0.7), (1750, 1.0)), 1750, 8.0, 3, "heavy_reme", (1003,)),
    NavalCategory("Octeres", ((1884, 1.0),), 1884, 7.0, 4, "naval_siege"),
    NavalCategory(
        "Naval unique unit",
        ((1923, 1.0), (2008, 0.7), (2009, 1.0)),
        1923,
        8.0,
        3,
        "naval_unique",
        (1174,),
        reference_by_unit=((1923, 1923), (2008, 2009), (2009, 2009)),
    ),
)


# Exact upgrade effects are validated against the current DAT on every
# evaluation run. Alternate gold/barrage forms are included even though only
# their canonical trainable family is scored.
NAVAL_UPGRADE_CHAINS = {
    "Polyreme": {34: ((539, 21),), 35: ((539, 442), (21, 442))},
    "Fire Ship": {34: ((1103, 529),), 246: ((529, 532), (1103, 532))},
    "Demolition Ship": {
        34: ((1104, 527),),
        1033: ((1104, 527),),
        244: ((527, 528), (1104, 528)),
    },
    "Scout Ship": {1007: ((1877, 1878),), 1008: ((1877, 1879), (1878, 1879))},
    "Hemiolia": {
        1005: ((1881, 1882), (1950, 1951)),
        1006: ((1882, 1883), (1881, 1883), (1950, 1952), (1951, 1952)),
    },
    "Boarding Ship": {},
    "Juggernaut": {376: ((420, 691), (1885, 1886))},
    "Quadrireme/Quinquereme": {1003: ((1870, 1750),)},
    "Octeres": {},
    "Naval unique unit": {1174: ((2008, 2009),)},
}

# Carthage's Cothon is exported as UI building 1854, while the authoritative
# DAT effects and the AI constant target the physical building unit 2480.  Its
# batch buttons cover the nine generic final hulls (the Boarding proxy is
# absent from Carthage's unit table in the current DAT and is therefore not
# credited).  Expanded Docking Bays changes each four-ship batch to five.
COTHON_BUILDING_UNIT_ID = 2480
COTHON_ENABLE_TECH_ID = 515
COTHON_WORK_RATE_TECH_ID = 993
COTHON_FIFTH_SHIP_TECH_ID = 994
COTHON_BATCH_SPECS = {
    "Scout Ship": (1892, 1879),
    "Polyreme": (1893, 442),
    "Fire Ship": (1894, 532),
    "Demolition Ship": (1895, 528),
    "Hemiolia": (1897, 1883),
    "Juggernaut": (1898, 691),
    "Quadrireme/Quinquereme": (1899, 1750),
    "Octeres": (1900, 1884),
}


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
        "work_rate": 1.0,
        "bonus_damage_resistance": float(type50.bonus_damage_resistance if type50 else 0.0),
        "blast_width": float(type50.blast_width if type50 else 0.0),
        "attack_delay_frames": int(type50.frame_delay if type50 else 0),
        "friendly_fire_damage": float(type50.friendly_fire_damage if type50 else 0.0),
        "projectile_count": max(
            1.0,
            float(unit.creatable.total_projectiles)
            if unit.creatable and unit.creatable.total_projectiles
            else 1.0,
        ),
        "max_projectile_count": max(
            1.0,
            float(unit.creatable.max_total_projectiles)
            if unit.creatable and unit.creatable.max_total_projectiles
            else 1.0,
        ),
        "garrison_capacity": float(unit.garrison_capacity),
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
        elif attribute == 2:
            state["garrison_capacity"] = apply_numeric(
                state["garrison_capacity"], command.type, command.d
            )
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
        elif attribute == 13:
            state["work_rate"] = apply_numeric(state["work_rate"], command.type, command.d)
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
    required_garrison = max(0.0, state["max_projectile_count"] - state["projectile_count"])
    operational_projectiles = max(
        state["projectile_count"],
        state["max_projectile_count"]
        * state["population"]
        / max(0.05, state["population"] + required_garrison),
    )
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
        "projectile_count": round(state["projectile_count"], 2),
        "max_projectile_count": round(state["max_projectile_count"], 2),
        "operational_projectile_factor": round(operational_projectiles, 4),
        "garrison_capacity": round(state["garrison_capacity"], 2),
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
            # Crossbowman is a separate branch with fixed attack statistics.
            # Padded/Leather/Ring armor and Ballistics apply; the three generic
            # archer attack/range upgrades and Marksmanship do not target it.
            applicable_techs = (
                (93, 211, 212, 219)
                if category.name == "Archer" and unit_id == 5
                else category.required_techs
            )
            missing = [tech_id for tech_id in applicable_techs if tech_id not in package]
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
                    applicable_techs,
                )
            )

    (
        _, number_adjusted, ratio, unit_id, state, researched, package_index, missing, full,
        rating, has_parthian, number_multiplier, applicable_techs,
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
        "applied_standard_tech_ids": sorted(set(applicable_techs) & researched),
        "compatible_package_count": len(research_packages),
        "combat_ratio": round(ratio, 4),
        "number_multiplier": round(number_multiplier, 4),
        "number_adjusted_ratio": round(number_adjusted, 4),
        "statistics": serialize_state(state, category),
        "reference_statistics": serialize_state(reference, category),
        "reason": " ".join(reasons),
    }


def naval_reference_state(data: Any, category: NavalCategory, unit_id: int) -> dict[str, Any]:
    reference_id = dict(category.reference_by_unit).get(unit_id, category.reference_unit_id)
    unit = data.civs[0].units[reference_id]
    if unit is None:
        raise ValueError(f"Gaia naval reference missing unit {reference_id}")
    state = base_state(unit)
    for tech_id in (101, 102, 103, 104):
        tech = data.techs[tech_id]
        if 0 <= tech.effect_id < len(data.effects):
            apply_effect(state, data.effects[tech.effect_id], reference_id, unit.class_)
    for tech_id in NAVAL_SUPPORT_TECH_WEIGHTS:
        tech = data.techs[tech_id]
        if 0 <= tech.effect_id < len(data.effects):
            apply_effect(state, data.effects[tech.effect_id], reference_id, unit.class_)
    return state


def naval_throughput_reference_state(data: Any, unit_id: int) -> dict[str, Any]:
    """Return the same hull without civ-specific production-speed bonuses."""
    unit = data.civs[0].units[unit_id]
    if unit is None:
        raise ValueError(f"Gaia naval throughput reference missing unit {unit_id}")
    state = base_state(unit)
    for tech_id in (101, 102, 103, 104):
        tech = data.techs[tech_id]
        if 0 <= tech.effect_id < len(data.effects):
            apply_effect(state, data.effects[tech.effect_id], unit_id, unit.class_)
    for tech_id in NAVAL_SUPPORT_TECH_WEIGHTS:
        tech = data.techs[tech_id]
        if 0 <= tech.effect_id < len(data.effects):
            apply_effect(state, data.effects[tech.effect_id], unit_id, unit.class_)
    # Conscription is the universal production-rate baseline. It is not part of
    # the 20-point naval combat/support-upgrade component, but omitting it here
    # would misclassify its ordinary 33% Shipyard rate as a civilization bonus.
    conscription = data.techs[315]
    if 0 <= conscription.effect_id < len(data.effects):
        apply_effect(state, data.effects[conscription.effect_id], unit_id, unit.class_)
    return state


def validate_naval_upgrade_chains(data: Any) -> None:
    """Fail evaluation when a hard-coded naval line no longer matches the DAT."""
    category_names = {category.name for category in NAVAL_CATEGORIES}
    if set(NAVAL_UPGRADE_CHAINS) != category_names:
        raise ValueError("Naval upgrade metadata does not cover every scored ship class")
    expected_triples: set[tuple[int, int, int]] = set()
    naval_members = {
        unit_id for category in NAVAL_CATEGORIES for unit_id, _ in category.units
    }
    for class_name, technologies in NAVAL_UPGRADE_CHAINS.items():
        for tech_id, expected_pairs in technologies.items():
            if not 0 <= tech_id < len(data.techs):
                raise ValueError(f"{class_name}: upgrade technology {tech_id} is outside the DAT")
            technology = data.techs[tech_id]
            if not 0 <= technology.effect_id < len(data.effects):
                raise ValueError(f"{class_name}: upgrade technology {tech_id} has no valid effect")
            actual_pairs = {
                (int(command.a), int(command.b))
                for command in data.effects[technology.effect_id].effect_commands
                if command.type == 3
            }
            missing = set(expected_pairs) - actual_pairs
            if missing:
                raise ValueError(
                    f"{class_name}: DAT technology {tech_id} is missing upgrade pairs {sorted(missing)}"
                )
            for source, target in expected_pairs:
                expected_triples.add((tech_id, source, target))
                naval_members.update((source, target))

    actual_triples: set[tuple[int, int, int]] = set()
    for tech_id, technology in enumerate(data.techs):
        if not 0 <= technology.effect_id < len(data.effects):
            continue
        for command in data.effects[technology.effect_id].effect_commands:
            source, target = int(command.a), int(command.b)
            if command.type == 3 and (source in naval_members or target in naval_members):
                actual_triples.add((tech_id, source, target))
    if actual_triples != expected_triples:
        raise ValueError(
            "DAT naval upgrade mapping drifted: "
            f"missing={sorted(expected_triples - actual_triples)}, "
            f"unexpected={sorted(actual_triples - expected_triples)}"
        )


def available_naval_upgrade_techs(
    data: Any,
    civ_id: int,
    available_units: set[int],
    disabled: set[int],
) -> set[int]:
    """Recover naval line techs represented as unit nodes by civTechTrees.

    The export normally exposes upgrades through the reachable target unit and
    omits their DAT technology ID from the Tech node list.  The audited DAT
    chain is therefore the authority: a line technology is available when it
    is not disabled, belongs to this/global civ, and one of its target hulls is
    present in the validated tree.
    """
    result: set[int] = set()
    for technologies in NAVAL_UPGRADE_CHAINS.values():
        for tech_id, pairs in technologies.items():
            technology = data.techs[tech_id]
            if tech_id in disabled or technology.civ not in {-1, civ_id}:
                continue
            if any(target in available_units for _, target in pairs):
                result.add(tech_id)
    return result


def naval_candidates_after_upgrade_closure(
    category: NavalCategory,
    available_units: set[int],
    package: set[int],
) -> list[tuple[int, float, tuple[int, ...]]]:
    """Apply executable type-3 line upgrades to the visible starting hulls.

    This matters when civTechTrees hides an intermediate target even though a
    shared researched technology necessarily upgrades an available source into
    it (currently Persia's Demo Raft 1104 -> Demolition Ship 527 via tech 34).
    """
    tier_by_unit = dict(category.units)
    states: dict[int, set[int]] = {
        unit_id: {unit_id} for unit_id in tier_by_unit if unit_id in available_units
    }
    technologies = NAVAL_UPGRADE_CHAINS[category.name]
    for tech_id in category.upgrade_tech_ids:
        if tech_id not in package:
            continue
        for source, target in technologies.get(tech_id, ()):
            if source not in states:
                continue
            origins = states.pop(source)
            states.setdefault(target, set()).update(origins)
    return [
        (unit_id, tier_by_unit[unit_id], tuple(sorted(origins - {unit_id})))
        for unit_id, origins in states.items()
        if unit_id in tier_by_unit
    ]


def validate_cothon_production(data: Any) -> None:
    """Validate the physical Cothon and batch mechanics used by scoring."""
    enable = data.effects[data.techs[COTHON_ENABLE_TECH_ID].effect_id].effect_commands
    if not any(
        command.type == 0
        and int(command.a) == COTHON_BUILDING_UNIT_ID
        and int(command.c) == 126
        and int(round(command.d)) == 1
        for command in enable
    ) or not any(
        command.type == 4
        and int(command.a) == COTHON_BUILDING_UNIT_ID
        and int(command.c) == 127
        and int(round(command.d)) == 4
        for command in enable
    ):
        raise ValueError("Cothon enable technology no longer grants a four-ship batch at unit 2480")

    rate = data.effects[data.techs[COTHON_WORK_RATE_TECH_ID].effect_id].effect_commands
    if not any(
        command.type == 5
        and int(command.a) == COTHON_BUILDING_UNIT_ID
        and int(command.c) == 13
        and abs(float(command.d) - 1.5) < 1e-6
        for command in rate
    ):
        raise ValueError("Assembly Line Methods no longer gives Cothon unit 2480 1.5x work rate")

    fifth = data.effects[data.techs[COTHON_FIFTH_SHIP_TECH_ID].effect_id].effect_commands
    # Tech 994 still targets 1896, but that slot is ARGALI in Gaia and absent
    # from Carthage, so it is validated as effect metadata without being
    # credited as usable Boarding Ship production.
    expected_batches = {batch_id for batch_id, _ in COTHON_BATCH_SPECS.values()} | {1896}
    cost_batches = {
        int(command.a)
        for command in fifth
        if command.type == 5 and int(command.c) == 100 and abs(float(command.d) - 1.25) < 1e-6
    }
    if cost_batches != expected_batches:
        raise ValueError(
            "Expanded Docking Bays no longer maps four-ship costs to five-ship batches: "
            f"expected={sorted(expected_batches)}, actual={sorted(cost_batches)}"
        )

    for batch_id, _ in COTHON_BATCH_SPECS.values():
        unit = data.civs[0].units[batch_id]
        if unit is None or not unit.creatable or not unit.creatable.train_locations:
            raise ValueError(f"Gaia Cothon batch unit {batch_id} is missing production metadata")
        if unit.creatable.train_locations[0].unit_id != COTHON_BUILDING_UNIT_ID:
            raise ValueError(f"Cothon batch unit {batch_id} no longer trains at unit 2480")


def naval_dps(state: dict[str, Any], category: NavalCategory) -> float:
    if category.profile == "boarding":
        # Boarding conversion utility has no ordinary attack in the DAT.  Its
        # relative quality is therefore evaluated by survival, speed, and
        # attainable numbers in naval_combat_ratio.
        return 1.0
    damage = max(0.1, state["attacks"].get(category.damage_class, 0.0))
    bonus_weight = {
        "ranged": 0.18,
        "fire": 0.35,
        "demolition": 0.45,
        "scout": 0.25,
        "naval_siege": 0.35,
        "heavy_reme": 0.30,
        "naval_unique": 0.20,
    }[category.profile]
    bonus = sum(
        max(0.0, amount)
        for class_id, amount in state["attacks"].items()
        if class_id != category.damage_class
    )
    accuracy = max(0.1, min(1.0, state["accuracy"] / 100.0)) if state["range"] > 0 else 1.0
    # Multi-projectile hulls (notably Hemiolias and heavy remes) deliver the
    # listed attack per projectile. Blast width is converted to a conservative
    # area-utility multiplier instead of being ignored or treated as guaranteed
    # full damage to every nearby target.
    area_multiplier = 1.0 + 0.25 * max(0.0, state["blast_width"])
    required_garrison = max(0.0, state["max_projectile_count"] - state["projectile_count"])
    operational_projectiles = max(
        state["projectile_count"],
        state["max_projectile_count"]
        * state["population"]
        / max(0.05, state["population"] + required_garrison),
    )
    return (
        (damage + bonus_weight * bonus)
        * accuracy
        * max(1.0, operational_projectiles)
        * area_multiplier
        / max(0.1, state["reload"])
    )


def naval_combat_ratio(
    state: dict[str, Any], reference: dict[str, Any], category: NavalCategory
) -> float:
    weights = {
        "ranged": (0.32, 0.35, 0.23, 0.10),
        "fire": (0.35, 0.45, 0.00, 0.20),
        "demolition": (0.20, 0.55, 0.00, 0.25),
        "scout": (0.20, 0.30, 0.15, 0.35),
        "boarding": (0.50, 0.00, 0.00, 0.50),
        "naval_siege": (0.30, 0.35, 0.30, 0.05),
        "heavy_reme": (0.35, 0.35, 0.15, 0.15),
        "naval_unique": (0.35, 0.35, 0.20, 0.10),
    }[category.profile]
    durability_weight, dps_weight, range_weight, speed_weight = weights
    range_ratio = max(0.5, state["range"]) / max(0.5, reference["range"])
    minimum_range_penalty = max(
        0.70,
        1.0 - 0.05 * max(0.0, state["minimum_range"] - reference["minimum_range"]),
    )
    return (
        (durability(state) / max(0.1, durability(reference))) ** durability_weight
        * (naval_dps(state, category) / max(0.1, naval_dps(reference, category))) ** dps_weight
        * ((range_ratio * minimum_range_penalty) ** range_weight)
        * ((max(0.1, state["speed"]) / max(0.1, reference["speed"])) ** speed_weight)
    )


def cothon_throughput(
    data: Any,
    civ_id: int,
    package: set[int],
    category: NavalCategory,
    unit_id: int,
    throughput_reference: dict[str, Any],
    shipyard_reference: dict[str, Any],
) -> tuple[float, float, int, float] | None:
    """Return normalized Cothon throughput, work rate, batch size, and per-ship cost."""
    if COTHON_ENABLE_TECH_ID not in package:
        return None
    spec = COTHON_BATCH_SPECS.get(category.name)
    if spec is None or spec[1] != unit_id:
        return None
    batch_id, _ = spec
    if COTHON_BUILDING_UNIT_ID >= len(data.civs[civ_id].units):
        return None
    cothon = data.civs[civ_id].units[COTHON_BUILDING_UNIT_ID]
    batch = data.civs[civ_id].units[batch_id] if batch_id < len(data.civs[civ_id].units) else None
    if cothon is None or batch is None or not batch.creatable or not batch.creatable.train_locations:
        return None
    cothon_state = state_for_unit(data, civ_id, COTHON_BUILDING_UNIT_ID, package)
    batch_state = state_for_unit(data, civ_id, batch_id, package)
    batch_size = 5 if COTHON_FIFTH_SHIP_TECH_ID in package else 4
    if batch_state["train_time"] <= 0 or throughput_reference["train_time"] <= 0:
        return None
    multiplier = (
        max(0.1, cothon_state["work_rate"])
        / max(0.1, shipyard_reference["work_rate"])
        * batch_size
        * throughput_reference["train_time"]
        / batch_state["train_time"]
    )
    cost_per_ship = resource_cost(batch_state) / batch_size
    return multiplier, max(0.1, cothon_state["work_rate"]), batch_size, cost_per_ship


def rate_navy(
    data: Any,
    civ_id: int,
    available_units: set[int],
    research_packages: list[set[int]],
    names: dict[int, str],
    shipyard_available: bool,
    primary_doctrine: bool,
) -> dict[str, Any]:
    """Return one composition-wide naval score from the strongest legal branch.

    Unlike the land-family cells, the component ships must coexist in one
    fleet.  Consequently this selects one legal mutually exclusive technology
    package for the whole navy instead of independently cherry-picking a
    different doctrine branch for each hull.
    """
    if not shipyard_available:
        return {
            "rating": "No",
            "capability_score": 0.0,
            "primary_navy_doctrine": primary_doctrine,
            "reason": "Shipyard is unavailable in the validated civilization tech tree.",
            "source": "Authoritative DAT and civTechTrees.json",
            "ship_classes": {},
        }

    packages = research_packages or [set()]
    evaluated_packages: list[tuple[Any, ...]] = []
    for package_index, package in enumerate(packages):
        lineup_points = 0.0
        quality_points = 0.0
        throughput_points = 0.0
        throughput_weight = 0.0
        class_records: list[dict[str, Any]] = []
        shipyard_state = state_for_unit(data, civ_id, 1251, package)
        shipyard_work_rate = max(0.1, shipyard_state["work_rate"])
        shipyard_reference = naval_throughput_reference_state(data, 1251)
        shipyard_throughput_multiplier = (
            shipyard_work_rate / max(0.1, shipyard_reference["work_rate"])
        )
        for category in NAVAL_CATEGORIES:
            candidates = naval_candidates_after_upgrade_closure(category, available_units, package)
            if not candidates:
                class_records.append(
                    {
                        "class": category.name,
                        "available": False,
                        "weight": category.weight,
                        "lineup_points": 0.0,
                        "quality_points": 0.0,
                        "upgrade_tech_ids": list(category.upgrade_tech_ids),
                        "applied_upgrade_tech_ids": [],
                    }
                )
                continue

            candidate_records = []
            for unit_id, tier, forced_sources in candidates:
                state = state_for_unit(data, civ_id, unit_id, package)
                reference = naval_reference_state(data, category, unit_id)
                throughput_reference = naval_throughput_reference_state(data, unit_id)
                ratio = naval_combat_ratio(state, reference, category)
                cost_multiplier = resource_cost(reference) / max(1.0, resource_cost(state))
                pop_multiplier = reference["population"] / max(0.05, state["population"])
                train_time_multiplier = (
                    throughput_reference["train_time"] / max(0.1, state["train_time"])
                    if throughput_reference["train_time"] > 0 and state["train_time"] > 0
                    else 1.0
                )
                throughput_multiplier = shipyard_throughput_multiplier * train_time_multiplier
                production_source = "Shipyard"
                production_work_rate = shipyard_work_rate
                production_batch_size = 1
                production_resource_cost_per_ship = resource_cost(state)
                potential_production_source = ""
                potential_throughput_multiplier = 0.0
                potential_production_work_rate = 0.0
                potential_production_batch_size = 0
                potential_production_resource_cost_per_ship = 0.0
                cothon = cothon_throughput(
                    data,
                    civ_id,
                    package,
                    category,
                    unit_id,
                    throughput_reference,
                    shipyard_reference,
                )
                if cothon is not None and cothon[0] > throughput_multiplier:
                    (
                        potential_throughput_multiplier,
                        potential_production_work_rate,
                        potential_production_batch_size,
                        potential_production_resource_cost_per_ship,
                    ) = cothon
                    potential_production_source = (
                        "Cothon potential (DAT unit 2480; tech-tree UI ID 1854; "
                        "not yet operated by AI)"
                    )
                number_multiplier = max(cost_multiplier, pop_multiplier)
                number_adjusted = ratio * number_multiplier
                # Only production paths the AI currently operates affect the
                # role score. Validated Cothon batch potential is retained as
                # evidence but cannot inflate current match competitiveness.
                quality_ratio = max(ratio, number_adjusted)
                candidate_records.append(
                    (
                        quality_ratio,
                        throughput_multiplier,
                        tier,
                        ratio,
                        number_adjusted,
                        unit_id,
                        state,
                        reference,
                        number_multiplier,
                        production_source,
                        production_work_rate,
                        production_batch_size,
                        production_resource_cost_per_ship,
                        potential_production_source,
                        potential_throughput_multiplier,
                        potential_production_work_rate,
                        potential_production_batch_size,
                        potential_production_resource_cost_per_ship,
                        forced_sources,
                    )
                )

            (
                quality_ratio,
                throughput_multiplier,
                tier,
                ratio,
                number_adjusted,
                unit_id,
                state,
                reference,
                number_multiplier,
                production_source,
                production_work_rate,
                production_batch_size,
                production_resource_cost_per_ship,
                potential_production_source,
                potential_throughput_multiplier,
                potential_production_work_rate,
                potential_production_batch_size,
                potential_production_resource_cost_per_ship,
                forced_sources,
            ) = max(candidate_records, key=lambda item: item[:4])
            class_lineup = category.weight * tier
            class_quality = category.weight * quality_ratio
            lineup_points += class_lineup
            quality_points += class_quality
            throughput_points += category.weight * throughput_multiplier
            throughput_weight += category.weight
            unit = data.civs[civ_id].units[unit_id]
            upgrade_tech_ids = (
                () if category.name == "Naval unique unit" and unit_id == 1923
                else category.upgrade_tech_ids
            )
            class_records.append(
                {
                    "class": category.name,
                    "available": True,
                    "weight": category.weight,
                    "unit_id": unit_id,
                    "unit_name": names.get(unit_id) or unit.name,
                    "tier_multiplier": tier,
                    "lineup_points": round(class_lineup, 3),
                    "quality_points": round(class_quality, 3),
                    "combat_ratio": round(ratio, 4),
                    "number_multiplier": round(number_multiplier, 4),
                    "number_adjusted_ratio": round(number_adjusted, 4),
                    "throughput_multiplier": round(throughput_multiplier, 4),
                    "production_source": production_source,
                    "production_work_rate": round(production_work_rate, 4),
                    "production_batch_size": production_batch_size,
                    "production_resource_cost_per_ship": round(
                        production_resource_cost_per_ship, 3
                    ),
                    "potential_production_source": potential_production_source,
                    "potential_throughput_multiplier": round(
                        potential_throughput_multiplier, 4
                    ),
                    "potential_production_work_rate": round(
                        potential_production_work_rate, 4
                    ),
                    "potential_production_batch_size": potential_production_batch_size,
                    "potential_production_resource_cost_per_ship": round(
                        potential_production_resource_cost_per_ship, 3
                    ),
                    "forced_upgrade_from_unit_ids": list(forced_sources),
                    "upgrade_tech_ids": list(upgrade_tech_ids),
                    "applied_upgrade_tech_ids": sorted(set(upgrade_tech_ids) & package),
                    "statistics": serialize_state(state, category),
                    "reference_statistics": serialize_state(reference, category),
                }
            )

        available_support = set(NAVAL_SUPPORT_TECH_WEIGHTS) & package
        support_points = sum(NAVAL_SUPPORT_TECH_WEIGHTS[tech_id] for tech_id in available_support)
        lineup_score = 30.0 * lineup_points / 80.0
        quality_score = min(50.0, 50.0 * quality_points / 80.0)
        fleet_throughput = throughput_points / max(1.0, throughput_weight)
        throughput_adjustment = min(5.0, max(-5.0, (fleet_throughput - 1.0) * 20.0))
        steady_state = min(100.0, lineup_score + quality_score + support_points)
        capability = min(100.0, max(0.0, steady_state + throughput_adjustment))
        evaluated_packages.append(
            (
                capability,
                steady_state,
                quality_score,
                support_points,
                throughput_adjustment,
                fleet_throughput,
                shipyard_work_rate,
                shipyard_throughput_multiplier,
                package_index,
                class_records,
                package,
            )
        )

    (
        capability,
        steady_state,
        quality_score,
        support_points,
        throughput_adjustment,
        fleet_throughput,
        shipyard_work_rate,
        shipyard_throughput_multiplier,
        package_index,
        class_records,
        selected_package,
    ) = max(evaluated_packages, key=lambda item: item[:4])
    lineup_score = 30.0 * sum(record["lineup_points"] for record in class_records) / 80.0
    if capability >= 80.0:
        rating = "Excellent"
    elif capability >= 70.0:
        rating = "Good"
    elif capability >= 60.0:
        rating = "Mediocre"
    else:
        rating = "Bad"

    available_support = sorted(set(NAVAL_SUPPORT_TECH_WEIGHTS) & selected_package)
    missing_support = sorted(set(NAVAL_SUPPORT_TECH_WEIGHTS) - selected_package)
    has_heavy_reme = bool({1870, 1750} & available_units)
    has_octeres = 1884 in available_units
    return {
        "rating": rating,
        "unit_name": f"Fleet capability {capability:.2f}/100",
        "combat_ratio": round(capability / 100.0, 4),
        "number_adjusted_ratio": round(capability / 100.0, 4),
        "capability_score": round(capability, 2),
        "steady_state_capability_score": round(steady_state, 2),
        "lineup_completeness_score": round(lineup_score, 2),
        "ship_class_quality_score": round(quality_score, 2),
        "support_upgrade_score": round(support_points, 2),
        "production_throughput_adjustment": round(throughput_adjustment, 2),
        "fleet_throughput_multiplier": round(fleet_throughput, 4),
        "shipyard_work_rate": round(shipyard_work_rate, 4),
        "shipyard_throughput_multiplier": round(shipyard_throughput_multiplier, 4),
        "maximum_scores": {
            "lineup_completeness": 30,
            "ship_class_quality": 50,
            "support_upgrades": 20,
            "production_throughput_adjustment": 5,
        },
        "primary_navy_doctrine": primary_doctrine,
        "selected_package_index": package_index,
        "compatible_package_count": len(packages),
        "available_support_tech_ids": available_support,
        "missing_support_tech_ids": missing_support,
        "support_tech_weights": {str(key): value for key, value in NAVAL_SUPPORT_TECH_WEIGHTS.items()},
        "has_quadrireme_or_quinquereme": has_heavy_reme,
        "has_octeres": has_octeres,
        "specialist_support_detachment": has_heavy_reme and has_octeres,
        "ship_classes": {record["class"]: record for record in class_records},
        "reason": (
            f"Data-derived competitive naval capability {capability:.2f}/100: steady-state lineup completeness "
            f"{lineup_score:.2f}/30, fully upgraded ship-class quality {quality_score:.2f}/50, "
            f"relevant support technologies {support_points:.2f}/20, and a signed production-throughput "
            f"adjustment of {throughput_adjustment:+.2f} within ±5 from {fleet_throughput:.3f}x weighted "
            f"fleet throughput (including missing Conscription, but excluding Cothon batches until "
            f"the AI implements Cothon construction and batch production). "
            f"Naval doctrine is {'Yes' if primary_doctrine else 'No'} and is kept separate from the numeric score; "
            "runtime role selection applies the explicit team-owner and enemy-Naval-Yes overrides."
        ),
        "source": "Authoritative DAT final statistics, legal civTechTrees.json technology package, and AI RAW.per doctrine preference",
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
    validate_naval_upgrade_chains(data)
    validate_cothon_production(data)
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
        naval_line_techs = available_naval_upgrade_techs(
            data, civ_id, available_units, disabled
        )
        visible_packages = compatible_tech_packages(
            data, visible_techs | naval_line_techs | {101, 102, 103, 104}, disabled
        )
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
        ratings["Navy"] = rate_navy(
            data,
            civ_id,
            available_units,
            research_packages,
            names,
            shipyard_available,
            affinity["good_navy"],
        )

        common_techs = set.intersection(*(set(package) for package in research_packages))
        civ_output[key] = {
            "civilization": DISPLAY_NAMES[key],
            "host_civilization": HOST_NAMES[key],
            "host_civilization_constant": host_constant,
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
        "schema_version": 2,
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
            "priests_and_navy": "Priest affinity automatically gives Excellent; other priests use a 7.5-point capability score. Navy combines a bounded 100-point steady-state score (30 lineup completeness, 50 final-stat/class quality including projectile and blast-area lethality plus superior cost/population efficiency, and 20 relevant support upgrades) with a signed -5 to +5 production-throughput adjustment, capped to 0..100 for runtime comparison. Naval Yes/No remains a separate strategic doctrine: it selects primary team owners and makes Naval No use support fleets rather than contest Naval Yes enemies one-for-one.",
        },
        "score_model": {
            "durability": "HP adjusted against representative 15 melee and 10 pierce attacks using final melee/pierce armor.",
            "damage": "Final primary and role-weighted bonus damage divided by reload time and adjusted for ranged accuracy. Naval quality also includes DAT projectile count and a conservative blast-width area multiplier. Garrison-scaled firepower records empty/max projectiles and fully upgraded capacity, then discounts contingent extra shots by the population required to crew them instead of granting free maximum volleys; counter families therefore retain their defining bonus damage.",
            "range": "30-35% of ranged/siege profiles with an additional whole-tile breakpoint and minimum-range penalty; archers therefore cannot hide a serious range deficit behind one strong stat.",
            "mobility": "5-20% by profile; slower cavalry can still qualify through damage and durability.",
            "numbers": "The better of weighted resource-cost advantage and population-use advantage.",
            "doctrine_packages": "Each category records its own strongest legal mutually exclusive technology package. Cells are unit-family potential ratings, not a claim that all best branches coexist in one match.",
            "naval_package": "All ship classes use one shared strongest legal technology package because the scored fleet must be attainable in one match. Audited DAT upgrade chains recover naval line technologies that civTechTrees represents as reachable unit nodes, and executable type-3 closure supersedes a contradictory hidden target when a researched shared tech necessarily transforms an available source hull. Forced source IDs are recorded per class. Class advantages above the fully upgraded reference may offset weaker classes inside the capped 50-point quality component. Shipyard work rate and ship train time provide a signed ±5 production-throughput adjustment, so missing Conscription is not silently treated as baseline. Validated Cothon batch size, work rate, and per-ship cost remain recorded as potential evidence but are excluded from the runtime role score until the AI implements Cothon construction and batch production. Research cost/time and age-of-unlock timing remain recorded runtime-calibration limits rather than inferred. The numeric capability does not inherit Naval Yes/No, but runtime roles deliberately apply its allied-primary and enemy-deterrence doctrine overrides.",
            "cothon_identifier_resolution": "civTechTrees uses UI Building ID 1854 for the Cothon column and technologies, while authoritative DAT effects and the AI constant target physical Cothon unit 2480. Evaluation uses 2480 to validate its four-ship batch and 1.5x work-rate effects and records the UI alias explicitly. That potential is not added to runtime capability until the AI can construct and operate the Cothon batches.",
        },
        "naval_upgrade_chains": {
            class_name: {
                str(tech_id): [list(pair) for pair in pairs]
                for tech_id, pairs in technologies.items()
            }
            for class_name, technologies in NAVAL_UPGRADE_CHAINS.items()
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
