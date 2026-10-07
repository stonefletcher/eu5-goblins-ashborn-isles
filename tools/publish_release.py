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
    # Existing assets are immutable on retries. A specifically authorized source
    # tag correction may advance only the known tag while retaining those bytes.
    exists=subprocess.run(['gh','release','view',tag],capture_output=True)
    if exists.returncode==0:
        previous=manifest.get('source_tag_correction_from')
        if not previous:raise SystemExit('Release already exists; inspect it before making changes.')
        assert re.fullmatch('[0-9a-f]{40}',previous)
        repo=os.environ['GH_REPO']
        def api(endpoint):
            return json.loads(subprocess.check_output(['gh','api',f'repos/{repo}/{endpoint}'],text=True))
        release=api(f'releases/tags/{tag}')
        assert not release['draft'] and not release.get('immutable',False)
        wanted={a['name']:(a['size'],'sha256:'+a['sha256']) for a in manifest['assets']}
        actual={a['name']:(a['size'],a.get('digest')) for a in release['assets']}
        assert actual==wanted,'Existing release assets differ; correction refused'
        ref=api(f'git/ref/tags/{tag}')
        assert ref['object']['type']=='commit'
        current=ref['object']['sha']
        assert current in (previous,target),'Tag moved unexpectedly; correction refused'
        if current!=target:
            compare=api(f'compare/{current}...{target}')
            assert compare['status']=='ahead','Source correction must be a fast-forward'
            subprocess.run(['gh','api','--method','PATCH',f'repos/{repo}/git/refs/tags/{tag}',
                            '-f',f'sha={target}','-F','force=false'],check=True)
        subprocess.run(['gh','release','edit',tag,'--target',target,'--latest',
                        '--notes-file',str(root/f'RELEASE_NOTES_{version}.md')],check=True)
        print('Source tag corrected; verified release assets preserved.')
        return
    subprocess.run(['gh','release','create',tag,*files,'--target',target,
                    '--title',f'Goblins of the Ashborn Isles {version} - Rough-Clad Goblins',
                    '--notes-file',str(root/f'RELEASE_NOTES_{version}.md'),'--latest'],check=True)


if __name__=='__main__':main()

