"""Canonical command-boundary observations, not a deployment overlay.

Only registered rules are split at a command; predicates run once, continuation
is unconditional on diagnostic budget. A private synchronous subroutine reads
final lists and restores the selected-object pointer. No search/filter mutation.
"""
import hashlib
from difflib import SequenceMatcher
import json
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
REG=ROOT/'command-boundary-registry.json'
PREFIX='gl-cb-'
WINDOW=180
LIMIT=4
CAPACITY=2
BOARDING_LATE_AGES=(12,20,28)
SOURCE_FILES=('rawai-military.per','rawai-homebase.per','rawai-hunt.per')
BASE=15869
NAMES=['enabled','entry','return','cont','site','family','local','local-last','remote','remote-last',
       'saved','now','serial','emit','idx','modifier','elapsed','distance','stage','reserved',
       'tid','ttype','tclass','tx','ty','towner','tgroup',
       'actor','atype','aclass','ax','ay','owner','group','action','order','intent','garrison','carry',
       'seek','probe','seek-rule','member','covered','first-actor','read-valid',
       'capture','b-observe-due','b-phase-time','b-phase-valid','b-episode-hull',
       'b-early-left','b-middle-left','b-late-left','b-final-left']
COUNTERS=['next','left','due','calls','nonempty','suppressed','detailed','missed','targets','invalid','rotation','turn']
PREV=['actor','hull','time','x','y','hx','hy','owner','group','howner','hgroup']
for f in ('b','r'):
    NAMES += [f+'-'+n for n in COUNTERS]
for i in range(CAPACITY):NAMES += [f'p{i}-'+n for n in PREV]
LABELS=['site','serial','family','now','modifier','local','remote','stage','reserved','index',
        'actor','ax','ay','action','order','intent','garrison','carry','group','owner','atype','aclass',
        'tid','ttype','tclass','tx','ty','towner','tgroup','distance',
        *['previous-'+n for n in PREV], 'elapsed','end',
        'coverage-family','calls','nonempty','suppressed','detailed','missed','targets','invalid','enabled','previous-member']
CODES={n:720+i for i,n in enumerate(LABELS)}
MARKER=re.compile(r';CB BEGIN (\d+)\n.*?;CB END \1\n?',re.S)


def g(n):return PREFIX+n
def setg(n,v):return f'(set-goal {g(n)} {v})'
def mod(n,op,v):return f'(up-modify-goal {g(n)} {op} {v})'
def copy(n,v):return mod(n,'g:=',g(v))
def cmp(n,op,v):return f'(up-compare-goal {g(n)} {op} {v})'
def goal(n,v):return f'(goal {g(n)} {v})'
def emit(label,operand):return [f'(up-chat-data-to-all str-t12-diag-id c: {CODES[label]})',
                              f'(up-chat-data-to-all str-t12-diag-value {operand})']
def report(label,n=None):return emit(label,'g: '+g(n or label))
def rule(facts,actions):return '(defrule\n\t'+'\n\t'.join(facts)+'\n=>\n\t'+'\n\t'.join(actions)+'\n)\n'
def read(field,n):return f'(up-get-object-data object-data-{field} {g(n)})'
def chunks(seq,n):return [seq[i:i+n] for i in range(0,len(seq),n)]


