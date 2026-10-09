"""Execute generated voyage scripts, including legacy open and queued events.

This bounded harness uses 30-day test months. Generated native durations are
checked separately; calendar arithmetic, GUI rendering and engine saves still
need an in-game playtest.
"""
from copy import deepcopy
from verify_harbor_bargains import World
from verify_055 import parse, flatten
from exploration_progress import FILES
from exploration import ROUTES


class Voyages(World):
    def __init__(self, definitions):
        super().__init__(definitions)
        for tag in ['POR','FRA','ENG','MOR']:
            self.countries[tag]=deepcopy(self.countries['CDM'])
        self.locations={}
        for route,r in ROUTES.items():
            for port in r['locations']:
                loc='location:'+port
                self.countries[loc]=deepcopy(self.countries['CDM'])
                self.locations[loc]=None if port=='strait_of_gibraltar' else 'POR'
        for data in self.countries.values():data.update(areas=set(),locations=set())

    def value(self, value, country, scopes):
        if value=='owner':return self.locations.get(country)
        if value=='root':return scopes.get('root',country)
        return super().value(value,country,scopes)

    def effects(self, rows, country, scopes):
        for k,op,v in rows:
            if k.startswith('location:'):self.effects(v,k,scopes)
            elif k=='owner':
                owner=self.locations[country]
                assert owner is not None
                self.effects(v,owner,scopes)
            elif k=='discover_area':self.countries[country]['areas'].add(v)
            elif k=='discover_location':self.countries[self.value(v,country,scopes)]['locations'].add(country)
            elif k=='set_variable':
                data=dict((key,value) for key,_,value in v)
                if 'months' in data:
                    data['days']=str(float(data.pop('months'))*30)
                super().effects([(k,op,[(key,'=',value) for key,value in data.items()])],country,scopes)
            elif k=='trigger_event_non_silently':
                fields=dict((key,value) for key,_,value in v)
                context=deepcopy(scopes)
                context['root']=country
                context['due']=self.day+30*float(fields.get('months',0))
                self.queue.append((fields['id'],country,context))
            else:super().effects([(k,op,v)],country,scopes)

    def monthly(self, country='CDM'):
        self.effects(dict((k,v) for k,_,v in self.defs['ga_exploration_monthly'])['effect'],country,{'root':country})

    def manual(self, force=False):
        fields=dict((k,v) for k,_,v in self.defs['ga_commission_voyage'])
        scopes={'root':'CDM','actor':'CDM'}
        allowed=self.condition(fields['allow'],'CDM',scopes)
        if allowed or force:self.effects(fields['effect'],'CDM',scopes)
        return allowed

    def deliver(self, event=None):
        i=next(i for i,p in enumerate(self.queue) if p[2]['due']<=self.day and (event is None or p[0]==event))
        popup=self.queue.pop(i);name,country,scopes=popup
        fields=dict((k,v) for k,_,v in self.defs[name])
        if not self.countries[country]['exists'] or not self.condition(fields['trigger'],country,scopes):return None
        self.effects(fields.get('immediate',[]),country,scopes)
        return popup

    def offer(self):
        self.monthly();self.day=36*30;self.monthly()
        return self.deliver('goblins_exploration.1')


