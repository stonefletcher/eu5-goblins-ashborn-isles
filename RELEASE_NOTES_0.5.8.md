# Goblins of the Ashborn Isles 0.5.8 — Portrait revision and holy-site variety

## Changes

- Ears now use the native portrait skin shader, skin palette, head-decal routing
  and skin scattering. Previously they used the attachment shader and a fixed
  clan texture, bypassing the face's skin-colour and lighting stages.
- Increase the shared head/torso/ear clan tint from 60% to 94%. This reduces
  inherited skin-colour differences and the pale-face/coloured-ear split.
  Native facial normal maps, ageing and facial morphology remain active.
- Use a neutral ear base with native RRxG normal packing, non-metallic rough
  skin properties and an explicit ambient-occlusion texture slot.
- Shorter, more upward-swept ears retain the cupped, rounded, closed geometry.
- Remove the separate external tusks that appeared as white dots beside the
  lips. The native animated mouth retains its own teeth.
- Stronger hooked noses, brow projection and lean cheek definition, retaining
  individual variation, hooded eyes, shorter necks and compact posture.
- Replace zero-strength outfit replacements with the native add-template
  suppression pattern and move the outfit modifier to priority 120. Clear
  clothes, hats, capes, neckwear and beards before applying the hide wardrobe.
  This addresses the formal hat/robe combinations shown in the screenshots;
  successful suppression still needs an engine test.
- Adults select native hide tunics, fringed leather overcoats and fur-trimmed
  hunter garments. Children retain fitted plain clothes; infants retain native
  swaddling. No adult clothing meshes are forced onto child bodies.
- All five goblin cultures remain covered; no global human skin or outfit
  definitions are replaced. Inherited 0.5.7 content and the working infantry
  pipeline are retained.

## Evidence and validation

The supplied screenshots show pale/green faces, blue-green ears, external tooth
studs and formal hats/clothing. The active Goblins playset used the local 0.5.8
copy, whose outfit modifier matched staging. No duplicate goblin copy was enabled
in that playset.

The shader mismatch is verified in the installed game source: PS_attachment
bypasses the palette/head decals and lacks the skin scattering define; PS_skin
applies them. Native beard suppression supplies an empty accessory template with
mode add and a selection range, unlike the old zero-strength replacements.
These findings explain plausible causes; the revised look is not engine-verified.

Checks cover native rigs, all seven portrait types, five cultures, watertight
ear shells, normals/weights, DDS format, skin shader/decal routing, material
channels, opacity and wardrobe suppression syntax. Full build, archive and clean
installation gate results are recorded in HANDOFF.md.

## In-game review

Fully restart EU5 after installing this newer 0.5.8 candidate. Enable one copy.
Review the same characters from the screenshots, including Murgash, plus women,
elders and generated nobles from all five cultures. Check ear/face/neck/hand
colour under the same portrait lighting, missing tooth studs, blink/talk/idle
poses, ear attachment at the root, hats/capes/beards and hide outfit selection.
Check children and infants separately and a human ruler as a negative control.

Compare an existing save with a new 1337 campaign. Existing portrait/DNA refresh
and every GUI's outfit selection need actual game confirmation. No game launch,
active-profile installation or Steam release was performed for this revision.

## Holy-site variety

Nine shrines replace the uniform one-per-island pattern: three on Cindermaw,
two on Brackmaw, one on each smaller island. Importance now spans 1-5.
Adds Blackwood Oathstones, Ashfield Hearth and Miregrove Witness, with local
lore and modest bonuses. Existing site IDs and event links are preserved.
Static validation passed; fresh-campaign gameplay review is pending.
