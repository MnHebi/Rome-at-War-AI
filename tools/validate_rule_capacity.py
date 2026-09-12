"""Count physical loaded PER rules, never the observer-stripped semantic view.

DE/UP documented ceiling:10,000 rules per AI, across loaded files.
https://airef.github.io/resources/articles/data-limits.html
The conservative matrix resolves civilization/difficulty/DE and includes BOTH
arms of all other conditions. It is an upper bound, not engine execution.
"""
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
LIMIT = 10000
TOKEN = re.compile(r'(?P<directive>^\s*#(?:load-if-defined|load-if-not-defined|else|end-if)\b[^\n]*)'
                   r'|\(load\s+"(?P<load>[^"]+)"\s*\)'
                   r'|(?P<comment>;[^\n]*)|(?P<string>"(?:[^"\\]|\\.)*")'
                   r'|(?P<rule>\(defrule\b)', re.M)

def source_tokens(text):
    return [(m.lastgroup, m[m.lastgroup], text.count('\n',0,m.start())+1)
            for m in TOKEN.finditer(text) if m.lastgroup not in ('comment','string')]

def loaded_rules(tokens, defined, unknown=(), entry='AI RAW.per'):
    unknown=set(unknown);result=[]
    def visit(name, chain=()):
        if name in chain:raise ValueError('recursive load: '+name)
        if name not in tokens:raise ValueError('missing load: '+name)
        stack=[];active=True
        for kind,value,line in tokens[name]:
            if kind=='directive':
                parts=value.split(';',1)[0].strip().split();op=parts[0]
                if op.startswith('#load-if-'):
                    if len(parts)!=2:raise ValueError('invalid conditional: '+value)
                    symbol=parts[1]
                    condition=None if symbol in unknown else symbol in defined
                    if op=='#load-if-not-defined' and condition is not None:condition=not condition
                    stack.append((active,condition,False));active=active and condition is not False
                elif op=='#else':
                    if not stack or stack[-1][2]:raise ValueError('unmatched/repeated else')
                    parent,condition,_=stack[-1];stack[-1]=(parent,condition,True)
                    active=parent and condition is not True
                else:
                    if not stack:raise ValueError('unmatched end-if')
                    active=stack.pop()[0]
            elif active and kind=='load':visit(value+'.per',chain+(name,))
            elif active:result.append((name,line))
        if stack:raise ValueError('unclosed conditional: '+name)
    visit(entry)
    return result

def report(root=ROOT, payload=None):
    if payload is None:
        payload={p.name:p.read_text(encoding='utf-8-sig') for p in root.glob('*.per')}
    tokens={n:source_tokens(t) for n,t in payload.items()}
    symbols=set(re.findall(r'^\s*#load-if-(?:not-)?defined\s+(\S+)', '\n'.join(payload.values()), re.M))
    civs=sorted(x for x in symbols if x.endswith('-CIV'))
    difficulties=sorted(x for x in symbols if x.startswith('DIFFICULTY-'))
    unknown=symbols-set(civs)-set(difficulties)-{'DE-AVAILABLE'}
    profiles=[]
    for civ in civs:
        for difficulty in difficulties:
            rules=loaded_rules(tokens,{civ,difficulty,'DE-AVAILABLE'},unknown)
            profiles.append(dict(civ=civ,difficulty=difficulty,rules=len(rules),
                first_overflow=rules[LIMIT] if len(rules)>LIMIT else None))
    worst=max(profiles,key=lambda p:p['rules'])
    return dict(status='PASS' if worst['rules']<=LIMIT else 'FAIL',limit=LIMIT,
                method='Physical recursive loads; civ/difficulty/DE resolved, both arms of other conditions counted',
                profiles=profiles,maximum=worst,headroom=LIMIT-worst['rules'],
                observer_rules={n:len([x for x in ts if x[0]=='rule']) for n,ts in tokens.items()
                                if n in ('rawai-command-boundary.per','rawai-command-boundary-coverage.per')})

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=ROOT)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args();result=report(args.root)
    if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='profiles'},indent=2))
    raise SystemExit(result['status']!='PASS')
