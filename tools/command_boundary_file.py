"""File mode for the existing command-boundary registry/generator.

No native packet hook: PRE describes inputs; INVOKED is script control flow.
Physical wrappers evaluate original predicates once and preserve action order.
"""
import hashlib
import json
import re
from pathlib import Path

import generate_command_boundary as cb

ROOT = cb.ROOT
PREFIX = 'gl-cbf-'
BASE = 10000
ROSTER = 400
ROSTER_BASE = 10500
STRIDE = 3  # actor, last observed reservation time, last hull
RELEASE_SECONDS = 60
FIELDS = ['id', 'type', 'class', 'player', 'precise-x', 'precise-y',
          'action', 'order', 'target-id', 'garrisoned', 'carry', 'group-flag', 'garrison-count']
NAMES = ['mode','entry','return','cont','site','kind','serial','now','saved','valid',
         'local','local-last','remote','remote-last','idx','loop','selector',
         'value','count','sum','size','slot','address','found','actor','last','hull',
         'next','periodic','outer-return','roster-loop','roster-size','start',
         'capture','b-turn','b-phase-valid','b-phase-time','b-observe-due',
         'b-early-left','b-middle-left','b-late-left','b-final-left', 'record',
         'args0','args1','args2','args3','point-y','live','bound','incomplete','intent-valid','sub','free','player']
LIFECYCLE = ['gl-island-migration-state','gl-island-migration-transport-id']
SETTINGS = ['sn-percent-civilian-gatherers','sn-percent-civilian-builders',
            'sn-percent-civilian-explorers','sn-cap-civilian-explorers',
            'sn-total-number-explorers','sn-disable-villager-garrison',
            'sn-keystates','sn-food-gatherer-percentage','sn-wood-gatherer-percentage',
            'sn-gold-gatherer-percentage','sn-stone-gatherer-percentage']
NAMES += ['sn-'+str(i) for i in range(len(SETTINGS))]
NAMES += ['data-'+str(i) for i in range(len(FIELDS))]
BEGIN = -2147483001
END = -2147483002
ESCAPE = -2147483003
SCHEMA = 58
BOOTSTRAP = {'rawai-customconstants.per','rawai-init-goals.per'}
DIRECT = re.compile(r'^\((up-target-objects|up-target-point|up-reset-unit|up-garrison|up-ungarrison|up-drop-resources)\b')
INDIRECT = re.compile(r'^\((build|build-forward|build-wall|build-gate|up-build|up-build-line|up-assign-builders|up-retask-gatherers|up-request-hunters|up-reset-scouts|up-send-scout|delete-unit|up-delete-idle-units)\b')
MUTATION = re.compile(r'^\((up-create-group|up-modify-group-flag|up-reset-group|up-disband-group-type)\b')


def g(n): return PREFIX+n
def put(n,v): return f'(set-goal {g(n)} {v})'
def mod(n,op,v): return f'(up-modify-goal {g(n)} {op} {v})'
def copy(n,v): return mod(n,'g:=',g(v))
def eq(n,v): return f'(goal {g(n)} {v})'
def cmp(n,op,v): return f'(up-compare-goal {g(n)} {op} {v})'
def read(n,out): return f'(up-get-object-data object-data-{n} {g(out)})'
def rule(f,a): return cb.rule(f,a)


