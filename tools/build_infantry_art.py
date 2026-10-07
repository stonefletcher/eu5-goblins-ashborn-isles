"""Culture-scoped 2D infantry illustrations; native definitions remain unchanged."""
from pathlib import Path
import argparse, hashlib, io, json, re, struct
from PIL import Image, ImageOps
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
REL = Path('main_menu/gfx/interface/illustrations/units')

def blocks(text):
    text = re.sub(r'#[^\n]*', '', text)
    result = {}
    for m in re.finditer(r'(?m)^(\w+)\s*=\s*\{', text):
        depth, end = 1, m.end()
        while depth:
            depth += (text[end] == '{') - (text[end] == '}')
            end += 1
        result[m[1]] = text[m.end():end-1]
    return result

def infantry_types(game):
    definitions = {}
    for p in sorted((game/'in_game/common/unit_types').glob('*.txt')):
        definitions.update(blocks(p.read_text(encoding='utf-8-sig')))
    def category(key, seen=()):
        if key in seen: raise ValueError('Circular unit inheritance: '+key)
        body = definitions[key]
        direct = re.search(r'\bcategory\s*=\s*(\w+)', body)
        if direct: return direct[1]
        parent = re.search(r'\bcopy_from\s*=\s*(\w+)', body)
        return category(parent[1], seen+(key,)) if parent else None
    return sorted(k for k in definitions if category(k) in ('army_light_infantry', 'army_heavy_infantry'))

def dds(image, pixel_format):
    width, height = image.size
    levels = []
    while True:
        if pixel_format == 'DXT5':
            # The mask is fully transparent black; no country-color recoloring.
            levels.append(bytes(((image.width+3)//4)*((image.height+3)//4)*16))
        else:
            pixels=np.asarray(image.convert('RGB'),dtype=np.int32)
            pixels=np.pad(pixels,((0,(-image.height)%4),(0,(-image.width)%4),(0,0)),mode='edge')
            blocks=pixels.reshape(pixels.shape[0]//4,4,pixels.shape[1]//4,4,3).transpose(0,2,1,3,4).reshape(-1,16,3)
            def pack(rgb):
                return ((rgb[:,0]>>3)<<11)|((rgb[:,1]>>2)<<5)|(rgb[:,2]>>3)
            hi=pack(blocks.max(axis=1));lo=pack(blocks.min(axis=1))
            hi=np.maximum(hi,1);lo=np.minimum(lo,hi-1)
            def unpack(v):
                r=(v>>11)&31;g=(v>>5)&63;b=v&31
                return np.stack(((r<<3)|(r>>2),(g<<2)|(g>>4),(b<<3)|(b>>2)),axis=1)
            a,b=unpack(hi),unpack(lo)
            colors=np.stack((a,b,(2*a+b)//3,(a+2*b)//3),axis=1)
            indices=((blocks[:,:,None,:]-colors[:,None,:,:])**2).sum(axis=3).argmin(axis=2)
            packed=(indices.astype(np.uint32) << (2*np.arange(16,dtype=np.uint32))).sum(axis=1,dtype=np.uint32)
            encoded=np.empty(len(blocks),dtype=[('hi','<u2'),('lo','<u2'),('idx','<u4')])
            encoded['hi']=hi;encoded['lo']=lo;encoded['idx']=packed
            levels.append(encoded.tobytes())
        if image.size == (1, 1): break
        image = image.resize((max(1,image.width//2),max(1,image.height//2)),Image.Resampling.LANCZOS)
    header=[124,0xA1007,height,width,len(levels[0]),0,len(levels)]+[0]*11
    header += [32,4,int.from_bytes(pixel_format.encode(),'little'),0,0,0,0,0]
    header += [0x401008,0,0,0,0]
    return b'DDS '+struct.pack('<31I',*header)+b''.join(levels)

def build(game, output):
    config = json.loads((ROOT/'data/island.json').read_text())
    cultures = [c['culture']+'_gfx' for c in config['countries']]
    unit_ids = infantry_types(game)
    # Native UI divides the 1080x440 sheet into three 360x440 portrait frames.
    picture = ImageOps.fit(Image.open(ROOT/'art/infantry/ashborn_infantry.png').convert('RGB'),(1080,440))
    art = dds(picture,'DXT1')
    mask = dds(Image.new('RGBA',(32,32),(0,0,0,0)),'DXT5')
    paths = []
    for culture in cultures:
        # Exact unit/culture keys outrank all native age and equipment fallbacks.
        names = [f'army_infantry_{unit}_{culture}' for unit in unit_ids]
        names += [f'army_infantry_{culture}']
        for name in names:
            for rel, content in [(REL/(name+'.dds'),art),(REL/'masks'/(name+'.dds'),mask)]:
                target=output/rel
                target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes(content)
                paths.append(rel.as_posix())
    report={'unit_types':unit_ids,'culture_tags':cultures,'files':paths,'engine_tested':False,
            'source_sha256':hashlib.sha256((ROOT/'art/infantry/ashborn_infantry.png').read_bytes()).hexdigest()}
    return report

def update_manifest(output, report):
    path=ROOT/'data/main_overlay.json'
    manifest=json.loads(path.read_text())
    manifest['files']=[item for item in manifest['files'] if not item['path'].startswith(REL.as_posix()+'/')]
    manifest['files'] += [{'path':p,'sha256':hashlib.sha256((output/p).read_bytes()).hexdigest()} for p in report['files']]
    path.write_text(json.dumps(manifest,indent=2)+'\n')

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--game',type=Path,required=True)
    parser.add_argument('--update-overlay',action='store_true')
    args=parser.parse_args()
    report=build(args.game,ROOT/'mod')
    if args.update_overlay: update_manifest(ROOT/'mod',report)
    (ROOT/'art/infantry/validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'infantry_types':len(report['unit_types']),'cultures':len(report['culture_tags']),'textures':len(report['files'])}))
