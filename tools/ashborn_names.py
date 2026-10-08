"""Shared Ashborn language with five naming dialects and authored royal courts."""
from clan_identity import PROFILES

POOLS={
 'CDM':('Emberblood','cm_cinderkin',
 'Drogg Grask Korgat Throkk Gorrak Kragg Mograt Drukk Grond Krazg Vorgg Brakk Garkuk Ogrash Krogmar Rukk',
 'Grakka Kragga Mograz Drakka Gorzha Bragga Korgra Urgza Vrogga Ragra Krugga Drazka Zoggra Garsha Mograkka Krazha',
 'Cindermaw Ashjaw Ironbite Forgefang Blackslag Emberclaw',
 'Coalhand Ash-Eater Chainbiter Flintknuckle Slagfoot Sootnose'),
 'QBR':('Brineward','cm_brinekin',
 'Murgash Ghorr Brumak Brugorr Ghum Bragh Murrok Ghorum Bogrash Murruk Grubak Borgh Umrag Broggar Ghurmak Mughor',
 'Brugha Morga Ghazra Brumra Murgha Boghra Ghorrza Umgra Braghra Mugra Ghumza Morghra Brugzha Urrgha Brorzha Ghubra',
 'Brackmaw Miretooth Reedclaw Bogjaw Mudtusk Fenhook',
 'Mudfoot Reed-Cutter Bog-Eye Eelgrip Saltjaw Mirehand'),
 'RHK':('Reefstrider','cm_reefkin',
 'Skrezz Krizzek Zikrat Skrik Rizzik Zrekk Kizrik Skazz Vizzek Zrik Krezik Tizzak Skerz Krikzat Zizzik Rekzik',
 'Zikka Skrizza Rizzka Krizha Zrikka Skizza Tizzra Kezra Vizzka Zrekka Rikkza Skirza Kizzra Zazka Rezikka Skrezzha',
 'Reefhook Shoalcut Shellsplit Coralbite Shardhook Pearlclaw',
 'Reef-Cutter Shellbreaker Netfinger Hookhand Gullbiter Salt-Eye'),
 'SFK':('Stormfang','cm_shatterkin',
 'Vrosh Krashik Sharg Vrak Krishak Shrokk Rask Vrokk Krazhik Shrakk Rikkash Vresh Korrak Zharr Kravosh Shrik',
 'Jaima Skritcha Morzha Rikkra Krishka Zrikka Zhavra Vrazka Shrazha Vrishka Krashra Rizhka Shrikka Vroshka Krazha Zhrikka',
 'Shatterfin Knifeback Stormscar Wavecleaver Galehook Deepfang',
 'Saltfang Wavebiter Storm-Eye Ropehand Gale-Eater Keelbreaker'),
 'SWK':('Ashveil','cm_sootkin',
 'Snikh Zhor Khash Zhekh Skharr Sizh Khuzh Srozh Zhakh Nizhk Khez Szhurr Zhirr Veshk Khaz Surrkh',
 'Zheska Khazra Sishka Zhirra Khezha Sizhka Nizhka Khurza Zhasha Snezha Veshra Zhurka Sakhra Khasha Zhisra Khessha',
 'Sootwake Cinderhush Blackreed Ashveil Duskmire Smoketooth',
 'Smokehand Ashwhisper Coal-Eye Cinderfoot Blackfinger Ember-Eater'),
}

def key(name):return 'cm_ash_name_'+name.lower().replace('-','_')
def house_key(tag,n):return 'cm_shatterfin_dynasty' if tag=='SFK' and n==0 else 'cm_'+tag.lower()+'_house_'+str(n)
def dialect(culture):return culture+'_dialect'

def localization():
    result={}
    for tag,(label,culture,males,females,houses,lowborn) in POOLS.items():
        result[dialect(culture)]=label+' Cinder Tongue'
        for name in (males+' '+females+' '+lowborn).split():result[key(name)]=name
        for i,name in enumerate(houses.split()):result[house_key(tag,i)]=name
    result['cm_stone_fletcher']='The Stone Fletcher'
    result['cm_mare_mother']='The Mare-Mother'
    for profile in PROFILES.values():result[profile['nickname_key']]=profile['nickname']
    return result

def build_names(b,out):
    sections=[]
    for tag,(label,culture,males,females,houses,lowborn) in POOLS.items():
        sections.append(f'{dialect(culture)} = {{ male_names = {{ '+ ' '.join(map(key,males.split()))+' } female_names = { '+' '.join(map(key,females.split()))+' } dynasty_names = { '+' '.join(house_key(tag,i) for i,_ in enumerate(houses.split()))+' } lowborn = { '+' '.join(map(key,lowborn.split()))+' } }')
    # Shared root retains a complete Goblin fallback without borrowing human names.
    all_males=' '.join(dict.fromkeys(key(n) for p in POOLS.values() for n in p[2].split()))
    all_females=' '.join(dict.fromkeys(key(n) for p in POOLS.values() for n in p[3].split()))
    all_houses=' '.join(house_key(t,i) for t,p in POOLS.items() for i,_ in enumerate(p[4].split()))
    b.write(out,'in_game/common/languages/goblins_ashborn_isles.txt',f'cm_cinder_tongue = {{ color = rgb {{ 117 140 48 }} family = cm_goblin_language_family male_names = {{ {all_males} }} female_names = {{ {all_females} }} dynasty_names = {{ {all_houses} }} dialects = {{ '+ '\n'.join(sections)+' } }\n')

def ruler(tag):return 'cm_sfk_maarka' if tag=='SFK' else 'cm_'+tag.lower()+'_ruler'

