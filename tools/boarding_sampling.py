"""Conditional scheduling demonstration, NOT recovered historical PER lists.

Reuses length-verified replay caches. Invocation-only headers are retained:
absence of a new SPECIAL5 packet does not mean the writer did not execute.
The pure scheduler is cross-checked against generated PER by its test suite.
"""
import argparse
import json
from pathlib import Path

from compare_boarding_contacts import records
from generate_command_boundary import BOARDING_LATE_AGES, LIMIT, WINDOW

FIXTURE=Path(__file__).parent/'fixtures'/'boarding-sampling-windows.json'
CASES=[
    ('T56-Yellow', 't56', 4,35010,2204000,2240000, {7706:2223713,34730:2238899}),
    ('T56-Red', 't56', 2,40285,3676000,3719000, {34636:3718157,34616:3718480}),
    ('T56-Green', 't56', 3,40020,3617000,3629000, {34564:3627901}),
    ('T55B-Cyan', 't55b', 5,39461,5543000,5551000, {43834:5549578}),
]


class Schedule:
    def __init__(self, policy='reserved', exhausted_until=0):
        self.policy=policy;self.next=exhausted_until;self.left=0
        self.lanes=[0]*4;self.due=0;self.turn=False;self.hull=None;self.phase=None

    def call(self, now, site, hull, nonempty=True, pointer_valid=True, enabled=True):
        if not nonempty:return None
        if now>=self.next:
            self.next=now+WINDOW;self.left=LIMIT;self.lanes=[1]*4
        if self.policy=='old':
            if enabled and pointer_valid and self.left and now>=self.due:
                self.left-=1;self.due=now+3;return 'unreserved'
            return None
        if hull!=self.hull or site==20:
            self.hull=hull;self.phase=None;self.turn=False;self.due=0
        if site==21:self.phase=now
        if not pointer_valid or now<self.due:return None
        self.due=now+3
        lane=None
        if enabled:
            for i,age in reversed(list(enumerate(BOARDING_LATE_AGES,1))):
                if site!=25 and self.lanes[i] and self.phase is not None and now-self.phase>=age:
                    lane=i;break
            if lane is None and self.lanes[0] and self.turn:lane=0
        self.turn=True
        if lane is not None:
            self.lanes[lane]=0;self.left-=1;self.turn=False
            return ('early','loading12','loading20','loading28')[lane]
        return None


def demonstrate(case, exhausted=False):
    result={}
    for policy in ('old','reserved'):
        schedule=Schedule(policy, case['calls'][0]['ms']//1000+WINDOW if exhausted else 0)
        emitted=[]
        for c in case['calls']:
            lane=schedule.call(c['ms']//1000,c['schedule_site'],case['hull'])
            if lane:
                emitted.append(dict(ms=c['ms'],lane=lane,site=c['site'],
                    packet_sequence=c['packet_sequence'],header_sequence=c['header_sequence'],
                    packet_members=c['packet_members'],final_PER_selection='unknown'))
        result[policy]=emitted
    return result


def extract(directory):
    caches={name:json.loads((directory/(name+'-exact.json')).read_text()) for name in ('t55b','t56')}
    out=[]
    for name,cache,p,hull,start,end,onsets in CASES:
        d=caches[cache]
        packets=[e for e in d['events'] if start<=e['milliseconds']<=end and
                 e.get('player_id')==p and e['action']=='SPECIAL' and
                 e.get('order_id')==5 and e.get('target_id')==hull]
        headers=[r for r in records(d['diagnostics'],700,705) if r['player']==p and
                 start<=r['milliseconds']<=end and r['702']==hull]
        used=set();calls=[]
        for h in headers:
            matches=[e for e in packets if 0<=e['milliseconds']-h['milliseconds']<=100 and
                     e['sequence']>h['sequence'] and h['704'] in e['object_ids']]
            assert len(matches)<=1,(name,h)
            packet=matches[0] if matches else None
            if packet:used.add(packet['sequence'])
            calls.append(dict(ms=h['milliseconds'],site=h['700'],schedule_site=h['700'],
                time_basis='writer-header',header_sequence=h['sequence'],
                packet_sequence=packet['sequence'] if packet else None,
                packet_members=packet['object_ids'] if packet else None,
                reported_count=h['703'],reported_candidate=h['704'],
                modifier=h['701'],shared_clock=h['705']))
        for e in packets:
            if e['sequence'] in used:continue
            calls.append(dict(ms=e['milliseconds'],site=None,schedule_site=24,
                time_basis='packet-proxy; mining-writer association inferred',header_sequence=None,
                packet_sequence=e['sequence'],packet_members=e['object_ids']))
        calls.sort(key=lambda c:c['ms'])
        if calls[0]['site'] is None:calls[0]['schedule_site']=20
        # Validate the named onset packet, but do not export the replay itself.
        for actor,ms in onsets.items():
            assert any(e['milliseconds']==ms and e.get('player_id')==p and
                e['action']=='AI_ORDER' and e.get('order_id')==706 and actor in e['object_ids']
                for e in d['events']),(name,actor,ms)
        out.append(dict(name=name,replay_sha256=d['sha256'],player=p,hull=hull,
            onsets=[dict(actor=a,ms=t) for a,t in onsets.items()],calls=calls,
            uncertainty='No historical final PER list/order, valid pointer, paired positions or family allowance state. '
                        'Unheadered packets are conditional mining-call proxies; missing unlogged invocations remain possible.'))
    return dict(schema=1,scope='Four named onset windows, not all historical episodes or population coverage.',cases=out)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--extract',type=Path,help='directory containing existing corrected caches')
    args=parser.parse_args()
    if args.extract:FIXTURE.write_text(json.dumps(extract(args.extract),indent=2)+'\n')
    for case in json.loads(FIXTURE.read_text())['cases']:
        print(case['name'])
        for policy,rows in demonstrate(case).items():
            print(' ',policy,[(r['ms']/1000,r['lane']) for r in rows])
        print('  exhausted carry-in:', {k:len(v) for k,v in demonstrate(case,True).items()})


if __name__=='__main__':main()
