"""Actual-PER postlanding ownership/retarget fixtures; not engine combat proof."""
import unittest

from test_assault_missions import Missions, GROUPS
from test_pre_backlog import expressions


class LandedAssaultTests(unittest.TestCase):
    def landed(self):
        m = Missions(); m.prepare(10); m.sweep()
        m.objects[10]['point'] = (150, 100); m.sweep(8)
        m.objects[10].update(point=(155, 100), cargo=0)
        for p in range(1000, 1009):
            m.objects[p].update(point=(155, 100), garrisoned=0, zone=3, idle=1)
        m.sweep(8)
        return m

    def target(self, m, i=99, player=6, zone=3, point=(165, 110)):
        m.objects[i] = dict(id=i, player=player, zone=zone, point=point, hp=100,
                            cls='building-class', type='house')

    def attacks(self, m):
        return [c for c in m.commands if c[2] and c[2][0] == 'object']

    def attack_rule(self, m, slot=1):
        token = '(up-target-objects 1 action-default -1 stance-aggressive)'
        rows = [row for row in m.rules
                if token in row[4] and f'(goal gl-am{slot}-sample 7)' in row[3]]
        self.assertEqual(len(rows), 1)
        return rows[0]

    def evaluate_rule(self, m, row):
        if all(m.fact(e) for e in expressions(row[3])):
            for action in expressions(row[4]):
                m.action(action)

    def test_hull_released_but_landed_manifest_keeps_combat_ownership(self):
        m = self.landed()
        self.assertEqual(m.g['gl-am1-state'], 6)
        self.assertEqual(m.objects[10]['flag'], -2)
        self.assertEqual(m.groups[GROUPS[0]], list(range(1000, 1009)))
        self.assertTrue(all(m.objects[p]['flag'] == GROUPS[0] for p in range(1000, 1009)))

    def test_target_destruction_retargets_despite_global_target_change(self):
        m = self.landed(); self.target(m); m.sweep(16)
        self.assertTrue(self.attacks(m))
        self.assertEqual(self.attacks(m)[-1][2], ('object', 99))
        del m.objects[99]; self.target(m, i=100)
        m.sn['sn-target-player-number'] = 7
        m.g['gl-land-transport-ready'] = 0
        m.sweep(16)
        self.assertEqual(self.attacks(m)[-1][2], ('object', 100))

    def test_one_object_attack_command_per_logical_combat_sample(self):
        m = self.landed(); self.target(m)
        attack_rule = self.attack_rule(m)
        before = len(self.attacks(m))

        # The fixture deliberately does not change object-data-action after a
        # command, modelling delayed engine visibility of actionid-attack.
        m.sweep(16)
        self.assertEqual(len(self.attacks(m)), before + 1)
        self.assertEqual(m.g['gl-am1-sample'], 10)
        self.assertNotEqual(m.objects[1000].get('action'), m.val('actionid-attack'))

        # Even direct repeated evaluation of the issuance rule cannot emit a
        # duplicate while this logical sample remains open in engine time.
        for _ in range(4):
            self.evaluate_rule(m, attack_rule)
        self.assertEqual(len(self.attacks(m)), before + 1)

        # The ordinary 16-second gate can open a later legitimate sample.
        m.sweep(16)
        self.assertEqual(len(self.attacks(m)), before + 2)

    def test_all_three_slots_have_post_issue_latch_and_failed_target_transition(self):
        m = Missions()
        command = '(up-target-objects 1 action-default -1 stance-aggressive)'
        for slot in (1, 2, 3):
            row = self.attack_rule(m, slot)
            self.assertEqual(row[4].count(command), 1)
            self.assertIn(f'(set-goal gl-am{slot}-sample 10)', row[4])
            failed = [candidate for candidate in m.rules
                      if f'(goal gl-am{slot}-sample 10)' in candidate[3]
                      and f'gl-am{slot}-combat-tries c:>= 3' in candidate[3]
                      and f'gl-am{slot}-combat-failed' in candidate[4]]
            self.assertEqual(len(failed), 1, slot)

    def test_stale_attacked_and_active_combat_members_obey_landed_ownership(self):
        m = self.landed(); self.target(m)
        m.objects[1000]['idle'] = 0
        m.objects[1001]['under_attack'] = 1
        for p, change in ((1002, {'player': 6}), (1003, {'flag': 18}),
                          (1004, {'zone': 4}), (1005, {'garrisoned': 1})):
            m.objects[p].update(change)
        m.objects[1006]['action'] = m.val('actionid-attack')
        m.objects[1010] = dict(m.objects[1007], id=1010, flag=-2)
        m.sweep(16)
        commanded = set(self.attacks(m)[-1][0])
        self.assertEqual(commanded, {1000, 1001, 1007, 1008})
        self.assertEqual(m.objects[1003]['flag'], 18)
        self.assertNotIn(1006, commanded)
        self.assertNotIn(1010, commanded)

    def test_hostile_military_unit_is_a_landed_combat_target(self):
        m = self.landed()
        m.objects[99] = dict(id=99, player=6, zone=3, point=(165, 110), hp=100,
                             cls='infantry-class', type='infantry')
        m.sweep(16)
        self.assertEqual(self.attacks(m)[-1][2], ('object', 99))

    def test_no_targets_probe_same_landmass_then_release_bounded(self):
        m = self.landed()
        initial = len(m.commands)
        for _ in range(12):
            m.sweep(16)
            self.assertEqual(m.g['gl-am1-state'], 6)
        probes = [c for c in m.commands[initial:] if c[1] == 'action-move']
        self.assertEqual(len(probes), 12)
        self.assertEqual(len({c[2] for c in probes}), 12)
        m.sweep(16)
        self.assertEqual(m.g['gl-am1-state'], 0)
        self.assertFalse(self.attacks(m))
        self.assertTrue(all(m.objects[p]['flag'] == -2 for p in range(1000, 1009)))

    def test_wrong_landmass_probe_is_skipped_without_releasing_ownership(self):
        m = self.landed(); initial = len(m.commands); m.zone = 4
        m.sweep(16)
        self.assertEqual(m.g['gl-am1-state'], 6)
        self.assertFalse(any(c[1] == 'action-move' for c in m.commands[initial:]))
        self.assertTrue(all(m.objects[p]['flag'] == GROUPS[0] for p in range(1000, 1009)))

    def test_total_combat_lease_remains_hard_bounded(self):
        m = self.landed(); self.target(m)
        for p in range(1000, 1009): m.objects[p]['idle'] = 0
        m.sweep(301)
        self.assertEqual(m.g['gl-am1-state'], 0)
        self.assertTrue(all(m.objects[p]['flag'] == -2 for p in range(1000, 1009)))

    def test_same_island_other_living_enemy_after_original_enemy_leaves(self):
        m = self.landed(); m.players[6]['active'] = False
        self.target(m, player=7); m.sweep(16)
        self.assertEqual(self.attacks(m)[-1][2], ('object', 99))

    def test_friendly_wrong_island_and_failed_target_are_not_selected(self):
        m = self.landed(); self.target(m, player=3); self.target(m, i=100, zone=4)
        m.sweep(16); self.assertFalse(self.attacks(m))
        self.target(m, i=101)
        for _ in range(3): m.sweep(16)  # three refused/idle orders, not progressing attacks
        self.target(m, i=102, point=(175, 110))
        m.sweep(16)
        self.assertEqual(self.attacks(m)[-1][2], ('object', 102))


if __name__ == '__main__': unittest.main()
