import unittest
from per_coastal_fixture import CoastalFixture
from test_pre_backlog import source
from validate_naval_doctrine import rule_blocks
from generate_expedition_admission import outputs
from test_assault_preparation import Admission
from test_assault_rendezvous import Rendezvous
from test_assault_missions import Missions, GROUPS


class Expedition(CoastalFixture):
    def __init__(self):
        super().__init__('rawai-expedition-admission.per','rawai-expedition-defs.per')
        self.g.update({'gl-home-zone':3,'gl-home-anchor-x':40,'gl-home-anchor-y':40,
            'gl-ap-seed-enemy':6,'naval-superiority':self.val('EQUAL')})
        self.counts={'transport-ship':2,'warship-class':4}
        self.add(1,'villager-class',(40,40),zone=3)
        self.add(2,'town-center',(140,140),zone=4,player=6)
        self.pathable=lambda o,p,exact:False

    def settled(self):
        self.sweep();self.sweep(180)
        return self


class ExpeditionTests(unittest.TestCase):
    def test_generated(self):
        for name,text in outputs().items():self.assertEqual(source(name),text)

    def test_safe_isolated_inferior_player_admits_but_old_normal_gate_survives(self):
        e=Expedition().settled();self.assertEqual(e.g['gl-exp-allowed'],1)
        for inferior,allowed,expected in ((True,1,True),(True,0,False),(False,0,True)):
            f=Admission();f.g.update({'military-superiority':0 if inferior else 2,'gl-exp-allowed':allowed})
            f.sweep()
            self.assertEqual(f.g['gl-transport-route-state']==f.val('TRANSPORT-ROUTE-MANIFEST-FIND'),expected)

    def test_safe_dwell_resets_on_actual_or_latched_home_attack(self):
        for flag in ('gl-home-defense-state','gl-self-attack-verified'):
            e=Expedition();e.sweep();e.sweep(179);self.assertEqual(e.g['gl-exp-allowed'],0)
            e.g[flag]=1;e.sweep(1);self.assertEqual(e.g['gl-exp-allowed'],0)
            e.g[flag]=0;e.sweep(179);self.assertEqual(e.g['gl-exp-allowed'],0)
            e.sweep(1);self.assertEqual(e.g['gl-exp-allowed'],1)

    def test_known_reachable_land_enemy_blocks_even_across_zone_boundary(self):
        for same_zone in (True,False):
            e=Expedition()
            if same_zone:e.objects[2]['zone']=3
            else:e.pathable=lambda o,p,exact:True
            e.settled();self.assertEqual(e.g['gl-exp-allowed'],0)

    def test_naval_pressure_inferiority_missing_workers_or_hulls_close_exception(self):
        for case in ('pressure','inferior','worker','hull','warship'):
            e=Expedition()
            if case=='pressure':e.add(9,'transport-ship',(60,40),player=7)
            if case=='inferior':e.g['naval-superiority']=0
            if case=='worker':del e.objects[1]
            if case=='hull':e.counts['transport-ship']=0
            if case=='warship':e.counts['warship-class']=1
            e.settled();self.assertEqual(e.g['gl-exp-allowed'],0,case)

    def test_home_zone_veto_is_not_limited_to_four_path_samples(self):
        e=Expedition()
        for i in range(4):e.add(20+i,'town-center',(50+i,50),zone=4,player=6)
        e.add(30,'infantry-class',(180,180),zone=3,player=6)
        e.settled();self.assertEqual(e.g['gl-exp-allowed'],0)

    def test_safety_lease_expires_and_focus_is_restored(self):
        e=Expedition();e.sn['sn-focus-player-number']=4;e.settled()
        self.assertEqual(e.sn['sn-focus-player-number'],4)
        e.g['gl-home-zone']=-1;e.sweep(36);self.assertEqual(e.g['gl-exp-allowed'],0)

    def manifest(self,count,naval=2,siege=False):
        e=Expedition().settled()
        e.rules=list(rule_blocks(source('rawai-expedition-budget.per')))
        e.disabled=set()
        e.g.update({'gl-transport-route-state':e.val('TRANSPORT-ROUTE-MANIFEST-FIND'),
            'gl-exp-manifest-limit':10,'gl-exp-siege-keep':-1,'naval-superiority':naval})
        for i in range(count):
            kind='siege-weapon-class' if siege and i<2 else 'infantry-class'
            e.add(100+i,kind,(40+i/10,40),zone=3)
        e.sweep()
        return e

    def test_only_surplus_is_exposed_and_sea_control_scales_reserve(self):
        for count,naval,limit,reserve in ((12,2,0,12),(16,2,4,12),(24,2,10,12),(80,2,10,20),
                                        (24,1,4,20),(60,1,5,30)):
            e=self.manifest(count,naval)
            self.assertEqual((e.g['gl-exp-manifest-limit'],e.g['gl-exp-reserve']),(limit,reserve))

    def test_mixed_manifest_keeps_one_free_siege_and_never_counts_owned_passengers(self):
        e=self.manifest(32,siege=True)
        self.assertEqual(e.g['gl-exp-siege-keep'],100)
        e.objects[110]['flag']=18;e.objects[111]['garrisoned']=1;e.objects[112]['idle']=0
        e.g['gl-exp-manifest-limit']=10;e.sweep()
        self.assertEqual(e.g['gl-exp-free'],29-12)
        # Exercise the integrated selector, not just the budget's arithmetic.
        m=Rendezvous(passenger_count=32)
        m.g.update({'gl-exp-allowed':1,'naval-superiority':2})
        m.objects[100]['cls']='siege-weapon-class';m.objects[101]['cls']='siege-weapon-class'
        text=source('rawai-military.per').replace('(load "rawai-expedition-budget")',source('rawai-expedition-budget.per'))
        from test_assault_rendezvous import STATES
        m.rules=[r for r in rule_blocks(text) if 'gl-transport-load-clock)' in r[4] or any(s in r[3] for s in STATES)]
        # Missions fixture needs only the newly used integer reserve arithmetic.
        original=m.action
        def arithmetic(e,pc=0):
            if e[0]=='up-modify-goal' and e[2] in ('c:/','c:max'):
                m.g[e[1]]=int(m.g.get(e[1],0)/int(e[3])) if e[2]=='c:/' else max(m.g.get(e[1],0),int(e[3]))
                return 0
            return original(e,pc)
        m.action=arithmetic;m.finish_preparation_step()
        owned=m.groups[m.val('attack-boarding-group')]
        self.assertEqual(len(owned),10);self.assertNotIn(100,owned);self.assertIn(101,owned)

    def test_three_existing_slots_and_one_second_preparation_reuse_preserved(self):
        self.assertEqual(GROUPS,(0,18,19))
        m=Missions()
        for hull in (10,11,12):m.prepare(hull);m.sweep()
        self.assertEqual({m.g[f'gl-am{i}-hull'] for i in range(1,4)},{10,11,12})
        self.assertTrue(all(m.g[f'gl-am{i}-state']==1 for i in range(1,4)))
        m.g['gl-am2-state']=0;m.prepare(13);m.sweep()
        self.assertEqual(m.g['gl-am2-hull'],13)
        self.assertEqual((m.g['gl-am1-hull'],m.g['gl-am3-hull']),(10,12))
        self.assertIn('(up-set-timer c: t-transport-route c: 1)',source('rawai-assault-missions.per'))

    def test_no_new_planner_and_failed_shore_validation_retained(self):
        script=source('rawai-expedition-admission.per')+source('rawai-expedition-budget.per')
        for forbidden in ('up-target-','up-create-group','up-modify-group-flag','set-strategic-number sn-target-player-number'):
            self.assertNotIn(forbidden,script)
        # Repeated successful campaigns retain their existing preferred opponent;
        # no new cached beach bypasses fresh screening/failed-sector validation.
        self.assertIn('gl-ap-preferred-enemy',source('rawai-assault-admission.per'))
        self.assertIn('gl-ap-memory16-until',source('rawai-assault-plans.per'))
