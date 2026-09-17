"""Execute the emitted observer's supported PER subset, not an AoE2 emulator.

Proves private-state/list/pointer/command contracts in deterministic fixtures
and decodes explicit historical record fixtures; the retired chat emitter is
neither generated nor executed here. Does not prove native scheduling, object
lifetime during a sweep or navigation.
"""
import math
import re
import unittest

import generate_command_boundary as gen
from command_boundary_observations import decode, paired_progress, correlate, frame_integrity


def atoms(text):return re.findall(r'\(([^()]*)\)',text)


PREV_FIELDS=('actor','hull','time','x','y','hx','hy','owner','group','howner','hgroup')


def record(player,label,value,sequence=0,milliseconds=100000):
    return dict(player=player,diag_id=gen.CODES[label],value=value,
                sequence=sequence,milliseconds=milliseconds)


def pair_records(player=2,site=24,serial=1,milliseconds=100000,end=None,frame=None,
                 member=None,drop=()):
    """Explicit historical record stream for one complete actor/hull pair.

    The decoder contract is exercised from recorded fields, not from executing
    the retired chat scheduler library. Overrides mutate the decoded frame or
    its single member so negative cases stay readable.
    """
    f=dict(site=site,serial=serial,now=100,modifier=2,local=1,remote=1,stage=4,
           reserved=20,tid=20,ttype=545,tclass=20,tx=6000,ty=5000,towner=player,tgroup=10)
    m=dict(index=0,actor=1,atype=83,aclass=4,ax=5900,ay=5000,owner=player,group=11,
           action=6,order=5,intent=1,garrison=0,carry=0,elapsed=5,**{'previous-member':1})
    for name,value in zip(PREV_FIELDS,(1,20,95,5000,5000,6000,5000,player,11,player,10)):
        m['previous-'+name]=value
    f.update(frame or {});m.update(member or {})
    for name in drop:
        f.pop(name,None);m.pop(name,None)
    rows=[record(player,k,v,milliseconds=milliseconds) for k,v in f.items()]
    rows+=[record(player,k,v,milliseconds=milliseconds) for k,v in m.items()]
    rows.append(record(player,'end',serial if end is None else end,milliseconds=milliseconds))
    return rows


