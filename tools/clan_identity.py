"""Shared authored identities for full builds and the small prototype add-on."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {'CDM': 'cindermaw', 'QBR': 'brackmaw', 'RHK': 'reefhook', 'SWK': 'sootwake'}
PROFILES = {tag: json.loads((ROOT / 'data' / (name + '.json')).read_text(encoding='utf-8'))
            for tag, name in SOURCES.items()}
CULTURES = {'CDM': 'cm_cinderkin', 'QBR': 'cm_brinekin', 'RHK': 'cm_reefkin', 'SWK': 'cm_sootkin'}
NAMES = {'CDM': 'Cindermaw — Emberblood', 'QBR': 'Brackmaw — Brineward', 'RHK': 'Reefhook — Reefstrider', 'SWK': 'Sootwake — Ashveil'}


def lore_sections():
    return ''.join('\n## ' + NAMES[tag] + '\n\n' + '\n\n'.join(
        profile[key] for key in ('ruler_story', 'dynasty_story', 'nation_story', 'ambition_story') if key in profile) + '\n'
        for tag, profile in PROFILES.items())
