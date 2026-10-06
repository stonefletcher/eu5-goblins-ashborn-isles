"""Check portrait references and native attachment compatibility; not a render test."""
import json,re,struct
from pathlib import Path
import numpy as np
from PIL import Image
from pdx_binary import read
from build_goblin_portraits import ROOT,ART,REL,TYPES

def verify(out,game=None):
    out=Path(out);folder=out/REL
    genes=(out/'in_game/common/genes/zz_ashborn_portraits.txt').read_text(encoding='utf-8-sig')
    modifiers=(out/'main_menu/gfx/portraits/portrait_modifiers/zz_ashborn.txt').read_text(encoding='utf-8-sig')
    ethnicity=(out/'in_game/common/ethnicities/ashborn.txt').read_text(encoding='utf-8-sig')
    gfx=(out/'in_game/gfx/graphical_culture_types/ashborn_goblins.txt').read_text(encoding='utf-8-sig')
    accessories=(out/'main_menu/gfx/portraits/accessories/ashborn.txt').read_text(encoding='utf-8-sig')
    asset=(folder/'ashborn_features.asset').read_text(encoding='utf-8-sig')
    for path in re.findall(r'"([^"\n]+\.(?:mesh|dds))"',asset):assert (folder/path).is_file(),path
    for path in re.findall(r'"(gfx/[^"\n]+\.dds)"',genes):assert (out/'in_game'/path).is_file(),path
    for entity in re.findall(r'entity = (cm_\w+)',accessories):assert f'name = "{entity}"' in asset,entity
    for name in re.findall(r'1 = "(cm_\w+)"',genes):assert name+' = {' in accessories,name
    clans=json.loads((ART/'clans.json').read_text())['clans']
    for clan in clans:
        ident=clan['id'];tag=clan['culture']+'_gfx'
        assert modifiers.count('gfx_culture_applicable = '+tag)==1
        assert f'100 = cm_{ident}_ethnicity' in gfx
        assert f'cm_{ident}_ethnicity = ' in ethnicity
        texture = folder/f'{ident}_skin.dds'
        raw = texture.read_bytes()
        assert raw[:4] == b'DDS ' and raw[84:88] == b'DXT5', texture
        assert struct.unpack_from('<II', raw, 12) == (1024, 1024), texture
        assert struct.unpack_from('<I', raw, 28)[0] == 11, texture
        assert len(raw) == 1398256, texture
        pixel = Image.open(texture).getpixel((0,0))
        target = bytes.fromhex(clan['skin_srgb'].lstrip('#'))
        assert all(abs(a-b) <= 4 for a,b in zip(pixel[:3], target)), texture
        assert pixel[3] == 255, texture
        if game:
            native_decal = Path(game)/'in_game/gfx/models/portraits/decals/male_body/decal_male_body_old_01_diffuse.dds'
            native_raw = native_decal.read_bytes()
            for start,end in [(12,20),(28,32),(76,108)]:
                assert raw[start:end] == native_raw[start:end], (texture, 'native texture array mismatch')
    for typ in TYPES:assert genes.count(typ+' = ')>=10,typ
    assert 'employer' not in modifiers and 'is_ruler' not in modifiers and 'is_female' not in modifiers
    triangles=0
    for sex in ['male','female','infant']:
        shape=read(folder/f'cm_{sex}_features.mesh')['children'][0]['children'][0]
        bones=next(c['children'] for c in shape['children'] if c['name']=='skeleton')
        if game:
            native=Path(game)/'in_game/gfx/models/portraits'
            native=native/(sex+'_head')/(sex+'_head.mesh') if sex!='infant' else native/'infant/infant_head_base.mesh'
            ns=read(native)['children'][0]['children'][0]
            nb={b['name']:b for b in next(c['children'] for c in ns['children'] if c['name']=='skeleton')}
            for bone in bones:assert np.allclose(bone['props']['tx'][1],nb[bone['name']]['props']['tx'][1]),bone['name']
        for mesh in [c for c in shape['children'] if c['name']=='mesh']:
            p=np.array(mesh['props']['p'][1]).reshape(-1,3);t=np.array(mesh['props']['tri'][1]).reshape(-1,3)
            skin=next(c['props'] for c in mesh['children'] if c['name']=='skin')
            assert np.isfinite(p).all() and t.min()>=0 and t.max()<len(p)
            assert np.allclose(np.linalg.norm(np.array(mesh['props']['n'][1]).reshape(-1,3),axis=1),1)
            assert min(skin['ix'][1])>=0 and max(skin['ix'][1])<len(bones)
            assert np.allclose(np.array(skin['w'][1]).reshape(-1,4).sum(axis=1),1)
            triangles+=len(t)
    for script in [genes,modifiers,accessories,asset,ethnicity]:assert script.count('{')==script.count('}')
    from build_goblin_outfits import OUTFITS, RESET
    outfit_genes=(out/'in_game/common/genes/zz_ashborn_outfits.txt').read_text(encoding='utf-8-sig')
    outfit_mods=(out/'main_menu/gfx/portraits/portrait_modifiers/zzz_ashborn_outfits.txt').read_text(encoding='utf-8-sig')
    for script in [outfit_genes,outfit_mods]:assert script.count('{')==script.count('}')
    assert 'priority = 100' in outfit_mods
    assert all(outfit_mods.count('gfx_culture_applicable = '+c['culture']+'_gfx')==1 for c in clans)
    assert all('mode = replace gene = '+g+' template = '+t in outfit_mods for g,t in RESET.items())
    assert OUTFITS['infant']==[(1,'empty')], 'Do not layer clothing over the native infant swaddle'
    if game:
        native_accessories=(Path(game)/'main_menu/gfx/portraits/accessories/clothes.txt').read_text(encoding='utf-8-sig')
        native_genes='\n'.join(p.read_text(encoding='utf-8-sig') for p in (Path(game)/'in_game/common/genes').glob('*.txt'))
        for choices in OUTFITS.values():
            for _,name in choices:
                assert name=='empty' or re.search(r'(?m)^'+re.escape(name)+r'\s*=\s*\{',native_accessories),name
        for template in RESET.values():assert re.search(r'\b'+template+r'\s*=\s*\{',native_genes),template
    return {'status':'static checks passed; in-game appearance unverified','cultures':5,'portrait_types':7,'attachment_triangles':triangles,'native_rig_bindings_checked':bool(game),'native_outfit_references_checked':bool(game),'engine_tested':False}

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=ROOT/'mod');ap.add_argument('--game',type=Path);a=ap.parse_args()
    print(json.dumps(verify(a.out,a.game),indent=2))