class Observer:
    """Execution helper for the current file-mode library.

    FileObserver replaces `rules` with the emitted file-trace library; the
    retired chat library is no longer constructed here.
    """
    def __init__(self,enabled=1):
        self.goals={gen.g(n):(-2 if n.startswith('p') and '-' in n else 0) for n in gen.NAMES}
        self.goals[gen.g('enabled')]=enabled
        self.goals.update({'gl-island-migration-state':4,'gl-island-migration-transport-id':20})
        self.sn=2;self.pointer=20;self.local=[1,2,3];self.remote=[20]
        self.objects={}
        for n in [1,2,3,20,21,90]:
            self.objects[n]={'id':n,'type':83 if n<10 else 545,'class':4 if n<10 else 20,
                'precise-x':100*n,'precise-y':100,'player':1,'group-flag':11 if n<10 else 10,
                'action':6,'order':5,'target-id':20,'garrisoned':0,'carry':0}
        self.time=100;self.messages=[];self.steps=0;self.pc=0

    def value(self,v):
        try:return int(v)
        except ValueError:return self.goals[v]

    def fact(self,s):
        a=s.split();op=a[0]
        if op=='true':return True
        if op=='false':return False
        if op=='goal':return self.goals[a[1]]==int(a[2])
        if op=='up-set-target-object':
            seq=self.local if a[1]=='search-local' else self.remote;idx=self.value(a[3])
            valid=0<=idx<len(seq) and seq[idx] in self.objects
            if valid:self.pointer=seq[idx]
            return valid
        if op=='up-compare-goal':
            left=self.goals[a[1]];right=self.value(a[3]);cmp=a[2].split(':')[1]
            return {'>':left>right,'>=':left>=right,'<':left<right,'<=':left<=right,
                    '==':left==right,'!=':left!=right}[cmp]
        raise AssertionError('Unknown observer fact '+s)

    def action(self,s):
        a=s.split();op=a[0]
        if op=='set-goal':self.goals[a[1]]=int(a[2])
        elif op=='up-modify-goal':
            mode,operator=a[2].split(':');v=self.sn if mode=='s' else self.value(a[3])
            if operator=='=':self.goals[a[1]]=v
            elif operator=='+':self.goals[a[1]]+=v
            elif operator=='-':self.goals[a[1]]-=v
            else:raise AssertionError(s)
        elif op=='up-get-rule-id':self.goals[a[1]]=self.pc
        elif op=='up-jump-rule':self.next_pc=self.pc+int(a[1])+1
        elif op=='up-jump-direct':self.next_pc=self.value(a[2])
        elif op=='up-get-fact':
            assert a[1:3]==['game-time','0'];self.goals[a[3]]=self.time
        elif op=='up-get-search-state':
            assert a[1]==gen.g('local')
            for n,v in zip(['local','local-last','remote','remote-last'],[len(self.local),0,len(self.remote),0]):self.goals[gen.g(n)]=v
        elif op=='up-get-object-data':self.goals[a[2]]=self.objects.get(self.pointer,{}).get(a[1].removeprefix('object-data-'),-2)
        elif op=='up-set-target-object':
            seq=self.local if a[1]=='search-local' else self.remote;idx=self.value(a[3])
            if 0<=idx<len(seq) and seq[idx] in self.objects:self.pointer=seq[idx]
        elif op=='up-set-target-by-id':
            n=self.value(a[2])
            if n in self.objects:self.pointer=n
        elif op=='up-get-point-distance':
            self.goals[a[3]]=int(math.hypot(self.goals[a[1]]-self.goals[a[2]],
                self.goals[a[1].replace('-ax','-ay')]-self.goals[a[2].replace('-tx','-ty')]))
        elif op=='up-chat-data-to-all':self.messages.append((a[1],self.value(a[3])))
        elif op=='do-nothing':pass
        else:raise AssertionError('Unknown observer action '+s)

    def call(self,family=1,site=24):
        self.goals[gen.g('family')]=family;self.goals[gen.g('site')]=site
        self.goals[gen.g('return')]=len(self.rules)
        self.pc=2;before=len(self.messages)
        while self.pc<len(self.rules):
            self.steps+=1
            if self.steps>50000:raise AssertionError('Unbounded observer loop')
            self.next_pc=self.pc+1
            _,_,_,facts,actions=self.rules[self.pc]
            if all(self.fact(s) for s in atoms(facts)):
                for s in atoms(actions):self.action(s)
            self.pc=self.next_pc
        pairs=[];pending=None
        for label,v in self.messages[before:]:
            if label=='str-t12-diag-id':pending=v
            else:
                assert pending is not None
                pairs.append(dict(player=1,diag_id=pending,value=v,sequence=len(pairs),milliseconds=self.time*1000))
                pending=None
        return decode(pairs)[0]


