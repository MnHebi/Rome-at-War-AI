"""Incremental RAW58 DE engine-log decoder and preflight/correlation CLI.

The per-player token stream is explicitly framed and checksummed. Missing data
is never filled from another event/player or the replay. Originals stay intact.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re

BEGIN=-2147483001
END=-2147483002
ESCAPE=-2147483003
TOKEN=re.compile(r'RAW58P([1-8]) (-?\d+)\s*$')
HEADER=9
MAX_FRAME=1024
LENGTHS={1:24,2:1,10:15,11:15,12:8,20:3,21:17,22:16,23:4,30:2,31:11,32:2,40:8,41:4,90:1}


def checksum(values):
    result=0
    for value in values: result=(result*31+value%65521)%65521
    return result


def decode_logs(paths,stats=None):
    """Yield framed records/failures; only one bounded frame/player in RAM.

    Paths must be chronological engine log segments from one capture. Missing
    parts can produce only explicit failures, never synthetic complete frames.
    """
    stats=stats if stats is not None else Counter()
    buffers={};last={};escaped=set()
    for path in paths:
        with Path(path).open('r',encoding='utf-8-sig',errors='replace') as stream:
            for line_no,line in enumerate(stream,1):
                stats['lines']+=1;stats['bytes_read']+=len(line.encode('utf-8'))
                match=TOKEN.search(line.rstrip())
                if not match:stats['unrelated_lines']+=1;continue
                player,value=map(int,match.groups());stats['tokens']+=1
                literal=player in escaped
                if literal:escaped.remove(player)
                elif value==ESCAPE:
                    escaped.add(player);continue
                if value==BEGIN and not literal:
                    if player in buffers:
                        stats['abandoned']+=1
                        yield dict(complete=False,player=player,error='new-header-before-tail',source=str(path),line=line_no)
                    buffers[player]=[value];continue
                if player not in buffers:
                    stats['orphan_tokens']+=1;continue
                frame=buffers[player];frame.append(value)
                if len(frame)>MAX_FRAME:
                    buffers.pop(player);stats['oversized']+=1
                    yield dict(complete=False,player=player,error='oversized-frame');continue
                # A data value equal to END is legal; use declared frame length,
                # not a blind sentinel scan. Header corruption stays incomplete.
                if len(frame)<HEADER:continue
                count=frame[8]
                expected=HEADER+count+4
                if not 0<=count<=MAX_FRAME-HEADER-4:
                    buffers.pop(player);stats['invalid_length']+=1
                    yield dict(complete=False,player=player,error='invalid-declared-length');continue
                if len(frame)<expected:continue
                buffers.pop(player)
                schema,session,record,event,typ,site,seconds=frame[1:8]
                payload=frame[:HEADER+count];n,check,tail_event,end=frame[-4:]
                errors=[]
                if schema!=58:errors.append('schema')
                if LENGTHS.get(typ)!=count:errors.append('record-shape')
                if n!=len(payload):errors.append('count')
                if check!=checksum(payload):errors.append('checksum')
                if event!=tail_event:errors.append('serial')
                if end!=END:errors.append('tail')
                key=(player,session);prev=last.get(key)
                if prev is not None and record<=prev:errors.append('duplicate-or-reordered')
                if prev is not None and record>prev+1:stats['record_gaps']+=record-prev-1
                if not errors:last[key]=record
                stats['complete' if not errors else 'incomplete']+=1
                yield dict(complete=not errors,errors=errors,player=player,session=session,
                    record=record,event=event,type=typ,site=site,game_seconds=seconds,
                    values=frame[HEADER:-4],source=str(path),line=line_no)
    for player,frame in buffers.items():
        stats['truncated_tails']+=1
        yield dict(complete=False,player=player,error='truncated-tail',tokens=len(frame))
    for player in escaped:
        stats['dangling_escape']+=1
        yield dict(complete=False,player=player,error='dangling-escape')


def classify_events(events,minimum=100):
    """T57 ORDER <=100ms same-target /706 <=1s; WORK explicitly <=1s same-target.

    Consecutive means consecutive packets of that family for an actor. Other
    families do not erase a run; a changed target breaks ORDER/WORK runs.
    Counts separate distinct packet sequences from actor incidences.
    """
    by=defaultdict(list);packets=defaultdict(set);inc=Counter()
    for e in events:
        family=e.get('action')
        if family=='AI_ORDER':
            if e.get('order_id')!=706:continue
            family='706'
        if family not in ('ORDER','WORK','706','STOP'):continue
        packets[family].add(e['sequence'])
        for actor in set(e.get('object_ids',[])):
            inc[family]+=1;by[(e.get('player_id'),actor,family)].append(e)
    runs=[]
    for (player,actor,family),rows in by.items():
        if family=='STOP':continue
        rows.sort(key=lambda e:(e['milliseconds'],e['sequence']))
        groups=[];gap=100 if family=='ORDER' else 1000
        for e in rows:
            if (not groups or e['milliseconds']-groups[-1][-1]['milliseconds']>gap or
                family!='706' and e.get('target_id')!=groups[-1][-1].get('target_id')):groups.append([])
            groups[-1].append(e)
        for group in groups:
            if len(group)<minimum:continue
            runs.append(dict(player=player,actor=actor,family=family,target=group[0].get('target_id'),
                first_ms=group[0]['milliseconds'],last_ms=group[-1]['milliseconds'],
                first_sequence=group[0]['sequence'],packets=len(group)))
    return dict(runs=sorted(runs,key=lambda x:x['first_ms']),
        counts={f:dict(distinct_packets=len(packets[f]),actor_incidences=inc[f]) for f in ('ORDER','WORK','706','STOP')},
        definitions=dict(minimum=minimum,ORDER_gap_ms=100,WORK_gap_ms=1000,AI_ORDER706_gap_ms=1000))


def observations(records):
    """Bounded per-player assembly; subrecord loss is a logical coverage gap."""
    active={}
    for r in records:
        player=r['player']
        if not r.get('complete'):
            if player in active:active[player]['gaps'].append('damaged-record')
            continue
        if r['type']==1:
            if player in active:
                old=active.pop(player);old['gaps'].append('missing-observation-tail');yield old
            active[player]=dict(entry=r,local=[],remote=[],gaps=[],last_record=r['record'],finished=False)
            continue
        f=active.get(player)
        if not f:continue
        if (r['session'],r['event'])!=(f['entry']['session'],f['entry']['event']):
            f['gaps'].append('event-identity-changed');active.pop(player);yield f;continue
        if r['record']!=f['last_record']+1:f['gaps'].append('missing-subrecords')
        f['last_record']=r['record']
        if r['type'] in (10,11):f['local' if r['type']==10 else 'remote'].append(r['values'])
        if r['type']==90:f['gaps'].append({'observer-failure':r['values']})
        if r['type']==2:
            f['finished']=True;f['end']=r
            if r['values']!=[f['entry']['values'][0]]:f['gaps'].append('observation-kind-mismatch')
            if f['entry']['values'][0] in (0,1,5):
                for name,count in zip(('local','remote'),f['entry']['values'][1:3]):
                    if not 0<=count<=241 or [row[0] for row in f[name]]!=list(range(count)):
                        f['gaps'].append(name+'-list-incomplete')
                    if any(row[1]!=1 or row[2]<0 for row in f[name]):f['gaps'].append(name+'-unknown-object')
            active.pop(player);yield f
    for f in active.values():
        f['gaps'].append('truncated-observation');yield f


def correlations(records,events,registry):
    """Require intact PRE plus INVOKED. Whole-second timing is only a candidate."""
    from audit_writer_trace import compatible
    commands={c['id']:c for s in registry['sites'] for c in s.get('file_commands',[])}
    buckets=defaultdict(list)
    for e in events:buckets[(e.get('player_id'),e['milliseconds']//1000)].append(e)
    pending={}
    for f in observations(records):
        entry=f['entry'];player=entry['player'];kind=entry['values'][0]
        if kind in (1,3):
            pending[player]=f;continue
        pre=pending.pop(player,None)
        if not pre or kind not in (2,5,6,7):continue
        a=pre['entry'];c=commands.get(a['site'])
        gaps=pre['gaps']+f['gaps']
        if (a['session'],a['event']+1,a['site'])!=(entry['session'],entry['event'],entry['site']):
            gaps.append('PRE-INVOKED-mismatch')
        actors=[v[2] for v in pre['local'] if v[1]==1]
        targets=[v[2] for v in pre['remote'] if v[1]==1]
        candidates=[]
        if c and not gaps and not c['indirect']:
            for second in range(a['game_seconds'],entry['game_seconds']+1):
                for e in buckets[(player,second)]:
                    ids=set(e.get('object_ids',[]))
                    if (ids and ids<=set(actors) and (not targets or e.get('target_id') in targets)
                        and compatible(e,{'actions':c['command']})):
                        candidates.append(e['sequence'])
        yield dict(player=player,event=a['event'],site=a['site'],actors=actors,targets=targets,
            coverage_gaps=gaps,packet_sequences=candidates,
            status='incomplete-inputs' if gaps else 'indirect-recipients-unknown' if c and c['indirect'] else
                   'ambiguous' if len(candidates)>1 else 'candidate-not-causation' if candidates else 'unmatched-not-native-proof',
            timing='PRE through INVOKED whole game-second buckets; subsets may be native expansion')


def actor_timelines(cache,classification):
    """Exact packet subsequence, not inferred simulation state or successful tasks."""
    pairs={(r['player'],r['actor']) for r in classification['runs']}
    pairs.update((8,a) for a in (34329,33901,35048,34455))
    rows=defaultdict(list)
    for e in cache['events']:
        for actor in set(e.get('object_ids',[])):
            key=e.get('player_id'),actor
            if key in pairs:rows[key].append(e)
    result=[]
    for key,events in sorted(rows.items()):
        runs=[r for r in classification['runs'] if (r['player'],r['actor'])==key]
        if not runs:continue
        onset=min(r['first_ms'] for r in runs)
        before=[e for e in events if e['milliseconds']<=onset]
        boards=[e for e in before if e['action']=='SPECIAL' and e.get('order_id')==5]
        board=boards[-1] if boards else None
        anchor=board['milliseconds'] if board else onset
        prior=[e for e in before if e['milliseconds']<anchor and e['action'] in ('ORDER','WORK','MOVE','SPECIAL','STOP')]
        # Store changes rather than duplicate streams; first/last sequences remain exact.
        changes=[]
        for e in events:
            if e['milliseconds']<anchor:continue
            signature=(e['action'],e.get('order_id'),e.get('target_id'))
            if changes and changes[-1]['signature']==signature:
                changes[-1]['last_ms']=e['milliseconds'];changes[-1]['last_sequence']=e['sequence'];changes[-1]['packets']+=1
            else:changes.append(dict(signature=signature,first_ms=e['milliseconds'],last_ms=e['milliseconds'],
                first_sequence=e['sequence'],last_sequence=e['sequence'],packets=1))
        result.append(dict(player=key[0],actor=key[1],last_assignment=prior[-1] if prior else None,
            last_boarding_before_onset=board,first_dense_ORDER=next((r for r in runs if r['family']=='ORDER'),None),
            first_dense_WORK=next((r for r in runs if r['family']=='WORK'),None),
            first706=next((e for e in events if e['action']=='AI_ORDER' and e.get('order_id')==706),None),
            task_packet_changes=changes,termination='UNKNOWN unless explicit delete; last packet is not recovery',
            last_observed_ms=events[-1]['milliseconds']))
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--logs',type=Path,nargs='+',required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--manifest',type=Path,required=True)
    p.add_argument('--cache',type=Path)
    p.add_argument('--registry',type=Path,default=Path(__file__).resolve().parents[1]/'command-boundary-registry.json')
    p.add_argument('--expected-players',type=int,nargs='+',default=list(range(1,9)))
    p.add_argument('--wall-seconds',type=float,help='Measured capture wall duration, not simulation time')
    a=p.parse_args();manifest=json.loads(a.manifest.read_text());stats=Counter();players=set();startup=set();multi=set();boarding=set()
    registry=json.loads(a.registry.read_text());cmds={c['id']:c for s in registry['sites'] for c in s.get('file_commands',[])}
    records_path=a.output.with_suffix('.records.jsonl');identities={};seconds={};peaks=[0,0];per_player=Counter()
    with records_path.open('w',encoding='utf-8') as out:
        for r in decode_logs(a.logs,stats):
            out.write(json.dumps(r)+'\n')
            if not r.get('complete'):continue
            players.add(r['player'])
            per_player[r['player']]+=1
            lo,hi=seconds.get(r['player'],(r['game_seconds'],r['game_seconds']))
            seconds[r['player']]=(min(lo,r['game_seconds']),max(hi,r['game_seconds']))
            if r['type']==40:identities[str(r['player'])]=r['values']
            if r['type']==1:
                peaks=[max(x,y) for x,y in zip(peaks,r['values'][1:3])]
            if r['type']==1 and r['values'][0]==0:startup.add(r['player'])
            if r['type']==1 and r['values'][1]>1:multi.add(r['player'])
            if r['type']==1 and 'action-garrison' in cmds.get(r['site'],{}).get('command',''):boarding.add(r['player'])
    source_files=[dict(path=str(x),bytes=x.stat().st_size,mtime_ns=x.stat().st_mtime_ns) for x in a.logs]
    result=dict(status='ENGINE PREFLIGHT PENDING',stats=dict(stats),players=sorted(players),
        startup_players=sorted(startup),multi_actor_entry_players=sorted(multi),boarding_entry_players=sorted(boarding),
        missing_players=sorted(set(a.expected_players)-players),files=source_files,
        manifest_sha256=hashlib.sha256(a.manifest.read_bytes()).hexdigest(),manifest=manifest,
        records=str(records_path),limitations=['Framing alone is not an ordinary-command or boarding execution PASS.',
        'Shared engine log volume includes unrelated engine output. No script/runtime slowdown measured offline.',
        'Missing writers/packets are unknown, not native proof. Session and payload matching require preflight verification.'])
    result['source_identity_words']=identities
    from command_boundary_file import identity_words
    result['registry_matches_manifest']=identity_words(registry)==manifest.get('source_identity_words')
    result['identity_mismatch_players']=[p for p,words in identities.items() if words!=manifest.get('source_identity_words')]
    result['identity_note']='Source map fingerprint, NOT full installed payload hash; verify manifest against installed bytes before capture.'
    result['cost']=dict(max_local=peaks[0],max_remote=peaks[1],
        records_per_game_second={p:per_player[p]/max(1,hi-lo) for p,(lo,hi) in seconds.items()},
        bytes_per_wall_minute=None if not a.wall_seconds else stats['bytes_read']*60/a.wall_seconds,
        projected_three_wall_hours_bytes=None if not a.wall_seconds else stats['bytes_read']*10800/a.wall_seconds,
        runtime_slowdown='UNMEASURED; no engine execution performed by parser')
    if a.cache:
        cache=json.loads(a.cache.read_text())
        result['replay_sha256']=cache.get('sha256')
        result['floods']=classify_events(cache['events'])
        result['actor_timelines']=actor_timelines(cache,result['floods'])
        result['correlation_status_counts']=dict()
        if result['identity_mismatch_players'] or not identities or not result['registry_matches_manifest']:
            result['correlation_blocked']='Missing or mismatched startup source identity; no writer joins attempted.'
        else:
            correlation_path=a.output.with_suffix('.correlations.jsonl');counts=Counter()
            with records_path.open() as inp, correlation_path.open('w',encoding='utf-8') as out:
                for row in correlations((json.loads(line) for line in inp),cache['events'],registry):
                    if str(row['player']) not in identities:continue
                    out.write(json.dumps(row)+'\n');counts[row['status']]+=1
            result['correlations']=str(correlation_path);result['correlation_status_counts']=dict(counts)
    a.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k in ('status','stats','missing_players','records')},indent=2))


if __name__=='__main__':main()
