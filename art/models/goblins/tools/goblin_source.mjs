// Goblins of the Ashborn Isles: editable glTF source preparation.
// No engine-specific mesh exporter is invoked by this module.
export function decode64(s) {
  const chars="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
  s=s.replace(/\s/g,""); const out=new Uint8Array(Math.floor(s.length*3/4)-(s.endsWith("==")?2:s.endsWith("=")?1:0));
  let bits=0,value=0,k=0;
  for(const c of s){if(c==="=")break;const n=chars.indexOf(c);if(n<0)throw Error("Invalid base64");value=(value<<6)|n;bits+=6;if(bits>=8){bits-=8;out[k++]=(value>>bits)&255;}}
  return out;
}
export function encode64(bytes) {
  const chars="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
  let out="";for(let i=0;i<bytes.length;i+=3){const n=(bytes[i]<<16)|((bytes[i+1]||0)<<8)|(bytes[i+2]||0);out+=chars[(n>>>18)&63]+chars[(n>>>12)&63]+(i+1<bytes.length?chars[(n>>>6)&63]:"=")+(i+2<bytes.length?chars[n&63]:"=");}return out;
}
export function sourceBuffers(g) {
  return g.buffers.map(b=>{if(!b.uri?.startsWith("data:application/octet-stream;base64,"))throw Error("Expected self-contained upstream glTF");const bytes=decode64(b.uri.split(",")[1]);if(bytes.length!==b.byteLength)throw Error("Buffer length mismatch");return bytes;});
}
export function readAccessor(g,buffers,index) {
  const a=g.accessors[index];if(a.sparse)throw Error("Sparse accessors not supported by this preparation tool");
  const v=g.bufferViews[a.bufferView], b=buffers[v.buffer];
  const components={SCALAR:1,VEC2:2,VEC3:3,VEC4:4,MAT4:16}[a.type];
  const sizes={5120:1,5121:1,5122:2,5123:2,5125:4,5126:4}, size=sizes[a.componentType], stride=v.byteStride||size*components;
  if(!components||!size)throw Error("Unsupported accessor");
  const start=(v.byteOffset||0)+(a.byteOffset||0), end=start+(a.count-1)*stride+size*components;
  if(end>(v.byteOffset||0)+v.byteLength||end>b.length)throw Error("Accessor exceeds buffer");
  const data=new DataView(b.buffer,b.byteOffset,b.byteLength), out=[];
  for(let i=0;i<a.count;i++){const row=[];for(let k=0;k<components;k++){const p=start+i*stride+k*size;
    const n=a.componentType===5126?data.getFloat32(p,true):a.componentType===5125?data.getUint32(p,true):a.componentType===5123?data.getUint16(p,true):a.componentType===5122?data.getInt16(p,true):a.componentType===5121?data.getUint8(p):data.getInt8(p);
    if(!Number.isFinite(n))throw Error("Non-finite accessor value");row.push(n);
  }out.push(row);}return out;
}
export function identity(){return [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1];}
export function multiply(a,b){const o=new Array(16).fill(0);for(let c=0;c<4;c++)for(let r=0;r<4;r++)for(let k=0;k<4;k++)o[c*4+r]+=a[k*4+r]*b[c*4+k];return o;}
export function transform(m,p){return [0,1,2].map(r=>m[r]*p[0]+m[4+r]*p[1]+m[8+r]*p[2]+m[12+r]);}
export function nodeMatrix(n){
  if(n.matrix)return n.matrix;
  const [x,y,z,w]=n.rotation||[0,0,0,1],s=n.scale||[1,1,1],t=n.translation||[0,0,0];
  return [(1-2*y*y-2*z*z)*s[0],(2*x*y+2*w*z)*s[0],(2*x*z-2*w*y)*s[0],0,
  (2*x*y-2*w*z)*s[1],(1-2*x*x-2*z*z)*s[1],(2*y*z+2*w*x)*s[1],0,
  (2*x*z+2*w*y)*s[2],(2*y*z-2*w*x)*s[2],(1-2*x*x-2*y*y)*s[2],0,...t,1];
}
export function worldMatrices(g){
  const worlds=new Array(g.nodes.length);
  function visit(i,parent){if(worlds[i])throw Error("Repeated/cyclic node");worlds[i]=multiply(parent,nodeMatrix(g.nodes[i]));for(const child of g.nodes[i].children||[])visit(child,worlds[i]);}
  for(const i of g.scenes[g.scene||0].nodes)visit(i,identity());return worlds;
}
export function posedGeometry(g,buffers){
  const worlds=worldMatrices(g), parts=[];
  for(let ni=0;ni<g.nodes.length;ni++){
    const node=g.nodes[ni];if(node.mesh===undefined||!worlds[ni])continue;
    const skin=node.skin===undefined?null:g.skins[node.skin];
    const ibm=skin?readAccessor(g,buffers,skin.inverseBindMatrices):null;
    const joints=skin?skin.joints.map((ji,i)=>multiply(worlds[ji],ibm[i])):null;
    for(const p of g.meshes[node.mesh].primitives){
      const positions=readAccessor(g,buffers,p.attributes.POSITION);
      const weights=skin?readAccessor(g,buffers,p.attributes.WEIGHTS_0):null;
      const indices=skin?readAccessor(g,buffers,p.attributes.JOINTS_0):null;
      const vertices=positions.map((v,i)=>{
        if(!skin)return transform(worlds[ni],v);
        const result=[0,0,0];for(let k=0;k<4;k++){const weight=weights[i][k];if(!weight)continue;const q=transform(joints[indices[i][k]],v);for(let c=0;c<3;c++)result[c]+=weight*q[c];}return result;
      });
      const faces=readAccessor(g,buffers,p.indices).flat();
      parts.push({vertices,indices:faces,material:p.material});
    }
  }return parts;
}
export function geometryBounds(parts){
  const min=[Infinity,Infinity,Infinity],max=[-Infinity,-Infinity,-Infinity];
  for(const p of parts)for(const v of p.vertices)for(let c=0;c<3;c++){min[c]=Math.min(min[c],v[c]);max[c]=Math.max(max[c],v[c]);}
  return {min,max,height:max[1]-min[1]};
}
export function firstAnimationPose(g,buffers,name="Idle"){
  const animation=g.animations.find(a=>a.name===name);if(!animation)throw Error("Missing "+name);
  for(const channel of animation.channels){
    const sampler=animation.samplers[channel.sampler];
    if(sampler.interpolation!=="LINEAR"&&sampler.interpolation!=="STEP")throw Error("Unsupported default-pose interpolation");
    const first=readAccessor(g,buffers,sampler.output)[0];
    g.nodes[channel.target.node][channel.target.path]=first;
  }
}
export function linearColor(hex){
  return hex.replace("#","").match(/../g).map(v=>{const c=parseInt(v,16)/255;return c<=0.04045?c/12.92:Math.pow((c+0.055)/1.055,2.4);}).concat(1);
}
export function buildVariant(source,clan,config){
  const g=JSON.parse(JSON.stringify(source)),buffers=sourceBuffers(source);
  firstAnimationPose(g,buffers);
  const bounds=geometryBounds(posedGeometry(g,buffers));
  const scale=config.height_m/bounds.height;
  const root=g.nodes.length;
  g.nodes.push({name:"Ashborn_Goblin_Root",children:g.scenes[g.scene||0].nodes.slice(),scale:[scale,scale,scale],translation:[0,-bounds.min[1]*scale,0]});
  g.scenes[g.scene||0].nodes=[root];
  const skin=g.materials.find(m=>m.name==="Skin");if(!skin)throw Error("Missing skin material");
  skin.name="goblin_skin_"+clan.id;skin.pbrMetallicRoughness.baseColorFactor=linearColor(clan.skin_srgb);skin.pbrMetallicRoughness.roughnessFactor=0.86;
  g.materials.find(m=>m.name==="Pants").pbrMetallicRoughness.roughnessFactor=0.92;
  g.materials.find(m=>m.name==="Teeth").pbrMetallicRoughness.roughnessFactor=0.72;
  g.meshes[0].name="Ashborn_Goblin_Body";
  g.scenes[g.scene||0].name=clan.name+" Goblin";
  g.asset.generator="Ashborn goblin preparation v1; base: "+source.asset.generator;
  g.asset.copyright="Base model by Quaternius, CC0 1.0; Ashborn variants by the Goblins of the Ashborn Isles project.";
  g.extras={ashborn:{stage:"art-source-prototype",clan:clan.id,country:clan.country,culture:clan.culture,skin_srgb:clan.skin_srgb,height_m:config.height_m,source_git_blob:config.source.git_blob,engine_exported:false}};
  g.buffers.forEach((b,i)=>{b.uri="../shared/goblin_"+i+".bin";});
  return {gltf:g,buffers,scale};
}
export function validateModel(g,buffers){
  const accessors=g.accessors.map((_,i)=>readAccessor(g,buffers,i));
  let triangles=0;
  for(const mesh of g.meshes)for(const p of mesh.primitives){
    if((p.mode??4)!==4)throw Error("Expected triangles");
    const count=g.accessors[p.attributes.POSITION].count;
    const indices=accessors[p.indices].flat();if(indices.length%3)throw Error("Incomplete triangle");
    for(const i of indices)if(i<0||i>=count)throw Error("Vertex index out of range");
    for(const ai of Object.values(p.attributes))if(g.accessors[ai].count!==count)throw Error("Attribute count mismatch");
    triangles+=indices.length/3;
    const ws=accessors[p.attributes.WEIGHTS_0],js=accessors[p.attributes.JOINTS_0];
    for(let i=0;i<ws.length;i++){if(Math.abs(ws[i].reduce((a,b)=>a+b,0)-1)>1e-4)throw Error("Skin weights do not sum to one");for(let k=0;k<4;k++)if(ws[i][k]&&js[i][k]>=g.skins[0].joints.length)throw Error("Joint index out of range");}
  }
  for(const a of g.animations)for(const c of a.channels){
    if(!g.nodes[c.target.node])throw Error("Animation targets missing node");
    const s=a.samplers[c.sampler],times=accessors[s.input].flat(),values=accessors[s.output];
    if(times.length!==values.length)throw Error("Animation sample count mismatch");
    for(let i=1;i<times.length;i++)if(times[i]<=times[i-1])throw Error("Animation times not strictly increasing");
    if(c.target.path==="rotation")for(const q of values)if(Math.abs(Math.hypot(...q)-1)>1e-3)throw Error("Non-unit animation quaternion");
  }
  const bounds=geometryBounds(posedGeometry(g,buffers));
  return {triangles,joints:g.skins[0].joints.length,animations:g.animations.map(a=>a.name),bounds};
}

