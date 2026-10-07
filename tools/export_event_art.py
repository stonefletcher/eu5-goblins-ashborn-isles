"""Export original Ashborn paintings to native-sized DDS with full mip chains."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageOps
from build_infantry_art import dds
from event_art import ROOT, ART, EVENTS, SITUATIONS, EVENT_DIR


def build(out):
    images = {}
    files = []
    for name in ART:
        source = ROOT / 'art/events/sources' / (name + '.png')
        with Image.open(source) as original:
            images[name] = ImageOps.fit(original.convert('RGB'), (1080, 440), method=Image.Resampling.LANCZOS)
        files.append((f'{EVENT_DIR}/{name}.dds', images[name]))
    for name, art in SITUATIONS.items():
        files.append((f'main_menu/gfx/interface/illustrations/situation/{name}.dds', images[art]))
        # The icon is a deliberate square detail from the same commissioned painting.
        # Gathering: central envoy; Eastern Hunger: expedition ship in the center.
        icon = ImageOps.fit(images[art], (128, 128), method=Image.Resampling.LANCZOS)
        files.append((f'main_menu/gfx/interface/icons/situations/{name}.dds', icon))
    rows = []
    for rel, img in files:
        target = out / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        raw = dds(img, 'DXT1')
        target.write_bytes(raw)
        rows.append({'path': rel, 'size': list(img.size), 'sha256': hashlib.sha256(raw).hexdigest()})
    return {'events': EVENTS, 'situations': SITUATIONS, 'original_paintings': len(ART),
            'format': 'DDS BC1/DXT1, full mip chain', 'files': rows, 'engine_tested': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, default=ROOT / 'mod')
    args = parser.parse_args()
    report = build(args.out)
    (ROOT / 'art/events/exports.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'paintings': report['original_paintings'], 'textures': len(report['files'])}))
