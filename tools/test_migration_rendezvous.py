"""Execute T24 migration rendezvous rules; no engine pathfinding model."""
import unittest

from test_assault_missions import Missions
from test_pre_backlog import expressions, source
from validate_naval_doctrine import rule_blocks


RENDEZVOUS = (
    'MIGRATION-RENDEZVOUS-ANCHOR',
    'MIGRATION-RENDEZVOUS-START', 'MIGRATION-RENDEZVOUS-WAIT',
    'MIGRATION-RENDEZVOUS-CHECK', 'MIGRATION-RENDEZVOUS-PASSENGER',
)


class MigrationRendezvous(Missions):
    def __init__(self, passengers=5):
        super().__init__()
        self.now = 1000
        self.timers = {}
        self.sn['sn-focus-player-number'] = 2
        self.g.update({
            'gl-transport-load-clock': self.now,
            'gl-island-migration-state': self.val('MIGRATION-OWNERSHIP-CLAIM'),
            'gl-island-migration-mission': self.val('MIGRATION-MISSION-MINING'),
            'gl-island-migration-transport-id': 10,
            'gl-island-migration-focus': 2,
            'gl-island-migration-load-target': 0,
            'gl-island-migration-load-terminal': self.val('TRANSPORT-LOAD-TERMINAL-NONE'),
            'gl-island-migration-load-reported': 0,
            'gl-island-migration-load-candidate-id': -1,
            'gl-transport-preparation-owned': 0,
            'gl-owner-worker-hold': 1,
        })
        self.objects = {
            10: dict(id=10, player=2, hp=100, cargo=0, garrisoned=0,
                     flag=self.val('migration-transport-group'), point=(0, 0), zone=8,
                     type='transport-ship', cls='transport-class', idle=1,
                     under_attack=0, order=0),
        }
        self.groups = {self.val('migration-transport-group'): [10]}
        for i in range(passengers):
            oid = 100 + i
            self.objects[oid] = dict(
                id=oid, player=2, hp=100, cargo=0, garrisoned=0, flag=-2,
                point=(50 + i, 50), zone=3, type='villager', cls='villager-class',
                idle=1, under_attack=0, order=0,
            )
        self.local = list(range(100, 100 + passengers))
        rows = list(rule_blocks(source('rawai-military.per')))
        self.rules = []
        for row in rows:
            trigger, action = row[3], row[4]
            exact_claim = ('MIGRATION-OWNERSHIP-CLAIM' in trigger
                           and '(or ' not in trigger
                           and trigger.count('MIGRATION-') == 1)
            rendezvous = any(state in trigger for state in RENDEZVOUS)
            issue = 'MIGRATION-ISSUE-BOARD' in trigger
            clock = '(up-get-fact game-time 0 gl-transport-load-clock)' in action
            if exact_claim or rendezvous or issue or clock:
                self.rules.append(row)

    def action(self, e, pc=0):
        if e[0] == 'fe-filter-garrisoned':
            return 0
        if e[0] == 'up-set-target-object':
            items = self.local if e[1] == 'search-local' else self.remote
            index = self.operand(e[2], e[3])
            self.target = items[index] if 0 <= index < len(items) else None
            return 0
        if e[0] == 'up-set-timer':
            self.timers[e[2]] = self.val(e[4])
            return 0
        return super().action(e, pc)

    def begin(self):
        self.sweep()
        self.assert_waiting()

    def assert_waiting(self):
        assert self.g['gl-island-migration-state'] == self.val('MIGRATION-RENDEZVOUS-WAIT')


class MigrationRendezvousTests(unittest.TestCase):
    def test_remote_travel_does_not_start_local_boarding_timer(self):
        m = MigrationRendezvous(); m.begin()
        self.assertEqual(m.g['gl-migration-rendezvous-x'], 50)
        self.assertEqual(m.g['gl-migration-rendezvous-until'], 1120)
        self.assertNotIn('t-island-migration', m.timers)
        self.assertIn(((10,), 'action-move', (50, 50)), m.commands)
        self.assertIn((tuple(range(100, 105)), 'action-garrison', ('object', 10)), m.commands)
        self.assertTrue(all(m.objects[i]['flag'] == m.val('migration-boarding-group')
                            for i in range(100, 105)))

    def test_local_proximity_starts_unchanged_thirty_second_boarding_window(self):
        m = MigrationRendezvous(); m.begin()
        m.objects[10]['point'] = (49, 50)
        m.sweep(4)
        m.sweep()
        self.assertEqual(m.g['gl-island-migration-state'], m.val('MIGRATION-LOADING'))
        self.assertEqual(m.timers['t-island-migration'], 30)
        self.assertEqual(m.timers['t-island-migration-board-retry'], 3)

    def test_rendezvous_timeout_is_distinct_and_hands_off_to_existing_recovery(self):
        m = MigrationRendezvous(); m.begin()
        m.sweep(121)
        m.sweep()
        self.assertEqual(m.g['gl-island-migration-state'], m.val('MIGRATION-LOADING'))
        self.assertEqual(m.timers['t-island-migration'], 1)
        self.assertIn(('"RAW44C migration terminal phase: %d"', 4), m.logs)

    def test_exact_hull_ownership_loss_uses_existing_owner_lost_path(self):
        m = MigrationRendezvous(); m.begin()
        m.objects[10]['flag'] = -2
        m.sweep(4)
        self.assertEqual(m.g['gl-island-migration-state'], m.val('MIGRATION-OWNER-LOST'))

    def test_no_manifest_remains_bounded_through_existing_rule(self):
        m = MigrationRendezvous(passengers=0); m.sweep()
        self.assertEqual(m.g['gl-island-migration-state'], m.val('MIGRATION-IDLE'))


if __name__ == '__main__':
    unittest.main()
