"""Patch PNG tile streams used by EU5's runtime terrain cache.

Vanilla tile indexes are mip-major, row-major in world Y-up coordinates;
individual PNG tiles are north-up. Preserve all unaffected entries byte-for-byte.
Release packages contain append-only deltas; the installer copies the user's
matching vanilla cache before appending them. No game installation is modified.
"""
from pathlib import Path
import io,json,re,shutil
import numpy as np
import archipelago
from PIL import Image

SEA_LEVEL=0.08340625*65535
CACHE='in_game/gfx/terrain2/terrain_cache'

def height_pyramid(game,cfg,source):
    """Filter one aligned native-resolution patch; do not resample each LOD's
    silhouette independently. The alignment preserves exact shared tile borders.
    """
    cx,cy=cfg['center']
    x0=int(np.floor(min(i['center'][0]-i['radius'][0]*2 for i in cfg['islands'])*4/512))*512
    x1=int(np.ceil(max(i['center'][0]+i['radius'][0]*2 for i in cfg['islands'])*4/512))*512
    y0=int(np.floor(min(i['center'][1]-i['radius'][1]*2 for i in cfg['islands'])*4/512))*512
    y1=int(np.ceil(max(i['center'][1]+i['radius'][1]*2 for i in cfg['islands'])*4/512))*512
    field=np.zeros((y1-y0,x1-x0),np.uint16)
    entries=[tuple(map(int,m)) for m in re.findall(r'offset=(-?\d+)\s+size=(-?\d+)',source(game,CACHE+'/heightmap.info').read_text())]
    with source(game,CACHE+'/heightmap.bin').open('rb') as stream:
        for py in range(y0,y1,128):
            for px in range(x0,x1,128):
                idx=(255-py//128)*512+px//128;o,n=entries[idx]
                if o<0:continue
                stream.seek(o);tile=np.array(Image.open(io.BytesIO(stream.read(n))),dtype=np.uint16)
                field[py-y0:py-y0+128,px-x0:px-x0+128]=tile[2:130,2:130]
    coverage=np.zeros(field.shape,bool)
    for top in range(0,len(field),128):
        yy,xx=np.mgrid[top:min(top+128,len(field)),:field.shape[1]]
        x=(xx+x0+.5)/4-cx;y=(yy+y0+.5)/4-cy
        mask=archipelago.surface(cfg,x,y)>-.12
        h=archipelago.heights(cfg,x,y)
        field[top:top+len(h)][mask]=h[mask];coverage[top:top+len(h)]=mask
    result=[]
    for mip in range(10):
        result.append((field,coverage,x0//(2**mip),y0//(2**mip)))
        if mip<9:
            h,w=field.shape
            # Integer accumulation avoids uint16 overflow and fixes each mip's
            # phase to the native grid instead of sampling isolated peak points.
            field=((field.astype(np.uint32).reshape(h//2,2,w//2,2).sum(axis=(1,3))+2)//4).astype(np.uint16)
            coverage=coverage.reshape(h//2,2,w//2,2).any(axis=(1,3))
    return result

def build_cache_patch(game,out,reports,cfg,footprint,source):
    root=out.parents[0];patchdir=root/'terrain_patch';patchdir.mkdir(exist_ok=True)
    pyramids=height_pyramid(game,cfg,source)
    cx,cy=cfg['center']; xmin=min(i['center'][0]-i['radius'][0]*2 for i in cfg['islands']);xmax=max(i['center'][0]+i['radius'][0]*2 for i in cfg['islands']);ymin=min(i['center'][1]-i['radius'][1]*2 for i in cfg['islands']);ymax=max(i['center'][1]+i['radius'][1]*2 for i in cfg['islands']);manifest={'version':cfg['version'],'files':[],'tile_order':'mip-major; Y-up tile rows; north-up PNG pixels','material_selection':'continuous island geology: rock, grass, woodland, soil, riverbanks','height_sampling':'area-filtered common heightfield with continuous submerged shoreline'}
    cache=out/CACHE;cache.mkdir(parents=True,exist_ok=True)
    for kind in ['heightmap','materials','index_map']:
        rel=f'{CACHE}/{kind}.bin';src=source(game,rel)
        info_rel=f'{CACHE}/{kind}.info';txt=source(game,info_rel).read_text()
        matches=list(re.finditer(r'offset=(-?\d+)\s+size=(-?\d+)',txt))
        assert len(matches)==174763
        entries=[tuple(map(int,m.groups())) for m in matches]
        target=out/rel;shutil.copyfile(src,target)
        delta_path=patchdir/f'{kind}.append';updates={};nchanged=0
        with src.open('rb') as inp,target.open('ab') as full,delta_path.open('wb') as delta:
            start=0;tw,th=512,256;mip=0
            while True:
                step=2**mip
                # Include borders; cache source covers 65536 x 32768 world units.
                tx0=max(0,int(xmin*4/(128*step))-1);tx1=min(tw-1,int(xmax*4/(128*step))+1)
                ty0=max(0,int((8192-ymax)*4/(128*step))-1);ty1=min(th-1,int((8192-ymin)*4/(128*step))+1)
                for ty in range(ty0,ty1+1):
                    for tx in range(tx0,tx1+1):
                        # Sample centers. The extra mip beyond height=1 is square padded.
                        gx=(tx*128+np.arange(132)-2+.5)*step
                        gy=((ty+1)*128-(np.arange(132)-2)-.5)*step
                        x,y=np.meshgrid(gx/4-cx,8192-gy/4-cy)
                        mask=footprint(x,y)>0
                        if kind=='heightmap':
                            field,coverage,ox,oy=pyramids[mip]
                            # Field coordinates are north-down; tile rows run Y-up.
                            ix=np.rint((x+cx)*4/step-.5).astype(int)-ox
                            iy=np.rint((y+cy)*4/step-.5).astype(int)-oy
                            valid=(ix>=0)&(iy>=0)&(ix<field.shape[1])&(iy<field.shape[0])
                            mask=np.zeros(x.shape,bool);mask[valid]=coverage[iy[valid],ix[valid]]
                        if not mask.any():continue
                        idx=start+ty*tw+tx;o,s=entries[idx]
                        if o<0:arr=np.zeros((132,132),np.uint16)
                        else:
                            inp.seek(o);arr=np.array(Image.open(io.BytesIO(inp.read(s))),dtype=np.uint16)
                        assert arr.shape==(132,132)
                        before=arr.copy()
                        if kind=='heightmap':arr[mask]=field[iy[mask],ix[mask]]
                        else:
                            import landscape
                            slots=landscape.material_indices(cfg,x,y)
                            arr[mask]=(1 << slots[mask]) if kind=='materials' else 35

                        assert np.array_equal(before[~mask],arr[~mask])
                        if kind=='heightmap':assert np.all(arr[mask]>=2234)
                        buf=io.BytesIO();Image.fromarray(arr).save(buf,format='PNG');data=buf.getvalue()
                        assert np.array_equal(np.array(Image.open(io.BytesIO(data))),arr)
                        offset=full.tell();full.write(data);delta.write(data);updates[idx]=(offset,len(data));nchanged+=1
                start+=tw*th
                if tw==1 and th==1:break
                tw=max(1,tw//2);th=max(1,th//2);mip+=1
            assert start==len(entries)
        for idx in sorted(updates,reverse=True):
            m=matches[idx];o,s=updates[idx];txt=txt[:m.start()]+f'offset={o}\n\t\tsize={s}'+txt[m.end():]
        (out/info_rel).write_text(txt,encoding='utf-8')
        # Validate all updated references from the final assembled binary.
        with target.open('rb') as f:
            for idx,(o,s) in updates.items():
                f.seek(o);tile=Image.open(io.BytesIO(f.read(s)));tile.load();assert tile.size==(132,132)
        import hashlib
        manifest['files'].append({'path':rel,'delta':delta_path.name,'source_size':src.stat().st_size,'source_sha256':hashlib.file_digest(src.open('rb'),'sha256').hexdigest(),'final_sha256':hashlib.file_digest(target.open('rb'),'sha256').hexdigest(),'final_size':target.stat().st_size,'tiles_changed':nchanged})
    (patchdir/'manifest.json').write_text(json.dumps(manifest,indent=2))
    # The shipped heightmap.png is a legacy Europe/Asia source, NOT a world
    # overview. Runtime geography is in the streamed tiles; never stamp global
    # coordinates into that unrelated image.
    return {'method':'append-only native PNG tile cache patch','tiles_changed':{Path(f['path']).stem:f['tiles_changed'] for f in manifest['files']},'unmodified_pixels_preserved':True,'coastline':'continuous sea-level crossing and submerged shelf','mips':'area-filtered from the same fine heightfield','legacy_regional_heightmap_override':False,'runtime_verified':False,'engine_bake':False}
