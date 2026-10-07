"""Shatterfin's maternal dynasty and seniority succession setup."""
from pathlib import Path

DYNASTY='cm_shatterfin_dynasty'
FAMILY=[
    ('cm_sfk_savra','cm_name_savra','1278.2.9',True,None,'1329.6.3',65,60,45),
    ('cm_sfk_maarka','cm_name_maarka','1298.3.12',True,'cm_sfk_savra',None,66,58,52),
    ('cm_sfk_ishra','cm_name_ishra','1301.8.4',True,'cm_sfk_savra',None,59,71,35),
    ('cm_sfk_korr','cm_name_korr','1316.1.6',False,'cm_sfk_maarka',None,70,55,98),
    ('cm_sfk_veshka','cm_name_veshka','1317.5.19',True,'cm_sfk_maarka',None,74,62,86),
    ('cm_sfk_neshri','cm_name_neshri','1318.9.2',True,'cm_sfk_maarka',None,61,76,44),
    ('cm_sfk_rikka','cm_name_rikka','1319.4.23',True,'cm_sfk_ishra',None,57,65,63),
    ('cm_sfk_sella','cm_name_sella','1335.7.11',True,'cm_sfk_veshka',None,48,54,39),
]
LOCALIZATION={
    'cm_tidemother_monarchy':'Tidemother Monarchy',
    'cm_tidemother_monarchy_desc':'Shatterfin is ruled by a maternal clan house. The Tidemother reigns for life; the eldest eligible adult woman of her dynasty succeeds, provided her mother belonged to that house. The crown retains normal monarchy institutions. Its succession law may be changed.',
    'cm_tidemother_seniority':'Seniority of the Tidemothers',
    'cm_tidemother_seniority_desc':'The eldest eligible adult Stormfang woman of the ruling dynasty inherits, with age measured to the day. Her mother must also belong to that dynasty. Sisters and maternal cousins may precede daughters. Men, children, foreign rulers and those barred from rule are excluded. Births into the maternal ruling house in Shatterfin retain their mother\'s dynasty while this law is active. No eligible adult woman means no eligible heir; the law does not admit men as a fallback.',
    'cm_tidemother_age_score':'Seniority within the maternal ruling house',
    'cm_shatterfin_dynasty':'Shatterfin',
    'cm_name_savra':'Zhavra','cm_name_maarka':'Jaima','cm_name_ishra':'Skritcha',
    'cm_name_korr':'Vrosh','cm_name_veshka':'Morzha','cm_name_neshri':'Rikkra',
    'cm_name_rikka':'Krishka','cm_name_sella':'Zrikka',
}

def build(b,game,out):
    dynasty=f'{DYNASTY} = {{ name = {{ name = {DYNASTY} }} home = cm_shatterfin }}'
    rel='main_menu/setup/start/04_dynasties.txt'
    b.write(out,rel,b.inject(b.read(game,rel),'dynasty_manager',dynasty))
    rows=[]
    for ident,name,born,female,mother,died,adm,dip,mil in FAMILY:
        row=f'{ident} = {{ first_name = {{ name = {name} }} culture = cm_shatterkin religion = cm_hunger_below dynasty = {DYNASTY} tag = SFK birth = cm_shatterfin birth_date = {born} adm = {adm} dip = {dip} mil = {mil}'
        if ident=='cm_sfk_maarka':row+=' nickname = { name = cm_mare_mother }'
        if female:row+=' female = yes'
        if mother:row+=' mother = '+mother
        if died:row+=' death_date = '+died
        rows.append(row+' }')
    rel='main_menu/setup/start/05_characters.txt'
    b.write(out,rel,b.inject(b.read(game,rel),'character_db','\n'.join(rows)))

def verify(b,out):
    law=(out/'in_game/common/heir_selections/shatterfin.txt').read_text(encoding='utf-8-sig')
    assert 'allow_male = no' in law and 'allow_children = no' in law
    assert 'value = root.character_age' in law and 'root.mil' not in law
    assert 'dynasty = scope:target.last_valid_ruler.dynasty' in law
    setup=(out/'main_menu/setup/start/10_countries.txt').read_text(encoding='utf-8-sig')
    for tag in ['CDM','QBR','RHK','SFK','SWK']:
        a,z=b.block_span(setup,tag);country=setup[a:z]
        assert ('heir_selection = cm_tidemother_seniority' if tag=='SFK' else 'heir_selection = cm_rule_of_the_strongest') in country
        if tag=='SFK':assert 'ruler = cm_sfk_maarka' in country and 'include = "cm_tidemothers"' in country
    seen=set()
    for ident,_,born,female,mother,died,*_ in FAMILY:
        if mother:assert mother in seen,'Parents must precede children'
        seen.add(ident)
    from datetime import date
    def birthday(row):return date(*map(int,row[2].split('.')))
    now=date(1337,11,11)
    eligible=sorted((r for r in FAMILY if r[0]!='cm_sfk_maarka' and r[3] and r[4] and r[5] is None and (now-birthday(r)).days>=18*365.25),key=birthday)
    assert [r[0] for r in eligible]==['cm_sfk_ishra','cm_sfk_veshka','cm_sfk_neshri','cm_sfk_rikka']
    return {'starting_ruler':'Jaima Shatterfin','starting_heir':'Skritcha Shatterfin','eligible_starting_women':4,'male_and_minor_exclusion':True,'parents_before_children':True,'engine_succession_tested':False}
