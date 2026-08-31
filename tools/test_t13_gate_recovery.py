"""Execute the actual T13 gates; not engine placement or trade-route proof."""
import operator
import re
import unittest

from test_pre_backlog import expressions, source
from validate_naval_doctrine import rule_blocks

CMP = {'==': operator.eq, '!=': operator.ne, '>': operator.gt,
       '>=': operator.ge, '<': operator.lt, '<=': operator.le}
CONSTANTS = {k: int(v) for k, v in re.findall(r'\(defconst ([\w-]+) (-?\d+)\)',
    source('rawai-constants.per') + source('rawai-unitconstants.per') + source('rawai-customconstants.per'))}
# Engine age constants are built-ins, not runtime declarations.
CONSTANTS.update({'dark-age': 0, 'feudal-age': 1, 'castle-age': 2, 'imperial-age': 3,
                  'early-antiquity-age': 1, 'middle-antiquity-age': 2})


class Gate:
    def __init__(self, **goals):
        self.goals = dict(goals)
        self.counts = {}
        self.pending = set()
        self.placement = set()
        self.affordable = self.buildable = True

    def value(self, token):
        if re.fullmatch(r'-?\d+', token): return int(token)
        return self.goals.get(token, CONSTANTS.get(token, token))

    def fact(self, e):
        op, *a = e
        if op in ('or', 'and'): return (any if op == 'or' else all)(self.fact(x) for x in a)
        if op == 'not': return not self.fact(a[0])
        if op == 'goal': return self.value(a[0]) == self.value(a[1])
        if op == 'up-compare-goal': return CMP[a[1].split(':')[-1]](self.value(a[0]), self.value(a[2]))
        if op in ('current-age', 'game-time'): return CMP[a[0]](self.value(op), self.value(a[1]))
        if op in ('building-type-count', 'building-type-count-total', 'unit-type-count-total'):
            return CMP[a[1].split(':')[-1]](self.counts.get(a[0], 0), self.value(a[2]))
        if op == 'can-afford-building': return self.affordable
        if op == 'up-can-build': return self.buildable
        if op == 'up-pending-placement': return a[1] in self.placement
        if op == 'up-pending-objects': return CMP[a[2]](int(a[1] in self.pending), int(a[3]))
        if op == 'player-in-game': return True
        raise AssertionError('unmodeled gate: ' + repr(e))

    def accepts(self, row):
        return all(self.fact(e) for e in expressions(row[3]))


def build_gate(kind, count=0, centers=1):
    g = Gate(**{'current-age': CONSTANTS['imperial-age'], 'gl-owner-worker-hold': 0,
        'wait-techup-requirements': 0, 'gl-migration-placement-lock': 0,
        'gl-placement-pressure-state': CONSTANTS['PLACEMENT-PRESSURE-IDLE'],
        'gl-game-time': 5000, 'gl-castle-request-next': 0, 'gl-placement-pressure-next': 0,
        'desired-number-castles': 3, 'desired-number-stables': 3, 'desired-number-ranges': 3,
        'gl-home-defense-state': 0, 'rush-rushing': 0})
    g.counts = {'town-center': centers, 'barracks': 1, kind: count}
    return g


class FirstMilitaryBuildingTests(unittest.TestCase):
    @staticmethod
    def rule(kind):
        rows = [r for r in rule_blocks(source('rawai-homebase.per'))
                if f'(up-build place-normal 0 c: {kind})' in r[4]]
        assert len(rows) == 1, (kind, len(rows))
        return rows[0]

    def test_single_completed_tc_can_request_first_demanded_structure(self):
        for kind in ('castle', 'archery-range', 'stable'):
            self.assertTrue(build_gate(kind).accepts(self.rule(kind)), kind)

    def test_expansion_still_requires_original_policy(self):
        for kind in ('castle', 'archery-range', 'stable'):
            self.assertFalse(build_gate(kind, count=1).accepts(self.rule(kind)), kind)
            self.assertTrue(build_gate(kind, count=1, centers=2).accepts(self.rule(kind)), kind)
            self.assertFalse(build_gate(kind, centers=0).accepts(self.rule(kind)), kind)

    def test_first_structure_does_not_bypass_need_resources_or_worker_ownership(self):
        for kind, desired in (('castle', 'desired-number-castles'),
                              ('archery-range', 'desired-number-ranges'), ('stable', 'desired-number-stables')):
            for change in ('demand', 'resources', 'workers', 'placement'):
                g = build_gate(kind)
                if change == 'demand': g.goals[desired] = 0
                if change == 'resources': g.affordable = False
                if change == 'workers': g.goals['gl-owner-worker-hold'] = 1
                if change == 'placement': g.buildable = False
                self.assertFalse(g.accepts(self.rule(kind)), (kind, change))

    def test_fortress_pressure_recovery_has_same_first_structure_admission(self):
        rows = [r for r in rule_blocks(source('rawai-homebase.per'))
                if '(not (up-can-build 0 c: castle))' in r[3]]
        self.assertEqual(len(rows), 1)
        g = build_gate('castle'); g.buildable = False
        self.assertTrue(g.accepts(rows[0]))
        g.counts['castle'] = 1
        self.assertFalse(g.accepts(rows[0]))


