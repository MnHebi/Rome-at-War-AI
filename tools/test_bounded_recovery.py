"""Exercise actual recovery-check predicates and command bounds, not pathfinding."""
import unittest
from test_assault_preparation import Preparation
from test_pre_backlog import source, expressions
from validate_naval_doctrine import rule_blocks


class Recovery(Preparation):
    def __init__(self, busy=False):
        super().__init__()
        self.recovering(cargo=10, distance=0)
        self.g.update({'gl-quarantine-transport-id': 88 if busy else -1,
                       'gl-route-unload-attempts': 0})

    def check(self):
        self.sweep(15)


class RecoveryTests(unittest.TestCase):
    def test_three_retries_then_exact_hull_terminal_quarantine(self):
        r = Recovery()
        for _ in range(4): r.check()
        self.assertEqual(len(r.commands), 3)
        self.assertTrue(all(action == 'action-unload' for _, action, _ in r.commands))
        self.assertEqual(r.g['gl-quarantine-transport-id'], 10)
        self.assertEqual(r.g['gl-quarantine-transport-attempts'], 3)
        self.assertEqual(r.g['gl-transport-route-state'], r.val('TRANSPORT-ROUTE-IDLE'))

    def test_busy_quarantine_does_not_restart_retry_budget(self):
        r = Recovery(busy=True)
        for _ in range(40): r.check()
        self.assertEqual(len(r.commands), 3)
        self.assertEqual(r.g['gl-quarantine-transport-id'], 88)
        self.assertEqual(r.g['gl-transport-route-state'], r.val('TRANSPORT-ROUTE-IDLE'))
        r.g['gl-quarantine-transport-id'] = -1
        r.check()
        self.assertEqual(r.g['gl-quarantine-transport-id'], -1)
        self.assertEqual(len(r.commands), 3)

    def test_empty_or_missing_hull_releases_without_retry(self):
        for missing in (False, True):
            r = Recovery()
            if missing: r.objects.clear()
            else: r.objects[10]['cargo'] = 0
            r.check()
            self.assertEqual(r.commands, [])
            self.assertEqual(r.g['gl-transport-route-state'], r.val('TRANSPORT-ROUTE-IDLE'))

    def test_every_external_recovery_entry_resets_budget(self):
        for row in rule_blocks(source('rawai-military.per')):
            if '(set-goal gl-transport-route-state TRANSPORT-ROUTE-RECOVERY-WAIT)' not in row[4]: continue
            if 'TRANSPORT-ROUTE-RECOVERY-CHECK' in row[3]: continue
            self.assertIn('(set-goal gl-route-unload-attempts 0)', row[4])


if __name__ == '__main__': unittest.main()
