"""Execute preparation recovery/admission PER; no engine pathfinding claims."""
import unittest

from test_assault_missions import Missions
from test_pre_backlog import source, expressions
from validate_naval_doctrine import rule_blocks


class Preparation(Missions):
    def __init__(self):
        super().__init__()
        text = source('rawai-military.per')
        text = text[text.index(';A recalled loaded transport'):text.index(';Recover idle soldiers left')]
        self.rules = list(rule_blocks(text))
        self.timers = {}
        self.g.update({'gl-quarantine-transport-id': 999,
                       'gl-transport-route-state': self.val('TRANSPORT-ROUTE-IDLE')})

    def fact(self, e):
        if e[0] == 'up-timer-status':
            return self.now >= self.timers.get(e[1], 0)
        return super().fact(e)

    def action(self, e, pc=0):
        if e[0] == 'up-set-timer':
            self.timers[e[2]] = self.now + self.operand(e[3], e[4])
            return 0
        return super().action(e, pc)

    def recovering(self, cargo=3, distance=30):
        self.prepare(10, cargo=cargo)
        self.objects[10]['point'] = (10+distance, 10)
        self.g.update({'gl-transport-route-state': self.val('TRANSPORT-ROUTE-RECOVERY-WAIT'),
                       'gl-transport-route-script-load': 1, 'gl-route-unload-attempts': 3,
                       'gl-home-anchor-x': 10, 'gl-home-anchor-y': 10})
        return self


class PreparationRecoveryTests(unittest.TestCase):
    def test_busy_quarantine_releases_lane_without_losing_cargo_or_old_id(self):
        m = Preparation().recovering()
        for _ in range(20): m.sweep(15)
        self.assertEqual(m.g['gl-transport-route-state'], m.val('TRANSPORT-ROUTE-IDLE'))
        self.assertEqual(m.g['gl-quarantine-transport-id'], 999)
        self.assertEqual(m.objects[10]['cargo'], 3)
        self.assertTrue(all(m.objects[p]['garrisoned'] == 1 for p in range(1000, 1003)))
        self.assertFalse(m.commands)

    def test_empty_stranded_hull_has_finite_recovery_and_keeps_last_order(self):
        m = Preparation().recovering(cargo=0)
        for _ in range(20): m.sweep(15)
        self.assertEqual(m.g['gl-transport-route-state'], m.val('TRANSPORT-ROUTE-IDLE'))
        self.assertLessEqual(len(m.commands), 6)
        count = len(m.commands)
        for _ in range(80): m.sweep(15)
        self.assertEqual(len(m.commands), count)

    def test_returned_empty_and_missing_hulls_still_release_immediately(self):
        for missing in (False, True):
            m = Preparation().recovering(cargo=0, distance=0)
            if missing: del m.objects[10]
            m.sweep()
            self.assertEqual(m.g['gl-transport-route-state'], m.val('TRANSPORT-ROUTE-IDLE'))

    def test_other_owner_is_not_commanded_or_released(self):
        m = Preparation().recovering()
        m.objects[10]['flag'] = m.val('assault-mission-2-group')
        for _ in range(20): m.sweep(15)
        self.assertEqual(m.g['gl-transport-route-state'], m.val('TRANSPORT-ROUTE-IDLE'))
        self.assertEqual(m.objects[10]['flag'], m.val('assault-mission-2-group'))
        self.assertFalse(m.commands)


