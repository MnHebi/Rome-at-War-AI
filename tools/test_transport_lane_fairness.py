"""Execute the shared migration/assault intake ordering contract."""
import unittest

from test_pre_backlog import source
from test_t13_gate_recovery import CMP, CONSTANTS, Gate
from validate_naval_doctrine import rule_blocks


class LaneGate(Gate):
    def __init__(self, route_due=True, admission_open=True, enemy=1,
                 home_defense=0, transports=1):
        super().__init__(**{
            'gl-island-migration-state': CONSTANTS['MIGRATION-IDLE'],
            'gl-relic-ferry-state': CONSTANTS['RELIC-FERRY-IDLE'],
            'gl-transport-recovery-state': CONSTANTS['TRANSPORT-RECOVERY-IDLE'],
            'gl-transport-repair-state': CONSTANTS['TRANSPORT-REPAIR-IDLE'],
            'gl-transport-route-state': CONSTANTS['TRANSPORT-ROUTE-IDLE'],
            'gl-transport-clear-state': CONSTANTS['TRANSPORT-CLEAR-IDLE'],
            'gl-colony-towncenter-state': CONSTANTS['COLONY-TC-IDLE'],
            'gl-assault-admission-open': int(admission_open),
            'gl-home-defense-state': home_defense,
            'gl-ap-seed-enemy': enemy,
            'map-type': CONSTANTS['ISLANDS'],
        })
        self.timers = {'t-island-migration': True,
                       't-transport-route': route_due}
        self.counts['transport-ship'] = transports

    def fact(self, e):
        op, *a = e
        if op == 'up-timer-status':
            return CMP[a[1]](self.timers.get(a[0], False),
                             a[2] == 'timer-triggered')
        if op == 'unit-type-count':
            return CMP[a[1]](self.counts.get(a[0], 0), self.value(a[2]))
        return super().fact(e)


class TransportLaneFairnessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rows = list(rule_blocks(source('rawai-military.per')))
        cls.migration = next(
            row for row in rows
            if '(set-goal gl-island-migration-state MIGRATION-GATE-OWNER)' in row[4]
        )
        cls.assault = next(
            row for row in rows
            if '(set-goal gl-transport-route-state TRANSPORT-ROUTE-FIND)' in row[4]
            and '(up-timer-status t-transport-route == timer-triggered)' in row[3]
        )

    def test_due_assault_gets_first_shared_lane_attempt(self):
        gate = LaneGate()
        self.assertFalse(gate.accepts(self.migration))
        self.assertTrue(gate.accepts(self.assault))

    def test_migration_proceeds_while_assault_timer_waits(self):
        gate = LaneGate(route_due=False)
        self.assertTrue(gate.accepts(self.migration))
        self.assertFalse(gate.accepts(self.assault))

    def test_nonviable_assault_does_not_starve_migration(self):
        for change in ({'admission_open': False}, {'enemy': 0},
                       {'home_defense': 1}, {'transports': 0}):
            with self.subTest(change=change):
                gate = LaneGate(**change)
                self.assertTrue(gate.accepts(self.migration))
                self.assertFalse(gate.accepts(self.assault))


if __name__ == '__main__':
    unittest.main()
