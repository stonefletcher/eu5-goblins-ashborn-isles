"""Small, optional voyages that reveal coastlines only after the crews return."""
import re

ROUTES = {
    'east': {'cost':5,'months':4,'event':2,'areas':['iberian_west_coast_area'],'locations':['lisbon','porto','setubal']},
    'north': {'cost':10,'months':6,'event':4,'areas':['bay_of_biscay_area','english_channel_area'],'locations':['brest','la_rochelle','bordeaux','plymouth','southampton']},
    'south': {'cost':10,'months':6,'event':5,'areas':['nw_africa_coast_area'],'locations':['cadiz','tangier','ceuta','strait_of_gibraltar']},
}

TEXT = {
    'goblins_exploration.1.title':'Beyond the Ashen Horizon',
    'goblins_exploration.1.desc':'Our charts end where the smoke of our mountains disappears. A fishing crew has returned with a plank unlike anything built in the isles, and the captains argue that it drifted from the east. A small expedition could follow the currents and bring back a route to whoever lives beyond them.',
    'goblins_exploration.1.east':'Provision a voyage east. The crew returns in four months.',
    'goblins_exploration.1.wait':'We need these provisions at home. Ask again in six months.',
    'goblins_exploration.2.title':'A Coast Beyond Counting',
    'goblins_exploration.2.desc':'The expedition returns with sketches of river mouths, broad sails and stone towns. Their coastal chart marks Porto, Lisbon and Setubal, with a sailing route back to our islands. What lies beyond those harbors remains a blank. Foreign harbor officials have questioned our crews: the rulers of these ports now know the Ashborn Isles and the waters around them.',
    'goblins_exploration.2.a':'Keep the charts dry. There will be more voyages.',
    'goblins_exploration.3.title':'The Captains Unroll Their Charts',
    'goblins_exploration.3.desc':'We know the eastern crossing, but the mainland coast continues beyond the last marks on our charts. Some crews favor the northern waters, others the warmer southern coast. Provisions for another expedition will cost ten gold, and the voyage will take six months.',
    'goblins_exploration.3.north':'Chart the northern coasts and the narrow sea beyond.',
    'goblins_exploration.3.south':'Follow the coast south toward the straits.',
    'goblins_exploration.3.wait':'Let the crews rest. Reconsider in six months.',
    'goblins_exploration.4.title':'Cold Seas and Foreign Harbors',
    'goblins_exploration.4.desc':'Our sailors bring back a northern coastal chart. Beyond the great bay lie Brest, La Rochelle and Bordeaux; across the narrow sea they found Plymouth and Southampton. The chart records their harbors and the waters between them. Inland roads and distant kingdoms remain unknown. The rulers of the ports we visited now know the Ashborn Isles.',
    'goblins_exploration.4.a':'Another stretch of the world has a name.',
    'goblins_exploration.5.title':'The Southern Straits',
    'goblins_exploration.5.desc':'The southern expedition has returned. Its chart shows Cadiz and the northern African coast, including Tangier and Ceuta near the straits. The captains count rich-looking harbors, but their map tells us little about the lands behind the walls. The rulers of these ports now know the route to the Ashborn Isles.',
    'goblins_exploration.5.a':'The sea is wider than our old stories claimed.',
}

def voyage_option(route,offer):
    r=ROUTES[route]
    return f'''    option = {{
        name = goblins_exploration.{offer}.{route}
        trigger = {{ gold >= {r['cost']} NOT = {{ has_variable = ga_charted_{route} }} }}
        add_gold = -{r['cost']}
        trigger_event_non_silently = {{ id = goblins_exploration.{r['event']} months = {r['months']} }}
        ai_chance = {{ factor = 10 }}
    }}'''

