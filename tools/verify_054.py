"""Regression checks for population conservation across splits and dynastic eligibility."""
from collections import Counter
from decimal import Decimal
import re

def verify(b,game,out,mapstats):
    cfg=b.CFG;locs=cfg['locations'];baseline=cfg['baseline_locations'];byid={l['id']:l for l in locs}
    assert len(byid)==len(locs)==72 and len({l['color'] for l in locs})==72
    assert set(baseline)<=set(byid)
    assert sum(Decimal(str(l['pop'])) for l in locs)==Decimal('682.694')
    for l in locs:
        assert sum(Decimal(str(v)) for v in l['pop_classes'].values())==Decimal(str(l['pop']))
        assert all(v>=0 for v in l['pop_classes'].values())
    for ident,old in baseline.items():
        children=[l for l in locs if l.get('split_from')==ident];assert len(children)==1
        assert byid[ident]['good']==old['good']
        combined=Decimal(str(byid[ident]['pop']))+Decimal(str(children[0]['pop']))
        assert abs(combined-Decimal(str(old['population']))*Decimal('1.15'))<=Decimal('.004')
        assert children[0]['province']!=byid[ident]['province']
    assert len({l['province'] for l in locs})==30
    # Check generated setup, not just input configuration.
    pops=(out/'main_menu/setup/start/06_pops.txt').read_text(encoding='utf-8-sig')
    for l in locs:
        a,z=b.block_span(pops,l['id']);rows=pops[a:z]
        assert sum(Decimal(v) for v in re.findall(r'\bsize\s*=\s*([\d.]+)',rows))==Decimal(str(l['pop']))
    defs=(out/'in_game/map_data/definitions.txt').read_text(encoding='utf-8-sig')
    a,z=b.block_span(defs,'cm_cindermaw_area');area=defs[a:z]
    for l in locs:assert len(re.findall(r'\b'+re.escape(l['id'])+r'\b',area))==1
    # Real starting courts: outsiders have MIL 86 and must lose to a dynastic son at MIL 82.
    chars=(out/'main_menu/setup/start/05_characters.txt').read_text(encoding='utf-8-sig')
    heirs={}
    for tag in ['CDM','QBR','RHK','SWK']:
        prefix='cm_'+tag.lower();candidates=[]
        for suffix in ['son','daughter','court_0','court_1','court_2']:
            ident=prefix+'_'+suffix;a,z=b.block_span(chars,ident);s=chars[a:z]
            house=re.search(r'\bdynasty\s*=\s*(\w+)',s)[1]
            if house!=prefix+'_house_0' or 'female = yes' in s:continue
            stats=[int(re.search(r'\b'+k+r'\s*=\s*(\d+)',s)[1]) for k in ['mil','adm']]
            candidates.append((tuple(stats),ident))
        assert max(candidates)[1]==prefix+'_son';heirs[tag]=max(candidates)[1]
    law=(out/'in_game/common/heir_selections/goblins_ashborn_isles.txt').read_text(encoding='utf-8-sig')
    assert 'dynasty = scope:target.last_valid_ruler.dynasty' in law
    assert 'regardless of dynasty' not in (out/'main_menu/localization/english/goblins_ashborn_isles_l_english.yml').read_text(encoding='utf-8-sig')
    import statistics
    provinces={p:sum(mapstats['locations'][l['id']]['pixels'] for l in locs if l['province']==p) for p in {l['province'] for l in locs}}
    return {'version':'0.5.4','population':682694,'increase_percent':round((682694/593647-1)*100,6),
            'locations':72,'provinces':30,'resources':dict(Counter(l['good'] for l in locs)),
            'starting_dynastic_heirs':heirs,'population_classes_and_generated_totals_checked':True,
            'original_ids_and_resources_preserved':True,
            'map_density':{'europe_reference_location_pixels_median':520,'europe_reference_province_pixels_median':2626,
                'ashborn_location_pixels_median':statistics.median(v['pixels'] for v in mapstats['locations'].values()),
                'ashborn_province_pixels_median':statistics.median(provinces.values())},'engine_tested':False}
