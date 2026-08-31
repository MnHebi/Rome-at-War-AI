"""Concrete-foundation boundary fixtures (not engine placement/path proof)."""
import unittest
from test_attack_verification import Verifier, obj
from test_pre_backlog import source, expressions
from validate_naval_doctrine import rule_blocks
from test_t13_gate_recovery import Gate, CONSTANTS


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


class PlacementPoint(Gate):
    def __init__(self, kind, attempt=0):
        super().__init__(**{'gl-island-migration-state': CONSTANTS['MIGRATION-PLACE-DROPSITE'],
            'gl-island-migration-placement-attempts': attempt, 'gl-owner-worker-hold': 0,
            'gl-island-migration-anchor-class': CONSTANTS[{
                'mining-camp': 'stone-mine-class', 'lumber-camp': 'tree-class', 'mill': 'forage-class'}[kind]],
            'gl-island-migration-target-x': 32, 'gl-island-migration-target-y': 51})
        self.kind, self.target, self.builds = kind, (158, 211), []
        # position-target is an enemy building, NOT up-set-target-point.
        self.enemy_point = (162, 137)
        self.queued_point = (154, 124)  # Red T17's first misplaced BUILD packet.
        self.point_buildable = True
        self.point_checks = []

    def fact(self, e):
        if e[0] == 'up-can-build-line':
            self.point_checks.append((e[-1], self.point(e[2])))
            return self.point_buildable
        return super().fact(e)

    def point(self, key): return (self.goals[key], self.goals[key[:-1] + 'y'])

    def store_point(self, key, value):
        self.goals[key], self.goals[key[:-1] + 'y'] = value

    def execute(self, row):
        if not self.accepts(row): return
        for op, *a in expressions(row[4]):
            if op == 'set-goal': self.goals[a[0]] = self.value(a[1])
            elif op in ('up-copy-point', 'up-bound-point'):
                # All test points are inside the 220x220 map, so bounding is identity.
                self.store_point(a[0], self.point(a[1]))
            elif op == 'up-modify-goal':
                self.goals[a[0]] += self.value(a[2]) * (-1 if a[1] == 'c:-' else 1)
            elif op == 'up-set-target-point': self.target = self.point(a[0])
            elif op == 'up-get-point':
                assert a[0] == 'position-target'
                self.store_point(a[1], self.enemy_point)
            elif op == 'up-build':
                # Native place-point searches a growing region, rather than
                # promising to use the requested point (AIRef + T17 packets).
                self.builds.append((a[-1], self.queued_point))
            elif op == 'up-build-line':
                assert self.point(a[0]) == self.point(a[1]), 'one foundation only'
                self.builds.append((a[-1], self.point(a[0])))
            elif op not in ('up-set-timer', 'up-chat-data-to-self'): raise AssertionError(op)

    def prepare(self):
        for r in rule_blocks(source('rawai-military.per')):
            if '(goal gl-island-migration-state MIGRATION-PLACE-DROPSITE)' in r[3]: self.execute(r)

    def issue(self):
        for r in rule_blocks(source('rawai-military.per')):
            if ('(goal gl-island-migration-state MIGRATION-ISSUE-DROPSITE)' in r[3]
                    and (f'(up-build place-point 0 c: {self.kind})' in r[4]
                         or f'(up-build-line gl-migration-build-x gl-migration-build-x c: {self.kind})' in r[4])):
                self.execute(r)

    def reject(self):
        for r in rule_blocks(source('rawai-military.per')):
            if ('(goal gl-island-migration-state MIGRATION-ISSUE-DROPSITE)' in r[3]
                    and f'(can-afford-building {self.kind})' in r[3]
                    and 'migration rejected' in r[4]): self.execute(r)


