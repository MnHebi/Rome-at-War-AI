"""Execute coastal PER rules; supplied geometry is NOT an engine simulation."""
import math
import re
from test_assault_missions import Missions
from test_pre_backlog import expressions, source
from validate_naval_doctrine import rule_blocks


class CoastalFixture(Missions):
    def __init__(self, filename, defs):
        super().__init__()
        self.constants.update({k:int(v) for k,v in re.findall(r'\(defconst ([\w-]+) (-?\d+)\)', source(defs))})
        self.rules=list(rule_blocks(source(filename)))
        self.objects={}; self.groups={}; self.disabled=set(); self.now=100
        self.counts={}; self.pending=0; self.placement=False; self.affordable=True
        self.buildable=True; self.age=self.val('middle-antiquity-age'); self.wood=500
        self.zone_at=lambda p: 8 if p[0]>=52 else 3
        self.pathable=lambda obj,p,exact: True
        self.can_site=lambda p: True
        self.path_queries=[]; self.builds=[]; self.status=None; self.point=(0,0)
        self.local_kind=None; self.local_cursor=0

    def pair(self,name):
        return self.point if name=='0' else (self.g.get(name,0), self.g.get(name[:-1]+'y',0))

    def data(self,field,target=False):
        if field=='object-data-status': return self.val(str(self.objects.get(self.target,{}).get('status','status-ready')))
        if field=='object-data-class': return self.val(str(self.objects.get(self.target,{}).get('cls',-1)))
        if field=='object-data-index':
            return (self.local if self.target in self.local else self.remote).index(self.target)
        return super().data(field,target)

    def fact(self,e):
        op,*a=e
        if op=='stance-toward':
            p=self.players.get(int(a[0]),{})
            return p.get('enemy',False) if a[1]=='enemy' else not p.get('enemy',True)
        if op in ('building-type-count','building-type-count-total','unit-type-count','unit-type-count-total'):
            return self.compare(self.counts.get(a[0],0),a[1],a[2])
        if op=='current-age': return self.compare(self.age,a[0],a[1])
        if op=='wood-amount': return self.compare(self.wood,a[0],a[1])
        if op in ('can-build','can-afford-building'): return self.affordable and self.buildable
        if op=='up-pending-objects': return self.compare(self.pending,a[2],a[3])
        if op=='up-pending-placement': return self.placement
        if op=='up-can-build-line':
            assert a[0]=='0'
            return self.can_site(self.pair(a[1]))
        if op=='up-path-distance':
            p=self.pair(a[0]); exact=a[1]=='1'; o=self.objects[self.target]
            self.path_queries.append((self.target,p,exact))
            distance=math.dist(o['point'],p) if self.pathable(o,p,exact) else 65535
            return self.compare(distance,a[2],a[3])
        return super().fact(e)

    def action(self,e,pc=0):
        op,*a=e
        if op=='up-get-fact' and a[0]!='game-time':
            self.g[a[-1]]=self.counts.get(a[0],0)
        elif op=='up-modify-goal':
            v=self.sn.get(a[2],0) if a[1].startswith('s:') else self.operand(a[1],a[2])
            old=self.g.get(a[0],0); operator=a[1].split(':')[-1]
            self.g[a[0]]={'=':lambda:v,'+':lambda:old+v,'-':lambda:old-v,
                'min':lambda:min(old,v),'max':lambda:max(old,v),'mod':lambda:old%v,
                '/':lambda:int(old/v),'*':lambda:old*v}[operator]()
        elif op=='up-get-point-zone': self.g[a[1]]=self.zone_at(self.pair(a[0]))
        elif op=='up-bound-point':
            self.g[a[0]],self.g[a[0][:-1]+'y']=(min(239,max(0,v)) for v in self.pair(a[1]))
        elif op=='up-get-point-distance':
            assert len(a)==3
            self.g[a[2]]=math.dist(self.pair(a[0]),self.pair(a[1]))
        elif op in ('up-cross-tiles','up-lerp-tiles'):
            p,q=self.pair(a[0]),self.pair(a[1]); d=self.operand(a[2],a[3]); dx,dy=q[0]-p[0],q[1]-p[1]; n=math.hypot(dx,dy) or 1
            x,y=(p[0]+dy*d/n,p[1]-dx*d/n) if op=='up-cross-tiles' else (p[0]+dx*d/n,p[1]+dy*d/n)
            self.g[a[0]],self.g[a[0][:-1]+'y']=x,y
        elif op=='up-full-reset-search':
            self.status=None
            self.local_kind=None; self.local_cursor=0
            return super().action(e,pc)
        elif op=='up-reset-search':
            assert len(a)==4 and all(v in ('0','1') for v in a)
            if a[0]=='1':self.local_kind=None; self.local_cursor=0
            if a[1]=='1':self.local=[]
            if a[3]=='1':self.remote=[]
        elif op=='up-filter-status': self.status=self.val(a[1])
        elif op in ('up-find-local','up-find-status-local'):
            status=self.val('status-ready') if op=='up-find-local' else self.status
            items=[i for i,o in self.objects.items() if o['player']==2 and a[1] in (o.get('type'),o.get('cls'))]
            if self.local_kind!=a[1]:self.local_kind=a[1];self.local_cursor=0
            found=[]
            for index in range(self.local_cursor,len(items)):
                self.local_cursor=index+1;i=items[index];o=self.objects[i]
                if (self.minradius<=math.dist(o['point'],self.point)<=self.radius
                    and (status is None or self.val(str(o.get('status','status-ready')))==status)):
                    found.append(i)
                    if len(found)>=self.val(a[-1]):break
            self.local += [i for i in found if i not in self.local][:240-len(self.local)]
        elif op=='up-find-remote':
            # Cached AIRef: remote capacity is 40, not local's 240. Search
            # classes find ready objects; concrete IDs may find pending ones.
            items=[i for i,o in self.objects.items() if o['player']==self.sn.get('sn-focus-player-number')
                and a[1] in (o.get('type'),o.get('cls'))
                and self.minradius<=math.dist(o['point'],self.point)<=self.radius
                and (not a[1].endswith('-class') or o.get('status','status-ready')=='status-ready')]
            self.remote += [i for i in items[:self.val(a[-1])] if i not in self.remote][:40-len(self.remote)]
        elif op=='up-build-line':
            assert a[0]==a[1]
            self.builds.append((a[-1],self.pair(a[0])))
        elif op=='disable-self': self.disabled.add(pc)
        else: return super().action(e,pc)
        return 0

    def add(self,i,kind,point,**kw):
        self.objects[i]=dict(id=i,player=2,hp=100,under_attack=0,cargo=0,garrisoned=0,flag=-2,
            point=point,zone=8,type=kind,cls=kind,idle=1,attacker=-1,action='actionid-idle',status='status-ready')
        self.objects[i].update(kw)


class ShipyardFixture(CoastalFixture):
    def __init__(self):
        super().__init__('rawai-specialplacement.per','rawai-shipyard-defs.per')
        self.g.update({'map-type':self.val('ISLANDS'),'desired-number-shipyards':8,
            'shipyard-placement-state':self.val('SHIPYARD-IDLE'),'gl-boar-lurer-id':-1})
        self.counts={'port':1,'shipyard':0}
        self.add(1,'port',(40,50)); self.add(2,'warship-class',(75,50)); self.add(3,'villager-class',(45,50),zone=3)