class Program:
    def __init__(self): self.rules=[]; self.labels={}; self.fix=[]
    def add(self,f,a): self.rules.append(rule(f,a))
    def label(self,name): self.labels[name]=len(self.rules)
    def jump(self,f,label):
        self.fix.append((len(self.rules),label)); self.add(f,['JUMP'])
    def text(self):
        for i,label in self.fix:
            self.rules[i]=self.rules[i].replace('JUMP',f'(up-jump-rule {self.labels[label]-i-1})')
        return ''.join(self.rules)
    def batch(self,f,actions):
        for c in cb.chunks(actions,24): self.add(f,c)
    def token(self,operand,framing=False):
        # Distinct per-player reusable formats, one scalar per documented call.
        # Every token contributes count and rolling checksum; reduce before add
        # so a legitimate signed32 object value cannot overflow the accumulator.
        self.add(['(true)'],[mod('value',operand.split()[0].replace(':',':='),operand.split()[1])])
        for p in range(1,9):
            if not framing:
                self.add([eq('player',p),
                          f'(or {eq("value",BEGIN)} {eq("value",ESCAPE)})'],
                         [f'(up-log-data 0 str-cbf-p{p} c: {ESCAPE})'])
            self.add([eq('player',p)],
                     [f'(up-log-data 0 str-cbf-p{p} g: {g("value")})'])
        self.add(['(true)'],[mod('count','c:+',1),mod('value','c:mod',65521),
                              mod('value','c:+',65521),mod('value','c:mod',65521),
                              mod('sum','c:*',31),mod('sum','g:+',g('value')),mod('sum','c:mod',65521)])
    def record(self,typ,values):
        if typ==90:
            self.add([eq('incomplete',0)],[put('incomplete',1),
                '(up-chat-data-to-all str-t12-diag-id c: 790)'])
        self.add(['(true)'],[put('count',0),put('sum',0),mod('sub','c:+',1)])
        self.token(f'c: {BEGIN}',framing=True)
        for op in [f'c: {SCHEMA}',f'g: {g("start")}',f'g: {g("sub")}',f'g: {g("serial")}',f'c: {typ}',
                   f'g: {g("site")}',f'g: {g("now")}',f'c: {len(values)}',*values]: self.token(op)
        # Snapshot checksum/count before logging them; trailer excludes itself.
        self.add(['(true)'],[copy('size','count'),copy('record','sum')])
        for op in [f'g: {g("size")}',f'g: {g("record")}',f'g: {g("serial")}',f'c: {END}']: self.token(op)


def constants():
    text=';Generated private file observer. No gameplay consumers.\n'
    text+='\n'.join(f'(defconst {g(n)} {BASE+i})' for i,n in enumerate(NAMES))+'\n'
    text+='\n'.join(f'(defconst str-cbf-p{p} "RAW58P{p} %d")' for p in range(1,9))+'\n'
    for index,c in enumerate(bootstrap_commands()):
        for offset,field in enumerate(('pre','post','time','ready')):
            text+=f'(defconst {journal(c["id"],field)} {10200+index*4+offset})\n'
    # Explicit named reservation proves allocator extent to static tooling.
    text+='\n'.join(f'(defconst {g("roster-"+str(i))} {ROSTER_BASE+i})' for i in range(ROSTER*STRIDE))+'\n'
    return text


def init():
    actions=[put(n,1 if n=='mode' else -2 if n.startswith('sn-') else 0) for n in NAMES]
    actions += [f'(set-goal {g("roster-"+str(i))} -2)' for i in range(ROSTER*STRIDE)]
    actions += [f'(set-goal {journal(c["id"],field)} {0 if field=="ready" else -2})'
                for c in bootstrap_commands() for field in ('pre','post','time','ready')]
    return ''.join(rule(['(true)'],c+['(disable-self)']) for c in cb.chunks(actions,28))+rule(['(true)'],[
        f'(up-get-precise-time 0 {g("start")})',f'(up-get-fact my-player-number 0 {g("player")})','(disable-self)'])


