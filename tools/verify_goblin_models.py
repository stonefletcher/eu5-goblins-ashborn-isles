"""Compare independently decoded native skinning against the GLB source poses."""
import json,re
from pathlib import Path
import numpy as np
from PIL import Image
from pdx_binary import read,write
from export_goblin_models import GLB,ART,MODEL_REL,FLIP,ROOT,trs,TEXTURE_REGISTRATION

def verify_texture_registration(out, game=None):
    """Check the attachment registry as well as the separate mesh asset registry."""
    from verify_055 import parse
    out=Path(out)
    attachments=(out/'main_menu/gfx/unit_graphics/attachments/zz_ashborn_goblins.txt').read_text(encoding='utf-8-sig')
    meshes=re.findall(r'mesh_name\s*=\s*"([^"]+)"',attachments)
    expected={f'cm_goblin_{c["id"]}_mesh' for c in json.loads((ART/'clans.json').read_text())['clans']}
    assert set(meshes)==expected and len(meshes)==len(expected)
    path=out/TEXTURE_REGISTRATION
    assert path.is_file(), 'Goblin attachments are missing texture-variation registration'
    rows=parse(path.read_text(encoding='utf-8-sig'))
    assert len(rows)==1 and rows[0][:2]==('assets_without_texture_variation','='), 'Use the native fixed-texture registry'
    entries=rows[0][2]
    assert all(op is None and value is None for _,op,value in entries)
    names=[name for name,_,_ in entries]
    assert set(names)==expected and len(names)==len(expected), 'Every clan mesh must be registered exactly once'
    assert not (out/'main_menu/gfx/unit_graphics/texture_variations/assets_without_texture_variations.txt').exists(), 'Do not replace the native registry'
    for name in names:
        asset=(out/MODEL_REL/(name.removesuffix('_mesh')+'.asset')).read_text(encoding='utf-8-sig')
        assert f'name = "{name}"' in asset, f'Unresolved texture registration: {name}'
    if game:
        native=Path(game)/'main_menu/gfx/unit_graphics/texture_variations/assets_without_texture_variations.txt'
        native_rows=parse(native.read_text(encoding='utf-8-sig'))
        assert native_rows[0][:2]==rows[0][:2]
        assert all(op is None and value is None for _,op,value in native_rows[0][2])
    return {'registered_fixed_palette_meshes':len(names),'native_contract_checked':bool(game),'native_registry_preserved':True}

def verify_graph(script, game=None):
    """Validate typed links and the native unit-constructor parameter contract."""
    nodes={}
    for match in re.finditer(r'(pdxns:[\w:]+)\s*=\s*\{',script):
        start=match.end();depth=1;end=start
        while depth:
            depth+=(script[end]=='{')-(script[end]=='}');end+=1
        block=script[start:end-1]
        ident=int(re.search(r'\bid\s*=\s*(\d+)',block)[1])
        assert ident not in nodes, 'Duplicate graph node'
        nodes[ident]=(match[1],block)
    outputs={'MeshType':{'mesh_components'},'create_skeleton_component':{'skeleton'},
             'animation_state_machine':{'state_machine_components'},'Float':{'value'},
             'ConstVector3f':{'value'},'String':{'value'},
             'create_local_transform':{'local_transform'},
             'get_schematic_parameter':{'output_arg'},'assemble_entity':{'entity_description'}}
    dependencies={}
    for ident,(kind,block) in nodes.items():
        links=re.findall(r'pin_id="([^"]+)"\s+linked_node=(\d+)\s+linked_pin="([^"]+)"',block)
        dependencies[ident]=[int(n) for _,n,_ in links]
        for pin,n,output in links:
            assert int(n) in nodes, ('Dangling link',ident,n)
            assert output in outputs[nodes[int(n)][0].split(':')[-1]], ('Wrong output pin',n,output)
        if kind.endswith(':create_local_transform'):
            pins={p:int(n) for p,n,_ in links}
            assert {'translation','scale'}<=pins.keys(), 'Transform needs explicit translation and scale'
            assert nodes[pins['translation']][0].endswith(':ConstVector3f')
            assert nodes[pins['scale']][0].endswith(':Float')
    roots=set(nodes)-{n for values in dependencies.values() for n in values}
    assert len(roots)==1 and nodes[next(iter(roots))][0].endswith(':assemble_entity')
    assert 'parameter="CustomAnimationMachineName"' in script
    if game:
        native=(Path(game)/'in_game/gfx/models/schematics/unit_skeleton_schematic.schematic').read_text(encoding='utf-8-sig')
        assert 'parameter="CustomAnimationMachineName"' in native
        for kind in {k for k,_ in nodes.values()}:
            # MeshType is present in the native full-body cavalry graph.
            reference=native if not kind.endswith(':MeshType') else (Path(game)/'in_game/gfx/models/schematics/aux_horse_schematic.schematic').read_text(encoding='utf-8-sig')
            assert kind+'=' in reference,kind

