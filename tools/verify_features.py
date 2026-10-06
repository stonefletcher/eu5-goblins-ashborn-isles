"""Integration checks for geography, scenery, reciprocal contact and startup economy."""
import copy, json, re
import numpy as np
from PIL import Image
import archipelago, landscape


def verify(b,out,mapstats):
    cfg=b.CFG
    baseline=json.loads((b.ROOT/'data/island.json').read_text())
    baseline['land_area_multiplier']=1
    for island in baseline['islands']:island['position_adjustment']=[0,0]
    # 0.4.1 had equal total land for all three minor clans.
    next(i for i in baseline['islands'] if i['id']=='reefhook')['area_ratio']=.105
    archipelago.prepare(baseline);ratios={}
    for old in baseline['islands']:
        cx,cy=old['center'];rx,ry=old['radius']
        yy,xx=np.mgrid[int(cy-ry*1.7):int(cy+ry*1.7)+1,int(cx-rx*1.7):int(cx+rx*1.7)+1]
        old_area=int((archipelago.shape(xx+.5-cx,yy+.5-cy,rx,ry,old['profile'])>0).sum())
        ratio=mapstats['island_pixels'][old['id']]/old_area
        target=1.5 if old['id']=='reefhook' else 1.25
        # Rasterized coastlines, especially tiny islands, round at pixel edges.
        # Require the requested area within one percent of its target.
        assert abs(ratio-target)<target*.01,(old['id'],'wrong area expansion',ratio)
        ratios[old['id']]=round(ratio,4)
    assert len(cfg['islands'][0]['locations'])==12 and len(cfg['islands'][1]['locations'])==8
    assert len({l['province'] for l in cfg['islands'][0]['locations']})==6
    assert len({l['province'] for l in cfg['islands'][1]['locations']})==4
    # Province seed/tag changes must leave the visual terrain unchanged.
    altered=copy.deepcopy(cfg);altered.pop('_landscape',None)
    for isl in altered['islands']:
        for loc in isl['locations']:loc['seed']=[100,100];loc['topography']='flatland';loc['vegetation']='desert'
    x,y=np.meshgrid(np.linspace(-280,230,75),np.linspace(-125,350,80))
    assert np.array_equal(landscape.heights(cfg,x,y),landscape.heights(altered,x,y))
    assert np.array_equal(landscape.material_indices(cfg,x,y),landscape.material_indices(altered,x,y))
    rivers=Image.open(out/'in_game/map_data/rivers.png');river_count=0
    for data in landscape.prepare(cfg):
        for path in data['rivers']:
            points=[(x+data['x0'],y+data['y0']) for y,x in path]
            assert rivers.getpixel(points[0])==0
            assert all(rivers.getpixel(p) in (3,4) for p in points[1:])
            assert all(abs(a[0]-c[0])+abs(a[1]-c[1])==1 for a,c in zip(points,points[1:]))
            assert len(points)>=9
            river_count+=1
    scenery_count=0
    for path in (out/'in_game/gfx/map/map_objects').glob('cm_ashborn_*.bin'):
        a=np.fromfile(path,dtype='<f4').reshape(-1,10)
        assert np.isfinite(a).all() and np.all(a[:,7:]>0)
        assert np.allclose(np.linalg.norm(a[:,3:7],axis=1),1,atol=1e-6)
        x=a[:,0]-cfg['center'][0];y=8192-a[:,2]-cfg['center'][1]
        assert np.all(archipelago.surface(cfg,x,y)>0),'Scenery placed outside land'
        scenery_count+=len(a)
    from exploration import ROUTES
    events=(out/'in_game/events/goblins_exploration.txt').read_text(encoding='utf-8-sig')
    for route in ROUTES.values():
        a,z=b.block_span(events,f'goblins_exploration.{route["event"]}')
        section=events[a:z]
        for location in route['locations']:
            la,lz=b.block_span(section,'location:'+location);contact=section[la:lz]
            assert 'exists = owner' in contact and 'owner = {' in contact
            assert 'discover_area = area:cm_cindermaw_area' in contact
            assert 'discover_area = area:cm_ashborn_seas_area' in contact
    economy=(out/'in_game/common/on_action/goblins_economy.txt').read_text(encoding='utf-8-sig')
    assert 'NOT = { has_variable = ga_economy_initialized }' in economy
    assert economy.count('change_max_raw_material_workers =')==len(cfg['locations'])
    assert sum(round(l['pop']*1000) for l in cfg['locations'])==593647
    return {'area_ratios_vs_0_4_1':ratios,'administrative_terrain_independence':True,
            'rivers':river_count,'validated_scenery_transforms':scenery_count,
            'reciprocal_routes_checked':list(ROUTES),'rgo_initialization_guard':True,
            'engine_tested':False}