def library():
    p=Program()
    p.add(['(true)'],[f'(up-get-rule-id {g("entry")})',mod('entry','c:+',2)])
    p.jump(['(true)'],'exit')
    # Entry is BEFORE any pointer/capture/credit test. get-object-data documents
    # -2 on failure; no selector runs until saved id is valid.
    p.jump([eq('mode',0)],'return')
    p.add(['(true)'],[mod('serial','c:+',1),f'(up-get-fact game-time 0 {g("now")})',
        f'(up-get-search-state {g("local")})',put('saved',-2),read('id','saved'),put('valid',0)])
    p.add([cmp('saved','c:>=',0)],[put('valid',1)])
    p.record(1,[f'g: {g(n)}' for n in ['kind','local','remote','saved','valid','mode']]+
        ['g: gl-island-migration-transport-id','g: gl-island-migration-state']+
        ['g: gl-cb-'+n for n in ['enabled','capture','b-turn','b-phase-valid','b-phase-time',
         'b-observe-due','b-early-left','b-middle-left','b-late-left','b-final-left']]+
        [f'g: {g("args"+str(i))}' for i in range(4)]+[f'g: {g("point-y")}','s: sn-keystates'])
    p.jump([cmp('kind','c:!=',6)],'not-setting')
    p.record(31,['s: '+sn for sn in SETTINGS])
    p.jump(['(true)'],'complete')
    p.label('not-setting')
    p.jump([cmp('kind','c:!=',7)],'not-lifecycle')
    p.record(32,['g: '+n for n in LIFECYCLE])
    p.jump(['(true)'],'complete')
    p.label('not-lifecycle')
    p.jump([eq('kind',2)],'complete')  # INVOKED: no selection inspection
    p.jump([eq('kind',3)],'complete')  # native admission: no claimed recipients
    p.jump([eq('valid',0)],'invalid')
    p.jump([eq('kind',4)],'periodic')
    # Enumerate both final lists with exact documented index bounds0..240.
    for source in ['local','remote']:
        p.add(['(true)'],[put('idx',0)])
        p.label(source+'-loop')
        p.jump([cmp('idx','g:>=',g(source))],source+'-done')
        p.jump([cmp('idx','c:>',240)],'capacity')
        p.add(['(true)'],[put('live',0)]+[put('data-'+str(i),-2) for i in range(len(FIELDS))])
        p.add([f'(up-set-target-object search-{source} g: {g("idx")})'],
            [put('live',1)]+[read(f,'data-'+str(i)) for i,f in enumerate(FIELDS)])
        p.record(10 if source=='local' else 11,[f'g: {g("idx")}',f'g: {g("live")}']+
                 [f'g: {g("data-"+str(i))}' for i in range(len(FIELDS))])
        if source=='local':
            p.jump([eq('live',0)],'track-done')
            p.jump([cmp('data-11','c:!=','migration-boarding-group')],'track-done')
            p.jump([cmp('data-3','g:!=',g('player'))],'track-done')
            p.add(['(true)'],[copy('actor','data-0'),put('slot',0),put('free',-1)])
            p.label('track-loop')
            p.jump([cmp('slot','g:>=',g('roster-size'))],'track-allocate')
            p.add(['(true)'],[copy('address','slot'),mod('address','c:*',STRIDE),mod('address','c:+',ROSTER_BASE),
                 f'(up-get-indirect-goal g: {g("address")} {g("found")})'])
            p.jump([cmp('found','g:==',g('actor'))],'track-write')
            p.add([cmp('found','c:<',0),eq('free',-1)],[copy('free','slot')])
            p.add(['(true)'],[mod('slot','c:+',1)]);p.jump(['(true)'],'track-loop')
            p.label('track-allocate')
            p.add([cmp('free','c:>=',0)],[copy('slot','free')])
            p.jump([cmp('slot','c:>=',ROSTER)],'track-full')
            p.add([cmp('slot','g:>=',g('roster-size'))],[copy('roster-size','slot'),mod('roster-size','c:+',1)])
            p.add(['(true)'],[copy('address','slot'),mod('address','c:*',STRIDE),mod('address','c:+',ROSTER_BASE)])
            p.jump(['(true)'],'track-write')
            p.label('track-full');p.record(90,['c: 4']);p.jump(['(true)'],'track-done')
            p.label('track-write')
            p.add(['(true)'],[f'(up-set-indirect-goal g: {g("address")} g: {g("actor")})',mod('address','c:+',1),
                f'(up-set-indirect-goal g: {g("address")} g: {g("now")})',mod('address','c:+',1),
                f'(up-set-indirect-goal g: {g("address")} g: gl-island-migration-transport-id)'])
            p.record(20,[f'g: {g("slot")}',f'g: {g("actor")}', 'g: gl-island-migration-transport-id'])
            p.label('track-done')
        # Capture actual current intent target data without changing selection.
        p.jump([eq('live',0)],source+'-next')
        p.batch(['(true)'],[f'(up-get-object-target-data object-data-{f} {g("data-"+str(i))})'
                            for i,f in enumerate(FIELDS[:6])])
        # Only emit when selector succeeded; stale target data never used.
        p.record(12,[f'c: {0 if source=="local" else 1}',f'g: {g("idx")}']+
                    [f'g: {g("data-"+str(i))}' for i in range(6)])
        p.label(source+'-next')
        p.add(['(true)'],[mod('idx','c:+',1)])
        p.jump(['(true)'],source+'-loop')
        p.label(source+'-done')
    p.add(['(true)'],[put('slot',-1),mod('hull','g:=','gl-island-migration-transport-id'),put('live',0)]+
          [put('data-'+str(i),-2) for i in range(len(FIELDS))])
    p.add([f'(up-set-target-by-id g: {g("hull")})'],[put('live',1)]+[read(f,'data-'+str(i)) for i,f in enumerate(FIELDS)])
    p.record(22,[f'g: {g(n)}' for n in ['slot','hull','live']]+[f'g: {g("data-"+str(i))}' for i in range(len(FIELDS))])
    p.jump(['(true)'],'restore')
    p.label('periodic')
    p.add(['(true)'],[put('slot',0)])
    p.label('roster-loop')
    p.jump([cmp('slot','g:>=',g('roster-size'))],'restore')
    p.add(['(true)'],[copy('address','slot'),mod('address','c:*',STRIDE),mod('address','c:+',ROSTER_BASE),
        f'(up-get-indirect-goal g: {g("address")} {g("actor")})',mod('address','c:+',1),
        f'(up-get-indirect-goal g: {g("address")} {g("last")})',mod('address','c:+',1),
        f'(up-get-indirect-goal g: {g("address")} {g("hull")})'])
    p.jump([cmp('actor','c:<',0)],'roster-next')
    p.add(['(true)'],[put('live',0)]+[put('data-'+str(i),-2) for i in range(len(FIELDS))])
    p.add([f'(up-set-target-by-id g: {g("actor")})'],[put('live',1)]+[read(f,'data-'+str(i)) for i,f in enumerate(FIELDS)])
    p.record(21,[f'g: {g(n)}' for n in ['slot','actor','hull','live']]+[f'g: {g("data-"+str(i))}' for i in range(len(FIELDS))])
    # Refresh only actual current reserved membership, not mere enter intent.
    p.add([eq('live',1),eq('data-11','migration-boarding-group'),cmp('data-3','g:==',g('player'))],[copy('last','now'),mod('address','c:-',1),
        f'(up-set-indirect-goal g: {g("address")} g: {g("now")})',mod('address','c:+',1)])
    p.add(['(true)'],[put('live',0)]+[put('data-'+str(i),-2) for i in range(len(FIELDS))])
    p.add([f'(up-set-target-by-id g: {g("hull")})'],[put('live',1)]+[read(f,'data-'+str(i)) for i,f in enumerate(FIELDS)])
    p.record(22,[f'g: {g(n)}' for n in ['slot','hull','live']]+[f'g: {g("data-"+str(i))}' for i in range(len(FIELDS))])
    p.add(['(true)'],[copy('bound','now'),mod('bound','g:-',g('last'))])
    p.jump([cmp('bound','c:<=',RELEASE_SECONDS)],'roster-next')
    p.record(23,[f'g: {g(n)}' for n in ['slot','actor','hull','last']])
    p.add(['(true)'],[mod('address','c:-',2),f'(up-set-indirect-goal g: {g("address")} c: -2)'])
    p.label('roster-next');p.add(['(true)'],[mod('slot','c:+',1)]);p.jump(['(true)'],'roster-loop')
    p.label('invalid')
    p.record(90,['c: 1']) # cannot restore invalid/null pointer, explicit gap
    p.jump(['(true)'],'complete')
    p.label('capacity')
    p.record(90,['c: 2']) # actual count retained in entry; never silently truncate
    p.label('restore')
    p.add(['(true)'],[put('live',0)])
    p.add([f'(up-set-target-by-id g: {g("saved")})'],[put('live',1)])
    p.jump([eq('live',1)],'complete')
    p.record(90,['c: 3'])
    p.label('complete')
    p.record(2,[f'g: {g("kind")}'])
    p.label('return')
    p.add(['(true)'],[f'(up-jump-direct g: {g("return")})'])
    p.label('exit')
    return p.text()


