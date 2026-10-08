"""Founding crowns: derive shared eligibility from authored country setup."""
import json
from pathlib import Path

COUNTRIES = json.loads((Path(__file__).resolve().parents[1] / 'data/island.json').read_text(encoding='utf-8-sig'))['countries']
TAGS = tuple(c['tag'] for c in COUNTRIES)
CULTURES = tuple(c['culture'] for c in COUNTRIES)
