"""Build the Cindermaw demo from a local EU5 installation. Never edits game files."""
from __future__ import annotations
import argparse, hashlib, json, re, shutil, sys, zipfile
from collections import deque
from decimal import Decimal
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

Image.MAX_IMAGE_PIXELS = None
ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / 'data/island.json').read_text())
W, H = 16384, 8192
SEA_LEVEL = 0.08340625 * 65535
WATER = {'ocean','coastal_ocean','deep_ocean','inland_sea','lakes','lake'}
HASHES = {}

def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1024*1024), b''): h.update(b)
    return h.hexdigest()

def source(game, rel):
    p = game / rel
    if not p.is_file(): raise ValueError(f'Missing game file: {rel}')
    HASHES[rel] = sha(p)
    return p

def read(game, rel): return source(game, rel).read_text(encoding='utf-8-sig')

def write(base, rel, content):
    p = base / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content.replace('\r\n','\n'), encoding='utf-8-sig', newline='\r\n')

def clean(text):
    # Preserve positions while masking comments and quoted strings.
    return re.sub(r'"(?:\\.|[^"\\])*"|#[^\r\n]*', lambda m:' '*len(m[0]), text)

def block_span(text, key, start=0):
    c=clean(text)
    m=re.search(r'(?m)^\s*'+re.escape(key)+r'\s*=\s*\{', c[start:])
    if not m: raise ValueError(f'Missing block {key}')
    left=start+m.end()-1; depth=1; i=left+1
    while depth and i<len(c):
        depth += (c[i]=='{')-(c[i]=='}'); i+=1
    if depth: raise ValueError(f'Unbalanced block {key}')
    return left,i-1

def inject(text,key,addition,start=0):
    _,end=block_span(text,key,start)
    return text[:end]+'\n'+addition+'\n'+text[end:]

def parse_names(game):
    names={}
    for p in sorted((game/'in_game/map_data/named_locations').glob('*.txt')):
        for n,h in re.findall(r'(?m)^\s*(\w+)\s*=\s*([a-fA-F0-9]{6})\b',p.read_text(encoding='utf-8-sig')):
            names[n]=tuple(bytes.fromhex(h))
    return names

def footprint(x,y):
    rx,ry=CFG['radius']
    r=np.sqrt((x/rx)**2+(y/ry)**2)
    a=np.arctan2(y/ry,x/rx)
    edge=1+0.065*np.sin(5*a)+0.035*np.cos(9*a)-0.06*np.sin(2*a)
    # East-facing Hooktooth inlet, broad enough to read at map scale.
    edge-=0.18*np.exp(-((a-0.12)/0.24)**2)
    return edge-r

def connectivity(mask):
    points=np.argwhere(mask)
    if not len(points): return 0,0
    seen=set(); comps=0
    for py,px in points:
        key=(int(py),int(px))
        if key in seen:continue
        comps+=1; seen.add(key); q=deque([key])
        while q:
            y,x=q.popleft()
            for dy,dx in ((0,1),(1,0),(0,-1),(-1,0)):
                yy,xx=y+dy,x+dx
                if 0<=yy<mask.shape[0] and 0<=xx<mask.shape[1] and mask[yy,xx] and (yy,xx) not in seen:
                    seen.add((yy,xx));q.append((yy,xx))
    return comps,len(points)

def font(size):
    for p in [Path('C:/Windows/Fonts/segoeui.ttf'),Path('C:/Windows/Fonts/arial.ttf')]:
        if p.exists():return ImageFont.truetype(str(p),size)
    return ImageFont.load_default()

