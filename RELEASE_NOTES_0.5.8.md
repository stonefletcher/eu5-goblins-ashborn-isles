# Goblins of the Ashborn Isles 0.5.8 — Portrait revision and holy-site variety

## Latest Drogg and hair correction

The latest screenshot shows Drogg's new crest layered over his long hairstyle.
The previous code added a custom hair accessory gene while the original native
hair was still active. This correction removes the separate hair gene and uses
the native historical-character pattern: mode replace on hair_styles, an explicit
accessory selection and a higher-priority modifier.

- Six equal male court choices: short curls, short swept hair, close curls,
  close textured crop, short straight hair and shaved. Five equal female choices:
  two pulled-back braids, parted hair, wrapped braids and a close textured crop.
- Weighted-random native selection replaces the old 50%-mohawk accessory pool.
  Weights control selection probabilities, not guaranteed exact court counts.
- Children use age-appropriate hair choices; no hairstyle is forced on infants.
- Drogg alone has a priority-140 modifier guarded by his existing cm_cdm_ruler
  ID and goblin culture. He gets a signature crest without the second hair layer,
  more restrained nose projection, firm jaw, less bulky head proportions and
  a cosmetic battle scar. No character stats, IDs, relationships or health traits
  change. Existing-save application requires engine confirmation.
- Shared ear/face skin, weathering, leather/hide/fur clothes and other goblins'
  facial ranges are preserved. No native assets are copied into the mod.

## Validation and game review

Native assets and modifiers are checked against EU5 1.3.11. Regression checks
reject the extra hair gene, require native replace operations, check adult pool
variety/weights and ensure only Drogg receives the named face/scar override.
Full build, archive and clean installation results are recorded in HANDOFF.md.
These checks do not establish in-game appearance.

After installing and restarting, check Drogg from front and three-quarter views:
one crest, no long hair beneath it, scar placement and facial expressions. Inspect
at least a dozen men and women in court, then save/reload to check hairstyle
stability. Repetition is possible with random selection, but the old heavily
favoured crest is reserved for Drogg. Review children, infants and a human ruler;
compare an existing save with a new campaign. In-game acceptance remains pending.

## Holy-site variety

Nine shrines replace the uniform one-per-island pattern: three on Cindermaw,
two on Brackmaw, one on each smaller island. Importance now spans 1-5.
Adds Blackwood Oathstones, Ashfield Hearth and Miregrove Witness, with local
lore and modest bonuses. Existing site IDs and event links are preserved.
Static validation passed; fresh-campaign gameplay review is pending.
