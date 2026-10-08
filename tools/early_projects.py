"""Small, one-off projects in the existing clan introductions."""
import food_storage

PROJECT_COST = 25
AI_RESERVE = 20
PROJECTS = {
    'GTF': (40, [
        ('b', 'Set one weight for every house.', 'ga_giltfang_honest_weights'),
        ('c', 'Let our envoys settle the accounts.', 'ga_giltfang_harbor_envoys'),
        ('d', 'Strengthen the harbor watch.', 'ga_giltfang_harbor_watch')], ''),
    'CDM': (10, [
        ('a', 'Fund Grask.', 'ga_cindermaw_drilled_captains'),
        ('b', 'Fund Kragga.', 'ga_cindermaw_court_envoys'),
        ('c', 'Fund Grakka.', 'ga_cindermaw_funded_accounts')],
        'Each adviser asks for 25 gold and five years of support. Grask offers +5% army morale; Kragga offers +0.5 diplomatic reputation; Grakka offers +5% army maintenance efficiency. We can fund only one project, or keep the treasury intact.'),
    'QBR': (11, [
        ('b', 'Repair the granary sluices.', 'ga_brackmaw_repaired_sluices'),
        ('c', 'Equip the marsh workshops.', 'ga_brackmaw_marsh_workshops'),
        ('d', 'Prepare the causeway defenses.', 'ga_brackmaw_causeway_defenses')],
        'Murgash must choose where the marsh houses put their effort: dry granaries, productive workshops, or defended approaches. Each project costs 25 gold and lasts five years. Only one can be funded; the crown may instead keep the gold. Fort preparations help existing forts and create no fort or troops.'),
    'RHK': (12, [
        ('b', 'Restore the rescue beacons.', 'ga_reefhook_restored_beacons'),
        ('c', 'Organize the repair yards.', 'ga_reefhook_repair_yards'),
        ('d', 'Send pilot envoys.', 'ga_reefhook_pilot_envoys')],
        'Skrezz can back Zikka\'s rescue lights, organize the harbor repair yards, or send skilled pilots as envoys to the other crowns. Each project costs 25 gold and lasts five years. Only one can be funded, or the treasury can be kept for other commitments. These projects grant no ship, alliance or opinion bonus.'),
    'SFK': (13, [
        ('b', 'Support crew households.', 'ga_shatterfin_crew_households'),
        ('c', 'Train the storm crews.', 'ga_shatterfin_storm_crews'),
        ('d', 'Send the maternal house\'s delegates.', 'ga_shatterfin_house_delegates')],
        'The maternal house weighs three paths: support the households that supply sailors, train crews to hold together in battle, or send delegates to defend Shatterfin\'s interests abroad. Each project costs 25 gold and lasts five years. Fund one or keep the gold. No project appoints an heir, changes succession or grants a ship or treaty.'),
    'SWK': (14, [
        ('b', 'Equip the woodland wardens.', 'ga_sootwake_woodland_wardens'),
        ('c', 'Support charcoal workshops.', 'ga_sootwake_charcoal_workshops'),
        ('d', 'Build sheltered stores.', 'ga_sootwake_sheltered_stores')],
        'Snikh must balance defended settlements, winter work and stores for growing households. Equip Zhor\'s wardens, support charcoal workshops, or shelter the food stores. Each project costs 25 gold and lasts five years. Fund one or keep the gold. The wardens improve existing fort defenses; no project grants a building or army.'),
}
MODIFIERS = {
    'ga_giltfang_honest_weights': ('global_production_efficiency', '0.05', 'Honest Weights', 'Standard measures improve production efficiency by 5% for five years.'),
    'ga_giltfang_harbor_envoys': ('diplomatic_reputation', '0.5', 'Accounts Between Crowns', 'Harbor envoys improve diplomatic reputation by 0.5 for five years.'),
    'ga_giltfang_harbor_watch': ('global_defensive', '0.10', 'Watch of Chainhaven', 'Supplied harbor watches improve fort defense by 10% for five years.'),
    'ga_cindermaw_funded_accounts': ('army_maintenance_efficiency', '0.05', "Grakka's Funded Audit", 'Funded muster accounts improve army maintenance efficiency by 5% for five years.'),
    'ga_shatterfin_crew_households': ('global_sailors_modifier', '0.05', 'Households of the Returning Tide', 'Support for crew households increases monthly sailor gain by 5% for five years.'),
    'ga_sootwake_woodland_wardens': ('global_defensive', '0.10', 'Wardens of the Blackbough', 'Equipped wardens and prepared approaches increase fort defense by 10% for five years.'),
    'ga_brackmaw_marsh_workshops': ('global_production_efficiency', '0.05', 'Tools for the Marsh Houses', 'Equipped workshops increase production efficiency by 5% for five years.'),
    'ga_brackmaw_causeway_defenses': ('global_defensive', '0.10', 'Guarded Causeways', 'Prepared causeway defenses increase fort defense by 10% for five years.'),
    'ga_reefhook_repair_yards': ('navy_maintenance_efficiency', '0.05', 'Ordered Repair Yards', 'Organized repair yards increase navy maintenance efficiency by 5% for five years.'),
    'ga_reefhook_pilot_envoys': ('diplomatic_reputation', '0.5', 'Pilots at Foreign Tables', 'Pilot envoys increase diplomatic reputation by 0.5 for five years.'),
    'ga_shatterfin_storm_crews': ('naval_morale_modifier', '0.05', 'Crews of the Stormfang', 'Crew drills increase naval morale by 5% for five years.'),
    'ga_shatterfin_house_delegates': ('diplomatic_reputation', '0.5', 'A Voice for the Maternal House', 'House delegates increase diplomatic reputation by 0.5 for five years.'),
    'ga_sootwake_charcoal_workshops': ('global_production_efficiency', '0.05', 'Work Through the Winter', 'Supported workshops increase production efficiency by 5% for five years.'),
    'ga_sootwake_sheltered_stores': ('global_food_capacity_modifier', '0.10', 'Stores Beneath the Boughs', 'Sheltered stores increase province food storage limit by 10% for five years.'),
}


