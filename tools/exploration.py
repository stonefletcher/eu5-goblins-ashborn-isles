"""Known Atlantic charts and optional voyages that establish foreign contact."""
import re
import event_art

FIRST_OFFER_MONTHS = 36
STARTING_REGIONS = ['iberia_region']
STARTING_SEA_AREAS = ['iberian_west_coast_area', 'bay_of_biscay_area',
                      'english_channel_area', 'nw_africa_coast_area']
# Coastal provinces near the voyage destinations; distant interiors stay hidden.
STARTING_PROVINCES = [
    'cornwall_province', 'devon_province', 'dorset_province', 'hampshire_province',
    'sussex_province', 'kent_province',
    'tregor_province', 'cornouaille_province', 'vannetais_province', 'nantais_province',
    'rennais_province', 'lower_poitou_province', 'saintonge_province',
    'bordelais_province', 'tursan_province', 'bayonne_province',
    'habat_province', 'azghar_province', 'fez_province', 'tamasna_province',
    'dukkala_province', 'haha_province', 'errif_province', 'kert_province',
]


def starting_knowledge():
    return (f"discovered_areas = {{ cm_cindermaw_area cm_ashborn_seas_area {' '.join(STARTING_SEA_AREAS)} }}\n"
            f" discovered_regions = {{ {' '.join(STARTING_REGIONS)} }}\n"
            f" discovered_provinces = {{ {' '.join(STARTING_PROVINCES)} }}")

ROUTES = {
    'east': {'cost':5,'months':4,'event':2,'areas':['iberian_west_coast_area'],'locations':['lisbon','porto','setubal']},
    'north': {'cost':10,'months':6,'event':4,'areas':['bay_of_biscay_area','english_channel_area'],'locations':['brest','la_rochelle','bordeaux','plymouth','southampton']},
    'south': {'cost':10,'months':6,'event':5,'areas':['nw_africa_coast_area'],'locations':['cadiz','tangier','ceuta','strait_of_gibraltar']},
}

