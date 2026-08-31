"""Execute the new PER policy against synthetic objects, not engine pathfinding.

No fixture invents cargo progress: tests explicitly supply it. Foundation requests
and concrete foundations remain separate, including delayed/failed placement.
"""
import math
import unittest
from test_pre_backlog import expressions, source
from test_t13_gate_recovery import CONSTANTS, CMP
from validate_naval_doctrine import rule_blocks

CONSTANTS = dict(CONSTANTS, dock=45)


def obj(i, kind, player=1, zone=3, point=(100, 100), carry=0, **kw):
    classes = {'fishing-ship': 'fishing-ship-class', 'fish-trap': 'farm-class',
               'dock': 'building-class', 'fish': 'ocean-fish-class'}
    o = dict(id=i, type=CONSTANTS.get(kind, 53), player=player, zone=zone,
             point=point, carry=carry, status=2, action=-1, idling=1, flag=-2,
             target=-1, attack=0, cls=CONSTANTS[classes[kind]])
    o.update(kw)
    return o


class Fishing:
    def __init__(self, objects):
        self.objects = {o['id']: o for o in objects}
        self.g = {'gl-game-time': 0, 'gl-owner-worker-hold': 0}
        self.sn = {'sn-focus-player-number': 7}
        self.local, self.remote, self.target = [], [], None
        self.point, self.radius, self.status = (0, 0), 99999, 2
        self.disabled, self.commands, self.builds = set(), [], []
        self.buildable, self.water_zone, self.pending = True, 3, False
        self.rules = list(rule_blocks(source('rawai-fishing.per')))

    def val(self, t):
        if t == 'my-player-number': return 1
        if t.lstrip('-').isdigit(): return int(t)
        if t in self.g: return self.g[t]
        if t.startswith('gl-'): return 0
        return CONSTANTS[t]

    def data(self, i, key):
        o = self.objects[i]
        if key == 'object-data-distance': return math.dist(o['point'], self.point)
        return o[{'object-data-id': 'id', 'object-data-type': 'type',
                  'object-data-player': 'player', 'object-data-map-zone-id': 'zone',
                  'object-data-carry': 'carry', 'object-data-action': 'action',
                  'object-data-status': 'status', 'object-data-idling': 'idling',
                  'object-data-group-flag': 'flag', 'object-data-target-id': 'target',
                  'object-data-under-attack': 'attack'}[key]]

    def fact(self, e):
        op, *a = e
        if op == 'true': return True
        if op == 'not': return not self.fact(a[0])
        if op in ('or', 'and'): return (any if op == 'or' else all)(self.fact(x) for x in a)
        if op == 'goal': return self.val(a[0]) == self.val(a[1])
        if op == 'up-compare-goal': return CMP[a[1].split(':')[-1]](self.val(a[0]), self.val(a[2]))
        if op == 'up-set-target-object':
            rows = self.local if a[0] == 'search-local' else self.remote
            self.target = rows[int(a[2])] if len(rows) > int(a[2]) else None
            return self.target is not None
        if op == 'up-object-data': return CMP[a[1].split(':')[-1]](self.data(self.target, a[0]), self.val(a[2]))
        if op in ('unit-type-count', 'building-type-count-total'):
            return CMP[a[1].split(':')[-1]](sum(o['type'] == self.val(a[0]) for o in self.objects.values() if o['player'] == 1), self.val(a[2]))
        if op == 'up-pending-objects': return CMP[a[2]](int(self.pending), int(a[3]))
        if op == 'up-pending-placement': return self.pending
        if op == 'up-can-build-line': return self.buildable
        raise AssertionError(('unmodeled fact', e))

    def putpoint(self, name, value):
        self.g[name], self.g[name[:-1]+'y'] = value

    def pointval(self, name): return (self.val(name), self.val(name[:-1]+'y'))

    def action(self, e, index):
        op, *a = e
        if op == 'disable-self': self.disabled.add(index)
        elif op == 'set-goal': self.g[a[0]] = self.val(a[1])
        elif op == 'set-strategic-number': self.sn[a[0]] = self.val(a[1])
        elif op == 'up-modify-goal':
            rhs = self.sn[a[2]] if a[1] == 's:=' else self.val(a[2])
            old = self.val(a[0])
            self.g[a[0]] = {'=': lambda: rhs, '+': lambda: old+rhs,
                           '-': lambda: old-rhs, '*': lambda: old*rhs}[a[1][-1]]()
        elif op == 'up-modify-sn': self.sn[a[0]] = self.val(a[2])
        elif op == 'up-get-indirect-goal': self.g[a[2]] = self.g.get(self.val(a[1]), 0)
        elif op == 'up-set-indirect-goal':
            address = self.val(a[1])
            assert CONSTANTS['FISH-WATCH-BASE'] <= address < CONSTANTS['FISH-WATCH-END']
            self.g[address] = self.val(a[3])
        elif op == 'up-get-fact':
            self.g[a[2]] = sum(o['type'] == self.val(a[1]) for o in self.objects.values() if o['player'] == 1)
        elif op == 'up-full-reset-search':
            self.local, self.remote = [], []
            self.radius, self.status = 99999, 2
        elif op == 'up-reset-search':
            if a[1] == '1': self.local = []
            if a[3] == '1': self.remote = []
        elif op == 'up-reset-filters': self.radius, self.status = 99999, 2
        elif op == 'up-filter-distance': self.radius = self.val(a[-1])
        elif op == 'up-filter-status': self.status = self.val(a[1])
        elif op == 'up-set-target-point': self.point = self.pointval(a[0])
        elif op == 'up-get-point': self.putpoint(a[1], self.objects[self.target]['point'])
        elif op == 'up-copy-point': self.putpoint(a[0], self.pointval(a[1]))
        elif op == 'up-get-point-zone': self.g[a[1]] = self.water_zone
        elif op == 'up-get-object-data': self.g[a[1]] = self.data(self.target, a[0])
        elif op in ('up-find-local', 'up-find-remote', 'up-find-status-remote'):
            local = op == 'up-find-local'
            owner = 1 if local else self.sn['sn-focus-player-number']
            kind = self.val(a[1]); rows = self.local if local else self.remote
            for i, o in sorted(self.objects.items()):
                if o['player'] != owner or kind not in (o['type'], o['cls']): continue
                statuses = (self.status,) if op == 'up-find-status-remote' else ((0, 1, 2, 3) if kind == o['type'] else (2,))
                if o['status'] not in statuses or self.data(i, 'object-data-distance') > self.radius: continue
                if i not in rows: rows.append(i)
        elif op == 'up-add-object-by-id':
            rows = self.local if a[0] == 'search-local' else self.remote
            i = self.val(a[2])
            if i in self.objects and i not in rows: rows.append(i)
        elif op == 'up-remove-objects':
            rows = self.local if a[0] == 'search-local' else self.remote
            kept = [i for n, i in enumerate(rows) if not CMP[a[2].split(':')[-1]](
                n if a[1] == 'object-data-index' else self.data(i, a[1]), self.val(a[3]))]
            if a[0] == 'search-local': self.local = kept
            else: self.remote = kept
        elif op == 'up-clean-search':
            rows = self.local if a[0] == 'search-local' else self.remote
            rows.sort(key=lambda i: self.data(i, a[1]))
        elif op == 'up-get-search-state': self.g[a[0]] = len(self.local)
        elif op == 'up-target-objects':
            self.commands.append((self.val('gl-game-time'), tuple(self.local), tuple(self.remote), a[1]))
        elif op == 'up-build-line': self.builds.append((self.val('gl-game-time'), self.pointval(a[0]), self.val(a[-1])))
        elif op in ('up-assign-builders', 'up-chat-data-to-self'): pass
        else: raise AssertionError(('unmodeled action', e))

    def sweep(self, time):
        self.g['gl-game-time'] = time
        for index, r in enumerate(self.rules):
            if index in self.disabled: continue
            if all(self.fact(e) for e in expressions(r[3])):
                for e in expressions(r[4]): self.action(e, index)
        assert self.sn['sn-focus-player-number'] == 7

    def run(self, start, end):
        for t in range(start, end): self.sweep(t)


