"""Regenerate the committed 0.5.5 minority distribution with its fixed seed."""
from pathlib import Path
import json, random
root=Path(__file__).resolve().parents[1]
cfg=json.loads((root/'data/island.json').read_text())
rng=random.Random(1337055)
cultures={c['tag']:c['culture'] for c in cfg['countries']}
# Rates are additions relative to the home population, not final population shares.
# Clan homelands remain dominant; ports and mines concentrate migrants/captives.
rates={'CDM':(.23,.32,.76,.90),'QBR':(.18,.26,.58,.76),'RHK':(.15,.23,.38,.59),'SFK':(.19,.27,.48,.68),'SWK':(.13,.20,.35,.55)}
locations={}; summary={}
for island in cfg['islands']:
 tag=island['country']; home=cultures[tag]; summary.setdefault(tag,{'added':0,'slaves':0})
 for loc in island['locations']:
  lo,hi,slo,shi=rates[tag]
  capital=loc['id']==next(c['capital'] for c in cfg['countries'] if c['tag']==tag)
  mine=loc['good'] in ['iron','copper','goods_gold','silver','stone','alum']
  count=round(loc['pop']*1000*rng.uniform(lo,hi)*(1.2 if capital else 1.1 if mine else 1))
  foreign=rng.sample([v for v in cultures.values() if v!=home],4)
  weights=[rng.uniform(.5,1.8) for _ in foreign]; remaining=count; pops=[]
  for i,culture in enumerate(foreign):
   people=remaining if i==len(foreign)-1 else int(count*weights[i]/sum(weights));remaining-=people
   slaves=round(people*min(.95,rng.uniform(slo,shi)+(.04 if mine else 0)))
   free=people-slaves
   workers=round(free*rng.uniform(.25,.55))
   merchants=round(free*rng.uniform(.15,.30)) if capital else 0
   for kind,n in [('slaves',slaves),('laborers',workers),('burghers',merchants),('peasants',free-workers-merchants)]:
    if n:pops.append({'type':kind,'size':n/1000,'culture':culture})
   summary[tag]['slaves']+=slaves
  locations[loc['id']]=pops;summary[tag]['added']+=count
(root/'data/mixed_populations.json').write_text(json.dumps({'seed':1337055,'description':'Additional goblins from other Ashborn islands. Existing home-culture populations and classes are preserved. Sizes are thousands of people.','locations':locations},indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(summary,indent=2))
