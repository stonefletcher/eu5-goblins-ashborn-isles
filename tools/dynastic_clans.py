"""Native dynasty naming, scoped to the five Ashborn countries."""
LOCALIZATION={
 'cm_ironfang_monarchy_desc':'The Ironfang Crown rules for life. Its musters provide +50% monthly manpower. The strongest eligible adult Ashborn man of the ruling dynasty inherits. A new ruling dynasty gives the country its clan name. The succession law may be changed through normal monarchy institutions.',
 'cm_rule_of_the_strongest':'Strongest of the Ruling Clan',
 'cm_rule_of_the_strongest_desc':'Only eligible adult Ashborn men of the ruling dynasty may inherit. Military ability decides; Administrative ability and then age break ties. Foreign rulers, children and characters barred from ruling are excluded. No eligible dynasty member means no eligible heir under this law; unrelated courtiers are not a fallback.',
}

def build(b,game,out):
    native=b.read(game,'in_game/common/on_action/_hardcoded.txt')
    assert 'on_new_ruler = {' in native and 'change_country_dynastic_name = {}' in native
    tags=' '.join('tag = '+c['tag'] for c in b.CFG['countries'])
    b.write(out,'in_game/common/scripted_effects/goblins_dynastic_clans.txt',f'''# Native effect updates the dynasty name and adjective. Stable country tags remain intact.
ga_update_dynastic_clan_name = {{
    if = {{
        limit = {{
            OR = {{ {tags} }}
            government_type = government_type:monarchy
            has_regent = no
            ruler ?= {{ has_dynasty = no }}
        }}
        ruler = {{ found_dynasty = random }}
    }}
    if = {{
        limit = {{
            OR = {{ {tags} }}
            government_type = government_type:monarchy
            has_regent = no
            ruler ?= {{ has_dynasty = yes }}
            OR = {{
                NOT = {{ has_variable = ga_named_dynasty }}
                NOT = {{ ruler = {{ dynasty = root.var:ga_named_dynasty }} }}
            }}
        }}
        ruler = {{ save_scope_as = new_ruler }}
        change_country_dynastic_name = {{}}
        set_variable = {{ name = ga_named_dynasty value = ruler.dynasty }}
    }}
}}
''')
    b.write(out,'in_game/common/on_action/goblins_dynastic_clans.txt',f'''# Additive hooks leave native on_new_ruler actions intact.
on_new_ruler = {{ on_actions = {{ ga_dynastic_clan_ruler }} }}
monthly_country_pulse = {{ on_actions = {{ ga_dynastic_clan_monthly }} }}
ga_dynastic_clan_ruler = {{
    trigger = {{ OR = {{ {tags} }} }}
    effect = {{ ga_update_dynastic_clan_name = yes }}
}}
# Reconciles first-month initialization, load/regency and later dynasty reassignment.
ga_dynastic_clan_monthly = {{
    trigger = {{ OR = {{ {tags} }} }}
    effect = {{ ga_update_dynastic_clan_name = yes }}
}}
''')

def verify(b,out):
    law=(out/'in_game/common/heir_selections/goblins_ashborn_isles.txt').read_text(encoding='utf-8-sig')
    assert 'all_in_dynasty = yes' in law and 'dynasty = scope:target.last_valid_ruler.dynasty' in law
    assert 'allow_female = no' in law and 'allow_children = no' in law and 'value = root.mil' in law
    effect=(out/'in_game/common/scripted_effects/goblins_dynastic_clans.txt').read_text(encoding='utf-8-sig')
    assert 'change_country_dynastic_name = {}' in effect and 'value = ruler.dynasty' in effect
    assert 'has_regent = no' in effect and 'change_tag' not in effect
    matriarchy=(out/'in_game/common/heir_selections/shatterfin.txt').read_text(encoding='utf-8-sig')
    assert 'allow_male = no' in matriarchy and 'value = root.character_age' in matriarchy
    return {'dynasty_only':True,'ranking':'military, administration, age','shatterfin_maternal_seniority_preserved':True,'native_dynamic_name_effect':True,'engine_tested':False}
