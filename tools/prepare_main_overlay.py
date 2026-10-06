"""Refresh only authored runtime art, culture tags and text for the main installer.

No terrain rebuild or user mod installation. The bundled release is immutable;
the main installer applies these checksum-listed files before normal installation.
"""
import hashlib,json
from pathlib import Path
import build as b,archipelago,export_goblin_models,verify_goblin_models,build_goblin_portraits
ROOT=b.ROOT

def main():
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--game',type=Path);args=ap.parse_args()
    output=ROOT/'mod'
    import exploration
    if not args.game:
        ap.error('--game is required to validate exploration locations and areas')
    exploration.build(b,args.game,output,validate_setup=False)
    report=export_goblin_models.build(output)
    portraits=build_goblin_portraits.build(output)
    import verify_goblin_portraits
    portraits["validation"]=verify_goblin_portraits.verify(output,args.game)
    verification=verify_goblin_models.verify(output,args.game)
    countries=b.CFG['countries']
    b.write(output,'in_game/common/cultures/goblins_ashborn_isles.txt','\n'.join(
        f'{c["culture"]} = {{ language = {c["culture"]}_dialect color = rgb {{ {" ".join(map(str,c["color"]))} }} tags = {{ european_gfx {c["culture"]}_gfx }} culture_groups = {{ cm_goblin_group }} opinions = {{ }} }}' for c in countries)+'\n')
    import ashborn_names
    ashborn_names.build_names(b,output)
    b.localization(output);archipelago.add_localization(b,output)
    paths=[p for prefix in ['in_game/gfx/models/units/ashborn_goblins','in_game/gfx/models/schematics','in_game/gfx/graphical_culture_types','main_menu/gfx/unit_graphics/units','main_menu/gfx/animation_state_machines'] for p in (output/prefix).rglob('*') if p.is_file()]
    paths.extend([output/'in_game/common/cultures/goblins_ashborn_isles.txt',output/'main_menu/localization/english/goblins_ashborn_isles_l_english.yml',output/'main_menu/gfx/unit_graphics/attachments/zz_ashborn_goblins.txt'])
    paths.extend(p for prefix in ['in_game/gfx/models/portraits/ashborn','in_game/common/ethnicities','main_menu/gfx/portraits'] for p in (output/prefix).rglob('*') if p.is_file())
    paths.append(output/'in_game/common/genes/zz_ashborn_portraits.txt')
    paths.append(output/'in_game/common/genes/zz_ashborn_outfits.txt')
    paths.append(output/'in_game/common/languages/goblins_ashborn_isles.txt')
    paths.extend(output/p for p in ['in_game/common/on_action/goblins_exploration.txt','in_game/events/goblins_exploration.txt','main_menu/localization/english/goblins_exploration_l_english.yml'])
    manifest={'base_release':b.CFG['version'],'stage':'development-models-and-culture-names','engine_tested':False,
              'files':[{'path':p.relative_to(output).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(paths)]}
    (ROOT/'data/main_overlay.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    (ROOT/'art/models/goblins/native_validation.json').write_text(json.dumps(verification,indent=2)+'\n')
    (ROOT/'art/models/goblins/native_export.json').write_text(json.dumps(report,indent=2)+'\n')
    (ROOT/'art/models/goblins/portrait_export.json').write_text(json.dumps(portraits,indent=2)+'\n')
    print(json.dumps({'overlay_files':len(paths),'verification':verification},indent=2))

if __name__=='__main__':main()
