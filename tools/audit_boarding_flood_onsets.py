"""Offline exact-actor 706 episodes; correlation is not writer attribution.

Input is read_stream's length-verified object-array cache, not the broad parser's
AI_ORDER actor list. Counts are per-actor packet references, not unique packets.
STOP counts address explicit STOP only; other commands may also interrupt work.
"""
from collections import defaultdict
import argparse
import json
from pathlib import Path

def summarize(events, gap_ms=1000, minimum_packets=100, window_ms=30000):
    if gap_ms < 0 or minimum_packets < 1 or window_ms < 0:
        raise ValueError('invalid episode thresholds')
    def position(e):
        return e['milliseconds'], e['sequence']
    def is_flood(e):
        return e.get('action') == 'AI_ORDER' and e.get('order_id') == 706
    actors=defaultdict(list)
    for e in events:
        for actor in set(e.get('object_ids', [])):
            actors[(e.get('player_id'),actor)].append(e)
    result=[]
    for (player,actor), rows in actors.items():
        rows.sort(key=position)
        bursts=[]
        for e in rows:
            if not is_flood(e): continue
            if not bursts or e['milliseconds']-bursts[-1][-1]['milliseconds']>gap_ms: bursts.append([])
            bursts[-1].append(e)
        for burst in bursts:
            if len(burst)<minimum_packets: continue
            first,last=burst[0],burst[-1]
            nearby=[e for e in rows if first['milliseconds']-window_ms<=e['milliseconds']<=first['milliseconds']+5000 and not is_flood(e)]
            compact=[]
            for e in nearby:
                key=tuple(e.get(k) for k in ('action','order_id','target_id','x','y'))
                if compact and compact[-1]['key']==key and compact[-1]['actors']==e.get('object_ids'):
                    compact[-1]['last_ms']=e['milliseconds']; compact[-1]['count']+=1
                else: compact.append(dict(key=key,first_ms=e['milliseconds'],last_ms=e['milliseconds'],count=1,sequence=e['sequence'],offset=e.get('offset'),actors=e.get('object_ids')))
            pre_stop=[e for e in rows if e['action']=='STOP' and first['milliseconds']-window_ms<=e['milliseconds'] and position(e)<position(first)]
            during_stop=[e for e in rows if e['action']=='STOP' and position(first)<=position(e)<=position(last)]
            result.append(dict(player=player,actor=actor,first_ms=first['milliseconds'],last_ms=last['milliseconds'],packets=len(burst),
                first_sequence=first['sequence'],first_offset=first.get('offset'),pre_stop=len(pre_stop),during_stop=len(during_stop),nearby_commands=compact))
    return sorted(result,key=lambda r:(r['first_ms'],r['player'] or 0,r['actor']))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('cache',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
    source=json.loads(a.cache.read_text()); rows=summarize(source['events'])
    a.output.write_text(json.dumps(dict(source_sha256=source.get('sha256'),episodes=rows,gap_ms=1000,minimum_packets=100),indent=2))
    print('episodes',len(rows),'actors',len({(r['player'],r['actor']) for r in rows}))
    for r in rows:
        print(r['player'],r['actor'],round(r['first_ms']/1000,3),round(r['last_ms']/1000,3),r['packets'],'stops',r['pre_stop'],r['during_stop'],
              [(x['key'][:3],round(x['first_ms']/1000,3),x['count']) for x in r['nearby_commands']])
