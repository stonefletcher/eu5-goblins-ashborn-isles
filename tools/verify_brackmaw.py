"""Compare prepared add-on with its base and the full-build character generator."""
from pathlib import Path
import argparse
import json
import re
import shutil
import tempfile
from types import SimpleNamespace

import ashborn_names
from verify_055 import parse


def verify(base, out):
    data = ashborn_names.BRACKMAW
    charrel = 'main_menu/setup/start/05_characters.txt'
    locrel = 'main_menu/localization/english/goblins_ashborn_isles_l_english.yml'
    before = (base / charrel).read_text(encoding='utf-8-sig')
    after = (out / charrel).read_text(encoding='utf-8-sig')
    pattern = r'(?m)^cm_qbr_ruler = \{[^\r\n]*\}'
    old, new = re.search(pattern, before)[0], re.search(pattern, after)[0]
    assert before.replace(old, '') == after.replace(new, ''), 'Unrelated characters changed'
    old_fields, new_fields = dict((k, v) for k, _, v in parse(old)[0][2]), dict((k, v) for k, _, v in parse(new)[0][2])
    for stat in ('adm', 'dip', 'mil'):
        assert new_fields.pop(stat) == str(data[stat])
        old_fields.pop(stat)
    assert new_fields.pop('nickname') == [('name', '=', data['nickname_key'])]
    assert new_fields == old_fields, 'Identity, family or chronology changed'
    def localization(path):
        text = path.read_text(encoding='utf-8-sig')
        rows = re.findall(r'(?m)^ ([\w.]+):\s*"(.*)"\s*$', text)
        assert len(rows) == len(dict(rows)), 'Duplicate localization'
        assert path.read_bytes().startswith(b'\xef\xbb\xbf')
        return dict(rows)
    original, changed = localization(base / locrel), localization(out / locrel)
    assert changed.pop(data['nickname_key']) == data['nickname']
    assert changed.pop('cm_brinekin_desc') == data['culture_description']
    original.pop('cm_brinekin_desc')
    assert original == changed, 'Unrelated localization changed'
    # Generate authored courts separately, then compare Murgash with the installed add-on.
    cfg = json.loads((Path(__file__).resolve().parents[1] / 'data/island.json').read_text())
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        for rel, block in [(charrel, 'character_db'), ('main_menu/setup/start/04_dynasties.txt', 'dynasty_manager')]:
            path = root / rel; path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(block + ' = {\n}\n', encoding='utf-8')
        def write(root, rel, text): (root / rel).write_text(text, encoding='utf-8')
        def inject(text, block, addition): return text[:text.rfind('}')] + addition + '\n}\n'
        ashborn_names.build_courts(SimpleNamespace(CFG=cfg, write=write, inject=inject), root)
        generated = re.search(pattern, (root / charrel).read_text())[0]
        assert parse(generated) == parse(new), 'Full build and add-on disagree'
    return {'brackmaw_character_and_localization': True, 'unrelated_base_entries_preserved': True,
            'full_build_matches_addon': True, 'gameplay_tested': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--base', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(verify(args.base, args.out), indent=2))