class FishingPolicyTests(unittest.TestCase):
    def test_visible_fish_beats_exploration_and_commands_are_bounded(self):
        f = Fishing([obj(1, 'fishing-ship', action=605), obj(3, 'fish', player=0, carry=100, status=3)])
        f.run(0, 120)
        self.assertTrue(f.commands)
        self.assertTrue(all(c[1:] == ((1,), (3,), 'action-gather') for c in f.commands))
        self.assertLessEqual(len(f.commands), 2)
        self.assertEqual(f.builds, [])

    def test_no_fish_or_stuck_visible_fish_gets_a_concrete_trap(self):
        for known in (False, True):
            objects = [obj(1, 'fishing-ship', action=605), obj(2, 'dock')]
            if known: objects.append(obj(3, 'fish', player=0, carry=100))
            f = Fishing(objects); f.run(0, 180)
            self.assertEqual(len(f.builds), 1)
            self.assertEqual(f.builds[0][1:], ((105, 100), CONSTANTS['fish-trap']))
            self.assertFalse(any(c[-1] == 'action-default' for c in f.commands))
            # Foundation is a distinct later engine event, not inferred from build.
            f.objects[9] = obj(9, 'fish-trap', point=(105, 100), status=0)
            f.run(180, 380)
            assignments = [c for c in f.commands if c[-1] == 'action-default']
            self.assertTrue(assignments)
            self.assertTrue(all(c[1:3] == ((1,), (9,)) for c in assignments))

    def test_cargo_progress_resets_watch_not_just_order_issuance(self):
        f = Fishing([obj(1, 'fishing-ship'), obj(2, 'dock')]); f.run(0, 130)
        f.objects[1]['carry'] = 5; f.sweep(130)
        f.run(131, 220)
        self.assertEqual(f.builds, [])

    def test_foundation_arriving_within_deadline_gets_its_builder_immediately(self):
        f = Fishing([obj(1, 'fishing-ship'), obj(2, 'dock')]); f.run(0, 165)
        self.assertEqual(len(f.builds), 1)
        f.objects[9] = obj(9, 'fish-trap', point=(105, 100), status=0)
        f.sweep(165)
        self.assertEqual(f.commands[-1], (165, (1,), (9,), 'action-default'))

    def test_lost_ship_cannot_issue_or_report_foundation_assignment(self):
        for changes in ({'player': 2}, {'flag': 7}, {'carry': 5}):
            f = Fishing([obj(1, 'fishing-ship'), obj(2, 'dock')]); f.run(0, 165)
            f.objects[1].update(changes)
            f.objects[9] = obj(9, 'fish-trap', point=(105, 100), status=0)
            f.sweep(165)
            self.assertFalse(any(c[-1] == 'action-default' for c in f.commands), changes)

    def test_busy_carrying_reserved_or_attacked_ship_is_not_retasked(self):
        for changes in ({'carry': 10}, {'flag': 7}, {'attack': 1}, {'action': CONSTANTS['actionid-build']}):
            f = Fishing([obj(1, 'fishing-ship', **changes), obj(2, 'dock'), obj(3, 'fish', player=0, carry=100)])
            f.run(0, 400)
            self.assertEqual(f.builds, [], changes)
            self.assertEqual(f.commands, [], changes)

    def test_other_water_or_hostile_port_does_not_become_target(self):
        f = Fishing([obj(1, 'fishing-ship'), obj(2, 'dock', player=2), obj(3, 'fish', player=0, zone=4, carry=100)])
        f.run(0, 400)
        self.assertEqual((f.builds, f.commands), ([], []))

    def test_unused_trap_is_reused_and_another_fisher_is_not_displaced(self):
        f = Fishing([obj(1, 'fishing-ship'), obj(2, 'dock'), obj(3, 'fish-trap', carry=500),
                     obj(4, 'fishing-ship', target=3, carry=5), obj(5, 'fish-trap', carry=500)])
        f.run(0, 200)
        self.assertEqual(f.builds, [])
        self.assertTrue(any(c[1:3] == ((1,), (5,)) for c in f.commands))
        self.assertFalse(any(3 in c[2] for c in f.commands))

    def test_invalid_geometry_and_missing_foundation_do_not_spam_builds(self):
        for setting in ('buildable', 'water_zone'):
            f = Fishing([obj(1, 'fishing-ship'), obj(2, 'dock')])
            setattr(f, setting, False if setting == 'buildable' else 9)
            f.run(0, 400)
            self.assertEqual(f.builds, [])
            self.assertLessEqual(f.g['gl-fish-attempt'], 4)
        f = Fishing([obj(1, 'fishing-ship'), obj(2, 'dock')]); f.run(0, 300)
        self.assertEqual(len(f.builds), 1)

    def test_slot_replacement_does_not_inherit_failure_deadline(self):
        f = Fishing([obj(1, 'fishing-ship'), obj(2, 'dock')]); f.run(0, 145)
        del f.objects[1]; f.objects[10] = obj(10, 'fishing-ship')
        f.run(145, 240)
        self.assertEqual(f.builds, [])

    def test_all_normal_fleet_members_are_sampled_and_indirect_memory_is_bounded(self):
        f = Fishing([obj(i, 'fishing-ship', carry=5) for i in range(1, 41)])
        f.run(0, 140)
        self.assertEqual({f.g[14400 + 4*i] for i in range(40)}, set(range(1, 41)))
        self.assertLess(f.g['gl-fish-slot'], 40)

    def test_source_no_fishing_deletion_or_native_disable_and_targeted_build_only(self):
        self.assertNotIn('(delete-unit fishing-ship)', source('rawai-economy.per'))
        text = source('rawai-fishing.per')
        self.assertNotIn('(build fish-trap)', text)
        self.assertNotIn('action-stop', text)
        self.assertNotIn('action-explore', text)
        self.assertIn('(up-assign-builders c: fish-trap c: -1)', text)
        self.assertNotIn('sn-maximum-fish-boat-drop-distance', text)
        for r in rule_blocks(text):
            if 'up-target-objects' in r[4]:
                self.assertIn('object-data-id g:!= gl-fish-id', r[4])
                self.assertIn('object-data-group-flag >= 0', r[4])
                if 'action-gather' in r[4]:
                    self.assertIn('(up-reset-search 1 1 0 0)', r[4])
                else:
                    self.assertIn('(up-compare-goal local-total c:> 0)', r[3])


if __name__ == '__main__': unittest.main()
