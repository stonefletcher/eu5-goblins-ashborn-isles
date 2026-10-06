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
        island['center']=[cx+island['offset'][0]*rx,cy+island['offset'][1]*ry]
        island['radius']=[rx*scale,ry*scale]
        for l in island['locations']:
            seq+=1;l['color']=f'ed12{seq:02x}';l['country']=island['country'];l['culture']=countries[l['country']]['culture'];l['island']=island['id']
            l['point']=[island['center'][i]+l['seed'][i]*island['radius'][i] for i in range(2)]
            locs.append(l)
    cfg['locations']=locs
    return cfg

def shape(x,y,rx,ry):
    r=np.sqrt((x/rx)**2+(y/ry)**2);a=np.arctan2(y/ry,x/rx)
    return 1+.065*np.sin(5*a)+.035*np.cos(9*a)-.06*np.sin(2*a)-.18*np.exp(-((a-.12)/.24)**2)-r

def surface(cfg,x,y):
    result=np.full(np.broadcast(x,y).shape,-100.,dtype=float)
    for island in cfg['islands']:
        dx=island['center'][0]-cfg['center'][0];dy=island['center'][1]-cfg['center'][1]
        result=np.maximum(result,shape(x-dx,y-dy,*island['radius']))
    return result

def warped(island,x,y):
    """Smooth bounded domain warp: organic borders without pixel noise or enclaves."""
    rx,ry=island['radius']
    u=x/rx;v=y/ry
    wx=x+rx*(.055*np.sin(5*v+1.1)+.025*np.sin(11*v+2*u)+.012*np.cos(19*v-3*u))
    wy=y+ry*(.050*np.sin(5*u-.7)+.025*np.cos(10*u+3*v)+.012*np.sin(18*u-2*v))
    return wx,wy

def heights(cfg,x,y):
    """Continuous terrain whose dominant relief follows each location's combat tag."""
    sea=.08340625*65535;result=np.full(np.broadcast(x,y).shape,2234.,dtype=float)
    for island in cfg['islands']:
        dx=island['center'][0]-cfg['center'][0];dy=island['center'][1]-cfg['center'][1]
        rx,ry=island['radius'];lx=x-dx;ly=y-dy
        inland=shape(lx,ly,rx,ry);mask=inland>0
        if not mask.any():continue
        distances=[];targets=[];wx,wy=warped(island,lx,ly)
        for loc in island['locations']:
            sx,sy=loc['seed'][0]*rx,loc['seed'][1]*ry
            d=(wx-sx)**2+(wy-sy)**2;distances.append(d)
            rough=np.sin(lx/max(2,rx*.06))*np.cos(ly/max(2,ry*.07))
            if loc['topography']=='flatland':
                target=sea+220+180*np.clip(inland,0,1)+35*rough
            elif loc['topography']=='hills':
                target=sea+450+1300*np.clip(inland,0,1)+650*np.exp(-d/(min(rx,ry)*.40)**2)+170*rough
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
    return result.astype(np.uint16)

