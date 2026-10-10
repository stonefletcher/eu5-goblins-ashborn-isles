"""Evaluate introduction dispatch and unit grants from the actual script trees."""
from collections import Counter
from verify_055 import parse
from ashborn_roster import TAGS


def verify(read):
    actions = dict((k, v) for k, _, v in parse(read('in_game/common/on_action/goblins_ashborn_isles.txt')))
    events = dict((k, v) for k, _, v in parse(read('in_game/events/goblins_ashborn_isles.txt')))
    triggers = dict((k, v) for k, _, v in parse(read('in_game/common/scripted_triggers/goblins_gathering.txt')))
    order = [k for k, _, _ in dict((k, v) for k, _, v in actions['monthly_country_pulse'])['on_actions']]
    assert order.count('ga_ashborn_intro_monthly') == 1
    event_trigger = dict((k, v) for k, _, v in events['cindermaw.1'])['trigger']

    def test(tag, variables=(), owns_hooktooth=True):
        state = {'variables': set(variables), 'events': 0, 'units': Counter()}

        def matches(rows):
            results = []
            for key, op, value in rows:
                assert op == '='
                if key == 'tag': result = tag == value
                elif key == 'has_variable': result = value in state['variables']
                elif key == 'owns':
                    assert value == 'location:cm_hooktooth'
                    result = owns_hooktooth
                elif key == 'AND': result = matches(value)
                elif key == 'NOT': result = not matches(value)
                elif key == 'OR': result = any(matches([row]) for row in value)
                elif key == 'ga_is_goblin': result = matches(triggers[key])
                else: raise AssertionError(key)
                results.append(result)
            return all(results)

        def effects(rows):
            for key, op, value in rows:
                if key == 'if':
                    fields = dict((k, v) for k, _, v in value)
                    if matches(fields['limit']): effects([r for r in value if r[0] != 'limit'])
                elif key == 'set_variable': state['variables'].add(dict((k, v) for k, _, v in value)['name'])
                elif key == 'trigger_event_non_silently':
                    assert dict((k, v) for k, _, v in value)['id'] == 'cindermaw.1'
                    assert matches(event_trigger), 'Scheduled introduction rejected by event trigger'
                    state['events'] += 1
                elif key == 'location:cm_hooktooth': effects(value)
                elif key == 'create_sub_unit': state['units'][value] += 1
                else: raise AssertionError(key)

        for _ in range(12):
            for name in order:
                if name not in ('ga_ashborn_intro_monthly', 'cm_demo_monthly'): continue
                fields = dict((k, v) for k, _, v in actions[name])
                if matches(fields['trigger']): effects(fields['effect'])
        return state

    cindermaw_units = Counter({'unit_type:a_footmen': 1, 'unit_type:n_traditional_galley': 2, 'unit_type:n_cog': 3})
    for tag in TAGS:
        fresh = test(tag)
        assert fresh['events'] == 1, tag
        assert fresh['units'] == (cindermaw_units if tag == 'CDM' else Counter()), tag
        reloaded = test(tag, fresh['variables'])
        assert reloaded['events'] == 0 and not reloaded['units'], tag
        displaced = test(tag, owns_hooktooth=False)
        assert displaced['events'] == 1 and not displaced['units'], tag
    old_cindermaw = test('CDM', ['cm_demo_initialized'])
    assert old_cindermaw['events'] == 0 and not old_cindermaw['units']
    foreign = test('POR')
    assert foreign['events'] == 0 and not foreign['units']
    return {'six_crowns_once': True, 'existing_save_catchup': True,
            'legacy_cindermaw_not_repeated': True, 'cindermaw_units_unchanged': True,
            'foreign_countries_excluded': True, 'gameplay_tested': False}


if __name__ == '__main__':
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[1] / 'mod'
    print(json.dumps(verify(lambda p: (root / p).read_text(encoding='utf-8-sig')), indent=2))
