"""Execute Age 2 allocations and camp admission; not engine placement proof."""
import unittest

from test_pre_backlog import expressions, source
from test_t13_gate_recovery import CMP, CONSTANTS, Gate
from validate_naval_doctrine import rule_blocks


class EarlyGold(Gate):
    def __init__(self, market=0, smith=0, food=800, phase=3):
        super().__init__(**{
            'current-phase': phase, 'current-age': 1,
            'gl-owner-worker-hold': 0, 'resources-depleted': 0,
            'age-up-started': CONSTANTS['EARLY-ANTIQUITY'],
            'age-up-finished': CONSTANTS['EARLY-ANTIQUITY'],
            'desired-number-miningcamps': 1, 'gl-home-zone': 3,
            'gl-island-migration-state': CONSTANTS['MIGRATION-IDLE'],
            'gl-miningcamp-placement-state': CONSTANTS['PLACEMENT-IDLE'],
            'gl-miningcamp-next-resource': 'gold',  # engine built-in, symbolic here
        })
        self.counts = {'market': market, 'blacksmith': smith, 'lumber-camp': 1}
        self.food = food
        self.sn = dict(zip(('food', 'wood', 'gold', 'stone'), (20, 80, 0, 0)))
        self.disabled = set()
        self.rules = [r for r in rule_blocks(source('rawai-economy.per'))
                      if '(goal current-phase 3)' in r[3]
                      and 'sn-gold-gatherer-percentage' in r[4]]

    def fact(self, e):
        op, *a = e
        if op == 'food-amount': return CMP[a[0]](self.food, self.value(a[1]))
        if op == 'strategic-number':
            return CMP[a[1]](self.sn[a[0].split('-')[1]], self.value(a[2]))
        if op == 'up-timer-status': return True  # due placement timer fixture
        return super().fact(e)

    def sweep(self):
        fired = 0
        for n, row in enumerate(self.rules):
            if n in self.disabled or not self.accepts(row): continue
            fired += 1
            for op, *a in expressions(row[4]):
                if op == 'up-modify-sn':
                    self.sn[a[0].split('-')[1]] = self.value(a[2])
                elif op == 'up-modify-goal': self.goals[a[0]] = self.value(a[2])
                elif op == 'disable-self': self.disabled.add(n)
                elif op != 'chat-local-to-self':
                    raise AssertionError('unmodeled action: ' + op)
        return fired

    def camp_allowed(self):
        row = next(r for r in rule_blocks(source('rawai-homebase.per'))
                   if '(building-type-count-total mining-camp == 0)' in r[3]
                   and '(up-find-remote c: gold-mine-class c: 40)' in r[4])
        return self.accepts(row)


class EarlyGoldBootstrapTests(unittest.TestCase):
    def test_missing_either_or_both_prerequisites_keeps_gold_and_admits_camp(self):
        for market, smith in ((0, 0), (1, 0), (0, 1)):
            for food in (100, 700, 800, 900, 1200):
                with self.subTest(market=market, smith=smith, food=food):
                    m = EarlyGold(market, smith, food)
                    self.assertEqual(m.sweep(), 1)
                    self.assertEqual(m.sn, dict(food=20, wood=70, gold=10, stone=0))
                    self.assertTrue(m.camp_allowed())

    def test_second_prerequisite_in_food_deadband_cannot_leave_zero_gold(self):
        for food in (700, 800, 900):
            m = EarlyGold(1, 1, food)
            self.assertEqual(m.sweep(), 1)
            self.assertEqual(m.sn, dict(food=80, wood=10, gold=10, stone=0))
            self.assertTrue(m.camp_allowed())

    def test_existing_food_gold_hysteresis_survives_without_allocation_churn(self):
        m = EarlyGold(1, 1, 1000)
        self.assertEqual(m.sweep(), 1)
        self.assertEqual(m.sn, dict(food=40, wood=20, gold=40, stone=0))
        m.food = 800
        for _ in range(10):
            self.assertEqual(m.sweep(), 0)
            self.assertEqual(m.sn['gold'], 40)
        m.food = 600
        self.assertEqual(m.sweep(), 1)
        self.assertEqual(m.sn, dict(food=80, wood=10, gold=10, stone=0))
        m.food = 800
        self.assertEqual(m.sweep(), 0)
        self.assertEqual(sum(m.sn.values()), 100)

    def test_building_loss_returns_to_gold_preserving_wood_priority(self):
        m = EarlyGold(1, 1, 1000); m.sweep()
        m.counts['market'] = 0
        self.assertEqual(m.sweep(), 1)
        self.assertEqual(m.sn, dict(food=20, wood=70, gold=10, stone=0))

    def test_worker_hold_depletion_and_other_phases_are_not_overridden(self):
        for change in ({'gl-owner-worker-hold': 1}, {'resources-depleted': 1},
                       {'current-phase': 1}, {'current-phase': 2}, {'current-phase': 5}):
            m = EarlyGold(); m.goals.update(change)
            before = dict(m.sn)
            self.assertEqual(m.sweep(), 0)
            self.assertEqual(m.sn, before)

    def test_bootstrap_still_respects_age_resources_pending_and_migration(self):
        for reason in ('age', 'wood', 'existing', 'pending', 'placement', 'migration', 'zone'):
            m = EarlyGold(); m.sweep()
            if reason == 'age': m.goals['current-age'] = 0
            elif reason == 'wood': m.affordable = False
            elif reason == 'existing': m.counts['mining-camp'] = 1
            elif reason == 'pending': m.pending.add('mining-camp')
            elif reason == 'placement': m.placement.add('mining-camp')
            elif reason == 'migration': m.goals['gl-island-migration-state'] = -999
            elif reason == 'zone': m.goals['gl-home-zone'] = -1
            self.assertFalse(m.camp_allowed(), reason)


if __name__ == '__main__':
    unittest.main()