def build_map(b,game,out,reports):
    cfg=b.CFG;locs=cfg['locations'];cx,cy=cfg['center'];rx,ry=cfg['radius'];sea=cfg['coastal_sea']
    scx=cx+sea['offset'][0]*rx;scy=cy+sea['offset'][1]*ry;srx=sea['radius_factor'][0]*rx;sry=sea['radius_factor'][1]*ry
    box=(math.floor(scx-srx-8),math.floor(scy-sry-8),math.ceil(scx+srx+8),math.ceil(scy+sry+8))
    yy,xx=np.mgrid[box[1]:box[3],box[0]:box[2]]
    names=b.parse_names(game);inv={v:k for k,v in names.items()};templates=b.read(game,'in_game/map_data/location_templates.txt')
    top=dict(re.findall(r'(?m)^\s*(\w+)\s*=\s*\{[^\n]*?topography\s*=\s*(\w+)',templates))
    im=Image.open(b.source(game,'in_game/map_data/locations.png'));original=np.array(im.crop(box));patch=original.copy()
    sea_color=tuple(bytes.fromhex(sea['color']));assert sea_color not in inv
    basin=((xx-scx)/srx)**2+((yy-scy)/sry)**2<=1
    basin &= np.all(original==names[sea['source_water']],axis=2)
    patch[basin]=sea_color
    island_labels=np.full(xx.shape,-1,np.int16);labels=np.full(xx.shape,-1,np.int16);land=np.zeros(xx.shape,bool);stats={};offset=0
    for ii,island in enumerate(cfg['islands']):
        ix,iy=island['center'];irx,iry=island['radius'];mask=shape(xx+.5-ix,yy+.5-iy,irx,iry)>0
        assert not (mask&land).any(),'Island footprints overlap'
        assert np.all(basin[mask]),f'{island["id"]} must fit inside new navigable basin and avoid vanilla sea lanes'
        island_labels[mask]=ii;land|=mask
        wx,wy=warped(island,xx+.5-ix,yy+.5-iy)
        d=np.stack([(wx-l['seed'][0]*irx)**2+(wy-l['seed'][1]*iry)**2 for l in island['locations']]);local=np.argmin(d,axis=0)
        for j,l in enumerate(island['locations']):
            lm=mask&(local==j);comp,n=b.connectivity(lm);assert comp==1 and n>=100,l['id']
            color=tuple(bytes.fromhex(l['color']));assert color not in inv and l['id'] not in names
            patch[lm]=color;labels[lm]=offset+j;stats[l['id']]={'pixels':n,'components':comp,'population':int(Decimal(str(l['pop']))*1000),'country':l['country'],'island':island['id']}
        offset+=len(island['locations'])
    seawater=basin&~land;assert b.connectivity(seawater)[0]==1,'Disconnected coastal sea'
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
            _,x,y=best;ports.append({'land':l['id'],'sea':sea['id'],'x':x,'y':b.H-y,'png_y':y})
    for c in cfg['countries']:assert c['capital'] in {p['land'] for p in ports},c['capital']
    b.write(out,'in_game/map_data/ports.csv',b.read(game,'in_game/map_data/ports.csv').rstrip()+'\n'+''.join(f'{p["land"]};{p["sea"]};{p["x"]};{p["y"]};x\n' for p in ports))
    b.write(out,'in_game/map_data/named_locations/cindermaw.txt','\n'.join(f'{l["id"]} = {l["color"]}' for l in locs)+f'\n{sea["id"]} = {sea["color"]}\n')
    capitals={c['capital'] for c in cfg['countries']};lines=[f'{sea["id"]} = {{ topography = coastal_ocean climate = {cfg["climate"]} }}']
    for l in locs:
        harbor=' natural_harbor_suitability = 0.80' if l['id'] in capitals else ''
        lines.append(f'{l["id"]} = {{ topography = {l["topography"]} vegetation = {l["vegetation"]} climate = {cfg["climate"]} religion = cm_hunger_below culture = {l["culture"]} raw_material = {l["good"]}{harbor} }}')
    b.write(out,'in_game/map_data/location_templates.txt',templates.rstrip()+'\n'+'\n'.join(lines)+'\n')
    provinces={l['province']:[x['id'] for x in locs if x['province']==l['province']] for l in locs}
    area='cm_cindermaw_area = {\n'+'\n'.join(f'{p} = {{ {" ".join(ids)} }}' for p,ids in provinces.items())+'\n}'
    defs=b.inject(b.read(game,'in_game/map_data/definitions.txt'),cfg['region'],area)
    defs=b.inject(defs,sea['province'],sea['id']);b.write(out,'in_game/map_data/definitions.txt',defs)
    pixels={isl['id']:sum(stats[l['id']]['pixels'] for l in isl['locations']) for isl in cfg['islands']};ratio=pixels['brackmaw']/pixels['cindermaw'];assert abs(ratio-.6)<.01
    # Exact generated map preview.
    preview=np.zeros_like(patch);preview[:]=(20,42,59);preview[seawater]=(34,71,88)
    for c in cfg['countries']:
        for i,l in enumerate(locs):
            if l['country']==c['tag']:preview[labels==i]=c['color']
    border=np.zeros_like(land)
    for dy,dx in [(0,1),(1,0)]:border |= land & (labels!=np.roll(labels,(dy,dx),(0,1)))
    preview[border]=(16,28,34)
    canvas=Image.new('RGB',(1400,1000),'#101c25');d=ImageDraw.Draw(canvas);d.text((35,25),'THE ASHBORN ISLES / CINDERMAW 0.2',font=b.font(32),fill='#edba5d')
    d.text((35,72),f'5 goblin countries | 19 locations | one faith | {sum(int(Decimal(str(l["pop"]))*1000) for l in locs):,} people',font=b.font(20),fill='#dae1d7')
    detail=Image.fromarray(preview);detail.thumbnail((800,620));canvas.paste(detail,(40,140));sx=detail.width/preview.shape[1];sy=detail.height/preview.shape[0]
    for c in cfg['countries']:
        l=next(l for l in locs if l['id']==c['capital']);x=40+(l['point'][0]-box[0])*sx;y=140+(l['point'][1]-box[1])*sy
        d.ellipse((x-4,y-4,x+4,y+4),fill='#ffe29a');d.text((x-22,y+9),c['name'],font=b.font(16),fill='white',stroke_width=1,stroke_fill='#101c25')
    for i,c in enumerate(cfg['countries']):
        total=sum(int(Decimal(str(l['pop']))*1000) for l in locs if l['country']==c['tag']);d.text((40,790+i*30),f'{c["name"]}: {total:,} people | {c["culture_name"]} | capital: '+next(l['name'] for l in locs if l['id']==c['capital']),font=b.font(18),fill='#d4ddd9')
    canvas.save(reports/'Cindermaw_Map_Preview.png')
    h=heights(cfg,xx+.5-cx,yy+.5-cy)
    for i,l in enumerate(locs):
        samples=h[labels==i].astype(float)-.08340625*65535
        stats[l['id']]['topography']=l['topography']
        stats[l['id']]['height_above_sea']={'min':round(float(samples.min()),1),'median':round(float(np.median(samples)),1),'max':round(float(samples.max()),1)}
    hp=np.clip((h.astype(float)-2234)/42,0,255).astype(np.uint8);Image.fromarray(hp).save(reports/'Cindermaw_Terrain_Preview.png')
    return {'center_png':cfg['center'],'bounds':list(box),'locations':stats,'ports':ports,'land_pixels':int(land.sum()),'island_pixels':pixels,'sister_area_ratio':ratio,'coastal_sea_connections':sorted(neighbors),'original_sea_lanes_preserved':True,'replaced_water_locations':[sea['source_water']],'adjacencies':[[locs[a]['id'],locs[c]['id']] for a,c in sorted(edges)]}

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
    b.write(out,'in_game/common/heir_selections/cindermaw.txt','cm_captain_elective = '+elections[a:z+1].replace('government_reform:pirate_brethren_reform','government_reform:cm_captains_confederation')+'\n')
    b.write(out,'in_game/setup/countries/cindermaw.txt','\n'.join(f'{c["tag"]} = {{ color = rgb {{ {" ".join(map(str,c["color"]))} }} color2 = rgb {{ 36 31 29 }} culture_definition = {c["culture"]} religion_definition = cm_hunger_below is_historic = no }}' for c in countries)+'\n')
    b.write(out,'in_game/common/cultures/cindermaw.txt','\n'.join(f'{c["culture"]} = {{ language = cm_cinder_tongue color = rgb {{ {" ".join(map(str,c["color"]))} }} tags = {{ european_gfx }} culture_groups = {{ cm_goblin_group }} opinions = {{ }} }}' for c in countries)+'\n')
    flag=(b.ROOT/'mod/main_menu/common/coat_of_arms/coat_of_arms/cindermaw.txt').read_text()
    b.write(out,'main_menu/common/coat_of_arms/coat_of_arms/cindermaw.txt','\n'.join(flag.replace('CDM =',c['tag']+' =').replace('color2 = red', 'color2 = '+['red','blue','yellow','purple','orange'][i]) for i,c in enumerate(countries)))
    return {'total_population':int(total*1000),'enslaved_population':int(slaves*1000),'starting_gold':20,'vanilla_population_entries_unchanged':True,'country_populations':{c['tag']:sum(int(Decimal(str(l['pop']))*1000) for l in locs if l['country']==c['tag']) for c in countries}}

def add_localization(b,out):
    rel='main_menu/localization/english/cindermaw_l_english.yml';p=out/rel;s=p.read_text(encoding='utf-8-sig');extra={}
    for c in b.CFG['countries']:
        if c['tag']!='CDM':extra.update({c['tag']:c['name'],c['tag']+'_ADJ':c['adjective'],c['culture']:c['culture_name']})
    extra.update({'cm_goblin_group':'Goblinkin','cm_goblin_group_desc':'The peoples who emerged with the Ashborn Isles in the early fourteenth century.','cm_captain_elective_desc':'Ship captains choose a High Captain to lead their confederation.','cm_ashen_faiths_ADJ':'Ashen','cm_ashen_faiths_desc':'The island faiths of the Goblinkin, united in reverence for the power beneath the volcanoes.'})
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

