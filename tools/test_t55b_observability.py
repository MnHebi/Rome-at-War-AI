"""T55B causal gaps: observe without changing command ownership or policy."""
import re
import unittest

from test_pre_backlog import source, expressions
from validate_naval_doctrine import rule_blocks
from test_assault_missions import Missions
from per_coastal_fixture import ShipyardFixture


class ObservabilityTests(unittest.TestCase):
    def test_economy_broadcast_and_explicit_modifier(self):
        text=source('rawai-homebase.per')
        self.assertNotIn('up-chat-data-to-self str-t12-diag', text)
        self.assertEqual(text.count('str-t12-diag-id c: 658'),2)
        self.assertEqual(text.count('(set-strategic-number sn-keystates 2)'),4)
        self.assertEqual(text.count('(set-strategic-number sn-keystates 0)'),4)

    def test_counters_do_not_gate_commands(self):
        text=source('rawai-homebase.per')
        commands=[r for r in rule_blocks(text) if 'sn-keystates 2' in r[4]]
        self.assertEqual(len(commands),4)
        for i,(_,_,_,facts,actions) in enumerate(commands,1):
            self.assertNotIn('gl-econ-retask-',facts)
            self.assertIn(f'(up-modify-goal gl-econ-retask-count{i} c:+ 1)',actions)
            self.assertIn('(set-strategic-number sn-keystates 2)\n\t(up-target-objects 0 action-default -1 stance-no-attack)\n\t(set-strategic-number sn-keystates 0)',actions)

    def test_summary_is_time_bounded_and_search_free(self):
        rows=[r for r in rule_blocks(source('rawai-homebase.per')) if 'str-t12-diag-id c: 659' in r[4]]
        self.assertEqual(len(rows),1)
        actions=expressions(rows[0][4])
        for a in actions:
            self.assertIn(a[0],('up-chat-data-to-all','up-modify-goal','set-goal'))
            if a[0]!='up-chat-data-to-all': self.assertTrue(a[1].startswith('gl-econ-retask-'))
        self.assertIn('gl-econ-retask-summary-next c:+ 300',rows[0][4])
        self.assertNotIn('gl-econ-retask-diag-armed',rows[0][3])
        self.assertIn('gl-econ-retask-unsampled',rows[0][4])

    def test_shipyard_rejection_observer_never_mutates_search_or_policy(self):
        rows=[r for r in rule_blocks(source('rawai-specialplacement.per')) if 'gl-sy-diag-site-next' in r[3]]
        self.assertEqual(len(rows),4)
        for r in rows:
            for a in expressions(r[4]):
                self.assertIn(a[0],('up-chat-data-to-all','up-get-fact','set-goal','up-modify-goal'))
                if a[0] in ('set-goal','up-modify-goal'): self.assertTrue(a[1].startswith('gl-sy-diag-'))
        self.assertIn('gl-sy-diag-site-next c:+ 60',rows[-1][4])

    def test_voyage_snapshot_uses_private_values_only(self):
        rows=[r for r in rule_blocks(source('rawai-assault-missions.per')) if 'str-t12-diag-id c: 680' in r[4]]
        self.assertEqual(len(rows),6)
        for _,_,_,facts,actions in rows:
            observer=actions.split('(set-goal')[0]
            for a in expressions(observer): self.assertEqual(a[0],'up-chat-data-to-all')
            self.assertNotIn('diag-left',facts)
            if '99999' in facts:
                self.assertRegex(facts,r'state\) 1|state 1')
                self.assertNotIn('state 4',facts)

    def test_quarantine_does_not_repeat_start_snapshot(self):
        m=Missions(); m.prepare(10,6); m.sweep()
        for _ in range(40): m.sweep(8)
        self.assertEqual(m.g['gl-am1-state'],4)
        count=len(m.commands)
        for _ in range(40): m.sweep(8)
        self.assertEqual(len(m.commands),count)

    def test_rejection_sampling_rearms_late_without_expanding_geometry(self):
        f=ShipyardFixture(); f.can_site=lambda p: False
        f.sweep()
        next_time=f.g['gl-sy-diag-site-next']
        self.assertGreater(next_time,f.now)
        for _ in range(10): f.sweep()
        self.assertEqual(f.g['gl-sy-diag-site-next'],next_time)
        f.now=6000; f.sweep()
        self.assertEqual(f.g['gl-sy-diag-site-next'],6060)
        self.assertEqual(f.builds,[])


if __name__=='__main__': unittest.main()
