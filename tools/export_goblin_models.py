"""Convert the pinned clan GLBs into native EU5 meshes and sampled animations.

No Blender dependency or Paradox model data is embedded. glTF metres/Y-up/RH
become engine centimetres/Y-up/LH. Runtime world scale is 0.08, like native units.
"""
import argparse,json,math,struct
from pathlib import Path
import numpy as np
from PIL import Image
from pdx_binary import node,read,write

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'art/models/goblins'
MODEL_REL=Path('in_game/gfx/models/units/ashborn_goblins')
FLIP=np.diag([100.,100.,-100.,1.]);UNFLIP=np.linalg.inv(FLIP)

def prop(typ,a):return (typ,np.asarray(a).ravel().tolist())
def quat_matrix(q):
    x,y,z,w=np.asarray(q)/np.linalg.norm(q)
    return np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],
                     [2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],
                     [2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]])
def trs(t,q,s):
    m=np.eye(4);m[:3,:3]=quat_matrix(q)@np.diag(s);m[:3,3]=t;return m
def slerp(a,b,f):
    a=a/np.linalg.norm(a);b=b/np.linalg.norm(b);dot=np.dot(a,b)
    if dot<0:b=-b;dot=-dot
    if dot>.9995:q=a+(b-a)*f
    else:
        theta=np.arccos(np.clip(dot,-1,1));q=(np.sin((1-f)*theta)*a+np.sin(f*theta)*b)/np.sin(theta)
    return q/np.linalg.norm(q)

class GLB:
    def __init__(self,path):
        raw=Path(path).read_bytes();magic,version,size=struct.unpack_from('<III',raw)
        assert magic==0x46546c67 and version==2 and size==len(raw)
        length,kind=struct.unpack_from('<II',raw,12);assert kind==0x4e4f534a
        self.g=json.loads(raw[20:20+length]);offset=20+length
        length,kind=struct.unpack_from('<II',raw,offset);assert kind==0x004e4942
        self.data=raw[offset+8:offset+8+length];self.cache={}
        self.parents={c:i for i,n in enumerate(self.g['nodes']) for c in n.get('children',[])}
        self.mesh_node=next(i for i,n in enumerate(self.g['nodes']) if 'mesh' in n)
        self.skin=self.g['skins'][self.g['nodes'][self.mesh_node]['skin']]
        needed=set(self.skin['joints'])
        for joint in list(needed):
            while joint in self.parents:joint=self.parents[joint];needed.add(joint)
        self.bones=[]
        def visit(j):
            if j in needed:self.bones.append(j)
            for c in self.g['nodes'][j].get('children',[]):visit(c)
        for j in self.g['scenes'][self.g.get('scene',0)]['nodes']:visit(j)
        self.indices={j:i for i,j in enumerate(self.bones)}
        self.names=[self.g['nodes'][j]['name'] for j in self.bones]
        assert len(set(self.names))==len(self.names)
        self.rest=self.pose()
        self.mesh_world=self.rest[self.mesh_node]
        self.ibm=self.access(self.skin['inverseBindMatrices']).reshape(-1,4,4).transpose(0,2,1)
    def access(self,index):
        if index in self.cache:return self.cache[index]
        a=self.g['accessors'][index];assert 'sparse' not in a
        v=self.g['bufferViews'][a['bufferView']]
        dtype=np.dtype({5126:'<f4',5125:'<u4',5123:'<u2',5121:'u1'}[a['componentType']])
        width={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}[a['type']]
        offset=v.get('byteOffset',0)+a.get('byteOffset',0);stride=v.get('byteStride',width*dtype.itemsize)
        x=np.ndarray((a['count'],width),dtype=dtype,buffer=self.data,offset=offset,strides=(stride,dtype.itemsize)).copy()
        if a.get('normalized'):x=x.astype(float)/np.iinfo(dtype).max
        self.cache[index]=x;return x
    def locals(self,animation=None,time=0):
        values=[{'translation':np.array(n.get('translation',[0,0,0]),float),
                 'rotation':np.array(n.get('rotation',[0,0,0,1]),float),
                 'scale':np.array(n.get('scale',[1,1,1]),float)} for n in self.g['nodes']]
        if animation is not None:
            for c in animation['channels']:
                sampler=animation['samplers'][c['sampler']];times=self.access(sampler['input']).ravel();vs=self.access(sampler['output'])
                assert sampler.get('interpolation','LINEAR') in ('LINEAR','STEP')
                hi=int(np.searchsorted(times,time,side='right'));lo=max(hi-1,0);hi=min(hi,len(times)-1)
                f=0 if lo==hi or sampler.get('interpolation')=='STEP' else (time-times[lo])/(times[hi]-times[lo])
                key=c['target']['path'];a,b=vs[lo].astype(float),vs[hi].astype(float)
                values[c['target']['node']][key]=slerp(a,b,f) if key=='rotation' else a+(b-a)*f
        return values
    def pose(self,animation=None,time=0):
        local=self.locals(animation,time);result={}
        def world(i):
            if i not in result:
                v=local[i];m=trs(v['translation'],v['rotation'],v['scale'])
                result[i]=world(self.parents[i])@m if i in self.parents else m
            return result[i]
        for i in range(len(local)):world(i)
        return result
    def primitives(self):return self.g['meshes'][self.g['nodes'][self.mesh_node]['mesh']]['primitives']

