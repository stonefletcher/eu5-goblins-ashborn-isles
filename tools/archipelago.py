"""Scalable Ashborn Isles map and campaign setup."""
import math,re,json
from decimal import Decimal
from collections import deque
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw

LORE = ('In the early years of the fourteenth century, fire rose from the Atlantic. '
'Months of eruptions left behind black volcanic islands. When the smoke cleared, goblins already walked their shores. '
'No one saw them arrive. Some captains claim the mountains birthed them; others speak of passages beneath the earth that have since collapsed. '
'Fishing camps became villages, crude mines opened in the ridges, and rival crews fought over sheltered harbors. '
'By 1337, Hooktooth has become Cindermaw\'s capital, but the Ashborn Isles remain divided. '
'The Brinekin of Brackmaw and the Reefhook, Shatterfin and Sootwake clans share the Cinderkin\'s faith in the Hunger Below, yet bow to their own captains. '
'Poor treasuries, crowded settlements and growing fleets drive them toward expansion. '
'The High Captain dreams first of uniting the islands. Beyond them lies a world the goblins have only begun to discover.')

def prepare(cfg):
    locs=[];seq=0
    countries={c['tag']:c for c in cfg['countries']}
    rx,ry=cfg['radius'];cx,cy=cfg['center']
    for island in cfg['islands']:
        scale=math.sqrt(island['area_ratio'])
        # Normalize silhouette area, so Brackmaw remains 60% despite a different outline.
        gy,gx=np.mgrid[-2:2:600j,-2:2:600j]
        unit_area=np.mean(shape(gx,gy,1,1,island['profile'])>0)*16
        scale*=math.sqrt(math.pi/unit_area)
        island['center']=[cx+island['offset'][0]*rx,cy+island['offset'][1]*ry]
        island['radius']=[rx*scale,ry*scale]
        for l in island['locations']:
            seq+=1;l['color']=f'ed12{seq:02x}';l['country']=island['country'];l['culture']=countries[l['country']]['culture'];l['island']=island['id']
            l['point']=[island['center'][i]+l['seed'][i]*island['radius'][i] for i in range(2)]
            locs.append(l)
    cfg['locations']=locs
    return cfg

def shape(x,y,rx,ry,profile):
    phase,stretch,rotation,bay=profile
    u=x/rx;v=y/ry;c=math.cos(rotation);s=math.sin(rotation)
    u,v=(u*c+v*s)/stretch,(-u*s+v*c)*stretch
    r=np.sqrt(u*u+v*v);a=np.arctan2(v,u)
    delta=np.arctan2(np.sin(a-bay),np.cos(a-bay))
    rim=1+.20*np.sin(3*a+phase)+.105*np.cos(5*a-phase)+.055*np.sin(11*a+phase)+.025*np.cos(19*a)
    return rim-.40*np.exp(-(delta/.30)**2)-r

def surface(cfg,x,y):
    result=np.full(np.broadcast(x,y).shape,-100.,dtype=float)
    for island in cfg['islands']:
        dx=island['center'][0]-cfg['center'][0];dy=island['center'][1]-cfg['center'][1]
        result=np.maximum(result,shape(x-dx,y-dy,*island['radius'],island['profile']))
    for px,py in cfg.get('coastal_fill',[]):
        result=np.maximum(result,np.minimum(.5-np.abs(x-px),.5-np.abs(y-py)))
    return result

def warped(island,x,y):
    """Smooth bounded domain warp: organic borders without pixel noise or enclaves."""
    rx,ry=island['radius']
    u=x/rx;v=y/ry
    wx=x+rx*(.055*np.sin(5*v+1.1)+.025*np.sin(11*v+2*u)+.012*np.cos(19*v-3*u))
    wy=y+ry*(.050*np.sin(5*u-.7)+.025*np.cos(10*u+3*v)+.012*np.sin(18*u-2*v))
    return wx,wy

