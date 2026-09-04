"""Shared bounded shoreline-search geometry for generated PER and fixtures.

The Python resolver is a mechanical model of the emitted state machines.  It
does not model AoE2 pathfinding; callers provide the zone and exact-hull path
predicates used by their test topology.
"""
from dataclasses import dataclass
from math import hypot


COARSE_STEP = 16
# Twenty-four samples cover a 255x255 map diagonal without an unbounded scan.
COARSE_LIMIT = 24
REFINE_STEP = 4
REFINE_LIMIT = 4
SHORE_OFFSETS = (0, 8, -8, 16, -16)
# Keep one failed local sector out without swallowing the materially different
# +/-16 fallback sectors (their per-axis separation is about 11 tiles).
MEMORY_RADIUS = 6


@dataclass(frozen=True)
class ShorelineResult:
    land: tuple[float, float]
    water: tuple[float, float]
    candidate: int
    path_queries: int


def _toward(point, target, distance):
    dx, dy = target[0] - point[0], target[1] - point[1]
    length = hypot(dx, dy)
    if length == 0:
        return point
    scale = min(distance, length) / length
    return point[0] + dx * scale, point[1] + dy * scale


def _cross(point, toward, distance):
    dx, dy = point[0] - toward[0], point[1] - toward[1]
    length = hypot(dx, dy) or 1
    return point[0] - dy / length * distance, point[1] + dx / length * distance


def shoreline_candidates(anchor, hull, target_zone, zone_at):
    """Return the bounded lateral fan around the first land-zone transition."""
    scan = last_land = anchor
    outside = None
    for _ in range(COARSE_LIMIT):
        scan = _toward(scan, hull, COARSE_STEP)
        if zone_at(scan) == target_zone:
            last_land = scan
        else:
            outside = scan
            break
    if outside is None:
        return []

    refine = last_land
    for _ in range(REFINE_LIMIT):
        refine = _toward(refine, outside, REFINE_STEP)
        if zone_at(refine) == target_zone:
            last_land = refine
        else:
            outside = refine
            break

    candidates = []
    for index, offset in enumerate(SHORE_OFFSETS):
        land = _cross(last_land, outside, offset) if offset else last_land
        water = _cross(outside, last_land, -offset) if offset else outside
        candidates.append((index, land, water))
    return candidates


def resolve_shoreline(anchor, hull, target_zone, zone_at, pathable,
                      failed_sectors=()):
    """Return the first bounded LAND/WATER pair accepted by supplied facts.

    ``pathable(point, exact)`` represents the exact selected Transport's
    option-0 land-vicinity or option-1 exact-water query.  Recently failed
    sectors are (x, y) points and are skipped before either path query.
    """
    path_queries = 0
    for index, land, water in shoreline_candidates(
            anchor, hull, target_zone, zone_at):
        if zone_at(land) != target_zone or zone_at(water) == target_zone:
            continue
        if any(abs(land[0] - x) <= MEMORY_RADIUS and
               abs(land[1] - y) <= MEMORY_RADIUS for x, y in failed_sectors):
            continue
        # The emitted PER stores both answers in the candidate-path state.
        # Keep the fixture's cost model identical even when the first answer
        # alone would already reject the pair.
        water_pathable = pathable(water, True)
        land_pathable = pathable(land, False)
        path_queries += 2
        if not water_pathable or not land_pathable:
            continue
        return ShorelineResult(land, water, index, path_queries)
    return None
