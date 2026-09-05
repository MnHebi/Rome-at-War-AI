import unittest
from per_coastal_fixture import ShipyardFixture
from generate_shipyard_placement import outputs, CANDIDATE_RADIUS, CANDIDATE_SPAN
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

    def test_minimum_capacity_does_not_require_a_preexisting_nearby_hull(self):
        first=ShipyardFixture(); del first.objects[2]
        first.sweep(); self.assertEqual(len(first.builds),1)
        second=ShipyardFixture(); del second.objects[2]
        second.counts['shipyard']=1; second.g['wait-techup-requirements']=1
        second.sweep(); second.sweep(89); self.assertEqual(second.builds,[])
        second.sweep(2); self.assertEqual(len(second.builds),1)

    def test_distant_trade_cog_is_a_valid_exact_water_probe(self):
        f=ShipyardFixture(); del f.objects[2]
        f.add(4,'trade-cog-class',(180,50),zone=8)
        f.sweep()
        self.assertEqual(len(f.builds),1)
        self.assertTrue(any(i==4 and exact for i,_,exact in f.path_queries))

    def test_expansion_beyond_minimum_still_requires_mobile_water_proof(self):
        f=ShipyardFixture(); del f.objects[2]
        f.counts['shipyard']=2; f.g['wait-techup-requirements']=0
        f.sweep()
        self.assertEqual(f.builds,[])
        self.assertEqual(f.g['gl-sy-reason'],8)

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

    def test_allied_naval_buildings_also_reserve_clearance(self):
        for kind,status in (('port','status-ready'),('shipyard','status-pending')):
            f=ShipyardFixture(); f.sn['sn-focus-player-number']=7
            f.add(10,kind,(54,50),player=3,status=status)
            f.sweep(); self.assertEqual(f.builds,[])
            self.assertEqual(f.sn['sn-focus-player-number'],7)

    def test_dense_near_anchor_sampling_and_cursor_wrap(self):
        f=ShipyardFixture(); f.random_values=[0,0,26,14]
        f.can_site=lambda point: point==(52,50)
        f.sweep()
        self.assertEqual(f.builds,[])
        self.assertEqual(f.g['gl-sy-reason'],64)
        self.assertEqual(f.g['gl-sy-sector'],1)
        # A single ready Port exhausts the ordered cursor here. The rebuilt
        # anchor list must wrap without reporting 61 or consuming this sample.
        f.sweep(2)
        self.assertEqual(f.builds,[('shipyard',(52,50))])
        self.assertNotEqual(f.g['gl-sy-reason'],61)

    def test_dense_candidate_domain_preserves_exact_safety_gates(self):
        generated=outputs()['rawai-specialplacement.per']
        self.assertEqual(CANDIDATE_SPAN,29)
        self.assertEqual(CANDIDATE_RADIUS,14)
        self.assertEqual(generated.count('(generate-random-number 29)'),2)
        self.assertIn('(up-can-build-line 0 gl-shipyard-x c: shipyard)',generated)
        self.assertIn('(up-filter-distance c: -1 c: 10)',generated)
        self.assertIn('(up-path-distance gl-sy-w1-x 1 == 65535)',generated)
        self.assertIn('(up-path-distance gl-shipyard-x 0 < 64)',generated)

    def test_coast_rejection_diagnostics_identify_the_actual_gate(self):
        cases = []

        no_anchor = ShipyardFixture(); del no_anchor.objects[1]
        no_anchor.disabled.add(0)
        no_anchor.g.update({'gl-sy-stage': 1,
                            'shipyard-placement-state': no_anchor.val('SHIPYARD-ANCHOR'),
                            'gl-shipyard-x': 0, 'gl-shipyard-y': 0})
        cases.append((no_anchor, 61))

        bounds = ShipyardFixture(); bounds.objects[1]['point'] = (235, 50)
        cases.append((bounds, 62))

        memory = ShipyardFixture()
        memory.disabled.add(0)
        memory.g.update({'gl-sy-memory0-x': 52, 'gl-sy-memory0-y': 50,
                         'gl-sy-memory0-until': 1000})
        cases.append((memory, 63))

        unbuildable = ShipyardFixture(); unbuildable.can_site = lambda _point: False
        cases.append((unbuildable, 64))

        own_clearance = ShipyardFixture(); own_clearance.add(4, 'shipyard', (52, 50))
        cases.append((own_clearance, 65))

        allied_clearance = ShipyardFixture(); allied_clearance.add(
            4, 'shipyard', (52, 50), player=3)
        cases.append((allied_clearance, 66))

        water_exit = ShipyardFixture()
        water_exit.pathable = lambda obj, _point, exact: obj['id'] != 2 or not exact
        cases.append((water_exit, 67))

        for fixture, expected in cases:
            with self.subTest(reason=expected):
                sweeps = 4 if expected == 67 else 1
                for _ in range(sweeps):
                    fixture.sweep()
                self.assertEqual(fixture.builds, [])
                self.assertEqual(fixture.g['gl-sy-reason'], expected)
