"""Publish hash-verified, locally built archives from a release transport branch.

The runner cannot build EU5 assets without a licensed game installation. Archives
are therefore transported in base64 chunks on release/*, never generated from
unavailable game files or included in the main source tree.
"""
from pathlib import Path
import base64, hashlib, json, os, re, subprocess, zipfile


def main():
    root=Path(__file__).resolve().parents[1]
    manifest=json.loads((root/'.release/manifest.json').read_text())
    version=manifest['version']
    assert re.fullmatch(r'\d+\.\d+\.\d+',version)
    assert version==json.loads((root/'data/island.json').read_text())['version']
    assert os.environ['GITHUB_REF_NAME']=='release/v'+version
    target=manifest['source_commit'];assert re.fullmatch('[0-9a-f]{40}',target)
    destination=root/'dist';destination.mkdir(exist_ok=True)
    files=[]
    for item in manifest['assets']:
        name=item['name'];assert re.fullmatch(r'[A-Za-z0-9_.-]+\.zip',name)
        data=bytearray()
        for chunk in item['chunks']:
            assert re.fullmatch(r'assets/[A-Za-z0-9_.-]+',chunk)
            data.extend(base64.b64decode((root/'.release'/chunk).read_bytes(),validate=True))
        assert len(data)==item['size']
        assert hashlib.sha256(data).hexdigest()==item['sha256']
        path=destination/name;path.write_bytes(data)
        with zipfile.ZipFile(path) as archive:assert archive.testzip() is None
        files.append(str(path))
    tag='v'+version
    # Do not replace an existing release or its assets on a retry.
    exists=subprocess.run(['gh','release','view',tag],capture_output=True)
    if exists.returncode==0:raise SystemExit('Release already exists; inspect it before making changes.')
    notes=root/f'RELEASE_NOTES_{version}.md'
    if not notes.is_file():notes=root/'RELEASE_NOTES.md'
    subprocess.run(['gh','release','create',tag,*files,'--target',target,
                    '--title',f'Goblins of the Ashborn Isles {version}',
                    '--notes-file',str(notes)],check=True)


if __name__=='__main__':main()
