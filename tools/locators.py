"""Append native map anchors; choose actual interior pixels, not unverified seeds."""
import numpy as np

def build_locators(b,game,out,labels,seawater,sea_labels,box,height,ports):
    anchors={};sets={k:[] for k in ['city','unit_stack','combat','vfx','dock']}
    def entry(name,x,y):
        return f'{{ id={name} position={{ {x:.3f} 0 {b.H-y:.3f} }} rotation={{ 0 0 0 1 }} scale={{ 1 1 1 }} }}'
    for i,loc in enumerate(b.CFG['locations']):
        mask=labels==i;inner=mask.copy()
        for _ in range(4):
            inner=inner&np.roll(inner,1,0)&np.roll(inner,-1,0)&np.roll(inner,1,1)&np.roll(inner,-1,1)
        assert inner.any(),loc['id']+' has no interior anchor'
        ys,xs=np.where(inner)
        gy,gx=np.gradient(height.astype(float))
        score=(gx[ys,xs]**2+gy[ys,xs]**2)*.02+height[ys,xs]*.15+(xs+box[0]-loc['point'][0])**2+(ys+box[1]-loc['point'][1])**2
        j=int(score.argmin());x=float(xs[j]+box[0]+.5);y=float(ys[j]+box[1]+.5)
        anchors[loc['id']]={'x':x,'png_y':y,'height':int(height[ys[j],xs[j]])}
        for kind in ['city','unit_stack','combat','vfx']:sets[kind].append(entry(loc['id'],x,y))
    for zi,zone in enumerate(b.CFG['coastal_sea']['zones']):
        ys,xs=np.where(seawater&(sea_labels==zi));mx=np.median(xs);my=np.median(ys)
        j=int(((xs-mx)**2+(ys-my)**2).argmin())
        for kind in ['unit_stack','combat']:sets[kind].append(entry(zone['id'],xs[j]+box[0]+.5,ys[j]+box[1]+.5))
    for port in ports:sets['dock'].append(entry(port['land'],port['x']+.5,port['png_y']+.5))
    for kind,rows in sets.items():
        rel=f'in_game/gfx/map/map_objects/generated_map_object_locators_{kind}.txt'
        b.write(out,rel,b.inject(b.read(game,rel),'instances','\n'.join(rows)))
    return anchors
