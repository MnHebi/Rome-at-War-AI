"""Execute the emitted observer's supported PER subset, not an AoE2 emulator.

Proves private-state/list/pointer/command contracts in deterministic fixtures.
Does not prove native scheduling, object lifetime during a sweep or navigation.
"""
from copy import deepcopy
import json
import math
import re
import unittest

import generate_command_boundary as gen
from command_boundary_observations import decode, paired_progress, correlate
from validate_naval_doctrine import rule_blocks


def atoms(text):return re.findall(r'\(([^()]*)\)',text)


class Observer:
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
        self.rules=rule_blocks(gen.library(),diagnostic_view=False)

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
    def test_two_member_pair_tracks_actor_and_hull_separately(self):
        o=Observer();self.assertEqual(o.call(),[]) # quiet first observation
        o.time+=5;o.local=[3,2,1]
        o.objects[1]['precise-x']+=100;o.objects[20]['precise-x']+=300
        second=o.call()[0];members=second['members']
        self.assertEqual([m['actor'] for m in members],[1,2])
        self.assertEqual([m['index'] for m in members],[2,1])
        p=paired_progress(second,members[0])
        self.assertTrue(p['valid']);self.assertEqual(p['actor_displacement'],1)
        self.assertEqual(p['hull_displacement'],3)
        self.assertGreater(p['separation_after'],p['separation_before'])

    def test_stale_changed_hull_owner_and_unresolved_positions_are_unknown(self):
        for change in ['stale','owner','position','group']:
            o=Observer();o.call();o.time+=5
            if change=='stale':o.time+=20
            if change=='owner':o.objects[1]['player']=2
            if change=='position':o.objects[1]['precise-x']=-2
            if change=='group':o.objects[20]['group-flag']=0
            frame=o.call()[0]
            self.assertFalse(paired_progress(frame,frame['members'][0])['valid'],change)
        o=Observer();o.call();o.time+=5
        o.remote=[21];o.goals['gl-island-migration-transport-id']=21
        self.assertEqual(o.call(),[]) # new hull cannot pair against old hull
        self.assertEqual(o.goals[gen.g('p0-hull')],21)

    def test_missing_final_member_is_not_false_pair(self):
        o=Observer();o.call();o.time+=5;o.local=[3,2]
        f=o.call()[0]
        self.assertEqual(f['members'][0]['previous-member'],0)
        self.assertFalse(paired_progress(f,f['members'][0])['valid'])

    def test_unknown_after_bounded_search_and_rotation(self):
        o=Observer();o.local=list(range(100,140))
        for n in o.local:o.objects[n]=dict(o.objects[1],id=n)
        o.call();o.time+=5;o.local=o.local[2:]+o.local[:2]
        f=o.call()[0]
        self.assertEqual(f['members'][0]['previous-member'],-1)
        self.assertFalse(paired_progress(f,f['members'][0])['valid'])
        self.assertEqual(o.goals[gen.g('b-rotation')],2)

    def test_actual_resource_target_not_reserved_or_intended_goal(self):
        o=Observer();o.remote=[90];o.objects[90].update(type=69,**{'class':33,'player':0})
        f=o.call(2,111)[0]
        self.assertEqual((f['tid'],f['ttype'],f['tclass']),(90,69,33))
        self.assertNotEqual(f['tid'],f['reserved']);self.assertEqual(len(f['members']),1)
        self.assertEqual(f['modifier'],2)
        ev=dict(action='WORK',player_id=1,object_ids=[1,2,3],target_id=90,milliseconds=100000,sequence=100)
        r=correlate([f],[ev])[0]
        self.assertEqual(r['status'],'matching-packet')
        self.assertEqual(r['task_outcome'],'not-established-by-command-packet')
        ev['object_ids']=[2,3]
        self.assertEqual(correlate([f],[ev])[0]['status'],'unmatched-not-native-proof')

    def test_independent_quotas_empty_calls_late_game_and_output_maximum(self):
        o=Observer();o.local=[];o.call();self.assertEqual(o.goals[gen.g('b-left')],0)
        o.local=[1,2,3,4];o.objects[4]=dict(o.objects[1],id=4)
        self.assertEqual(o.call(site=21),[])
        for age in (3,12,20,28):o.time=100+age;self.assertEqual(len(o.call()),1)
        count=len(o.messages)
        for i in range(100):o.time=129;self.assertEqual(o.call(),[])
        self.assertEqual(len(o.messages),count)
        self.assertEqual(o.goals[gen.g('b-suppressed')],101)
        self.assertEqual(o.goals[gen.g('b-missed')],412)
        self.assertEqual(len(o.call(2,101)),1)
        o.time=7200;self.assertEqual(len(o.call()),1)
        # Header16 + end1 + two members(14 current +13 previous), all two lines.
        self.assertEqual(count,4*(16+1+2*(14+13))*2)
        r=Observer();r.call(2,101);self.assertEqual(len(r.messages),(16+1+14)*2)

    def test_duplicate_tracked_actor_not_double_counted_after_list_change(self):
        o=Observer();o.call();o.time+=5;o.local=[2]
        f=o.call()[0]
        self.assertEqual([m['actor'] for m in f['members']],[2])
        self.assertEqual(o.goals[gen.g('covered')],1)

    def test_pointer_lists_shared_goals_and_modifier_preserved_with_output_on_or_off(self):
        traces=[]
        for enabled in (0,1):
            o=Observer(enabled);o.pointer=90
            before=(deepcopy(o.local),deepcopy(o.remote),o.pointer,o.sn,
                    {k:v for k,v in o.goals.items() if not k.startswith(gen.PREFIX)})
            for i in range(7):
                o.time=100+i*4;o.call()
                self.assertEqual(before,(o.local,o.remote,o.pointer,o.sn,
                    {k:v for k,v in o.goals.items() if not k.startswith(gen.PREFIX)}))
            traces.append((tuple(o.local),tuple(o.remote),'action-garrison',-1,'stance-no-attack',o.sn))
        self.assertEqual(traces[0],traces[1])

    def test_invalid_pointer_and_multiple_targets_coverage(self):
        o=Observer();o.pointer=-1;o.call()
        self.assertEqual(o.pointer,-1);self.assertEqual(o.goals[gen.g('b-invalid')],1)
        self.assertEqual(o.messages,[])
        o.pointer=20;o.remote=[20,21];self.assertEqual(o.call(),[])
        o.time+=3;f=o.call()[0]
        self.assertEqual(o.goals[gen.g('b-targets')],1)
        self.assertFalse(paired_progress(f,f['members'][0])['valid'])

    def test_stale_objects_in_final_lists_are_not_substituted_by_pointer(self):
        o=Observer();o.local=[999];o.call();o.time+=3;f=o.call()[0]
        self.assertEqual(f['members'],[]);self.assertEqual(o.pointer,20)
        o=Observer();o.remote=[999];o.call();o.time+=3;f=o.call()[0]
        self.assertEqual(f['tid'],-2);self.assertEqual(o.pointer,20)
        self.assertFalse(paired_progress(f,f['members'][0])['valid'])

    def test_source_bridges_preserve_ordered_original_actions_and_are_tamper_evident(self):
        reg=json.loads(gen.REG.read_text())
        if reg.get('schema')==2:
            self.skipTest('Legacy chat bridge retired; all physical file bridges checked in test_command_boundary_file')
        self.assertEqual(len(reg['sites']),18)
        for s in reg['sites']:
            bridge=gen.render_site(s);actual=[]
            for _,_,_,_,a in rule_blocks(bridge,diagnostic_view=False):
                actual+=['('+x+')' for x in atoms(a) if gen.PREFIX not in x]
            self.assertEqual(actual,s['actions'],s['id'])
            self.assertEqual(gen.strip_source(bridge,reg),s['original'])
            with self.assertRaises(ValueError):gen.strip_source(bridge.replace('action-', 'altered-action-',1),reg)
        for name in gen.SOURCE_FILES:
            text=(gen.ROOT/name).read_text(encoding='utf-8-sig')
            physical=rule_blocks(text,diagnostic_view=False)
            self.assertGreater(len(physical),len(rule_blocks(text)))

    def test_no_list_mutators_shared_writers_or_new_strings_in_observer(self):
        if json.loads(gen.REG.read_text()).get('schema')==2:
            self.skipTest('Legacy chat support retired; file-mode private state and string budget checked separately')
        for name,text in gen.support().items():
            self.assertEqual((gen.ROOT/name).read_text(encoding='utf-8-sig'),text)
            self.assertNotIn('"',text)
            self.assertNotRegex(text,r'\((?:up-target-|up-find-|up-add-|up-remove-|up-reset-|up-full-|up-set-timer|set-strategic-number|up-modify-group)')
            for n in re.findall(r'\((?:set-goal|up-modify-goal) ([^ ]+)',text):self.assertTrue(n.startswith(gen.PREFIX))
        defs=gen.support()['rawai-command-boundary-defs.per']
        nums={n:int(v) for n,v in re.findall(r'\(defconst (\S+) (\d+)\)',defs)}
        for i,n in enumerate(['local','local-last','remote','remote-last']):
            self.assertEqual(nums[gen.g(n)],nums[gen.g('local')]+i)

    def test_natural_traversal_skips_library_and_direct_call_returns(self):
        o=Observer();o.pc=0;o.next_pc=1
        for s in atoms(o.rules[0][4]):o.action(s)
        self.assertEqual(o.goals[gen.g('entry')],2)
        self.assertEqual(o.next_pc,len(o.rules))
        o.call();self.assertEqual(o.pc,len(o.rules))

    def test_legacy_line_endings_preserved_without_reverting_text(self):
        old=b'a\r\nb\nc\r\n'
        self.assertEqual(gen.preserve_endings('a\nb\nx\nc\n',old),b'a\r\nb\nx\r\nc\r\n')

    def test_decoder_incomplete_frames_and_coverage_cross_player(self):
        def d(p,n,v,s):return dict(player=p,diag_id=gen.CODES[n],value=v,sequence=s,milliseconds=0)
        frames,c=decode([d(1,'site',24,1),d(2,'site',101,2),d(2,'serial',1,3),d(2,'end',1,4),
                         d(1,'site',24,5),d(2,'coverage-family',2,6),d(2,'calls',2,7),d(2,'invalid',0,8)])
        self.assertTrue(frames[0]['incomplete']);self.assertFalse(frames[1]['incomplete'])
        self.assertTrue(frames[2]['incomplete']);self.assertEqual(c[0]['calls'],2)


if __name__=='__main__':unittest.main()