def library():
    rules=[]
    def add(f,a):rules.append(rule(f,a))
    # Natural traversal skips this subroutine; calls enter after this header.
    add(['(true)'],[f'(up-get-rule-id {g("entry")})',mod('entry','c:+',2),'SKIP_LIBRARY'])
    # A skipped sentinel makes entry+2 stable and explicit.
    add(['(false)'],['(do-nothing)'])
    add(['(true)'],[setg('emit',0),setg('capture',0),setg('covered',0),setg('first-actor',-2),f'(up-get-fact game-time 0 {g("now")})',
        f'(up-get-search-state {g("local")})',read('id','saved'),
        mod('modifier','s:=','sn-keystates'),mod('stage','g:=','gl-island-migration-state'),
        mod('reserved','g:=','gl-island-migration-transport-id'),mod('serial','c:+',1)])
    for fam,num in [('b',1),('r',2)]:
        ff=[goal('family',num)]
        # No startup scans: counters/replenishment happen only on real calls.
        add(ff,[mod(fam+'-calls','c:+',1)])
        add(ff+[cmp('local','c:>',0),cmp('remote','c:>',0)], [mod(fam+'-nonempty','c:+',1)])
        add(ff+[cmp('now','g:>=',g(fam+'-next')),cmp('local','c:>',0),cmp('remote','c:>',0)],
            [setg(fam+'-left',LIMIT),copy(fam+'-next','now'),mod(fam+'-next','c:+',WINDOW)]+
            ([setg('b-'+n+'-left',1) for n in ('early','middle','late','final')] if fam=='b' else []))
        add(ff+[cmp('local','c:>',0),cmp('remote','c:>',0),cmp('saved','c:<',0)],
            [mod(fam+'-invalid','c:+',1)])
        if fam=='b':
            active=ff+[cmp('local','c:>',0),cmp('remote','c:>',0),cmp('reserved','c:>',0)]
            # A new hull/start resets tracking and phase, NEVER family credits.
            reset=[copy('b-episode-hull','reserved'),setg('b-phase-valid',0),setg('b-turn',0),
                   setg('b-rotation',0),setg('b-observe-due',0),setg('p0-actor',-2),setg('p1-actor',-2)]
            add(active+[cmp('reserved','g:!=',g('b-episode-hull'))],reset)
            add(active+[goal('site',20)],reset)
            # Site21 starts the EXISTING local30s boarding phase after travel.
            # This diagnostic timestamp does not touch that timer/deadline.
            add(active+[goal('site',21)],[copy('b-phase-time','now'),setg('b-phase-valid',1)])
            add(active+[cmp('saved','c:>=',0),cmp('now','g:>=',g('b-observe-due'))],
                [setg('capture',1),copy('b-observe-due','now'),mod('b-observe-due','c:+',3)])
            add(ff,[copy('elapsed','now'),mod('elapsed','g:-',g('b-phase-time'))])
            # Reserve1 early +1 each at12/20/28s. Older stage wins after a gap;
            # only one report per call. No missed stage can spend another lane.
            for lane,age in reversed(list(zip(('middle','late','final'),BOARDING_LATE_AGES))):
                add(ff+[goal('enabled',1),goal('capture',1),goal('emit',0),goal('b-phase-valid',1),
                        cmp('site','c:!=',25),goal('b-'+lane+'-left',1),cmp('elapsed','c:>=',age)],
                    [setg('emit',1),setg('b-'+lane+'-left',0),mod('b-left','c:-',1),mod('b-detailed','c:+',1)])
            add(ff+[goal('enabled',1),goal('capture',1),goal('emit',0),goal('b-early-left',1),goal('b-turn',1)],
                [setg('emit',1),setg('b-early-left',0),mod('b-left','c:-',1),mod('b-detailed','c:+',1)])
        else:
            add(ff+[goal('enabled',1),cmp('local','c:>',0),cmp('remote','c:>',0),cmp('saved','c:>=',0),
                cmp(fam+'-left','c:>',0),cmp('now','g:>=',g(fam+'-due'))],
            [setg('emit',1),setg('capture',1),mod(fam+'-left','c:-',1),copy(fam+'-due','now'),mod(fam+'-due','c:+',3),
             mod(fam+'-detailed','c:+',1)])
        add(ff+[goal('emit',0),cmp('local','c:>',0),cmp('remote','c:>',0)],
            [mod(fam+'-suppressed','c:+',1),mod(fam+'-missed','g:+',g('local'))])
        add(ff+[goal('capture',1),cmp(fam+'-rotation','g:>=',g('local'))],[setg(fam+'-rotation',0)])
        add(ff+[goal('capture',1)],[copy('idx',fam+'-rotation')])
    add([goal('capture',0)],[f'(up-jump-direct g: {g("return")})'])
    # Only known-valid saved pointers reach these selected-object reads.
    add([goal('capture',1)],[setg(n,-2) for n in ['tid','ttype','tclass','tx','ty','towner','tgroup']])
    add([goal('capture',1),'(up-set-target-object search-remote c: 0)'],[
        *[read(f,n) for f,n in [('id','tid'),('type','ttype'),('class','tclass'),('precise-x','tx'),
            ('precise-y','ty'),('player','towner'),('group-flag','tgroup')]]])
    header=[]
    for n in ['site','serial','family','now','modifier','local','remote','stage','reserved',
              'tid','ttype','tclass','tx','ty','towner','tgroup']:header+=report(n)
    for c in chunks(header,24):add([goal('emit',1)],c)
    # Rolling quiet observations retain both sides of each selected pair.
    # Rotate after a report; rebind quietly, then follow the same actors.
    for i in range(CAPACITY):
        # Second observation of each pair locates the SAME earlier actor in the
        # final list, rather than assuming that selection order stayed fixed.
        sf=[goal('capture',1),goal('family',1),goal('b-turn',1),cmp(f'p{i}-actor','c:>',0)]
        add([goal('capture',1)],[setg('member',-1),setg('seek',0)])
        add(sf,[f'(up-get-rule-id {g("seek-rule")})',mod('seek-rule','c:+',1)])
        scan=sf+[cmp('seek','g:<',g('local')),cmp('seek','c:<',32),cmp('member','c:!=',1)]
        add(scan,[setg('probe',-2)])
        add(scan+[f'(up-set-target-object search-local g: {g("seek")})'],[read('id','probe')])
        add(scan+[cmp('probe','g:==',g(f'p{i}-actor'))],[setg('member',1),copy('idx','seek')])
        add(scan,[mod('seek','c:+',1),f'(up-jump-direct g: {g("seek-rule")})'])
        add(sf+[cmp('member','c:!=',1),cmp('seek','g:>=',g('local'))],[setg('member',0)])
        ff=[goal('capture',1),cmp('idx','g:<',g('local'))]+([] if i==0 else [goal('family',1)])
        if i:
            add(ff,[setg('probe',-2)])
            add(ff+[f'(up-set-target-object search-local g: {g("idx")})'],[read('id','probe')])
            ff=ff+[cmp('probe','g:!=',g('first-actor'))]
        fields=[('id','actor'),('type','atype'),('class','aclass'),('precise-x','ax'),('precise-y','ay'),
                ('player','owner'),('group-flag','group'),('action','action'),('order','order'),
                ('target-id','intent'),('garrisoned','garrison'),('carry','carry')]
        add([goal('capture',1)],[setg('read-valid',0)])
        add(ff+[f'(up-set-target-object search-local g: {g("idx")})'],[setg('read-valid',1),*[read(f,n) for f,n in fields],
                f'(up-get-point-distance {g("ax")} {g("tx")} {g("distance")})'])
        ff=ff+[goal('read-valid',1)]
        if i==0:add(ff,[copy('first-actor','actor')])
        details=report('index','idx')
        for n in ['actor','ax','ay','action','order','intent','garrison','carry','group','owner','atype','aclass','distance']:
            details+=report(n)
        for c in chunks(details,24):add(ff+[goal('emit',1)],c)
        bf=ff+[goal('family',1)] if i==0 else ff
        add(bf,[copy('elapsed','now'),mod('elapsed','g:-',g(f'p{i}-time'))])
        previous=[]
        for n in PREV:previous+=report('previous-'+n,f'p{i}-'+n)
        previous+=report('elapsed')+report('previous-member','member')
        for c in chunks(previous,24):add(bf+[goal('emit',1)],c)
        current=['actor','tid','now','ax','ay','tx','ty','owner','group','towner','tgroup']
        add(bf,[copy(f'p{i}-'+n,v) for n,v in zip(PREV,current)])
        # idx increments only when a member was actually read.
        add(ff,[mod('idx','c:+',1),mod('covered','c:+',1)])
    for fam,num in [('b',1),('r',2)]:
        ff=[goal('family',num),goal('emit',1)]
        # index-start = covered members; missed includes all remaining members.
        add(ff,[mod(fam+'-missed','g:+',g('local')),mod(fam+'-missed','g:-',g('covered')),
                mod(fam+'-targets','g:+',g('remote')),mod(fam+'-targets','c:-',1)])
        if fam=='b':
            add([goal('family',1),goal('capture',1)],[setg('b-turn',1)])
            add(ff,[setg('b-turn',0),mod('b-rotation','c:+',CAPACITY)])
        else:add(ff,[mod('r-rotation','c:+',1)])
    add([goal('emit',1)],report('end','serial'))
    add([goal('capture',1)],[f'(up-set-target-by-id g: {g("saved")})',
        f'(up-jump-direct g: {g("return")})'])
    rules[0]=rules[0].replace('SKIP_LIBRARY',f'(up-jump-rule {len(rules)-1})')
    return ';Generated command-boundary read-only subroutine.\n'+''.join(rules)


