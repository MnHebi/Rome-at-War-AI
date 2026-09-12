"""Physical emitted file-mode fixtures, including imperfect delivery.

Not an engine emulator or proof of DE file delivery/scheduling performance.
"""
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import re
import tempfile
import unittest

import command_boundary_file as f
import command_boundary_log as log
import generate_command_boundary as cb
from test_command_boundary import Observer,atoms
from validate_naval_doctrine import rule_blocks
from test_pre_backlog import expressions


class FileObserver(Observer):
    def __init__(self,mode=1):
        super().__init__()
        self.rules=rule_blocks(f.library(),diagnostic_view=False)
        self.const={'my-player-number':1,'migration-boarding-group':11}
        self.const.update({f.g(n):f.BASE+i for i,n in enumerate(f.NAMES)})
        self.ids={v:k for k,v in self.const.items() if k.startswith(f.PREFIX)}
        self.goals.update({f.g(n):0 for n in f.NAMES})
        self.goals[f.g('mode')]=mode;self.goals[f.g('start')]=10001
        self.goals[f.g('player')]=1
        self.indirect={i:-2 for i in range(f.ROSTER_BASE,f.ROSTER_BASE+f.ROSTER*f.STRIDE)}
        self.settings={s:0 for s in f.SETTINGS};self.settings['sn-keystates']=2
        self.lines=[]

    def value(self,x):
        if x in self.goals:return self.goals[x]
        if x in self.const:return self.const[x]
        return int(x)

    def fact(self,s):
        a=s.split()
        if a[0]=='goal':return self.value(a[1])==self.value(a[2])
        if a[0]=='up-compare-const':
            return self.const[a[1]]==self.value(a[3])
        if a[0]=='up-set-target-by-id':
            n=self.value(a[2])
            if n not in self.objects:return False
            self.pointer=n;return True
        return super().fact(s)

    def action(self,s):
        a=s.split();op=a[0]
        if op=='set-goal':self.goals[a[1]]=self.value(a[2])
        elif op=='up-modify-goal':
            mode,oper=a[2].split(':');v=self.settings[a[3]] if mode=='s' else self.value(a[3])
            old=self.goals[a[1]]
            self.goals[a[1]]={'=':lambda:v,'+':lambda:old+v,'-':lambda:old-v,'*':lambda:old*v,
                             'mod':lambda:old%v}[oper]()
        elif op=='up-get-search-state':
            for name,v in zip(['local','local-last','remote','remote-last'],[len(self.local),0,len(self.remote),0]):
                self.goals[f.g(name)]=v
        elif op=='up-get-object-target-data':
            target=self.objects.get(self.pointer,{}).get('target-id')
            self.goals[a[2]]=self.objects.get(target,{}).get(a[1].removeprefix('object-data-'),-2)
        elif op=='up-log-data':
            player=int(a[2].removeprefix('str-cbf-p'))
            self.lines.append(f'engine unrelated prefix RAW58P{player} {self.value(a[4])}\n')
        elif op=='up-get-indirect-goal':self.goals[a[3]]=self.indirect[self.value(a[2])]
        elif op=='up-set-indirect-goal':self.indirect[self.value(a[2])]=self.value(a[4])
        elif op=='up-chat-data-to-all':pass
        else:super().action(s)

    def call(self,kind=1):
        self.goals[f.g('kind')]=kind;self.goals[f.g('site')]=1001
        self.goals[f.g('return')]=len(self.rules);self.pc=2;self.steps=0
        begin=len(self.lines)
        while self.pc<len(self.rules):
            self.steps+=1
            if self.steps>2000000:raise AssertionError('unbounded physical observer')
            self.next_pc=self.pc+1
            *_,facts,actions=self.rules[self.pc]
            def evaluate(e):
                if e[0]=='or':return any(evaluate(x) for x in e[1:])
                return self.fact(' '.join(e))
            if all(evaluate(e) for e in expressions(facts)):
                for s in atoms(actions):self.action(s)
            self.pc=self.next_pc
        return self.lines[begin:]


def decode(lines):
    with tempfile.TemporaryDirectory() as d:
        p=Path(d)/'engine.log';p.write_text(''.join(lines));stats=Counter()
        return list(log.decode_logs([p],stats)),stats


