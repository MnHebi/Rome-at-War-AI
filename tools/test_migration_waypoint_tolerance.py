"""Execute T26 migration waypoint terminal handling; no pathfinding model."""
import unittest

from test_assault_missions import Missions
from test_pre_backlog import source
from validate_naval_doctrine import rule_blocks


class MigrationWaypoint(Missions):
    def __init__(self, distance, best=10, waits=4):
        super().__init__()
        self.g.update({
            'gl-island-migration-state': self.val('MIGRATION-ROUTE-WAYPOINT-CHECK'),
            'gl-island-migration-transport-id': 10,
            'gl-island-migration-route-waypoint-x': 0,
            'gl-island-migration-route-waypoint-y': 0,
            'gl-island-migration-target-x': 80,
            'gl-island-migration-target-y': 80,
            'gl-island-migration-route-distance': best,
            'gl-island-migration-route-waits': waits,
            'gl-island-migration-focus': 2,
            'gl-home-anchor-x': 40,
            'gl-home-anchor-y': 40,
            'gl-island-migration-rejected-zone': -1,
            'gl-island-migration-rejected-zone2': -1,
            'gl-island-migration-rejected-zone3': -1,
            'gl-island-migration-zone': 3,
        })
        group = self.val('migration-transport-group')
        self.objects = {
            10: dict(id=10, player=2, hp=100, cargo=2, garrisoned=0,
                     flag=group, point=(distance, 0), zone=8,
                     type='transport-ship', cls='transport-class', idle=0,
                     under_attack=0, order=0),
        }
        self.groups = {group: [10]}
        self.local = [10]
        self.point = (0, 0)
        self.rules = [row for row in rule_blocks(source('rawai-military.per'))
                      if 'MIGRATION-ROUTE-WAYPOINT-CHECK' in row[3]]


class MigrationWaypointToleranceTests(unittest.TestCase):
    def test_stalled_ten_tile_approach_advances_to_exact_landing_validation(self):
        m = MigrationWaypoint(distance=10)
        m.sweep()
        self.assertEqual(m.g['gl-island-migration-state'],
                         m.val('MIGRATION-CHECK-LANDING-PATH'))
        self.assertEqual((m.g['gl-island-migration-route-waypoint-x'],
                          m.g['gl-island-migration-route-waypoint-y']), (80, 80))
        self.assertFalse(any(action == 'action-unload' for _, action, _ in m.commands))

    def test_far_stalled_route_retains_bounded_recall(self):
        m = MigrationWaypoint(distance=13)
        m.sweep()
        self.assertEqual(m.g['gl-island-migration-state'], m.val('MIGRATION-RETURNING'))
        self.assertTrue(any(action == 'action-unload' for _, action, _ in m.commands))

    def test_normal_eight_tile_arrival_is_unchanged(self):
        m = MigrationWaypoint(distance=8, best=20, waits=0)
        m.sweep()
        self.assertEqual(m.g['gl-island-migration-state'],
                         m.val('MIGRATION-CHECK-LANDING-PATH'))


if __name__ == '__main__':
    unittest.main()
