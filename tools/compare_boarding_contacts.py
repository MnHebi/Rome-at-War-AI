"""Matched contacts from verified caches. No simulation-state inference."""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path

try:
    from audit_boarding_flood_onsets import summarize
except ImportError:
    from tools.audit_boarding_flood_onsets import summarize


def records(pairs, first, last):
    open_records, result = {}, []
    for d in pairs:
        p, code = d['player'], d['diag_id']
        if code == first:
            open_records[p] = dict(player=p, milliseconds=d['milliseconds'], sequence=d['sequence'])
        if p in open_records and first <= code <= last:
            open_records[p][str(code)] = d['value']
            if code == last:
                result.append(open_records.pop(p))
    return result


def compare(events, known_actors, known_hulls, follow_ms=30000, diagnostics=()):
    """Negative = fully followed command, not proof of successful boarding.

    Follow-up is censored at replay end, explicit DELETE, or the last later
    command observation of the same player/actor. Replay survival alone is not
    evidence that a quiet actor remained alive/owned throughout the window.
    Known identity is supplied separately, never inferred from absent flooding.
    Overlapping contact windows are associations, not independent trials.
    """
    rows = sorted(events, key=lambda e:(e['milliseconds'], e['sequence']))
    end = max((e['milliseconds'] for e in rows), default=0)
    bursts = defaultdict(list)
    for b in summarize(rows):
        bursts[b['player'], b['actor']].append(b)
    by_actor, death = defaultdict(list), {}
    for e in rows:
        for actor in set(e.get('object_ids', [])):
            key = e.get('player_id'), actor
            by_actor[key].append(e)
            if e['action'] == 'DELETE': death.setdefault(key, e['milliseconds'])
    states = defaultdict(list)
    for s in records(diagnostics, 706, 718):
        if s.get('710') == 1: states[s['player'], s['706']].append(s)
    stages=defaultdict(list)
    for d in diagnostics:
        if d['diag_id']==550:stages[d['player']].append(d)
    contacts, prior, run = [], {}, Counter()
    exclusions = Counter()
    for e in rows:
        if e['action'] != 'SPECIAL' or e.get('order_id') != 5: continue
        p, hull, now = e.get('player_id'), e.get('target_id'), e['milliseconds']
        for actor in set(e.get('object_ids', [])):
            key = p, actor
            if key not in known_actors or (p,hull) not in known_hulls:
                exclusions['unresolved_actor_or_hull'] += 1; continue
            previous = prior.get(key)
            kind = ('first-observed-hull' if previous is None else
                    'same-hull-renewal' if previous[0] == hull else 'different-hull')
            if kind != 'same-hull-renewal': run[key] = 0
            else: run[key] += 1
            active = next((b for b in bursts[key] if
                (b['first_ms'], b['first_sequence']) <= (now,e['sequence']) <=
                (b['last_ms'], 10**20)), None)
            onsets = [b for b in bursts[key] if
                      (now,e['sequence']) < (b['first_ms'],b['first_sequence']) and b['first_ms'] <= now+follow_ms]
            actor_last=max((x['milliseconds'] for x in by_actor[key]),default=now)
            complete = now+follow_ms <= min(end, death.get(key,end),actor_last)
            future = [x for x in by_actor[key] if (now,e['sequence']) < (x['milliseconds'],x['sequence'])
                      and x['milliseconds'] <= now+follow_ms]
            any706 = any(x['action']=='AI_ORDER' and x.get('order_id')==706 for x in future)
            outcome = ('already-active' if active else 'sustained-onset' if onsets else
                       'censored' if not complete else 'isolated706-only' if any706 else 'no706-in-window')
            near = [x for x in by_actor[key] if now-5000 <= x['milliseconds'] <= now+5000 and x['action'] in ('WORK','ORDER','STOP')]
            snapshot = next((s for s in reversed(states[key]) if s['milliseconds'] <= now), None)
            stage=next((s for s in reversed(stages[p]) if s['milliseconds']<=now),None)
            emit_age=None if snapshot is None else now-snapshot['milliseconds']
            clock_age=None if snapshot is None else now-snapshot['711']*1000
            contacts.append(dict(player=p,actor=actor,hull=hull,ms=now,sequence=e['sequence'],offset=e.get('offset'),
                kind=kind,outcome=outcome,followup_complete=complete,renewals=run[key],
                spacing_ms=None if previous is None else now-previous[1],
                onset_ms=onsets[0]['first_ms'] if onsets else None,
                nearby_counts=dict(Counter(x['action'] for x in near)),
                nearby_targets=sorted({(x['action'], x.get('target_id',-1)) for x in near}),
                state=snapshot, state_age_ms=emit_age, state_clock_age_ms=clock_age,
                actor_last_observed_ms=actor_last,
                migration_stage=None if stage is None else stage['value'],
                migration_stage_age_ms=None if stage is None else now-stage['milliseconds'],
                state_fresh=snapshot is not None and 0<=emit_age<=1000 and 0<=clock_age<=1000
                            and snapshot.get('707')==hull))
            prior[key] = hull,now
    totals=Counter((r['kind'],r['outcome']) for r in contacts)
    return dict(window_ms=follow_ms,replay_end_ms=end,contacts=contacts,
        denominators=[dict(kind=k[0],outcome=k[1],count=v) for k,v in sorted(totals.items())],
        actor_incidences=len(contacts), unique_packets=len({r['sequence'] for r in contacts}),
        actors=len({(r['player'],r['actor']) for r in contacts}),exclusions=dict(exclusions))


def cohorts(cache):
    """Within-affected-actor cohort + independently mining-site-linked T56 cohort.

    Whole cohort is explicitly NOT a population estimate. T56 adds nonflooding
    peers through the five mining-only source sites, independent of706 outcome.
    Only exact array/target matches within100ms of complete diagnostics qualify.
    """
    e,d=cache['events'],cache['diagnostics']
    actors={(b['player'],b['actor']) for b in summarize(e)}
    hulls={(x['player'],x['value']) for x in d if x['diag_id'] in (552,563,702) and x['value']>0}
    linked=[]
    garrisons=[x for x in e if x['action']=='SPECIAL' and x.get('order_id')==5]
    # 719 is interleaved before704/705;705 ends the T56 issuance header.
    headers=records(d,700,705)
    for h in headers:
        if h.get('700') not in (20,21,23,24,25) or h.get('701')!=2:continue
        candidates=[x for x in garrisons if x.get('player_id')==h['player'] and x.get('target_id')==h.get('702')
                    and len(x.get('object_ids',[]))==h.get('703') and abs(x['milliseconds']-h['milliseconds'])<=100]
        if len(candidates)!=1:continue
        x=candidates[0];hulls.add((h['player'],h['702']))
        actors.update((h['player'],a) for a in x['object_ids'])
        linked.append(dict(writer=h['700'],sequence=x['sequence'],player=h['player'],hull=h['702'],actors=x['object_ids']))
    return actors,hulls,linked


if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('cache',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
    cache=json.loads(a.cache.read_text());actors,hulls,linked=cohorts(cache)
    result=compare(cache['events'],actors,hulls,diagnostics=cache['diagnostics'])
    result.update(source_sha256=cache.get('sha256'),mining_site_links=linked,
        cohort='within affected actors plus T56 mining-site-selected peers; not population incidence')
    a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('contacts','mining_site_links')},indent=2))
