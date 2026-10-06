"""Culture-selected goblin portrait features, using the native portrait rig.

Geometry is authored here; portrait_bindings contains only attachment rig metadata.
No vanilla mesh, texture, or animation is redistributed. Engine testing is pending.
"""
import json, math, struct
from pathlib import Path
import numpy as np
from PIL import Image
from pdx_binary import node, write, read

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'art/models/goblins'
REL='in_game/gfx/models/portraits/ashborn'
TYPES=['male','female','boy','girl','adolescent_boy','adolescent_girl','infant']

def text(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(value,encoding='utf-8-sig')

def skin_decal(path, rgb):
    """Constant-color BC3 decal matching native 1024px / 11-mip arrays."""
    width, mip_count = 1024, 11
    header = [124, 0xA1007, width, width, width * width, 0, mip_count]
    header += [0] * 11
    header += [32, 4, int.from_bytes(b'DXT5', 'little'), 0, 0, 0, 0, 0]
    header += [0x401008, 0, 0, 0, 0]
    r, g, b = rgb
    color = (round(r * 31 / 255) << 11) | (round(g * 63 / 255) << 5) | round(b * 31 / 255)
    block = bytes([255, 255]) + bytes(6) + struct.pack('<HHI', color, color, 0)
    payload = b''.join(block * (max(1, (width >> level) // 4) ** 2) for level in range(mip_count))
    path.write_bytes(b'DDS ' + struct.pack('<31I', *header) + payload)


def geometry(sex,bones):
    """Closed pointed pinnae and tapered lower tusks; face points toward -Z."""
    parts=[[],[]]
    names={b['name']:i for i,b in enumerate(bones)}
    def tri(part,a,b,c,j):parts[part].append((np.array([a,b,c],float),j))
    young=sex=='infant'; female=sex=='female'
    x=5.8 if not female else 5.5
    y=15.7 if not female else 15.3
    if young:x,y=5.9,9.2
    for sign in [-1,1]:
        length=5.8 if not young else 3.1
        rim=np.array([[x,y-2.1,-1.6],[x+2,y-1.5,-1.0],
                      [x+length,y+3.2,-.4],[x+1.3,y+2.2,-1.5],
                      [x-.2,y+1.2,-1.8]])
        front=np.array([x+1.25,y+.15,-2.25]);back=front+np.array([0,0,1.7])
        rim[:,0]*=sign;front[0]*=sign;back[0]*=sign
        joint=names['Head_B'] if young else names['bn_ear_L_main' if sign>0 else 'bn_ear_R_main']
        for i in range(len(rim)):
            a,b=rim[i],rim[(i+1)%len(rim)]
            if sign>0:tri(0,front,b,a,joint);tri(0,back,a,b,joint)
            else:tri(0,front,a,b,joint);tri(0,back,b,a,joint)
        if young:continue
        # Separate jaw-bound teeth follow speech/idle jaw movement.
        joint=names['bn_jaw_main'];rings=[]
        for h,r,forward in [(0,.30,0),(.40,.22,-.12),(.80,.10,-.24),(1.12,.015,-.32)]:
            rings.append([np.array([sign*2.0+r*math.cos(t),10.7+h,-9.05+forward+r*math.sin(t)]) for t in np.linspace(0,2*math.pi,9)[:-1]])
        for k in range(3):
            for i in range(8):
                a,b=rings[k][i],rings[k][(i+1)%8];c,d=rings[k+1][i],rings[k+1][(i+1)%8]
                tri(1,a,c,b,joint);tri(1,b,c,d,joint)
    meshes=[]
    for faces in parts:
        if not faces:continue
        p=[];n=[];ix=[]
        for verts,j in faces:
            normal=np.cross(verts[1]-verts[0],verts[2]-verts[0]);normal/=np.linalg.norm(normal)
            p.extend(verts);n.extend([normal]*3);ix.extend([[j,0,0,0]]*3)
        p=np.array(p);n=np.array(n);axis=np.tile([0.,1,0],(len(n),1));axis[np.abs(n[:,1])>.9]=[1,0,0]
        tangent=np.cross(axis,n);tangent/=np.linalg.norm(tangent,axis=1)[:,None]
        prop=lambda t,v:(t,np.asarray(v).ravel().tolist())
        low,high=p.min(0),p.max(0);center=(low+high)/2
        meshes.append(node('mesh',{'p':prop('f',p),'n':prop('f',n),'ta':prop('f',np.c_[tangent,np.ones(len(n))]),
            'u0':prop('f',np.full((len(p),2),.5)),'tri':prop('i',np.arange(len(p))),
            'boundingsphere':prop('f',np.r_[center,np.linalg.norm(p-center,axis=1).max()])},[
            node('aabb',{'min':prop('f',low),'max':prop('f',high)}),
            node('material',{'shader':('s','portrait_attachment')}),
            node('skin',{'bones':('i',[4]),'ix':prop('i',ix),'w':prop('f',np.tile([1.,0,0,0],(len(p),1)))})]))
    return node('root',{'pdxasset':('i',[1,0])},[node('object',children=[node('ashborn_features',children=meshes+[node('skeleton',children=bones)])])])

def build(out):
    out=Path(out);dest=out/REL;dest.mkdir(parents=True,exist_ok=True)
    clans=json.loads((ART/'clans.json').read_text())['clans']
    bindings=json.loads((ART/'portrait_bindings.json').read_text())
    for sex,bones in bindings.items():write(dest/f'cm_{sex}_features.mesh',geometry(sex,bones))
    for name,color in [('normal',(128,128,255,128)),('properties',(255,96,0,210)),('ivory',(222,210,164,255))]:
        Image.new('RGBA',(4,4),color).save(dest/f'{name}.dds')
    # Opt-in visual effects, never ordinary DNA: zero-strength defaults can render globally.
    genes=['special_genes = {\nmorph_genes = {'];accessories=[];assets=[];modifiers=['cm_ashborn_appearance = {\n usage = game'];ethnicities=[]
    # Kept within supported native gene ranges. Individuals retain all other DNA.
    face={'gene_nose_length':(.76,.90),'gene_nose_tip_forward':(.8,.95),
          'gene_nose_tip_angle':(.12,.28),'gene_nose_width':(.30,.48),
          'gene_jaw_width':(.27,.43),'gene_eye_size':(.72,.88),'gene_chin_size':(.20,.34),
          'gene_head_height':(.30,.43),'gene_jaw_height':(.28,.42)}
    for clan in clans:
        ident=clan['id'];culture=clan['culture'];tag=culture+'_gfx'
        rgb=tuple(bytes.fromhex(clan['skin_srgb'].lstrip('#')))
        skin_decal(dest/f'{ident}_skin.dds', rgb)
        gene='cm_'+ident+'_skin'
        decals=''
        for part in ['head','torso']:
            decals+=f'''decal = {{ body_part = {part}
 textures = {{ diffuse = "gfx/models/portraits/ashborn/{ident}_skin.dds" }}
 blend_modes = {{ diffuse = replace }}
 alpha_curve = {{ {{ 0 0.88 }} {{ 1 0.88 }} }}
 decal_apply_order = post_skin_color priority = 100
 }}\n'''
        genes.append(f'{gene} = {{ inheritable = no {gene} = {{ index = 0 male = {{ {decals} }} '+
                     ' '.join(f'{t} = male' for t in TYPES if t!='male')+' } }')
        for sex in ['male','female','infant']:
            name=f'cm_{ident}_{sex}_features'
            settings=''
            for i,texture in enumerate([ident+'_skin','ivory'] if sex!='infant' else [ident+'_skin']):
                settings+=f'''meshsettings = {{ name = "ashborn_features" index = {i}
 texture_diffuse = "{texture}.dds" texture_normal = "normal.dds" texture_specular = "properties.dds"
 shader = "portrait_attachment" shader_file = "gfx/FX/jomini/portrait.shader" }}\n'''
            assets.append(f'pdxmesh = {{ name = "{name}_mesh" file = "cm_{sex}_features.mesh" {settings} }}\nentity = {{ name = "{name}_entity" pdxmesh = "{name}_mesh" }}')
            accessories.append(f'{name} = {{ entity = {{ required_tags = "" shared_pose_entity = head entity = {name}_entity }} }}')
        dna=f'morph = {{ mode = add gene = {gene} template = {gene} value = 1 }}\naccessory = {{ mode = add gene = cm_ashborn_features template = cm_{ident}_features value = 1 }}\n'
        dna+='\n'.join(f'morph = {{ mode = replace gene = {g} template = template_1 range = {{ {a} {b} }} }}' for g,(a,b) in face.items())
        modifiers.append(f'cm_{ident}_appearance = {{ ignore_outfit_tags = yes dna_modifiers = {{ {dna} }} weight = {{ base = 0 modifier = {{ add = 100 gfx_culture_applicable = {tag} }} }} }}')
        ethnicities.append(f'cm_{ident}_ethnicity = {{ template = "ethnicity_template"\n'+
            '\n'.join(f'{g} = {{ 100 = {{ name = template_1 range = {{ {a} {b} }} }} }}' for g,(a,b) in face.items())+
            '\n}')
    genes.append('}\naccessory_genes = { cm_ashborn_features = { inheritable = no')
    for i,clan in enumerate(clans):
        ident=clan['id'];genes.append(f'cm_{ident}_features = {{ index = {i}\n'+
            '\n'.join(f'{t} = {{ 1 = "cm_{ident}_{"infant" if t=="infant" else "female" if t in ["female","girl","adolescent_girl"] else "male"}_features" }}' for t in TYPES)+'\n}')
    genes.append('} }\n}');modifiers.append('}')
    text(dest/'ashborn_features.asset','\n'.join(assets)+'\n')
    text(out/'in_game/common/genes/zz_ashborn_portraits.txt','\n'.join(genes)+'\n')
    text(out/'in_game/common/ethnicities/ashborn.txt','\n'.join(ethnicities)+'\n')
    text(out/'main_menu/gfx/portraits/accessories/ashborn.txt','\n'.join(accessories)+'\n')
    text(out/'main_menu/gfx/portraits/portrait_modifiers/zz_ashborn.txt','\n'.join(modifiers)+'\n')
    from build_goblin_outfits import build as build_outfits
    outfits = build_outfits(out, clans)
    return {'engine_tested':False,'cultures':len(clans),'portrait_types':TYPES,'method':'muted skin with partial albedo retention, narrow jaws, pointed ears and small teeth','infants':'skin and smaller pointed ears; no tusks','outfits':outfits,'portrait_stature':'native body height unchanged; female height attribute is disabled in vanilla'}

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=ROOT/'mod');a=ap.parse_args()
    print(json.dumps(build(a.out),indent=2))