def verify(read):
    defs={}
    for p in FILES[:-1]:defs.update({k:v for k,_,v in parse(read(p)) if k!='namespace'})
    scenarios=[]
    def passed(name):scenarios.append(name)
    def status(w,scopes=None,key='ga_exp_status'):
        for k,_,v in defs[key]:
            if k!='text':continue
            row=dict((k,v) for k,_,v in v)
            if w.condition(row.get('trigger',[]),'CDM',scopes or {}):return row['localization_key']
        raise AssertionError('Missing fallback')
    w=Voyages(defs);w.monthly();assert not w.queue
    assert status(w)=='ga_exp_preparing'
    w.day=36*30-1;w.monthly();assert not w.queue and not w.manual()
    w.day+=1;w.monthly();popup=w.deliver();assert status(w)=='ga_exp_decision'
    assert len(w.queue)==0 and not w.manual();w.monthly();assert not w.queue
    assert w.countries['CDM']['gold']==50
    passed('36-month initial preparation; offers and monthly pulses never charge or duplicate')
    for funds,allowed in [(4.99,False),(5,True),(50,True)]:
        w=Voyages(defs);p=w.offer();w.countries['CDM']['gold']=funds
        assert w.choose(p,0)==allowed
        if not allowed:
            before=deepcopy(w.countries);w.choose(p,0,force=True);assert w.countries==before
        else:
            assert w.countries['CDM']['gold']==funds-5
            before=deepcopy(w.countries);w.choose(p,0,force=True);w.choose(p,1,force=True);w.choose(p,2,force=True)
            w.manual(force=True);assert w.countries==before and len(w.queue)==1
            assert status(w)=='ga_exp_at_sea_east'
    passed('exact affordability; one debit and expedition; stale launch/wait/pause/manual effects cannot mutate an active voyage')
    w=Voyages(defs);p=w.offer();assert w.choose(p,1)
    assert status(w)=='ga_exp_postponed_status' and w.countries['CDM']['gold']==50
    w.day+=179;w.monthly();assert not w.queue and not w.manual()
    w.day+=1;w.monthly();fresh=w.deliver();before=deepcopy(w.countries)
    w.choose(p,0,force=True);w.choose(p,2,force=True);assert w.countries==before
    assert w.choose(fresh,2);assert status(w)=='ga_exp_paused_status'
    w.day+=3*365;w.monthly();assert not w.queue
    assert w.manual();fresh=w.deliver();assert w.choose(fresh,0)
    passed('six-month postponement; indefinite stopped reminders; manual reopening without fees; old offer isolation')
    departure=w.day
    for elapsed,expected in [(0,4),(29,4),(30,3),(60,2),(90,1)]:
        w.day=departure+elapsed
        assert status(w,key='ga_exp_remaining')==f'ga_exp_remaining_{expected}_text'
    w.day=departure+120
    # Conquer a port while its expedition is at sea; reports/contact follow arrival owners.
    w.locations['location:lisbon']='FRA';w.locations['location:setubal']=None
    saved=deepcopy(w);arrival=saved.deliver('goblins_exploration.2');assert arrival
    assert arrival[2]['ga_exp_contact_lisbon']=='FRA' and arrival[2]['ga_exp_contact_porto']=='POR'
    assert 'ga_exp_contact_setubal' not in arrival[2]
    assert saved.countries['FRA']['areas']=={'area:cm_cindermaw_area','area:cm_ashborn_seas_area'}
    assert saved.countries['ENG']['areas']==set()
    assert saved.countries['CDM']['locations']=={'location:'+name for name in ROUTES['east']['locations']}
    assert saved.countries['CDM']['areas']=={'area:iberian_west_coast_area'}
    assert len(saved.queue)==2 and all(x[0]=='goblins_exploration.6' for x in saved.queue)
    saved.locations['location:lisbon']='ENG'
    assert arrival[2]['ga_exp_contact_lisbon']=='FRA'
    assert status(saved)=='ga_exp_resting_status'
    before=deepcopy(saved.countries);saved.choose(arrival,0);saved.choose(arrival,0,force=True)
    assert saved.countries==before
    assert saved.countries['CDM']['gold']==45
    w=saved;w.queue=[];w.day+=359;assert not w.manual();w.day+=1;w.monthly();assert not w.queue
    assert w.manual();p=w.deliver();assert p[0]=='goblins_exploration.3'
    passed('saved state retains voyage and countdown; arrival reveals only listed coasts to current owners; report snapshots survive later conquest; exactly 12-month rest')
    for order in [('north','south'),('south','north')]:
        trial=deepcopy(w);offer=deepcopy(p)
        for route in order:
            index=0 if route=='north' else 1
            trial.countries['CDM']['gold']=9.99;assert not trial.choose(offer,index)
            trial.countries['CDM']['gold']=10;assert trial.choose(offer,index)
            assert trial.countries['CDM']['gold']==0
            assert not trial.choose(offer,1-index)
            trial.day+=180;returned=trial.deliver(f'goblins_exploration.{ROUTES[route]["event"]}')
            assert returned
            assert {'location:'+name for name in ROUTES[route]['locations']} <= trial.countries['CDM']['locations']
            assert {'area:'+name for name in ROUTES[route]['areas']} <= trial.countries['CDM']['areas']
            before=deepcopy(trial.countries)
            trial.effects(dict((k,v) for k,_,v in defs[returned[0]])['immediate'],'CDM',returned[2])
            assert trial.countries==before
            trial.queue=[];trial.day+=360
            if route!=order[-1]:
                assert trial.manual();offer=trial.deliver()
        assert status(trial)=='ga_exp_completed' and not trial.manual()
        trial.monthly();assert not trial.queue
    passed('both remaining-route orders; 10-gold boundaries; six-month crossings; replay-proof arrivals; completed routes cannot reopen')
    for num in [1,3]:
        for choice in [0,1,2 if num==1 else 3]:
            legacy=Voyages(defs);c=legacy.countries['CDM']['vars']
            c.update(ga_exploration_initialized=(True,None),ga_exploration_pending=(True,None))
            if num==3:c['ga_charted_east']=(True,None)
            p=(f'goblins_exploration.{num}','CDM',{'root':'CDM'})
            legacy.monthly();assert not legacy.queue
            assert legacy.choose(p,choice)
            before=deepcopy(legacy.countries);legacy.choose(p,choice,force=True);assert legacy.countries==before
    passed('older unanswered offers can launch, wait or stop reminders exactly once')
    for route,r in ROUTES.items():
        for open_already in [False,True]:
            legacy=Voyages(defs);c=legacy.countries['CDM']['vars']
            c.update(ga_exploration_initialized=(True,None),ga_exploration_pending=(True,None))
            if route!='east':c['ga_charted_east']=(True,None)
            legacy.countries['CDM']['gold']=40
            p=(f'goblins_exploration.{r["event"]}','CDM',{'root':'CDM','due':0})
            if open_already:assert legacy.choose(p,0)
            else:legacy.queue.append(p);assert legacy.deliver()
            assert legacy.variable('CDM','ga_charted_'+route) is True
            assert legacy.countries['CDM']['gold']==40
            before=deepcopy(legacy.countries);legacy.choose(p,0,force=True);assert legacy.countries==before
    passed('all older paid voyages settle without another fee, including already-open return messages')
    # Restore reminders explicitly after manually opening a paused offer.
    w=Voyages(defs);p=w.offer();w.choose(p,2);assert w.manual();p=w.deliver();w.choose(p,1)
    assert w.variable('CDM','ga_exp_paused') is None
    w.day+=180;w.monthly();assert len(w.queue)==1
    passed('six-month reminder choice explicitly restores reminders after manual mode')
    # Delivery rejects wrong-route and wrong-token events before their immediate.
    w=Voyages(defs);p=w.offer();w.choose(p,0)
    correct=deepcopy(w.queue[0]);w.day+=120
    wrong=deepcopy(correct);wrong=(wrong[0],wrong[1],dict(wrong[2],ga_exp_token=999))
    w.queue.insert(0,wrong);before=deepcopy(w.countries);assert w.deliver() is None and w.countries==before
    wrong=('goblins_exploration.4',correct[1],correct[2]);w.queue.insert(0,wrong)
    assert w.deliver() is None and w.countries==before
    assert w.deliver()
    passed('stale and wrong-route scheduled returns are suppressed before discovery')
    for route,r in ROUTES.items():
        offer=defs['goblins_exploration.'+('1' if route=='east' else '3')]
        option=next(v for k,_,v in offer if k=='option' and ('name','=',f'goblins_exploration.{1 if route=="east" else 3}.{route}') in v)
        assert ('add_gold','=',str(-r['cost'])) in list(flatten(option))
        dispatches=[dict((k,v) for k,_,v in v) for k,_,v in flatten(option) if k=='trigger_event_non_silently']
        assert dispatches==[{'id':f'goblins_exploration.{r["event"]}','months':str(r['months'])}]
    for sit in ['ga_gathering_of_five','ga_eastern_hunger']:
        gui=read(f'in_game/gui/panels/situation/{sit}.gui')
        assert 'ga_commission_voyage' not in gui
        assert 'ga_exp_panel_status' not in gui
    gui=read('in_game/gui/panels/situation/ga_ashborn_voyages.gui')
    assert gui.count('action_name = "ga_commission_voyage"')==1
    for route in ROUTES: assert 'ga_exp_chart_'+route+'_row' in gui
    assert 'ga_ashborn_voyages' in defs
    localization=read(FILES[-1])
    for rows in defs.values():
        for key,_,value in flatten(rows):
            if key=='localization_key':assert '\n '+value+':' in localization,value
    assert {'plymouth','portsmouth','cadiz','gibraltar','tangier','ceuta','london','sevilla','fez'} <= set(ROUTES['north']['locations'])
    assert 'This return message was already open' not in localization
    assert 'The report records owners encountered' not in localization
    assert 'Newly charted:' in localization
    passed('native calendar-month prices/durations and dedicated voyage situation controls; all custom text registered')
    return {'scenario_groups':len(scenarios),'scenarios':scenarios,'additional_monthly_scans':0,
            'new_event_ids':0,'engine_playtested':False}


if __name__=='__main__':
    import json
    from pathlib import Path
    root=Path(__file__).resolve().parents[1]
    print(json.dumps(verify(lambda p:(root/'mod'/p).read_text(encoding='utf-8-sig')),indent=2))