def coverage():
    text=';Generated independent coverage counters; no detail quota is shared.\n'
    # Separate report timer does not reset call counters or detail credits.
    for f,num in [('b',1),('r',2)]:
        cond=[cmp(f+'-calls','c:>',0),cmp('now','g:>=',g(f+'-report'))]
        fields=emit('coverage-family',f'c: {num}')+report('now')+report('enabled')
        for n in ['calls','nonempty','suppressed','detailed','missed','targets','invalid']:fields+=report(n,f+'-'+n)
        for c in chunks(fields,24):text+=rule(cond,c)
        text+=rule(cond,[copy(f+'-report','now'),mod(f+'-report','c:+',WINDOW)])
    return rule(['(true)'],[f'(up-get-fact game-time 0 {g("now")})'])+text


def support():
    names=NAMES+['b-report','r-report']
    assert BASE+len(names)-1<=16000
    defs=';Generated. Private command observations; no gameplay consumer.\n'
    defs+='\n'.join(f'(defconst {g(n)} {BASE+i})' for i,n in enumerate(names))+'\n'
    init=''
    for c in chunks([setg(n,1 if n=='enabled' else -2 if n.startswith('p') and '-' in n else 0) for n in names],28):
        init+=rule(['(true)'],c+['(disable-self)'])
    return {'rawai-command-boundary-defs.per':defs,'rawai-command-boundary-init.per':init,
            'rawai-command-boundary.per':library(),'rawai-command-boundary-coverage.per':coverage()}