class PlacementPointLifetimeTests(unittest.TestCase):
    def test_delayed_request_ignores_another_controllers_target_point(self):
        for kind in ('mining-camp', 'lumber-camp', 'mill'):
            for attempt, offset in enumerate(((3, 3), (-3, 3), (3, -3), (-3, -3))):
                p = PlacementPoint(kind, attempt)
                p.prepare()
                p.buildable = False
                p.issue()
                self.assertEqual(p.builds, [])
                p.target = (158, 211)  # Unrelated global point, not a decoded request.
                p.buildable = True
                p.issue()
                self.assertEqual(p.builds, [(kind, (32 + offset[0], 51 + offset[1]))])
                self.assertEqual(p.point('gl-t12-drop-x'), p.builds[0][1])

    def test_immediate_request_and_attempt_limit_are_preserved(self):
        for kind in ('mining-camp', 'lumber-camp', 'mill'):
            p = PlacementPoint(kind)
            p.prepare(); p.issue()
            self.assertEqual(p.builds, [(kind, (35, 54))])
            p = PlacementPoint(kind, 4)
            p.prepare(); p.issue()
            self.assertEqual(p.builds, [])

    def test_t17_exact_foundation_is_accepted_without_queue_drift(self):
        p = PlacementPoint('mining-camp')
        p.store_point('gl-island-migration-target-x', (175, 136))
        p.prepare(); p.issue()
        self.assertEqual(p.builds, [('mining-camp', (178, 139))])
        self.assertEqual(p.point_checks, [('mining-camp', (178, 139))])
        self.assertNotEqual(p.builds[0][1], p.queued_point)
        self.assertNotEqual(p.point('gl-t12-drop-x'), p.enemy_point)
        f = Foundation([camp(point=p.builds[0][1])])
        f.objects[99]['status'] = f.val('status-pending')
        f.g.update({'gl-island-migration-target-x': 175, 'gl-island-migration-target-y': 136,
                    'gl-migration-build-x': 178, 'gl-migration-build-y': 139})
        self.assertEqual(f.sweep(), f.val('MIGRATION-ASSIGN-DROPSITE'))

    def test_t17_far_foundations_are_not_accepted_as_colony_progress(self):
        for point in ((154, 124), (152, 126), (151, 113)):
            f = Foundation([camp(point=point)])
            f.objects[99]['status'] = f.val('status-pending')
            f.g.update({'gl-island-migration-target-x': 175, 'gl-island-migration-target-y': 136,
                        'gl-migration-build-x': 178, 'gl-migration-build-y': 139})
            self.assertEqual(f.sweep(), f.val('MIGRATION-WAIT-DROPSITE'))

    def test_exact_blocked_points_advance_four_offsets_then_fail_bounded(self):
        for kind in ('mining-camp', 'lumber-camp', 'mill'):
            p = PlacementPoint(kind)
            p.point_buildable = False
            for attempt in range(4):
                p.prepare(); p.issue(); p.reject()
                self.assertEqual(p.builds, [])
                state = p.goals['gl-island-migration-state']
                if attempt < 3:
                    self.assertEqual(state, CONSTANTS['MIGRATION-VALIDATE-DROPSITE-ANCHOR'])
                    self.assertEqual(p.goals['gl-island-migration-placement-attempts'], attempt + 1)
                    # Successful exact-anchor revalidation leads back to PLACE.
                    p.goals['gl-island-migration-state'] = CONSTANTS['MIGRATION-PLACE-DROPSITE']
                else:
                    self.assertEqual(state, CONSTANTS['MIGRATION-DROPSITE-FAILED'])

    def test_no_escrow_ownership_or_pending_placement_bypass(self):
        for kind in ('mining-camp', 'lumber-camp', 'mill'):
            for block in ('escrow', 'owner', 'pending', 'placement', 'point'):
                p = PlacementPoint(kind); p.prepare()
                if block == 'escrow': p.buildable = False  # exact-point API alone could pass
                if block == 'owner': p.goals['gl-owner-worker-hold'] = 1
                if block == 'pending': p.pending.add(kind)
                if block == 'placement': p.placement.add(kind)
                if block == 'point': p.point_buildable = False
                p.issue()
                self.assertEqual(p.builds, [], (kind, block))

    def test_generic_unavailability_keeps_existing_bounded_recovery(self):
        for kind in ('mining-camp', 'lumber-camp', 'mill'):
            p = PlacementPoint(kind); p.prepare(); p.buildable = False
            p.issue(); p.reject()
            self.assertEqual(p.builds, [])
            self.assertEqual(p.goals['gl-island-migration-state'],
                             CONSTANTS['MIGRATION-VALIDATE-DROPSITE-ANCHOR'])


if __name__ == '__main__': unittest.main()
