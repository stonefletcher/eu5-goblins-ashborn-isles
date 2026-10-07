"""Culture-only rough clothing selection; references installed native accessories.

First pass: plain wraps, harnesses and overcoats. No native art is copied.
Custom torn hems, patches and distressed materials remain an art follow-up.
"""
from pathlib import Path

OUTFITS = {
    'male': [(4, 'male_clothes_deccan_commoner_harness'),
             (3, 'male_clothes_aztec_common_tilmatl'),
             (2, 'male_clothes_german_common_short_sleeves_jacket')],
    'female': [(4, 'female_clothes_iroquois_common_overcoat'),
               (3, 'female_clothes_aztec_common_huipilli'),
               (2, 'female_clothes_syrian_common_dress_scarf')],
    'boy': [(1, 'ger_child_cloth_set_a')],
    'girl': [(1, 'child_cloth')],
    # The native no_clothes template already supplies infant swaddling.
    'infant': [(1, 'empty')],
}
RESET = {'clothes': 'no_clothes', 'headwear': 'no_headwear',
         'capes': 'no_cape', 'neckware_neck': 'no_neckware_neck'}

def build(out, clans):
    from build_goblin_portraits import text
    out = Path(out)
    # Separate custom gene avoids replacing vanilla clothing template definitions.
    genes = ['special_genes = {\naccessory_genes = { cm_ashborn_clothing = { inheritable = no',
             'cm_rough_clothing = { index = 0']
    for sex, choices in OUTFITS.items():
        genes.append(sex + ' = { ' + ' '.join(f'{w} = "{a}"' for w, a in choices) + ' }')
    genes += ['adolescent_boy = boy adolescent_girl = girl', '} } } }']
    text(out/'in_game/common/genes/zz_ashborn_outfits.txt', '\n'.join(genes)+'\n')
    mods = ['cm_ashborn_outfits = { usage = game priority = 100']
    for clan in clans:
        dna = [f'accessory = {{ mode = replace gene = {g} template = {t} value = 0 }}'
               for g, t in RESET.items()]
        dna.append('accessory = { mode = add gene = cm_ashborn_clothing template = cm_rough_clothing range = { 0 1 } }')
        mods.append(f'cm_{clan["id"]}_rough_clothing = {{ ignore_outfit_tags = yes\n'
                    'dna_modifiers = {\n'+'\n'.join(dna)+'\n}\n'
                    f'weight = {{ base = 0 modifier = {{ add = 100 gfx_culture_applicable = {clan["culture"]}_gfx }} }} }}')
    mods.append('}')
    text(out/'main_menu/gfx/portraits/portrait_modifiers/zzz_ashborn_outfits.txt', '\n'.join(mods)+'\n')
    return {'method':'native plain garments, culture-scoped, priority 100',
            'royal_clothes_and_crowns_removed':True, 'engine_tested':False,
            'custom_rag_geometry':False}
