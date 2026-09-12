"""Per-site policy from the T53 Villager subset of the ownership inventory.

Conservatively includes all migration rules (some mixed hull/passenger sites).
Regeneration is a review operation, not automatic permission to add Ctrl.
"""
import hashlib
import json
import re
from pathlib import Path
import sys
from validate_naval_doctrine import rule_blocks

ROOT = Path(__file__).resolve().parents[1]
DUC = re.compile(r'\(up-target-(?:objects|point) [^()]+\)')

def semantic(text):
    return ' '.join(text.split())

def inventory(root=ROOT):
    sites=[]
    all_commands=[]
    for path in sorted(root.glob('*.per')):
        text=path.read_text(encoding='utf-8-sig')
        if ';CB BEGIN ' in text:
            from generate_command_boundary import strip_source, REG
            text=strip_source(text,json.loads(REG.read_text()))
        for a,b,block,facts,actions in rule_blocks(text):
            commands=list(DUC.finditer(actions))
            if not commands:
                continue
            identity=hashlib.sha256(semantic(facts+actions).encode()).hexdigest()
            all_commands.append((path.name,identity))
            candidate=(
                'migration-boarding-group' in actions or
                'gl-island-migration-state' in facts or
                'villager' in actions or
                path.name in {'rawai-general.per','rawai-hunt.per'} or
                any(s in facts for s in ['FARM-STAFFING-','COLONY-TC-ASSIGN',
                    'TRADE-RETIRE-CHECK','TRANSPORT-REPAIR-TASK','LOCAL-RESPONSE-COMMAND']) or
                (path.name=='rawai-homebase.per' and 'action-default' in actions))
            if not candidate:
                continue
            for index,m in enumerate(commands):
                command=m.group()
                prefix=actions[:m.start()]
                # Modifier applies to exactly the next command, not the whole rule.
                last_modifier=re.findall(r'sn-keystates ([02])', prefix)
                modifier=int(last_modifier[-1]) if last_modifier else 0
                action=re.search(r' action-[\w-]+',command).group().strip()
                if modifier==2:
                    policy='EXPERIMENT: mining boarding' if action=='action-garrison' else 'EXISTING: zero-carry economy'
                    assessment='Ctrl2 issuance semantics documented; family runtime effect unproven.'
                else:
                    policy='EXCEPTION: unchanged modifier 0'
                    assessment={
                        'action-garrison':'Rescue/scout/recovery/reboarding semantics not assessed by this mining-load experiment.',
                        'action-default':'Gather/deposit/build/repair Ctrl effects not interchangeable; retain existing carry and task policy.',
                        'action-stop':'Terminal release semantics not assessed; no modifier change.',
                        'action-delete':'Destructive retirement semantics not assessed; no modifier change.',
                    }.get(action,'Movement/unload/patrol semantics not assessed; no modifier change.')
                sites.append(dict(file=path.name,line=text.count('\n',0,a)+1,
                    rule=identity,command_index=index,states=re.findall(r'\(goal ([^()]+)\)',facts),
                    command=command,modifier=modifier,policy=policy,assessment=assessment))
    return dict(schema=1,provenance='T53-VILLAGER-KEYSTATES-AUDIT.md + current ownership rule enumeration',
        boundary='Conservative per-command superset: mixed migration hull/scout sites retained explicitly, not assumed to be Villagers.',
        all_duc_digest=hashlib.sha256(json.dumps(all_commands).encode()).hexdigest(),sites=sites)

def main():
    path=ROOT/'villager-command-modifier-policy.json'
    actual=inventory()
    if '--write' in sys.argv:
        path.write_text(json.dumps(actual,indent=2)+'\n',encoding='utf-8')
    elif json.loads(path.read_text(encoding='utf-8')) != actual:
        raise SystemExit('DUC policy changed: review every changed/new site before regenerating')
    print(f'Villager policy: PASS ({len(actual["sites"])} explicit command entries)')

if __name__=='__main__':
    main()
