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

def build_cache_patch(game,out,reports,cfg,footprint,source):
    root=out.parents[0];patchdir=root/'terrain_patch';patchdir.mkdir(exist_ok=True)
    cx,cy=cfg['center']; xmin=min(i['center'][0]-i['radius'][0]*2 for i in cfg['islands']);xmax=max(i['center'][0]+i['radius'][0]*2 for i in cfg['islands']);ymin=min(i['center'][1]-i['radius'][1]*2 for i in cfg['islands']);ymax=max(i['center'][1]+i['radius'][1]*2 for i in cfg['islands']);manifest={'version':cfg['version'],'files':[],'tile_order':'mip-major; Y-up tile rows; north-up PNG pixels','material_selection':'native oceanic biome slot 8; limited lowland vegetation'}
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
                        if not mask.any():continue
                        idx=start+ty*tw+tx;o,s=entries[idx]
                        if o<0:arr=np.zeros((132,132),np.uint16)
                        else:
                            inp.seek(o);arr=np.array(Image.open(io.BytesIO(inp.read(s))),dtype=np.uint16)
                        assert arr.shape==(132,132)
                        before=arr.copy()
                        if kind=='heightmap':arr[mask]=archipelago.heights(cfg,x,y)[mask]
                        else:
                            # Material bit 8 is rock on mountain/sparse biomes and dirt
                            # on lower oceanic biomes (verified in native materials.txt).
                            # Small sheltered lowlands retain the prior vegetation mask.
                            low=mask & (archipelago.heights(cfg,x,y)<6100)
                            arr[mask]=256 if kind=='materials' else 35
                            arr[low]=9216 if kind=='materials' else 63
                        assert np.array_equal(before[~mask],arr[~mask])
                        if kind=='heightmap':assert np.all(arr[mask]>SEA_LEVEL)
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
    # The overview is a separate engine input, not automatically rebuilt from tiles.
    rel='in_game/gfx/terrain2/heightmap.png'
    overview=Image.open(source(game,rel));sx=16384/overview.width;sy=8192/overview.height
    box=(max(0,int(xmin/sx)),max(0,int(ymin/sy)),min(overview.width,int(xmax/sx)+1),min(overview.height,int(ymax/sy)+1))
    yy,xx=np.mgrid[box[1]:box[3],box[0]:box[2]];x=(xx+.5)*sx-cx;y=(yy+.5)*sy-cy
    arr=np.array(overview.crop(box),dtype=np.uint16);mask=footprint(x,y)>0
    arr[mask]=archipelago.heights(cfg,x,y)[mask]
    overview.paste(Image.fromarray(arr),box);overview.save(out/rel)
    return {'method':'append-only native PNG tile cache patch','tiles_changed':{Path(f['path']).stem:f['tiles_changed'] for f in manifest['files']},'unmodified_pixels_preserved':True,'runtime_verified':False,'engine_bake':False}