def clean_actions(actions):
    # Registered rules have simple one-line actions; reject anything ambiguous.
    code=re.sub(r';[^\n]*','',actions).strip()
    if code.endswith(')'):code=code[:-1].rstrip() # rule terminator from rule_blocks
    return re.findall(r'\([^()]*\)',code)


def render_site(site):
    facts=site['facts']; actions=site['actions'];idx=site['command_index']
    prefix,suffix=actions[:idx],actions[idx:]
    ident=site['id'];result=[]
    # Prefix may include the existing Ctrl2 setter. Nothing changes it before
    # the original command and immediate reset in the continuation.
    tail=[setg('site',ident),setg('family',site['family']),f'(up-get-rule-id {g("return")})',
          mod('return','c:+',1),f'(up-jump-direct g: {g("entry")})']
    fact_count=facts.count('(')
    firstcap=32-fact_count-1
    first=prefix[:firstcap];prefix=prefix[firstcap:]
    result.append(rule([facts],[setg('cont',ident)]+first))
    for c in chunks(prefix,25):result.append(rule([goal('cont',ident)],c))
    result.append(rule([goal('cont',ident)],tail))
    for c in chunks(suffix,28):result.append(rule([goal('cont',ident)],c))
    result.append(rule([goal('cont',ident)],[setg('cont',0)]))
    return f';CB BEGIN {ident}\n'+''.join(result)+f';CB END {ident}\n'


def strip_source(text,registry):
    byid={s['id']:s for s in registry['sites']}
    def replace(m):
        s=byid[int(m[1])]
        if hashlib.sha256(s['original'].encode()).hexdigest()!=s['original_sha256']:
            raise ValueError('original contract hash changed: '+m[1])
        if m.group()!=render_site(s):raise ValueError('modified diagnostic bridge: '+m[1])
        return s['original']
    return MARKER.sub(replace,text)


def preserve_endings(text,reference):
    """Keep each unchanged legacy line's terminator; new generated lines CRLF."""
    old=reference.decode('utf-8-sig').splitlines(keepends=True)
    new=text.splitlines(keepends=True)
    old_text=[s.rstrip('\r\n') for s in old];new_text=[s.rstrip('\r\n') for s in new]
    output=[s.rstrip('\r\n')+'\r\n' if s.endswith('\n') else s for s in new]
    for block in SequenceMatcher(None,old_text,new_text,autojunk=False).get_matching_blocks():
        output[block.b:block.b+block.size]=old[block.a:block.a+block.size]
    return ''.join(output).encode('utf-8')