def verify(out,game=None):
    out=Path(out);folder=out/MODEL_REL;g=GLB(ART/'variants/cindermaw.glb')
    tree=read(folder/'cm_goblin_cindermaw.mesh');shape=tree['children'][0]['children'][0]
    bones=next(n for n in shape['children'] if n['name']=='skeleton')['children']
    meshes=[n for n in shape['children'] if n['name']=='mesh'];assert len(meshes)==len(g.primitives())
    parents=[n['props'].get('pa',('i',[-1]))[1][0] for n in bones]
    assert all(p<i for i,p in enumerate(parents))
    inverses=[]
    for n in bones:
        m=np.eye(4);m[:3,:]=np.array(n['props']['tx'][1]).reshape(4,3).T;inverses.append(m)
    assert [n['name'] for n in bones]==g.names
    maximum=0.;poses=0;triangles=0
    for mesh,p in zip(meshes,g.primitives()):
        xyz=np.array(mesh['props']['p'][1]).reshape(-1,3);norm=np.array(mesh['props']['n'][1]).reshape(-1,3)
        ix=np.array(mesh['props']['tri'][1]);assert ix.min()>=0 and ix.max()<len(xyz);triangles+=len(ix)//3
        assert np.isfinite(xyz).all() and np.allclose(np.linalg.norm(norm,axis=1),1,atol=1e-5)
        skin=next(n for n in mesh['children'] if n['name']=='skin')['props']
        weights=np.array(skin['w'][1]).reshape(-1,4);ids=np.array(skin['ix'][1]).reshape(-1,4)
        assert np.allclose(weights.sum(axis=1),1,atol=1e-6) and ids.max()<len(bones)
    for anim in g.g['animations']:
        native=read(folder/('cm_goblin_'+anim['name']+'.anim'));info,streams=native['children']
        count=info['props']['sa'][1][0];joint_count=info['props']['j'][1][0]
        assert joint_count==len(bones) and [n['name'] for n in info['children']]==g.names
        data={k:np.array(streams['props'][k][1]).reshape(count,joint_count,width) for k,width in [('t',3),('q',4),('s',1)]}
        assert all(np.isfinite(x).all() for x in data.values())
        assert np.allclose(np.linalg.norm(data['q'],axis=2),1,atol=1e-5)
        duration=max(float(g.access(s['input'])[-1,0]) for s in anim['samplers'])
        for frame in sorted({0,(count-1)//2,count-1}):
            world=[]
            for i in range(len(bones)):
                m=trs(data['t'][frame,i],data['q'][frame,i],np.repeat(data['s'][frame,i],3))
                world.append(world[parents[i]]@m if parents[i]>=0 else m)
            source_pose=g.pose(anim,duration*frame/(count-1))
            for mesh,p in zip(meshes,g.primitives()):
                a=p['attributes'];original=np.c_[g.access(a['POSITION']),np.ones(len(g.access(a['POSITION'])))]
                source_ids=g.access(a['JOINTS_0']).astype(int);source_w=g.access(a['WEIGHTS_0']).astype(float);source_w/=source_w.sum(axis=1)[:,None]
                expected=np.zeros_like(original)
                for influence in range(4):
                    matrices=np.array([source_pose[j]@g.ibm[k] for k,j in enumerate(g.skin['joints'])])[source_ids[:,influence]]
                    expected+=np.einsum('nij,nj->ni',matrices,original)*source_w[:,influence,None]
                expected=(FLIP@expected.T).T[:,:3]
                xyz=np.c_[np.array(mesh['props']['p'][1]).reshape(-1,3),np.ones(len(original))]
                skin=next(n for n in mesh['children'] if n['name']=='skin')['props']
                ids=np.array(skin['ix'][1]).reshape(-1,4);weights=np.array(skin['w'][1]).reshape(-1,4)
                actual=np.zeros_like(xyz)
                for influence in range(4):
                    matrices=np.array([world[i]@inverses[i] for i in range(len(bones))])[ids[:,influence]]
                    actual+=np.einsum('nij,nj->ni',matrices,xyz)*weights[:,influence,None]
                error=float(np.max(np.linalg.norm(actual[:,:3]-expected,axis=1)));maximum=max(maximum,error)
                assert error<.03,(anim['name'],frame,error)
            poses+=1
    roundtrips=0
    # Exact native round trips verify the independent parser/writer against
    # installed engine data, not only files generated by this exporter.
    if game:
        game=Path(game);temp=ROOT/'.local/pdx_roundtrip';temp.mkdir(parents=True,exist_ok=True)
        for rel in ['in_game/gfx/models/units/unit_skeleton.mesh','in_game/gfx/models/units/animations/unit_drowning.anim']:
            original=game/rel;target=temp/original.name;write(target,read(original));assert target.read_bytes()==original.read_bytes();roundtrips+=1
    clan_count=0
    for p in folder.glob('cm_goblin_*.mesh'):
        candidate=read(p);assert candidate==tree,'Clan geometry should be shared; palettes are external textures';clan_count+=1
    assert clan_count==len(json.loads((ART/'clans.json').read_text())['clans']) and triangles==2476
    config=json.loads((ART/'clans.json').read_text())
    texture_registration=verify_texture_registration(out,game)
    constructors=(out/'main_menu/gfx/unit_graphics/units/zz_ashborn_goblins.txt').read_text()
    attachments=(out/'main_menu/gfx/unit_graphics/attachments/zz_ashborn_goblins.txt').read_text(encoding='utf-8-sig')
    assert constructors.count('animation_state_machine_name = cm_goblin_infantry')==2*clan_count
    assert attachments.count('node = shared_pose_entity')==clan_count
    if game:
        native_attachments=(Path(game)/'main_menu/gfx/unit_graphics/attachments/torsos/00_european_torsos.txt').read_text(encoding='utf-8-sig')
        assert 'node = shared_pose_entity' in native_attachments and 'mesh_name =' in native_attachments
    for clan in config['clans']:
        stem='cm_goblin_'+clan['id'];tag=clan['culture']+'_gfx'
        color=Image.open(folder/(stem+'_0_diffuse.dds')).convert('RGBA').getpixel((0,0))
        expected=tuple(bytes.fromhex(clan['skin_srgb'][1:]))+(255,)
        assert color==expected,(clan['id'],color,expected)
        assert f'{tag}:army_light_infantry' in constructors and f'{tag}:army_heavy_infantry' in constructors
        assert constructors.count(f'attach = {{ 100 = {stem}_body }}')==2
        assert f'{stem}_body = {{' in attachments and f'mesh_name = "{stem}_mesh"' in attachments
        asset=(folder/(stem+'.asset')).read_text()
        for texture in re.findall(r'"([^"\n]+\.dds)"',asset):assert (folder/texture).is_file()
        for clip in re.findall(r'type = "([^"\n]+\.anim)"',asset):assert (folder/clip).is_file()
        schematic=(out/'in_game/gfx/models/schematics'/(stem+'_schematic.schematic')).read_text()
        verify_graph(schematic,game)
        ids=set(re.findall(r'(?<!_)\bid=(\d+)',schematic));links=set(re.findall(r'linked_node=(\d+)',schematic));assert links<=ids
        assert 'MeshType' not in schematic and 'mesh_components' not in schematic, 'Unit mesh must be created by the attachment factory'
        assert 'skeleton' in schematic and 'state_machine_components' in schematic
    machine=(out/'main_menu/gfx/animation_state_machines/cm_goblin_infantry.animsm').read_text()
    for clip in re.findall(r'animation="([^"]+)"',machine):assert (folder/(clip+'.anim')).is_file()
    for path in list(folder.glob('*.asset'))+list((out/'in_game/gfx/models/schematics').glob('cm_goblin_*.schematic')):
        text=path.read_text();assert text.count('{')==text.count('}')
    return {'status':'STATIC MODEL CHECKS PASSED; ENGINE PLAYTEST PENDING','runtime_infantry':'factory-created shared-pose goblin attachment','clans':clan_count,'source_joints':23,'exported_bones':len(bones),'triangles_per_clan':triangles,'animations':len(g.g['animations']),'sampled_poses':poses,'maximum_pose_error_cm':maximum,'native_byte_exact_roundtrips':roundtrips,'palettes_and_runtime_references':True,'typed_graph_links_and_unit_parameters':True,'texture_registration':texture_registration,'engine_tested':False}

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=ROOT/'build/goblin_models');ap.add_argument('--game',type=Path);args=ap.parse_args()
    report=verify(args.out,args.game);(args.out/'model_verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
