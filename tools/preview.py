"""Create a geographic context panel using the actual generated location map."""
from pathlib import Path
import json,re,sys
import numpy as np
from PIL import Image,ImageDraw
import build as b

def context(game,out,reports):
    cfg=b.CFG;im=Image.open(out/'in_game/map_data/locations.png');box=(6000,1450,8500,3350)
    a=np.array(im.crop(box).resize((525,399),Image.Resampling.NEAREST));names=b.parse_names(game)
    top=dict(re.findall(r'(?m)^\s*(\w+)\s*=\s*\{[^\n]*?topography\s*=\s*(\w+)',(game/'in_game/map_data/location_templates.txt').read_text(encoding='utf-8-sig')))
    water={c for n,c in names.items() if top.get(n) in b.WATER|{'ocean_wasteland','high_lakes','narrows'}};water.update(tuple(bytes.fromhex(z['color'])) for z in cfg['coastal_sea']['zones'])
    codes=(a[:,:,0].astype(np.uint32)<<16)+(a[:,:,1].astype(np.uint32)<<8)+a[:,:,2];ocean=np.isin(codes,[(r<<16)+(g<<8)+bb for r,g,bb in water]);rgb=np.zeros_like(a);rgb[ocean]=(24,45,59);rgb[~ocean]=(129,139,120)
    for c in cfg['countries']:
        for l in cfg['locations']:
            if l['country']==c['tag']:rgb[np.all(a==tuple(bytes.fromhex(l['color'])),axis=2)]=c['color']
    panel=Image.fromarray(rgb);d=ImageDraw.Draw(panel)
    def xy(x,y):return ((x-box[0])*525/(box[2]-box[0]),(y-box[1])*399/(box[3]-box[1]))
    for label,x,y in [('ENGLAND',7620,1850),('FRANCE',7850,2110),('PORTUGAL',7280,2640),('CASTILE',7620,2690),('MAGHREB',7570,3160),('AZORES',6390,2770)]:
        px,py=xy(x,y);d.text((px-18,py),label,font=b.font(12),fill='white',stroke_width=1,stroke_fill='#182d3b')
    x1,y1=xy(6650,2380);x2,y2=xy(7140,2840);d.rectangle((x1,y1,x2,y2),outline='#edba5d',width=2)
    px,py=xy(6680,2320);d.text((px,py),'ASHBORN ISLES',font=b.font(13),fill='#edba5d',stroke_width=1,stroke_fill='#182d3b')
    with Image.open(reports/'Goblins_Map_Preview.png') as original: canvas=original.copy()
    cd=ImageDraw.Draw(canvas)
    canvas.paste(panel,(835,180));cd.text((835,136),'ATLANTIC PLACEMENT',font=b.font(23),fill='#edba5d')
    cd.text((835,604),'Between the Azores and Portugal',font=b.font(19),fill='#d4ddd9')
    cd.text((835,640),'Gold dots: capital city or town\nCindermaw: city of Hooktooth\nBrackmaw: town of Brackhaven\nSmall clans: one town each\n\nBrackmaw land area = 60% of Cindermaw\nSix varied islands / five countries',font=b.font(17),fill='#d4ddd9',spacing=7)
    canvas.save(reports/'Goblins_Map_Preview.png')
    return str(reports/'Goblins_Map_Preview.png')

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--game',type=Path,required=True);args=p.parse_args();print(context(args.game,b.ROOT/'build/goblins_ashborn_isles',b.ROOT/'build/reports'))