def join_border_fragments(local,mask):
    """Keep the largest component of each district; reassign clipped coastal tips."""
    result=local.copy();result[~mask]=-1
    for value in np.unique(local[mask]):
        remaining=set(map(tuple,np.argwhere(mask&(local==value))));parts=[]
        while remaining:
            seed=remaining.pop();part=[seed];queue=deque([seed])
            while queue:
                y,x=queue.popleft()
                for q in [(y-1,x),(y+1,x),(y,x-1),(y,x+1)]:
                    if q in remaining:remaining.remove(q);part.append(q);queue.append(q)
            parts.append(part)
        for part in sorted(parts,key=len,reverse=True)[1:]:
            yy,xx=zip(*part);result[yy,xx]=-1
    while np.any(mask&(result<0)):
        before=int(np.sum(mask&(result<0)))
        for dy,dx in [(0,1),(1,0),(0,-1),(-1,0)]:
            neighbor=np.roll(result,(dy,dx),(0,1));take=mask&(result<0)&(neighbor>=0);result[take]=neighbor[take]
        assert int(np.sum(mask&(result<0)))<before,'Detached island fragment'
    return result

def heights(cfg,x,y):
    """Continuous terrain whose dominant relief follows each location's combat tag."""
    sea=.08340625*65535;result=np.full(np.broadcast(x,y).shape,2234.,dtype=float)
    for island in cfg['islands']:
        dx=island['center'][0]-cfg['center'][0];dy=island['center'][1]-cfg['center'][1]
        rx,ry=island['radius'];lx=x-dx;ly=y-dy
        inland=shape(lx,ly,rx,ry,island['profile']);mask=inland>0
        if not mask.any():continue
        distances=[];targets=[];wx,wy=warped(island,lx,ly)
        for loc in island['locations']:
            sx,sy=loc['seed'][0]*rx,loc['seed'][1]*ry
            d=(wx-sx)**2+(wy-sy)**2;distances.append(d)
            rough=np.sin(lx/max(2,rx*.06))*np.cos(ly/max(2,ry*.07))
            if loc['topography']=='flatland':
                target=sea+220+180*np.clip(inland,0,1)+35*rough
            elif loc['topography']=='hills':
                target=sea+650+2400*np.clip(inland,0,1)+1100*np.exp(-d/(min(rx,ry)*.40)**2)+230*rough
            else:
                cone=7800*np.exp(-d/(min(rx,ry)*.32)**2)
                crater=4300*np.exp(-d/(min(rx,ry)*.095)**2)
                ridges=500*(np.sin(lx/max(2,rx*.08))**2)*np.clip(inland*3,0,1)
                target=sea+1400+2400*np.clip(inland,0,1)+cone-crater+ridges
            targets.append(target)
        ds=np.stack(distances);dmin=ds.min(axis=0)
        # Smooth narrow boundaries, preserving flatter harbors and farm districts.
        weights=np.exp(-(ds-dmin)/max(4,(min(rx,ry)*.18)**2))
        h=(weights*np.stack(targets)).sum(axis=0)/weights.sum(axis=0)
        shore=np.clip(inland/.14,0,1)
        h=sea+110+(h-sea-110)*shore
        result[mask]=h[mask]
    for px,py in cfg.get('coastal_fill',[]):
        fill=(np.abs(x-px)<.5)&(np.abs(y-py)<.5)
        result[fill]=np.maximum(result[fill],sea+120)
    return result.astype(np.uint16)

