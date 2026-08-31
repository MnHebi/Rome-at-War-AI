"""Execute screening fallback PER rules; not path, damage or fog-of-war simulation."""
import math
import re
import unittest
from pathlib import Path

from test_attack_verification import Verifier
from test_pre_backlog import source, expressions
from validate_naval_doctrine import rule_blocks


class ScreenFallback(Verifier):
    def __init__(self, cargo=10, capacity=20, enemies=(6, 7), accepted=None):
        super().__init__([], enemies=enemies)
        definitions = source('rawai-assault-mission-defs.per')
        self.constants.update({k: int(v) for k, v in re.findall(
            r'\(defconst ([\w-]+) (-?\d+)\)', definitions)})
        self.string_constants = dict(re.findall(r'\(defconst ([\w-]+) ("[^"\n]*")\)', definitions))
        self.constants['my-player-number'] = 2
        self.objects = {10: dict(id=10, player=2, hp=100, under_attack=0, cargo=cargo,
                                flag=self.val('attack-transport-group'), point=(10, 10))}
        self.local, self.remote, self.logs, self.commands = [], [], [], []
        self.radius, self.zone, self.now = 99999, 3, 1000
        self.groups = {}
        self.players = {p: dict(active=True, enemy=True, buildings=10) for p in enemies}
        self.g.update({'gl-transport-route-state': self.val('TRANSPORT-ROUTE-UNSCREENED-START'),
            'gl-transport-route-id': 10, 'gl-transport-capacity': capacity,
            'gl-transport-route-load-target': cargo, 'gl-assault-fallback-reason': 3,
            'gl-assault-manifest-hull': 10, 'gl-assault-manifest-count': cargo if accepted is None else accepted,
            'gl-assault-manifest-player': 6,
            'gl-assault-fallback-deadline': -1, 'gl-transport-load-clock': self.now,
            'gl-transport-screen-id': -1, 'gl-transport-route-focus': 2,
            'gl-transport-route-waypoint-x': 50, 'gl-transport-route-waypoint-y': 50,
            'gl-transport-route-landing-x': 90, 'gl-transport-route-landing-y': 90,
            'gl-transport-route-target-zone': 3})
        self.admission_rules = list(rule_blocks(source('rawai-assault-admission.per')))
        self.admission_disabled = set()
        self.rules = list(rule_blocks(source('rawai-assault-screen-fallback.per').replace(
            '(load "rawai-assault-cancel-details")', source('rawai-assault-cancel-details.per')).replace(
            '(load "rawai-assault-enemy-scan")', source('rawai-assault-enemy-scan.per'))))

    def data(self, field, target=False):
        if field == 'object-data-order':
            return self.objects.get(self.target, {}).get('order', 0)
        if field in ('object-data-under-attack', 'object-data-garrison-count', 'object-data-group-flag',
                     'object-data-garrisoned'):
            return self.objects.get(self.target, {}).get({
                'object-data-under-attack': 'under_attack', 'object-data-garrison-count': 'cargo',
                'object-data-group-flag': 'flag', 'object-data-garrisoned': 'garrisoned'}[field], -1)
        return super().data(field, target)

    def fact(self, e):
        if e[0] in ('or', 'and'):
            return (any if e[0] == 'or' else all)(self.fact(x) for x in e[1:])
        if e[0] == 'up-set-target-object':
            items = self.local if e[1] == 'search-local' else self.remote
            index = self.operand(e[2], e[3])
            self.target = items[index] if 0 <= index < len(items) else None
            return self.target is not None
        if e[0] in ('player-in-game', 'stance-toward', 'players-building-count'):
            player = self.sn.get('sn-focus-player-number') if e[1] == 'focus-player' else int(e[1])
            p = self.players.get(player, {})
            if e[0] == 'player-in-game': return p.get('active', False)
            if e[0] == 'stance-toward':
                assert e[2] == 'enemy'
                return p.get('enemy', False)
            return self.compare(p.get('buildings', 0), e[2], e[3])
        return super().fact(e)

    def action(self, e, pc=0):
        op, *a = e
        if op == 'up-full-reset-search':
            self.local, self.remote, self.target, self.radius = [], [], None, 99999
        elif op == 'set-strategic-number': self.sn[a[0]] = self.val(a[1])
        elif op == 'up-filter-distance': self.radius = self.val(a[-1])
        elif op == 'up-find-remote':
            found = [i for i, o in self.objects.items() if
                     o['player'] == self.sn.get('sn-focus-player-number')
                     and a[1] in (o.get('cls'), o.get('type'))
                     and math.dist(o['point'], self.point) <= self.radius]
            self.remote.extend(found[:self.val(a[-1])])
        elif op == 'up-get-search-state':
            self.g.update({'local-total': len(self.local), 'remote-total': len(self.remote)})
        elif op == 'up-add-object-by-id':
            i = self.operand(a[1], a[2])
            if i in self.objects: (self.local if a[0] == 'search-local' else self.remote).append(i)
        elif op == 'up-remove-objects':
            items = self.local if a[0] == 'search-local' else self.remote
            keep = []
            for i in items:
                self.target = i
                if not self.compare(self.data(a[1]), a[2], a[3]): keep.append(i)
            if a[0] == 'search-local': self.local = keep
            else: self.remote = keep
        elif op == 'up-modify-goal' and a[1].split(':')[-1] in ('min', '-'):
            value = self.operand(a[1], a[2])
            self.g[a[0]] = min(self.g[a[0]], value) if a[1].endswith('min') else self.g[a[0]] - value
        elif op == 'up-get-point-zone': self.g[a[-1]] = self.zone
        elif op == 'up-get-fact':
            assert a[:2] == ['game-time', '0']
            self.g[a[-1]] = self.now
        elif op == 'up-bound-point':
            self.g[a[0]], self.g[a[0][:-1]+'y'] = self.g[a[1]], self.g[a[1][:-1]+'y']
        elif op == 'up-cross-tiles': pass  # Staging geometry is outside these state/gate tests.
        elif op == 'up-target-point': self.commands.append((list(self.local), a[1]))
        elif op == 'up-modify-group-flag':
            flag = self.val(a[-1])
            if a[0] == '0':
                for o in self.objects.values():
                    if o.get('flag') == flag: o['flag'] = -2
            else:
                assert a[0] == '1'
                for i in self.groups.get(flag, []): self.objects[i]['flag'] = flag
        elif op == 'up-reset-group': self.groups.pop(self.val(a[-1]), None)
        elif op == 'up-create-group': self.groups[self.val(a[-1])] = list(self.local)
        elif op == 'up-reset-search':
            assert a == ['1', '1', '0', '0']
            self.local = []
        elif op in ('up-chat-data-to-all', 'up-chat-data-to-self'):
            self.logs.append((self.string_constants.get(a[0], a[0]), self.operand(a[1], a[2])))
        else: return super().action(e, pc)
        return 0

    def admission_snapshot(self):
        # Execute the actual liveness/diagnostic snapshot, including literal
        # player checks. Do not model the intended classification in Python.
        for n, row in enumerate(self.admission_rules):
            if n in self.admission_disabled: continue
            if all(self.fact(e) for e in expressions(row[3])):
                for e in expressions(row[4]):
                    if e[0] == 'disable-self': self.admission_disabled.add(n)
                    else: self.action(e)

    def sweep(self):
        self.admission_snapshot()
        for row in self.rules:
            self.rule(row)
        return self.g['gl-transport-route-state']

    def rule(self, row):
        if not all(self.fact(e) for e in expressions(row[3])): return False
        for e in expressions(row[4]): self.action(e)
        return True

    def scout(self, reason):
        self.g.update({'gl-assault-fallback-reason': reason, 'gl-transport-screen-id': 11,
                       'gl-assault-screen-start-hp': 100})
        self.objects[11] = dict(id=11, player=2, hp=100, under_attack=0,
            flag=self.val('transport-screen-group'), point=(20, 20))

    def finish(self):
        for _ in range(10):
            state = self.sweep()
            if state in (self.val('TRANSPORT-ROUTE-DEPARTURE-START'),
                         self.val('TRANSPORT-ROUTE-SCREEN-RECALL')): return state
        raise AssertionError('unbounded screening fallback')

    def scan_first_enemy(self):
        for _ in range(8):
            self.sweep()
            if self.g.get('gl-assault-fallback-seen') == 1: return
        raise AssertionError('did not scan first enemy')

    def defense(self, player=7, point=(90, 90), kind='castle'):
        self.objects[100] = dict(id=100, player=player, hp=1000, point=point, type=kind)


