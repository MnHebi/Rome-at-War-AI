import unittest
from per_coastal_fixture import CoastalFixture
from generate_ranged_threat import generate
from test_pre_backlog import source

class Census(CoastalFixture):
    def __init__(self):
        super().__init__('rawai-reactive-ranged-threat.per','rawai-reactive-ranged-threat.per')
        self.sn['sn-focus-player-number']=7
    def action(self,e,pc=0):
        if e[0]=='up-get-search-state' and e[1]=='gl-reactive-ranged-local':
            for name,value in zip(('local','local-last','remote','remote-last'),(len(self.local),len(self.local),len(self.remote),len(self.remote))):
                self.g['gl-reactive-ranged-'+name]=value
        else: super().action(e,pc)

class RangedThreatTests(unittest.TestCase):
    def test_generated_and_private_output_layout(self):
        self.assertEqual(source('rawai-reactive-ranged-threat.per'),generate())
        c=Census()
        self.assertEqual([c.val('gl-reactive-ranged-'+n) for n in ('local','local-last','remote','remote-last')],list(range(15865,15869)))
    def test_threshold_per_enemy_and_class(self):
        for kind in ('archery-class','cavalry-archer-class'):
            for count in (0,2,3,8):
                c=Census()
                for i in range(count): c.add(100+i,kind,(50,50),player=6)
                c.sweep()
                self.assertEqual(c.g['gl-reactive-ranged-threat'],int(count>=3))
                self.assertEqual(c.sn['sn-focus-player-number'],7)
                self.assertEqual(c.remote,[])
    def test_no_pooling_allies_or_different_classes(self):
        c=Census(); c.players[6]['enemy']=False
        for i in range(4): c.add(100+i,'archery-class',(50,50),player=6)
        for i in range(2):
            c.add(200+i,'archery-class',(50,50),player=7)
            c.add(300+i,'cavalry-archer-class',(50,50),player=7)
        c.sweep(); self.assertEqual(c.g['gl-reactive-ranged-threat'],0)
    def test_refresh_clears_threat_and_no_commands(self):
        c=Census()
        for i in range(3):c.add(100+i,'archery-class',(50,50),player=6)
        c.sweep(); self.assertEqual(c.g['gl-reactive-ranged-threat'],1)
        c.objects.clear(); c.sweep(4); self.assertEqual(c.g['gl-reactive-ranged-threat'],1)
        c.sweep(1); self.assertEqual(c.g['gl-reactive-ranged-threat'],0)
        self.assertNotIn('up-target-',generate())
        self.assertNotIn('cc-players-unit-type-count',generate())
    def test_all_four_counter_rules_keep_existing_limits(self):
        for file in ('rawai-military-units-common.per','rawai-military-units-common-hard.per'):
            s=source(file)
            self.assertEqual(s.count('(goal gl-reactive-ranged-threat YES)'),2)
            self.assertNotIn('(players-unit-type-count any-enemy archery-class >= 3)',s)
            self.assertIn('(up-can-train gl-unitescrow-state c: skirmisher-line)',s)
            self.assertIn('(unit-type-count-total skirmisher-line g:< gl-five-percent)',s)
            self.assertIn('(food-amount > 150)',s)

if __name__=='__main__':unittest.main()
