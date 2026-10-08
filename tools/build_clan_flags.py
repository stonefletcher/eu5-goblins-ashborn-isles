"""Export five reference-matched clan flags using native textured emblems."""
from pathlib import Path
import argparse
import hashlib
import io
import json
import struct
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
FLAGS = json.loads((ROOT / 'data/clan_flags.json').read_text(encoding='utf-8'))
COATS = 'main_menu/common/coat_of_arms/coat_of_arms/goblins_ashborn_isles.txt'
TEXTURES = 'main_menu/gfx/coat_of_arms/textured_emblems'


def runtime_paths():
    return [COATS] + [f'{TEXTURES}/te_ashborn_{v["source"]}.dds' for v in FLAGS.values()]


def rgba_dds(image):
    width, height = image.size
    levels = []
    while True:
        buffer = io.BytesIO()
        image.save(buffer, format='DDS', pixel_format='DXT5')
        raw = buffer.getvalue()
        assert raw[84:88] == b'DXT5'
        levels.append(raw[128:])
        if image.size == (1, 1):
            break
        image = image.resize((max(1, image.width // 2), max(1, image.height // 2)), Image.Resampling.LANCZOS)
    header = [124, 0xA1007, height, width, len(levels[0]), 0, len(levels)] + [0] * 11
    header += [32, 4, int.from_bytes(b'DXT5', 'little'), 0, 0, 0, 0, 0]
    header += [0x401008, 0, 0, 0, 0]
    return b'DDS ' + struct.pack('<31I', *header) + b''.join(levels)


def build(out):
    definitions = []
    report = []
    for tag, flag in FLAGS.items():
        texture = f'te_ashborn_{flag["source"]}.dds'
        with Image.open(ROOT / 'art/flags/sources' / (flag['source'] + '.png')) as source:
            assert source.size == (384, 256) and source.mode == 'RGBA'
            raw = rgba_dds(source.copy())
        target = out / TEXTURES / texture
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        color = ' '.join(map(str, flag['field']))
        definitions.append(f'''{tag} = {{
    pattern = "pattern_solid.dds"
    color1 = rgb {{ {color} }}
    textured_emblem = {{
        texture = "{texture}"
        instance = {{ position = {{ 0.5 0.5 }} scale = {{ 1.0 1.0 }} }}
    }}
}}''')
        report.append({'tag': tag, 'path': target.relative_to(out).as_posix(),
                       'sha256': hashlib.sha256(raw).hexdigest()})
    target = out / COATS
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text('\n\n'.join(definitions) + '\n', encoding='utf-8', newline='\r\n')
    return {'clans': len(FLAGS), 'emblems': report, 'dimensions': [384, 256],
            'format': 'BC3/DXT5 with alpha and nine mip levels', 'engine_render_tested': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, default=ROOT / 'mod')
    args = parser.parse_args()
    result = build(args.out)
    (ROOT / 'art/flags/exports.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2))
