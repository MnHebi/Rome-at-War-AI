"""Mechanical/state-machine coverage for the bounded shoreline resolver.

These fixtures model point geometry, map-zone answers, and caller-supplied
pathability.  They do not claim to simulate AoE2 DE pathfinding.
"""
import math
import unittest

from shoreline_resolver import (COARSE_LIMIT, COARSE_STEP, REFINE_LIMIT,
                                SHORE_OFFSETS, resolve_shoreline,
                                shoreline_candidates)
from test_pre_backlog import source
from validate_naval_doctrine import rule_blocks


def diagonal_zone(point):
    return 3 if point[0] + point[1] >= 100 else 8


class ShorelineGeometryTests(unittest.TestCase):
    def test_t33_style_inland_geometry_is_replaced_by_land_water_pair(self):
        old_corridor, old_unload = (155, 108), (86, 61)
        self.assertEqual((diagonal_zone(old_corridor), diagonal_zone(old_unload)),
                         (3, 3))
        result = resolve_shoreline(old_corridor, (10, 10), 3,
                                   diagonal_zone, lambda point, exact: True)
        self.assertIsNotNone(result)
        self.assertEqual(diagonal_zone(result.land), 3)
        self.assertNotEqual(diagonal_zone(result.water), 3)
        self.assertNotEqual(result.land, old_unload)

    def test_straightforward_coast_accepts_direct_sector(self):
        result = resolve_shoreline((100, 100), (10, 10), 3,
                                   diagonal_zone, lambda point, exact: True)
        self.assertEqual(result.candidate, 0)
        self.assertEqual(result.path_queries, 2)
        self.assertLess(math.dist(result.land, result.water), 5)

    def test_direct_cliff_can_fall_back_to_lateral_sector(self):
        direct_water = shoreline_candidates((100, 100), (10, 10), 3,
                                            diagonal_zone)[0][2]

        def pathable(point, exact):
            return not (exact and point == direct_water)

        result = resolve_shoreline((100, 100), (10, 10), 3,
                                   diagonal_zone, pathable)
        self.assertEqual(result.candidate, 1)
        self.assertEqual(result.path_queries, 4)

    def test_all_candidates_invalid_stops_at_ten_path_queries(self):
        calls = []

        def water_reachable_land_blocked(point, exact):
            calls.append((point, exact))
            return exact

        result = resolve_shoreline((100, 100), (10, 10), 3,
                                   diagonal_zone, water_reachable_land_blocked)
        self.assertIsNone(result)
        self.assertEqual(len(calls), 2 * len(SHORE_OFFSETS))
        self.assertEqual(len(calls), 10)

    def test_recent_failed_sector_is_skipped_before_path_queries(self):
        candidates = shoreline_candidates((100, 100), (10, 10), 3,
                                           diagonal_zone)
        calls = []
        result = resolve_shoreline((100, 100), (10, 10), 3,
                                   diagonal_zone,
                                   lambda point, exact: calls.append(point) or True,
                                   failed_sectors=(candidates[0][1],))
        # The six-tile cache also excludes the immediately adjacent +/-8
        # sectors; the materially different +16 sector remains available.
        self.assertEqual(result.candidate, 3)
        self.assertEqual(len(calls), 2)
        self.assertNotIn(candidates[0][2], calls)

    def test_migration_resolves_coast_beyond_old_anchor_plus_two_search(self):
        anchor = (180, 180)
        old_candidates = (anchor, (182, 180), (178, 180),
                          (180, 182), (180, 178))
        self.assertTrue(all(diagonal_zone(point) == 3 for point in old_candidates))
        result = resolve_shoreline(anchor, (10, 10), 3,
                                   diagonal_zone, lambda point, exact: True)
        self.assertIsNotNone(result)
        self.assertGreater(math.dist(anchor, result.land), 100)
        self.assertNotEqual(diagonal_zone(result.water), 3)

    def test_no_coast_terminates_at_coarse_budget_without_path_query(self):
        calls = []
        result = resolve_shoreline((200, 200), (10, 10), 3,
                                   lambda point: 3,
                                   lambda point, exact: calls.append(point) or True)
        self.assertIsNone(result)
        self.assertFalse(calls)
        self.assertEqual(COARSE_LIMIT * COARSE_STEP, 384)
        self.assertEqual(REFINE_LIMIT, 4)


class ShorelineEmissionTests(unittest.TestCase):
    def test_assault_and_migration_emit_same_bounded_shape_with_separate_state(self):
        assault = source('rawai-assault-plans.per')
        migration = source('rawai-migration-shoreline.per')
        for text in (assault, migration):
            self.assertIn('(up-lerp-tiles ', text)
            self.assertIn('(up-get-point-zone ', text)
            self.assertEqual(text.count('(up-cross-tiles '), 8)
        self.assertIn('(up-get-path-distance gl-ap-shore-scan-x 1 gl-ap-shore-water-distance)', assault)
        self.assertIn('(up-get-path-distance gl-transport-route-landing-x 0 gl-ap-shore-land-distance)', assault)
        self.assertIn('(up-get-path-distance gl-msr-candidate-water-x 1 gl-msr-water-distance)', migration)
        self.assertIn('(up-get-path-distance gl-island-migration-route-waypoint-x 0 gl-msr-land-distance)', migration)
        self.assertNotIn('gl-msr-', assault)
        self.assertNotIn('gl-ap-', migration)
        self.assertNotIn('gl-am1-', assault)

    def test_corridor_uses_validated_water_and_has_safe_direct_fallback(self):
        military = source('rawai-military.per')
        self.assertIn('(up-bound-point gl-transport-route-waypoint-left-x gl-ap-shore-selected-water-x)', military)
        self.assertIn('(up-bound-point gl-island-migration-route-left-x gl-msr-selected-water-x)', military)
        assault = source('rawai-assault-plans.per')
        direct = [row for row in rule_blocks(assault)
                  if '(goal gl-transport-route-state AP-PATH)' in row[3]
                  and '(goal gl-ap-direct-threats 0)' in row[3]]
        self.assertEqual(len(direct), 1)
        self.assertIn('(up-bound-point gl-transport-route-waypoint-x gl-ap-shore-selected-water-x)',
                      direct[0][4])
        self.assertIn('(set-goal gl-transport-route-state AP-DIRECT-PATH)', direct[0][4])

    def test_t34_danger_manifests_and_bounded_replan_remain_present(self):
        assault = source('rawai-assault-plans.per')
        self.assertIn('(set-goal gl-ap-failure 36)', assault)
        self.assertIn('(set-goal gl-ap-failure 37)', assault)
        self.assertIn('(goal gl-transport-route-state AP-SAFETY)', assault)
        self.assertIn('(up-compare-goal gl-assault-manifest-count c:< 5)', assault)
        self.assertNotIn('action-unload', '\n'.join(
            row[4] for row in rule_blocks(assault)
            if 'AP-SHORE-' in row[3] or 'AP-CANDIDATE' in row[3]))
        military = source('rawai-military.per')
        self.assertIn('(load "rawai-migration-shoreline")', military)
        self.assertIn('(set-goal gl-island-migration-state MIGRATION-SHORE-INIT)', military)
        self.assertNotIn('(up-modify-goal gl-island-migration-route-waypoint-x c:+ 2)', military)


if __name__ == '__main__':
    unittest.main()
