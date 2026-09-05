import unittest
from per_coastal_fixture import CoastalFixture
from generate_naval_right_of_way import outputs
from test_pre_backlog import source


class Traffic(CoastalFixture):
    def __init__(self,active=True,count=1):
        super().__init__('rawai-naval-right-of-way.per','rawai-naval-row-defs.per')
        self.zone_at=lambda p:8
        self.add(10,'transport-ship',(80,80),cargo=10,flag=18,action='actionid-move',move_x=140,move_y=80,idle=0)
        self.add(90,'dock',(150,80),player=3)
        for i in range(count):
            self.add(20+i,'trade-cog-class',(81+i,81),action='actionid-trade' if active else 'actionid-idle',target=90,idle=0 if active else 1)

    def movements(self):
        return [c for c in self.commands if c[0] and c[1]=='action-move']

    def data(self,field,target=False):
        if field in ('object-data-move-x','object-data-move-y'):
            return self.objects[self.target].get(
                {'object-data-move-x':'move_x','object-data-move-y':'move_y'}[field],-1)
        return super().data(field,target)


class RightOfWayTests(unittest.TestCase):
    def test_generated(self):
        for name,text in outputs().items():self.assertEqual(source(name),text)

    def test_active_and_idle_merchants_yield_only_after_two_no_progress_samples(self):
        for active in (True,False):
            f=Traffic(active); f.sweep();f.sweep(8);self.assertEqual(f.movements(),[])
            f.sweep(8);self.assertEqual(len(f.movements()),1)
            self.assertEqual(f.movements()[0][0],(20,))
            self.assertEqual(f.objects[20]['flag'],-2)
            self.assertFalse(any(c[0]==(10,) for c in f.commands))

    def test_progress_and_intent_change_prevent_clearance(self):
        for field,value in (('point',(84,80)),('move_x',150),('cargo',0)):
            f=Traffic();f.sweep();f.sweep(8);f.objects[10][field]=value
            if field=='cargo':f.objects[10]['flag']=-2
            f.sweep(8);self.assertEqual(f.movements(),[])

    def test_choke_saturation_three_active_cogs_one_at_a_time(self):
        f=Traffic(count=5);f.sweep();f.sweep(8)
        for _ in range(3):
            before=len(f.movements());f.sweep(8)
            self.assertEqual(len(f.movements())-before,1)
            # The engine accepted the move; don't count fixture immobility as
            # native reacquisition. Other active merchants keep blocking.
            command=f.movements()[-1]
            for i in command[0]:f.objects[i].update(point=command[2],action='actionid-move',
                move_x=command[2][0],move_y=command[2][1])
        self.assertEqual({c[0] for c in f.movements()},{(20,),(21,),(22,)})
        for _ in range(10):f.sweep(8)
        self.assertEqual(len(f.movements()),3)

    def test_progress_stops_clearance_and_resumes_real_trade_target(self):
        f=Traffic(count=3);f.sweep();f.sweep(8);f.sweep(8)
        f.objects[20].update(action='actionid-move',point=f.movements()[0][2])
        f.objects[10]['point']=(85,80);f.sweep(8)
        self.assertEqual(len(f.movements()),1)
        self.assertTrue(any(c[0]==(20,) and c[1]=='action-default' and c[2]==('object',90) for c in f.commands))
        self.assertEqual(f.g['gl-row-active'],0)

    def test_cooldown_and_renewals_are_bounded_under_native_reacquisition(self):
        f=Traffic();f.sweep();f.sweep(8);f.sweep(8)
        for _ in range(14):f.sweep(8)
        self.assertLessEqual(len(f.movements()),4) # one initial + three maximum renewals
        self.assertFalse(any('action-stop' in c for c in f.commands))
        self.assertEqual(f.g['gl-row-m0-target'],-1)

    def test_native_fleet_move_override_repairs_same_merchant_before_advancing(self):
        f=Traffic(count=3);f.sweep();f.sweep(8);f.sweep(8)
        self.assertEqual([c[0] for c in f.movements()],[(20,)])
        hold=(f.g['gl-row-m0-x'],f.g['gl-row-m0-y'])
        # Runtime T41 issued the single-merchant hold, then native trade replaced
        # it in the same second with a fleet MOVE to a different destination.
        f.objects[20].update(action='actionid-move',move_x=1,move_y=143,idle=0)
        f.sweep(8)
        self.assertEqual([c[0] for c in f.movements()],[(20,),(20,)])
        self.assertEqual(f.movements()[-1][2],hold)
        self.assertEqual(f.g['gl-row-m0-renewals'],1)
        self.assertEqual(f.g['gl-row-m1-id'],-1)

    def test_correct_hold_destination_does_not_spam_renewal(self):
        f=Traffic(count=3);f.sweep();f.sweep(8);f.sweep(8)
        f.objects[20].update(action='actionid-move',
            move_x=f.g['gl-row-m0-x'],move_y=f.g['gl-row-m0-y'],idle=0)
        f.sweep(8)
        self.assertEqual(sum(c[0]==(20,) for c in f.movements()),1)
        self.assertEqual(f.g['gl-row-m0-renewals'],0)
        self.assertTrue(any(c[0]==(21,) for c in f.movements()))

    def test_wrong_zone_hostile_holding_and_unreachable_point_rejected(self):
        for case in ('zone','path','castle','town-center','sea-tower'):
            f=Traffic()
            if case=='zone':f.zone_at=lambda p:3
            if case=='path':f.pathable=lambda o,p,exact:False
            if case in ('castle','town-center','sea-tower'):f.add(100,case,(81,81),player=7)
            f.sweep();f.sweep(8);f.sweep(8)
            self.assertEqual(f.movements(),[],case)

    def test_distant_owned_or_enemy_merchants_untouched(self):
        for changes in ({'point':(100,100)},{'flag':3},{'player':3},{'under_attack':1},{'zone':3}):
            f=Traffic();f.objects[20].update(changes)
            f.sweep();f.sweep(8);f.sweep(8);self.assertEqual(f.movements(),[],changes)

    def test_active_mission_warship_after_transports_and_no_firing_interference(self):
        for moving in (True,False):
            f=Traffic();f.objects[10].update(type='warship-class',cls='warship-class',cargo=0,
                action='actionid-move' if moving else 'actionid-attack')
            f.sweep();f.sweep(8);f.sweep(8)
            self.assertEqual(len(f.movements()),1 if moving else 0)

    def test_loaded_unload_and_boarding_transport_intent_can_clear(self):
        for action,cargo in (('actionid-transport',0),('actionid-unload',10)):
            f=Traffic();f.objects[10].update(action=action,cargo=cargo)
            f.sweep();f.sweep(8);f.sweep(8);self.assertEqual(len(f.movements()),1)

    def test_hold_lost_ownership_and_enemy_dock_never_retasked(self):
        for changed in ('merchant','dock'):
            f=Traffic();f.sweep();f.sweep(8);f.sweep(8)
            f.objects[20]['action']='actionid-move'
            f.objects[20 if changed=='merchant' else 90]['player']=7
            f.objects[10]['point']=(86,80);n=len(f.commands);f.sweep(8)
            self.assertEqual(f.commands[n:],[])