def call(site,kind,args):
    values=[mod('args'+str(i),'g:=',v) if isinstance(v,str) and v.endswith('-x') else put('args'+str(i),v)
            for i,v in enumerate(args)]
    y=mod('point-y','g:=',args[0][:-1]+'y') if isinstance(args[0],str) and args[0].endswith('-x') else put('point-y',-2)
    return [put('site',site),put('kind',kind),*values,y,
            f'(up-get-rule-id {g("return")})',mod('return','c:+',1),f'(up-jump-direct g: {g("entry")})']


def identity_words(reg=None):
    if reg is None:reg=json.loads(cb.REG.read_text())
    # Stable source/command map identity, excluding emitted wrappers/self-hash.
    data=[(s['id'],s['file'],s['original_sha256'],s.get('file_commands',[])) for s in reg['sites']]
    digest=hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':')).encode()).digest()
    return [int.from_bytes(digest[i:i+4],'big',signed=True) for i in range(0,32,4)]


def bootstrap_commands():
    reg=json.loads(cb.REG.read_text())
    return [c for s in reg['sites'] if s['file'] in BOOTSTRAP for c in s['file_commands']]


def journal(site,field):return g(f'boot-{site}-{field}')


def coverage():
    p=Program()
    p.jump([eq('mode',0)],'done')
    p.add(['(true)'],[f'(up-get-fact game-time 0 {g("now")})'])
    p.jump([cmp('now','g:<',g('next'))],'done')
    p.jump([cmp('next','c:>',0)],'sample')
    p.add(['(true)'],call(0,0,[-2]*4))
    p.record(40,[f'c: {word}' for word in identity_words()])
    for c in bootstrap_commands():
        p.jump([f'(goal {journal(c["id"],"ready")} 0)'],'boot-'+str(c['id']))
        p.record(41,[f'c: {c["id"]}']+[f'g: {journal(c["id"],k)}' for k in ('time','pre','post')])
        p.label('boot-'+str(c['id']))
    p.label('sample')
    p.add(['(true)'],[copy('next','now'),mod('next','c:+',1)])
    p.add(['(true)'],call(0,4,[-2]*4))
    for i,sn in enumerate(SETTINGS):
        p.add(['(true)'],[mod('value','s:=',sn)])
        p.jump([cmp('value','g:==',g('sn-'+str(i)))],'setting-'+str(i))
        p.add(['(true)'],[copy('sn-'+str(i),'value'),mod('serial','c:+',1)])
        p.record(30,[f'c: {i}',f'g: {g("sn-"+str(i))}'])
        p.label('setting-'+str(i))
    p.label('done')
    return p.text()