def export_mesh(g,path):
    joint_to_bone=np.array([g.indices[j] for j in g.skin['joints']])
    convert=FLIP@g.mesh_world;normal_matrix=np.linalg.inv(convert[:3,:3]).T
    meshes=[]
    for p in g.primitives():
        a=p['attributes'];positions=g.access(a['POSITION']).astype(float)
        positions=(convert@np.c_[positions,np.ones(len(positions))].T).T[:,:3]
        normals=(normal_matrix@g.access(a['NORMAL']).T).T
        normals/=np.linalg.norm(normals,axis=1)[:,None]
        axis=np.tile([1.,0,0],(len(normals),1));axis[np.abs(normals[:,0])>.9]=[0,1,0]
        tangent=np.cross(axis,normals);tangent/=np.linalg.norm(tangent,axis=1)[:,None]
        weights=g.access(a['WEIGHTS_0']).astype(float);weights/=weights.sum(axis=1)[:,None]
        ids=joint_to_bone[g.access(a['JOINTS_0']).astype(int)]
        tris=g.access(p['indices']).reshape(-1,3)[:,[0,2,1]]
        low,high=positions.min(axis=0),positions.max(axis=0);center=(low+high)/2
        mesh=node('mesh',{'p':prop('f',positions),'n':prop('f',normals),'ta':prop('f',np.c_[tangent,np.ones(len(tangent))]),
             'u0':prop('f',np.full((len(positions),2),.5)),'u1':prop('f',np.full((len(positions),2),.5)),
             'tri':prop('i',tris),'boundingsphere':prop('f',np.r_[center,np.linalg.norm(positions-center,axis=1).max()])},[
             node('aabb',{'min':prop('f',low),'max':prop('f',high)}),
             node('material',{'shader':('s','unit_material_repaint')}),
             node('skin',{'bones':('i',[4]),'ix':prop('i',ids),'w':prop('f',weights)})])
        meshes.append(mesh)
    bones=[];source_ids={j:i for i,j in enumerate(g.skin['joints'])}
    for j in g.bones:
        # glTF node transforms can describe a posed model rather than its bind pose.
        # Weighted joints must use the actual inverse-bind accessor.
        inverse=g.ibm[source_ids[j]]@np.linalg.inv(g.mesh_world) if j in source_ids else np.linalg.inv(g.rest[j])
        inverse=FLIP@inverse@UNFLIP
        attrs={'ix':('i',[g.indices[j]])}
        if j in g.parents:attrs['pa']=('i',[g.indices[g.parents[j]]])
        attrs['tx']=prop('f',inverse[:3,:].T)
        bones.append(node(g.g['nodes'][j]['name'],attrs))
    shape=node('cm_goblin_body',children=meshes+[node('skeleton',children=bones)])
    write(path,node('root',{'pdxasset':('i',[1,0])},[node('object',children=[shape])]))

