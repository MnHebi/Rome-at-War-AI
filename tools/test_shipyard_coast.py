import unittest
from per_coastal_fixture import ShipyardFixture
from generate_shipyard_placement import outputs, OFFSETS
from test_pre_backlog import source


class ShipyardTests(unittest.TestCase):
    def test_generated_source(self):
        for name,text in outputs().items(): self.assertEqual(source(name),text)

    def test_first_shipyard_ignores_tech_hold_and_verifies_foundation(self):
        f=ShipyardFixture(); f.g['wait-techup-requirements']=1; f.sweep()
        self.assertEqual(len(f.builds),1)
        self.assertEqual(f.g['gl-sy-stage'],20)
        f.sweep(8); self.assertEqual(len(f.builds),1)
        f.add(10,'shipyard',f.builds[0][1],status='status-pending')
        f.sweep(8); self.assertEqual(f.g['gl-sy-stage'],22)
        self.assertEqual(f.g['gl-sy-foundation'],10)
        f.objects[10]['status']='status-ready'; f.counts['shipyard']=1
        f.sweep(); self.assertEqual(f.g['gl-sy-stage'],0)

    def test_persistent_second_yard_bypasses_only_policy_not_affordability(self):
        f=ShipyardFixture(); f.counts['shipyard']=1; f.g['wait-techup-requirements']=1
        f.sweep(); f.sweep(89); self.assertEqual(f.builds,[])
        f.affordable=False; f.sweep(2); self.assertEqual(f.builds,[])
        f.affordable=True; f.sweep(2); self.assertEqual(len(f.builds),1)

    def test_later_expansion_keeps_tech_hold_and_desired_limit(self):
        f=ShipyardFixture(); f.counts['shipyard']=2; f.g['wait-techup-requirements']=1
        f.sweep(); f.sweep(300); self.assertEqual(f.builds,[])
        f.g['wait-techup-requirements']=0; f.sweep(2); self.assertEqual(len(f.builds),1)
        for desired in (0,1,2):
            f=ShipyardFixture(); f.counts['shipyard']=max(desired,1); f.g['desired-number-shipyards']=desired
            f.sweep(); f.sweep(300); self.assertEqual(f.builds,[])

    def test_missing_foundation_rotates_without_false_success(self):
        f=ShipyardFixture(); f.sweep(); first=f.builds[0][1]
        f.sweep(25)
        self.assertEqual(f.g['gl-sy-reason'],3)
        self.assertEqual(f.g['gl-sy-sector'],1)
        self.assertEqual((f.g['gl-sy-memory0-x'],f.g['gl-sy-memory0-y']),first)
        self.assertEqual(f.g['gl-sy-foundation'],-1)

    def test_status_change_resets_same_type_search_index(self):
        f=ShipyardFixture(); f.sweep()
        f.add(10,'shipyard',f.builds[0][1],status='status-ready')
        f.sweep(8)
        self.assertEqual(f.g['gl-sy-foundation'],10)
        self.assertEqual(f.g['gl-sy-stage'],0)
        f=ShipyardFixture();f.add(10,'shipyard',(54,50),status='status-pending')
        f.sweep();self.assertEqual(f.builds,[])

    def test_crevice_exit_fails_but_open_front_passes(self):
        # Four probes must pass for ONE direction. Different directions cannot
        # combine their individually good tiles into a fabricated open exit.
        for failed in ((64,50),(64,54),(64,46)):
            f=ShipyardFixture()
            f.pathable=lambda o,p,exact: p!=failed and (not exact or p[0]>52)
            for _ in range(4): f.sweep(2)
            self.assertEqual(f.builds,[],failed)
        f=ShipyardFixture(); f.sweep()
        queried={p for i,p,exact in f.path_queries if i==2 and exact}
        self.assertTrue({(58,50),(64,50),(64,54),(64,46)}<=queried)
        self.assertEqual(len(f.builds),1)

    def test_worker_reachability_and_global_hold(self):
        for mode in ('blocked','owned','hold'):
            f=ShipyardFixture()
            if mode=='blocked': f.pathable=lambda o,p,exact:o['id']!=3
            if mode=='owned': f.objects[3]['flag']=8
            if mode=='hold': f.g['gl-owner-worker-hold']=1
            f.sweep(); self.assertEqual(f.builds,[],mode)

    def test_separation_pending_and_map_caps(self):
        f=ShipyardFixture(); f.add(4,'shipyard',(54,50)); f.sweep(); self.assertEqual(f.builds,[])
        for maptype,cap in (('LAKE',4),('RIVERS',6),('ISLANDS',8),('TEAM-ISLANDS',8)):
            f=ShipyardFixture(); f.g['map-type']=f.val(maptype); f.sweep()
            self.assertEqual(f.g['desired-number-shipyards'],cap)
        for pending,placement in ((1,False),(0,True)):
            f=ShipyardFixture(); f.pending=pending; f.placement=placement; f.sweep(); self.assertEqual(f.builds,[])

    def test_finite_coastal_distribution(self):
        self.assertEqual(len(OFFSETS),24)
        self.assertEqual(len(set(OFFSETS)),24)
        self.assertIn((40,0),OFFSETS)
