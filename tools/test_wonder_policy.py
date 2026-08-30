"""Execute Wonder PER rules over deterministic loss/build fixtures, not the engine."""
import unittest
from test_release_backlog import Policy
from test_pre_backlog import source, expressions
from validate_naval_doctrine import rule_blocks


class Wonder(Policy):
    def __init__(self):
        super().__init__()
        self.victory, self.villagers = 'standard', 60
        self.own_wonder = self.ally_wonder = self.pending = 0
        self.loss = dict(enemy_build=0, enemy_unit=0, ally_build=0, ally_unit=0, self_build=0, self_unit=0)
        self.stock.update(wood=1400, gold=1500, stone=1400)
        self.requests, self.foundations = 0, True

    def fact(self, e):
        op, *a = e
        if op == 'or': return any(self.fact(x) for x in a)
        if op == 'victory-condition': return self.victory == a[0]
        if op == 'building-type-count': return self.compare(1, a[1], a[2])
        if op == 'building-type-count-total': return self.compare(self.own_wonder, a[1], a[2])
        if op == 'players-building-type-count': return self.compare(self.ally_wonder, a[2], a[3])
        if op == 'up-object-type-count-total': return self.compare(self.villagers, a[2], a[3])
        if op == 'up-pending-objects': return self.compare(self.pending, a[2], a[3])
        if op == 'up-pending-placement': return bool(self.pending)
        if op == 'up-can-build': return True
        return super().fact(e)

    def action(self, e, pc):
        op, *a = e
        if op in ('up-get-fact', 'up-get-fact-sum'):
            team = 'enemy' if a[0] == 'any-enemy' else 'ally' if a[0] == 'any-ally' else 'self'
            kind = 'build' if 'amount-razed-by-others' in a else 'unit'
            self.g[a[-1]] = self.loss[team+'_'+kind]
        elif op == 'up-modify-goal':
            rhs = self.operand(a[1], a[2])
            old = self.g.get(a[0], 0)
            self.g[a[0]] = {'+': old+rhs, '-': old-rhs, '*': old*rhs, '=': rhs}[a[1][-1]]
        elif op == 'up-build':
            self.requests += 1
            self.pending = 1
            if self.foundations: self.own_wonder = 1
        elif op == 'up-reset-placement': self.pending = 0
        elif op in ('chat-to-allies', 'chat-local-to-self', 'up-chat-data-to-self'): pass
        else: return super().action(e, pc)
        return 0

    def tick(self, time):
        self.g['gl-game-time'] = time
        for row in rule_blocks(source('rawai-wonder.per')):
            if row[0] not in self.disabled and all(self.fact(e) for e in expressions(row[3])):
                for e in expressions(row[4]): self.action(e, row[0])

    def quiet(self):
        for t in (3600, 3900, 4200, 4500): self.tick(t)


class WonderTests(unittest.TestCase):
    def test_three_windows_then_staggered_build_with_low_enemy_counts(self):
        w = Wonder()
        for t in (3600, 3900, 4200):
            w.tick(t)
            self.assertEqual(w.requests, 0)
        w.tick(4500)
        self.assertEqual(w.g['gl-wonder-stall-windows'], 3)
        w.tick(4559)
        self.assertEqual(w.requests, 0)
        w.tick(4560)
        self.assertEqual(w.requests, 1)

    def test_standard_late_imperial_only(self):
        for attr, value in (('victory', 'conquest'), ('age', 2)):
            w = Wonder()
            setattr(w, attr, value)
            w.quiet(); w.tick(5000)
            self.assertEqual(w.requests, 0)
        w = Wonder(); w.tick(3599)
        self.assertEqual(w.g['gl-wonder-baseline-valid'], 0)

    def test_losses_on_either_team_reset_even_if_replacements_mask_net_counts(self):
        for key, count in (('enemy_build', 3), ('ally_build', 3), ('self_build', 3),
                           ('enemy_unit', 5), ('ally_unit', 5), ('self_unit', 5)):
            w = Wonder(); w.tick(3600); w.tick(3900)
            w.loss[key] = count
            w.tick(4200)
            self.assertEqual(w.g['gl-wonder-stall-windows'], 0, key)

    def test_saving_continues_sampling_without_postponing_election(self):
        w = Wonder(); w.stock['wood'] = 0; w.quiet()
        election = w.g['gl-wonder-election-time']
        w.tick(4800)
        self.assertEqual(w.g['gl-wonder-election-time'], election)
        self.assertEqual(w.g['gl-wonder-sample-next'], 5100)
        w.loss['enemy_build'] = 3; w.tick(5100)
        self.assertEqual(w.g['gl-wonder-state'], w.val('WONDER-STATE-MONITOR'))

    def test_ally_wonder_worker_hold_defense_and_reserves_gate_build(self):
        for cause in ('ally', 'hold', 'defense', 'villagers', 'wood', 'gold', 'stone'):
            w = Wonder(); w.quiet()
            if cause == 'ally': w.ally_wonder = 1
            elif cause == 'hold': w.g['gl-owner-worker-hold'] = 1
            elif cause == 'defense': w.g['gl-home-defense-state'] = 1
            elif cause == 'villagers': w.villagers = 59
            else: w.stock[cause] -= 1
            w.tick(4560)
            self.assertEqual(w.requests, 0, cause)

    def test_three_failed_placements_then_cooldown_even_if_pending_flag_sticks(self):
        w = Wonder(); w.foundations = False; w.quiet()
        for t in range(4560, 5200): w.tick(t)
        self.assertEqual(w.requests, 3)
        self.assertEqual(w.g['gl-wonder-state'], w.val('WONDER-STATE-COOLDOWN'))
        self.assertEqual(w.pending, 0)

    def test_wonder_writes_no_protected_controller_or_strategic_number(self):
        for row in rule_blocks(source('rawai-wonder.per')):
            for e in expressions(row[4]):
                if e[0] in ('set-goal', 'up-modify-goal'):
                    self.assertTrue(e[1].startswith('gl-wonder-'))
                self.assertNotIn(e[0], ('attack-now', 'up-reset-attack-now', 'set-strategic-number',
                                       'up-modify-sn', 'up-reset-group', 'up-target-point'))


if __name__ == '__main__': unittest.main()
