"""Capacity regression and unchanged physical log streams; not engine proof."""
from pathlib import Path
import unittest
from unittest.mock import patch

import command_boundary_file as f
from test_command_boundary import atoms
from test_command_boundary_file import FileObserver
from test_pre_backlog import expressions
from validate_naval_doctrine import rule_blocks
from validate_rule_capacity import loaded_rules, source_tokens, report, LIMIT


class InlineTokenProgram(f.Program):
    """Frozen failed506 emission algorithm, used only as a comparison oracle."""
    def token(self, operand, framing=False):
        self.add(['(true)'],[f.mod('value',operand.split()[0].replace(':',':='),operand.split()[1])])
        for player in range(1,9):
            if not framing:
                self.add([f.eq('player',player),
                          f'(or {f.eq("value",f.BEGIN)} {f.eq("value",f.ESCAPE)})'],
                         [f'(up-log-data 0 str-cbf-p{player} c: {f.ESCAPE})'])
            self.add([f.eq('player',player)],[f'(up-log-data 0 str-cbf-p{player} g: {f.g("value")})'])
        self.add(['(true)'],[f.mod('count','c:+',1),f.mod('value','c:mod',65521),
                              f.mod('value','c:+',65521),f.mod('value','c:mod',65521),
                              f.mod('sum','c:*',31),f.mod('sum','g:+',f.g('value')),f.mod('sum','c:mod',65521)])


def execute(observer, text, start=0):
    observer.rules=rule_blocks(text,diagnostic_view=False)
    observer.pc=start
    for _ in range(2000000):
        if observer.pc>=len(observer.rules):return
        observer.next_pc=observer.pc+1
        *_,facts,actions=observer.rules[observer.pc]
        def evaluate(e):
            return any(evaluate(x) for x in e[1:]) if e[0]=='or' else observer.fact(' '.join(e))
        if all(evaluate(e) for e in expressions(facts)):
            for action in atoms(actions):observer.action(action)
        observer.pc=observer.next_pc
    raise AssertionError('unbounded generated control flow')


class FileCapacityTests(unittest.TestCase):
    def test_identical_boundary_and_late_roster_streams_for_every_player(self):
        for player in range(1,9):
            with patch.object(f,'Program',InlineTokenProgram):old=FileObserver()
            new=FileObserver()
            for observer in (old,new):
                observer.goals[f.g('player')]=player
                for obj in observer.objects.values():obj['player']=player
                observer.objects[1]['target-id']=f.BEGIN
                observer.objects[2]['precise-x']=f.ESCAPE
                observer.objects[3]['carry']=-2147483648
                observer.call();observer.call(2)
                observer.objects[1]['group-flag']=0
                observer.time+=30;observer.call(4)
                observer.time+=32;observer.call(4)
            self.assertEqual(old.lines,new.lines,player)
            self.assertEqual((old.pointer,old.local,old.remote,old.objects,old.indirect),
                             (new.pointer,new.local,new.remote,new.objects,new.indirect))

    def test_coverage_and_library_returns_work_at_nonzero_global_offsets(self):
        streams=[]
        for program in (InlineTokenProgram,f.Program):
            with patch.object(f,'Program',program):
                text=f.rule(['(true)'],['(do-nothing)'])*7+f.library()+f.coverage()
            observer=FileObserver()
            for command in f.bootstrap_commands():
                for field in ('time','pre','post','ready'):
                    observer.goals[f.journal(command['id'],field)]=1
            execute(observer,text)
            observer.time+=1
            execute(observer,text)
            streams.append(observer.lines)
            self.assertEqual((observer.pointer,observer.local,observer.remote),(20,[1,2,3],[20]))
        self.assertEqual(*streams)

    def test_loaded_matrix_rejects_failed506_and_accepts_compact(self):
        payload={p.name:p.read_text(encoding='utf-8-sig') for p in f.ROOT.glob('*.per')}
        result=report(payload=payload)
        self.assertEqual(result['status'],'PASS')
        self.assertEqual(len(result['profiles']),34*6)
        self.assertGreaterEqual(result['headroom'],500)
        with patch.object(f,'Program',InlineTokenProgram):
            payload['rawai-command-boundary.per']=f.library()
            payload['rawai-command-boundary-coverage.per']=f.coverage()
        failed=report(payload=payload)
        self.assertEqual(failed['status'],'FAIL')
        self.assertGreater(failed['maximum']['rules'],LIMIT)
        self.assertEqual(failed['maximum']['first_overflow'][0],'rawai-command-boundary-coverage.per')

    def test_loads_count_again_and_branches_comments_strings_are_handled(self):
        root='; (defrule fake)\n(up-chat-data-to-all "(defrule fake)" c: 0)\n'
        root+='#load-if-defined A\n(load "child")\n#else\n(load "other")\n#end-if\n(load "child")\n'
        tokens={n:source_tokens(t) for n,t in {'AI RAW.per':root,
                 'child.per':'(defrule (true) => (do-nothing))',
                 'other.per':'(defrule (true) => (do-nothing))\n(defrule (true) => (do-nothing))'}.items()}
        self.assertEqual(len(loaded_rules(tokens,{'A'})),2)
        self.assertEqual(len(loaded_rules(tokens,set())),3)
        self.assertEqual(len(loaded_rules(tokens,set(),{'A'})),4)
        with self.assertRaisesRegex(ValueError,'missing load'):
            loaded_rules({'AI RAW.per':source_tokens('(load "missing")')},set())
        with self.assertRaisesRegex(ValueError,'recursive load'):
            loaded_rules({'AI RAW.per':source_tokens('(load "AI RAW")')},set())

    def test_shared_emitter_is_compact_and_never_falls_through(self):
        p=f.Program();p.record(90,['c: -2147483648','c: 2147483647',f'c: {f.BEGIN}',f'c: {f.ESCAPE}'])
        text=p.text();self.assertEqual(text,p.text())
        self.assertLess(len(rule_blocks(text,diagnostic_view=False)),50)
        self.assertEqual(text.count('(up-log-data'),16)
        old=InlineTokenProgram();old.record(90,['c: -2147483648','c: 2147483647',f'c: {f.BEGIN}',f'c: {f.ESCAPE}'])
        a=FileObserver();b=FileObserver();execute(a,text);execute(b,old.text())
        self.assertEqual(a.lines,b.lines)


if __name__=='__main__':unittest.main()
