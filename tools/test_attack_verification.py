"""Execute the verifier's actual PER rules against bounded object fixtures.

Only documented fact/search semantics are modeled, not visibility/pathfinding.
"""
import math
import re
import unittest

from test_pre_backlog import source, expressions
from validate_naval_doctrine import rule_blocks


def obj(i, player, target=-1, action=600, point=(50, 50), hp=100):
    return dict(id=i, player=player, target=target, action=action, point=point,
                hp=hp, zone=9, cls='infantry-class')


class Verifier:
    def __init__(self, objects, enemies=(7,), victim=2, relief=False):
        self.objects = {o['id']: o for o in objects}
        self.enemies = list(enemies)
        self.constants = {}
        for name in ('rawai-constants.per', 'rawai-customconstants.per', 'rawai-unitconstants.per'):
            self.constants.update({k: int(v) for k, v in re.findall(r'\(defconst ([\w-]+) (-?\d+)\)', source(name))})
        self.g = {'gl-self-player-number': 2, 'gl-ally-help-player': victim,
                  'gl-ally-help-state': 1 if relief else 0, 'gl-home-defense-state': 0}
        self.sn, self.remote, self.target, self.point, self.include = {}, [], None, (0, 0), None
        self.disabled = set()

    def val(self, token):
        return int(token) if re.fullmatch(r'-?\d+', token) else self.constants.get(token, token)

    def operand(self, mode, token):
        return self.g.get(token, 0) if mode.startswith('g:') else self.val(token)

    def data(self, field, target=False):
        o = self.objects.get(self.target, {})
        if target:
            o = self.objects.get(o.get('target'), {})
        if field == 'object-data-distance':
            return math.dist(o.get('point', (9999, 9999)), self.point)
        key = {'object-data-id': 'id', 'object-data-player': 'player',
               'object-data-action': 'action', 'object-data-target-id': 'target',
               'object-data-hitpoints': 'hp', 'object-data-class': 'cls',
               'object-data-map-zone-id': 'zone'}[field]
        return self.val(str(o.get(key, -1)))

    def compare(self, lhs, mode, token):
        rhs = self.operand(mode, token)
        op = mode.split(':')[-1]
        if op == '==': return lhs == rhs
        if op == '!=': return lhs != rhs
        if op == '>=': return lhs >= rhs
        if op == '<': return lhs < rhs
        if op == '<=': return lhs <= rhs
        if op == '>': return lhs > rhs
        raise AssertionError(op)

    def fact(self, e):
        op, *a = e
        if op == 'true': return True
        if op == 'goal': return self.g.get(a[0], 0) == self.val(a[1])
        if op == 'not': return not self.fact(a[0])
        if op == 'up-compare-goal': return self.compare(self.g.get(a[0], 0), a[1], a[2])
        if op == 'up-set-target-object':
            index = self.operand(a[1], a[2])
            self.target = self.remote[index] if 0 <= index < len(self.remote) else None
            return self.target is not None
        if op in ('up-object-data', 'up-object-target-data'):
            return self.compare(self.data(a[0], op == 'up-object-target-data'), a[1], a[2])
        raise AssertionError(e)

    def action(self, e, pc):
        op, *a = e
        if op == 'disable-self': self.disabled.add(pc)
        elif op == 'up-get-fact': self.g[a[-1]] = 100
        elif op == 'set-goal': self.g[a[0]] = self.val(a[1])
        elif op == 'up-modify-goal':
            rhs = self.sn.get(a[2], 0) if a[1] == 's:=' else self.operand(a[1], a[2])
            self.g[a[0]] = self.g.get(a[0], 0) + rhs if a[1].endswith('+') else rhs
        elif op == 'up-modify-sn': self.sn[a[0]] = self.g.get(a[2], 0)
        elif op == 'up-find-player': self.g[a[-1]] = self.enemies[0] if self.enemies else -1
        elif op == 'up-find-next-player':
            old = self.g[a[-1]]
            self.g[a[-1]] = self.enemies[(self.enemies.index(old)+1) % len(self.enemies)] if self.enemies else -1
        elif op == 'up-full-reset-search': self.remote, self.target, self.include = [], None, None
        elif op == 'up-filter-include': self.include = self.val(a[1])
        elif op == 'up-find-remote':
            self.remote = [i for i, o in self.objects.items()
                           if o['player'] == self.sn.get('sn-focus-player-number')
                           and (self.include is None or o['action'] == self.include)][:self.val(a[-1])]
        elif op == 'up-remove-objects':
            kept = []
            for i in self.remote:
                self.target = i
                if not self.compare(self.data(a[1]), a[2], a[3]): kept.append(i)
            self.remote = kept
        elif op == 'up-get-object-data': self.g[a[1]] = self.data(a[0])
        elif op == 'up-get-point':
            self.g[a[1]], self.g[a[1][:-1]+'y'] = self.objects[self.target]['point']
        elif op == 'up-copy-point':
            self.g[a[0]], self.g[a[0][:-1]+'y'] = self.g[a[1]], self.g[a[1][:-1]+'y']
        elif op == 'up-set-target-point': self.point = self.g[a[0]], self.g[a[0][:-1]+'y']
        elif op == 'up-add-object-by-id':
            i = self.operand(a[1], a[2])
            if i in self.objects: self.remote.append(i)
        elif op == 'up-jump-rule': return int(a[0])
        else: raise AssertionError(e)
        return 0

    def run(self):
        rows = list(rule_blocks(source('rawai-attack-verification.per')))
        for sweep in range(20):
            pc, steps = 0, 0
            while pc < len(rows):
                steps += 1
                assert steps < 800, 'unbounded candidate loop'
                jump = 0
                if pc not in self.disabled and all(self.fact(e) for e in expressions(rows[pc][3])):
                    for e in expressions(rows[pc][4]): jump += self.action(e, pc)
                pc += 1 + jump
            if self.g['gl-verify-state'] == 0:
                return self.g
        raise AssertionError('scan did not terminate')


