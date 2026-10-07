"""Modest starting production using native buildings and native RGO effects."""
import re


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
    capitals={c['capital'] for c in cfg['countries']}
    for loc in cfg['locations']:
        for key,level in loc['buildings'].items():
            assert level>0
            a,z=b.block_span(corpus,key);definition=corpus[a:z]
            rank='town' if loc['id'] in capitals else 'rural_settlement'
            if loc['id']=='cm_hooktooth':rank='city'
            assert re.search(r'\b'+rank+r'\s*=\s*yes',definition),(loc['id'],key,'incompatible rank')
            if key=='fishing_village':assert loc['good']=='fish'
            if key=='forest_village':assert loc['vegetation']=='woods'
            if key=='farming_village':assert loc['good'] in {'wheat','livestock','wool'}
            if key=='windmill':assert loc['good'] in {'wheat','rice','millet'}
            if key=='local_smelters':assert loc['good'] in {'iron','copper','tin','lead'}
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
            'tax_penalty_removed':True,'runtime_balance_verified':False}
