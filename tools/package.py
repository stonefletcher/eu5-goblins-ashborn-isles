"""Package generated output and authored sources; do not install or publish."""
from pathlib import Path
import json,zipfile
ROOT=Path(__file__).resolve().parents[1]
version=json.loads((ROOT/'data/island.json').read_text())['version']
report=ROOT/'build/reports/validation.json'
if not report.is_file():raise SystemExit('Run build.py successfully first.')
checks=json.loads(report.read_text())
if checks['version']!=version:raise SystemExit('Rebuild before packaging this version.')
dist=ROOT/'dist';dist.mkdir(exist_ok=True)
docs=['README.md','TESTING.md','LORE.md','Install-Cindermaw.ps1','Install-Cindermaw.cmd']
with zipfile.ZipFile(dist/f'Cindermaw_Demo_{version}.zip','w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted((ROOT/'build/cindermaw_demo').rglob('*')):
        if p.is_file() and not (p.suffix=='.bin' and 'terrain_cache' in p.parts):z.write(p,'cindermaw_demo/'+p.relative_to(ROOT/'build/cindermaw_demo').as_posix())
    for p in sorted((ROOT/'build/terrain_patch').iterdir()):
        if p.is_file():z.write(p,'terrain_patch/'+p.name)
    for name in docs:z.write(ROOT/name,name)
    for p in (ROOT/'build/reports').iterdir():
        if p.is_file():z.write(p,'reports/'+p.name)
with zipfile.ZipFile(dist/f'Cindermaw_Source_{version}.zip','w',zipfile.ZIP_DEFLATED) as z:
    for name in docs+['requirements.txt','.gitignore']:z.write(ROOT/name,'cindermaw-source/'+name)
    for folder in ['data','mod','tools','art']:
        for p in sorted((ROOT/folder).rglob('*')):
            if p.is_file() and '__pycache__' not in p.parts:z.write(p,'cindermaw-source/'+p.relative_to(ROOT).as_posix())
for p in dist.iterdir():print(f'{p.name}: {p.stat().st_size:,} bytes')
