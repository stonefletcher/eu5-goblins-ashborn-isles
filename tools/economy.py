"""Modest starting production using native buildings and native RGO effects."""
import re
from collections import Counter
from decimal import Decimal


def audit(b, game):
    """Report native employment demand separately from RGO capacity and income."""
    import economy_reference, mixed_populations
    definitions = {}
    for path in (game/'in_game/common/building_types').glob('*.txt'):
        definitions.update(economy_reference.blocks(path.read_text(encoding='utf-8-sig')))
    values = b.read(game, 'main_menu/common/script_values/default_values.txt')
    scalar = {key: Decimal(value) for key, value in re.findall(r'(?m)^\s*(\w+)\s*=\s*([\d.]+)\s*(?:#.*)?$', values)}
    countries = {}
    staffing = []
    for country in b.CFG['countries']:
        locs = [l for l in b.CFG['locations'] if l['country'] == country['tag']]
        levels = Counter()
        for loc in locs:
            demand = Counter()
            available = {k: Decimal(str(v)) for k,v in loc['pop_classes'].items()}
            for pop in mixed_populations.additions().get(loc['id'], []):
                available[pop['type']] = available.get(pop['type'], Decimal(0)) + Decimal(str(pop['size']))
            for key, level in loc['buildings'].items():
                definition = definitions[key]
                employment = re.search(r'\bemployment_size\s*=\s*([\w.]+)', definition)
                pop_type = re.search(r'\bpop_type\s*=\s*(\w+)', definition)
                if employment and pop_type:
                    token = employment[1]
                    amount = scalar[token] if token in scalar else Decimal(token)
                    demand[pop_type[1]] += amount * level
                levels[key] += level
            for pop_type, amount in demand.items():
                if amount > available.get(pop_type, 0):
                    staffing.append({'location': loc['id'], 'class': pop_type,
                                     'building_jobs': float(amount*1000),
                                     'starting_people': float(available.get(pop_type, 0)*1000)})
        countries[country['tag']] = {
            'population': sum(int((Decimal(str(l['pop']))+mixed_populations.extra(l['id']))*1000) for l in locs),
            'building_levels': dict(levels), 'total_building_levels': sum(levels.values()),
            'capital_levels': sum(next(l['buildings'] for l in locs if l['id']==country['capital']).values()),
            'rgo_bonus': sum(l['rgo_expansion'] for l in locs)}
    return {'countries': countries, 'staffing_shortfalls': staffing,
            'vanilla_references': economy_reference.compare(b, game),
            'scope': 'Explicit 1337 setup only; jobs exclude RGOs, levies, migration and engine initialization. Building levels are not GDP.',
            'runtime_balance_verified': False}


def build(b,game,out):
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
