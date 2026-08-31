"""Execute generated three-slot PER against object fixtures, not engine pathfinding."""
import re
import unittest
from copy import deepcopy

from generate_assault_missions import FIELDS, GROUPS, outputs
from test_assault_screen_fallback import ScreenFallback
from test_pre_backlog import source, expressions
from validate_naval_doctrine import rule_blocks


class Missions(ScreenFallback):
    def __init__(self):
        super().__init__()
        self.constants.update({k: int(v) for k, v in re.findall(
            r'\(defconst ([\w-]+) (-?\d+)\)', source('rawai-assault-mission-defs.per'))})
        self.objects, self.groups, self.commands = {}, {}, []
        self.g.update({f'gl-am{i}-{f}': 0 for i in range(1, 4) for f in FIELDS})
        self.rules = list(rule_blocks(source('rawai-assault-missions.per')))
        self.disabled = set()
        self.players = {p: dict(active=True, enemy=p >= 5, buildings=10) for p in range(1, 9)}
        self.minradius = -1

    def data(self, field, target=False):
        obj = self.objects.get(self.target, {})
        keys = {'object-data-attacker-id': 'attacker', 'object-data-idling': 'idle',
                'object-data-type': 'type', 'object-data-order': 'order'}
        if field in keys: return self.val(str(obj.get(keys[field], -1)))
        if field == 'object-data-index': return self.local.index(self.target)
        return super().data(field, target)

    def fact(self, e):
        if e[0] in ('player-in-game', 'stance-toward') and e[1].isdigit():
            p = self.players[int(e[1])]
            return p['active'] if e[0] == 'player-in-game' else p['enemy']
        if e[0] == 'up-group-size':
            return self.compare(len(self.groups.get(self.val(e[2]), [])), e[3], e[4])
        return super().fact(e)

    def action(self, e, pc=0):
        op, *a = e
        if op == 'up-set-group':
            items = [i for i in self.groups.get(self.val(a[2]), []) if i in self.objects]
            if a[0] == 'search-local': self.local = items
            else: self.remote = items
        elif op == 'up-modify-group-flag':
            group = self.val(a[2])
            for i in self.groups.get(group, []):
                if i in self.objects: self.objects[i]['flag'] = group if a[0] == '1' else -2
        elif op == 'up-set-timer': pass  # preparation timer is outside this independent voyage module
        elif op == 'up-target-point':
            point = (self.g.get(a[0], 0), self.g.get(a[0][:-1]+'y', 0))
            self.commands.append((tuple(self.local), a[1], point))
        elif op == 'up-target-objects':
            if self.local and self.remote:
                self.commands.append((tuple(self.local), a[1], ('object', self.remote[0])))
        elif op == 'up-modify-sn' and a[1] == 'c:=':
            self.sn[a[0]] = self.val(a[2])
        elif op == 'up-remove-objects' and a[-1] == 'focus-player':
            return super().action([*e[:-1], str(self.sn['sn-focus-player-number'])], pc)
        elif op == 'up-clean-search':
            def key(i):
                self.target = i
                return self.data(a[1])
            items = self.local if a[0] == 'search-local' else self.remote
            items.sort(key=key, reverse=a[2] == 'search-order-desc')
        elif op == 'up-find-local':
            import math
            found = [i for i, o in self.objects.items() if o['player'] == 2
                     and a[1] in (o.get('cls'), o.get('type'))
                     and self.minradius <= math.dist(o['point'], self.point) <= self.radius]
            self.local += [i for i in found[:self.val(a[3])] if i not in self.local]
        elif op == 'up-full-reset-search':
            self.minradius = -1
            return super().action(e, pc)
        elif op == 'up-filter-distance':
            self.minradius, self.radius = self.val(a[1]), self.val(a[3])
        else: return super().action(e, pc)
        return 0

    def sweep(self, advance=0):
        self.now += advance
        self.g['gl-game-time'] = self.now
        for n, row in enumerate(self.rules):
            if n in self.disabled: continue
            if all(self.fact(e) for e in expressions(row[3])):
                for e in expressions(row[4]): self.action(e, n)

    def prepare(self, hull, enemy=6, cargo=9):
        self.g.update({'gl-transport-route-state': self.val('TRANSPORT-ROUTE-DEPARTURE-START'),
            'gl-assault-preflight-live': 1, 'gl-transport-route-id': hull,
            'gl-assault-manifest-hull': hull, 'gl-assault-manifest-player': enemy,
            'gl-assault-manifest-count': cargo, 'gl-transport-screen-id': -1,
            'gl-assault-fallback-deadline': 0, 'gl-transport-route-target-zone': 3,
            'gl-transport-route-origin-x': hull, 'gl-transport-route-origin-y': 10,
            'gl-transport-route-waypoint-x': 150, 'gl-transport-route-waypoint-y': 100,
            'gl-transport-route-landing-x': 155, 'gl-transport-route-landing-y': 100,
            'gl-transport-route-target-x': 165, 'gl-transport-route-target-y': 110})
        self.objects[hull] = dict(id=hull, player=2, hp=100, cargo=cargo, garrisoned=0,
            flag=self.val('attack-transport-group'), point=(hull, 10), zone=8,
            type='transport-ship', cls='transport-class', idle=0, attacker=-1)
        self.groups[self.val('attack-transport-group')] = [hull]
        passengers = list(range(hull*100, hull*100+cargo))
        for p in passengers:
            self.objects[p] = dict(id=p, player=2, hp=100, cargo=0, garrisoned=1,
                flag=self.val('attack-boarding-group'), point=(hull, 10), zone=8,
                cls='infantry-class', idle=0)
        self.groups[self.val('attack-boarding-group')] = passengers


