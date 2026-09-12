"""Execute allied-base last-choice PER. Terrain/path results are fixture inputs,
not proof of engine reachability or runtime assault success.
"""
import unittest
from copy import deepcopy

from test_assault_plans import Planner
from shoreline_resolver import shoreline_candidates


def ally(p, player=3, oid=200, point=(140, 20), zone=3, **changes):
    p.players[player].update(active=True, enemy=False, ally=True)
    p.objects[oid] = dict(id=oid, player=player, type='town-center', hp=1000,
                          status='status-ready', point=point, zone=zone)
    p.objects[oid].update(changes)
    p.zones[point] = zone
    return oid


def exhausted(p, cargo=9):
    p.begin(cargo=cargo)
    p.step()
    p.g['gl-transport-route-state'] = p.val('AP-ENEMY-FAILED')
    p.g['gl-ap-enemy6-failures'] = 3


def finish(p):
    return p.until('TRANSPORT-ROUTE-DEPARTURE-START', 'TRANSPORT-ROUTE-RECOVERY-WAIT')


def reasons(p):
    return [value for text, value in p.logs if 'plan reason:' in text]


class AlliedFallbackTests(unittest.TestCase):
    def test_healthy_direct_plan_does_not_use_ally(self):
        p = Planner(enemies=(6,)); ally(p); p.witness(); p.begin()
        self.assertEqual(finish(p), p.val('TRANSPORT-ROUTE-DEPARTURE-START'))
        self.assertNotIn(42, reasons(p))
        self.assertEqual(p.g['gl-ap-ally-tried'], p.val('NO'))

    def test_last_choice_preserves_enemy_and_accepted_full_or_partial_load(self):
        for cargo in (5, 9, 10):
            with self.subTest(cargo=cargo):
                p = Planner(enemies=(6,)); ally(p); p.witness(); exhausted(p, cargo)
                before = deepcopy({k:v for k,v in p.g.items() if k.startswith('gl-am')})
                deadline = p.g['gl-ap-until']
                self.assertEqual(finish(p), p.val('TRANSPORT-ROUTE-DEPARTURE-START'))
                self.assertIn(42, reasons(p)); self.assertIn(46, reasons(p))
                self.assertEqual((p.g['gl-ap-objective'], p.g['gl-assault-manifest-player']), (100, 6))
                self.assertEqual(p.point_value('gl-transport-route-target-x'), (100,100))
                self.assertEqual((p.g['gl-assault-manifest-hull'], p.g['gl-assault-manifest-count']), (10,cargo))
                self.assertEqual(p.objects[10]['cargo'], cargo)
                self.assertEqual(p.g['gl-ap-until'], deadline)
                self.assertEqual({k:v for k,v in p.g.items() if k.startswith('gl-am')}, before)
                self.assertEqual(p.g['gl-ap-ally-base'], 200)
                self.assertIn(p.point_value('gl-transport-route-landing-x'),
                              [land for _, land, _ in shoreline_candidates((140,20),(10,10),3,p.zone_function)])
                self.assertFalse(any(10 in ids and action=='action-unload' for ids,action,_ in p.commands))

    def test_ineligible_bases_never_become_anchors(self):
        for change in ('other-island','self','neutral','dead-ally','foundation','packed','dead-base'):
            with self.subTest(change=change):
                p = Planner(enemies=(6,)); ally(p); p.witness()
                if change=='other-island': p.objects[200]['zone']=9
                if change=='self': p.objects[200]['player']=2; p.players[2].update(active=True,ally=True)
                if change=='neutral': p.players[3]['ally']=False
                if change=='dead-ally': p.players[3]['active']=False
                if change=='foundation': p.objects[200]['status']=-1
                if change=='packed': p.objects[200]['type']='packed-town-center'
                if change=='dead-base': p.objects[200]['hp']=0
                exhausted(p)
                self.assertEqual(finish(p),p.val('TRANSPORT-ROUTE-RECOVERY-WAIT'))
                self.assertNotIn(42,reasons(p))

    def test_no_witness_is_not_same_zone_permission(self):
        p=Planner(enemies=(6,)); ally(p); exhausted(p)
        self.assertEqual(finish(p),p.val('TRANSPORT-ROUTE-RECOVERY-WAIT'))
        self.assertIn(45,reasons(p)); self.assertNotIn(46,reasons(p))

    def test_cliff_disconnected_ally_shore_rejected(self):
        p=Planner(enemies=(6,)); ally(p); p.witness()
        for _,land,_ in shoreline_candidates((140,20),(10,10),3,p.zone_function):
            p.exact_only_blocked_pairs.add((101,land))
        exhausted(p)
        self.assertEqual(finish(p),p.val('TRANSPORT-ROUTE-RECOVERY-WAIT'))
        self.assertIn(41,reasons(p)); self.assertNotIn(46,reasons(p))

    def test_defended_ally_coast_rejected(self):
        p=Planner(enemies=(6,)); ally(p); p.witness()
        p.defend_objective(200)
        for oid,obj in p.objects.items():
            if oid>=100000: obj['player']=6
        exhausted(p)
        self.assertEqual(finish(p),p.val('TRANSPORT-ROUTE-RECOVERY-WAIT'))
        self.assertIn(11,reasons(p)); self.assertNotIn(46,reasons(p))

    def test_revalidate_ally_base_before_commit(self):
        for change in ('dead','packed','neutral'):
            with self.subTest(change=change):
                p=Planner(enemies=(6,)); ally(p); p.witness(); exhausted(p)
                p.until('AP-PATH')
                if change=='dead': p.objects[200]['hp']=0
                if change=='packed': p.objects[200]['type']='packed-town-center'
                if change=='neutral': p.players[3]['ally']=False
                self.assertEqual(finish(p),p.val('TRANSPORT-ROUTE-RECOVERY-WAIT'))
                self.assertNotIn(46,reasons(p))

    def test_bounded_attempt_does_not_extend_total_clock(self):
        p=Planner(enemies=(6,)); ally(p); p.witness(); exhausted(p)
        p.until('AP-SHORE-INIT')
        original=p.g['gl-ap-until']
        p.step(121)
        self.assertEqual(p.g['gl-ap-until'],original)
        self.assertEqual(p.g['gl-ap-active'],p.val('NO'))
        self.assertNotIn(46,reasons(p))

    def test_normal_coasts_really_exhaust_before_allied_fallback(self):
        p=Planner(enemies=(6,)); ally(p); p.witness()
        for _,land,_ in shoreline_candidates((100,100),(10,10),3,p.zone_function):
            p.blocked_path_pairs.add((10,land))
        p.begin()
        self.assertEqual(finish(p),p.val('TRANSPORT-ROUTE-DEPARTURE-START'))
        self.assertGreater(p.g['gl-ap-enemy6-failures'],0)
        self.assertIn(42,reasons(p)); self.assertIn(46,reasons(p))
        self.assertTrue(p.memories())

    def test_second_ally_tried_without_restarting_enemy_coasts(self):
        p=Planner(enemies=(6,)); ally(p); ally(p,4,201,(20,140)); p.witness()
        for _,land,_ in shoreline_candidates((140,20),(10,10),3,p.zone_function):
            p.exact_only_blocked_pairs.add((101,land))
        exhausted(p)
        self.assertEqual(finish(p),p.val('TRANSPORT-ROUTE-DEPARTURE-START'))
        self.assertEqual(p.g['gl-ap-ally-base'],201)
        self.assertEqual(reasons(p).count(42),2)
        self.assertEqual(p.g['gl-ap-enemy6-failures'],3)

    def test_successful_screen_and_final_revalidation_fit_bounded_attempt(self):
        p=Planner(enemies=(6,)); ally(p); p.witness(); exhausted(p); p.scout()
        p.until('TRANSPORT-ROUTE-SCREEN-WAIT')
        p.objects[11]['point']=p.point_value('gl-transport-route-waypoint-x'); p.step(31)
        self.assertEqual(p.g['gl-transport-route-state'],p.val('TRANSPORT-ROUTE-SCREEN-LANDING-WAIT'))
        p.objects[11]['point']=p.point_value('gl-transport-route-landing-x'); p.step(31)
        self.assertEqual(p.g['gl-transport-route-state'],p.val('AP-FINAL-SAFETY'))
        self.assertEqual(finish(p),p.val('TRANSPORT-ROUTE-DEPARTURE-START'))
        self.assertIn(46,reasons(p))

    def test_unscreened_final_base_loss_blocks_commit(self):
        p=Planner(enemies=(6,)); ally(p); p.witness(); exhausted(p)
        p.until('AP-FINAL-SAFETY')
        p.objects[200]['hp']=0
        self.assertEqual(finish(p),p.val('TRANSPORT-ROUTE-RECOVERY-WAIT'))
        self.assertNotIn(46,reasons(p))

    def test_total_mission_deadline_still_wins(self):
        p=Planner(enemies=(6,)); ally(p); p.witness(); exhausted(p)
        p.until('AP-SHORE-INIT')
        p.now=p.g['gl-ap-until']
        p.step()
        self.assertEqual(p.g['gl-ap-active'],p.val('NO'))
        self.assertIn(22,reasons(p))
        self.assertEqual(reasons(p).count(42),1)

    def test_real_hull_emergency_is_not_an_ally_replan(self):
        p=Planner(enemies=(6,)); ally(p); p.witness(); exhausted(p)
        p.until('AP-SHORE-INIT')
        p.objects[10]['under_attack']=1
        p.step(121)
        self.assertEqual(p.g['gl-ap-active'],p.val('NO'))
        self.assertIn(24,reasons(p))
        self.assertNotIn(46,reasons(p))


if __name__=='__main__': unittest.main()
