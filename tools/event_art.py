"""Single source of truth for authored event and situation illustrations."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVENTS = {
    'cindermaw.1': 'cindermaw',
    **{f'ga_gathering.{n}': art for n, art in {
        1: 'gathering', 2: 'harbor_pact', 3: 'oath', 4: 'oath',
        5: 'unification', 6: 'eastern_hunger', 7: 'unification',
        8: 'eastern_harbor', 10: 'cindermaw', 11: 'brackmaw',
        12: 'reefhook', 13: 'shatterfin', 14: 'sootwake', 15: 'shatterfin',
        16: 'harbor_pact', 17: 'harbor_pact', 18: 'oath',
    }.items()},
    **{f'goblins_exploration.{n}': art for n, art in {
        1: 'departure', 2: 'iberia', 3: 'charts',
        4: 'biscay', 5: 'africa', 6: 'foreign_sails',
    }.items()},
}
SITUATIONS = {'ga_gathering_of_five': 'gathering', 'ga_eastern_hunger': 'eastern_hunger'}
ART = sorted(set(EVENTS.values()) | set(SITUATIONS.values()))
EVENT_DIR = 'main_menu/gfx/interface/illustrations/event/ashborn'


def image(event_id):
    return 'gfx/interface/illustrations/event/ashborn/' + EVENTS[event_id] + '.dds'


def runtime_paths():
    return ([f'{EVENT_DIR}/{name}.dds' for name in ART]
            + [f'main_menu/gfx/interface/illustrations/situation/{name}.dds' for name in SITUATIONS]
            + [f'main_menu/gfx/interface/icons/situations/{name}.dds' for name in SITUATIONS])
