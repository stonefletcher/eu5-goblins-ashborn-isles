"""Validate the source-download installer bundle without a local build or EU5."""
import base64, hashlib, io, json, re, zipfile
from decimal import Decimal
from datetime import date
from pathlib import Path

def verify(root):
    root=Path(root)
    source=(root/'data/island.json').read_text(encoding='utf-8')
    config=json.loads(source)
    release=json.loads((root/'.release/manifest.json').read_text())
    overlay=json.loads((root/'data/main_overlay.json').read_text())
    version=config['version']
    assert version==release['version']==overlay['base_release'],'Source, bundle and overlay versions differ'
    digest=lambda b:hashlib.sha256(b).hexdigest()
    assert digest(source.encode())==release['source_config_sha256'],'Stale source configuration hash'
    asset=next(a for a in release['assets'] if a['name']==f'Goblins_Ashborn_Isles_{version}.zip')
    chunks=[]
    for path in asset['chunks']:
        assert re.fullmatch(r'assets/[A-Za-z0-9_.-]+',path),path
        chunks.append(base64.b64decode((root/'.release'/path).read_bytes(),validate=True))
    raw=b''.join(chunks)
    assert len(raw)==asset['size'] and digest(raw)==asset['sha256'],'Corrupt archive transport'
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        assert len(z.namelist())==len(set(z.namelist())),'Duplicate archive members'
        assert z.testzip() is None,'ZIP CRC failure'
        metadata=json.loads(z.read('goblins_ashborn_isles/.metadata/metadata.json'))
        terrain=json.loads(z.read('terrain_patch/manifest.json'))
        report=json.loads(z.read('reports/validation.json'))
        assert version==metadata['version']==terrain['version']==report['version'],'Stale packaged metadata or terrain'
        assert metadata['id']=='alex.goblins_ashborn_isles'
        assert z.read('Install-Goblins.ps1').decode('utf-8-sig').replace('\r\n','\n')==(root/'Install-Goblins.ps1').read_text(encoding='utf-8-sig'),'Stale embedded installer'
        assert len(terrain['files'])==3
        for item in terrain['files']:
            assert item['final_size']>item['source_size']
            assert len(z.read('terrain_patch/'+item['delta']))==item['final_size']-item['source_size']
            assert z.read('goblins_ashborn_isles/'+str(Path(item['path']).with_suffix('.info')).replace('\\','/'))
        for name in ['10_countries.txt','06_pops.txt','07_cities_and_buildings.txt','03_markets.txt']:
            assert z.read('goblins_ashborn_isles/main_menu/setup/start/'+name)
        if 'country_population_targets' in config:
            # Check the delivered setup, not merely the manifest's claimed config hash.
            pops=z.read('goblins_ashborn_isles/main_menu/setup/start/06_pops.txt').decode('utf-8-sig')
            actual={tag:0 for tag in config['country_population_targets']}
            for island in config['islands']:
                for location in island['locations']:
                    start=re.search(r'(?m)^\s*'+re.escape(location['id'])+r'\s*=\s*\{',pops)
                    assert start,location['id']
                    depth=1;end=start.end()
                    while depth:
                        depth+=(pops[end]=='{')-(pops[end]=='}');end+=1
                    n=sum(Decimal(v) for v in re.findall(r'\bsize\s*=\s*([\d.]+)',pops[start.end():end]))
                    assert n==Decimal(str(location['pop'])),f'Stale packaged population: {location["id"]}'
                    actual[island['country']]+=int(n*1000)
            assert actual==config['country_population_targets']==report['economy']['country_populations']
            assert sum(actual.values())==config['population_target']
            assert report['economy']['longevity']['goblin_character_life_expectancy_bonus_years']==15
            assert report['economy']['longevity']['starting_ruler_ages']==config['starting_ruler_ages']
            chars=z.read('goblins_ashborn_isles/main_menu/setup/start/05_characters.txt').decode('utf-8-sig')
            now=date(1337,11,11)
            for tag,expected in config['starting_ruler_ages'].items():
                ident='cm_sfk_maarka' if tag=='SFK' else 'cm_'+tag.lower()+'_ruler'
                row=re.search(r'(?m)^\s*'+ident+r'\s*=\s*\{[^\r\n]+',chars)
                assert row,ident
                born=date(*map(int,re.search(r'birth_date = ([\d.]+)',row[0])[1].split('.')))
                age=now.year-born.year-((now.month,now.day)<(born.month,born.day))
                assert age==expected,f'Stale packaged ruler age: {tag}'
        for item in overlay['files']:
            path=item['path']
            assert re.fullmatch(r'[A-Za-z0-9_./-]+',path) and '..' not in Path(path).parts and not path.startswith('/')
            authored=(root/'mod'/path).read_bytes()
            assert digest(authored)==item['sha256'],f'Overlay checksum mismatch: {path}'
            assert z.read('goblins_ashborn_isles/'+path)==authored,f'Stale bundled art: {path}'
    return {'version':version,'overlay_files':len(overlay['files']),'archive_bytes':len(raw),'status':'prepared bundle verified'}

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);args=ap.parse_args()
    print(json.dumps(verify(args.root),indent=2))
