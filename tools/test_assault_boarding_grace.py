"""Execute the T26 bounded boarding-grace policy against exact passenger state."""
import unittest

from test_assault_missions import Missions
from test_pre_backlog import source
from validate_naval_doctrine import rule_blocks


LOAD_STATES = (
    'TRANSPORT-ROUTE-LOAD-WAIT', 'TRANSPORT-ROUTE-LOAD-CHECK',
    'TRANSPORT-ROUTE-LOAD-DIAG-FIND', 'TRANSPORT-ROUTE-LOAD-DIAG-PASSENGER',
    'TRANSPORT-ROUTE-LOAD-DIAG-APPLY', 'TRANSPORT-ROUTE-LOAD-PARTIAL-MANIFEST',
)


class BoardingGrace(Missions):
    def __init__(self, cargo=9, distance=3, action='action-garrison', target=10):
        super().__init__()
        self.now = 1000
        boarding = self.val('attack-boarding-group')
        transport = self.val('attack-transport-group')
        self.objects = {
            10: dict(id=10, player=2, hp=100, cargo=cargo, garrisoned=0,
                     flag=transport, point=(0, 0), zone=8,
                     type='transport-ship', cls='transport-class', idle=1,
                     under_attack=0, order=0),
        }
        passengers = []
        for i in range(10):
            oid = 20 + i
            aboard = i < cargo
            self.objects[oid] = dict(
                id=oid, player=2, hp=100, cargo=0, garrisoned=int(aboard),
                flag=boarding, point=(0 if aboard else distance, 0), zone=3,
                type='soldier', cls='infantry-class', idle=0,
                action=self.val(action), target=target,
                order=self.val('orderid-transport'), cmdid=1,
                move_x=0, move_y=0,
            )
            passengers.append(oid)
        self.groups = {boarding: passengers, transport: [10]}
        self.g.update({
            'gl-transport-route-state': self.val('TRANSPORT-ROUTE-LOAD-WAIT'),
            'gl-transport-route-id': 10,
            'gl-transport-route-load-target': 10,
            'gl-transport-route-load-deadline': self.now,
            'gl-transport-route-load-next': self.now,
            'gl-transport-route-load-reported': 1,
            'gl-transport-route-load-grace-used': 0,
            'gl-transport-route-origin-x': 0,
            'gl-transport-route-origin-y': 0,
            'gl-transport-route-focus': 2,
            'gl-owner-explore-suspended': 1,
        })
        rows = list(rule_blocks(source('rawai-military.per')))
        self.rules = [row for row in rows if any(state in row[3] for state in LOAD_STATES)]


class AssaultBoardingGraceTests(unittest.TestCase):
    def test_exact_nearby_passenger_gets_one_bounded_grace(self):
        m = BoardingGrace()
        m.sweep()
        self.assertEqual(m.g['gl-transport-route-load-grace-used'], 1)
        self.assertEqual(m.g['gl-transport-route-load-deadline'], 1012)
        self.assertEqual(m.g['gl-transport-route-state'], m.val('TRANSPORT-ROUTE-LOAD-WAIT'))
        self.assertTrue(any(action == 'action-garrison' for _, action, _ in m.commands))
        m.g['gl-transport-load-clock'] = 1013
        m.sweep(13)
        self.assertEqual(m.g['gl-transport-route-load-grace-used'], 1)
        self.assertEqual(m.g['gl-transport-route-state'], m.val('TRANSPORT-ROUTE-LOAD-READY'))
        self.assertEqual(m.g['gl-assault-manifest-count'], 9)

    def test_grace_rejects_wrong_hull_retasked_or_distant_passenger(self):
        fixtures = (
            dict(target=99),
            dict(action='action-move', target=-1),
            dict(distance=13),
        )
        for fixture in fixtures:
            with self.subTest(fixture=fixture):
                m = BoardingGrace(**fixture)
                if fixture.get('action') == 'action-move':
                    m.objects[29]['order'] = 0
                m.sweep()
                self.assertEqual(m.g['gl-transport-route-load-grace-used'], 0)
                self.assertEqual(m.g['gl-transport-route-state'], m.val('TRANSPORT-ROUTE-LOAD-READY'))
                self.assertEqual(m.g['gl-assault-manifest-count'], 9)

    def test_sub_useful_load_also_gets_only_one_chance_to_complete(self):
        m = BoardingGrace(cargo=4)
        m.sweep()
        self.assertEqual(m.g['gl-transport-route-load-deadline'], 1012)
        m.g['gl-transport-load-clock'] = 1013
        m.sweep(13)
        self.assertEqual(m.g['gl-transport-route-load-grace-used'], 1)
        self.assertEqual(m.g['gl-transport-route-state'], m.val('TRANSPORT-ROUTE-RECOVERY-WAIT'))


if __name__ == '__main__':
    unittest.main()