def discover():
    from validate_naval_doctrine import rule_blocks
    sites=[];r_id=101
    policy=json.loads((ROOT/'villager-command-modifier-policy.json').read_text())
    resource_sites={(s['file'],s['line']) for s in policy['sites'] if 'action-default' in s['command']}
    for name in SOURCE_FILES:
        text=(ROOT/name).read_text(encoding='utf-8-sig')
        for start,end,body,facts,actions in rule_blocks(text):
            commands=clean_actions(actions)
            board=re.search(r'\(set-goal gl-board-diag-issued (\d+)\)',actions)
            if board:
                target='(up-target-objects 0 action-garrison -1 stance-no-attack)'
                ident=int(board[1]);family=1
            elif (name,text.count('\n',0,start)+1) in resource_sites and '(up-target-objects 0 action-default -1 stance-no-attack)' in commands:
                target='(up-target-objects 0 action-default -1 stance-no-attack)'
                ident=r_id;r_id+=1;family=2
            else:continue
            assert commands.count(target)==1
            assert not any('up-jump-' in c or 'disable-self' in c for c in commands)
            sites.append(dict(id=ident,family=family,file=name,line=text.count('\n',0,start)+1,
                facts=facts.removeprefix('(defrule').strip(),actions=commands,
                command_index=commands.index(target),original=body,
                original_sha256=hashlib.sha256(body.encode()).hexdigest()))
    assert len([s for s in sites if s['family']==1])==5
    assert len([s for s in sites if s['family']==2])==13
    return dict(schema=1,fields=CODES,private_base=BASE,private_names=NAMES+['b-report','r-report'],
        sites=sites,window_seconds=WINDOW,detail_commands_per_family=LIMIT,tracking_capacity=CAPACITY,
        provenance='Extends shared RAW12 numeric diagnostics after T56 IDs700-719; no new strings.')


def main():
    if '--restore-legacy-endings' in sys.argv:
        # Formatting only: retain current text/edits; reuse HEAD terminators for
        # exactly matching lines. Never substitute HEAD gameplay/source text.
        import subprocess
        for name in (*SOURCE_FILES,'AI RAW.per'):
            p=ROOT/name;reference=subprocess.check_output(['git','show','HEAD:'+name],cwd=ROOT)
            p.write_bytes(preserve_endings(p.read_text(encoding='utf-8-sig'),reference))
        print('Legacy terminators restored without source-text changes');return
    reg=json.loads(REG.read_text()) if REG.exists() else discover()
    reg.update(fields=CODES,private_names=NAMES+['b-report','r-report'],boarding_sampling=dict(
        early_reports=1,late_loading_ages=list(BOARDING_LATE_AGES),quiet_capture_gap=3,
        phase_anchor_site=21,family_limit=LIMIT,window_seconds=WINDOW,
        reset_note='New hull/start resets tracking, not credits. Quiet snapshots never authorize gameplay.'))
    if '--write' in sys.argv:REG.write_text(json.dumps(reg,indent=2)+'\n')
    rendered=support()
    for name in SOURCE_FILES:
        text=(ROOT/name).read_text(encoding='utf-8-sig')
        original=strip_source(text,reg) if ';CB BEGIN ' in text else text
        updated=original
        for s in reg['sites']:
            if s['file']!=name:continue
            assert updated.count(s['original'])==1,(name,s['id'])
            updated=updated.replace(s['original'],render_site(s),1)
        # Original jumps are wholly outside the registered scopes. Assert this
        # rather than silently changing control-flow operands.
        from validate_naval_doctrine import rule_blocks
        rr=rule_blocks(original)
        for i,(a,b,body,_,_) in enumerate(rr):
            for m in re.finditer(r'\(up-jump-rule (-?\d+)\)',body):
                dest=i+int(m[1])+1
                assert 0<=dest<=len(rr)
                lo,hi=sorted((i,dest))
                assert not any(rr[k][2] in [s['original'] for s in reg['sites']] for k in range(lo,hi)),(name,i,dest)
        rendered[name]=updated
    for name,text in rendered.items():
        p=ROOT/name
        if '--write' in sys.argv:
            p.write_bytes(preserve_endings(text,p.read_bytes()) if name in SOURCE_FILES else text.replace('\n','\r\n').encode())
        elif not p.exists() or p.read_text(encoding='utf-8-sig')!=text:raise SystemExit('out of sync: '+name)
    print('command boundary generation: PASS; registered sites',len(reg['sites']))


if __name__=='__main__':main()
