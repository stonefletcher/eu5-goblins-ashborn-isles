"""Run the delivered early-project options at affordability and repeat boundaries."""
from copy import deepcopy
from verify_harbor_bargains import World, parse


def verify(read):
    definitions = {k:v for k,_,v in parse(read('in_game/events/goblins_gathering.txt')) if k != 'namespace'}
    modifiers = {k:v for k,_,v in parse(read('main_menu/common/static_modifiers/goblins_gathering.txt'))}
    expected = {
        'CDM': (10, [('ga_cindermaw_drilled_captains','land_morale_modifier','0.05'),('ga_cindermaw_court_envoys','diplomatic_reputation','0.5'),('ga_cindermaw_funded_accounts','army_maintenance_efficiency','0.05')]),
        'QBR': (11, [('ga_brackmaw_repaired_sluices','global_food_capacity_modifier','0.10'),('ga_brackmaw_marsh_workshops','global_production_efficiency','0.05'),('ga_brackmaw_causeway_defenses','global_defensive','0.10')]),
        'RHK': (12, [('ga_reefhook_restored_beacons','naval_morale_recovery','0.05'),('ga_reefhook_repair_yards','navy_maintenance_efficiency','0.05'),('ga_reefhook_pilot_envoys','diplomatic_reputation','0.5')]),
        'SFK': (13, [('ga_shatterfin_crew_households','global_sailors_modifier','0.05'),('ga_shatterfin_storm_crews','naval_morale_modifier','0.05'),('ga_shatterfin_house_delegates','diplomatic_reputation','0.5')]),
        'SWK': (14, [('ga_sootwake_woodland_wardens','global_defensive','0.10'),('ga_sootwake_charcoal_workshops','global_production_efficiency','0.05'),('ga_sootwake_sheltered_stores','global_food_capacity_modifier','0.10')]),
    }
    expected['GTF'] = (40, [('ga_giltfang_honest_weights','global_production_efficiency','0.05'),('ga_giltfang_harbor_envoys','diplomatic_reputation','0.5'),('ga_giltfang_harbor_watch','global_defensive','0.10')])
    checks=0
    for tag,(number,projects) in expected.items():
        event='ga_gathering.'+str(number)
        assert len([v for k,_,v in definitions[event] if k=='option'])==4
        # The original Shatterfin flavour follow-up is validated separately by verify_055.
        defs=deepcopy(definitions);defs[event]=[row for row in defs[event] if row[0]!='after']
        for index,(modifier,key,value) in enumerate(projects):
            assert modifiers[modifier]==[(key,'=',value)]
            choice = [v for k,_,v in definitions[event] if k=='option'][index]
            preview = next(v for k,_,v in choice if k=='show_as_tooltip')
            assert preview == [('add_gold', '=', '-10'), ('add_country_modifier', '=',
                [('modifier', '=', modifier), ('years', '=', '5'), ('mode', '=', 'replace')])]
            w=World(defs); before=deepcopy(w.countries)
            w.effects([('show_as_tooltip','=',preview)],tag,{})
            assert w.countries==before, 'Hover preview must not apply rewards'
            for ai,gold,allowed in [(False,0,False),(False,9.99,False),(False,10,True),(False,50,True),(True,29.99,False),(True,30,True)]:
                w=World(defs);w.countries[tag].update(gold=gold,is_ai=ai)
                popup=(event,tag,{})
                assert w.choose(popup,index)==allowed
                assert w.countries[tag]['gold']==gold-(10 if allowed else 0)
                assert w.countries[tag]['modifiers']==({modifier:1825} if allowed else {})
                before=deepcopy(w.countries);w.choose(popup,index,force=True)
                assert w.countries==before, 'Stale option bypassed cost or repeated grant'
                checks+=1
            w=World(defs);popup=(event,tag,{})
            assert w.choose(popup,index)
            before=deepcopy(w.countries)
            for other in range(3): w.choose(popup,other,force=True)
            assert w.countries==before, 'A second project was granted'
            checks+=1
        w=World(defs);w.countries[tag]['gold']=0
        assert w.choose((event,tag,{}),len(projects))
        assert not w.countries[tag]['modifiers'] and w.countries[tag]['gold']==0
        w.countries[tag]['gold']=50;before=deepcopy(w.countries)
        w.choose((event,tag,{}),0,force=True)
        assert w.countries==before, 'Project granted after decline'
        checks+=1
    assert modifiers['ga_cindermaw_counted_stores']==[('army_maintenance_efficiency','=','0.10')]
    return {'scenario_checks':checks,'clans':len(expected),'paid_options':sum(len(p) for _,p in expected.values()),'cost':10,'duration_years':5,
            'ai_reserve':20,'free_decline':True,'legacy_accounts_preserved':True,'engine_tested':False}
