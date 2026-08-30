"""Policy boundary fixtures tied to the actual integrated PER rules."""
import re
import unittest
from test_attack_verification import Verifier
from test_pre_backlog import source, expressions
from validate_naval_doctrine import rule_blocks


class Policy(Verifier):
    def val(self, token):
        return {'imperial-age': 3, 'middle-antiquity-age': 2, 'early-antiquity-age': 1}.get(token, super().val(token))

    def __init__(self):
        super().__init__([])
        self.stock = dict(food=0, wood=0, gold=0, stone=0)
        self.age, self.taunts, self.market = self.val('imperial-age'), set(), True

    def fact(self, e):
        op, *a = e
        if op.endswith('-amount'): return self.compare(self.stock[op[:-7]], a[0], a[1])
        if op == 'current-age': return self.compare(self.age, *a)
        if op in ('players-building-type-count', 'building-type-count'): return self.market
        if op == 'taunt-detected': return (self.val(a[0]), self.val(a[1])) in self.taunts
        if op == 'stance-toward': return True
        return super().fact(e)


class AidTests(unittest.TestCase):
    def test_actual_request_tiers_need_stock_shortage_and_both_deadlines(self):
        rows = [r for r in rule_blocks(source('rawai-trade.per')) if 'please send' in r[4]]
        self.assertEqual(len(rows), 12)
        for resource in ('food', 'wood', 'gold', 'stone'):
            for bank, amount in ((0, 100), (499, 100), (500, 500), (999, 500), (1000, 1000), (80000, 1000)):
                for stock in (0, 99, 100, 499):
                    p = Policy()
                    p.stock = dict.fromkeys(p.stock, 1000)
                    p.stock[resource] = stock
                    p.g['gl-request-'+resource+'-bank'] = bank
                    eligible = [r for r in rows if all(p.fact(e) for e in expressions(r[3]))]
                    self.assertEqual(len(eligible), int(stock < 100))
                    if eligible: self.assertIn('please send '+str(amount)+' '+resource, eligible[0][4])
            for deadline in ('gl-request-'+resource+'-next', 'gl-resource-request-next'):
                p = Policy()
                p.g[deadline] = 120
                chosen = [r for r in rows if '('+resource+'-amount' in r[3]]
                self.assertFalse(any(all(p.fact(e) for e in expressions(r[3])) for r in chosen))

    def test_all_donors_preserve_reserves_and_reject_self(self):
        rows = [r for r in rule_blocks(source('rawai-trade.per')) if '(tribute-to-player' in r[4]]
        self.assertEqual(len(rows), 120)
        for row in rows:
            player, resource, amount = re.search(r'tribute-to-player (\d) (\w+) (\d+)', row[4]).groups()
            token = re.search(r'taunt-detected \d ([\w-]+)', row[3])[1]
            p = Policy()
            if '(current-age < imperial-age)' in row[3]: p.age -= 1
            reserve = {'food': 1000, 'wood': 600, 'stone': 600, 'gold': 500 if p.age == p.val('imperial-age') else 800}[resource]
            p.taunts.add((int(player), p.val(token)))
            p.g['gl-self-player-number'] = 9
            for delta, expected in ((-1, False), (0, True)):
                p.stock[resource] = reserve + int(amount) + delta
                self.assertEqual(all(p.fact(e) for e in expressions(row[3])), expected)
            p.g['gl-self-player-number'] = int(player)
            self.assertFalse(all(p.fact(e) for e in expressions(row[3])))

    def test_all_unaffordable_requests_consumed_without_delayed_gift(self):
        rows = list(rule_blocks(source('rawai-trade.per')))
        donors = [r for r in rows if '(tribute-to-player' in r[4]]
        drains = [r for r in rows if '(taunt-detected' in r[3] and '(tribute-to-player' not in r[4]]
        self.assertEqual(len(drains), 96)
        for row in donors:
            pair = re.search(r'\(taunt-detected ([^)]*)\)', row[3])[1]
            drain = next(r for r in drains if '(taunt-detected '+pair+')' in r[3])
            self.assertGreater(drain[0], max(r[0] for r in donors))
            self.assertIn('(acknowledge-taunt '+pair+')', drain[4])

    def test_lifetime_banks_are_engine_totals_not_current_stock(self):
        text = source('rawai-trade.per')
        for resource in ('food', 'wood', 'gold', 'stone'):
            self.assertIn('resource-amount amount-'+resource+'-total gl-request-'+resource+'-bank', text)
            self.assertIn('gl-request-'+resource+'-next c:+ 120', text)
        self.assertIn('gl-resource-request-next c:+ 10', text)


if __name__ == '__main__': unittest.main()