def build_map(b,game,out,reports):
    cfg=b.CFG;locs=cfg['locations'];cx,cy=cfg['center'];rx,ry=cfg['radius'];sea=cfg['coastal_sea']
    scx=cx+sea['offset'][0]*rx;scy=cy+sea['offset'][1]*ry;srx=sea['radius_factor'][0]*rx;sry=sea['radius_factor'][1]*ry
    box=(math.floor(scx-srx-8),math.floor(scy-sry-8),math.ceil(scx+srx+8),math.ceil(scy+sry+8))
    yy,xx=np.mgrid[box[1]:box[3],box[0]:box[2]]
    names=b.parse_names(game);inv={v:k for k,v in names.items()};templates=b.read(game,'in_game/map_data/location_templates.txt')
    top=dict(re.findall(r'(?m)^\s*(\w+)\s*=\s*\{[^\n]*?topography\s*=\s*(\w+)',templates))
    im=Image.open(b.source(game,'in_game/map_data/locations.png'));original=np.array(im.crop(box));patch=original.copy()
    zones=sea['zones']
    for zone in zones:assert tuple(bytes.fromhex(zone['color'])) not in inv
    basin=((xx-scx)/srx)**2+((yy-scy)/sry)**2<=1
    basin &= np.all(original==names[sea['source_water']],axis=2)
    # Three broad connected waters, with gently curved borders between them.
    split_y=yy+12*np.sin((xx-cx)/95)
    sea_labels=np.where(split_y<cy+ry*.9,0,np.where(split_y<cy+ry*1.9,1,2))
    for zi,zone in enumerate(zones):patch[basin&(sea_labels==zi)]=tuple(bytes.fromhex(zone['color']))
    island_labels=np.full(xx.shape,-1,np.int16);labels=np.full(xx.shape,-1,np.int16);land=np.zeros(xx.shape,bool);stats={};offset=0
    for ii,island in enumerate(cfg['islands']):
        ix,iy=island['center'];irx,iry=island['radius'];mask=shape(xx+.5-ix,yy+.5-iy,irx,iry,island['profile'])>0
        assert not (mask&land).any(),'Island footprints overlap'
        assert np.all(basin[mask]),f'{island["id"]} must fit inside new navigable basin and avoid vanilla sea lanes'
        island_labels[mask]=ii;land|=mask
        wx,wy=warped(island,xx+.5-ix,yy+.5-iy)
        d=np.stack([(wx-l['seed'][0]*irx)**2+(wy-l['seed'][1]*iry)**2 for l in island['locations']]);local=np.argmin(d,axis=0)
        local=join_border_fragments(local,mask)
        for j,l in enumerate(island['locations']):
            lm=mask&(local==j);comp,n=b.connectivity(lm);assert comp==1 and n>=100,l['id']
            color=tuple(bytes.fromhex(l['color']));assert color not in inv and l['id'] not in names
            patch[lm]=color;labels[lm]=offset+j;stats[l['id']]={'pixels':n,'components':comp,'population':int(Decimal(str(l['pop']))*1000),'country':l['country'],'island':island['id']}
        offset+=len(island['locations'])
    seawater=basin&~land
    if b.connectivity(seawater)[0]!=1:
        remaining=set(map(tuple,np.argwhere(seawater)));parts=[]
        while remaining:
            seed=remaining.pop();part=[seed];queue=deque([seed])
            while queue:
                y,x=queue.popleft()
                for q in [(y-1,x),(y+1,x),(y,x-1),(y,x+1)]:
                    if q in remaining:remaining.remove(q);part.append(q);queue.append(q)
            parts.append(part)
        # Rasterized concave shorelines can enclose single water pixels. Fill
        # only these tiny holes and carry the correction into all terrain mips.
        small=sorted(parts,key=len,reverse=True)[1:]
        assert all(len(p)<=4 for p in small),'Disconnected coastal sea'
        cfg['coastal_fill']=[]
        for part in small:
            for y,x in part:
                adjacent=[labels[qy,qx] for qy,qx in [(y-1,x),(y+1,x),(y,x-1),(y,x+1)] if labels[qy,qx]>=0]
                assert adjacent
                li=int(max(set(adjacent),key=adjacent.count));labels[y,x]=li;land[y,x]=True
                patch[y,x]=tuple(bytes.fromhex(locs[li]['color']));stats[locs[li]['id']]['pixels']+=1
                cfg['coastal_fill'].append((x+box[0]+.5-cx,y+box[1]+.5-cy))
        seawater=basin&~land
        assert b.connectivity(seawater)[0]==1
    sea_labels=join_border_fragments(sea_labels,seawater)
    for zi,zone in enumerate(zones):patch[seawater&(sea_labels==zi)]=tuple(bytes.fromhex(zone['color']))
    defaults=b.read(game,'in_game/map_data/default.map')
    a,z=b.block_span(defaults,'sea_zones');native_seas=set(re.findall(r'\b\w+\b',b.clean(defaults[a:z])))
    a,z=b.block_span(defaults,'impassable_mountains');blocked=set(re.findall(r'\b\w+\b',b.clean(defaults[a:z])))
    native_seas-=blocked
    sea_graph={z['id']:set() for z in zones};exits={z['id']:set() for z in zones}
    for zi,zone in enumerate(zones):
        zm=seawater&(sea_labels==zi)
        assert b.connectivity(zm)[0]==1,zone['id']+' disconnected'
        for dy,dx in ((0,1),(1,0),(0,-1),(-1,0)):
            adjacent=np.roll(zm,(dy,dx),(0,1))
            for zj,other in enumerate(zones):
                if zj!=zi and np.any(adjacent&seawater&(sea_labels==zj)):sea_graph[zone['id']].add(other['id'])
            for color in np.unique(original[adjacent&~basin],axis=0):
                name=inv[tuple(color)]
                if name in native_seas:exits[zone['id']].add(name)
    for zone in zones:
        reached={zone['id']}
        for _ in zones:reached|=set().union(*(sea_graph[n] for n in reached))
        assert len(reached)==3 and any(exits[n] for n in reached),'No navigable Atlantic route'
    defaults=b.inject(defaults,'sea_zones',' '.join(z['id'] for z in zones))
    b.write(out,'in_game/map_data/default.map',defaults)
    neighbors=set()
    for dy,dx in ((0,1),(1,0),(0,-1),(-1,0)):
        edge=seawater & ~np.roll(basin,(dy,dx),(0,1))
        for c in np.unique(np.roll(original,(dy,dx),(0,1))[edge],axis=0):
            n=inv[tuple(c)]
            if top.get(n) in b.WATER:neighbors.add(n)
    assert neighbors,'Basin cannot reach existing navigable sea'
    assert np.array_equal(patch[~basin],original[~basin]),'Existing sea lanes changed'
    im.paste(Image.fromarray(patch),box);p=out/'in_game/map_data/locations.png';p.parent.mkdir(parents=True,exist_ok=True);im.save(p)
    rivers=Image.open(b.source(game,'in_game/map_data/rivers.png'));a=np.array(rivers.crop(box));a[land]=255;rim=Image.fromarray(a,'P');rim.putpalette(rivers.getpalette());rivers.paste(rim,box);rivers.save(out/'in_game/map_data/rivers.png')
    edges=set()
    for dy,dx in [(0,1),(1,0)]:
        other=np.roll(labels,(dy,dx),(0,1));m=land&(other>=0)&(labels!=other)
        edges.update(tuple(sorted((int(a),int(c)))) for a,c in zip(labels[m],other[m]))
    for island in cfg['islands']:
        ids={i for i,l in enumerate(locs) if l['island']==island['id']};reach={min(ids)}
        while True:
            nxt=reach|{c for a,c in edges if a in reach}|{a for a,c in edges if c in reach}
            if nxt==reach:break
            reach=nxt
        assert reach==ids,'Island land movement graph disconnected'
    # Every coastal location gets a port. Separate islands connect by sea, never fake land links.
    ports=[]
    for i,l in enumerate(locs):
        m=labels==i;best=None
        for dy,dx in ((0,1),(1,0),(0,-1),(-1,0)):
            edge=m&np.roll(seawater,(dy,dx),(0,1));ys,xs=np.where(edge)
            if len(xs):
                scores=(xs+box[0]-l['point'][0])**2+(ys+box[1]-l['point'][1])**2;k=int(scores.argmin());entry=(int(scores[k]),int(xs[k]-dx+box[0]),int(ys[k]-dy+box[1]))
                if best is None or entry<best:best=entry
        if best:
            _,x,y=best;ports.append({'land':l['id'],'sea':zones[int(sea_labels[y-box[1],x-box[0]])]['id'],'x':x,'y':b.H-y,'png_y':y})
    for c in cfg['countries']:assert c['capital'] in {p['land'] for p in ports},c['capital']
    b.write(out,'in_game/map_data/ports.csv',b.read(game,'in_game/map_data/ports.csv').rstrip()+'\n'+''.join(f'{p["land"]};{p["sea"]};{p["x"]};{p["y"]};x\n' for p in ports))
    b.write(out,'in_game/map_data/named_locations/goblins_ashborn_isles.txt','\n'.join(f'{l["id"]} = {l["color"]}' for l in locs+zones)+'\n')
    capitals={c['capital'] for c in cfg['countries']};lines=[f'{z["id"]} = {{ topography = coastal_ocean climate = {cfg["climate"]} }}' for z in zones]
    for l in locs:
        harbor=' natural_harbor_suitability = 0.80' if l['id'] in capitals else ''
        lines.append(f'{l["id"]} = {{ topography = {l["topography"]} vegetation = {l["vegetation"]} climate = {cfg["climate"]} religion = cm_hunger_below culture = {l["culture"]} raw_material = {l["good"]}{harbor} }}')
    b.write(out,'in_game/map_data/location_templates.txt',templates.rstrip()+'\n'+'\n'.join(lines)+'\n')
    provinces={l['province']:[x['id'] for x in locs if x['province']==l['province']] for l in locs}
    area='cm_cindermaw_area = {\n'+'\n'.join(f'{p} = {{ {" ".join(ids)} }}' for p,ids in provinces.items())+'\n}'
    defs=b.inject(b.read(game,'in_game/map_data/definitions.txt'),cfg['region'],area)
    defs=b.inject(defs,sea['province'],' '.join(z['id'] for z in zones));b.write(out,'in_game/map_data/definitions.txt',defs)
    pixels={isl['id']:sum(stats[l['id']]['pixels'] for l in isl['locations']) for isl in cfg['islands']};ratio=pixels['brackmaw']/pixels['cindermaw'];assert abs(ratio-.6)<.01
    # Exact generated map preview.
    preview=np.zeros_like(patch);preview[:]=(20,42,59)
    for zi,color in enumerate([(34,71,88),(40,85,99),(28,60,80)]):preview[seawater&(sea_labels==zi)]=color
    for c in cfg['countries']:
        for i,l in enumerate(locs):
            if l['country']==c['tag']:preview[labels==i]=c['color']
    border=np.zeros_like(land)
    for dy,dx in [(0,1),(1,0)]:border |= land & (labels!=np.roll(labels,(dy,dx),(0,1)))
    preview[border]=(16,28,34)
    canvas=Image.new('RGB',(1400,1000),'#101c25');d=ImageDraw.Draw(canvas);d.text((35,25),'GOBLINS / THE ASHBORN ISLES '+cfg['version'],font=b.font(32),fill='#edba5d')
    d.text((35,72),f'5 goblin countries | 19 locations | one faith | {sum(int(Decimal(str(l["pop"]))*1000) for l in locs):,} people',font=b.font(20),fill='#dae1d7')
    detail=Image.fromarray(preview);detail.thumbnail((800,620));canvas.paste(detail,(40,140));sx=detail.width/preview.shape[1];sy=detail.height/preview.shape[0]
    for c in cfg['countries']:
        l=next(l for l in locs if l['id']==c['capital']);x=40+(l['point'][0]-box[0])*sx;y=140+(l['point'][1]-box[1])*sy
        d.ellipse((x-4,y-4,x+4,y+4),fill='#ffe29a');d.text((x-22,y+9),c['name'],font=b.font(16),fill='white',stroke_width=1,stroke_fill='#101c25')
    for i,c in enumerate(cfg['countries']):
        total=sum(int(Decimal(str(l['pop']))*1000) for l in locs if l['country']==c['tag']);d.text((40,790+i*30),f'{c["name"]}: {total:,} people | {c["culture_name"]} | capital: '+next(l['name'] for l in locs if l['id']==c['capital']),font=b.font(18),fill='#d4ddd9')
    canvas.save(reports/'Goblins_Map_Preview.png')
    h=heights(cfg,xx+.5-cx,yy+.5-cy)
    from locators import build_locators
    anchors=build_locators(b,game,out,labels,seawater,sea_labels,box,h,ports)
    for i,l in enumerate(locs):
        samples=h[labels==i].astype(float)-.08340625*65535
        stats[l['id']]['topography']=l['topography']
        stats[l['id']]['height_above_sea']={'min':round(float(samples.min()),1),'median':round(float(np.median(samples)),1),'max':round(float(samples.max()),1)}
    hp=np.clip((h.astype(float)-2234)/42,0,255).astype(np.uint8);Image.fromarray(hp).save(reports/'Goblins_Terrain_Preview.png')
    return {'center_png':cfg['center'],'bounds':list(box),'locations':stats,'ports':ports,'settlement_locators':anchors,'sea_zone_adjacency':{k:sorted(v) for k,v in sea_graph.items()},'sea_zone_exits':{k:sorted(v) for k,v in exits.items()},'land_pixels':int(land.sum()),'island_pixels':pixels,'sister_area_ratio':ratio,'coastal_sea_connections':sorted(neighbors),'original_sea_lanes_preserved':True,'replaced_water_locations':[sea['source_water']],'adjacencies':[[locs[a]['id'],locs[c]['id']] for a,c in sorted(edges)]}

