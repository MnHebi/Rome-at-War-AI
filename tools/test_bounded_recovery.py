"""Exercise actual recovery-check predicates and command bounds, not pathfinding."""
import unittest
from test_attack_verification import Verifier, obj
from test_pre_backlog import source, expressions
from validate_naval_doctrine import rule_blocks


class Recovery(Verifier):
    def __init__(self, busy=False):
        super().__init__([obj(99, 2, point=(0, 0))])
        self.g.update({'gl-transport-route-id': 99, 'gl-quarantine-transport-id': 88 if busy else -1,
                       'gl-transport-route-script-load': self.val('YES')})
        self.loaded, self.orders = 10, []

    def val(self, t): return 2 if t == 'my-player-number' else super().val(t)

    def data(self, field, target=False):
        if field == 'object-data-garrison-count': return self.loaded
        if field == 'object-data-group-flag': return self.val('attack-transport-group')
        return super().data(field, target)

    def action(self, e, pc):
        if e[0] == 'up-target-point': self.orders.append(e[1:])
        elif e[0] in ('up-modify-group-flag', 'up-reset-group', 'up-set-timer', 'up-chat-data-to-self'): pass
        else: return super().action(e, pc)
        return 0

    def check(self):
        self.g['gl-transport-route-state'] = self.val('TRANSPORT-ROUTE-RECOVERY-CHECK')
        self.remote, self.target = list(self.objects), 99 if self.objects else None
        for row in rule_blocks(source('rawai-military.per')):
            if '(goal gl-transport-route-state TRANSPORT-ROUTE-RECOVERY-CHECK)' not in row[3]: continue
            if all(self.fact(e) for e in expressions(row[3])):
                for e in expressions(row[4]): self.action(e, row[0])


class RecoveryTests(unittest.TestCase):
    def test_three_retries_then_exact_hull_terminal_quarantine(self):
        r = Recovery()
        for _ in range(4): r.check()
        self.assertEqual([x[0] for x in r.orders], ['gl-home-anchor-x']*2+['gl-transport-route-origin-x'])
        self.assertEqual(r.g['gl-quarantine-transport-id'], 99)
        self.assertEqual(r.g['gl-quarantine-transport-attempts'], 3)
        self.assertEqual(r.g['gl-transport-route-state'], r.val('TRANSPORT-ROUTE-IDLE'))

    def test_busy_quarantine_does_not_restart_retry_budget(self):
        r = Recovery(busy=True)
        for _ in range(40): r.check()
        self.assertEqual(len(r.orders), 3)
        self.assertEqual(r.g['gl-quarantine-transport-id'], 88)
        r.g['gl-quarantine-transport-id'] = -1
        r.check()
        self.assertEqual(r.g['gl-quarantine-transport-id'], 99)
        self.assertEqual(len(r.orders), 3)

    def test_empty_or_missing_hull_releases_without_retry(self):
        for missing in (False, True):
            r = Recovery()
            if missing: r.objects.clear()
            else: r.loaded = 0
            r.check()
            self.assertEqual(r.orders, [])
            self.assertEqual(r.g['gl-transport-route-state'], r.val('TRANSPORT-ROUTE-IDLE'))

    def test_every_external_recovery_entry_resets_budget(self):
        for row in rule_blocks(source('rawai-military.per')):
            if '(set-goal gl-transport-route-state TRANSPORT-ROUTE-RECOVERY-WAIT)' not in row[4]: continue
            if 'TRANSPORT-ROUTE-RECOVERY-CHECK' in row[3]: continue
            self.assertIn('(set-goal gl-route-unload-attempts 0)', row[4])


if __name__ == '__main__': unittest.main()
