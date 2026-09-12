import json
import unittest

import generate_command_boundary as gen
from boarding_sampling import FIXTURE, Schedule, demonstrate
from test_command_boundary import Observer
from command_boundary_observations import paired_progress


class BoardingSamplingTests(unittest.TestCase):
    def test_historical_schedule_model_matches_actual_generated_PER(self):
        for case in json.loads(FIXTURE.read_text())['cases']:
            for exhausted in (False,True):
                o=Observer();s=Schedule(exhausted_until=case['calls'][0]['ms']//1000+180 if exhausted else 0)
                if exhausted:o.goals[gen.g('b-next')]=s.next
                frames=[]
                # Synthetic known lists test scheduling only, not historical actor coverage.
                for c in case['calls']:
                    o.time=c['ms']//1000
                    expected=s.call(o.time,c['schedule_site'],20)
                    actual=o.call(site=c['schedule_site'])
                    self.assertEqual(bool(actual),bool(expected),(case['name'],c['ms'],exhausted))
                    self.assertEqual(o.goals[gen.g('b-left')],s.left)
                    if actual:frames.append(c['ms'])
                self.assertEqual(frames,[r['ms'] for r in demonstrate(case,exhausted)['reserved']])

    def test_late_reports_are_reserved_without_increasing_cap(self):
        cases={c['name']:c for c in json.loads(FIXTURE.read_text())['cases']}
        yellow=demonstrate(cases['T56-Yellow'])
        self.assertEqual([r['ms'] for r in yellow['old']],[2205076,2208887,2212704,2215980])
        self.assertEqual([r['ms'] for r in yellow['reserved']],[2208887,2222525,2229065,2238884])
        red=demonstrate(cases['T56-Red'])
        self.assertEqual([r['ms'] for r in red['reserved']],[3680598,3710858,3717502])
        for c in cases.values():
            self.assertLessEqual(len(demonstrate(c)['reserved']),4)
            self.assertEqual(demonstrate(c,True)['reserved'],[])

    def test_invocation_without_packet_and_missing_historical_state_stay_explicit(self):
        cases={c['name']:c for c in json.loads(FIXTURE.read_text())['cases']}
        yellow=cases['T56-Yellow']
        invocation=next(c for c in yellow['calls'] if c['ms']==2212704)
        self.assertEqual(invocation['site'],23)
        self.assertIsNone(invocation['packet_members'])
        self.assertIsNone(invocation['packet_sequence'])
        green=demonstrate(cases['T56-Green'])['reserved']
        self.assertEqual([r['ms'] for r in green],[3620817]) # no exact immediate pre-onset report
        for c in cases.values():
            for r in demonstrate(c)['reserved']:
                self.assertEqual(r['final_PER_selection'],'unknown')
        self.assertTrue(all(c['site'] is None for c in cases['T55B-Cyan']['calls']))

    def test_quiet_capture_preserves_recent_pair_until_late_report(self):
        o=Observer();self.assertEqual(o.call(site=21),[])
        o.time=103;self.assertEqual(len(o.call()),1)
        for t in (106,109):o.time=t;self.assertEqual(o.call(),[])
        o.time=112;o.objects[3]['precise-x']+=200;o.objects[20]['precise-x']+=100
        frame=o.call()[0];pair=paired_progress(frame,frame['members'][0])
        self.assertTrue(pair['valid'])
        self.assertEqual(frame['members'][0]['previous-time'],109)
        self.assertEqual(pair['actor_displacement'],2)
        self.assertEqual(pair['hull_displacement'],1)

    def test_travel_cannot_spend_late_credits_and_new_hull_cannot_refill(self):
        o=Observer();o.call(site=20);o.time=103;o.call(site=25)
        for t in (110,120,130,140):o.time=t;self.assertEqual(o.call(site=25),[])
        self.assertEqual(o.goals[gen.g('b-left')],3)
        o.time=145;o.call(site=21)
        o.time=160;self.assertEqual(o.call(site=25),[]) # even stale local-phase anchor
        for t in (163,166,175):o.time=t;self.assertEqual(len(o.call()),1)
        self.assertEqual(o.goals[gen.g('b-left')],0)
        o.goals['gl-island-migration-transport-id']=21;o.remote=[21]
        o.time=180;o.call(site=20);o.time=183;self.assertEqual(o.call(site=21),[])
        self.assertEqual(o.goals[gen.g('b-left')],0)

    def test_unobserved_intermediate_renewal_does_not_consume_future_tier(self):
        o=Observer();o.call(site=20);o.time=103;o.call(site=21)
        for t in (106,109):o.time=t;self.assertEqual(o.call(site=24),[])
        self.assertEqual(o.goals[gen.g('b-left')],3)
        o.time=115;self.assertEqual(len(o.call(site=24)),1)
        self.assertEqual(o.goals[gen.g('b-left')],2)


if __name__=='__main__':unittest.main()