def build_setup(b,game,out):
    cfg=b.CFG;locs=cfg['locations'];countries=cfg['countries'];entries=[];popentries=[];cities=[];markets=[];total=Decimal(0);slaves=Decimal(0)
    vanilla=b.read(game,'main_menu/setup/start/10_countries.txt');outer,_=b.block_span(vanilla,'countries')
    for c in countries:
        assert not re.search(r'(?m)^\s*'+c['tag']+r'\s*=\s*\{',vanilla),c['tag']+' collision'
        ids=' '.join(l['id'] for l in locs if l['country']==c['tag'])
        entries.append(f'''{c['tag']} = {{
 own_control_core = {{ {ids} }}
 include = "{cfg['discovery_template']}"
 include = "cm_captains"
 discovered_areas = {{ cm_cindermaw_area }}
 discovered_regions = {{ {cfg['region']} }}
 capital = {c['capital']}
 country_rank = rank_duchy
 starting_technology_level = 3
 government = {{ type = republic heir_selection = cm_captain_elective ruler = random }}
 currency_data = {{ gold = {c['gold']} stability = 20 government_power = 50 prestige = 0 }}
}}''')
        cities.append(f'{c["capital"]} = {{ rank = {c["rank"]} town_setup = cm_scrap_port }}')
        # One archipelago market supports small clans without five isolated tiny markets.
    for l in locs:
        n=Decimal(str(l['pop']));captive=Decimal('3') if l['id']=='cm_hooktooth' else (Decimal('1.5') if l['id'] in ['cm_copperfang','cm_cinder_crown'] else Decimal(0))
        burghers=Decimal('6') if l['id']=='cm_hooktooth' else (Decimal('2') if l['id'] in {c['capital'] for c in countries} else Decimal('.1'))
        parts=[('nobles',Decimal('.1')),('clergy',Decimal('.2')),('burghers',burghers),('peasants',n-captive-burghers-Decimal('.3'))]
        if captive:parts.append(('slaves',captive))
        rows=[f' define_pop = {{ type = {typ} size = {v:.3f} culture = {l["culture"]} religion = cm_hunger_below }}' for typ,v in parts]
        popentries.append(l['id']+' = {\n'+'\n'.join(rows)+'\n}');total+=n;slaves+=captive
    b.write(out,'main_menu/setup/start/10_countries.txt',b.inject(vanilla,'countries','\n'.join(entries),outer+1))
    for file,addition in [('06_pops.txt','\n'.join(popentries)),('07_cities_and_buildings.txt','\n'.join(cities))]:
        rel='main_menu/setup/start/'+file;b.write(out,rel,b.inject(b.read(game,rel),'locations',addition))
    rel='main_menu/setup/start/03_markets.txt';b.write(out,rel,b.inject(b.read(game,rel),'market_manager','add_market = cm_hooktooth'))
    elections=b.read(game,'in_game/common/heir_selections/republic.txt');a,z=b.block_span(elections,'pirate_elective')
    b.write(out,'in_game/common/heir_selections/goblins_ashborn_isles.txt','cm_captain_elective = '+elections[a:z+1].replace('government_reform:pirate_brethren_reform','government_reform:cm_captains_confederation')+'\n')
    rel='in_game/common/government_types/00_default.txt'
    b.write(out,rel,b.inject(b.read(game,rel),'republic','heir_selection = cm_captain_elective'))
    b.write(out,'in_game/setup/countries/goblins_ashborn_isles.txt','\n'.join(f'{c["tag"]} = {{ color = rgb {{ {" ".join(map(str,c["color"]))} }} color2 = rgb {{ 36 31 29 }} culture_definition = {c["culture"]} religion_definition = cm_hunger_below is_historic = no }}' for c in countries)+'\n')
    b.write(out,'in_game/common/cultures/goblins_ashborn_isles.txt','\n'.join(f'{c["culture"]} = {{ language = cm_cinder_tongue color = rgb {{ {" ".join(map(str,c["color"]))} }} tags = {{ european_gfx }} culture_groups = {{ cm_goblin_group }} opinions = {{ }} }}' for c in countries)+'\n')
    flag=(b.ROOT/'mod/main_menu/common/coat_of_arms/coat_of_arms/goblins_ashborn_isles.txt').read_text()
    b.write(out,'main_menu/common/coat_of_arms/coat_of_arms/goblins_ashborn_isles.txt','\n'.join(flag.replace('CDM =',c['tag']+' =').replace('color2 = red', 'color2 = '+['red','blue','yellow','purple','orange'][i]) for i,c in enumerate(countries)))
    return {'total_population':int(total*1000),'enslaved_population':int(slaves*1000),'starting_gold':20,'vanilla_population_entries_unchanged':True,'country_populations':{c['tag']:sum(int(Decimal(str(l['pop']))*1000) for l in locs if l['country']==c['tag']) for c in countries}}