def render_site(site):
    if site.get('jump_only'):
        body=site['original']
        for old,new in site.get('jumps',[]):body=body.replace(f'(up-jump-rule {old})',f'(up-jump-rule {new})',1)
        return f';CB BEGIN {site["id"]}\n'+body+f';CB END {site["id"]}\n'
    actions=site['actions']; targets={x['index']:x for x in site['file_commands']}
    ident=site['id'];result=[]
    # disable-self takes effect next pass: move to predicate-bearing rule,
    # never disable only a continuation. Other action ordering stays exact.
    result.append(rule([site['facts']],[put('cont',ident)]+(['(disable-self)'] if '(disable-self)' in actions else [])))
    pending=[]
    def flush():
        nonlocal pending
        for chunk in cb.chunks(pending,26):result.append(rule([eq('cont',ident)],chunk))
        pending=[]
    for i,action in enumerate(actions):
        if action=='(disable-self)':continue
        if action.startswith('(up-jump-rule '):
            flush();old=int(action.split()[-1][:-1]);new=dict(site.get('jumps',[])).get(old,old)
            result.append(rule([eq('cont',ident)],[put('cont',0),f'(up-jump-rule {new})']))
            continue
        if i in targets:
            flush(); t=targets[i]
            if site['file'] in BOOTSTRAP:
                # These are one-shot setting/initialization writes, not DUC.
                # Record values at issuance into a per-site journal; file
                # delivery happens only after the shared logger initializes.
                if '(disable-self)' not in actions or not t['indirect']:
                    raise ValueError('bootstrap site requires reviewed one-shot setting: '+str(t['id']))
                target=action.split()[1];mode='s' if target.startswith('sn-') else 'g'
                result.append(rule([eq('cont',ident)],
                    [f'(up-get-fact game-time 0 {journal(t["id"],"time")})',
                     f'(up-modify-goal {journal(t["id"],"pre")} {mode}:= {target})']))
                result.append(rule([eq('cont',ident)],[action,
                    f'(up-modify-goal {journal(t["id"],"post")} {mode}:= {target})',
                    f'(set-goal {journal(t["id"],"ready")} 1)']))
                continue
            result.append(rule([eq('cont',ident)],call(t['id'],3 if t['indirect'] else 1,t['args'])))
            # Original action executes unconditionally on logger outcome.
            result.append(rule([eq('cont',ident)],[action]))
            after=(6 if any(sn in action for sn in SETTINGS) else 7 if any(n in action for n in LIFECYCLE)
                   else 5 if MUTATION.match(action) else 2)
            result.append(rule([eq('cont',ident)],call(t['id'],after,t['args'])))
        else: pending.append(action)
    flush();result.append(rule([eq('cont',ident)],[put('cont',0)]))
    return f';CB BEGIN {ident}\n'+''.join(result)+f';CB END {ident}\n'


