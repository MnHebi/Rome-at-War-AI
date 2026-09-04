"""Actual T19 candidate zone gates; physical unloading remains a replay test."""
import math
import unittest

from test_assault_plans import Planner
from test_pre_backlog import source
from validate_naval_doctrine import rule_blocks


class AssaultLandingZoneTests(unittest.TestCase):
    def choose(self, invalid_offsets=(), unknown=False):
        p=Planner(enemies=(6,));p.begin();p.step();p.failed(8)
        for offset in invalid_offsets:
            s=offset/math.sqrt(2)
            p.zones[(100-s,100+s)]=5
        if unknown: p.g['gl-transport-route-target-zone']=-1
        state=p.until('TRANSPORT-ROUTE-DEPARTURE-START','TRANSPORT-ROUTE-RECOVERY-WAIT')
        return p,state

    def test_other_island_left_landing_does_not_beat_valid_right(self):
        p,state=self.choose((28,))
        self.assertEqual(state,p.val('TRANSPORT-ROUTE-DEPARTURE-START'))
        self.assertEqual(p.g['gl-ap-candidate'],2)

    def test_other_island_right_landing_does_not_beat_valid_left(self):
        p,state=self.choose((-28,))
        self.assertEqual(state,p.val('TRANSPORT-ROUTE-DEPARTURE-START'))
        self.assertEqual(p.g['gl-ap-candidate'],1)

    def test_no_valid_candidate_retains_bounded_recovery(self):
        for unknown in (False,True):
            p,state=self.choose((28,-28,56,-56),unknown)
            self.assertEqual(state,p.val('TRANSPORT-ROUTE-RECOVERY-WAIT'))
            self.assertTrue(any(m['reason']==21 for m in p.memories()))

    def test_two_failed_lateral_candidates_do_not_exhaust_coastline(self):
        p,state=self.choose((28,-28))
        self.assertEqual(state,p.val('TRANSPORT-ROUTE-DEPARTURE-START'))
        self.assertEqual(p.g['gl-ap-candidate'],3)
        self.assertEqual(p.g['gl-assault-manifest-player'],6)

    def test_zone_captured_from_exact_points_on_every_entry_path(self):
        rows=list(rule_blocks(source('rawai-assault-plans.per')))
        objectives=[r for r in rows if '(up-get-point-zone gl-transport-route-target-x ' in r[4]]
        self.assertEqual(len(objectives),1)
        self.assertIn('(goal gl-transport-route-state AP-OBJECTIVE)',objectives[0][3])
        candidates=[r for r in rows if '(up-get-point-zone gl-transport-route-landing-x ' in r[4]]
        self.assertEqual(len(candidates),5)
        for r in candidates:
            self.assertLess(r[4].index('(up-bound-point '),r[4].index('(up-get-point-zone '))
            if '(up-cross-tiles ' in r[4]:
                self.assertLess(r[4].index('(up-cross-tiles '),r[4].index('(up-get-point-zone '))

    def test_loaded_hull_proves_unload_vicinity_and_exact_corridor_before_screening(self):
        plans=source('rawai-assault-plans.per')
        rows=list(rule_blocks(plans))
        path_rows=[r for r in rows if '(goal gl-transport-route-state AP-PATH)' in r[3]]
        self.assertEqual(len(path_rows),4)
        selector=path_rows[0]
        self.assertIn('(up-add-object-by-id search-local g: gl-transport-route-id)',selector[4])
        self.assertIn('(up-remove-objects search-local object-data-player != my-player-number)',selector[4])
        self.assertIn('(up-remove-objects search-local object-data-group-flag != attack-transport-group)',selector[4])
        self.assertIn('(up-path-distance gl-transport-route-landing-x 0 == 65535)',path_rows[1][3])
        self.assertIn('(set-goal gl-ap-failure 36)',path_rows[1][4])
        self.assertIn('(up-path-distance gl-transport-route-waypoint-x 1 == 65535)',path_rows[2][3])
        self.assertIn('(set-goal gl-ap-failure 37)',path_rows[2][4])
        self.assertIn('(up-path-distance gl-transport-route-landing-x 0 != 65535)',path_rows[3][3])
        self.assertIn('(up-path-distance gl-transport-route-waypoint-x 1 != 65535)',path_rows[3][3])
        self.assertIn('(set-goal gl-transport-route-state TRANSPORT-ROUTE-SCREEN-FIND)',path_rows[3][4])

        military=source('rawai-military.per')
        corridor_rows=[r for r in rule_blocks(military)
                       if '(goal gl-transport-route-state TRANSPORT-ROUTE-CORRIDOR-' in r[3]
                       and '(up-bound-point gl-transport-route-waypoint-x ' in r[4]]
        self.assertEqual(len(corridor_rows),4)
        for row in corridor_rows:
            self.assertIn('(set-goal gl-transport-route-state AP-PATH)',row[4])
            self.assertNotIn('TRANSPORT-ROUTE-SCREEN-FIND',row[4])


if __name__=='__main__': unittest.main()