def export_animation(g,anim,path):
    duration=max(float(g.access(s['input'])[-1,0]) for s in anim['samplers'])
    count=max(2,math.ceil(duration*30)+1);times=np.linspace(0,duration,count);samples=[]
    max_nonuniform=0
    for time in times:
        local=g.locals(anim,time);frame=[]
        for j in g.bones:
            v=local[j];t=v['translation']*np.array([100,100,-100]);q=v['rotation']*np.array([-1,-1,1,1]);q/=np.linalg.norm(q)
            s=v['scale'];max_nonuniform=max(max_nonuniform,float(np.ptp(s)))
            assert np.ptp(s)<.001, 'A genuinely nonuniform scale needs explicit engine support'
            s=np.array([float(np.mean(s))])
            frame.append((t,q,s))
        samples.append(frame)
    # Match native unit animations' scalar scale encoding. Source bone scales
    # differ only by exporter noise (<0.0001); retain their uniform mean and
    # the authored root stature. Pose verification measures the resulting error.
    bones=[node(name,{'sa':('s','tqs'),'t':prop('f',samples[0][i][0]),'q':prop('f',samples[0][i][1]),'s':prop('f',samples[0][i][2])}) for i,name in enumerate(g.names)]
    streams={k:prop('f',[frame[i][c] for frame in samples for i in range(len(g.bones))]) for c,k in enumerate(('t','q','s'))}
    root=node('root',{'pdxasset':('i',[1,0])},[
        node('info',{'fps':('f',[(count-1)/duration]),'sa':('i',[count]),'j':('i',[len(bones)])},bones),node('samples',streams)])
    write(path,root)
    return {'name':anim['name'],'frames':count,'duration':duration,'max_scale_axis_difference':max_nonuniform}

def srgb(x):return 12.92*x if x<=.0031308 else 1.055*x**(1/2.4)-.055
def write_text(path,text):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding='utf-8-sig')
def schematic(mesh):
    return f'''name="{mesh}_schematic"
graph={{ nodes={{
 pdxns:ecs:MeshType={{ id=0 node={{ mesh_name="{mesh}_mesh" inputs={{ "Lod_Override_0" }} }} inputs={{}} }}
 pdxns:ecs:create_skeleton_component={{ id=1 node={{ value="{mesh}_mesh" }} inputs={{}} }}
 pdxns:ecs:animation_state_machine={{ id=2 node={{}} inputs={{ link={{ pin_id="state_machine_name" linked_node=7 linked_pin="output_arg" }} }} }}
 pdxns:values:Float={{ id=3 node={{ value=0.080000 }} inputs={{}} }}
 pdxns:ecs:create_local_transform={{ id=4 node={{}} inputs={{
  link={{ pin_id="translation" linked_node=6 linked_pin="value" }}
  link={{ pin_id="scale" linked_node=3 linked_pin="value" }}
 }} }}
 pdxns:ecs:assemble_entity={{ id=5 node={{}} inputs={{
  link={{ pin_id="components" linked_node=0 linked_pin="mesh_components" }}
  link={{ pin_id="components" linked_node=1 linked_pin="skeleton" }}
  link={{ pin_id="components" linked_node=2 linked_pin="state_machine_components" }}
  link={{ pin_id="components" linked_node=4 linked_pin="local_transform" }}
 }} }}
 pdxns:values:ConstVector3f={{ id=6 node={{ value={{ 0.000000 0.000000 0.000000 }} }} inputs={{}} }}
 pdxns:ecs:get_schematic_parameter={{ id=7 node={{ parameter="CustomAnimationMachineName" }} inputs={{ link={{ pin_id="String" linked_node=8 linked_pin="value" }} }} }}
 pdxns:values:String={{ id=8 node={{ value="cm_goblin_infantry" }} inputs={{}} }}
}} }}
'''

def state_machine():
    states=[('Idle',0,'Idle'),('Attack',1,'SwordSlash'),('Move',2,'Walk'),('Retreat',3,'Run'),('Charge',4,'Run')]
    text='local_variables={ "UnitState"=int }\nbehavioral_states={\n'
    for name,number,clip in states:text+=f' "{name}"={{ timeline_layer={{ timeline="{name}" }} }}\n'
    text+='}\nevents={\n behavioral_state_transition={ name="Start" behavioral_state="Idle" transition_interval=0 }\n'
    for name,number,clip in states:
        text+=f' behavioral_state_transition={{ name="Select {name}" trigger_interval_relative={{ 0 1 }} conditions={{ "UnitState"="{number}" }} behavioral_state="{name}" transition_interval=0.15 }}\n'
    text+='}\ntimelines={\n'
    for name,number,clip in states:
        events=' '.join(f'"Select {other}"' for other,_,_ in states if other!=name)
        text+=f' "{name}"={{ events={{ {events} }} boundary_behavior=loop starttime_offset=0 playback_rate=1 layer=0 animation="cm_goblin_{clip}" duration_source=animation }}\n'
    text+='}\nstarting_timeline={ on_enter={ "Start" } boundary_behavior=loop starttime_offset=0 playback_rate=1 layer=0 }\n'
    return text

