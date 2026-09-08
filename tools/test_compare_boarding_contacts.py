import unittest
from compare_boarding_contacts import compare


def e(ms,seq,action='SPECIAL',order=5,actors=(1,),p=1,target=20):
    return dict(milliseconds=ms,sequence=seq,action=action,order_id=order,
                object_ids=list(actors),player_id=p,target_id=target,offset=seq)


class ContactTests(unittest.TestCase):
    def run_case(self,events):return compare(events,{(1,1),(1,2)},{(1,20),(1,21)})

    def test_first_repeat_different_and_counts(self):
        r=self.run_case([e(0,1,actors=(1,2,2)),e(10,2),e(20,3,target=21),e(60000,4,'CHAT')])
        self.assertEqual((r['unique_packets'],r['actor_incidences']),(3,4))
        self.assertEqual([x['kind'] for x in r['contacts']],['first-observed-hull','first-observed-hull','same-hull-renewal','different-hull'])

    def test_unknown_actor_hull_and_wrong_player_excluded(self):
        r=self.run_case([e(0,1,p=2),e(1,2,target=99),e(2,3,actors=(99,)),e(60000,4,'CHAT')])
        self.assertEqual(r['contacts'],[])
        self.assertEqual(r['exclusions']['unresolved_actor_or_hull'],3)

    def test_followup_censor_and_isolated_packet(self):
        r=self.run_case([e(0,1),e(10,2,'AI_ORDER',706),e(20000,3)])
        self.assertTrue(all(c['outcome']=='censored' for c in r['contacts']))
        r=self.run_case([e(0,1),e(10,2,'AI_ORDER',706),e(60000,3,'CHAT')])
        self.assertEqual(r['contacts'][0]['outcome'],'isolated706-only')

    def test_active_onset_and_window_boundary(self):
        events=[e(0,1)]+[e(1000+i*13,2+i,'AI_ORDER',706) for i in range(110)]+[e(1100,999),e(60000,1000,'CHAT')]
        r=self.run_case(events)
        self.assertEqual([c['outcome'] for c in r['contacts']],['sustained-onset','already-active'])

    def test_delete_censors_negative_control(self):
        r=self.run_case([e(0,1),e(100,2,'DELETE'),e(60000,3,'CHAT')])
        self.assertEqual(r['contacts'][0]['outcome'],'censored')

    def test_replay_survival_does_not_prove_actor_survival(self):
        r=self.run_case([e(0,1),e(2000,2,'WORK'),e(60000,3,'CHAT',actors=())])
        self.assertEqual(r['contacts'][0]['outcome'],'censored')
