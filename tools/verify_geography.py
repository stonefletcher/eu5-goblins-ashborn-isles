"""Raster checks for channel clearance and playable district geometry."""
import json
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
import archipelago


def verify_geography(cfg,preview=None):
    import build
    yy,xx=np.mgrid[2310:2930,6580:7190]
    masks={};borders={};minimum={}
    canvas=np.zeros((*xx.shape,3),np.uint8);canvas[:]=[22,43,58]
    colors=[(153,116,82),(124,137,105),(168,147,90),(150,144,143),(124,133,148),(127,103,95)]
    for ii,island in enumerate(cfg['islands']):
        cx,cy=island['center'];rx,ry=island['radius']
        mask=archipelago.shape(xx+.5-cx,yy+.5-cy,rx,ry,island['profile'])>0
        assert build.connectivity(mask)[0]==1,(island['id'],'disconnected coastline')
        assert not any(np.any(mask&m) for m in masks.values()),'Overlapping islands'
        masks[island['id']]=mask
        edge=mask & (~np.roll(mask,1,0)|~np.roll(mask,-1,0)|~np.roll(mask,1,1)|~np.roll(mask,-1,1))
        borders[island['id']]=np.argwhere(edge)
        wx,wy=archipelago.warped(island,xx+.5-cx,yy+.5-cy)
        district=np.argmin(np.stack([(wx-l['seed'][0]*rx)**2+(wy-l['seed'][1]*ry)**2 for l in island['locations']]),axis=0)
        district=archipelago.join_border_fragments(district,mask)
        sizes=[]
        for j,loc in enumerate(island['locations']):
            tile=mask&(district==j);components,pixels=build.connectivity(tile)
            assert components==1 and pixels>=100,(loc['id'],components,pixels)
            sizes.append(pixels)
            canvas[tile]=np.clip(np.array(colors[ii])+((j%3)-1)*13,0,255)
        internal=mask & ((district!=np.roll(district,1,0))|(district!=np.roll(district,1,1)))
        canvas[internal]=[63,61,56];canvas[edge]=[204,189,157]
        minimum[island['id']]=min(sizes)
    gaps={}
    names=list(borders)
    for n,a in enumerate(names):
        for b in names[n+1:]:
            pa,pb=borders[a],borders[b]
            distance=min(float(np.sqrt(((chunk[:,None,:]-pb[None,:,:])**2).sum(axis=2)).min()) for chunk in np.array_split(pa,8))
            gaps[a+'/'+b]=round(distance,2)
    for pair in ['cindermaw/brackmaw','brackmaw/sootwake']:
        assert gaps[pair]>=24,(pair,'channel narrower than 24 map pixels',gaps[pair])
    assert min(gaps.values())>=10,('narrow island gap',gaps)
    if preview:
        im=Image.fromarray(canvas).resize((915,930));d=ImageDraw.Draw(im)
        for i in cfg['islands']:
            x,y=i['center'];d.text(((x-6580)*1.5,(y-2310)*1.5),i['name'],fill='white',stroke_width=2,stroke_fill='black')
        preview.parent.mkdir(parents=True,exist_ok=True);im.save(preview)
    return {'shoreline_distance_pixels':gaps,'minimum_tile_pixels':minimum}

if __name__=='__main__':
    root=Path(__file__).resolve().parents[1]
    cfg=archipelago.prepare(json.loads((root/'data/island.json').read_text()))
    result=verify_geography(cfg,root/'build/reports/Terrain_Layout.png')
    print(json.dumps(result,indent=2))