// Sculpt the reusable base without changing its skeleton or animation tracks.
export function prepareBase(source) {
 const g=JSON.parse(JSON.stringify(source)), buffers=sourceBuffers(g), original=buffers[0];
 const data=new Uint8Array(original),view=new DataView(data.buffer);
 function writeAccessor(index,rows){
   const a=g.accessors[index],v=g.bufferViews[a.bufferView],stride=v.byteStride||rows[0].length*4;
   rows.forEach((row,i)=>row.forEach((n,c)=>view.setFloat32((v.byteOffset||0)+(a.byteOffset||0)+i*stride+c*4,n,true)));
   if(a.type==="VEC3"&&a.min){a.min=[0,1,2].map(c=>Math.min(...rows.map(v=>v[c])));a.max=[0,1,2].map(c=>Math.max(...rows.map(v=>v[c])));}
 }
 function components(positions,indices){
   const parent=positions.map((_,i)=>i),seen=new Map();
   const find=i=>parent[i]===i?i:(parent[i]=find(parent[i])),union=(a,b)=>{parent[find(a)]=find(b);};
   positions.forEach((v,i)=>{const key=v.map(n=>n.toFixed(5)).join();if(seen.has(key))union(i,seen.get(key));else seen.set(key,i);});
   for(let i=0;i<indices.length;i+=3){union(indices[i],indices[i+1]);union(indices[i],indices[i+2]);}
   const groups=new Map();positions.forEach((v,i)=>{const key=find(i);if(!groups.has(key))groups.set(key,[]);groups.get(key).push(i);});
   return [...groups.values()];
 }
 function normals(positions,indices){
   const out=positions.map(()=>[0,0,0]);
   for(let i=0;i<indices.length;i+=3){const [a,b,c]=indices.slice(i,i+3),u=positions[b].map((v,k)=>v-positions[a][k]),v=positions[c].map((v,k)=>v-positions[a][k]);
    const n=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]];
    for(const j of [a,b,c])for(let k=0;k<3;k++)out[j][k]+=n[k];
   }return out.map(n=>{const length=Math.hypot(...n);return length?n.map(v=>v/length):[0,1,0];});
 }
 for(const p of g.meshes[0].primitives){
   const pos=readAccessor(g,buffers,p.attributes.POSITION),indices=readAccessor(g,buffers,p.indices).flat(),mat=g.materials[p.material].name;
   const groups=components(pos,indices);
   for(const group of groups){
     const minY=Math.min(...group.map(i=>pos[i][1])),maxY=Math.max(...group.map(i=>pos[i][1]));
     for(const i of group){
       let [x,y,z]=pos[i];
       if(mat==="Skin"&&minY>2&&maxY>3){
         const jaw=Math.max(0,Math.min(1,(2.55-y)/.25)),forehead=Math.max(0,Math.min(1,(y-2.75)/.35));
         x*=1+.16*jaw-.13*forehead;
         y-=.10*Math.max(0,Math.min(1,(y-2.65)/.45));
         if(z>0)z+=.035*jaw;
       }else if(mat==="Skin"&&minY>2.3){
         const tip=Math.max(0,(Math.abs(x)-.53)/.257);
         x+=Math.sign(x)*.29*tip;y+=.10*tip;
         if(x<0)y-=.025*tip;
       }else if(mat==="Face"&&minY>2.4&&maxY<2.66){
         const center=Math.sign(x)*.2436;
         x=center+(x-center)*1.8;
         y=2.585+(y-2.55856)*.48+.30*(Math.abs(x)-.2436);
         z+=.025;
       }else if(mat==="Face"&&minY>2.65){
         y+=.20*(Math.abs(x)-.25)-.055;z+=.022;
       }else if(mat==="Face"&&maxY<2.4){
         y+=.028*x/.20;z+=.045;
       }else if(mat==="Teeth"){
         y=2.25645+(y-2.25645)*(x>0?1.38:1.22);z+=.045;
       }
       pos[i]=[x,y,z];
     }
   }
   writeAccessor(p.attributes.POSITION,pos);
   writeAccessor(p.attributes.NORMAL,normals(pos,indices));
 }
 // A faceted hooked nose, weighted to the original Head joint.
 const points=[[-.09,2.74,.435],[.09,2.74,.435],[-.13,2.53,.445],[.13,2.53,.445],
 [-.085,2.49,.72],[.085,2.49,.72],[.018,2.72,.64],[.018,2.47,.81],[0,2.43,.46]];
 const faces=[[0,1,6],[0,6,4],[0,4,2],[1,3,5],[1,5,6],[6,5,7],[6,7,4],[4,7,8],[7,5,8],[2,4,8],[5,3,8],[2,8,3],[0,2,3],[0,3,1]];
 const position=[],normal=[],joint=[],weight=[],index=[];
 const headJoint=g.skins[0].joints.findIndex(i=>g.nodes[i].name==="Head");if(headJoint<0)throw Error("Head joint missing");
 for(const face of faces){
   let pv=face.map(i=>points[i]);
   const edge=(a,b)=>a.map((n,i)=>n-b[i]);let u=edge(pv[1],pv[0]),v=edge(pv[2],pv[0]);
   const outward=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]],center=[0,2.59,.55],direction=[0,1,2].map(k=>pv.reduce((s,p)=>s+p[k],0)/3-center[k]);
   if(outward.reduce((s,n,k)=>s+n*direction[k],0)<0){pv=[pv[0],pv[2],pv[1]];u=edge(pv[1],pv[0]);v=edge(pv[2],pv[0]);}
   let n=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]];const length=Math.hypot(...n);n=n.map(c=>c/length);
   // Materials remain double sided, matching the upstream mesh.
   for(const p of pv){position.push(p);normal.push(n);joint.push([headJoint,0,0,0]);weight.push([1,0,0,0]);index.push([index.length]);}
 }
 const chunks=[data];let byteLength=data.length;
 function append(rows,type,componentType){
   const components=rows[0].length,size=componentType===5126?4:componentType===5123?2:1;
   const padding=(4-byteLength%4)%4;if(padding){chunks.push(new Uint8Array(padding));byteLength+=padding;}
   const bytes=new Uint8Array(rows.length*components*size),dv=new DataView(bytes.buffer);
   rows.forEach((row,i)=>row.forEach((n,k)=>{const off=(i*components+k)*size;if(size===4)dv.setFloat32(off,n,true);else if(size===2)dv.setUint16(off,n,true);else dv.setUint8(off,n);}));
   const bufferView=g.bufferViews.length;g.bufferViews.push({buffer:0,byteOffset:byteLength,byteLength:bytes.length});
   const accessor={bufferView,componentType,count:rows.length,type};
   if(rows===position){accessor.min=[0,1,2].map(c=>Math.min(...rows.map(v=>v[c])));accessor.max=[0,1,2].map(c=>Math.max(...rows.map(v=>v[c])));}
   const ai=g.accessors.length;g.accessors.push(accessor);chunks.push(bytes);byteLength+=bytes.length;return ai;
 }
 g.meshes[0].primitives.push({attributes:{POSITION:append(position,"VEC3",5126),NORMAL:append(normal,"VEC3",5126),JOINTS_0:append(joint,"VEC4",5121),WEIGHTS_0:append(weight,"VEC4",5126)},indices:append(index,"SCALAR",5123),material:0});
 const merged=new Uint8Array(byteLength);let cursor=0;for(const bytes of chunks){merged.set(bytes,cursor);cursor+=bytes.length;}
 g.buffers[0]={byteLength,uri:"data:application/octet-stream;base64,"+encode64(merged)};
 return g;
}

export function toGLB(gltf,buffers){
 if(buffers.length!==1)throw Error("Expected a single model buffer");
 const g=JSON.parse(JSON.stringify(gltf));delete g.buffers[0].uri;
 const json=JSON.stringify(g);if([...json].some(c=>c.charCodeAt(0)>127))throw Error("Use UTF-8 encoding for non-ASCII metadata");
 const jsonLength=Math.ceil(json.length/4)*4,binLength=Math.ceil(buffers[0].length/4)*4;
 const bytes=new Uint8Array(12+8+jsonLength+8+binLength),dv=new DataView(bytes.buffer);
 dv.setUint32(0,0x46546c67,true);dv.setUint32(4,2,true);dv.setUint32(8,bytes.length,true);
 dv.setUint32(12,jsonLength,true);dv.setUint32(16,0x4e4f534a,true);
 bytes.fill(32,20,20+jsonLength);for(let i=0;i<json.length;i++)bytes[20+i]=json.charCodeAt(i);
 const b=20+jsonLength;dv.setUint32(b,binLength,true);dv.setUint32(b+4,0x004e4942,true);bytes.set(buffers[0],b+8);
 return bytes;
}