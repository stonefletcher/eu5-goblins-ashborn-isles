"""Verify and publish a prepared release; refresh documentation only."""
from pathlib import Path
import base64, hashlib, json, os, re, subprocess, zipfile
from verify_prepared_bundle import verify

DOCUMENTS = ['README.md', 'RELEASE_NOTES.md', 'TESTING.md',
             'WORKSHOP_UPLOAD.md', 'STEAM_DESCRIPTION.txt', 'STEAM_CHANGELOG.txt']

def main():
    root = Path(__file__).resolve().parents[1]
    manifest_path = root / '.release/manifest.json'
    manifest = json.loads(manifest_path.read_text())
    version = manifest['version']
    assert re.fullmatch(r'\d+\.\d+\.\d+', version)
    branch = 'release/v' + version
    assert os.environ['GITHUB_REF_NAME'] == branch
    tag = 'v' + version
    exists = subprocess.run(['gh', 'release', 'view', tag], capture_output=True)
    if exists.returncode == 0:
        raise SystemExit('Release already exists; inspect it before changing its assets.')
    print(json.dumps(verify(root), indent=2), flush=True)
    assert len(manifest['assets']) == 1, 'Use the standard installer package only'
    item = manifest['assets'][0]
    assert item['name'] == f'Goblins_Ashborn_Isles_{version}.zip'
    raw = b''.join(base64.b64decode((root / '.release' / chunk).read_bytes(), validate=True)
                   for chunk in item['chunks'])
    assert len(raw) == item['size']
    assert hashlib.sha256(raw).hexdigest() == item['sha256']
    destination = root / 'dist'
    destination.mkdir(exist_ok=True)
    path = destination / item['name']
    path.write_bytes(raw)
    documents = DOCUMENTS + [f'RELEASE_NOTES_{version}.md']
    replacement = {name: (root / name).read_bytes() for name in documents}
    with zipfile.ZipFile(path) as archive:
        changed = {name: data for name, data in replacement.items()
                   if name not in archive.namelist() or archive.read(name) != data}
        original_members = {entry.filename: (entry.CRC, entry.file_size)
                            for entry in archive.infolist()
                            if entry.filename not in replacement}
    if changed:
        with zipfile.ZipFile(path, 'a', zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
            archive.start_dir = len(raw)
            archive.filelist = [entry for entry in archive.filelist if entry.filename not in changed]
            archive.NameToInfo = {entry.filename: entry for entry in archive.filelist}
            for name, data in changed.items():
                archive.writestr(name, data)
        complete = path.read_bytes()
        assert complete[:len(raw)] == raw
        suffix = complete[len(raw):]
        digest = hashlib.sha256(suffix).hexdigest()
        for index, offset in enumerate(range(0, len(suffix), 512 * 1024)):
            chunk = f'assets/{item["name"]}.docs.{digest[:12]}.{index:04d}.b64'
            (root / '.release' / chunk).write_bytes(base64.b64encode(suffix[offset:offset + 512 * 1024]))
            item['chunks'].append(chunk)
        item['size'] = len(complete)
        item['sha256'] = hashlib.sha256(complete).hexdigest()
    manifest['source_commit'] = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
    manifest['release_branch'] = branch
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(verify(root), indent=2), flush=True)
    with zipfile.ZipFile(path) as archive:
        assert len(archive.namelist()) == len(set(archive.namelist()))
        for name, data in replacement.items():
            assert archive.read(name) == data, name
        final_members = {entry.filename: (entry.CRC, entry.file_size)
                         for entry in archive.infolist() if entry.filename not in replacement}
        assert final_members == original_members, 'Non-document members changed'
        assert archive.testzip() is None
    subprocess.run(['git', 'config', 'user.name', 'github-actions[bot]'], check=True)
    subprocess.run(['git', 'config', 'user.email', '41898282+github-actions[bot]@users.noreply.github.com'], check=True)
    subprocess.run(['git', 'add', '.release'], check=True)
    if subprocess.run(['git', 'diff', '--cached', '--quiet']).returncode:
        subprocess.run(['git', 'commit', '-m', f'Finalize {version} package documentation and checksums [skip ci]'], check=True)
        subprocess.run(['git', 'push', 'origin', f'HEAD:refs/heads/{branch}'], check=True)
    target = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
    assert not subprocess.check_output(['git', 'status', '--porcelain', '--untracked-files=no'], text=True).strip()
    checksum = destination / 'SHA256SUMS.txt'
    checksum.write_text(f'{item["sha256"]}  {item["name"]}\n', encoding='utf-8')
    print(f'Verified release commit: {target}', flush=True)
    subprocess.run(['gh', 'release', 'create', tag, str(path), str(checksum),
                    '--target', target,
                    '--title', f'Goblins of the Ashborn Isles {version} - Districts and Dynasties',
                    '--notes-file', str(root / f'RELEASE_NOTES_{version}.md'),
                    '--latest'], check=True)

if __name__ == '__main__':
    main()
