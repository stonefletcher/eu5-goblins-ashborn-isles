"""Build the small additive prototype manifest without bundling terrain or game assets."""
from pathlib import Path
import hashlib
import json
from clan_identity import SOURCES
from event_art import runtime_paths

ROOT = Path(__file__).resolve().parents[1]

def main():
    cfg = json.loads((ROOT / 'data/island.json').read_text(encoding='utf-8-sig'))
    paths = sorted((ROOT / 'mod').glob('in_game/common/**/goblins_gathering.txt'))
    paths += [ROOT / 'mod/in_game/events/goblins_gathering.txt',
              ROOT / 'mod/main_menu/common/static_modifiers/goblins_gathering.txt',
              ROOT / 'mod/main_menu/localization/english/goblins_gathering_l_english.yml']
    assert len(paths) == 10
    paths += [ROOT / 'mod/in_game/events/goblins_ashborn_isles.txt',
              ROOT / 'mod/in_game/events/goblins_exploration.txt']
    paths += [ROOT / 'mod' / rel for rel in runtime_paths()]
    from build_clan_flags import runtime_paths as flag_paths
    paths += [ROOT / 'mod' / rel for rel in flag_paths()]
    paths = sorted(set(paths))
    import mixed_populations
    population_additions = {ident: '\n'.join(mixed_populations.rows(ident)) for ident in mixed_populations.additions()}
    manifest = {'population_additions': population_additions, 'version': '0.5.5', 'base_version': '0.5.4',
                'identities': [{'tag': tag, 'path': 'data/'+name+'.json',
                                'sha256': hashlib.sha256((ROOT / 'data' / (name+'.json')).read_bytes()).hexdigest()}
                               for tag,name in SOURCES.items()],
                'homeland_locations': [x['id'] for island in cfg['islands'] for x in island['locations']],
                'files': [{'path': p.relative_to(ROOT / 'mod').as_posix(),
                           'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths]}
    (ROOT / 'data/prototype_055_files.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8',newline='\n')
    print(json.dumps({'files': len(paths), 'homeland_locations': len(manifest['homeland_locations'])}))

if __name__ == '__main__': main()