class FileTraceTests(unittest.TestCase):
    def test_bootstrap_uses_player_constant_not_fact_id_for_all_players(self):
        # Previous fixtures injected player=1 and never executed bootstrap.
        # Exercise the emitted initialization, including its private resets.
        for player in range(1,9):
            o=FileObserver();o.const['my-player-number']=player
            before=(o.pointer,list(o.local),list(o.remote),deepcopy(o.objects))
            for _,_,_,_,actions in rule_blocks(f.init(),diagnostic_view=False):
                for action in atoms(actions):
                    if action=='disable-self':continue
                    if action.startswith('up-get-precise-time '):
                        self.assertEqual(action.split()[1],'0')
                        o.goals[action.split()[2]]=10001
                    else:o.action(action)
            self.assertEqual(o.goals[f.g('player')],player)
            self.assertEqual(before,(o.pointer,o.local,o.remote,o.objects))
            # The same identity controls emitted prefixes and roster eligibility.
            for obj in o.objects.values():obj['player']=player
            records,_=decode(o.call())
            self.assertTrue(records)
            self.assertEqual({r['player'] for r in records},{player})
            self.assertTrue(any(r['type']==20 for r in records),player)
        self.assertNotIn('up-get-fact my-player-number',f.init())

    def test_entry_survives_all_old_gates_and_invalid_saved_object(self):
        o=FileObserver();o.pointer=-1
        for n in ('capture','b-turn','b-phase-valid','b-early-left','b-middle-left','b-late-left','b-final-left'):
            o.goals[cb.g(n)]=0
        records,stats=decode(o.call())
        self.assertTrue(all(x['complete'] for x in records),records)
        self.assertEqual([r['type'] for r in records],[1,90,2])
        self.assertEqual(records[0]['values'][1:5],[3,1,-2,0])
        self.assertEqual(o.pointer,-1)

    def test_full_multi_actor_and_multi_target_no32_limit(self):
        o=FileObserver();o.local=list(range(100,141));o.remote=[20,21]
        for n in o.local:o.objects[n]=dict(o.objects[1],id=n)
        before=(deepcopy(o.local),deepcopy(o.remote),o.pointer,o.sn)
        records,_=decode(o.call())
        self.assertTrue(all(x['complete'] for x in records))
        self.assertEqual([r['values'][2] for r in records if r['type']==10],o.local)
        self.assertEqual([r['values'][2] for r in records if r['type']==11],o.remote)
        self.assertEqual((o.local,o.remote,o.pointer,o.sn),before)

    def test_invalid_list_entry_does_not_read_stale_pointer(self):
        o=FileObserver();o.local=[999]
        records,_=decode(o.call());row=next(r for r in records if r['type']==10)
        self.assertEqual(row['values'],[0,0]+[-2]*len(f.FIELDS))
        self.assertEqual(o.pointer,20)

    def test_periodic_covers_all_members_through_release_and_expires(self):
        o=FileObserver();o.call();o.objects[1]['group-flag']=0
        o.time+=30
        records,_=decode(o.call(4));actors=[r for r in records if r['type']==21]
        self.assertEqual(len(actors),3)
        o.time+=32
        records,_=decode(o.call(4))
        self.assertEqual([r['values'][1] for r in records if r['type']==23],[1])
        self.assertEqual(o.pointer,20)

    def test_logging_disabled_preserves_all_external_state(self):
        o=FileObserver(0);before=(deepcopy(o.objects),o.pointer,deepcopy(o.local),deepcopy(o.remote),o.sn)
        self.assertEqual(o.call(),[])
        self.assertEqual(before,(o.objects,o.pointer,o.local,o.remote,o.sn))

    def test_empty_and_repeated_invocations_remain_distinct(self):
        o=FileObserver();o.local=[]
        first,_=decode(o.call());second,_=decode(o.call())
        self.assertNotEqual(first[0]['event'],second[0]['event'])
        self.assertEqual(first[0]['values'][1],0)

    def test_delivery_loss_interleaving_duplicates_and_tail(self):
        a=FileObserver();one=a.call();two=[s.replace('RAW58P1','RAW58P2') for s in one]
        rows,_=decode([s for pair in zip(one,two) for s in pair]+['unrelated\n'])
        self.assertTrue(all(r['complete'] for r in rows));self.assertEqual({r['player'] for r in rows},{1,2})
        for broken in (one[1:],one[:-1],one[:20]+one[21:],one+one):
            rows,stats=decode(broken)
            self.assertTrue(any(not r['complete'] for r in rows) or stats['orphan_tokens'])

    def test_private_layout_and_no_runtime_mutators(self):
        ids={n:f.BASE+i for i,n in enumerate(f.NAMES)}
        for i,n in enumerate(['local','local-last','remote','remote-last']):
            self.assertEqual(ids[n],ids['local']+i)
        text=f.library()+f.coverage()
        self.assertNotRegex(text,r'\((up-target-|up-find-|up-reset-|up-add-object|up-remove-|set-strategic-number|up-set-timer)')
        self.assertLess(f.ROSTER_BASE+f.STRIDE*f.ROSTER,13000)
        self.assertLess(f.BASE+len(f.NAMES),f.ROSTER_BASE)

    def test_all_physical_bridges_preserve_gameplay_actions_and_hashes(self):
        reg=json.loads(cb.REG.read_text())
        for s in reg['sites']:
            bridge=f.render_site(s)
            self.assertEqual(cb.strip_source(bridge,reg),s['original'])
            actual=[]
            for *_,actions in rule_blocks(bridge,diagnostic_view=False):
                actual += ['('+a+')' for a in atoms(actions) if f.PREFIX not in a]
            expected=s['actions']
            normalize=lambda seq:[re.sub(r'\(up-jump-rule -?\d+\)','JUMP',a) for a in seq if a!='(disable-self)']
            self.assertEqual(normalize(actual),normalize(expected),s['id'])
            self.assertEqual(actual.count('(disable-self)'),expected.count('(disable-self)'))
            self.assertEqual(cb.strip_source(bridge.replace('gl-cbf-kind','gl-cbf-kind',1),reg),s['original'])
            with self.assertRaises(ValueError):
                cb.strip_source(bridge.replace('(defrule','(defrule\n ;tamper',1),reg)

    def test_load_order_bootstrap_and_storage_bounds(self):
        root=cb.ROOT;entry=(root/'AI RAW.per').read_text()
        self.assertLess(entry.index('(load "rawai-command-boundary-defs")'),entry.index('(load "rawai-customconstants")'))
        self.assertLess(entry.index('(load "rawai-command-boundary-private-init")'),entry.index('(load "rawai-customconstants")'))
        self.assertTrue((root/'rawai-command-boundary-private-init.per').is_file())
        self.assertLess(entry.index('(load "rawai-command-boundary")'),entry.index('(load "rawai-sn-defines")'))
        self.assertLess(10200+4*len(f.bootstrap_commands()),f.ROSTER_BASE)
        for name in f.BOOTSTRAP:
            self.assertNotIn('(up-jump-direct g: gl-cbf-entry)',(root/name).read_text())
        for path in root.glob('*.per'):
            if path.name.startswith('rawai-command-boundary'):continue
            text=cb.strip_source(path.read_text(encoding='utf-8-sig'),json.loads(cb.REG.read_text()))
            for name,value in re.findall(r'\(defconst ((?:gl-|sn-)[\w-]+) (\d+)\)',text):
                self.assertFalse(10000<=int(value)<11700,(path.name,name,value))

    def test_original_command_executes_with_mode_on_and_off(self):
        target='(up-target-objects 0 action-garrison -1 stance-no-attack)'
        site=dict(id=9999,file='fixture.per',facts='(true)',actions=[
            '(set-strategic-number sn-keystates 2)',target,'(set-strategic-number sn-keystates 0)'],
            file_commands=[dict(index=1,id=9999,command=target,indirect=False,args=[0,'action-garrison',-1,'stance-no-attack'])])
        for mode in (0,1):
            o=FileObserver(mode);o.const.update({'action-garrison':5,'stance-no-attack':0})
            o.rules=rule_blocks(f.library()+f.render_site(site),diagnostic_view=False)
            original=o.action;issued=[]
            def action(s):
                if s.startswith('set-strategic-number '):o.settings['sn-keystates']=int(s.split()[-1])
                elif '('+s+')'==target:issued.append((list(o.local),list(o.remote),o.pointer,o.settings['sn-keystates']))
                else:original(s)
            o.action=action;o.pc=0
            for _ in range(200000):
                if o.pc>=len(o.rules):break
                o.next_pc=o.pc+1;*_,facts,actions=o.rules[o.pc]
                def evaluate(e):
                    return any(evaluate(x) for x in e[1:]) if e[0]=='or' else o.fact(' '.join(e))
                if all(evaluate(e) for e in expressions(facts)):
                    for s in atoms(actions):o.action(s)
                o.pc=o.next_pc
            else:self.fail('wrapper did not return')
            self.assertEqual(issued,[([1,2,3],[20],20,2)])
            self.assertEqual(o.settings['sn-keystates'],0)

    def test_relative_jumps_reach_same_original_destination(self):
        reg=json.loads(cb.REG.read_text())
        for name in {s['file'] for s in reg['sites'] if s.get('jumps')}:
            text=(cb.ROOT/name).read_text(encoding='utf-8-sig')
            original=rule_blocks(cb.strip_source(text,reg),diagnostic_view=False)
            physical=rule_blocks(text,diagnostic_view=False)
            old=[(i,int(m[1])) for i,r in enumerate(original) for m in re.finditer(r'\(up-jump-rule (-?\d+)\)',r[4])]
            new=[(i,int(m[1])) for i,r in enumerate(physical) for m in re.finditer(r'\(up-jump-rule (-?\d+)\)',r[4])]
            self.assertEqual(len(old),len(new))
            for (i,a),(j,b) in zip(old,new):
                x,y=i+a+1,j+b+1
                if x==len(original):self.assertEqual(y,len(physical))
                else:self.assertEqual(' '.join(original[x][3].split()),' '.join(physical[y][3].split()),name)

    def test_roster_holes_do_not_duplicate_remaining_members(self):
        o=FileObserver();o.call();o.indirect[f.ROSTER_BASE]=-2
        o.local=[2];o.call()
        self.assertEqual([o.indirect[f.ROSTER_BASE+i*3] for i in range(3)],[-2,2,3])

    def test_signed_sentinel_values_are_losslessly_escaped(self):
        o=FileObserver();o.objects[1]['target-id']=f.BEGIN;o.objects[2]['precise-x']=f.ESCAPE
        records,_=decode(o.call())
        self.assertTrue(all(r['complete'] for r in records))
        local=[r['values'][2:] for r in records if r['type']==10]
        self.assertEqual(local[0][8],f.BEGIN);self.assertEqual(local[1][4],f.ESCAPE)

    def test_supported241_member_limit_and_explicit_overflow(self):
        o=FileObserver();o.local=list(range(1000,1241));o.remote=[]
        for n in o.local:o.objects[n]=dict(o.objects[20],id=n)
        records,_=decode(o.call())
        self.assertEqual(len([r for r in records if r['type']==10]),241)
        o.local.append(1241);o.objects[1241]=dict(o.objects[20],id=1241)
        records,_=decode(o.call())
        self.assertIn([2],[r['values'] for r in records if r['type']==90])

    def test_dropped_whole_member_record_cannot_match_packet(self):
        o=FileObserver();rows,_=decode(o.call()+o.call(2))
        intact=list(log.observations(rows));self.assertFalse(intact[0]['gaps'])
        broken=[r for r in rows if not (r['type']==10 and r['values'][0]==1)]
        observed=list(log.observations(broken));self.assertIn('missing-subrecords',observed[0]['gaps'])
        registry={'sites':[{'file_commands':[dict(id=1001,command='(up-target-objects 0 action-garrison -1 stance-no-attack)',indirect=False)]}]}
        packet=dict(action='SPECIAL',order_id=5,player_id=1,object_ids=[1,3],target_id=20,milliseconds=100010,sequence=10)
        result=list(log.correlations(broken,[packet],registry))
        self.assertEqual(result[0]['status'],'incomplete-inputs');self.assertEqual(result[0]['packet_sequences'],[])

    def test_distinct_order_work706_and_actor_incidence(self):
        events=[]
        for i in range(100):
            for family,sub in [('ORDER',None),('WORK',None),('AI_ORDER',706)]:
                events.append(dict(action=family,order_id=sub,sequence=len(events),milliseconds=i*13,
                                   player_id=8,object_ids=[34329,33901],target_id=34365))
        result=log.classify_events(events)
        self.assertEqual(len(result['runs']),6)
        self.assertEqual(result['counts']['706'],dict(distinct_packets=100,actor_incidences=200))


if __name__=='__main__':unittest.main()