class AssaultMissionTests(unittest.TestCase):
    def three(self):
        m = Missions()
        for hull, enemy in ((10, 6), (20, 7), (30, 8)):
            m.prepare(hull, enemy)
            m.sweep()
        self.assertEqual([m.g[f'gl-am{i}-state'] for i in (1, 2, 3)], [1, 1, 1])
        return m

    def test_generated_files_match(self):
        for name, value in outputs().items(): self.assertEqual(source(name), value)

    def test_storage_and_point_pairs_do_not_alias(self):
        m = Missions()
        ids = [m.val(f'gl-am{i}-{key}') for i in range(1, 4) for key in FIELDS]
        self.assertEqual(len(ids), len(set(ids)))
        for i in range(1, 4):
            for key in ('origin-', 'waypoint-', 'landing-', 'target-', '', 'clear-'):
                self.assertEqual(m.val(f'gl-am{i}-{key}y'), m.val(f'gl-am{i}-{key}x')+1)
        self.assertEqual(len(set(GROUPS)), 3)
        self.assertTrue(all(0 <= g <= 19 for g in GROUPS))

    def test_three_concurrent_independent_manifests(self):
        m = self.three()
        for i, (hull, enemy) in enumerate(((10, 6), (20, 7), (30, 8)), 1):
            self.assertEqual(m.g[f'gl-am{i}-hull'], hull)
            self.assertEqual(m.g[f'gl-am{i}-enemy'], enemy)
            self.assertEqual(len(m.groups[GROUPS[i-1]]), 10)
            self.assertTrue(all(m.objects[p]['flag'] == GROUPS[i-1] for p in m.groups[GROUPS[i-1]]))

    def test_global_target_and_routine_defense_do_not_recall(self):
        m = self.three()
        m.sn['sn-target-player-number'] = 5
        m.g.update({'gl-land-target-current-player': 5, 'gl-home-defense-state': 1})
        for _ in range(5):
            for hull in (10, 20, 30):
                x, y = m.objects[hull]['point']; m.objects[hull]['point'] = x+4, y+4
            m.sweep(8)
        self.assertEqual([m.g[f'gl-am{i}-state'] for i in (1, 2, 3)], [1, 1, 1])
        self.assertFalse(any(a == 'action-unload' for _, a, _ in m.commands))

    def test_building_count_zero_does_not_mean_enemy_defeated(self):
        m = self.three()
        m.players[6]['buildings'] = 0
        m.sweep(8)
        self.assertEqual(m.g['gl-am1-state'], 1)

    def test_enemy_exit_recalls_only_its_slot(self):
        m = self.three()
        m.players[7]['active'] = False
        m.sweep(8)
        self.assertEqual([m.g[f'gl-am{i}-state'] for i in (1, 2, 3)], [1, 3, 1])
        self.assertIn(((20,), 'action-unload', (20, 10)), m.commands)

    def test_friendly_fire_is_not_a_preemption_reason(self):
        m = self.three()
        m.objects[90] = dict(id=90, player=3, hp=100, point=(10, 11))
        m.objects[10].update(hp=70, attacker=90)
        m.sweep(8)
        self.assertEqual(m.g['gl-am1-state'], 1)
        m.objects[91] = dict(id=91, player=8, hp=100, point=(10, 11))
        m.objects[10].update(hp=60, attacker=91)
        m.sweep(8)
        self.assertEqual(m.g['gl-am1-state'], 3)
        self.assertEqual(m.g['gl-am1-reason'], 2)

    def test_moving_hulls_do_not_receive_repeated_orders(self):
        m = self.three()
        self.assertEqual(len(m.commands), 3)
        for _ in range(7):
            for h in (10, 20, 30):
                x, y = m.objects[h]['point']; m.objects[h]['point'] = x+2, y+2
            m.sweep(8)
        self.assertEqual(len(m.commands), 3)

    def test_no_progress_recovers_then_quarantines_without_command_loop(self):
        m = self.three()
        m.sweep(96)
        self.assertEqual(m.g['gl-am1-state'], 3)
        m.sweep(184)
        self.assertEqual(m.g['gl-am1-state'], 4)
        commands = len(m.commands)
        m.sweep(300)
        self.assertEqual(len(m.commands), commands)
        self.assertEqual(m.objects[10]['flag'], GROUPS[0])

    def test_same_island_landing_and_independent_release(self):
        m = self.three()
        m.objects[10]['point'] = (150, 100)
        m.sweep(8)
        self.assertEqual(m.g['gl-am1-state'], 2)
        m.objects[10].update(point=(155, 100), cargo=0)
        for p in range(1000, 1009): m.objects[p].update(garrisoned=0, zone=3)
        m.sweep(8)
        self.assertEqual(m.g['gl-am1-state'], 6)
        self.assertEqual([m.g[f'gl-am{i}-state'] for i in (2, 3)], [1, 1])
        self.assertTrue(any(a == 'action-default' and point == (165, 110) for _, a, point in m.commands))
        self.assertTrue(all(m.objects[p]['flag'] == GROUPS[0] for p in range(1000, 1009)))

    def test_wrong_island_never_unloads_there(self):
        m = self.three(); m.zone = 99
        m.objects[10]['point'] = (150, 100)
        m.sweep(8)
        self.assertEqual(m.g['gl-am1-state'], 3)
        self.assertNotIn(((10,), 'action-unload', (155, 100)), m.commands)

    def test_new_landing_leg_measures_its_own_progress_in_every_slot(self):
        # T19 Red44797: waypoint reached82:38, still-loaded recall83:42.
        # Arrival near the waypoint must not become the beach's best distance.
        # Exercise a longer second leg; this fixture is NOT a pathfinding model.
        for slot, hull in ((1, 10), (2, 20), (3, 30)):
            with self.subTest(slot=slot):
                m = self.three()
                m.g[f'gl-am{slot}-landing-x'] = 230
                m.objects[hull]['point'] = (150, 100)
                voyage_deadline = m.g[f'gl-am{slot}-travel-until']
                m.sweep(8)
                self.assertEqual(m.g[f'gl-am{slot}-state'], 2)
                command_count = len(m.commands)
                for step in range(1, 13):
                    m.objects[hull]['point'] = (150 + 4*step, 100)
                    m.sweep(8)
                    self.assertEqual(m.g[f'gl-am{slot}-state'], 2)
                self.assertEqual(m.g[f'gl-am{slot}-best'], 30)
                self.assertEqual(m.g[f'gl-am{slot}-travel-until'], voyage_deadline)
                # No repeated move/unload command to this moving hull.
                self.assertFalse(any(hull in ids for ids, _, _ in m.commands[command_count:]))

    def test_landing_leg_still_recovers_when_progress_really_stops(self):
        m = self.three()
        m.g['gl-am1-landing-x'] = 230
        m.objects[10]['point'] = (150, 100)
        m.sweep(8)
        m.sweep(8)  # first sample establishes the new leg's baseline
        m.sweep(96)
        self.assertEqual(m.g['gl-am1-state'], 3)
        self.assertEqual(m.g['gl-am1-reason'], 4)

    def test_completed_landing_wins_over_simultaneous_expired_watchdogs(self):
        # T19 Red44797 emits event4 then9 at93:58: cargo was already empty,
        # but timeout ran before delivery and suppressed the passengers' order.
        for expired in ('progress-until', 'travel-until'):
            with self.subTest(expired=expired):
                m = self.three()
                m.objects[10]['point'] = (150, 100)
                m.sweep(8)
                m.objects[10]['point'] = (155, 100)
                m.sweep(8)  # last sample was close to the beach but still loaded
                m.g[f'gl-am1-{expired}'] = m.now + 8
                m.objects[10].update(point=(155, 100), cargo=0)
                for p in range(1000, 1009):
                    m.objects[p].update(garrisoned=0, zone=3)
                m.sweep(8)
                self.assertEqual(m.g['gl-am1-state'], 6)
                self.assertEqual(m.g['gl-am1-reason'], 8)
                self.assertTrue(any(set(ids)==set(range(1000,1009)) and point==(165,110)
                                    for ids, _, point in m.commands))
                self.assertFalse(any(ids==(10,) and a=='action-unload' and point==(10,10)
                                     for ids,a,point in m.commands))

    def test_hull_conversion_does_not_clear_foreign_flags(self):
        m = self.three()
        m.objects[10]['player'] = 8
        m.sweep(8)
        self.assertEqual(m.g['gl-am1-state'], 0)
        self.assertEqual(m.objects[10]['flag'], GROUPS[0])

    def test_busy_admission_and_native_takeover_guard(self):
        m = self.three()
        rules = list(rule_blocks(source('rawai-assault-admission.per')))
        for row in rules[3:]: m.rule(row)
        self.assertEqual(m.g['gl-assault-admission-open'], 0)
        s = source('rawai-military.per')
        intake = next(r for r in rule_blocks(s) if 'gl-assault-admission-open YES' in r[3]
                      and 'up-find-remote c: transport-ship' in r[4])
        for term in ('orderid-transport', 'orderid-unload', 'object-data-group-flag >= 0'):
            self.assertIn(term, intake[4])

    def test_scratch_and_severe_defense_never_write_voyage_groups(self):
        general = source('rawai-general.per')
        self.assertNotRegex(general, r'\(up-(?:set-group|create-group|reset-group|modify-group-flag)[^\n]*c: 0\)')
        self.assertIn('(not (goal gl-transport-route-state TRANSPORT-ROUTE-IDLE))', general)
        severe = source('rawai-severe-defense.per')
        self.assertNotIn('assault-mission-', severe)
        for n in range(1, 4):
            self.assertIn(f'assault-mission-{n}-group', source('rawai-native-attack-ownership.per'))

    def test_only_free_idle_blocker_yields_to_stalled_mission(self):
        m = self.three()
        m.objects[10]['idle'] = 1
        for h, point, flag, idle in ((40, (12, 10), -2, 1), (41, (13, 10), 5, 1),
                                     (42, (14, 10), -2, 0), (80, (70, 10), -2, 0)):
            m.objects[h] = dict(id=h, player=2, hp=100, cargo=0, flag=flag, idle=idle,
                                 point=point, zone=8, type='transport-ship', cls='transport-class', under_attack=0)
        for _ in range(4): m.sweep(8)
        moved = [(ids, p) for ids, a, p in m.commands if a == 'action-move' and any(h in ids for h in (40, 41, 42, 80))]
        self.assertEqual(moved, [((40,), (70, 10))])
        self.assertEqual(m.g['gl-am1-waypoint-x'], 150)
        # Physically moving the blocker away removes it from subsequent local
        # clearance attempts; the original hull continues the same destination.
        m.objects[40]['point'] = (70, 10)
        m.objects[10].update(point=(60, 40), idle=0)
        for _ in range(3): m.sweep(8)
        self.assertEqual(m.g['gl-am1-state'], 1)
        self.assertEqual(m.g['gl-am1-clear-count'], 1)

    def test_landing_stages_only_its_screen_and_paired_escorts(self):
        m = self.three()
        m.g['gl-am1-screen'] = 99
        m.objects[99] = dict(id=99, player=2, hp=100, cargo=0, flag=0, point=(150, 100),
                             zone=8, cls='warship-class', target=10)
        m.groups[0].append(99)
        for n, target in ((91, 10), (92, 20)):
            m.objects[n] = dict(id=n, player=2, hp=100, cargo=0, flag=9,
                                point=(150, 100), zone=8, cls='warship-class', target=target)
        m.groups[9] = [91, 92]
        m.objects[10]['point'] = (150, 100)
        m.sweep(8)
        self.assertTrue(any(91 in ids and a == 'action-move' for ids, a, _ in m.commands))
        self.assertTrue(any(99 in ids and a == 'action-move' for ids, a, _ in m.commands))
        self.assertFalse(any(92 in ids for ids, _, _ in m.commands))
        self.assertEqual(m.objects[92]['flag'], 9)


if __name__ == '__main__': unittest.main()