TEXT = {
    'goblins_exploration.6.title':'Strange Visitors on Our Shores',
    'goblins_exploration.6.desc':'Fishermen report that a strange little vessel put ashore along our coast. Its crew were unlike any people they had seen: short, ugly creatures with long pointed ears, sharp teeth and restless eyes. They picked through the shallows and argued in a rasping tongue, but the moment they realized they had been spotted, they scrambled aboard and fled out to sea.\n\nA scout ship followed at a cautious distance, keeping their patched sails just within sight. Beyond our familiar waters, the pursuit led to a cluster of smoke-wreathed islands, their coves crowded with crooked docks and more of the same vessels. Our scouts have returned with a chart of the crossing. Whatever these creatures may be, we now know where they live.',
    'goblins_exploration.6.a':'Mark the islands on our charts. Keep watch on the sea.',
    'goblins_exploration.1.title':'Beyond the Ashen Horizon',
    'goblins_exploration.1.desc':'Our rough charts show Iberia and the nearby mainland shores, but no captain has returned with a close account of their harbors. After years of gathering provisions and seaworthy hulls, the crews are ready. A small expedition could cross the eastern waters and learn who lives beyond them.',
    'goblins_exploration.1.east':'Provision a voyage east. The crew returns in four months.',
    'goblins_exploration.1.wait':'We need these provisions at home. Ask again in six months.',
    'goblins_exploration.2.title':'A Coast Beyond Counting',
    'goblins_exploration.2.desc':'The expedition returns with sketches of river mouths, broad sails and stone towns. Porto, Lisbon and Setubal are more than marks on an old chart now: our crews have seen their harbors and sailed the crossing home. They fled when shore watchers spotted them, but a foreign sail shadowed their return. The rulers of these ports now know the Ashborn Isles and the waters around them.',
    'goblins_exploration.2.a':'Keep the charts dry. There will be more voyages.',
    'goblins_exploration.3.title':'The Captains Unroll Their Charts',
    'goblins_exploration.3.desc':'We have sailed the eastern crossing, but much of the coastline on our charts is still known only through old accounts. Some crews favor visiting the northern harbors, others the warmer southern coast. Provisions for another expedition will cost ten gold, and the voyage will take six months.',
    'goblins_exploration.3.north':'Chart the northern coasts and the narrow sea beyond.',
    'goblins_exploration.3.south':'Follow the coast south toward the straits.',
    'goblins_exploration.3.wait':'Let the crews rest. Reconsider in six months.',
    'goblins_exploration.4.title':'Cold Seas and Foreign Harbors',
    'goblins_exploration.4.desc':'Our sailors bring back firsthand accounts of the northern coast. They visited Brest, La Rochelle and Bordeaux, then Plymouth and Southampton across the narrow sea. Old chart marks now carry sketches of harbors and notes on their inhabitants. Distant interiors remain unknown. The rulers of the ports we visited now know the Ashborn Isles.',
    'goblins_exploration.4.a':'Another stretch of the world has a name.',
    'goblins_exploration.5.title':'The Southern Straits',
    'goblins_exploration.5.desc':'The southern expedition has returned from Cadiz, Tangier and Ceuta near the straits. The captains have replaced rumors with firsthand sketches of rich-looking harbors, though they learned little of life behind the walls. The rulers of these ports now know the route to the Ashborn Isles.',
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

def build(b,game,out,validate_setup=True):
    names=b.parse_names(game);defs=b.read(game,'in_game/map_data/definitions.txt')
    for key in STARTING_REGIONS + STARTING_SEA_AREAS + STARTING_PROVINCES:
        b.block_span(defs,key)
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
            set_variable = {{ name = ga_exploration_cooldown months = {FIRST_OFFER_MONTHS} }}
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
    image = "{event_art.image(f'goblins_exploration.{num}')}"
'''+ '\n'.join(voyage_option(route,num) for route in routes)+f'''
    option = {{
        name = goblins_exploration.{num}.wait
        remove_variable = ga_exploration_pending
        set_variable = {{ name = ga_exploration_cooldown months = 6 }}
        ai_chance = {{ factor = 1 }}
    }}
}}
''')
    events.append(f'''goblins_exploration.6 = {{
    type = country_event
    outcome = neutral
    title = goblins_exploration.6.title
    desc = goblins_exploration.6.desc
    trigger = {{ NOT = {{ OR = {{ {tags} }} }} }}
    image = "{event_art.image('goblins_exploration.6')}"
    option = {{ name = goblins_exploration.6.a }}
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
                    if = {{
                        limit = {{
                            NOT = {{ OR = {{ {tags} }} }}
                            NOT = {{ has_variable = ga_received_goblin_first_contact }}
                        }}
                        set_variable = {{ name = ga_received_goblin_first_contact value = yes }}
                        trigger_event_non_silently = {{ id = goblins_exploration.6 }}
                    }}
                }}
            }}
        }}'''
        events.append(f'''goblins_exploration.{num} = {{
    type = country_event
    outcome = neutral
    title = goblins_exploration.{num}.title
    desc = goblins_exploration.{num}.desc
    trigger = {{ OR = {{ {tags} }} }}
    image = "{event_art.image(f'goblins_exploration.{num}')}"
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
    b.write(out,'main_menu/localization/english/goblins_exploration_l_english.yml','l_english:\n'+'\n'.join(' '+k+': "'+v.replace('\n',r'\n')+'"' for k,v in TEXT.items())+'\n')
    # Runtime-only installer overlays do not contain generated starting setup.
    # Full builds always retain these starting-knowledge checks.
    if validate_setup:
        setup=(out/'main_menu/setup/start/10_countries.txt').read_text(encoding='utf-8-sig')
        for c in b.CFG['countries']:
            a,z=b.block_span(setup,c['tag']);country=setup[a:z]
            assert 'expl_western_europe' not in country
            assert starting_knowledge() in country
    # Mutual contact is limited to the owners of this voyage's named ports.
    return {'starting_knowledge':{'regions':STARTING_REGIONS,'sea_areas':STARTING_SEA_AREAS,
                                'coastal_provinces':STARTING_PROVINCES,'fog_of_war':'normal'},
            'countries':[c['tag'] for c in b.CFG['countries']],
            'first_offer_after_months':FIRST_OFFER_MONTHS,'routes':ROUTES,'reciprocal_discovery':True,
            'recipients':'current owners of visited locations; unowned sea locations skipped','runtime_verified':False}
