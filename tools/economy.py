"""Modest starting production using native buildings and native RGO effects."""
import re
from collections import Counter
from decimal import Decimal


def employment_requirements(b, game):
    """Native building jobs, in thousands, summed by class in each district."""
    import economy_reference
    definitions = {}
    for path in (game/'in_game/common/building_types').glob('*.txt'):
        definitions.update(economy_reference.blocks(path.read_text(encoding='utf-8-sig')))
    values = b.read(game, 'main_menu/common/script_values/default_values.txt')
    scalar = {key: Decimal(value) for key, value in re.findall(r'(?m)^\s*(\w+)\s*=\s*([\d.]+)\s*(?:#.*)?$', values)}
    result = {}
    for loc in b.CFG['locations']:
        demand = Counter()
        for key, level in loc['buildings'].items():
            definition = b.clean(definitions[key])
            employment = re.search(r'\bemployment_size\s*=\s*([\w.]+)', definition)
            pop_type = re.search(r'\bpop_type\s*=\s*(\w+)', definition)
            if employment:
                assert pop_type, (key, 'employment without class')
                token = employment[1]
                amount = scalar[token] if token in scalar else Decimal(token)
                demand[pop_type[1]] += amount * level
        result[loc['id']] = demand
    return result


def audit(b, game):
    """Report native employment demand separately from RGO capacity and income."""
    import economy_reference, mixed_populations
    requirements = employment_requirements(b, game)
    policy = b.CFG.get('population_062', {})
    countries = {}
    staffing = []
    workforce = []
    for country in b.CFG['countries']:
        locs = [l for l in b.CFG['locations'] if l['country'] == country['tag']]
        levels = Counter()
        for loc in locs:
            demand = requirements[loc['id']]
            available = {k: Decimal(str(v)) for k,v in loc['pop_classes'].items()}
            for pop in mixed_populations.additions().get(loc['id'], []):
                available[pop['type']] = available.get(pop['type'], Decimal(0)) + Decimal(str(pop['size']))
            for key, level in loc['buildings'].items():
                levels[key] += level
            planned = Counter(demand)
            if policy:
                planned = Counter({k:v*Decimal(str(policy['building_staffing_multiplier'])) for k,v in demand.items()})
                planned['laborers'] += Decimal(str(policy['rgo_base_reserve'])) + loc['rgo_expansion']
            for pop_type, amount in planned.items():
                if amount > available.get(pop_type, 0):
                    staffing.append({'location': loc['id'], 'class': pop_type,
                                     'required_people': float(amount*1000),
                                     'starting_people': float(available.get(pop_type, 0)*1000)})
            workforce.append({'location':loc['id'], 'building_jobs':{k:float(v*1000) for k,v in demand.items()},
                              'planning_target':{k:float(v*1000) for k,v in planned.items()},
                              'starting_people':{k:float(v*1000) for k,v in available.items()}})
        countries[country['tag']] = {
            'population': sum(int((Decimal(str(l['pop']))+mixed_populations.extra(l['id']))*1000) for l in locs),
            'building_levels': dict(levels), 'total_building_levels': sum(levels.values()),
            'capital_levels': sum(next(l['buildings'] for l in locs if l['id']==country['capital']).values()),
            'rgo_bonus': sum(l['rgo_expansion'] for l in locs)}
    return {'countries': countries, 'staffing_shortfalls': staffing, 'workforce':workforce,
            'vanilla_references': economy_reference.compare(b, game),
            'scope': 'Native building jobs plus the configured laborer reserve for RGOs. Reserve is a planning allowance, not an engine capacity measurement. Hiring, profitability, levies and migration need gameplay verification.',
            'runtime_balance_verified': False}


