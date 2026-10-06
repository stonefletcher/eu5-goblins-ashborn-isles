"""Offline terrain/material diagnostic, not a screenshot from the game engine."""
from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import archipelago,landscape

ROOT=Path(__file__).resolve().parents[1]
cfg=archipelago.prepare(json.loads((ROOT/'data/island.json').read_text()))
yy,xx=np.mgrid[2330:2860,6630:7170]
h=(landscape.heights(cfg,xx+.5-6900,yy+.5-2500).astype(float)-landscape.SEA)/landscape.RAW_PER_WORLD
slots=landscape.material_indices(cfg,xx+.5-6900,yy+.5-2500)
colors=np.array([[128,115,95],[131,126,118],[111,120,77],[62,86,61],[130,126,85],[76,67,62],[82,96,76],[119,108,89],[115,109,99],[91,90,88],[102,119,81],[110,93,77],[103,99,94],[62,86,61],[111,120,77],[111,120,77]])
gy,gx=np.gradient(h);shade=np.clip((.9-.7*gx-.5*gy)/np.sqrt(1+gx*gx+gy*gy),.3,1.15)
rgb=np.clip(colors[slots]*shade[...,None],0,255).astype('uint8');rgb[h<=0]=[22,43,58]
im=Image.fromarray(rgb).resize((1080,1060),Image.Resampling.LANCZOS)
canvas=Image.new('RGB',(1120,1170),'#101c25');canvas.paste(im,(20,90));draw=ImageDraw.Draw(canvas)
font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',24);small=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',17)
draw.text((24,14),'ASHBORN ISLES / VOLCANIC TERRAIN PASS',font=font,fill='#edba5d')
draw.text((24,50),'Offline height and material-class preview. In-game texture appearance still requires playtesting.',font=small,fill='#d4ddd9')
for i in cfg['islands']:
 x,y=i['center'];draw.text((20+(x-6630)*2,90+(y-2330)*2),i['name'],font=small,fill='white',stroke_width=2,stroke_fill='#101c25')
out=ROOT/'art/Goblins_Volcanic_Preview.png';canvas.save(out);print(out)

