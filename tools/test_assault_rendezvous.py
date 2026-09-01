"""Execute T23 passenger-first assault rendezvous rules; no pathfinding model."""
import unittest

from test_assault_missions import Missions
from test_pre_backlog import source
from validate_naval_doctrine import rule_blocks


STATES = (
    'TRANSPORT-ROUTE-MANIFEST-FIND', 'TRANSPORT-ROUTE-MANIFEST-CHECK',
    'TRANSPORT-ROUTE-HULL-FIND', 'TRANSPORT-ROUTE-LOAD-FIND',
    'TRANSPORT-ROUTE-HULL-VERIFY', 'TRANSPORT-ROUTE-RENDEZVOUS-START',
    'TRANSPORT-ROUTE-RENDEZVOUS-WAIT', 'TRANSPORT-ROUTE-RENDEZVOUS-CHECK',
    'TRANSPORT-ROUTE-RENDEZVOUS-PASSENGER', 'TRANSPORT-ROUTE-LOAD-ISSUE',
)


class Rendezvous(Missions):
    def __init__(self, passenger_count=10, hulls=True):
        super().__init__()
        self.now = 1000
        self.sn['sn-focus-player-number'] = 2
        self.g.update({
            'gl-transport-route-state': self.val('TRANSPORT-ROUTE-MANIFEST-FIND'),
            'gl-transport-route-focus': 2, 'gl-transport-route-load-player': 6,
            'gl-transport-capacity': 30, 'gl-home-zone': 3,
            'gl-home-anchor-x': 0, 'gl-home-anchor-y': 0,
            'gl-owner-explore-suspended': 1, 'gl-quarantine-transport-id': -1,
            'gl-assault-recovery-rejected': -1, 'gl-transport-route-script-load': 0,
            'gl-transport-route-load-deadline': 0,
        })
        self.objects = {}
        for i in range(passenger_count):
            oid = 100 + i
            self.objects[oid] = dict(
                id=oid, player=2, hp=100, cargo=0, garrisoned=0, flag=-2,
                point=(90 + i, 90), zone=3, type='soldier', cls='infantry-class',
                idle=1, under_attack=0, order=0,
            )
        if hulls:
            # Hull10 is closest to the old home-anchor selector. Hull11 is
            # closest to the reserved manifest but still outside local range.
            self.objects[10] = dict(
                id=10, player=2, hp=100, cargo=0, garrisoned=0, flag=-2,
                point=(0, 0), zone=8, type='transport-ship', cls='transport-class',
                idle=1, under_attack=0, order=0,
            )
            self.objects[11] = dict(
                id=11, player=2, hp=100, cargo=0, garrisoned=0, flag=-2,
                point=(60, 60), zone=8, type='transport-ship', cls='transport-class',
                idle=1, under_attack=0, order=0,
            )
        rows = list(rule_blocks(source('rawai-military.per')))
        self.rules = [row for row in rows if
                      'gl-transport-load-clock)' in row[4]
                      or any(state in row[3] for state in STATES)]

    def finish_preparation_step(self, limit=12):
        for _ in range(limit):
            before = self.g['gl-transport-route-state']
            self.sweep()
            if self.g['gl-transport-route-state'] == before:
                return
        raise AssertionError('preparation state did not quiesce')


class AssaultRendezvousTests(unittest.TestCase):
    def test_manifest_is_reserved_before_nearest_manifest_hull_is_claimed(self):
        m = Rendezvous()
        m.finish_preparation_step()
        self.assertEqual(m.g['gl-transport-route-id'], 11)
        self.assertEqual(m.g['gl-assault-rendezvous-x'], 90)
        self.assertEqual(len(m.groups[m.val('attack-boarding-group')]), 10)
        self.assertTrue(all(m.objects[i]['flag'] == m.val('attack-boarding-group')
                            for i in range(100, 110)))
        self.assertEqual(m.g['gl-transport-route-state'], m.val('TRANSPORT-ROUTE-RENDEZVOUS-WAIT'))
        self.assertEqual(m.g['gl-transport-route-load-deadline'], 0)
        self.assertIn(((11,), 'action-move', (90, 90)), m.commands)
        self.assertIn((tuple(range(100, 110)), 'action-garrison', ('object', 11)), m.commands)

    def test_boarding_clock_starts_only_after_local_proximity(self):
        m = Rendezvous(); m.finish_preparation_step()
        m.sweep(4)
        self.assertEqual(m.g['gl-transport-route-state'], m.val('TRANSPORT-ROUTE-RENDEZVOUS-WAIT'))
        self.assertEqual(m.g['gl-transport-route-load-deadline'], 0)
        m.objects[11]['point'] = (89, 90)
        m.sweep(8)
        self.assertEqual(m.g['gl-transport-route-state'], m.val('TRANSPORT-ROUTE-LOAD-WAIT'))
        self.assertEqual(m.g['gl-transport-route-load-deadline'], m.now + 30)
        self.assertTrue(any(value == 24 for _, value in m.logs))

    def test_rendezvous_timeout_is_distinct_and_enters_bounded_recovery(self):
        m = Rendezvous(); m.finish_preparation_step()
        m.sweep(121)
        self.assertEqual(m.g['gl-transport-route-state'], m.val('TRANSPORT-ROUTE-RECOVERY-WAIT'))
        self.assertEqual(m.g['gl-transport-route-load-deadline'], 0)
        self.assertTrue(any(value == 25 for _, value in m.logs))
        self.assertEqual(m.objects[11]['flag'], m.val('attack-transport-group'))
        self.assertTrue(all(m.objects[i]['flag'] == m.val('attack-boarding-group')
                            for i in range(100, 110)))

    def test_rendezvous_lease_detects_loss_of_the_exact_claimed_hull(self):
        m = Rendezvous(); m.finish_preparation_step()
        m.objects[11]['flag'] = -2
        m.sweep()
        self.assertEqual(m.g['gl-transport-route-state'], m.val('TRANSPORT-ROUTE-OWNER-LOST'))
        self.assertEqual(m.objects[10]['flag'], -2)

    def test_no_hull_or_too_small_manifest_releases_only_its_reservation(self):
        for m in (Rendezvous(hulls=False), Rendezvous(passenger_count=4)):
            with self.subTest(passengers=len([i for i in m.objects if i >= 100])):
                m.finish_preparation_step()
                self.assertEqual(m.g['gl-transport-route-state'], m.val('TRANSPORT-ROUTE-IDLE'))
                self.assertTrue(all(o['flag'] == -2 for o in m.objects.values()
                                    if o.get('cls') == 'infantry-class'))
                self.assertFalse(any(o.get('flag') == m.val('attack-transport-group')
                                     for o in m.objects.values()))


if __name__ == '__main__':
    unittest.main()
