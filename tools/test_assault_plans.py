"""Execute actual planner + corridor + screening PER; not engine path simulation."""
import math
import re
import unittest
from copy import deepcopy

from generate_assault_plans import APPROACHES, FIELDS, MEMORY, outputs
from test_assault_missions import Missions
from test_pre_backlog import source, expressions
from validate_naval_doctrine import rule_blocks


class Planner(Missions):
    def __init__(self, enemies=(6, 7)):
        super().__init__()
        defs = source('rawai-assault-plan-defs.per')
        self.constants.update({k: int(v) for k, v in re.findall(r'\(defconst ([\w-]+) (-?\d+)\)', defs)})
        self.string_constants.update(dict(re.findall(r'\(defconst ([\w-]+) ("[^"\n]*")\)', defs)))
        self.players = {p: dict(active=p in enemies, enemy=p in enemies, buildings=10) for p in range(1, 9)}
        self.starts = {6: (100, 100), 7: (220, 220), 8: (220, 20)}
        self.timers, self.zones = {}, {}
        # Exact points listed here model engine path rejection for the selected
        # Transport.  The fixture deliberately does not simulate pathfinding.
        self.blocked_paths = set()
        self.disabled = set()
        s = source('rawai-military.per')
        s = s[s.index('(load "rawai-assault-plans")'):s.index(';The preparation owner hands')]
        for name in ('rawai-assault-plans', 'rawai-assault-screen-fallback',
                     'rawai-assault-enemy-scan', 'rawai-assault-cancel-details'):
            s = s.replace(f'(load "{name}")', source(name+'.per'))
        self.rules = list(rule_blocks(s))
        self.g['gl-transport-route-state'] = self.val('TRANSPORT-ROUTE-IDLE')
        self.step()

    def point_value(self, name):
        return self.g.get(name, 0), self.g.get(name[:-1]+'y', 0)

    def fact(self, e):
        if e[0] == 'up-timer-status': return self.now >= self.timers.get(self.val(e[1]), 0)
        if e[0] == 'up-path-distance':
            point = self.point_value(e[1])
            distance = 65535 if point in self.blocked_paths else math.dist(
                self.objects[self.target]['point'], point)
            return self.compare(distance, e[3], e[4])
        return super().fact(e)

    def action(self, e, pc=0):
        op, *a = e
        if op == 'generate-random-number': self.random = 0
        elif op == 'up-get-fact' and a[0] == 'random-number': self.g[a[-1]] = self.random
        elif op == 'up-get-point' and a[0] == 'position-focus':
            self.g[a[1]], self.g[a[1][:-1]+'y'] = self.starts.get(self.sn['sn-focus-player-number'], (200, 200))
        elif op == 'up-set-timer': self.timers[self.val(a[1])] = self.now + self.val(a[3])
        elif op == 'up-get-point-zone':
            point = self.point_value(a[0])
            self.g[a[1]] = next((z for p,z in self.zones.items() if math.dist(p,point) < 0.001),3)
        elif op == 'up-cross-tiles':
            # Deterministic perpendicular geometry only, NOT terrain/path reachability.
            x, y = self.point_value(a[0]); ox, oy = self.point_value(a[1])
            dx, dy = x-ox, y-oy
            length = math.hypot(dx, dy) or 1
            distance = self.val(a[3])
            self.g[a[0]], self.g[a[0][:-1]+'y'] = x-dy/length*distance, y+dx/length*distance
        elif op == 'up-lerp-percent':
            p, q, f = self.point_value(a[0]), self.point_value(a[1]), self.val(a[3])/100
            self.g[a[0]], self.g[a[0][:-1]+'y'] = tuple(x+(y-x)*f for x,y in zip(p,q))
        elif op == 'up-clean-search' and a[0] == 'search-remote':
            self.remote.sort(key=lambda i: math.dist(self.objects[i]['point'], self.point),
                             reverse=a[2] == 'search-order-desc')
        elif op == 'up-get-search-state':
            self.g.update({'local-total':len(self.local), 'remote-total':len(self.remote)})
        else: return super().action(e, pc)
        return 0

    def step(self, seconds=0):
        self.now += seconds
        self.g['gl-transport-load-clock'] = self.now
        self.admission_snapshot()
        for n, row in enumerate(self.rules):
            if n not in self.disabled and all(self.fact(e) for e in expressions(row[3])):
                for e in expressions(row[4]): self.action(e, n)
        return self.g['gl-transport-route-state']

    def objective(self, oid=100, player=6, point=(100, 100), zone=3):
        self.objects[oid] = dict(id=oid, player=player, hp=1000, point=point, zone=zone, type='barracks')
        self.zones[point] = zone

    def scout(self, oid=11):
        self.objects[oid]=dict(id=oid,player=2,hp=100,under_attack=0,flag=-2,
                              type='scout-galley-line',point=(10,10),zone=8,order=0)

    def begin(self, enemy=6, cargo=9, objective=100):
        self.prepare(10, enemy=enemy, cargo=cargo)
        self.objects[10]['under_attack'] = 0
        self.g['gl-transport-route-state'] = self.val('TRANSPORT-ROUTE-TARGET')
        self.g['gl-transport-route-focus'] = 2
        self.sn['sn-focus-player-number'] = enemy
        if objective not in self.objects: self.objective(objective, enemy)
        self.remote = [objective]
        self.g['gl-transport-route-target-x'], self.g['gl-transport-route-target-y'] = self.objects[objective]['point']

    def until(self, *states, bound=150):
        allowed = {self.val(s) for s in states}
        for _ in range(bound):
            if self.step(1) in allowed: return self.g['gl-transport-route-state']
        raise AssertionError(('planner did not terminate', self.g))

    def failed(self, reason=8):
        self.g.update({'gl-ap-failure': reason, 'gl-transport-route-state': self.val('AP-FAIL')})
        self.step()

    def memories(self):
        return [{k: self.g.get(f'gl-ap-memory{i}-{k}', 0) for k in ('enemy','objective','x','y','reason','until')}
                for i in range(1,MEMORY+1) if self.g.get(f'gl-ap-memory{i}-until',0) > self.now]

    def defend_objective(self, oid):
        p = self.objects[oid]['point']; origin = (10,10)
        dx,dy = p[0]-origin[0],p[1]-origin[1]; length = math.hypot(dx,dy)
        for n, offset in enumerate(APPROACHES):
            point = (p[0]-dy/length*offset,p[1]+dx/length*offset)
            i = 100000+oid*10+n
            self.objects[i] = dict(id=i, player=self.objects[oid]['player'], hp=1000,
                                  point=point, zone=3, cls='tower-class', type='test-tower')


