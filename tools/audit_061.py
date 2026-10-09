"""Inspect province connectivity against the actual installed location raster."""
import json
from pathlib import Path
import numpy as np
from PIL import Image
import build as b

def graph(path):
    Image.MAX_IMAGE_PIXELS = None
    im = Image.open(path).convert('RGB')
    points = [l['point'] for l in b.CFG['locations']]
    box = (int(min(p[0] for p in points))-300, int(min(p[1] for p in points))-300,
           int(max(p[0] for p in points))+300, int(max(p[1] for p in points))+300)
    pixels = np.array(im.crop(box))
    labels = np.full(pixels.shape[:2], -1, dtype=np.int16)
    locs = b.CFG['locations']
    for i,l in enumerate(locs):
        labels[np.all(pixels == tuple(bytes.fromhex(l['color'])), axis=2)] = i
    edges = {l['id']: set() for l in locs}
    for a,c in [(labels[:-1],labels[1:]),(labels[:,:-1],labels[:,1:])]:
        valid = (a>=0)&(c>=0)&(a!=c)
        for x,y in np.unique(np.stack((a[valid],c[valid]),axis=1),axis=0):
            edges[locs[x]['id']].add(locs[y]['id'])
            edges[locs[y]['id']].add(locs[x]['id'])
    return edges

def components(ids,edges):
    remaining=set(ids); result=[]
    while remaining:
        reached={remaining.pop()}; todo=list(reached)
        while todo:
            for n in edges[todo.pop()] & remaining:
                remaining.remove(n); reached.add(n); todo.append(n)
        result.append(sorted(reached))
    return sorted(result,key=len,reverse=True)

if __name__=='__main__':
    import sys
    edges=graph(Path(sys.argv[1]))
    for province in sorted({l['province'] for l in b.CFG['locations']}):
        ids=[l['id'] for l in b.CFG['locations'] if l['province']==province]
        assert len(components(ids,edges))==1,(province,components(ids,edges))
    for island in b.CFG['islands']:
        print('\nISLAND',island['id'])
        for province in dict.fromkeys(l['province'] for l in island['locations']):
            ids=[l['id'] for l in island['locations'] if l['province']==province]
            print(province,components(ids,edges))
        for l in island['locations']:
            print(l['id'],l['good'],l['pop_classes']['laborers'],l['pop_classes']['burghers'],l['buildings'],'neighbors',sorted(edges[l['id']]))
    (b.ROOT/'build').mkdir(exist_ok=True)
    (b.ROOT/'build/adjacency-061.json').write_text(json.dumps({k:sorted(v) for k,v in edges.items()},indent=2))
