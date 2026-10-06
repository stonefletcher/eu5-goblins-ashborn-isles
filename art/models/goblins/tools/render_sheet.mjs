// Deterministic orthographic contact sheet made from the actual skinned vertices.
export function renderSheet(models, buffers, config, core) {
 const W=1600,H=690,columns=5,margin=48,scale=400,base=568;
 const rgb=new Uint8Array(W*H*3),depth=new Float64Array(W*H).fill(-Infinity);
 for(let y=0;y<H;y++)for(let x=0;x<W;x++){const i=(y*W+x)*3;rgb[i]=23;rgb[i+1]=28;rgb[i+2]=27;}
 const svg=['<svg xmlns="http://www.w3.org/2000/svg" width="'+W+'" height="'+H+'" viewBox="0 0 '+W+' '+H+'"><rect width="1600" height="690" fill="#171c1b"/><g fill="#e4e9df" font-family="sans-serif"><text x="40" y="42" font-size="26">GOBLINS OF THE ASHBORN ISLES</text><text x="40" y="70" font-size="14" fill="#a7b3aa">Actual 3D source models · first body and skin pass · 1.12 m · EU5 export pending</text></g>'];
 const yaw=-0.30,pitch=0.05;
 function project(p,center){const x=Math.cos(yaw)*p[0]+Math.sin(yaw)*p[2],z=-Math.sin(yaw)*p[0]+Math.cos(yaw)*p[2];return [center+x*scale,base-(Math.cos(pitch)*p[1]-Math.sin(pitch)*z)*scale,Math.sin(pitch)*p[1]+Math.cos(pitch)*z];}
 const cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
 const sub=(a,b)=>a.map((x,i)=>x-b[i]);
 const srgb=c=>Math.round(255*(c<=0.0031308?12.92*c:1.055*Math.pow(Math.max(c,0),1/2.4)-0.055));
 for(let m=0;m<models.length;m++){
  const center=(m+.5)*W/columns, g=models[m], parts=core.posedGeometry(g,buffers), tris=[];
  for(const part of parts){const material=g.materials[part.material].pbrMetallicRoughness.baseColorFactor;
   for(let i=0;i<part.indices.length;i+=3){
    const v=part.indices.slice(i,i+3).map(k=>part.vertices[k]),p=v.map(v=>project(v,center));
    const n=cross(sub(v[1],v[0]),sub(v[2],v[0])),length=Math.hypot(...n);if(length<1e-10)continue;
    const light=Math.max(0,(n[0]*(-.4)+n[1]*.75+n[2]*.7)/(length*Math.hypot(.4,.75,.7)));
    const color=material.slice(0,3).map(c=>Math.max(0,Math.min(255,srgb(c*(.54+.7*light)))));
    tris.push({p,color,z:p.reduce((s,v)=>s+v[2],0)/3});
    const area=(p[1][0]-p[0][0])*(p[2][1]-p[0][1])-(p[1][1]-p[0][1])*(p[2][0]-p[0][0]);if(Math.abs(area)<1e-10)continue;
    const minx=Math.max(0,Math.floor(Math.min(...p.map(v=>v[0])))),maxx=Math.min(W-1,Math.ceil(Math.max(...p.map(v=>v[0]))));
    const miny=Math.max(0,Math.floor(Math.min(...p.map(v=>v[1])))),maxy=Math.min(H-1,Math.ceil(Math.max(...p.map(v=>v[1]))));
    for(let y=miny;y<=maxy;y++)for(let x=minx;x<=maxx;x++){
      const px=x+.5,py=y+.5;
      const a=((p[1][0]-px)*(p[2][1]-py)-(p[1][1]-py)*(p[2][0]-px))/area;
      const b=((p[2][0]-px)*(p[0][1]-py)-(p[2][1]-py)*(p[0][0]-px))/area,c=1-a-b;
      if(a<0||b<0||c<0)continue;
      const z=a*p[0][2]+b*p[1][2]+c*p[2][2],id=y*W+x;if(z<=depth[id])continue;
      depth[id]=z;rgb.set(color,id*3);
    }
   }
  }
  svg.push('<ellipse cx="'+center+'" cy="'+(base+5)+'" rx="90" ry="9" fill="#101513"/>');
  for(const t of tris.sort((a,b)=>a.z-b.z))svg.push('<polygon points="'+t.p.map(v=>v[0].toFixed(1)+','+v[1].toFixed(1)).join(' ')+'" fill="rgb('+t.color.join(',')+')" />');
  const clan=config.clans[m];
  svg.push('<rect x="'+(center-72)+'" y="600" width="144" height="4" rx="2" fill="'+clan.skin_srgb+'"/><text x="'+center+'" y="632" text-anchor="middle" font-family="sans-serif" font-size="21" fill="#e4e9df">'+clan.name+'</text><text x="'+center+'" y="657" text-anchor="middle" font-family="sans-serif" font-size="14" fill="#a7b3aa">'+clan.shade+'</text>');
 }
 svg.push('</svg>');
 return {width:W,height:H,rgb,svg:svg.join('\n')};
}
export function encodePNG(width,height,rgb) {
 const join=arrays=>{const out=new Uint8Array(arrays.reduce((s,a)=>s+a.length,0));let p=0;for(const a of arrays){out.set(a,p);p+=a.length;}return out;};
 const u32=n=>new Uint8Array([(n>>>24)&255,(n>>>16)&255,(n>>>8)&255,n&255]);
 const table=new Uint32Array(256);for(let i=0;i<256;i++){let c=i;for(let k=0;k<8;k++)c=c&1?0xedb88320^(c>>>1):c>>>1;table[i]=c>>>0;}
 function crc(b){let c=0xffffffff;for(const n of b)c=table[(c^n)&255]^(c>>>8);return (c^0xffffffff)>>>0;}
 function chunk(name,data){const body=join([new Uint8Array([...name].map(c=>c.charCodeAt(0))),data]);return join([u32(data.length),body,u32(crc(body))]);}
 const scan=new Uint8Array(height*(width*3+1));
 for(let y=0;y<height;y++)scan.set(rgb.subarray(y*width*3,(y+1)*width*3),y*(width*3+1)+1);
 let a=1,b=0;for(const n of scan){a=(a+n)%65521;b=(b+a)%65521;}
 const parts=[new Uint8Array([0x78,0x01])];
 for(let p=0;p<scan.length;p+=65535){const n=Math.min(65535,scan.length-p);parts.push(new Uint8Array([p+n===scan.length?1:0,n&255,n>>>8,(~n)&255,((~n)>>>8)&255]),scan.subarray(p,p+n));}
 parts.push(u32((b<<16)|a));
 const ihdr=join([u32(width),u32(height),new Uint8Array([8,2,0,0,0])]);
 return join([new Uint8Array([137,80,78,71,13,10,26,10]),chunk("IHDR",ihdr),chunk("IDAT",join(parts)),chunk("IEND",new Uint8Array())]);
}