def choices(tag, option):
    number, projects, text = PROJECTS[tag]
    flag = 'ga_early_project_resolved_'+tag.lower()
    available = f'NOT = {{ has_variable = {flag} }} gold >= {PROJECT_COST} OR = {{ is_ai = no gold >= {PROJECT_COST + AI_RESERVE} }}'
    result = []
    for suffix, label, modifier in projects:
        effect = f'''show_as_tooltip = {{
            add_gold = -{PROJECT_COST}
            add_country_modifier = {{ modifier = {modifier} years = 5 mode = replace }}
        }}
        custom_tooltip = ga_early_project_exclusive_tt
        hidden_effect = {{ if = {{ limit = {{ {available} }}
            set_variable = {{ name = {flag} value = yes }}
            add_gold = -{PROJECT_COST}
            add_country_modifier = {{ modifier = {modifier} years = 5 mode = replace }}
        }} }}'''
        if modifier in {'ga_brackmaw_repaired_sluices', 'ga_sootwake_sheltered_stores'}:
            effect += '\ncustom_tooltip = ' + food_storage.KEY
        result.append(option(number, suffix, label, effect,
                             'custom_tooltip = { text = ga_early_project_available_tt '+available+' }'))
    result.append(option(number, 'd' if tag == 'CDM' else 'a', 'Our other commitments come first.',
                         'custom_tooltip = ga_early_project_decline_tt\n'
                         + f'hidden_effect = {{ set_variable = {{ name = {flag} value = yes }} }}'))
    return '\n'.join(result), text


def modifiers(loc):
    loc('ga_early_project_available_tt', f'Requires #Y {PROJECT_COST} gold#! and an unresolved clan project.')
    loc(food_storage.KEY, food_storage.HELP)
    loc('ga_early_project_exclusive_tt', 'Only #Y one#! project can be funded. The other projects will be declined.')
    loc('ga_early_project_decline_tt', 'Keep your gold. All three projects are declined #Y permanently#!.\nNo project modifier is gained.')
    rows = []
    for key, (modifier, value, name, description) in MODIFIERS.items():
        rows.append(f'{key} = {{ {modifier} = {value} }}')
        loc('STATIC_MODIFIER_NAME_'+key, name)
        if modifier == 'global_food_capacity_modifier':
            description += '\n\n' + food_storage.REFERENCE
        loc('STATIC_MODIFIER_DESC_'+key, description)
    return '\n'.join(rows)
