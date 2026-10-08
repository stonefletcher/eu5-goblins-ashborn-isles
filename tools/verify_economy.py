"""Focused 0.5.6 setup build and economic regression checks; no terrain rebuild."""
import argparse
import json
import re
from decimal import Decimal
from pathlib import Path
import build as b
import economy
import economy_reference
import mixed_populations


def verify(game, out):
    out.mkdir(parents=True, exist_ok=True)
    b.build_setup(game, out)
    report = economy.build(b, game, out)
    audit = report['balance_audit']
    # Only the pre-existing capital stockade needs a class not seeded at start.
    assert all(row['location']=='cm_hooktooth' and row['class']=='soldiers'
               for row in audit['staffing_shortfalls']), audit['staffing_shortfalls']
    templates = dict(economy_reference.blocks((out/'in_game/common/town_setups/goblins_ashborn_isles.txt').read_text(encoding='utf-8-sig')))
    pops = dict(economy_reference.blocks(dict(economy_reference.blocks((out/'main_menu/setup/start/06_pops.txt').read_text()))['locations']))
    for loc in b.CFG['locations']:
        actual = {k:int(v) for k,v in re.findall(r'(\w+)\s*=\s*(\d+)', templates[loc['id']+'_settlement'])}
        assert actual == loc['buildings'], loc['id']
        total = sum((Decimal(v) for v in re.findall(r'\bsize\s*=\s*([\d.]+)', pops[loc['id']])), Decimal(0))
        assert total == Decimal(str(loc['pop'])) + mixed_populations.extra(loc['id'])
    countries = audit['countries']
    assert sum(c['population'] for c in countries.values()) == 1923313
    assert countries['CDM']['total_building_levels'] > countries['QBR']['total_building_levels'] > countries['SFK']['total_building_levels'] > countries['RHK']['total_building_levels']
    assert countries['CDM']['building_levels']['weapon_guild'] == 3
    assert countries['QBR']['building_levels']['naval_supplies_guild'] > countries['CDM']['building_levels']['naval_supplies_guild']
    assert countries['SWK']['building_levels']['charcoal_maker'] > countries['CDM']['building_levels']['charcoal_maker']
    assert len({tuple(sorted(next(l['buildings'] for l in b.CFG['locations'] if l['id']==c['capital']).items())) for c in b.CFG['countries']}) == len(b.CFG['countries'])
    # Two native markets and once-only, ownership-guarded investment remain intact.
    markets = (out/'main_menu/setup/start/03_markets.txt').read_text()
    assert 'add_market = cm_hooktooth' in markets
    assert 'add_market = cm_chainhaven' in markets
    actions = (out/'in_game/common/on_action/goblins_economy.txt').read_text(encoding='utf-8-sig')
    assert actions.count('NOT = { has_variable = ga_economy_initialized }') == 1
    assert actions.count('limit = { owns = location:') == len(b.CFG['locations'])
    report['checks'] = ['native building ranks/resources', 'generated settlement levels',
                        'unchanged population totals', 'production staffing',
                        'country specialization and scale', 'two markets and guarded initialization']
    (out/'economy-audit.json').write_text(json.dumps(report, indent=2)+'\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--game', type=Path, required=True)
    parser.add_argument('--out', type=Path, default=b.ROOT/'build/economy-check')
    args = parser.parse_args()
    result = verify(args.game, args.out)
    print(json.dumps({'checks': result['checks'], 'rgo_bonus': result['rgo_expansion_total'],
                      'runtime_balance_verified': False}, indent=2))
