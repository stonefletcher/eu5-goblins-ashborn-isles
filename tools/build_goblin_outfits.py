"""Culture-only rough clothing selection; references installed native accessories.

Native hide, fringe and fur materials inspected against the installed assets.
No native art is copied. Children retain fitted plain clothes, infants swaddling.
"""
from pathlib import Path

OUTFITS = {
    'male': [(5, 'male_clothes_iroquois_low_beadwork_shirt'),
             (3, 'male_clothes_iroquois_low_beadwork'),
             (2, 'male_clothes_iroquois_royal_bear_hunter')],
    'female': [(7, 'female_clothes_iroquois_common_overcoat'),
               (3, 'female_clothes_iroquois_noble_overcoat')],
    'boy': [(1, 'ger_child_cloth_set_a')],
    'girl': [(1, 'child_cloth')],
    # The native no_clothes template already supplies infant swaddling.
    'infant': [(1, 'empty')],
}
RESET = {'clothes': 'no_clothes', 'headwear': 'no_headwear',
         'capes': 'no_cape', 'neckware_neck': 'no_neckware_neck',
         'beards': 'no_beard'}

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
    mods = ['cm_ashborn_outfits = { usage = game selection_behavior = max priority = 120']
    for clan in clans:
        # Match native beard/headwear suppression: add the empty template with a
        # selection range. A zero-strength replace did not suppress noble outfits.
        dna = [f'accessory = {{ mode = add gene = {g} template = {t} range = {{ 0 1 }} }}'
               for g, t in RESET.items()]
        dna.append('accessory = { mode = add gene = cm_ashborn_clothing template = cm_rough_clothing range = { 0 1 } }')
        mods.append(f'cm_{clan["id"]}_rough_clothing = {{ ignore_outfit_tags = yes\n'
                    'dna_modifiers = {\n'+'\n'.join(dna)+'\n}\n'
                    f'weight = {{ base = 0 modifier = {{ add = 100 gfx_culture_applicable = {clan["culture"]}_gfx }} }} }}')
    mods.append('}')
    text(out/'main_menu/gfx/portraits/portrait_modifiers/zzz_ashborn_outfits.txt', '\n'.join(mods)+'\n')
    return {'method':'native hide tunics, fringed leather overcoats and fur-trimmed hunter garments; culture-scoped native add-template suppression, priority 120',
            'royal_clothes_and_crowns_suppression':'configured; in-game confirmation pending', 'engine_tested':False,
            'custom_rag_geometry':False, 'beards_removed':True,
            'adult_leather_garment_weight':1.0,
            'children':'native fitted plain clothes; no adult meshes on child rigs'}
