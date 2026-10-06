"""Check final streamed height tiles against their actual neighboring PNGs."""
from pathlib import Path
import io,re,json
import numpy as np
from PIL import Image

def verify(game,out,reports):
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
    (reports/'terrain_verification.json').write_text(json.dumps(result,indent=2));return result