class CommandBoundaryTests(unittest.TestCase):
    def test_pair_tracks_actor_and_hull_displacement_separately(self):
        frames,_=decode(pair_records())
        self.assertEqual(len(frames),1);self.assertFalse(frames[0]['incomplete'])
        pair=paired_progress(frames[0],frames[0]['members'][0])
        self.assertTrue(pair['valid'],pair)
        self.assertEqual(pair['actor_displacement'],9)
        self.assertEqual(pair['hull_displacement'],0)
        self.assertEqual(pair['separation_before'],10)
        self.assertEqual(pair['separation_after'],1)

    def test_unverifiable_pairs_name_the_failed_condition(self):
        cases=(('stale',dict(member={'elapsed':0}),'stale-or-same-time'),
               ('time-mismatch',dict(member={'previous-time':94}),'time-mismatch'),
               ('actor-changed',dict(member={'previous-actor':2}),'identity-changed'),
               ('hull-changed',dict(frame={'tid':21}),'not-exact-reserved-hull'),
               ('more-than-one-target',dict(frame={'remote':2}),'not-exact-reserved-hull'),
               ('passenger-owner',dict(member={'owner':3}),'passenger-ownership'),
               ('passenger-group',dict(member={'group':10}),'passenger-ownership'),
               ('hull-owner',dict(frame={'towner':1}),'hull-ownership'),
               ('hull-group',dict(frame={'tgroup':11}),'hull-ownership'),
               ('not-final-member',dict(member={'previous-member':0}),'no-final-membership-proof'),
               ('invalid-position',dict(member={'ax':-1}),'invalid-position'))
        for name,change,reason in cases:
            with self.subTest(case=name):
                frames,_=decode(pair_records(**change))
                pair=paired_progress(frames[0],frames[0]['members'][0])
                self.assertFalse(pair['valid'],name)
                self.assertIn(reason,pair['reasons'],name)

    def test_incomplete_frame_or_missing_member_field_is_not_a_pair(self):
        frames,_=decode(pair_records(end=7))
        self.assertTrue(frames[0]['incomplete'])
        self.assertEqual(paired_progress(frames[0],frames[0]['members'][0]),
                         dict(valid=False,reasons=['incomplete-pair']))
        frames,_=decode(pair_records(drop=('actor',)))
        self.assertFalse(frames[0]['incomplete'])
        self.assertEqual(paired_progress(frames[0],frames[0]['members'][0]),
                         dict(valid=False,reasons=['incomplete-pair']))

    def test_packet_attribution_requires_recorded_actor_and_target(self):
        frames,_=decode(pair_records())
        event=dict(action='WORK',player_id=2,object_ids=[1,2,3],target_id=20,
                   milliseconds=100000,sequence=100)
        row=correlate(frames,[event])[0]
        self.assertEqual(row['status'],'matching-packet')
        self.assertEqual(row['packet_sequences'],[100])
        self.assertEqual(row['task_outcome'],'not-established-by-command-packet')
        event['object_ids']=[2,3]
        self.assertEqual(correlate(frames,[event])[0]['status'],'unmatched-not-native-proof')
        event['object_ids']=[1];event['target_id']=21
        self.assertEqual(correlate(frames,[event])[0]['status'],'unmatched-not-native-proof')

    def test_legacy_line_endings_preserved_without_reverting_text(self):
        old=b'a\r\nb\nc\r\n'
        self.assertEqual(gen.preserve_endings('a\nb\nx\nc\n',old),b'a\r\nb\nx\r\nc\r\n')

    def test_decoder_incomplete_frames_and_coverage_cross_player(self):
        def d(p,n,v,s):return dict(player=p,diag_id=gen.CODES[n],value=v,sequence=s,milliseconds=0)
        frames,c=decode([d(1,'site',24,1),d(2,'site',101,2),d(2,'serial',1,3),d(2,'end',1,4),
                         d(1,'site',24,5),d(2,'coverage-family',2,6),d(2,'calls',2,7),d(2,'invalid',0,8)])
        self.assertTrue(frames[0]['incomplete']);self.assertFalse(frames[1]['incomplete'])
        self.assertTrue(frames[2]['incomplete']);self.assertEqual(c[0]['calls'],2)

    def test_orphan_end_is_visible_without_fabricating_frame(self):
        # T57 contains609 such ends, but no720 headers. Preserve uncertainty.
        pairs=[dict(player=8,diag_id=gen.CODES[n],value=v,sequence=i,milliseconds=0)
               for i,(n,v) in enumerate([('actor',34455),('owner',8),('end',12)])]
        frames,_=decode(pairs)
        self.assertEqual(frames,[])
        self.assertEqual(frame_integrity(pairs)['counts']['orphan_ends'],1)

    def test_integrity_separates_players_and_broken_serials(self):
        pairs=[dict(player=p,diag_id=gen.CODES[n],value=v) for p,n,v in
               [(1,'site',24),(2,'site',101),(1,'serial',4),(2,'end',7),
                (1,'end',4),(3,'site',23),(3,'site',24)]]
        counts=frame_integrity(pairs)['counts']
        self.assertEqual(counts['starts'],4)
        self.assertEqual(counts['ends'],2)
        self.assertEqual(counts['serial_mismatches'],1)
        self.assertEqual(counts['abandoned_headers'],1)
        self.assertEqual(counts['unclosed_headers'],1)


if __name__=='__main__':unittest.main()