class AssaultScreenFallbackTests(unittest.TestCase):
    def test_no_scout_is_immediate_but_approach_timeouts_remain_bounded(self):
        rows = [r for r in rule_blocks(source('rawai-military.per'))
                if '(set-goal gl-transport-route-state TRANSPORT-ROUTE-UNSCREENED-START)' in r[4]]
        self.assertEqual(len(rows), 3)
        self.assertEqual({int(e[2]) for r in rows for e in expressions(r[4])
                          if e[:2] == ['set-goal', 'gl-assault-fallback-reason']}, {3, 5, 9})
        for row in rows:
            if '(set-goal gl-assault-fallback-reason 3)' in row[4]:
                self.assertNotIn('gl-transport-screen-waits', row[3])
                m = ScreenFallback()
                m.g['gl-transport-route-state'] = m.val('TRANSPORT-ROUTE-SCREEN-CHECK')
                self.assertTrue(m.rule(row))
                self.assertEqual(m.finish(), m.val('TRANSPORT-ROUTE-DEPARTURE-START'))
            else:
                self.assertIn('gl-transport-screen-waits c:>= 4', row[3])
            self.assertNotIn('action-unload', row[4])

    def test_full_regular_manifest_can_depart_for_all_three_reasons(self):
        for reason in (3, 5, 9):
            m = ScreenFallback()
            if reason != 3: m.scout(reason)
            self.assertEqual(m.finish(), m.val('TRANSPORT-ROUTE-DEPARTURE-START'))
            self.assertEqual(m.g['gl-assault-fallback-deadline'], 1300)
            self.assertEqual(m.logs[-1][1], reason)
            self.assertFalse(any(action == 'action-unload' for _, action in m.commands))

    def test_accepted_partial_and_full_manifests_are_independent_of_capacity(self):
        for cargo in range(5, 11):
            for capacity in (10, 20, 40):
                for reason in (3, 5, 9):
                    m = ScreenFallback(cargo=cargo, capacity=capacity)
                    if reason != 3: m.scout(reason)
                    self.assertEqual(m.finish(), m.val('TRANSPORT-ROUTE-DEPARTURE-START'))
                    self.assertEqual(m.g['gl-assault-fallback-required'], cargo)

    def test_lowered_request_is_not_acceptance_and_cannot_reuse_another_hull(self):
        for cargo, accepted, hull in ((9, 0, 10), (9, 10, 10), (4, 4, 10), (9, 9, 99)):
            m = ScreenFallback(cargo=cargo, accepted=accepted)
            m.g['gl-assault-manifest-hull'] = hull
            self.assertEqual(m.finish(), m.val('TRANSPORT-ROUTE-SCREEN-RECALL'))
            self.assertEqual(m.g['gl-assault-fallback-denial'], 1)

    def test_invalid_attacked_or_transferred_hull_cannot_depart(self):
        for override in ({'hp': 0}, {'under_attack': 1}, {'player': 3}, {'flag': -2}):
            m = ScreenFallback(); m.objects[10].update(override)
            self.assertEqual(m.finish(), m.val('TRANSPORT-ROUTE-SCREEN-RECALL'))
        m = ScreenFallback(); del m.objects[10]
        self.assertEqual(m.finish(), m.val('TRANSPORT-ROUTE-SCREEN-RECALL'))

    def test_known_defenses_at_either_point_or_later_enemy_veto_departure(self):
        for point in ((50, 50), (90, 90)):
            for kind in ('tower-class', 'sea-tower', 'castle', 'town-center'):
                m = ScreenFallback(); m.defense(point=point, kind=kind)
                self.assertEqual(m.finish(), m.val('TRANSPORT-ROUTE-SCREEN-RECALL'))
                self.assertEqual(m.g['gl-assault-fallback-denial'], 2)

    def test_friendly_or_distant_defenses_do_not_veto_departure(self):
        for player, point in ((3, (90, 90)), (7, (150, 150))):
            m = ScreenFallback(); m.defense(player=player, point=point)
            self.assertEqual(m.finish(), m.val('TRANSPORT-ROUTE-DEPARTURE-START'))

    def test_rechecks_cargo_ownership_and_fire_after_enemy_scan(self):
        for override in ({'cargo': 1}, {'flag': -2}, {'under_attack': 1}):
            m = ScreenFallback(); m.scan_first_enemy()
            self.assertEqual(m.g['gl-assault-fallback-seen'], 1)
            m.objects[10].update(override)
            self.assertEqual(m.finish(), m.val('TRANSPORT-ROUTE-SCREEN-RECALL'))

    def test_changed_acceptance_token_during_scan_is_rejected(self):
        for key, value in (('gl-assault-manifest-count', 9), ('gl-assault-manifest-hull', 99)):
            m = ScreenFallback(); m.sweep()
            m.g[key] = value
            self.assertEqual(m.finish(), m.val('TRANSPORT-ROUTE-SCREEN-RECALL'))

    def test_full_and_partial_acceptance_rules_seal_the_actual_manifest(self):
        rows = list(rule_blocks(source('rawai-military.per')))
        full = next(r for r in rows if '"RAW44C assault ready target:' in r[4])
        partial_gate = next(r for r in rows if '"RAW44B attack load partial hull:' in r[4])
        partial_commit = next(r for r in rows if '"RAW44B attack partial departure:' in r[4])
        for count in range(5, 11):
            m = ScreenFallback(cargo=count, accepted=0)
            m.g['gl-transport-route-state'] = m.val('TRANSPORT-ROUTE-LOAD-CHECK')
            m.local = [10]
            self.assertTrue(m.rule(full))
            self.assertEqual((m.g['gl-assault-manifest-hull'], m.g['gl-assault-manifest-count']), (10, count))
        for count in range(5, 10):
            m = ScreenFallback(cargo=count, accepted=0)
            m.g.update({'gl-transport-route-state': m.val('TRANSPORT-ROUTE-LOAD-CHECK'),
                        'gl-transport-route-load-target': 10, 'gl-transport-route-load-deadline': m.now})
            m.local = [10]
            self.assertFalse(m.rule(full))
            self.assertTrue(m.rule(partial_gate))
            self.assertEqual(m.g['gl-assault-manifest-count'], 0)  # Diagnosis is not yet acceptance.
            # The existing partial diagnostic supplies boarded-only objects to the rebuild.
            for i in range(20, 30):
                m.objects[i] = dict(id=i, player=2, garrisoned=int(i < 20+count),
                                   flag=m.val('attack-boarding-group'), point=(10, 10))
            m.local = list(range(20, 20+count))
            m.g['gl-transport-route-state'] = m.val('TRANSPORT-ROUTE-LOAD-PARTIAL-MANIFEST')
            self.assertTrue(m.rule(partial_commit))
            self.assertEqual((m.g['gl-assault-manifest-hull'], m.g['gl-assault-manifest-count']), (10, count))
            self.assertTrue(all(m.objects[i]['flag'] < 0 for i in range(20+count, 30)))
            m.g['gl-transport-route-state'] = m.val('TRANSPORT-ROUTE-UNSCREENED-START')
            self.assertEqual(m.finish(), m.val('TRANSPORT-ROUTE-DEPARTURE-START'))

    def test_native_loaded_claim_seals_observed_load_and_new_mission_clears_tokens(self):
        rows = list(rule_blocks(source('rawai-military.per')))
        claim = next(r for r in rows if 'object-data-garrison-count gl-assault-manifest-count)' in r[4])
        m = ScreenFallback(cargo=15, accepted=0)
        m.objects[10]['flag'] = -2
        m.remote = [10]
        m.g['gl-transport-route-state'] = m.val('TRANSPORT-ROUTE-FIND')
        self.assertTrue(m.rule(claim))
        self.assertEqual(m.g['gl-assault-manifest-count'], 15)
        self.assertEqual(m.objects[10]['flag'], m.val('attack-transport-group'))
        start = next(r for r in rows if '(set-goal gl-assault-manifest-hull -1)' in r[4])
        self.assertIn('TRANSPORT-ROUTE-IDLE', start[3])
        for goal, value in (('gl-assault-manifest-hull', -1), ('gl-assault-manifest-count', 0),
                            ('gl-assault-fallback-deadline', 0), ('gl-assault-fallback-progress-deadline', 0)):
            self.assertIn(f'(set-goal {goal} {value})', start[4])
        target = next(r for r in rows if 'gl-assault-manifest-player g:= gl-ap-seed-enemy' in r[4])
        self.assertIn('TRANSPORT-ROUTE-IDLE', target[3])
        self.assertIn('gl-ap-seed-enemy', target[4])
        self.assertIn('s:= sn-target-player-number', source('rawai-assault-admission.per'))

    def test_scout_loss_damage_and_fire_during_validation_cannot_be_relaxed(self):
        for reason in (5, 9):
            for override in ({'hp': 99}, {'hp': 0}, {'under_attack': 1}, {'player': 3}, {'flag': -2}, None):
                m = ScreenFallback(); m.scout(reason); m.sweep()
                if override is None: del m.objects[11]
                else: m.objects[11].update(override)
                self.assertEqual(m.finish(), m.val('TRANSPORT-ROUTE-SCREEN-RECALL'))
                self.assertEqual(m.g['gl-assault-fallback-denial'], 5)

    def test_original_enemy_must_still_be_live_and_hostile_not_have_buildings(self):
        for override in ({'active': False}, {'enemy': False}):
            m = ScreenFallback(); m.sweep()
            m.players[6].update(override)  # Enemy7 is still active; not an acceptable silent retarget.
            self.assertEqual(m.finish(), m.val('TRANSPORT-ROUTE-SCREEN-RECALL'))
            self.assertEqual(m.g['gl-assault-fallback-denial'], 4)
        m = ScreenFallback()
        m.players[6]['buildings'] = 0  # Absence of known buildings is not defeat.
        m.sn['sn-target-player-number'] = 3  # Mutable strategic focus cannot replace the mission enemy.
        self.assertEqual(m.finish(), m.val('TRANSPORT-ROUTE-DEPARTURE-START'))

    def test_unknown_or_different_landing_zone_vetoes_departure(self):
        for zone in (-1, 5):
            m = ScreenFallback(); m.zone = zone
            self.assertEqual(m.finish(), m.val('TRANSPORT-ROUTE-SCREEN-RECALL'))
            self.assertEqual(m.g['gl-assault-fallback-denial'], 3)

    def test_no_enemy_uses_bounded_recovery(self):
        m = ScreenFallback(enemies=())
        self.assertEqual(m.finish(), m.val('TRANSPORT-ROUTE-SCREEN-RECALL'))
        self.assertEqual(m.g['gl-assault-fallback-denial'], 4)

    def test_hard_threat_and_scout_loss_veto_candidate_not_whole_mission(self):
        rows = list(rule_blocks(source('rawai-military.per')))
        for reason in (2, 4, 6, 7, 8, 10, 11):
            row = next(r for r in rows if f'(set-goal gl-ap-failure {reason})' in r[4])
            self.assertNotIn('UNSCREENED', row[4])
            self.assertIn('(set-goal gl-transport-route-state AP-FAIL)', row[4])

    def test_does_not_steal_other_scout_or_release_passengers(self):
        m = ScreenFallback()
        m.g['gl-transport-screen-id'] = 11
        m.objects[11] = dict(id=11, player=2, flag=m.val('transport-escort-group'), point=(90, 90))
        m.objects[12] = dict(id=12, player=2, flag=m.val('attack-boarding-group'), point=(10, 10))
        m.finish()
        self.assertEqual(m.objects[10]['flag'], m.val('attack-transport-group'))
        self.assertEqual(m.objects[11]['flag'], m.val('transport-escort-group'))
        self.assertEqual(m.objects[12]['flag'], m.val('attack-boarding-group'))
        self.assertFalse(any(11 in ids for ids, _ in m.commands))

    def test_one_transition_log_pair_and_bounded_unscreened_travel(self):
        m = ScreenFallback(); m.finish()
        self.assertEqual(len(m.logs), 2)
        for _ in range(8): m.sweep()
        self.assertEqual(len(m.logs), 2)
        m.g['gl-transport-route-state'] = m.val('TRANSPORT-ROUTE-WAYPOINT-WAIT')
        m.g['gl-transport-load-clock'] = 1300
        self.assertEqual(m.sweep(), m.val('TRANSPORT-ROUTE-SCREEN-RECALL'))
        self.assertEqual(m.logs[-1][1], 13)
        self.assertEqual(m.g['gl-assault-fallback-deadline'], 0)

    def test_progress_watchdog_ignores_retry_resets_and_bounds_all_voyage_states(self):
        states = ('WAYPOINT-WAIT', 'WAYPOINT-CHECK', 'DEPARTURE-START', 'DEPARTURE-EVALUATE',
                  'DEPARTURE-ORIGIN', 'DEPARTURE-BLOCKERS', 'DEPARTURE-DESTINATION',
                  'DEPARTURE-CLEAR', 'DEPARTURE-CLEAR-WAIT', 'DEPARTURE-RETRY',
                  'DEPARTURE-ISSUE', 'DEPARTURE-CLEAR-CHECK')
        for reason in (3, 5, 9):
            for state in states:
                m = ScreenFallback()
                if reason != 3: m.scout(reason)
                m.finish()
                m.g.update({'gl-transport-route-state': m.val('TRANSPORT-ROUTE-'+state),
                            'gl-transport-load-clock': 1060, 'gl-transport-departure-stalls': 0,
                            'gl-transport-departure-best-distance': 9999})
                self.assertEqual(m.sweep(), m.val('TRANSPORT-ROUTE-SCREEN-RECALL'))
                self.assertEqual(m.logs[-1][1], 14)
                self.assertEqual(m.g['gl-assault-fallback-progress-deadline'], 0)
                before = list(m.logs)
                for _ in range(5): m.sweep()
                self.assertEqual(m.logs, before)  # Terminal once, never a screening retry.

    def test_only_net_waypoint_progress_refreshes_deadline_not_oscillation(self):
        from test_assault_missions import Missions
        m = Missions(); m.prepare(10); m.sweep()
        m.objects[10]['point'] = (40, 40); m.sweep(40)
        deadline = m.g['gl-am1-progress-until']
        m.objects[10]['point'] = (10, 10); m.sweep(24)
        m.objects[10]['point'] = (40, 40); m.sweep(24)
        self.assertEqual(m.g['gl-am1-progress-until'], deadline)
        m.now = deadline; m.sweep()
        self.assertEqual(m.g['gl-am1-state'], 3)
        self.assertEqual(m.g['gl-am1-reason'], 4)

    def test_voyage_graph_cannot_return_to_screening_before_terminal_recovery(self):
        # Inspect every runtime writer, not merely this new module.
        root = Path(__file__).resolve().parents[1]
        edges = {}
        terminal = {'TRANSPORT-ROUTE-IDLE', 'TRANSPORT-ROUTE-RECOVERY-WAIT',
                    'TRANSPORT-ROUTE-RECOVERY-CHECK', 'TRANSPORT-ROUTE-SCREEN-RECALL'}
        for path in root.glob('*.per'):
            for row in rule_blocks(path.read_text(encoding='utf-8-sig')):
                destinations = re.findall(r'\(set-goal gl-transport-route-state ([\w-]+)\)', row[4])
                origins = re.findall(r'\(goal gl-transport-route-state ([\w-]+)\)', row[3])
                if destinations and not origins:
                    if path.name == 'rawai-assault-plans.per':
                        # Active is cleared at handoff/IDLE. Actual integrated
                        # slot-isolation tests cover these preparation guards.
                        self.assertIn('(goal gl-ap-active YES)', row[3])
                        self.assertTrue(set(destinations) <= {'AP-NEXT-ENEMY', 'TRANSPORT-ROUTE-OWNER-LOST',
                                                              'AP-TERMINAL', 'AP-FAIL'})
                    else:
                        self.assertTrue(set(destinations) <= terminal, (path.name, destinations))
                for origin in origins: edges.setdefault(origin, set()).update(destinations)
        seen, todo = set(), ['TRANSPORT-ROUTE-DEPARTURE-START']
        while todo:
            node = todo.pop()
            if node in terminal or node in seen: continue
            seen.add(node)
            self.assertNotIn('SCREEN', node)
            self.assertNotIn('LOAD-', node)
            todo.extend(edges.get(node, ()))
        self.assertIn('101', seen)  # atomic handoff; independent slot states own the voyage
        mission_source = source('rawai-assault-missions.per')
        for i in range(1, 4):
            for r in rule_blocks(mission_source):
                if f'gl-am{i}-' in r[3] and '(goal gl-transport-route-state ' not in r[3]:
                    self.assertNotRegex(r[4], r'\(set-goal gl-transport-route-state TRANSPORT-ROUTE-(?:SCREEN|LOAD)')

    def test_normal_screened_trips_and_unloading_do_not_inherit_timeout(self):
        m = ScreenFallback()
        m.g.update({'gl-transport-route-state': m.val('TRANSPORT-ROUTE-WAYPOINT-WAIT'),
                    'gl-transport-load-clock': 9999, 'gl-assault-fallback-deadline': 0})
        self.assertEqual(m.sweep(), m.val('TRANSPORT-ROUTE-WAYPOINT-WAIT'))
        self.assertEqual(m.logs, [])
        m.g.update({'gl-transport-route-state': m.val('TRANSPORT-ROUTE-RETURN-WAIT'),
                    'gl-assault-fallback-deadline': 1300})
        self.assertEqual(m.sweep(), m.val('TRANSPORT-ROUTE-RETURN-WAIT'))
        self.assertEqual(m.g['gl-assault-fallback-deadline'], 0)


if __name__ == '__main__': unittest.main()