def add_localization(b,out):
    rel='main_menu/localization/english/goblins_ashborn_isles_l_english.yml';p=out/rel;s=p.read_text(encoding='utf-8-sig');extra={}
    for c in b.CFG['countries']:
        if c['tag']!='CDM':extra.update({c['tag']:c['name'],c['tag']+'_ADJ':c['adjective'],c['culture']:c['culture_name']})
    extra.update({'cm_goblin_group':'Goblinkin','cm_goblin_group_desc':'The peoples who emerged with the Ashborn Isles in the early fourteenth century.','cm_captain_elective_desc':'Ship captains choose a High Captain to lead their confederation.','cm_ashen_faiths_ADJ':'Ashen','cm_ashen_faiths_desc':'The island faiths of the Goblinkin, united in reverence for the power beneath the volcanoes.'})
    extra.update({z['id']:z['name'] for z in b.CFG['coastal_sea']['zones']})
    # Replace existing keys rather than emit duplicate localization.
    extra.update({'cindermaw.1.desc':LORE,'cm_demo_building_tip':'Hooktooth is a city with a marketplace, naval-supplies guild and stockade. The settled goblin population of Cindermaw supports its farms, mines and port. The neighboring goblin captains rule independent countries.','cm_cindermaw_area':'The Ashborn Isles'})
    for l in b.CFG['locations']:extra.setdefault(l['province'],l['province'].replace('cm_','').replace('_province','').replace('_',' ').title())
    for k,v in extra.items():
        line=' '+k+': "'+v.replace('"','\\"')+'"'
        pattern=r'(?m)^ '+re.escape(k)+r':.*$'
        if re.search(pattern,s):s=re.sub(pattern,lambda m:line,s)
        else:s+=line+'\n'
    b.write(out,rel,s)
    (b.ROOT/'LORE.md').write_text('# Cindermaw - The Ashborn Isles\n\n'+LORE+'\n',encoding='utf-8')