class AttackIdentityTests(unittest.TestCase):
    def test_yellow_near_green_is_not_a_green_attack(self):
        g = Verifier([obj(10, 3), obj(20, 2), obj(100, 7, 10)]).run()
        self.assertEqual(g['gl-self-attack-verified'], 0)

    def test_friendly_damage_and_unrelated_enemy_do_not_verify(self):
        g = Verifier([obj(10, 3), obj(20, 2), obj(90, 3, 20), obj(100, 7, 10)]).run()
        self.assertEqual(g['gl-self-attack-verified'], 0)

    def test_real_green_asset_uses_exact_location(self):
        g = Verifier([obj(20, 2, point=(70, 80)), obj(100, 7, 20, point=(72, 80))]).run()
        self.assertEqual((g['gl-t12-help-asset'], g['gl-t12-help-anchor-x'], g['gl-t12-help-anchor-y']), (20, 70, 80))
        self.assertEqual(g['gl-self-attack-verified'], 1)

    def test_first_enemy_invalid_second_valid(self):
        g = Verifier([obj(10, 3), obj(20, 2), obj(90, 6, 10), obj(100, 7, 20)], enemies=(6, 7)).run()
        self.assertEqual((g['gl-self-attack-verified'], g['gl-verify-enemy']), (1, 7))

    def test_relocated_colony_relief_ignores_original_tc(self):
        g = Verifier([obj(20, 3, point=(220, 190)), obj(100, 7, 20, point=(221, 190))], victim=3, relief=True).run()
        self.assertEqual((g['gl-ally-help-state'], g['gl-ally-help-target-x'], g['gl-ally-help-target-y']), (3, 220, 190))

    def test_no_victim_owned_target_no_claim(self):
        g = Verifier([obj(20, 2), obj(100, 7, 999)]).run()
        self.assertEqual(g['gl-self-attack-verified'], 0)

    def test_invalid_first_asset_does_not_hide_next_asset(self):
        g = Verifier([obj(10, 2, hp=0), obj(20, 2), obj(90, 7, 10), obj(100, 7, 20)]).run()
        self.assertEqual((g['gl-self-attack-verified'], g['gl-verify-asset']), (1, 20))

    def test_warning_requires_verified_pulse_not_proximity(self):
        for row in rule_blocks(source('rawai-diplomacy.per')):
            if '(chat-to-allies "48 ' in row[4]:
                self.assertIn('(goal gl-self-attack-verified YES)', row[3])
        self.assertIn('gl-verify-players-seen c:< 8', source('rawai-attack-verification.per'))


if __name__ == '__main__':
    unittest.main()
