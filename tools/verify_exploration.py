"""Focused setup/contact checks against installed EU5; no terrain or install."""
import argparse
import json
import re
from pathlib import Path
import build as b
import exploration as e


def verify(game, out):
    b.build_setup(game, out)
    report = e.build(b, game, out)
    definitions = b.read(game, 'in_game/map_data/definitions.txt')
    known = set()
    for key in e.STARTING_REGIONS + e.STARTING_SEA_AREAS + e.STARTING_PROVINCES:
        start, end = b.block_span(definitions, key)
        known.update(re.findall(r'\b\w+\b', b.clean(definitions[start:end])))
    # All voyage destinations have chart visibility; distant capitals stay hidden.
    assert {loc for route in e.ROUTES.values() for loc in route['locations']} - {'strait_of_gibraltar'} <= known
    assert not {'paris', 'london', 'fez_region', 'beijing'} & known
    actions = (out/'in_game/common/on_action/goblins_exploration.txt').read_text(encoding='utf-8-sig')
    assert 'name = ga_exploration_cooldown months = 36' in actions
    assert 'NOT = { has_variable = ga_exploration_initialized }' in actions
    assert 'NOT = { has_variable = ga_exploration_pending }' in actions
    events = (out/'in_game/events/goblins_exploration.txt').read_text(encoding='utf-8-sig')
    for num in (1, 3):
        start, end = b.block_span(events, f'goblins_exploration.{num}')
        offer = events[start:end]
        assert 'discover_area' not in offer and 'discover_location' not in offer
        assert 'remove_variable = ga_exploration_pending' in offer
        assert 'name = ga_exploration_cooldown months = 6' in offer
    for route, config in e.ROUTES.items():
        assert f"id = goblins_exploration.{config['event']} months = {config['months']}" in events
        start, end = b.block_span(events, f"goblins_exploration.{config['event']}")
        arrival = events[start:end]
        assert arrival.count('limit = { exists = owner }') == len(config['locations'])
        assert arrival.count('NOT = { has_variable = ga_received_goblin_first_contact }') == len(config['locations'])
        assert f'name = ga_charted_{route} value = yes' in arrival
        assert 'name = ga_exploration_cooldown months = 12' in arrival
    assert 'lift_fog_of_war' not in actions + events
    report['checks'] = ['native map references', 'starting knowledge for all five crowns',
                        'visible voyage ports and hidden distant capitals', 'three-year initial cooldown',
                        'pending/retry guards', 'delayed owner-scoped first contact']
    (out/'exploration-audit.json').write_text(json.dumps(report, indent=2)+'\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--game', type=Path, required=True)
    parser.add_argument('--out', type=Path, default=b.ROOT/'build/exploration-check')
    args = parser.parse_args()
    print(json.dumps(verify(args.game, args.out), indent=2))
