"""Read-only runtime preparation/evidence tools. Never deploy, launch or clean up."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import time

import command_boundary_file as trace
from command_boundary_log import classify_events, actor_timelines
from compare_boarding_contacts import compare, cohorts
from validate_naval_doctrine import rule_blocks
from writer_trace import string_budget

ROOT=Path(__file__).resolve().parents[1]


def manifest(root=ROOT):
    payload={p.name:p.read_bytes() for p in sorted(root.iterdir()) if p.is_file() and p.suffix in ('.ai','.per')}
    hashes={n:hashlib.sha256(b).hexdigest() for n,b in payload.items()}
    aggregate=hashlib.sha256(''.join(n+'\0'+hashes[n]+'\n' for n in sorted(hashes)).encode()).hexdigest()
    reg=json.loads((root/'command-boundary-registry.json').read_text())
    commands=[c for s in reg['sites'] for c in s['file_commands']]
    return dict(status='SOURCE CANDIDATE ONLY — ENGINE PREFLIGHT PENDING',root=str(root),
        head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
        file_count=len(payload),files=hashes,aggregate_sha256=aggregate,
        aggregate_algorithm='SHA256(sorted filename + NUL + file SHA256 + LF); not interchangeable with older aggregate formats',
        source_identity_words=trace.identity_words(),string_budget=string_budget(payload),
        observer_physical_rules={n:len(rule_blocks(b.decode('utf-8-sig'),diagnostic_view=False))
            for n,b in payload.items() if n.startswith('rawai-command-boundary')},
        sites=len(reg['sites']),commands=len(commands),direct_list_commands=sum(not c['indirect'] for c in commands),
        bootstrap_commands=len(trace.bootstrap_commands()),roster_capacity=trace.ROSTER,
        list_supported_count=241,postrelease_game_seconds=trace.RELEASE_SECONDS,
        storage='private named goals10000.. plus journal10200.. and400x3 roster10500..11699',
        installed_exceptions='Not incorporated. Future authorized deployment must reconcile rawai-general/customconstants experiments explicitly.')


def assess(cache, supplement=None):
    floods=classify_events(cache['events'])
    actors,hulls,links=cohorts(cache)
    contacts=compare(cache['events'],actors,hulls,diagnostics=cache.get('diagnostics',[]))
    unknown={}
    for target in (34365,35071):
        rows=[e for e in cache['events'] if e.get('target_id')==target or target in e.get('object_ids',[])]
        typed=[e for e in rows if any(k in e for k in ('target_type','target_owner','instance_id'))]
        unknown[str(target)]=dict(type='UNKNOWN',owner='UNKNOWN',
            initial_object=None if not supplement else supplement.get('header_controls',{}).get(str(target)),
            referenced_packets=len(rows),first_reference=rows[0] if rows else None,
            last_reference=rows[-1] if rows else None,explicit_identity_candidates=typed[:20],
            boundary='Packet target references do not identify target type/owner. BUILD intents lacking an instance-ID link cannot resolve this.')
    return dict(replay_sha256=cache.get('sha256'),floods=floods,
        actor_timelines=actor_timelines(cache,floods),contact_comparison=contacts,dynamic_targets=unknown,
        cohort='Affected actors plus independently mining-site-linked peers; not population incidence',
        missing_evidence='Matching complete file PRE/INVOKED/state traces do not exist for historical T57; no actor-list reconstruction asserted.')


def snapshot(paths,previous=None):
    now=time.time();sizes={str(p):dict(bytes=p.stat().st_size,mtime_ns=p.stat().st_mtime_ns) for p in paths}
    result=dict(wall_timestamp=now,files=sizes,free_bytes={str(p.anchor):shutil.disk_usage(p.anchor).free for p in paths})
    if previous:
        elapsed=now-previous['wall_timestamp']
        growth=sum(v['bytes']-previous['files'].get(n,{'bytes':v['bytes']})['bytes'] for n,v in sizes.items())
        result.update(elapsed_wall_seconds=elapsed,observed_growth_bytes=growth,
            bytes_per_wall_minute=growth*60/elapsed if elapsed>0 else None,
            three_wall_hour_projection_bytes=max(0,growth)*10800/elapsed if elapsed>0 else None)
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='mode',required=True)
    m=sub.add_parser('manifest');m.add_argument('output',type=Path)
    a=sub.add_parser('assess-cache');a.add_argument('cache',type=Path);a.add_argument('output',type=Path);a.add_argument('--supplement',type=Path)
    s=sub.add_parser('snapshot');s.add_argument('output',type=Path);s.add_argument('--logs',type=Path,nargs='+',required=True);s.add_argument('--previous',type=Path)
    args=p.parse_args()
    if args.mode=='manifest':result=manifest()
    elif args.mode=='assess-cache':result=assess(json.loads(args.cache.read_text()),None if not args.supplement else json.loads(args.supplement.read_text()))
    else:result=snapshot(args.logs,None if not args.previous else json.loads(args.previous.read_text()))
    args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(str(args.output))


if __name__=='__main__':main()