def build(b,game,out):
    names=b.parse_names(game);defs=b.read(game,'in_game/map_data/definitions.txt')
    for route in ROUTES.values():
        for area in route['areas']:b.block_span(defs,area)
        for name in route['locations']:assert name in names,name
    tags=' '.join('tag = '+c['tag'] for c in b.CFG['countries'])
    on_action=f'''ga_exploration_monthly = {{
    trigger = {{ OR = {{ {tags} }} }}
    effect = {{
        if = {{
            limit = {{ NOT = {{ has_variable = ga_exploration_initialized }} }}
            set_variable = {{ name = ga_exploration_initialized value = yes }}
            set_variable = {{ name = ga_exploration_cooldown months = 3 }}
        }}
        if = {{
            limit = {{
                NOT = {{ has_variable = ga_exploration_cooldown }}
                NOT = {{ has_variable = ga_exploration_pending }}
                NOT = {{ AND = {{ has_variable = ga_charted_north has_variable = ga_charted_south }} }}
            }}
            set_variable = {{ name = ga_exploration_pending value = yes }}
            if = {{
                limit = {{ NOT = {{ has_variable = ga_charted_east }} }}
                trigger_event_non_silently = {{ id = goblins_exploration.1 }}
            }}
            else = {{ trigger_event_non_silently = {{ id = goblins_exploration.3 }} }}
        }}
    }}
}}
'''
    events=['namespace = goblins_exploration\n']
    for num,routes in [(1,['east']),(3,['north','south'])]:
        events.append(f'''goblins_exploration.{num} = {{
    type = country_event
    outcome = neutral
    title = goblins_exploration.{num}.title
    desc = goblins_exploration.{num}.desc
    trigger = {{ OR = {{ {tags} }} }}
    illustration_tags = {{ 10 = exterior }}
'''+ '\n'.join(voyage_option(route,num) for route in routes)+f'''
    option = {{
        name = goblins_exploration.{num}.wait
        remove_variable = ga_exploration_pending
        set_variable = {{ name = ga_exploration_cooldown months = 6 }}
        ai_chance = {{ factor = 1 }}
    }}
}}
''')
    for route,r in ROUTES.items():
        num=r['event']
        effects='\n'.join('        discover_area = area:'+area for area in r['areas'])
        # Scope through current owners, so conquest or a changed start date does
        # not reveal the isles to an unrelated hard-coded country tag.
        for name in r['locations']:
            effects+=f'''\n        location:{name} = {{
            discover_location = root
            if = {{
                limit = {{ exists = owner }}
                owner = {{
                    discover_area = area:cm_cindermaw_area
                    discover_area = area:cm_ashborn_seas_area
                }}
            }}
        }}'''
        events.append(f'''goblins_exploration.{num} = {{
    type = country_event
    outcome = neutral
    title = goblins_exploration.{num}.title
    desc = goblins_exploration.{num}.desc
    trigger = {{ OR = {{ {tags} }} }}
    illustration_tags = {{ 10 = exterior }}
    option = {{
        name = goblins_exploration.{num}.a
{effects}
        set_variable = {{ name = ga_charted_{route} value = yes }}
        remove_variable = ga_exploration_pending
        set_variable = {{ name = ga_exploration_cooldown months = 12 }}
    }}
}}
''')
    b.write(out,'in_game/common/on_action/goblins_exploration.txt',on_action)
    b.write(out,'in_game/events/goblins_exploration.txt','\n'.join(events))
    b.write(out,'main_menu/localization/english/goblins_exploration_l_english.yml','l_english:\n'+'\n'.join(' '+k+': "'+v+'"' for k,v in TEXT.items())+'\n')
    setup=(out/'main_menu/setup/start/10_countries.txt').read_text(encoding='utf-8-sig')
    for c in b.CFG['countries']:
        a,z=b.block_span(setup,c['tag']);country=setup[a:z]
        assert 'expl_western_europe' not in country and 'discovered_regions' not in country
        assert 'cm_cindermaw_area cm_ashborn_seas_area' in country
    # Mutual contact is limited to the owners of this voyage's named ports.
    return {'starting_knowledge':'Ashborn land and sea areas only','countries':[c['tag'] for c in b.CFG['countries']],
            'first_offer_after_months':3,'routes':ROUTES,'reciprocal_discovery':True,
            'recipients':'current owners of visited locations; unowned sea locations skipped','runtime_verified':False}
