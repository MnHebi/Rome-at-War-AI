"""Imperial cutoff source/ownership fixtures; fresh engine acceptance required."""
import unittest
from test_pre_backlog import source, expressions
from test_t13_gate_recovery import Gate, CONSTANTS, CMP
from test_ownership_contract import FilterMachine, unit
from validate_naval_doctrine import rule_blocks


class ExplorerGate(Gate):
    def __init__(self, age, phase=3):
        super().__init__(**{'current-age': age, 'current-phase': phase,
            'gl-owner-explore-suspended': 0, 'gl-island-migration-state': CONSTANTS['MIGRATION-IDLE'],
            'desired-military-explorers': 2, 'desired-civilian-explorers': 1})
        self.sn = {}; self.resets = 0

    def fact(self, e):
        if e[0] == 'up-group-size': return CMP[e[3]](0, int(e[4]))
        if e[0] == 'up-compare-sn': return CMP[e[2].split(':')[-1]](self.sn.get(e[1], 0), self.value(e[3]))
        return super().fact(e)

    def run(self, row):
        if not self.accepts(row): return
        for op, *a in expressions(row[4]):
            if op == 'set-goal': self.goals[a[0]] = self.value(a[1])
            elif op == 'set-strategic-number': self.sn[a[0]] = self.value(a[1])
            elif op == 'up-modify-sn': self.sn[a[0]] = self.value(a[2])
            elif op == 'up-reset-scouts': self.resets += 1
            elif op == 'up-modify-goal': pass  # invocation counter only
            else: raise AssertionError(op)

    def sweep(self):
        for r in rule_blocks(source('rawai-ownership.per')):
            if '(goal gl-owner-explore-suspended' in r[3]: self.run(r)
        for r in rule_blocks(source('rawai-general.per'))[:6]: self.run(r)


class ImperialExplorationTests(unittest.TestCase):
    def test_imperial_ends_native_exploration_even_if_economy_phase_is_low(self):
        g = ExplorerGate(2); g.sweep()
        self.assertEqual(g.sn['sn-number-explore-groups'], 2)
        g.goals['current-age'] = 3
        for _ in range(100): g.sweep()
        self.assertEqual(g.resets, 1)
        self.assertEqual(g.goals['gl-owner-explore-suspended'], 1)
        for sn in ('sn-number-explore-groups', 'sn-total-number-explorers', 'sn-cap-civilian-explorers', 'sn-minimum-civilian-explorers'):
            self.assertEqual(g.sn[sn], 0)

    def test_early_exploration_and_preexisting_ownership_suppression_survive(self):
        g = ExplorerGate(1); g.sweep(); self.assertEqual(g.resets, 0)
        g.goals['current-phase'] = 4; g.sweep(); self.assertEqual(g.resets, 1)
        g.goals['current-phase'] = 3; g.sweep()
        self.assertEqual(g.sn['sn-number-explore-groups'], 2)

    def test_naval_retirement_is_once_and_only_its_exact_own_group(self):
        row = list(rule_blocks(source('rawai-exploration-policy.per')))[0]
        self.assertIn('(disable-self)', row[4])
        self.assertIn('(current-age >= imperial-age)', row[3])
        m = FilterMachine([unit(1, 16), unit(2, 7), unit(3, 16, player=2), unit(4)], groups={16: [1, 2, 3]})
        m.run(row[4]); self.assertEqual(m.commands, [[1]])
        self.assertEqual([m.units[i]['object-data-group-flag'] for i in (1, 2, 3, 4)], [-2, 7, 16, -2])
        self.assertEqual(m.groups[16], [])

    def test_scripted_naval_admission_and_all_route_consumers_have_age_guard(self):
        rows = [r for r in rule_blocks(source('rawai-military.per'))
                if ('naval-scout' in r[3] and ('up-create-group' in r[4] or 'action-move' in r[4] or 'up-find-local' in r[4]))]
        self.assertEqual(len(rows), 6)
        for r in rows: self.assertIn('(current-age < imperial-age)', r[3])

    def test_new_scout_ferry_is_gated_but_inflight_mission_can_finish_landing(self):
        rows = list(rule_blocks(source('rawai-military.per')))
        admission = next(r for r in rows if '(set-goal gl-island-migration-state MIGRATION-PLAN-SCOUT)' in r[4])
        self.assertIn('(current-age < imperial-age)', admission[3])
        retire = next(r for r in rule_blocks(source('rawai-exploration-policy.per')) if 'MIGRATION-RETIRE-SCOUT)' in r[4])
        for state, expected in [('MIGRATION-TASK-SCOUT', True), ('MIGRATION-SCOUT-PATROL-WAIT', True), ('MIGRATION-SAILING', False), ('MIGRATION-LOADING', False)]:
            g = Gate(**{'current-age': 3, 'gl-island-migration-mission': CONSTANTS['MIGRATION-MISSION-SCOUT'], 'gl-island-migration-state': CONSTANTS[state]})
            self.assertEqual(g.accepts(retire), expected)
        for r in rows:
            if 'MIGRATION-' in r[3] and 'action-patrol' in r[4]: self.assertIn('(current-age < imperial-age)', r[3])

    def test_retirement_does_not_touch_resource_fishing_or_assault_screening(self):
        text = source('rawai-exploration-policy.per')
        for forbidden in ('transport-screen-group', 'attack-boarding-group', 'fishing-ship', 'MIGRATION-MISSION-MINING'):
            self.assertNotIn(forbidden, text)
        main = source('AI RAW.per')
        self.assertLess(main.index('(load "rawai-ownership")'), main.index('(load "rawai-exploration-policy")'))
        self.assertLess(main.index('(load "rawai-exploration-policy")'), main.index('(load "rawai-military")'))


if __name__ == '__main__': unittest.main()
