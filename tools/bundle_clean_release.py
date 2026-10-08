"""Create compact prepared-release transport from a freshly validated player ZIP."""
import base64
import hashlib
import json
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    source = (ROOT / 'data/island.json').read_text(encoding='utf-8')
    version = json.loads(source)['version']
    archive = ROOT / 'dist' / f'Goblins_Ashborn_Isles_{version}.zip'
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        assert len(z.namelist()) == len(set(z.namelist()))
        assert json.loads(z.read('reports/validation.json'))['version'] == version
    raw = archive.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    release = ROOT / '.release'
    assets = release / 'assets'
    assets.mkdir(parents=True, exist_ok=True)
    chunks = []
    for i, offset in enumerate(range(0, len(raw), 512 * 1024)):
        name = f'assets/{version}-{digest[:12]}-{i:04d}.b64'
        (release / name).write_bytes(base64.b64encode(raw[offset:offset + 512 * 1024]))
        chunks.append(name)
    manifest = {'version': version,
                'source_commit': subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, text=True).strip(),
                'source_config_sha256': hashlib.sha256(source.encode()).hexdigest(),
                'assets': [{'name': archive.name, 'size': len(raw), 'sha256': digest, 'chunks': chunks}]}
    (release / 'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
    # Only reproducible archive chunks in this checkout's exact assets folder.
    for path in assets.glob('*.b64'):
        assert path.resolve().parent == assets.resolve()
        if path.relative_to(release).as_posix() not in chunks:
            path.unlink()
    from verify_prepared_bundle import verify
    print(json.dumps(verify(ROOT), indent=2))


if __name__ == '__main__':
    main()
