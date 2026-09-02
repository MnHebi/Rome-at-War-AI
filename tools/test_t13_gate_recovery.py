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


class TradeProducerEpochTests(unittest.TestCase):
    @staticmethod
    def gate(land=False):
        state = 'TRADE-ROUTE-LAND-PROOF-START' if land else 'TRADE-ROUTE-WATER-PROOF-START'
        g = Gate(**{
            'current-age': CONSTANTS['imperial-age'], 'team-game': 1,
            'gl-trade-route-state': CONSTANTS[state],
            'gl-land-trade-route': int(land),
            'gl-water-trade-route': int(not land),
            'gl-game-time': 5000, 'gl-trade-route-next': 4900,
            'gl-trade-probe-trained': 0, 'map-type': CONSTANTS['RIVERS'],
            'gl-trade-land-producer-total': 1,
            'gl-trade-water-producer-total': 1,
            'gl-trade-land-growth-limit': 5,
            'gl-trade-water-growth-limit': 5,
            'gl-trade-land-verified': int(land),
            'gl-trade-water-verified': int(not land),
            'gl-trade-action-verified': 1,
        })
        g.counts = {'market': 1, 'dock': 1, 'trade-cog': 1, 'trade-cart': 1}
        return g

    @staticmethod
    def rule(land=False):
        check = 'ACTION' if land else 'WATER'
        start = 'LAND' if land else 'WATER'
        rows = [r for r in rule_blocks(source('rawai-economy.per'))
                if f'(goal gl-trade-route-state TRADE-ROUTE-{start}-PROOF-START)' in r[3]
                and f'(set-goal gl-trade-route-state TRADE-ROUTE-{check}-PROOF-CHECK)' in r[4]]
        assert len(rows) == 1
        return rows[0]

    def test_changed_producer_count_cannot_renew_stale_proof(self):
        for land, producer, goal in (
                (False, 'dock', 'gl-trade-water-producer-total'),
                (True, 'market', 'gl-trade-land-producer-total')):
            g = self.gate(land)
            self.assertTrue(g.accepts(self.rule(land)))
            for count in (0, 2, 3):
                g.counts[producer] = count
                self.assertFalse(g.accepts(self.rule(land)), (producer, count))
            g.counts[producer] = g.goals[goal] = 2
            self.assertTrue(g.accepts(self.rule(land)))

    def test_each_full_merchant_rule_uses_its_own_verified_epoch_and_growth_bound(self):
        for land, unit, producer, epoch, verified, growth in (
                (True, 'trade-cart', 'market', 'gl-trade-land-producer-total',
                 'gl-trade-land-verified', 'gl-trade-land-growth-limit'),
                (False, 'trade-cog', 'dock', 'gl-trade-water-producer-total',
                 'gl-trade-water-verified', 'gl-trade-water-growth-limit')):
            rows = [r for r in rule_blocks(source('rawai-economy.per'))
                    if f'(train {unit})' in r[4]
                    and f'(goal {verified} YES)' in r[3]
                    and '(goal gl-trade-action-verified YES)' in r[3]]
            self.assertEqual(len(rows), 1)
            facts = rows[0][3]
            for constraint in (f'building-type-count {producer} g:== {epoch}',
                               f'unit-type-count-total {unit} g:< {growth}',
                               f'unit-type-count-total {unit} g:< desired-number-'
                               + ('carts' if land else 'cogs')):
                self.assertIn('(' + constraint + ')', facts)
            if not land:
                self.assertNotIn('(goal gl-land-trade-route NO)', facts)

    def test_water_full_growth_remains_eligible_when_land_is_also_available(self):
        rows = [r for r in rule_blocks(source('rawai-economy.per'))
                if '(train trade-cog)' in r[4]
                and '(goal gl-trade-water-verified YES)' in r[3]
                and '(goal gl-trade-action-verified YES)' in r[3]]
        self.assertEqual(len(rows), 1)
        self.assertNotIn('(goal gl-land-trade-route NO)', rows[0][3])


if __name__ == '__main__': unittest.main()