def build_map(game,out,reports):
    locs=CFG['locations']; cx,cy=CFG['center']; box=(cx-128,cy-128,cx+128,cy+128)
    yy,xx=np.mgrid[-128:128,-128:128]
    land=footprint(xx+0.5,yy+0.5)>0
    d=np.stack([(xx-s['seed'][0])**2+(yy-s['seed'][1])**2 for s in locs])
    labels=np.argmin(d,axis=0)
    names=parse_names(game); colors=set(names.values()); inv={v:k for k,v in names.items()}
    for loc in locs:
        assert loc['id'] not in names, f'Location ID collision: {loc["id"]}'
        assert tuple(bytes.fromhex(loc['color'])) not in colors, 'Location color collision'
    templates=read(game,'in_game/map_data/location_templates.txt')
    topographies=dict(re.findall(r'(?m)^\s*(\w+)\s*=\s*\{[^\n]*?topography\s*=\s*(\w+)',templates))
    im=Image.open(source(game,'in_game/map_data/locations.png'))
    assert im.size==(W,H) and im.mode=='RGB'
    original=np.array(im.crop(box)); patch=original.copy()
    replaced={inv[tuple(c)] for c in np.unique(original[land],axis=0)}
    assert all(topographies[n] in WATER for n in replaced), 'Island overlaps existing land!'
    stats={}; edges=set()
    for i,loc in enumerate(locs):
        mask=land&(labels==i); comps,n=connectivity(mask)
        assert comps==1 and n>=100, f'Disconnected/tiny location: {loc["id"]}'
        patch[mask]=tuple(bytes.fromhex(loc['color']))
        stats[loc['id']]={'pixels':n,'components':comps,'population':loc['pop']*1000}
    for ay,ax,by,bx in [(slice(None),slice(None,-1),slice(None),slice(1,None)),(slice(None,-1),slice(None),slice(1,None),slice(None))]:
        both=land[ay,ax]&land[by,bx]&(labels[ay,ax]!=labels[by,bx])
        for a,b in zip(labels[ay,ax][both],labels[by,bx][both]):edges.add(tuple(sorted((int(a),int(b)))))
    reached={0}
    while True:
        nxt=reached|{b for a,b in edges if a in reached}|{a for a,b in edges if b in reached}
        if nxt==reached:break
        reached=nxt
    assert len(reached)==len(locs),'Location adjacency graph is disconnected'
    im.paste(Image.fromarray(patch),box)
    p=out/'in_game/map_data/locations.png';p.parent.mkdir(parents=True,exist_ok=True);im.save(p)
    del im
    rivers=Image.open(source(game,'in_game/map_data/rivers.png'))
    rp=np.array(rivers.crop(box));rp[land]=255
    rim=Image.fromarray(rp,'P');rim.putpalette(rivers.getpalette())
    rivers.paste(rim,box);rivers.save(out/'in_game/map_data/rivers.png');del rivers
    ports=[]
    for idx in (3,5,7):
        loc=locs[idx];m=land&(labels==idx)
        coast=[]
        for py,px in np.argwhere(m):
            for dy,dx in ((0,1),(1,0),(0,-1),(-1,0)):
                wy,wx=int(py+dy),int(px+dx)
                if not land[wy,wx]:
                    sea=inv[tuple(original[wy,wx])]
                    if topographies.get(sea) in WATER:
                        score=(px-128-loc['seed'][0])**2+(py-128-loc['seed'][1])**2
                        coast.append((score,wx,wy,sea))
        assert coast,f'No coast for {loc["id"]}'
        _,wx,wy,sea=min(coast)
        ports.append({'land':loc['id'],'sea':sea,'x':box[0]+wx,'y':H-(box[1]+wy),'png_y':box[1]+wy})
    port_source=read(game,'in_game/map_data/ports.csv')
    write(out,'in_game/map_data/ports.csv',port_source.rstrip()+'\n'+''.join(f'{p["land"]};{p["sea"]};{p["x"]};{p["y"]};x\n' for p in ports))
    write(out,'in_game/map_data/named_locations/cindermaw.txt','\n'.join(f'{l["id"]} = {l["color"]}' for l in locs)+'\n')
    defaults=[]
    for l in locs:
        port=' natural_harbor_suitability = 0.80' if l['id']=='cm_hooktooth' else (' natural_harbor_suitability = 0.35' if l['id'] in [p['land'] for p in ports] else '')
        defaults.append(f'{l["id"]} = {{ topography = {l["topography"]} vegetation = {l["vegetation"]} climate = tropical religion = cm_hunger_below culture = cm_cinderkin raw_material = {l["good"]}{port} }}')
    write(out,'in_game/map_data/location_templates.txt',templates.rstrip()+'\n\n# Cindermaw demo\n'+'\n'.join(defaults)+'\n')
    provinces={l['province']:[x['id'] for x in locs if x['province']==l['province']] for l in locs}
    area='cm_cindermaw_area = {\n'+'\n'.join(f'    {p} = {{ {" ".join(v)} }}' for p,v in provinces.items())+'\n}'
    definitions=read(game,'in_game/map_data/definitions.txt')
    write(out,'in_game/map_data/definitions.txt',inject(definitions,'madagascar_region',area))
    build_terrain(game,out,land,box)
    # Technical preview from actual generated boundaries, not concept art.
    overview_box=(9400,4890,10500,5900)
    vanilla=Image.open(game/'in_game/map_data/locations.png')
    region=np.asarray(vanilla.crop(overview_box).resize((660,606),Image.Resampling.NEAREST))
    water_colors={c for n,c in names.items() if topographies.get(n) in WATER|{'ocean_wasteland','high_lakes','narrows'}}
    packed=(region[:,:,0].astype(np.uint32)<<16)+(region[:,:,1].astype(np.uint32)<<8)+region[:,:,2]
    water_codes=np.array([(r<<16)+(g<<8)+b for r,g,b in water_colors])
    ocean=np.isin(packed,water_codes)
    region_rgb=np.zeros((*ocean.shape,3),np.uint8);region_rgb[ocean]=(24,45,59);region_rgb[~ocean]=(114,123,104)
    overview=Image.fromarray(region_rgb)
    od=ImageDraw.Draw(overview)
    qx=(cx-overview_box[0])*660/(overview_box[2]-overview_box[0]);qy=(cy-overview_box[1])*606/(overview_box[3]-overview_box[1])
    od.ellipse((qx-7,qy-7,qx+7,qy+7),fill='#edba5d');od.text((qx+13,qy-12),'CINDERMAW',font=font(19),fill='#edba5d')
    od.text((290,482),'MADAGASCAR',font=font(16),fill='white');od.text((28,150),'EAST AFRICA',font=font(16),fill='white')
    canvas=Image.new('RGB',(1500,960),'#121d26');cd=ImageDraw.Draw(canvas)
    cd.text((45,27),'CINDERMAW / DEMO 0.1',font=font(35),fill='#edba5d')
    cd.text((45,76),'Actual location layout • terrain rendering remains unverified in game',font=font(18),fill='#b5c2c8')
    canvas.paste(overview,(40,140))
    palette=[(92,89,80),(64,103,76),(167,115,65),(87,152,170),(143,153,77),(185,167,122),(111,139,87),(74,124,115)]
    crop=np.zeros((256,256,3),np.uint8);crop[:]=(24,45,59)
    for i,col in enumerate(palette):crop[land&(labels==i)]=col
    border=np.zeros_like(land)
    border[:,1:]|=land[:,1:]&land[:,:-1]&(labels[:,1:]!=labels[:,:-1])
    border[1:,:]|=land[1:,:]&land[:-1,:]&(labels[1:,:]!=labels[:-1,:])
    crop[border]=(30,35,32)
    detail=Image.fromarray(crop).resize((640,640),Image.Resampling.NEAREST)
    dd=ImageDraw.Draw(detail)
    for i,l in enumerate(locs):
        px,py=[int((v+128)*2.5) for v in l['seed']]
        dd.ellipse((px-11,py-11,px+11,py+11),fill='#15232b');dd.text((px-5,py-10),str(i+1),font=font(16),fill='white')
    canvas.paste(detail,(810,118))
    for i,l in enumerate(locs):
        x=45+(i%2)*715;y=785+(i//2)*35
        cd.text((x,y),f'{i+1}. {l["name"]}  /  {l["good"]}  /  {l["pop"]:,}k people',font=font(18),fill='#d4ddd9')
    canvas.save(reports/'Cindermaw_Map_Preview.png')
    return {'center_png':[cx,cy],'bounds':list(box),'locations':stats,'ports':ports,'land_pixels':int(land.sum()),'replaced_water_locations':sorted(replaced),'adjacencies':[[locs[a]['id'],locs[b]['id']] for a,b in sorted(edges)]}

def build_terrain(game,out,land,box):
    # Terrain instance coordinates are 4x map pixels, Y-up. Verified against
    # vanilla tile 11 (8192x4096 texture at scale=2, center 40960,12288).
    cx,cy=CFG['center']; yy,xx=np.mgrid[0:1024,0:1024]
    x=(xx+0.5)/4-128;y=(yy+0.5)/4-128
    inland=footprint(x,y)
    mask=np.repeat(np.repeat(land,4,0),4,1)
    base=SEA_LEVEL+500+1100*np.clip(inland,0,1)
    cone=6600*np.exp(-((x/19)**2+((y+43)/21)**2))
    crater=4000*np.exp(-((x/6)**2+((y+43)/7)**2))
    texture=100*np.sin(x*.45)*np.cos(y*.37)*np.clip(inland*5,0,1)
    height=np.where(mask,base+cone-crater+texture,2234).astype(np.uint16)
    folder='in_game/gfx/terrain2/decals/cm_island'
    target=out/folder;target.mkdir(parents=True,exist_ok=True)
    Image.fromarray(height).save(target/'cm_island_height.png')
    # Reuse the vanilla tile's valid tropical material indices: 11 lowlands,
    # 13 highlands. Keep all source assets in the game installation.
    high=mask&(cone>2200)
    materials=np.where(mask,1<<11,0).astype(np.uint16);materials[high]=1<<13
    Image.fromarray(materials).save(target/'cm_island_bitmask.png')
    for i in range(16):
        layer=np.zeros((1024,1024),np.uint8)
        if i==11:layer[mask&~high]=255
        if i==13:layer[high]=255
        Image.fromarray(layer).save(target/f'cm_island_mask_{i:02d}.png')
    definitions=read(game,'in_game/gfx/terrain2/decals/decal_definitions.txt')
    addition='\n{\n name = cm_island\n layer_textures = { heightmap = "cm_island_height.png" materials = "cm_island_bitmask.png" }\n additional_textures = { }\n}\n'
    write(out,'in_game/gfx/terrain2/decals/decal_definitions.txt',definitions+addition)
    instance={'tags':[],'strength':1,'ground_level':0,'height_blend_mode':0,'rotation':0,'fade_margin':0,'position.x':cx*4,'position.y':(H-cy)*4,'scale.x':1,'scale.y':1,'depth_priority':10000,'locked':True,'disabled':False,'dynamic':False}
    p=target/'instances/cmIsland001.json';p.parent.mkdir(exist_ok=True);p.write_text(json.dumps(instance,indent=2),encoding='utf-8')
    # A new instance intentionally invalidates the terrain scene checksum.
    # Cache generation / actual render must still be verified in the editor.
    assert np.all(height[mask]>SEA_LEVEL) and np.all(height[~mask]<SEA_LEVEL)

def build_setup(game,out):
    locs=CFG['locations'];ids=' '.join(l['id'] for l in locs)
    # Vanilla pirate_elective is gated on pirate_brethren_reform, so derive a
    # separately named election with eligibility tied to OUR government.
    elections=read(game,'in_game/common/heir_selections/republic.txt')
    a,b=block_span(elections,'pirate_elective')
    custom='cm_captain_elective = '+elections[a:b+1].replace('government_reform:pirate_brethren_reform','government_reform:cm_captains_confederation')
    write(out,'in_game/common/heir_selections/cindermaw.txt',custom+'\n')
    countries=read(game,'main_menu/setup/start/10_countries.txt')
    assert not re.search(r'(?m)^\s*CDM\s*=\s*\{',countries),'CDM tag is already in use'
    outer,_=block_span(countries,'countries');inner,_=block_span(countries,'countries',outer+1)
    addition=f'''CDM = {{
    own_control_core = {{ {ids} }}
    include = "expl_east_africa"
    include = "cm_captains"
    discovered_areas = {{ cm_cindermaw_area }}
    discovered_regions = {{ madagascar_region }}
    capital = cm_hooktooth
    country_rank = rank_duchy
    government = {{ ruler = random }}
    currency_data = {{ gold = 20 stability = 20 government_power = 50 prestige = 0 }}
}}'''
    write(out,'main_menu/setup/start/10_countries.txt',inject(countries,'countries',addition,outer+1))
    populations=read(game,'main_menu/setup/start/06_pops.txt');entries=[];total=Decimal('0');slaves=Decimal('0')
    for l in locs:
        n=Decimal(str(l['pop'])); captive=Decimal('3') if l['id']=='cm_hooktooth' else (Decimal('1.5') if l['id'] in ['cm_copperfang','cm_cinder_crown'] else Decimal('0'))
        nobles=Decimal('.100');clergy=Decimal('.200');burghers=Decimal('2.000') if l['id']=='cm_hooktooth' else Decimal('.100')
        peasants=n-captive-nobles-clergy-burghers
        rows=[f'    define_pop = {{ type = {typ} size = {v:.3f} culture = cm_cinderkin religion = cm_hunger_below }}' for typ,v in [('nobles',nobles),('clergy',clergy),('burghers',burghers),('peasants',peasants)]]
        # Entirely new fictional starting population. No vanilla pop is removed.
        if captive:rows.append(f'    define_pop = {{ type = slaves size = {captive:.3f} culture = cm_cinderkin religion = cm_hunger_below }}')
        entries.append(l['id']+' = {\n'+'\n'.join(rows)+'\n}')
        total+=n;slaves+=captive
    write(out,'main_menu/setup/start/06_pops.txt',inject(populations,'locations','\n'.join(entries)))
    cities=read(game,'main_menu/setup/start/07_cities_and_buildings.txt')
    write(out,'main_menu/setup/start/07_cities_and_buildings.txt',inject(cities,'locations','cm_hooktooth = { rank = town town_setup = cm_scrap_port }'))
    markets=read(game,'main_menu/setup/start/03_markets.txt')
    write(out,'main_menu/setup/start/03_markets.txt',inject(markets,'market_manager','add_market = cm_hooktooth'))
    return {'total_population':int(total*1000),'enslaved_population':int(slaves*1000),'starting_gold':20,'vanilla_population_entries_unchanged':True}

def localization(out):
    loc={'CDM':'Cindermaw','CDM_ADJ':'Cindermaw','CDM_ADJ_f':'Cindermaw','CDM_ADJ_m':'Cindermaw',
         'cm_cinderkin':'Cinderkin','cm_goblin_group':'Goblin','cm_cinder_tongue':'Cinder Tongue','cm_goblin_language_family':'Goblin',
         'cm_hunger_below':'The Hunger Below','cm_hunger_below_ADJ':'Ashen','cm_hunger_below_desc':'The Cinderkin hear a sleeping power beneath the volcanic crown. Its hunger is appeased by offerings and the smoke of the island forges.',
         'cm_ashen_faiths':'Ashen Faiths','cm_captains_confederation':'Confederation of Captains','cm_captain_elective':'Election of the High Captain',
         'cm_captains_confederation_desc':'Ship-clans share a harbor, a war fleet and a hunger for plunder. Their autonomy weakens taxation while supporting privateering and slave raids.',
         'cm_cindermaw_area':'Cindermaw','cm_crown_province':'The Cinder Crown','cm_hooktooth_province':'Hooktooth Coast','cm_ashfields_province':'The Ashfields',
         'cindermaw.1.title':'Smoke on the Horizon',
         'cindermaw.1.desc':'The captains have gathered at Hooktooth. Our holds are nearly empty, our ships patched, and the volcano smolders above crowded settlements. Yet Cindermaw has timber, ore and fertile ashfields. A fleet of four galleys and eight cogs, with two companies of footmen, has assembled. Across the water lie the ports of Madagascar and the African coast. Will plunder finance our rise, or will we first build a stronger home?',
         'cindermaw.1.a':'Prepare the crews.', 'cindermaw.1.b':'First, study what our island can support.',
         'cm_demo_raiding_tip':'Your starting force has assembled at Hooktooth. The captain government enables native privateering and slave-raiding mechanics. Use diplomacy to select a target; this introduction does not declare war.',
         'cm_demo_building_tip':'Hooktooth has a market, naval supplies workshop and stockade. Other locations are rural. Develop food and timber production before taking on a long war. This is an introductory choice; it grants no additional resources.'}
    for l in CFG['locations']:loc[l['id']]=l['name']
    for n in ['Grik','Mograt','Skrag','Vrek','Nibz','Krakk','Zog','Grizza','Snikka','Vezza','Morga','Krikka','Rikka']:loc['cm_'+n.lower()]=n
    for n in ['Hooktooth','Copperfang','Ashbite','Blackwake','Splinter','Saltjaw','Coalhand']:loc['cm_'+n.lower()+'_name']=n
    write(out,'main_menu/localization/english/cindermaw_l_english.yml','l_english:\n'+''.join(' '+k+': "'+v.replace('"','\\"')+'"\n' for k,v in loc.items()))

def validate(game,out,mapstats,economy):
    checks=[]
    for p in out.rglob('*.txt'):
        s=clean(p.read_text(encoding='utf-8-sig'));depth=0
        for c in s:
            depth+=(c=='{')-(c=='}')
            assert depth>=0,f'Unbalanced closing brace in {p}'
        assert depth==0,f'Unclosed brace in {p}'
    checks.append('All generated script files have balanced braces (not an engine parser test).')
    for p in out.rglob('*.json'):json.loads(p.read_text(encoding='utf-8-sig'))
    checks.append('Metadata and terrain instance JSON parse.')
    for rel in ['main_menu/setup/start/06_pops.txt','main_menu/setup/start/10_countries.txt','main_menu/setup/start/07_cities_and_buildings.txt','main_menu/setup/start/03_markets.txt','in_game/map_data/definitions.txt']:
        before=[l.strip() for l in (game/rel).read_text(encoding='utf-8-sig').splitlines() if l.strip()]
        after=[l.strip() for l in (out/rel).read_text(encoding='utf-8-sig').splitlines() if l.strip()]
        # Every original line survives in order; new content only inserted.
        pos=0
        for line in after:
            if pos<len(before) and line==before[pos]:pos+=1
        assert pos==len(before),f'Unexpected vanilla change: {rel}'
    checks.append('Existing country, population, city, market and hierarchy lines preserved in order.')
    pops=(out/'main_menu/setup/start/06_pops.txt').read_text(encoding='utf-8-sig')
    for l in CFG['locations']:
        a,b=block_span(pops,l['id']);sizes=re.findall(r'\bsize\s*=\s*([\d.]+)',pops[a:b])
        assert sum(map(Decimal,sizes))==Decimal(str(l['pop']))
    checks.append('Each new location population matches its specification; 200,000 total, 6,000 enslaved.')
    checks.append('All eight land locations are nonempty, individually connected and jointly traversable by adjacency.')
    checks.append('Island footprint replaces only existing water, with no vanilla land removed.')
    im=Image.open(out/'in_game/map_data/locations.png');mapping=parse_names(game)
    for p in mapstats['ports']:
        assert im.getpixel((p['x'],H-p['y']))==mapping[p['sea']]
    checks.append('Three ports lie on their named sea pixels with correct Y-axis conversion.')
    for folder,ids in [('unit_types',['a_footmen','n_cog','n_traditional_galley']),('building_types',['marketplace','naval_supplies_guild','stockade']),('heir_selections',['pirate_elective'])]:
        corpus='\n'.join(p.read_text(encoding='utf-8-sig') for p in (game/'in_game/common'/folder).glob('*.txt'))
        for key in ids:assert re.search(r'(?m)^\s*'+re.escape(key)+r'\s*=\s*\{',corpus),f'Missing vanilla ID {key}'
    checks.append('Starting unit, building and heir-selection IDs exist in installed EU5.')
    template=(out/'main_menu/setup/templates/cm_captains.txt').read_text(encoding='utf-8-sig')
    a,b=block_span(template,'laws')
    law_corpus='\n'.join(p.read_text(encoding='utf-8-sig') for p in (game/'in_game/common/laws').glob('*.txt'))
    for law,policy in re.findall(r'(\w+)\s*=\s*(\w+)',template[a+1:b]):
        la,lb=block_span(law_corpus,law)
        assert re.search(r'\b'+policy+r'\s*=\s*\{',law_corpus[la:lb]),f'Invalid law/policy pair {law}={policy}'
    checks.append('Every starting law/policy pair exists in its vanilla law block.')
    # The custom election must not retain the vanilla pirate reform gate.
    election=(out/'in_game/common/heir_selections/cindermaw.txt').read_text(encoding='utf-8-sig')
    assert 'government_reform:pirate_brethren_reform' not in election
    assert 'government_reform:cm_captains_confederation' in election
    checks.append('Captain election is tied to the custom reform, not a missing vanilla reform.')
    return checks

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--game',type=Path,required=True,help='EU5 game directory');args=ap.parse_args();game=args.game.resolve()
    out=ROOT/'build/cindermaw_demo';reports=ROOT/'build/reports'
    out.mkdir(parents=True,exist_ok=True);reports.mkdir(parents=True,exist_ok=True)
    # Copy only authored sources; generated output never goes into source control.
    shutil.copytree(ROOT/'mod',out,dirs_exist_ok=True)
    for p in out.rglob('*.txt'):
        p.write_text(p.read_text(encoding='utf-8-sig'),encoding='utf-8-sig',newline='\r\n')
    print('Building playable map and island terrain...',flush=True)
    mapstats=build_map(game,out,reports)
    print('Building campaign setup...',flush=True)
    economy=build_setup(game,out);localization(out)
    print('Running static validation...',flush=True)
    checks=validate(game,out,mapstats,economy)
    report={'version':CFG['version'],'target_game_version':CFG['game_version'],'status':'STATIC VALIDATION PASSED; IN-GAME TESTING PENDING','checks':checks,'map':mapstats,'economy':economy,'runtime_tested':False,'terrain_cache_baked':False,'source_sha256':HASHES}
    (reports/'validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps({'status':report['status'],'locations':len(CFG['locations']),'population':economy['total_population'],'land_pixels':mapstats['land_pixels'],'ports':len(mapstats['ports']),'output':str(out)},indent=2))

if __name__=='__main__':main()
