# Goblins of the Ashborn Isles 0.5.8 — Portraits and holy-site variety

Staging candidate, incorporating the completed 0.5.7 release at b4940c7.
Not a Steam release and not installed into the active game profile.

## Portrait changes

- Replace the flat ear fans with closed, cupped ears: recessed bowls, raised rims,
  smooth normals, swept tips and subtle left/right differences. Retain native
  skeleton bindings and the working shared-pose attachment route.
- Replace oversized eyes and broad mouths with smaller, recessed, hooded eyes,
  stronger brows, lean cheeks and restrained mouths. Keep hooked noses without
  combining maximum nose length, maximum projection and minimum jaw size.
- Use 94% clan skin tint, with native normal detail and ageing retained. Ears
  share the head skin shader, decal routing and palette.
- Shorter necks; compact torso strength 0.32 to 0.42 and stoop 0.18 to 0.24.
  These are rig parameters, not measured height in metres. Female height poses
  remain unsupported, so no disabled height attribute is introduced.
- Remove detached external fangs; keep native animated mouth teeth. Remove
  native beards to expose goblin facial anatomy.
- Replace the mixed adult cloth wardrobe entirely with inspected native hide
  tunics, fringed leather overcoats and fur-trimmed hunter garments. No Chinese,
  German jacket, Aztec wrap or Syrian scarf-dress entries remain in the adult
  selection. Children retain fitted plain garments and infants retain swaddling.
  Custom torn-leather geometry remains future work.
- Apply by goblin culture to court members, nobles, relatives and generated
  characters, preserving human appearance and unrelated individual DNA.
- Keep infant skin/ears separate from adult teeth and compact-body treatment;
  native child ageing still controls the adult facial morphs.

## Validation and visual acceptance

Static checks cover all five cultures and seven portrait age/sex types, native
rig transforms and clothing references, DDS array compatibility, finite mesh
data, normalized normals/weights and closed consistently wound ear shells.
Full build and clean-source installer checks are recorded in HANDOFF.md.

No in-game visual acceptance is claimed. Review the court, noble/estate and
character views at their normal small size and in close-up: men, women,
children, adolescents, infants and elders from all five cultures; an existing
save and newly generated characters; a human ruler as a negative control.
Check blink/talk/idle poses, ear roots and lighting, teeth/lip clipping, neck
and hand colour seams, hair overlap, clothing fit and portrait framing.

The reference is art/events/sources/gathering.png. Judge whether the faces read
as weathered, ugly goblins with short adult proportions. A technical mesh
preview is not a screenshot of the engine result.

## Inherited 0.5.7 changes

Retains the Ashen Covenant religion and goblin estate names, homeland-only
starting land discovery, delayed voyages, Harbor Pact response notifications,
Ashen Compact refusal notifications and removal of AI custom Harbor Pact spam.
New campaigns are required for inherited starting-world/discovery changes.
Portrait modifiers should also affect existing culture-matched characters;
verify this in a saved game rather than assuming the engine refreshes every view.

## Holy-site variety

Nine shrines replace the uniform one-per-island pattern: three on Cindermaw,
two on Brackmaw, one on each smaller island. Importance now spans 1-5.
Adds Blackwood Oathstones, Ashfield Hearth and Miregrove Witness, with local
lore and modest bonuses. Existing site IDs and event links are preserved.
Static validation passed; fresh-campaign gameplay review is pending.
