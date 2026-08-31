"""T17: execute actual hull claims/lease recovery; not an engine pathing test."""
import unittest

from test_assault_missions import Missions
from test_pre_backlog import source
from validate_naval_doctrine import rule_blocks


class TransportAcquisitionTests(unittest.TestCase):
    def fixture(self, kind, order=0, model=Missions):
        m = model()
        m.objects = {10: dict(id=10, player=2, hp=100, cargo=0, flag=-2,
                             point=(100, 100), idle=1, under_attack=0, order=order,
                             type='transport-ship', cls='transport-class')}
        m.remote, m.local, m.target, m.groups = [10], [], 10, {}
        migration = kind != 'assault'
        state = 'gl-island-migration-state' if migration else 'gl-transport-route-state'
        group = 'migration-transport-group' if migration else 'attack-transport-group'
        prefix = 'MIGRATION-' if migration else 'TRANSPORT-ROUTE-'
        find = prefix + ('FIND-TRANSPORT' if migration else 'LOAD-FIND')
        m.g[state] = m.val(find)
        m.g['gl-island-migration-mission'] = m.val('MIGRATION-MISSION-'+kind.upper())
        m.g['gl-island-scout-attempts'] = 0
        rows = list(rule_blocks(source('rawai-military.per')))
        claim = next(r for r in rows if f'(goal {state} {find})' in r[3]
                     and f'(up-create-group 0 0 c: {group})' in r[4]
                     and (not migration or 'MIGRATION-MISSION-'+kind.upper() in r[3]))
        verify = [r for r in rows if f'(goal {state} {prefix}HULL-VERIFY)' in r[3]]
        return m, state, group, prefix, claim, verify

    def acquire(self, m, claim, verify):
        self.assertTrue(m.rule(claim))
        for row in verify: m.rule(row)

    def test_idle_empty_reused_native_order_hulls_are_acquired_before_boarding(self):
        for kind in ('assault', 'mining', 'scout'):
            for order in (0, 714, 721):
                with self.subTest(kind=kind, order=order):
                    m, state, group, prefix, claim, verify = self.fixture(kind, order)
                    self.acquire(m, claim, verify)
                    self.assertEqual(m.groups[m.val(group)], [10])
                    self.assertEqual(m.objects[10]['flag'], m.val(group))
                    self.assertEqual(m.g[state], m.val(prefix+('LOAD-SELECT' if kind=='assault' else 'BOARDING')))
                    self.assertEqual(m.g['gl-island-scout-attempts'], int(kind=='scout'))
                    self.assertEqual(m.commands, [])  # acquisition is not a movement/STOP order

    def test_selection_to_claim_changes_cannot_board_or_consume_scout_attempt(self):
        for kind in ('assault', 'mining', 'scout'):
            for override in ({'player': 3}, {'flag': 0}, {'flag': 18}, {'flag': 19},
                             {'flag': 9}, {'cargo': 1}, {'idle': 0}, {'under_attack': 1}):
                with self.subTest(kind=kind, override=override):
                    m, state, group, prefix, claim, verify = self.fixture(kind, 714)
                    m.objects[10].update(override)
                    self.acquire(m, claim, verify)
                    self.assertEqual(m.g[state], m.val(prefix+'IDLE'))
                    self.assertEqual(m.groups.get(m.val(group)), [])
                    self.assertEqual(m.objects[10]['flag'], override.get('flag', -2))
                    self.assertEqual(m.g['gl-island-scout-attempts'], 0)
                    self.assertEqual(m.commands, [])
                    self.assertTrue(any('claim rejected hull:' in s for s, _ in m.logs))

    def test_missing_exact_lookup_does_not_advance_and_does_not_claim_another_hull(self):
        class MissingExact(Missions):
            def action(self, e, pc=0):
                if e[:2] == ['up-add-object-by-id', 'search-local']: return 0
                return super().action(e, pc)
        for kind in ('assault', 'mining', 'scout'):
            m, state, group, prefix, claim, verify = self.fixture(kind, model=MissingExact)
            m.objects[11] = dict(m.objects[10], id=11)
            self.acquire(m, claim, verify)
            self.assertEqual(m.g[state], m.val(prefix+'IDLE'))
            self.assertEqual(m.g['gl-island-scout-attempts'], 0)
            self.assertEqual(m.objects[11]['flag'], -2)

    def prepare_guard(self, kind, override=None):
        m, state, group, prefix, _, _ = self.fixture(kind)
        m.objects[10].update(cargo=9, flag=m.val(group))
        m.objects[10].update(override or {})
        hull = 'gl-transport-route-id' if kind=='assault' else 'gl-island-migration-transport-id'
        m.g[hull] = 10
        m.g[state] = m.val(prefix+('LOAD-WAIT' if kind=='assault' else 'LOADING'))
        m.g['gl-transport-route-script-load'] = m.val('YES')
        m.groups[m.val(group)] = [10]
        m.rules = list(rule_blocks(source('rawai-transport-preparation-ownership.per')))
        return m, state, group, prefix

    def guard(self, m):
        for row in m.rules: m.rule(row)

    def test_acknowledged_hulls_are_never_reordered_by_the_lease_guard(self):
        for kind in ('assault', 'mining', 'scout'):
            for idle in (0, 1):
                m, state, group, prefix = self.prepare_guard(kind, {'idle': idle, 'order': 714})
                before = m.g[state]
                self.guard(m)
                self.assertEqual(m.g[state], before)
                self.assertEqual(m.commands, [])
                self.assertEqual(m.logs, [])

    def test_lost_idle_original_hull_is_recovered_once_not_readmitted_as_success(self):
        for kind in ('assault', 'mining', 'scout'):
            m, state, group, prefix = self.prepare_guard(kind, {'flag': -2, 'order': 721})
            self.guard(m)
            expected = 'TRANSPORT-ROUTE-RECOVERY-WAIT' if kind=='assault' else 'MIGRATION-RETURNING'
            self.assertEqual(m.g[state], m.val(expected))
            self.assertEqual(m.objects[10]['flag'], m.val(group))
            self.assertEqual([(ids, action) for ids, action, _ in m.commands], [((10,), 'action-unload')])
            logs, commands = list(m.logs), list(m.commands)
            for _ in range(20): self.guard(m)
            self.assertEqual(m.logs, logs)
            self.assertEqual(m.commands, commands)

    def test_other_owners_active_native_voyages_and_missing_hulls_are_not_recovered(self):
        for kind in ('assault', 'mining', 'scout'):
            for override in ({'flag': 0}, {'flag': 18}, {'flag': 19}, {'flag': 9},
                             {'flag': -2, 'idle': 0, 'order': 714},
                             {'flag': -2, 'under_attack': 1}, {'player': 3}, None):
                with self.subTest(kind=kind, override=override):
                    m, state, group, prefix = self.prepare_guard(kind, override)
                    if override is None: del m.objects[10]
                    self.guard(m)
                    self.assertEqual(m.g[state], m.val(prefix+'IDLE'))
                    self.assertEqual(m.commands, [])
                    if 10 in m.objects:
                        self.assertEqual(m.objects[10]['flag'], override.get('flag', m.val(group)))

    def test_committed_voyage_slots_are_outside_preparation_recovery(self):
        m, state, _, _ = self.prepare_guard('assault', {'flag': 0})
        m.g[state] = m.val('TRANSPORT-ROUTE-IDLE')
        m.g['gl-am1-state'] = 1
        self.guard(m)
        self.assertEqual(m.g['gl-am1-state'], 1)
        self.assertEqual(m.commands, [])
        self.assertEqual(m.logs, [])


if __name__ == '__main__': unittest.main()
