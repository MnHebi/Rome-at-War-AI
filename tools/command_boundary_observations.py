"""Decode bounded720+ records and validate paired measurements offline."""
import math
from collections import Counter
try:
    from generate_command_boundary import CODES, PREV
except ImportError:
    from tools.generate_command_boundary import CODES, PREV


def decode(pairs):
    names={v:k for k,v in CODES.items()}
    active={};frames=[];coverage=[];cov={}
    for d in pairs:
        name=names.get(d['diag_id']);p=d['player']
        if name is None:continue
        if name=='site':
            if p in active:active[p]['incomplete']=True
            frame=dict(player=p,site=d['value'],sequence=d['sequence'],ms=d['milliseconds'],members=[],incomplete=True)
            frames.append(frame);active[p]=frame
        elif name=='coverage-family':
            cov[p]=dict(player=p,family=d['value'],ms=d['milliseconds']);coverage.append(cov[p])
        elif p in cov and name in ('now','enabled','calls','nonempty','suppressed','detailed','missed','targets','invalid') and p not in active:
            cov[p][name]=d['value']
            if name=='invalid':cov.pop(p)
        elif p in active:
            f=active[p]
            if name=='index':f['members'].append(dict(index=d['value']))
            elif name=='end':
                f['incomplete']=d['value']!=f.get('serial');f['end_sequence']=d['sequence'];active.pop(p)
            elif f['members']:f['members'][-1][name]=d['value']
            else:f[name]=d['value']
    return frames,coverage


def frame_integrity(pairs):
    """Expose lost framing without inventing site/actor links from orphan tails.

    Counts describe recorded fields, not successful PER calls or the mechanism
    that lost them. In particular, zero decoded frames is not zero activity.
    """
    active={};counts=Counter();players={}
    for d in pairs:
        p,code=d['player'],d['diag_id']
        if code not in (CODES['site'],CODES['serial'],CODES['end']):continue
        row=players.setdefault(p,Counter())
        def add(key):
            counts[key]+=1;row[key]+=1
        if code==CODES['site']:
            add('starts')
            if p in active:add('abandoned_headers')
            active[p]=None
        elif code==CODES['serial']:
            if p in active:active[p]=d['value']
            else:add('orphan_serials')
        else:
            add('ends')
            if p not in active:add('orphan_ends')
            elif active.pop(p)!=d['value']:add('serial_mismatches')
    counts['unclosed_headers']=len(active)
    return dict(counts=dict(counts),by_player={p:dict(v) for p,v in players.items()},
                limitation='Orphan tails cannot identify their missing site or establish native origin.')


def paired_progress(frame,member,max_age=15,map_tiles=480):
    reasons=[]
    required=['actor','ax','ay','owner','group','elapsed',*['previous-'+n for n in PREV]]
    if frame.get('incomplete') or any(k not in member for k in required):
        return dict(valid=False,reasons=['incomplete-pair'])
    if frame.get('remote')!=1 or frame.get('tid')!=frame.get('reserved'):reasons.append('not-exact-reserved-hull')
    if member['actor']!=member['previous-actor'] or frame.get('tid')!=member['previous-hull']:reasons.append('identity-changed')
    if not 0<member['elapsed']<=max_age:reasons.append('stale-or-same-time')
    if member['elapsed']!=frame.get('now',0)-member['previous-time']:reasons.append('time-mismatch')
    if member['owner']!=frame['player'] or member['owner']!=member['previous-owner'] or member['group']!=member['previous-group'] or member['group']!=11:reasons.append('passenger-ownership')
    if frame.get('towner')!=frame['player'] or frame.get('towner')!=member['previous-howner'] or frame.get('tgroup')!=member['previous-hgroup'] or frame.get('tgroup')!=10:reasons.append('hull-ownership')
    if member.get('previous-member')!=1:reasons.append('no-final-membership-proof')
    coords=[member[k] for k in ('ax','ay','previous-x','previous-y','previous-hx','previous-hy')]+[frame.get('tx',-2),frame.get('ty',-2)]
    if any(not 0<=v<map_tiles*100 for v in coords):reasons.append('invalid-position')
    if reasons:return dict(valid=False,reasons=reasons)
    actor_move=math.hypot(member['ax']-member['previous-x'],member['ay']-member['previous-y'])/100
    hull_move=math.hypot(frame['tx']-member['previous-hx'],frame['ty']-member['previous-hy'])/100
    before=math.hypot(member['previous-x']-member['previous-hx'],member['previous-y']-member['previous-hy'])/100
    after=math.hypot(member['ax']-frame['tx'],member['ay']-frame['ty'])/100
    return dict(valid=True,actor_displacement=actor_move,hull_displacement=hull_move,
                separation_before=before,separation_after=after,
                limitation='Displacement is not path progress or proof that a detour is useless.')


def correlate(frames,events,window_ms=100):
    """A decoded packet corroborates invocation; absence never proves native origin."""
    packets=[e for e in events if e['action'] in ('WORK','ORDER','SPECIAL')]
    result=[]
    for f in frames:
        for m in f['members']:
            matches=[e for e in packets if e.get('player_id')==f['player'] and m.get('actor') in e.get('object_ids',[])
                     and e.get('target_id')==f.get('tid') and abs(e['milliseconds']-f['ms'])<=window_ms
                     and (f.get('family')!=1 or (e['action']=='SPECIAL' and e.get('order_id')==5))]
            result.append(dict(player=f['player'],actor=m.get('actor'),site=f['site'],serial=f.get('serial'),
                complete=not f['incomplete'],covered_target_count=1,total_targets=f.get('remote'),
                packet_sequences=[e['sequence'] for e in matches],
                invocation='nonempty-command-site' if f.get('local',0)>0 and f.get('remote',0)>0 else 'empty-or-unknown',
                first706_ms=next((e['milliseconds'] for e in events if e.get('player_id')==f['player']
                    and m.get('actor') in e.get('object_ids',[]) and e['action']=='AI_ORDER' and e.get('order_id')==706
                    and f['ms']<=e['milliseconds']<=f['ms']+30000),None),
                task_outcome='not-established-by-command-packet',
                status='matching-packet' if len(matches)==1 else 'ambiguous' if matches else 'unmatched-not-native-proof',
                progress=paired_progress(f,m) if f.get('family')==1 else None))
    return result


if __name__=='__main__':
    import argparse
    import json
    from pathlib import Path
    p=argparse.ArgumentParser();p.add_argument('cache',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
    data=json.loads(a.cache.read_text());frames,coverage=decode(data['diagnostics'])
    result=dict(source_sha256=data.get('sha256'),frames=frames,coverage=coverage,
                frame_integrity=frame_integrity(data['diagnostics']),
                correlations=correlate(frames,data['events']),
                limitations=['No sampled message is not proof of native origin.',
                             'Only emitted actors and target0 have command-boundary coverage.',
                             'Movement and task success require follow-up evidence.'])
    a.output.write_text(json.dumps(result,indent=2)+'\n')