def build(b,game,out):
    starting_trades(b,game,out)
    cfg=b.CFG;tags=' '.join('tag = '+c['tag'] for c in cfg['countries'])
    entries=[]
    for country in cfg['countries']:
        locations=[l for l in cfg['locations'] if l['country']==country['tag']]
        effects=[]
        for loc in locations:
            effects.append(f'''            if = {{
                limit = {{ owns = location:{loc['id']} }}
                location:{loc['id']} = {{ change_max_raw_material_workers = {loc['rgo_expansion']} }}
            }}''')
        entries.append('        if = {\n            limit = { tag = '+country['tag']+' }\n'+'\n'.join(effects)+'\n        }')
    script=f'''# Initial RGO investment runs once on the first monthly pulse.
ga_economy_monthly = {{
    trigger = {{ OR = {{ {tags} }} }}
    effect = {{
        if = {{
            limit = {{ NOT = {{ has_variable = ga_economy_initialized }} }}
            set_variable = {{ name = ga_economy_initialized value = yes }}
{chr(10).join(entries)}
        }}
    }}
}}
'''
    b.write(out,'in_game/common/on_action/goblins_economy.txt',script)
    # Flat, explicit starting development supplements native terrain/rank rules.
    rel='main_menu/setup/start/14_development.txt';native=b.read(game,rel)
    lines=['cm_cindermaw_area = 7']+[c['capital']+' = 3' for c in cfg['countries']]
    b.write(out,rel,b.inject(native,'development','\n'.join(lines)))
    corpus='\n'.join(p.read_text(encoding='utf-8-sig') for p in (game/'in_game/common/building_types').glob('*.txt'))
    capital_ranks={c['capital']:c['rank'] for c in cfg['countries']}
    for loc in cfg['locations']:
        for key,level in loc['buildings'].items():
            assert level>0
            a,z=b.block_span(corpus,key);definition=corpus[a:z]
            rank=loc.get('rank', capital_ranks.get(loc['id'],'rural_settlement'))
            assert re.search(r'\b'+rank+r'\s*=\s*yes',definition),(loc['id'],key,'incompatible rank')
            if key=='fishing_village':assert loc['good']=='fish'
            if key=='forest_village':assert loc['vegetation']=='woods'
            if key=='farming_village':assert loc['good'] in {'wheat','livestock','wool'}
            if key=='windmill':assert loc['good'] in {'wheat','rice','millet'}
            if key=='local_smelters':assert loc['good'] in {'iron','copper','tin','lead'}
            if key=='charcoal_maker':assert loc['vegetation']=='woods'
        assert isinstance(loc['rgo_expansion'], int) and 0 < loc['rgo_expansion'] <= 6
    goods='\n'.join(p.read_text(encoding='utf-8-sig') for p in (game/'in_game/common/goods').glob('*.txt'))
    for loc in cfg['locations']:
        a,z=b.block_span(goods,loc['good'])
        assert 'category = raw_material' in goods[a:z] or loc['good'] in {'fish','wheat','livestock','lumber','tar','wool'},(loc['id'],'invalid RGO')
    effects=b.read(game,'in_game/common/scripted_effects/country_effects.txt')
    assert 'change_max_raw_material_workers = 1' in effects,'Native RGO effect changed'
    return {'rgo_expansion_total':sum(l['rgo_expansion'] for l in cfg['locations']),
            'rgo_initialization':'once, on first monthly pulse; ownership checked',
            'village_levels':sum(n for l in cfg['locations'] for key,n in l['buildings'].items() if key.endswith('_village')),
            'capital_industry':{c['tag']:{k:v for k,v in next(l for l in cfg['locations'] if l['id']==c['capital'])['buildings'].items() if k.endswith('_guild')} for c in cfg['countries']},
            'tax_penalty_removed':True,'runtime_balance_verified':False,
            'balance_audit':audit(b,game)}


# Each crown funds an import using merchants in its destination market.
STARTING_TRADES = [('CDM','cm_chainhaven','cm_hooktooth','silver'),
                   ('GTF','cm_hooktooth','cm_chainhaven','lumber')]

def starting_trades(b,game,out):
    native=b.read(game,'in_game/common/generic_actions/markets.txt')
    for key in ['from','to','merchant','goods','desired','locked']:
        assert key+' = scope:' in native,key
    effects=[]
    for tag,source,target,good in STARTING_TRADES:
        route=f'from_market = location:{source}.market to_market = location:{target}.market'
        effects.append(f'''ga_seed_trade_{tag.lower()} = {{
    if = {{ limit = {{ NOT = {{ has_variable = ga_starting_trade_061 }} }}
        if = {{ limit = {{
            owns = location:{target}
            exists = location:{source}.market exists = location:{target}.market
            location:{source} = {{ NOT = {{ market = location:{target}.market }} }}
            NOT = {{ any_trade = {{ {route} }} }}
            location:{target}.market = {{
                has_merchant = c:{tag}
                available_merchant_capacity = {{ country = c:{tag} value >= 1 }}
            }}
            can_find_trade_route = {{ from = location:{source}.market to = location:{target}.market }}
        }}
            create_trade = {{
                from = location:{source}.market to = location:{target}.market
                merchant = location:{target}.market goods = goods:{good}
                desired = 1 locked = yes
            }}
        }}
        # Confirm creation before marking completion. A player-created route
        # also satisfies this; never recreate a cancelled initial route.
        if = {{ limit = {{ any_trade = {{ {route} }} }}
            set_variable = {{ name = ga_starting_trade_061 value = yes }}
        }}
    }}
}}''')
    b.write(out,'in_game/common/scripted_effects/goblins_starting_trades.txt','\n'.join(effects))
    b.write(out,'in_game/common/on_action/goblins_starting_trades.txt','''# New campaigns attempt both routes immediately after setup.
on_game_start = { on_actions = { ga_starting_trade_setup } }
monthly_country_pulse = { on_actions = { ga_starting_trade_retry } }
ga_starting_trade_setup = {
    effect = {
        if = { limit = { country_exists = c:CDM } c:CDM = { ga_seed_trade_cdm = yes } }
        if = { limit = { country_exists = c:GTF } c:GTF = { ga_seed_trade_gtf = yes } }
    }
}
# Bounded fallback if merchants/pathfinding are not ready at game-start.
# Also permits adoption in early saves without duplicating existing routes.
ga_starting_trade_retry = {
    trigger = {
        current_date < 1338.12.1
        OR = { tag = CDM tag = GTF }
        NOT = { has_variable = ga_starting_trade_061 }
    }
    effect = {
        if = { limit = { tag = CDM } ga_seed_trade_cdm = yes }
        if = { limit = { tag = GTF } ga_seed_trade_gtf = yes }
    }
}
''')