def build(out):
    out=Path(out);directory=out/MODEL_REL;directory.mkdir(parents=True,exist_ok=True)
    config=json.loads((ART/'clans.json').read_text());report={'stage':'native-export-prototype','engine_tested':False,'clans':[]}
    constructors=[];cultures=[]
    for index,clan in enumerate(config['clans']):
        g=GLB(ART/'variants'/f'{clan["id"]}.glb');name='cm_goblin_'+clan['id']
        export_mesh(g,directory/(name+'.mesh'))
        if index==0:
            report['animations']=[export_animation(g,a,directory/('cm_goblin_'+a['name']+'.anim')) for a in g.g['animations']]
        asset=f'pdxmesh = {{\n name = "{name}_mesh"\n file = "{name}.mesh"\n'
        for a in g.g['animations']:asset+=f' animation = {{ id = "cm_goblin_{a["name"]}" type = "cm_goblin_{a["name"]}.anim" }}\n'
        for i,p in enumerate(g.primitives()):
            mat=g.g['materials'][p['material']]['pbrMetallicRoughness'];color=[round(srgb(v)*255) for v in mat['baseColorFactor'][:3]]+[255]
            stem=f'{name}_{i}'
            for suffix,rgba in [('diffuse',color),('normal',[128,128,255,128]),('properties',[255,128,0,round(mat.get('roughnessFactor',.85)*255)]),('mask',[0,0,0,255])]:
                Image.new('RGBA',(4,4),tuple(rgba)).save(directory/f'{stem}_{suffix}.dds')
            asset+=f''' meshsettings = {{ name = "cm_goblin_body" index = {i}
  texture_diffuse = "{stem}_diffuse.dds"
  texture_normal = "{stem}_normal.dds"
  texture_specular = "{stem}_properties.dds"
  texture = {{ index = 3 srgb = no file = "{stem}_mask.dds" }}
  shader = "unit_material_repaint" shader_file = "gfx/FX/units.shader"
 }}
'''
        asset+='}\n';write_text(directory/(name+'.asset'),asset)
        write_text(out/'in_game/gfx/models/schematics'/f'{name}_schematic.schematic',schematic(name))
        tag=clan['culture']+'_gfx'
        # Runtime containment after the 2026-10-06 infantry-spawn access violation.
        # Preserve custom assets for offline diagnosis, but instantiate only the
        # native rig, state machine and attachment set until engine-tested.
        for category in ['army_light_infantry','army_heavy_infantry']:
            constructors.append(f'''{tag}:{category} = {{
 schematic_name = unit_skeleton_schematic
 attach = {{ 100 = heads use_uniformity = no }}
 attach = {{ 100 = torsos }}
 attach = {{ 100 = legs }}
 attach = {{ 100 = headgear }}
 attach = {{ 100 = hairstyles }}
 attach = {{ 100 = beards }}
 attach = {{ 100 = weapons }}
 attach = {{ 100 = shields }}
 attach = {{ 100 = back }}
 attach = {{ 100 = offhand }}
 animation_state_machine_name = unit_skeleton_state_machine_one_handed_axe
}}''')
        cultures.append(f'{tag} = {{ priority = 600 culture_tag = {tag} ethnicities = {{ 100 = cm_{clan["id"]}_ethnicity }} }}')
        report['clans'].append({'clan':clan['id'],'culture':clan['culture'],'gfx_tag':tag,'bones':len(g.bones),'source_joints':len(g.skin['joints']),'mesh':str(MODEL_REL/(name+'.mesh'))})
    write_text(out/'main_menu/gfx/unit_graphics/units/zz_ashborn_goblins.txt','\n'.join(constructors)+'\n')
    write_text(out/'in_game/gfx/graphical_culture_types/ashborn_goblins.txt','\n'.join(cultures)+'\n')
    write_text(out/'main_menu/gfx/animation_state_machines/cm_goblin_infantry.animsm',state_machine())
    report['runtime_infantry']='native fallback; custom goblin renderer quarantined after spawn-time crash'
    return report

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=ROOT/'build/goblin_models');args=ap.parse_args()
    result=build(args.out);write_text(args.out/'model_export.json',json.dumps(result,indent=2));print(json.dumps(result,indent=2))