def upgrade(reg):
    from validate_naval_doctrine import rule_blocks
    from writer_trace import DIRECT as ALL_DIRECT, DELEGATE
    originals={p.name:cb.strip_source(p.read_text(encoding='utf-8-sig'),reg)
               for p in ROOT.glob('*.per') if not p.name.startswith('rawai-command-boundary')}
    sites=[];seq=1000
    for name,text in originals.items():
        # Conservative superset of every DUC writer, plus native admissions.
        for start,end,body,facts,actions in rule_blocks(text,diagnostic_view=False):
            aa=cb.clean_actions(actions); commands=[]
            for i,a in enumerate(aa):
                setting=a.startswith(('(set-strategic-number ','(up-modify-sn ')) and a.split()[1] in SETTINGS
                parts=a[1:-1].split()
                destination=parts[2] if parts[0]=='up-get-object-data' else parts[1] if len(parts)>1 else ''
                lifecycle=parts[0] in ('set-goal','up-modify-goal','up-get-object-data') and destination in LIFECYCLE
                if not (ALL_DIRECT.match(a) or DELEGATE.match(a) or setting or lifecycle or DIRECT.match(a) or INDIRECT.match(a) or
                        MUTATION.match(a) and 'migration-' in a):continue
                indirect=not a.startswith(('(up-target-objects ','(up-target-point '))
                args=[-2]*4
                if not indirect:
                    # Command expression is authoritative in registry; dynamic
                    # operand values are copied into private fields by bridge.
                    args=a[1:-1].split()[1:]
                old_writer=re.search(r'\(set-goal gl-board-diag-issued (\d+)\)',actions)
                commands.append(dict(index=i,id=seq,command=a,indirect=indirect,args=args,
                    legacy_boarding_writer=int(old_writer[1]) if old_writer and 'action-garrison' in a else None));seq+=1
            jump_only=not commands and '(up-jump-rule ' in actions
            if not commands and not jump_only:continue
            if any(x in actions for x in ('up-jump-direct','up-jump-dynamic','up-get-rule-id')):
                raise ValueError(f'Needs explicit control-flow relocation: {name}:{start}')
            ident=commands[0]['id'] if commands else seq
            if not commands:seq+=1
            sites.append(dict(id=ident,file=name,line=text.count('\n',0,start)+1,jump_only=jump_only,
                facts=facts.removeprefix('(defrule').strip(),actions=aa,file_commands=commands,
                original=body,original_sha256=hashlib.sha256(body.encode()).hexdigest()))
    relocate(sites,originals)
    return dict(schema=2,sites=sites,fields=reg['fields'],
                file_trace=dict(schema=SCHEMA,mode=1,base=BASE,private_names=NAMES,
                    roster_base=ROSTER_BASE,roster_capacity=ROSTER,release_seconds=RELEASE_SECONDS,
                    selector_max_index=240,fields=FIELDS,settings=SETTINGS,
                    missing_pointer='ENTRY and explicit failure only; no selection mutation'),
                private_base=reg['private_base'],private_names=reg['private_names']),originals


