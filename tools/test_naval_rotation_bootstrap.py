"""Execute the active roster rotation from the replay-observed unset state."""
import unittest

from test_t13_gate_recovery import Gate, CONSTANTS
from test_pre_backlog import source, expressions
from validate_naval_doctrine import rule_blocks


class Rotation(Gate):
    def __init__(self, role):
        super().__init__(**{'ship-train': -1, 'gl-naval-role': CONSTANTS[role]})
        self.timer = 'timer-running'
        init = [r for r in rule_blocks(source('rawai-init-goals.per'))
                if '(up-set-timer c: t-ship-train c: 12)' in r[4]]
        assert len(init) == 1
        self.init = init[0]
        for e in expressions(self.init[4]):
            if e[:2] == ['set-goal', 'ship-train']:
                self.goals['ship-train'] = self.value(e[2])
        military = source('rawai-military.per')
        active = military.split(';Keep one choice stable', 1)[1].split('#load-if-not-defined', 1)[0]
        self.rules = list(rule_blocks(active))

    def fact(self, e):
        if e[0] == 'up-timer-status':
            assert e[1:] == ['t-ship-train', '!=', 'timer-running']
            return self.timer != 'timer-running'
        return super().fact(e)

    def sweep(self, expired=False):
        if expired: self.timer = 'timer-triggered'
        for row in self.rules:
            if not self.accepts(row): continue
            for e in expressions(row[4]):
                if e[0] == 'set-goal': self.goals[e[1]] = self.value(e[2])
                elif e[0] == 'up-set-timer':
                    assert e[1:] == ['c:', 't-ship-train', 'c:', '12']
                    self.timer = 'timer-running'
                else: raise AssertionError(e)
        return self.goals['ship-train']


class NavalRotationBootstrapTests(unittest.TestCase):
    def test_unset_replay_state_is_initialized_once(self):
        r = Rotation('NAVAL-ROLE-COMPETITIVE')
        self.assertEqual(r.goals['ship-train'], CONSTANTS['SCOUTSHIP'])
        self.assertIn('(true)', r.init[3])
        self.assertIn('(disable-self)', r.init[4])

    def test_primary_and_competitive_visit_both_heavy_families(self):
        for role in ('NAVAL-ROLE-PRIMARY', 'NAVAL-ROLE-COMPETITIVE'):
            r = Rotation(role)
            cycle = [r.sweep(expired=True) for _ in range(9)]
            self.assertEqual(cycle, [1, 2, 3, 4, 5, 6, 7, 8, 0], role)

    def test_support_retains_its_existing_limited_roster(self):
        r = Rotation('NAVAL-ROLE-SUPPORT')
        self.assertEqual([r.sweep(expired=True) for _ in range(4)], [2, 5, 8, 0])

    def test_no_rotation_while_choice_timer_is_running(self):
        r = Rotation('NAVAL-ROLE-COMPETITIVE')
        self.assertEqual([r.sweep() for _ in range(20)], [0] * 20)
        self.assertEqual(r.sweep(expired=True), 1)
        self.assertEqual([r.sweep() for _ in range(20)], [1] * 20)


if __name__ == '__main__': unittest.main()
