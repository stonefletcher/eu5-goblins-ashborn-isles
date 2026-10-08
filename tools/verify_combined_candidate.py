"""Guard the prior release fixes alongside the newer gameplay candidate."""
import re
from verify_055 import parse, flatten

def verify(read):
    asset = read('in_game/gfx/models/portraits/ashborn/ashborn_features.asset')
    assert asset.count('shader = "portrait_skin"') == 15
    assert asset.count('file = "ssao.dds" index = 3') == 15
    assert asset.count('portrait_decal = { body_part = head }') == 15
    assert 'portrait_attachment' not in asset
    assert 'ear_base.dds' in asset
    genes = read('in_game/common/genes/zz_ashborn_portraits.txt')
    assert 'cm_ashborn' in genes and 'old_forehead' in genes
    sites = read('in_game/common/holy_sites/ashen_covenant.txt')
    levels = re.findall(r'importance = (\d+)', sites)
    assert len(levels) == 9 and set(levels) == set('12345')
    panel = read('in_game/gui/panels/situation/ga_gathering_of_five.gui')
    for tag in ['CDM','QBR','RHK','SFK','SWK']:
        assert panel.count("[GetCountry('"+tag+"')]") == 1
    assert panel.count('text = "ga_gathering_annexed"') == 5
    body = panel[panel.index('blockoverride "situation_panel_main_content"'):]
    assert 'ga_ui_compact_route' in body and 'ga_ui_homeland_progress' in body
    assert panel.count('action_name = "ga_commission_voyage"') == 2
    values = dict((k,v) for k,_,v in parse(read('in_game/common/script_values/ga_gathering_ui.txt')))
    assert values['ga_gathering_realm_locations'] == [('value','=','ga_ui_homeland_count')]
    assert {v for k,_,v in flatten(values['ga_gathering_crown_status']) if k=='is_subject_type'} == {'vassal','ga_compact_autonomy','ga_compact_protection'}
    return {'skin_materials':15,'holy_sites':9,'founding_crown_rows':5,
            'shared_current_ownership_counter':True,'active_and_ended_voyage_controls':True,
            'engine_visual_acceptance':False}
