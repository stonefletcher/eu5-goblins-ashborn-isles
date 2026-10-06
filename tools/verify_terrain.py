"""Check final streamed height tiles against their actual neighboring PNGs."""
from pathlib import Path
import io,re,json
import numpy as np
from PIL import Image

def verify(game,out,reports,cfg=None):
    rel='in_game/gfx/terrain2/terrain_cache/heightmap'
    def entries(path):return [tuple(map(int,m)) for m in re.findall(r'offset=(-?\d+)\s+size=(-?\d+)',path.read_text())]
    a=entries(out/(rel+'.info'));old=entries(game/(rel+'.info'));changes=[i for i in range(len(a)) if a[i]!=old[i]]
    levels=[];start=0;w,h=512,256
    while True:
     levels.append((start,w,h));start+=w*h
     if w==h==1:break
     w=max(1,w//2);h=max(1,h//2)
    compared=0;max_seam=0;counts={}
    with (out/(rel+'.bin')).open('rb') as stream:
     cache={}
     def tile(i):
      if i not in cache:
       o,n=a[i]
       if o<0:cache[i]=np.zeros((132,132),np.uint16)
       else:stream.seek(o);cache[i]=np.array(Image.open(io.BytesIO(stream.read(n))),np.uint16)
      return cache[i]
     for level,(start,w,h) in enumerate(levels):
      ids=[i for i in changes if start<=i<start+w*h];counts[level]=len(ids)
      for i in ids:
       y,x=divmod(i-start,w);t=tile(i).astype(int)
       for side,j in [('right',i+1 if x<w-1 else None),('up',i+w if y<h-1 else None)]:
        if j is None:continue
        v=tile(j).astype(int)
        diff=np.abs(t[:,128:]-v[:,:4]) if side=='right' else np.abs(t[:4]-v[128:])
        seam=int(diff.max());max_seam=max(max_seam,seam);assert seam==0,(level,x,y,side,seam);compared+=1
      cache.clear()
    assert counts[0]>0 and counts[8]>0 and counts[9]>0,counts
    assert not (out/'in_game/gfx/terrain2/heightmap.png').exists()
    result={'updated_height_tiles':len(changes),'tiles_per_mip':counts,'shared_borders_checked':compared,'max_shared_border_error':max_seam,'legacy_heightmap_override':False,'engine_visual_verified':False}
    if cfg is not None:
        result['relief_world_units']=verify_relief(out,reports,cfg,a)
    (reports/'terrain_verification.json').write_text(json.dumps(result,indent=2));return result


def verify_relief(out,reports,cfg,entries):
    """Measure the assembled cache at gameplay-map resolution, not its recipe.

    Mip 2 is 16384x8192, exactly the location map resolution. Decode the
    final binary independently and compare its terrain with location colors.
    The earlier seam-only test could pass perfectly flat terrain.
    """
    from PIL import ImageDraw, ImageFont
    box=(int(min(i['center'][0]-i['radius'][0]*1.7 for i in cfg['islands'])),
         int(min(i['center'][1]-i['radius'][1]*1.7 for i in cfg['islands'])),
         int(max(i['center'][0]+i['radius'][0]*1.7 for i in cfg['islands']))+1,
         int(max(i['center'][1]+i['radius'][1]*1.7 for i in cfg['islands']))+1)
    x0,y0,x1,y1=box
    heights=np.zeros((y1-y0,x1-x0),np.uint16)
    start=512*256+256*128
    with (out/'in_game/gfx/terrain2/terrain_cache/heightmap.bin').open('rb') as f:
        for py in range(y0//128*128,y1,128):
            for px in range(x0//128*128,x1,128):
                offset,length=entries[start+(63-py//128)*128+px//128]
                if offset<0: continue
                f.seek(offset)
                tile=np.array(Image.open(io.BytesIO(f.read(length))),np.uint16)[2:130,2:130]
                left,top=max(px,x0),max(py,y0);right,bottom=min(px+128,x1),min(py+128,y1)
                heights[top-y0:bottom-y0,left-x0:right-x0]=tile[top-py:bottom-py,left-px:right-px]
    with Image.open(out/'in_game/map_data/locations.png') as locations:
        pixels=np.array(locations.crop(box))
    sea=.08340625*65535
    world=(heights.astype(float)-sea)*32/65535
    metrics={};land=np.zeros(world.shape,bool)
    for loc in cfg['locations']:
        mask=np.all(pixels==tuple(bytes.fromhex(loc['color'])),axis=2)
        assert mask.any(),loc['id']
        land|=mask;values=world[mask]
        metrics[loc['id']]={'terrain':loc['topography'],'max':round(float(values.max()),3),
                          'median':round(float(np.median(values)),3),
                          'above_water_fraction':round(float(np.mean(values>0)),4)}
        assert np.mean(values>0)>.97,(loc['id'],'heightfield does not cover land',metrics[loc['id']])
    for island in cfg['islands']:
        island_mask=np.zeros(land.shape,bool)
        for loc in island['locations']:
            island_mask |= np.all(pixels==tuple(bytes.fromhex(loc['color'])),axis=2)
        values=world[island_mask]
        minimum=4 if island['id']=='reefhook' else (12 if island['id']=='cindermaw' else 7)
        assert values.max()>=minimum,(island['id'],'missing island mountain spine',float(values.max()))
        assert np.mean(values<1.5)>.06,(island['id'],'no coastal lowlands')
    # Native heightfield values are shown in true world units. This is an
    # offline diagnostic, not a claim that the engine rendered this result.
    gy,gx=np.gradient(world)
    shade=np.clip((.8-.8*gx-.6*gy)/np.sqrt(1+gx*gx+gy*gy),.25,1.0)
    low=np.array([111,118,79]);high=np.array([172,161,144])
    blend=np.clip(world/18,0,1)[...,None]
    colors=(low*(1-blend)+high*blend)*shade[...,None]
    rgb=np.clip(colors,0,255).astype(np.uint8);rgb[~land]=[20,40,56]
    preview=Image.fromarray(rgb).resize((1080,round(rgb.shape[0]*1080/rgb.shape[1])),Image.Resampling.LANCZOS)
    canvas=Image.new('RGB',(1120,preview.height+100),'#101c25');canvas.paste(preview,(20,80))
    draw=ImageDraw.Draw(canvas)
    font_path=Path('C:/Windows/Fonts/segoeui.ttf')
    heading=ImageFont.truetype(str(font_path),25) if font_path.exists() else ImageFont.load_default()
    small=ImageFont.truetype(str(font_path),16) if font_path.exists() else ImageFont.load_default()
    draw.text((20,12),'ASHBORN ISLES '+cfg['version']+' / DECODED TERRAIN CACHE',font=heading,fill='#edba5d')
    draw.text((20,47),'Offline heightfield preview; native vertical scale. In-game appearance still requires verification.',font=small,fill='#d4ddd9')
    canvas.save(reports/'Goblins_Cache_Relief.png')
    return metrics


def verify_center_continuity(cfg):
    """Reject the angular shoreline function being reused as interior height.

    Probe a tiny ring around each island's origin: the old formula jumped
    hundreds of uint16 units even as radius approached zero. Two units
    allow 16-bit quantization without accepting a directional discontinuity.
    """
    import archipelago
    angles=np.linspace(0,2*np.pi,32,endpoint=False)
    jumps={}
    for island in cfg['islands']:
        x=island['center'][0]-cfg['center'][0]+.0001*np.cos(angles)
        y=island['center'][1]-cfg['center'][1]+.0001*np.sin(angles)
        values=archipelago.heights(cfg,x,y).astype(int)
        jumps[island['id']]=int(np.ptp(values))
        assert jumps[island['id']]<=2,(island['id'],'radial height singularity',jumps[island['id']])
    return jumps
