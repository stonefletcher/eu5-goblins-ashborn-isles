"""Fixed, seeded additions: never replace a homeland population or class."""
from decimal import Decimal
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def additions():
    return json.loads((ROOT / 'data/mixed_populations.json').read_text(encoding='utf-8'))['locations']

def extra(location):
    return sum((Decimal(str(p['size'])) for p in additions().get(location, [])), Decimal(0))

def rows(location):
    return [f' define_pop = {{ type = {p["type"]} size = {Decimal(str(p["size"])):.3f} culture = {p["culture"]} religion = cm_hunger_below }}'
            for p in additions().get(location, [])]