def relocate(sites,originals):
    from validate_naval_doctrine import rule_blocks
    for name,text in originals.items():
        rr=rule_blocks(text,diagnostic_view=False)
        bybody={s['original']:s for s in sites if s['file']==name}
        starts=[];parts=[];total=0
        for _,_,body,_,_ in rr:
            starts.append(total)
            rendered=render_site(bybody[body]) if body in bybody else body
            parts.append(rule_blocks(rendered,diagnostic_view=False));total+=len(parts[-1])
        starts.append(total)
        for i,(_,_,body,_,_) in enumerate(rr):
            for m in re.finditer(r'\(up-jump-rule (-?\d+)\)',body):
                old=int(m[1]);dest=i+old+1
                if not 0<=dest<=len(rr):raise ValueError('invalid original jump')
                lo,hi=sorted((rr[i][0],rr[dest][0] if dest<len(rr) else len(text)))
                if re.search(r'^\s*#(?:load-if|else|end-if)',text[lo:hi],re.M):
                    raise ValueError('conditional compilation crosses jump '+name)
                position=next(j for j,r in enumerate(parts[i]) if '(up-jump-rule ' in r[4])
                bybody[body]['jumps']=[(old,starts[dest]-starts[i]-position-1)]


def generate(write=False):
    reg=json.loads(cb.REG.read_text())
    if reg['schema']==1 or '--rescan' in __import__('sys').argv:
        if not write:raise ValueError('file upgrade requires --file-write')
        reg,originals=upgrade(reg)
    else:
        originals={name:cb.strip_source((ROOT/name).read_text(encoding='utf-8-sig'),reg)
                   for name in {s['file'] for s in reg['sites']}}
    reg['file_trace'].update(fields=FIELDS,private_names=NAMES,settings=SETTINGS,lifecycle=LIFECYCLE)
    if write:
        # Coverage startup embeds this source map identity, not a circular hash.
        cb.REG.write_text(json.dumps(reg,indent=2)+'\n')
    rendered={}
    from validate_naval_doctrine import rule_blocks
    for name,text in originals.items():
        relevant=[s for s in reg['sites'] if s['file']==name]
        if not relevant:
            if ';CB BEGIN ' in (ROOT/name).read_text(encoding='utf-8-sig'):rendered[name]=text
            continue
        offsets=[0]
        for line in text.splitlines(keepends=True):offsets.append(offsets[-1]+len(line))
        for s in sorted(relevant,key=lambda s:s['line'],reverse=True):
            start=offsets[s['line']-1];end=start+len(s['original'])
            if text[start:end]!=s['original']:raise ValueError(f'original position mismatch {name}:{s["id"]}')
            text=text[:start]+render_site(s)+text[end:]
        rendered[name]=text
    # Old observer disabled, definitions retained so ENTRY can expose its gates.
    rendered.update(cb.support())
    rendered['rawai-command-boundary.per']=library()
    rendered['rawai-command-boundary-coverage.per']=coverage()
    rendered['rawai-command-boundary-defs.per']+=constants()
    rendered['rawai-command-boundary-private-init.per']=init()
    if write:
        for s in reg['sites']:s['emitted_sha256']=hashlib.sha256(render_site(s).encode()).hexdigest()
        cb.REG.write_text(json.dumps(reg,indent=2)+'\n')
    for name,text in rendered.items():
        path=ROOT/name
        if write:
            if path.exists() and path.read_text(encoding='utf-8-sig')==text:continue
            path.write_bytes(text.replace('\n','\r\n').encode() if name.startswith('rawai-command-boundary') else
                             cb.preserve_endings(text,path.read_bytes() if path.exists() else b''))
        elif path.read_text(encoding='utf-8-sig')!=text:raise ValueError('out of sync '+name)
    print('file command boundary generation PASS',len(reg['sites']),'rules',
          sum(len(s['file_commands']) for s in reg['sites']),'commands')