class AssaultPlanTests(unittest.TestCase):
    def test_scripted_load_preserves_admitted_overseas_objective(self):
        p = Planner(); p.begin(objective=100)
        p.objective(101, 6, point=(20, 20), zone=8)
        p.g.update({'gl-transport-route-script-load': 1, 'gl-assault-admission-objective': 100,
                    'gl-home-zone': 8})
        p.remote = [101, 100]  # closest generic enemy TC would be on the home island
        p.step()
        self.assertEqual(p.g['gl-ap-objective'], 100)
        self.assertEqual(p.g['gl-transport-route-target-zone'], 3)

    def test_admitted_objective_loss_explicitly_replans_without_home_anchor_substitution(self):
        p = Planner(); p.begin(objective=100)
        p.g.update({'gl-transport-route-script-load': 1, 'gl-assault-admission-objective': 999,
                    'gl-home-zone': 8})
        p.step()
        self.assertTrue(any('plan reason:' in text and value == 30 for text, value in p.logs))
        self.assertEqual(p.objects[10]['cargo'], 9)
        self.assertFalse(any(ids == (10,) and action == 'action-unload' for ids, action, _ in p.commands))

    def test_generated_outputs_and_storage_are_consistent(self):
        for name, text in outputs().items(): self.assertEqual(source(name), text)
        p = Planner()
        ids = [p.val('gl-ap-'+f) for f in FIELDS]
        ids += [p.val(f'gl-ap-memory{i}-{f}') for i in range(1,MEMORY+1)
                for f in ('enemy','objective','x','y','reason','until')]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all(15000 <= n < 16000 for n in ids))
        from pathlib import Path
        all_goals=[(k,int(v)) for f in Path(__file__).resolve().parents[1].glob('*.per')
                   for k,v in re.findall(r'\(defconst (gl-[\w-]+) (-?\d+)\)',source(f.name))]
        for key,value in all_goals:
            if key.startswith('gl-ap-'):
                self.assertEqual([k for k,v in all_goals if v==value],[key])

    def test_safe_full_and_accepted_partial_keep_same_hull_manifest(self):
        for cargo in (5,9,10):
            p=Planner(); p.begin(cargo=cargo)
            self.assertEqual(p.until('TRANSPORT-ROUTE-DEPARTURE-START','TRANSPORT-ROUTE-RECOVERY-WAIT'),
                             p.val('TRANSPORT-ROUTE-DEPARTURE-START'))
            self.assertEqual((p.g['gl-assault-manifest-hull'],p.g['gl-assault-manifest-count']), (10,cargo))
            self.assertFalse(any(10 in ids and a=='action-unload' for ids,a,point in p.commands))

    def test_unreachable_unload_is_remembered_then_another_approach_departs(self):
        p=Planner();p.begin()
        p.until('AP-PATH')
        first=p.point_value('gl-transport-route-landing-x')
        p.blocked_paths.add(first)
        state=p.until('TRANSPORT-ROUTE-DEPARTURE-START','TRANSPORT-ROUTE-RECOVERY-WAIT')
        self.assertEqual(state,p.val('TRANSPORT-ROUTE-DEPARTURE-START'))
        self.assertTrue(any(m['reason']==36 and (m['x'],m['y'])==first for m in p.memories()))
        self.assertNotEqual(p.point_value('gl-transport-route-landing-x'),first)
        self.assertEqual(p.objects[10]['cargo'],9)
        self.assertFalse(any(10 in ids and action=='action-unload'
                             for ids,action,_ in p.commands))

    def test_unreachable_exact_corridor_is_remembered_then_another_approach_departs(self):
        p=Planner();p.begin()
        p.until('AP-PATH')
        first_landing=p.point_value('gl-transport-route-landing-x')
        first_waypoint=p.point_value('gl-transport-route-waypoint-x')
        p.blocked_paths.add(first_waypoint)
        state=p.until('TRANSPORT-ROUTE-DEPARTURE-START','TRANSPORT-ROUTE-RECOVERY-WAIT')
        self.assertEqual(state,p.val('TRANSPORT-ROUTE-DEPARTURE-START'))
        self.assertTrue(any(m['reason']==37 and (m['x'],m['y'])==first_landing
                            for m in p.memories()))
        self.assertNotEqual(p.point_value('gl-transport-route-landing-x'),first_landing)
        self.assertEqual(p.objects[10]['cargo'],9)
        self.assertFalse(any(10 in ids and action=='action-unload'
                             for ids,action,_ in p.commands))

    def test_failure_remembers_candidate_without_unloading_or_resetting_budget(self):
        p=Planner(); p.begin(); p.step()
        point=p.point_value('gl-transport-route-landing-x'); until=p.g['gl-ap-until']
        p.failed(8)
        self.assertEqual(p.memories()[0], dict(enemy=6,objective=100,x=point[0],y=point[1],reason=8,until=p.now+300))
        p.step()
        self.assertNotEqual(p.point_value('gl-transport-route-landing-x'), point)
        self.assertEqual(p.g['gl-ap-until'],until)
        self.assertEqual(p.objects[10]['cargo'],9)
        self.assertEqual(p.objects[10]['flag'],p.val('attack-transport-group'))
        self.assertFalse(any(10 in ids for ids,a,point in p.commands))

    def test_memory_survives_new_mission_then_expires(self):
        p=Planner(); p.begin(); p.step(); p.failed()
        p.g['gl-transport-route-state']=p.val('TRANSPORT-ROUTE-IDLE'); p.step()
        p.begin(); p.step(); p.step()
        self.assertNotEqual(p.point_value('gl-transport-route-landing-x'),(100,100))
        expiry=p.memories()[0]['until']
        p.now=expiry
        p.g['gl-transport-route-state']=p.val('TRANSPORT-ROUTE-IDLE');p.step()
        p.begin();p.step()
        self.assertEqual(p.point_value('gl-transport-route-landing-x'),(100,100))

    def test_all_screen_failures_enter_replan_not_unload(self):
        rows=list(rule_blocks(source('rawai-military.per')))
        for reason in (2,4,6,7,8,10,11):
            r=next(r for r in rows if f'(set-goal gl-ap-failure {reason})' in r[4])
            self.assertIn('(set-goal gl-transport-route-state AP-FAIL)',r[4])
            self.assertNotIn('action-unload',r[4])
            self.assertNotIn('UNSCREENED',r[4])

    def test_lost_scout_uses_different_beach_before_unscreened_fallback(self):
        p=Planner();p.begin();p.step();first=p.point_value('gl-transport-route-landing-x')
        p.failed(10)
        self.assertEqual(p.until('TRANSPORT-ROUTE-DEPARTURE-START','TRANSPORT-ROUTE-RECOVERY-WAIT'),
                         p.val('TRANSPORT-ROUTE-DEPARTURE-START'))
        self.assertNotEqual(p.point_value('gl-transport-route-landing-x'),first)
        self.assertEqual(p.g['gl-assault-fallback-reason'],3)

    def test_known_other_enemy_defense_vetoes_candidate(self):
        p=Planner();p.begin()
        p.objects[900]=dict(id=900,player=7,hp=1000,point=(100,100),type='castle')
        p.until('TRANSPORT-ROUTE-DEPARTURE-START','TRANSPORT-ROUTE-RECOVERY-WAIT')
        self.assertTrue(any(m['reason']==11 and (m['x'],m['y'])==(100,100) for m in p.memories()))
        self.assertNotEqual(p.point_value('gl-transport-route-landing-x'),(100,100))

    def test_wrong_island_candidate_is_recorded_and_skipped(self):
        p=Planner();p.begin();p.step();p.failed()
        target=(100,100);s=28/math.sqrt(2)
        p.zones[(target[0]-s,target[1]+s)]=9
        p.step()
        self.assertTrue(any(m['reason']==21 for m in p.memories()))

    def test_exhausted_objective_searches_same_landmass_before_enemy(self):
        p=Planner();p.objective();p.objective(200,6,(160,100));p.defend_objective(100);p.begin()
        p.until('TRANSPORT-ROUTE-DEPARTURE-START','TRANSPORT-ROUTE-RECOVERY-WAIT')
        self.assertEqual(p.g['gl-assault-manifest-player'],6)
        self.assertEqual(p.g['gl-ap-objective'],200)
        self.assertEqual(p.g['gl-ap-enemy6-failures'],1)

    def test_three_exhausted_objectives_rotate_persistently_without_touching_slots(self):
        p=Planner()
        for oid,point in ((100,(70,70)),(200,(130,70)),(300,(190,70))):
            p.objective(oid,6,point);p.defend_objective(oid)
        p.objective(400,7,(220,220));p.begin()
        saved={f'gl-am{i}-{f}':p.g.get(f'gl-am{i}-{f}',0) for i in (1,2,3) for f in ('state','hull','enemy','cargo')}
        p.until('TRANSPORT-ROUTE-DEPARTURE-START','TRANSPORT-ROUTE-RECOVERY-WAIT')
        self.assertEqual(p.g['gl-assault-manifest-player'],7)
        self.assertEqual(p.g['gl-ap-enemy6-failures'],3)
        self.assertGreater(p.g['gl-ap-enemy6-until'],p.now)
        self.assertEqual({k:p.g.get(k,0) for k in saved},saved)
        p.sn['sn-target-player-number']=6;p.admission_snapshot()
        self.assertEqual(p.g['gl-ap-seed-enemy'],7)

    def test_fourth_living_enemy_is_evaluated_before_loaded_mission_recovers(self):
        # T25 Yellow exhausted defended/wrong-zone approaches to player 8, then
        # found no overseas objectives for players 5 and 6. The historical
        # three-opponent cap recovered the load before player 7 was inspected.
        p=Planner(enemies=(5,6,7,8))
        p.objective(100,8,(100,100));p.defend_objective(100)
        p.objective(400,7,(220,220));p.begin(enemy=8,objective=100)
        p.until('TRANSPORT-ROUTE-DEPARTURE-START','TRANSPORT-ROUTE-RECOVERY-WAIT',bound=300)
        self.assertEqual(p.g['gl-transport-route-state'],p.val('TRANSPORT-ROUTE-DEPARTURE-START'))
        self.assertEqual(p.g['gl-assault-manifest-player'],7)
        self.assertEqual(p.g['gl-ap-enemies-tried'],4)

    def test_enemy_deadline_rotates_and_total_deadline_recovers(self):
        p=Planner();p.objective(200,7,(220,220));p.begin();p.step()
        p.step(180)
        self.assertEqual(p.g['gl-assault-manifest-player'],7)
        self.assertGreater(p.g['gl-ap-enemy6-until'],p.now)
        p.step(180)
        self.assertEqual(p.g['gl-transport-route-state'],p.val('TRANSPORT-ROUTE-RECOVERY-WAIT'))
        self.assertTrue(any(10 in ids and a=='action-unload' for ids,a,point in p.commands))

    def test_invalid_manifest_or_attacked_hull_recovers_without_blame_to_enemy(self):
        for change in ({'cargo':4},{'under_attack':1}):
            p=Planner();p.begin();p.objects[10].update(change);p.step()
            self.assertEqual(p.g['gl-transport-route-state'],p.val('TRANSPORT-ROUTE-RECOVERY-WAIT'))
            self.assertEqual(p.g.get('gl-ap-enemy6-failures',0),0)

    def test_replaced_owner_is_not_commanded(self):
        p=Planner();p.begin();p.objects[10]['flag']=p.val('assault-mission-2-group');p.step()
        self.assertEqual(p.g['gl-transport-route-state'],p.val('TRANSPORT-ROUTE-OWNER-LOST'))
        self.assertFalse(any(10 in ids for ids,a,point in p.commands))

    def test_no_alternative_enemy_is_bounded_recovery(self):
        p=Planner(enemies=(6,));p.begin();p.step();p.step(180)
        self.assertEqual(p.g['gl-transport-route-state'],p.val('TRANSPORT-ROUTE-RECOVERY-WAIT'))
        self.assertTrue(p.memories())

    def test_actual_scout_loss_records_a_then_acquires_replacement_for_b(self):
        p=Planner();p.begin();p.scout()
        p.until('TRANSPORT-ROUTE-SCREEN-WAIT')
        first=p.point_value('gl-transport-route-landing-x')
        del p.objects[11]
        p.step(31)
        self.assertEqual(p.g['gl-transport-route-state'],p.val('AP-FAIL'))
        self.assertEqual(p.g['gl-ap-failure'],6)
        p.scout(12)
        p.until('TRANSPORT-ROUTE-SCREEN-WAIT')
        self.assertEqual(p.g['gl-transport-screen-id'],12)
        self.assertNotEqual(p.point_value('gl-transport-route-landing-x'),first)
        self.assertEqual(p.memories()[0]['reason'],6)
        self.assertFalse(any(10 in ids for ids,a,point in p.commands))

    def test_scout_damage_at_either_screen_stage_vetoes_candidate(self):
        for landing in (False,True):
            p=Planner();p.begin();p.scout();p.until('TRANSPORT-ROUTE-SCREEN-WAIT')
            if landing:
                p.objects[11]['point']=p.point_value('gl-transport-route-waypoint-x')
                p.step(31)
                self.assertEqual(p.g['gl-transport-route-state'],p.val('TRANSPORT-ROUTE-SCREEN-LANDING-WAIT'))
            p.objects[11]['hp']=90  # damage remains evidence after under-attack clears
            p.step(31)
            self.assertEqual(p.g['gl-transport-route-state'],p.val('AP-FAIL'))
            self.assertEqual(p.g['gl-ap-failure'],8 if landing else 4)
            p.step()
            self.assertEqual(p.memories()[0]['reason'],8 if landing else 4)
            self.assertFalse(any(10 in ids for ids,a,point in p.commands))

    def test_danger_checked_before_scout_and_again_after_successful_screen(self):
        p=Planner();p.begin();p.scout();p.step()
        self.assertFalse(any(11 in ids for ids,a,point in p.commands))
        p.until('TRANSPORT-ROUTE-SCREEN-WAIT')
        p.objects[11]['point']=p.point_value('gl-transport-route-waypoint-x');p.step(31)
        p.objects[11]['point']=p.point_value('gl-transport-route-landing-x');p.step(31)
        self.assertEqual(p.g['gl-transport-route-state'],p.val('AP-FINAL-SAFETY'))
        p.objects[900]=dict(id=900,player=7,hp=1000,point=p.point_value('gl-transport-route-landing-x'),type='castle')
        p.step()
        self.assertEqual(p.memories()[0]['reason'],11)
        self.assertFalse(any(10 in ids for ids,a,point in p.commands))

    def test_converted_scout_and_other_controller_are_not_retasked_by_replan(self):
        for change in ({'player':7},{'flag':14}):
            p=Planner();p.begin();p.scout();p.until('TRANSPORT-ROUTE-SCREEN-WAIT')
            p.objects[11].update(change);before=deepcopy(p.objects[11]);p.commands.clear()
            p.failed(6)
            self.assertEqual(p.objects[11],before)
            self.assertFalse(any(11 in ids for ids,a,point in p.commands))

    def test_plan_guards_leave_two_active_slots_untouched_and_third_handoff_one_way(self):
        m=Missions()
        for hull,enemy in ((20,6),(30,7)): m.prepare(hull,enemy);m.sweep()
        p=Planner();p.g.update(m.g);p.objects=deepcopy(m.objects);p.groups=deepcopy(m.groups)
        p.begin();p.step();p.failed(8)
        saved={k:v for k,v in p.g.items() if k.startswith(('gl-am1-','gl-am2-'))}
        p.sn['sn-target-player-number']=8
        p.until('TRANSPORT-ROUTE-DEPARTURE-START')
        self.assertEqual(saved,{k:p.g[k] for k in saved})
        self.assertEqual(p.g['gl-assault-manifest-player'],6)
        self.assertFalse(any(set(ids)&{20,30} for ids,a,point in p.commands))
        oldrules,olddisabled=p.rules,p.disabled
        p.rules=list(rule_blocks(source('rawai-assault-missions.per')));p.disabled=set()
        Missions.sweep(p)
        p.rules,p.disabled=oldrules,olddisabled
        self.assertEqual(p.g['gl-am3-hull'],10)
        self.assertEqual(p.g['gl-transport-route-state'],p.val('TRANSPORT-ROUTE-IDLE'))
        saved={k:v for k,v in p.g.items() if k.startswith('gl-am')};p.commands.clear()
        p.step(400)
        self.assertEqual(p.g['gl-ap-active'],0)
        self.assertEqual(saved,{k:p.g[k] for k in saved})
        self.assertFalse(p.commands)

    def test_memory_skips_do_not_multiply_failure_counts_and_cooldown_expires(self):
        p=Planner();p.begin();p.step();p.failed(8)
        p.g['gl-transport-route-state']=p.val('AP-CANDIDATE');p.g['gl-ap-candidate']=0
        count=len(p.logs);p.step()
        self.assertEqual(len(p.logs),count)
        self.assertEqual(p.g.get('gl-ap-enemy6-failures',0),0)
        p.g['gl-ap-enemy6-until']=p.now+300;p.g['gl-ap-enemy6-failures']=3
        p.g['gl-ap-preferred-enemy']=6;p.sn['sn-target-player-number']=6;p.admission_snapshot()
        self.assertEqual(p.g['gl-ap-seed-enemy'],7)
        p.now+=300;p.admission_snapshot()
        self.assertEqual(p.g['gl-ap-seed-enemy'],6)
        self.assertEqual(p.g['gl-ap-enemy6-failures'],0)

    def test_enemy_departure_is_explicit_replan_with_original_enemy_identity(self):
        for field,reason in (('active',28),('enemy',29)):
            p=Planner();p.objective(200,7,(220,220));p.begin();p.step()
            p.players[6][field]=False;p.step()
            self.assertEqual(p.g['gl-assault-manifest-player'],7)
            self.assertIn(('"RAW plan enemy: %d"',6),p.logs)
            self.assertIn(('"RAW plan reason: %d"',reason),p.logs)
            self.assertIn(('"RAW plan next-enemy: %d"',7),p.logs)
            self.assertEqual(p.objects[10]['cargo'],9)


if __name__=='__main__': unittest.main()
