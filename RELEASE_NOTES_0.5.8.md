# Goblins of the Ashborn Isles 0.5.8 — Portrait revision and holy-site variety

## Latest portrait refinement

The user confirms the previous skin/ear/clothing pass looks better. New screenshots
show Drogg with a high rounded forehead and long smooth hair, while all three
rulers still have overly smooth faces. This revision targets that evidence.

- Lower, flatter foreheads and slightly shorter, broader heads.
- Firmer jaws/chins without broad orc jaws; less exaggerated nose length and
  projection; slightly lower mouth corners while retaining individual variation.
- Culture-scoped adult hair selection: mohawks, short curly crops and short
  swept hair for men; tied-back braids for women. Long court hair, balding bobs
  and wigs are excluded from the adult male pool, including Drogg's selection.
- Subtle native early-age brow, eye and mouth diffuse/normal detail applied
  after the strong clan tint. Strength varies and fades in between 18 and 30;
  children, adolescents and infants have empty weathering definitions. Ordinary
  ageing remains active; no disease or scar traits are assigned.
- Ear UVs sample a transparent corner of these detail maps, preventing facial
  creases from appearing on ears. Shared skin rendering and clan tint remain.
- Preserve cupped swept ears, compact posture, shorter necks, native animated
  teeth, adult leather/hide/fur clothing and fitted child clothes.

## Evidence and validation

The previous attachment/skin shader mismatch is corrected. The new user
screenshots support improved colour matching and clothing; they do not verify
this newer forehead, hair or weathering candidate. Native gene definitions,
sex-specific texture references, fitted hair accessories and mesh bindings are
checked against EU5 1.3.11. No game-derived textures are redistributed.

Regression checks cover all five cultures and seven portrait types, native
rigs, closed ear meshes, DDS format, palette/decal routing, material channels,
wardrobe/hair suppression, empty child weathering and transparent ear sampling.
Full build and matching clean-download/isolated-install results are recorded
in HANDOFF.md. Gameplay acceptance remains pending.

## In-game review

Install this refreshed 0.5.8 package with EU5 closed and fully restart. Check
Drogg first: forehead height, jaw weight and replacement of his long hair.
Compare Jaima and Murgash under the same light. Check variation across nobles,
sexes and clans; weathering should be subtle, ears should keep matching skin,
and hair should not obscure or clip ears. Check older adults, children, infants
and a human ruler. Review blink/talk/idle poses and both existing-save portrait
refresh and a new 1337 campaign. The portrait changes do not alter character
IDs, relationships, stats or health traits. Active profiles and Steam are not
modified by this staging preparation.

## Holy-site variety

Nine shrines replace the uniform one-per-island pattern: three on Cindermaw,
two on Brackmaw, one on each smaller island. Importance now spans 1-5.
Adds Blackwood Oathstones, Ashfield Hearth and Miregrove Witness, with local
lore and modest bonuses. Existing site IDs and event links are preserved.
Static validation passed; fresh-campaign gameplay review is pending.
