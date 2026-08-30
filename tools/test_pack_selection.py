"""Execute the actual fallback selection rules against clobbered DUC lists.

This models selection/order recipients, not engine packing or search timing.
"""
import operator
import re
import unittest

from test_pre_backlog import expressions, source
from validate_naval_doctrine import rule_blocks


COMPARE = {'==': operator.eq, '!=': operator.ne, '>': operator.gt,
           '>=': operator.ge, '<': operator.lt, '<=': operator.le}
CONSTANTS = {name: int(value) for name, value in re.findall(
    r'\(defconst ([\w-]+) (-?\d+)\)',
    source('rawai-unitconstants.per') + source('rawai-customconstants.per'))}
CONSTANTS['my-player-number'] = 2


def obj(identity, kind, **overrides):
    result = {'object-data-id': identity, 'object-data-type': CONSTANTS[kind],
              'object-data-player': 2, 'object-data-group-flag': -1,
              'object-data-map-zone-id': 14, 'object-data-idling': 1,
              'object-data-under-attack': 0, 'object-data-garrisoned': 0}
    result.update({'object-data-' + key.replace('_', '-'): value
                   for key, value in overrides.items()})
    return result


class FallbackSelection:
    def __init__(self, world, incoming, zone):
        self.world, self.local = world, list(incoming)
        self.goals = {'gl-siege-target-state': CONSTANTS['SIEGE-TARGET-FALLBACK'],
                      'gl-siege-target-zone': zone, 'gl-siege-source-count': 99}
        self.commands, self.logs = [], []

    def value(self, token):
        if re.fullmatch(r'-?\d+', token):
            return int(token)
        if token in self.goals:
            return self.goals[token]
        return CONSTANTS[token]

    def fact(self, e):
        op, *a = e
        if op == 'goal':
            return self.value(a[0]) == self.value(a[1])
        if op == 'up-compare-goal':
            return COMPARE[a[1].split(':')[-1]](self.value(a[0]), self.value(a[2]))
        if op == 'up-set-target-object':
            assert a == ['search-local', 'c:', '0']
            return bool(self.local)
        if op == 'not':
            return not self.fact(a[0])
        raise AssertionError('unsupported selection fact: ' + repr(e))

    def action(self, e):
        op, *a = e
        if op == 'up-full-reset-search':
            self.local = []
        elif op == 'up-find-local':
            assert a[0] == a[2] == 'c:'
            self.local.extend([o for o in self.world
                               if o['object-data-player'] == 2
                               and o['object-data-type'] == self.value(a[1])
                               and not o['object-data-garrisoned']][:int(a[3])])
        elif op == 'up-remove-objects':
            assert a[0] == 'search-local'
            compare = COMPARE[a[2].split(':')[-1]]
            self.local = [o for o in self.local if not compare(o[a[1]], self.value(a[3]))]
        elif op == 'up-get-search-state':
            assert a == ['local-total']
            self.goals['local-total'] = len(self.local)
        elif op == 'up-modify-goal':
            assert a[1] == 'g:='
            self.goals[a[0]] = self.value(a[2])
        elif op == 'set-goal':
            self.goals[a[0]] = self.value(a[1])
        elif op == 'up-target-point':
            assert a == ['position-self-x', 'action-pack', '-1', 'stance-no-attack']
            self.commands.append([o['object-data-id'] for o in self.local])
        elif op == 'up-chat-data-to-self':
            self.logs.append(self.value(a[2]))
        elif op == 'up-set-timer':
            assert a == ['c:', 't-siege-target', 'c:', '12']
        else:
            raise AssertionError('unsupported selection action: ' + repr(e))

    def run(self):
        for row in rule_blocks(source('rawai-military.per')):
            if '(goal gl-siege-target-state SIEGE-TARGET-FALLBACK)' not in row[3]:
                continue
            if all(self.fact(e) for e in expressions(row[3])):
                for e in expressions(row[4]):
                    self.action(e)
        return self


class PackingSelectionTests(unittest.TestCase):
    def test_clobbered_building_list_never_receives_pack(self):
        buildings = [obj(4501, 'port'), obj(12511, 'shipyard')]
        result = FallbackSelection(buildings, buildings, 14).run()
        self.assertEqual(result.commands, [])
        self.assertEqual(result.logs, [])
        self.assertEqual(result.goals['gl-siege-target-state'], CONSTANTS['SIEGE-TARGET-IDLE'])

    def test_fresh_eligible_engine_is_reacquired_and_count_is_actual(self):
        buildings = [obj(4501, 'port'), obj(12511, 'shipyard')]
        result = FallbackSelection(buildings + [obj(4201, 'palintonon')], buildings, 14).run()
        self.assertEqual(result.commands, [[4201]])
        self.assertEqual(result.logs, [1])

    def test_owned_idle_ungarrisoned_unthreatened_unpacked_only(self):
        objects = [obj(1, 'palintonon'), obj(2, 'palintonon', group_flag=4),
                   obj(3, 'palintonon', player=3), obj(4, 'palintonon', idling=0),
                   obj(5, 'palintonon', under_attack=1),
                   obj(6, 'palintonon', garrisoned=1), obj(7, 'palintonon-packed'),
                   obj(8, 'battering-ram'), obj(9, 'port'), obj(10, 'shipyard')]
        result = FallbackSelection(objects, objects, 14).run()
        self.assertEqual(result.commands, [[1]])

    def test_objective_zone_and_global_emergency_scope_are_preserved(self):
        objects = [obj(1, 'palintonon'), obj(2, 'palintonon', map_zone_id=15)]
        self.assertEqual(FallbackSelection(objects, objects, 14).run().commands, [[1]])
        self.assertEqual(FallbackSelection(objects, objects, -1).run().commands, [[1, 2]])

    def test_every_pack_has_exact_unpacked_type_and_owner_boundary(self):
        rows = [r for r in rule_blocks(source('rawai-military.per'))
                if any(e[0] == 'up-target-point' and 'action-pack' in e
                       for e in expressions(r[4]))]
        self.assertEqual(len(rows), 2)
        for row in rows:
            actions = expressions(row[4])
            command = next(i for i, e in enumerate(actions) if 'action-pack' in e)
            for field, compare, value in [('type', '!=', 'palintonon'),
                                           ('player', '!=', 'my-player-number'),
                                           ('group-flag', '>=', '0')]:
                self.assertIn(['up-remove-objects', 'search-local', 'object-data-' + field,
                               compare, value], actions[:command])

    def test_fallback_rebuild_is_adjacent_and_emergency_clears_zone(self):
        rows = list(rule_blocks(source('rawai-military.per')))
        fallback = [i for i, r in enumerate(rows)
                    if '(goal gl-siege-target-state SIEGE-TARGET-FALLBACK)' in r[3]]
        self.assertEqual(len(fallback), 4)
        self.assertEqual(fallback, list(range(fallback[0], fallback[0] + 4)))
        preparation = rows[fallback[0]][4]
        self.assertLess(preparation.index('(up-full-reset-search)'),
                        preparation.index('(up-find-local c: palintonon c: 20)'))
        emergency = next(r for r in rows if '(unit-type-count-total palintonon >= 1)' in r[3]
                         and '(players-building-count any-enemy < 1)' in r[3])
        self.assertIn('(set-goal gl-siege-target-zone -1)', emergency[4])


if __name__ == '__main__':
    unittest.main()
