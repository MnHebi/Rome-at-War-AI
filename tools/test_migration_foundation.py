"""Concrete-foundation boundary fixtures (not engine placement/path proof)."""
import unittest
from test_attack_verification import Verifier, obj
from test_pre_backlog import source, expressions
from validate_naval_doctrine import rule_blocks


class Foundation(Verifier):
    def val(self, token):
        return 2 if token == 'my-player-number' else super().val(token)

    def __init__(self, objects):
        super().__init__(objects)
        self.g.update({'gl-island-migration-state': self.val('MIGRATION-WAIT-DROPSITE'),
                       'gl-island-migration-anchor-class': self.val('stone-mine-class'),
                       'gl-island-migration-zone': 9, 'gl-migration-build-x': 53,
                       'gl-migration-build-y': 50, 'gl-island-migration-target-x': 50,
                       'gl-island-migration-target-y': 50})

    def action(self, e, pc):
        op, *a = e
        if op == 'set-strategic-number': self.sn[a[0]] = 2
        elif op == 'up-filter-distance': self.radius = self.val(a[-1])
        elif op == 'up-filter-status': self.status = self.val(a[1])
        elif op == 'up-find-status-local':
            self.remote = []
            for i, o in self.objects.items():
                self.target = i
                if (o['player'] == 2 and o['type'] == a[1] and o['status'] == self.status
                        and self.data('object-data-distance') <= self.radius):
                    self.remote.append(i)
        elif op == 'up-clean-search': pass
        else: return super().action(e, pc)
        return 0

    def fact(self, e):
        if e[0] == 'or': return any(self.fact(x) for x in e[1:])
        return super().fact(e)

    def sweep(self):
        for row in rule_blocks(source('rawai-military.per')):
            facts = row[3]
            if not ('MIGRATION-WAIT-DROPSITE)' in facts and 'up-find-status-local' in row[4]
                    or 'MIGRATION-FIND-DROPSITE)' in facts): continue
            if all(self.fact(e) for e in expressions(facts)):
                for e in expressions(row[4]): self.action(e, row[0])
        return self.g['gl-island-migration-state']


def camp(**kw):
    o = obj(99, 2, point=(53, 50))
    o.update(type='mining-camp', status=0)
    o.update(kw)
    return o


class FoundationTests(unittest.TestCase):
    def test_delayed_foundation_does_not_recall_settlers(self):
        f = Foundation([])
        for _ in range(19): self.assertEqual(f.sweep(), f.val('MIGRATION-WAIT-DROPSITE'))
        f.objects[99] = camp(status=f.val('status-pending'))
        self.assertEqual(f.sweep(), f.val('MIGRATION-ASSIGN-DROPSITE'))

    def test_wrong_owner_type_zone_anchor_or_issued_point_ignored(self):
        for kw in ({'player': 3}, {'type': 'lumber-camp'}, {'zone': 8},
                   {'point': (60, 50)}, {'point': (44, 50)}):
            f = Foundation([camp(**kw)])
            f.objects[99]['status'] = f.val('status-pending')
            self.assertEqual(f.sweep(), f.val('MIGRATION-WAIT-DROPSITE'), kw)

    def test_global_pending_is_not_a_progress_gate(self):
        rows = [r for r in rule_blocks(source('rawai-military.per'))
                if 'MIGRATION-WAIT-DROPSITE)' in r[3] and 'up-find-status-local' in r[4]]
        self.assertEqual(len(rows), 3)
        for row in rows: self.assertNotIn('up-pending-objects', row[3])

    def test_deadline_and_four_offsets_preserved(self):
        rows = list(rule_blocks(source('rawai-military.per')))
        wait = [r for r in rows if 'MIGRATION-FIND-DROPSITE)' in r[3]]
        self.assertTrue(all('up-set-timer' not in r[4] for r in wait))
        expires = [r for r in rows if 'MIGRATION-WAIT-DROPSITE)' in r[3]
                   and 'timer-triggered' in r[3]]
        self.assertEqual(len(expires), 2)
        self.assertTrue(any('placement-attempts c:< 4' in r[3] for r in expires))
        self.assertTrue(any('placement-attempts c:>= 4' in r[3] for r in expires))


if __name__ == '__main__': unittest.main()
