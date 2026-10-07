"""Package generated output and authored sources; do not install or publish."""
from pathlib import Path
import json,zipfile
ROOT=Path(__file__).resolve().parents[1]
version=json.loads((ROOT/'data/island.json').read_text())['version']
report=ROOT/'build/reports/validation.json'
if not report.is_file():raise SystemExit('Run build.py successfully first.')
checks=json.loads(report.read_text())
if checks['version']!=version:raise SystemExit('Rebuild before packaging this version.')
output=ROOT/'build/goblins_ashborn_isles'
metadata=json.loads((output/'.metadata/metadata.json').read_text())
manifest=json.loads((ROOT/'build/terrain_patch/manifest.json').read_text())
if metadata['id']!='alex.goblins_ashborn_isles' or metadata['version']!=version or manifest['version']!=version:
    raise SystemExit('Metadata/terrain version mismatch: rebuild first.')
for item in manifest['files']:
    p=output/item['path']
    if not p.is_file() or p.stat().st_size!=item['final_size'] or not p.with_suffix('.info').is_file():
        raise SystemExit('Incomplete terrain build.')
for filename in ['10_countries.txt','06_pops.txt','07_cities_and_buildings.txt','03_markets.txt']:
    if not (output/'main_menu/setup/start'/filename).is_file():raise SystemExit('Incomplete campaign setup.')
dist=ROOT/'dist';dist.mkdir(exist_ok=True)
docs=['NAMING_PROPOSALS.md','README.md','TESTING.md','LORE.md','RELEASE_NOTES.md','PROTOTYPE_055.md','STEAM_DESCRIPTION.txt','STEAM_CHANGELOG.txt','Install-Goblins.ps1','Install-Goblins.cmd']
with zipfile.ZipFile(dist/f'Goblins_Ashborn_Isles_{version}.zip','w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted((ROOT/'build/goblins_ashborn_isles').rglob('*')):
        if p.is_file() and not (p.suffix=='.bin' and 'terrain_cache' in p.parts):z.write(p,'goblins_ashborn_isles/'+p.relative_to(ROOT/'build/goblins_ashborn_isles').as_posix())
    for p in sorted((ROOT/'build/terrain_patch').iterdir()):
        if p.is_file():z.write(p,'terrain_patch/'+p.name)
    for name in docs:z.write(ROOT/name,name)
    for name in ['validation.json','terrain_verification.json','feature_verification.json','model_export.json','model_verification.json','portrait_verification.json','Goblins_Map_Preview.png','Goblins_Terrain_Preview.png','Goblins_Cache_Relief.png']:
        p=ROOT/'build/reports'/name
        if p.is_file():z.write(p,'reports/'+p.name)
    for p in sorted((ROOT/'art').glob('*')):
        if p.is_file():z.write(p,'art/'+p.name)
    for name in ['art/events/README.md','art/flags/README.md','art/events/sources/gathering.png']:
        z.write(ROOT/name,name)
with zipfile.ZipFile(dist/f'Goblins_Ashborn_Isles_Source_{version}.zip','w',zipfile.ZIP_DEFLATED) as z:
    for name in docs+['requirements.txt','.gitignore','.gitattributes']:z.write(ROOT/name,'goblins-ashborn-isles-source/'+name)
    for folder in ['data','mod','tools','art','.github']:
        for p in sorted((ROOT/folder).rglob('*')):
            if p.is_file() and '__pycache__' not in p.parts:z.write(p,'goblins-ashborn-isles-source/'+p.relative_to(ROOT).as_posix())
for p in dist.iterdir():print(f'{p.name}: {p.stat().st_size:,} bytes')