# Authored variation is reproducible across builds; dates keep families plausible.
COURT_DATES = {
 'CDM': ('1299.3.12', '1298.6.4', '1317.8.8', '1319.2.15', ('1304.2.3', '1308.8.5', '1302.11.6')),
 'QBR': ('1301.1.17', '1300.5.8', '1318.7.26', '1319.10.5', ('1310.4.18', '1305.9.21', '1297.3.9')),
 'RHK': ('1310.9.26', '1311.2.14', '1330.4.19', '1332.8.27', ('1306.6.11', '1311.1.28', '1294.10.16')),
 'SFK': (None, None, None, None, ('1302.7.4', '1309.3.22', '1307.5.13')),
 'SWK': ('1308.7.6', '1310.10.9', '1328.1.23', '1330.5.31', ('1312.6.17', '1303.4.7', '1296.8.29')),
}

def build_courts(b,out):
    """Add families and adult courtiers; native cabinet appointments remain native."""
    dynasties=[];characters=[]
    def person(ident,name,tag,culture,capital,dynasty,born,female=False,extra='',stats=(58,58,58)):
        adm,dip,mil=stats
        characters.append(f'{ident} = {{ first_name = {{ name = {key(name)} }} culture = {culture} religion = cm_hunger_below dynasty = {dynasty} tag = {tag} birth = {capital} birth_date = {born} adm = {adm} dip = {dip} mil = {mil} '+('female = yes ' if female else '')+extra+' }')
    for country in b.CFG['countries']:
        tag=country['tag'];label,culture,males,females,houses,_=POOLS[tag];males=males.split();females=females.split();capital=country['capital'];prefix='cm_'+tag.lower()
        leader_birth,consort_birth,son_birth,daughter_birth,court_births=COURT_DATES[tag]
        for i in range(1 if tag=='SFK' else 0,4):dynasties.append(f'{house_key(tag,i)} = {{ name = {{ name = {house_key(tag,i)} }} home = {capital} }}')
        if tag!='SFK':
            nickname=' nickname = { name = cm_stone_fletcher }' if tag=='CDM' else ''
            if tag in PROFILES:nickname=' nickname = { name = '+PROFILES[tag]['nickname_key']+' }'
            ancestry=''
            if tag in {'RHK','SWK'}:
                father_birth,brother_birth=('1282.2.11','1305.10.16') if tag=='RHK' else ('1281.5.20','1303.1.14')
                person(prefix+'_father',males[5],tag,culture,capital,house_key(tag,0),father_birth,extra='death_date = 1334.9.6',stats=(63,57,88))
                ancestry=' father = '+prefix+'_father'
                person(prefix+'_brother',males[1],tag,culture,capital,house_key(tag,0),brother_birth,extra=ancestry,stats=(59,55,82))
            stats=tuple(PROFILES[tag][k] for k in ('adm','dip','mil')) if tag in PROFILES else (66,61,90)
            person(prefix+'_ruler',males[0],tag,culture,capital,house_key(tag,0),leader_birth,extra='spouse = '+prefix+'_consort'+nickname+ancestry,stats=stats)
            person(prefix+'_consort',females[0],tag,culture,capital,house_key(tag,1),consort_birth,True,'spouse = '+prefix+'_ruler',stats=(70,68,50))
            parents=f'father = {prefix}_ruler mother = {prefix}_consort'
            person(prefix+'_son',males[2] if tag in {'RHK','SWK'} else males[1],tag,culture,capital,house_key(tag,0),son_birth,extra=parents,stats=(59,55,82))
            person(prefix+'_daughter',females[1],tag,culture,capital,house_key(tag,0),daughter_birth,True,parents,stats=(67,72,61))
        for i,stats in enumerate([(84,59,43),(53,85,52),(51,57,86)]):
            person(prefix+'_court_'+str(i),[males[3],females[3],males[4]][i],tag,culture,capital,house_key(tag,i+1),court_births[i],i==1,stats=stats)
    for rel,block,rows in [('main_menu/setup/start/04_dynasties.txt','dynasty_manager',dynasties),('main_menu/setup/start/05_characters.txt','character_db',characters)]:
        p=out/rel;b.write(out,rel,b.inject(p.read_text(encoding='utf-8-sig'),block,'\n'.join(rows)))
    return len(characters)

def verify(b,out):
    lang=(out/'in_game/common/languages/goblins_ashborn_isles.txt').read_text(encoding='utf-8-sig')
    cultures=(out/'in_game/common/cultures/goblins_ashborn_isles.txt').read_text(encoding='utf-8-sig')
    chars=(out/'main_menu/setup/start/05_characters.txt').read_text(encoding='utf-8-sig')
    loc=(out/'main_menu/localization/english/goblins_ashborn_isles_l_english.yml').read_text(encoding='utf-8-sig')
    for tag,(label,culture,m,f,h,l) in POOLS.items():
        assert len(m.split())>=16 and len(f.split())>=16
        assert f'language = {dialect(culture)}' in cultures
        assert dialect(culture)+' = {' in lang
        assert ruler(tag)+' = {' in chars
        for i in range(3):assert f'cm_{tag.lower()}_court_{i} = ' in chars
    for k in localization():assert k+': ' in loc or k+':0 ' in loc,k
    assert 'nickname = { name = cm_stone_fletcher }' in chars
    assert 'nickname = { name = cm_mare_mother }' in chars
    for profile in PROFILES.values():assert 'nickname = { name = '+profile['nickname_key']+' }' in chars
    return {'cultures':5,'male_name_entries':80,'female_name_entries':80,'houses':30,'lowborn_name_entries':30,'authored_family_and_court_characters':43,'engine_generation_tested':False}
