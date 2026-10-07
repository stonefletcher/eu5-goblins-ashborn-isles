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

---

# Goblins of the Ashborn Isles 0.5.6

## Changes

- Specialized starting economies for all five kingdoms, scaled to population and local resources.
- Opening exploration delayed to 36 months, with nearby Atlantic starting charts.
- Added missing Gathering and Eastern Hunger situation panels.
- Replaced expensive completion-tooltip expansion with concise descriptions while preserving unification rules.
- Corrected unnamed Gathering modifiers.
- One Fire, Many Blades offers three five-year rewards: +5% army morale, +0.5 diplomatic reputation, or +10% army maintenance efficiency.
- Rebuilt the complete installer against the current configuration, fixing the stale terrain configuration error.

## Installation

Download Goblins_Ashborn_Isles_0.5.6.zip, extract into a new folder, close EU5 and run Install-Goblins.cmd. No earlier package is required. Enable only this mod and start a new 1337 campaign. Targets EU5 1.3.11.

## Validation

Full build and static checks passed. Clean-source preparation and isolated installation passed; all 1,644 installed files matched. Gameplay, balance, panel rendering and performance still need in-game acceptance. Crash resolution has not been confirmed.


# 0.5.6 installer repair candidate

Combines the staging economy and exploration pacing with situation layouts, concise completion tooltips, named modifiers and three Cindermaw council rewards. Rebuilds the complete installer payload against the current source configuration. New campaign required. Runtime testing pending.

# 0.5.5 — The Gathering of the Five

Complete release candidate for EU5 1.3.11. Start a new 1337 campaign. Disable the
earlier Gathering Prototype add-on: this full mod includes its content and
installs without a 0.5.4 prerequisite.

- Unite the 72 homeland districts through conquest, vassalage or senior unions
  in the Gathering of the Five, then pursue a European coastal foothold through
  Eastern Hunger.
- Seven situation actions support alliances, paid aid, voluntary submission,
  war goals and fleet preparation. Offers can be refused; conquests follow
  normal EU5 declarations, warfare and peace rules.
- Five clan introductions, expanded royal-family stories, revised ruler
  abilities and Shatterfin's maternal-house follow-up. Existing family
  relationships and succession laws are preserved.
- 323,941 additional minority-culture goblins bring the Isles to 1,618,696 people.
  All five Ashborn cultures live in every district.
- Seventeen original paintings cover all 21 authored events. Both situations
  have custom headers and icons; all five clans have matching custom flags.
- One regular installer and a matching 0.5.5 terrain/package bundle replace the
  separate prototype installation. The README is now a player guide.

In-game acceptance of the new situations, art, AI behavior and balance remains
pending. Automated checks and package verification do not establish gameplay
readiness. Earlier release notes follow.

## 0.5.5 Jaima Gathering update

Shatterfin is included in the ruler table at Jaima’s unchanged 66/58/52 ADM/DIP/MIL. Expanded The Tidemother’s Terms and new The Maternal House Endures give her two Shatterfin-only narrative events. The follow-up is scheduled 30 days after the introduction and guarded against repeats. All five kingdoms retain their introductions; total events rise from 13 to 14. Maternal seniority, family setup, situation costs and population additions are preserved. README, prototype guide and generated lore now cover her role. Static and packaging checks are separate from pending gameplay acceptance.

## 0.5.4 demographic revision

- Starting populations: Cindermaw 552,739; Brackmaw 318,463; Reefhook 108,437; Shatterfin 213,487; Sootwake 101,629. Total 1,294,755. All clans gain at least another 50% over the first 0.5.4 pass; Shatterfin is the largest smaller clan.
- Rulers start at varied ages of 27-39, with varied consort/court birthdays; their family dates preserve plausible parent ages, adult dynastic heirs, younger rulers with minor children and adult brothers, and Shatterfin maternal seniority.
- Native character auto modifier grants Ashborn goblins +15 years of life expectancy by culture, independent of country, dynasty and employment. Conditional application avoids stacking and excludes humans. Mortality remains probabilistic; combat, illness and scripted deaths remain possible.
- Starting RGO expansion scales with the additional population, reaching 387 levels. Geography, resources and buildings retain the previous 0.5.4 layout.
- Static and installer checks are separate from pending engine acceptance. Starting-population and birth-date edits require a new campaign.

The earlier 0.5.4 entries below describe the initial pass.

# 0.5.4 — Districts and Dynasties

Built on tested staging/0.5.3. EU5 1.3.11; a new 1337 campaign is required.

- 682,694 goblins, up from 593,647 (+15%, rounded to whole people). Each original population is split between two districts, with all starting population classes expanded.
- 36 → 72 inhabited locations and 15 → 30 provinces. Every original location and province is subdivided. Stable country tags, original location IDs, capitals, coastlines and thirteen sea zones remain.
- Starting building levels rise from 47 to 114: stronger capital markets, five granaries, tools/cloth/pottery guilds, rural villages, wheat windmills and smelters on iron/copper RGOs.
- Once-only, ownership-checked first-month RGO expansion rises from 70 to 160 levels across the larger map.
- New RGOs: 2 gold, 3 silver, 2 dyes, 2 saffron, 1 silk, 1 pearls and 2 alum. New food/timber/material districts support basic demand; original districts retain their resources. Native gold ID: goods_gold.
- Ironfang: strongest eligible adult Ashborn man within the ruling dynasty inherits. Military ability decides, with Administration and age breaking ties. Unrelated courtiers cannot inherit through this law; no eligible dynasty member means no eligible heir.
- Native country naming follows the reigning house after a takeover or dynasty reassignment; succession hooks and monthly reconciliation cover changes. Regents do not rename the country. Shatterfin keeps maternal seniority.
- Retains 0.5.3 human portrait isolation, working shared-pose infantry, recruitment art and first-contact events.

Installed Europe reference medians: 520 map pixels/location, 2,626 pixels/province and 5 locations/province. The new districts use this spatial scale as a reference while preserving the islands' smaller political units.

Volcanic/hydrothermal seams explain gold, silver and alum; reeds/lichens supply dyes; drained sheltered volcanic plots grow saffron. Knifeback has a small cultivated silk grove and Reefhook has pearl-diving grounds. These are fictional resources appropriate to the setting.

Extra production capacity is not guaranteed profitability. Food, employment, balance and succession require gameplay acceptance. Use only a verified matching 0.5.4 installer; older instructions below refer to earlier releases.

## 0.5.3 companion first-contact event

Owners of ports visited by an Ashborn expedition now receive Strange Visitors on Our Shores when reciprocal discovery occurs. Strange creatures flee the shore and a scout ship follows them to the islands. Each non-Ashborn nation receives the event once across all clans and voyage routes. Already-completed voyages are not replayed. Static checks only; in-game testing pending.

## 0.5.3 infantry attachment repair — user tested

Native fallback infantry were visible and did not reproduce the crash in the user's test. Custom goblin infantry are now re-enabled through the native attachment workflow: the base graph supplies the skeleton, transform and animation machine; a named shared_pose_entity attachment supplies the visible mesh. The direct root MeshType is removed.

The user confirmed on October 6, 2026 that the repaired infantry no longer crashes and appears properly. The precise engine fault is not proven, and exhaustive state coverage is not claimed. Visual refinement is deferred in issue #4: make the units less goofy while preserving this working attachment route. Continue regression checks for movement, combat and save/reload.

## 0.5.3 development: rough-clad goblins

Portrait refinement: ears now extend 9 cm from their base (previously 5.8), with longer hooked noses, smaller jaws/chins, prominent cheeks, wider mouths and smaller teeth. A culture-only special gene applies compact torso proportions and a mild stoop to adult males and females, fading out during childhood. Human cultures remain outside these modifiers. Exact stature, portrait framing and clothing fit await engine review.

Infantry repair candidate: connect the missing translation input explicitly, consume the native CustomAnimationMachineName parameter, and write graphics scripts with a UTF-8 BOM. Typed graph-link checks now complement mesh/animation validation. The prior graph was rejected in the game log; the subsequent shared-pose attachment repair has now passed the user's visibility/crash test.

First art pass on a separate branch based on 0.5.2. Infantry stature is reduced from 1.12 m to 0.92 m, jaws are narrower and teeth smaller. Clan skin palettes are muted olive, marsh, lichen, slate and soot greens. Portrait recoloring retains 12% of underlying albedo detail.

Portraits select native plain harnesses, wraps, jackets and overcoats for both sexes and all Ashborn cultures, including rulers and courts. Crowns, normal court clothes, capes and neck ornaments are overridden. Children retain basic clothes and infants retain a single native swaddle.

Static model, animation, texture, rig and clothing-reference checks pass. In-game appearance remains unverified. Exact full-body stature and custom torn/patchwork leather-and-rag art remain pending. This branch includes a prepared 0.5.3 installer. Download a fresh branch ZIP, extract it into a new folder and run Install-Goblins.cmd with EU5 closed. In-game art acceptance and Workshop publication remain separate.

## 0.5.2 portrait fix integration

- Includes the 0.5.1 portrait decal correction: 1024 x 1024 BC3 textures with all 11 mip levels, matching native portrait arrays.
- Validates texture dimensions, format, mip count, payload size and native headers during the build.
- Rejects a bundled installer whose version or terrain configuration does not match the source.
- In-game succession, portrait rendering and terrain acceptance remain pending.

## 0.5.2 â€” Shatterfin Tidemothers (feature branch)

Shatterfin alone starts with **Tidemother Monarchy** and **Seniority of the
Tidemothers**. Normal monarchy institutions and the existing naval modifiers
remain. The oldest eligible adult Stormfang woman of the ruling dynasty inherits;
her mother must belong to that same dynasty. Age is measured to the day, with no
Military or administrative score. Men, minors, foreign rulers and blocked
characters are excluded. This is maternal dynastic seniority, not daughter-first
primogeniture or an election. The law can be changed through normal monarchy
controls; removing the reform falls back to absolute cognatic primogeniture.

**Jaima Shatterfin, the Mare-Mother** begins as Tidemother. Her younger sister **Skritcha** is the
oldest eligible successor, followed by Morzha, Rikkra and Krishka. Vrosh is excluded
because he is male despite his high Military ability; Zrikka is too young. The
family is authored parent-before-child, with a deceased maternal founder, Zhavra.
Children born in Shatterfin to women of the ruling house inherit their mother's
dynasty while the law is active. The birth action is restricted to Shatterfin and
this law. Other clans retain Ironfang Monarchy and Rule of the Strongest.

If no eligible adult woman survives, the rule does not silently admit a man or
an unrelated woman. The engine's handling of an exhausted candidate list needs
in-game testing. Existing campaigns are not forcibly migrated: use a new 1337
campaign for the authored dynasty and government setup.

This branch includes the 0.5.1 terrain source and the portrait test pass. Its
prepared installer and metadata are **0.5.2**. The branch remains separate from
main; the published 0.5.0 release is unchanged. Static setup and build checks do
not certify in-game succession, maternal inheritance or portrait rendering.

# 0.5.1 terrain development (source integration)

- Wider CindermawÃ¢â‚¬â€œBrackmaw and BrackmawÃ¢â‚¬â€œSootwake channels; land area reduced 12%.
- Individual coast profiles with broad bays, headlands and restrained coastal erosion.
- 15 Cindermaw, 12 Brackmaw, four Reefhook, three Shatterfin and two Sootwake playable tiles. Province groupings remain unchanged.
- National populations and total starting RGO expansion are preserved when subdividing locations.
- Wider crater bowls and raised rims; dark lava aprons, exposed rock and reduced woodland on dry volcanic ground.
- New raster checks enforce channel clearance, island continuity and playable tile size.
- Static validation passed: 36 connected land tiles, 31 coastal ports, all settlement anchors, navigable sea graph, population totals, rivers and scenery; terrain cache shared-border error is zero. Final shoreline gaps are 40.79 pixels (CindermawÃ¢â‚¬â€œBrackmaw) and 26.93 pixels (BrackmawÃ¢â‚¬â€œSootwake), up from 5.00 and 5.39.
- Full game rendering and navigation acceptance require a new campaign. Published archives and existing installations are unchanged; build from source to test this terrain pass.

---
# Development on main after 0.5.0

- Merged the release and goblin-model art branches into main. Code > Download ZIP now reconstructs the prepared release and applies checked development files.
- Added five native goblin infantry variants, materials, clan graphics selection and 17 animation exports. Idle, movement, attack, retreat and charge are wired; engine rendering and death-event integration remain pending. Cavalry and equipment fitting need separate work. The portrait test pass is documented below.
- Renamed the shared culture group to Ashborn, with Emberblood, Brineward, Reefstrider, Stormfang and Ashveil cultures. Technical IDs are preserved.
- Native checks cover 51 source/engine pose comparisons, palettes, graphics references and exact native asset round trips. The main-download installer preparation path was tested.
- The published 0.5.0 archives and currently installed games are unchanged. Use a fresh main download to test the development additions.

# Goblins of the Ashborn Isles 0.5.0 - Ironfang Isles

For **Europa Universalis V 1.3.11 (Pavia)**. **Close the game, install, and start a NEW 1337 campaign.** Earlier saves are incompatible with the expanded location map.

- Every island gains approximately 25% land area. Reefhook gains extra land and is about 20% larger than either smaller rival clan. Native land and navigable sea lanes are preserved.
- Cindermaw now has 12 locations in 6 provinces; Brackmaw has 8 in 4. The smaller clans retain two locations each. National population totals remain unchanged.
- Terrain follows continuous island geology: Cindermaw's mountain spine, irregular foothills, craters, eroded valleys, beaches, woodland, exposed rock and short rivers. Ground materials no longer change at administrative borders. Native tree and rock meshes add visible scenery to all six islands.
- All five clans use **Ironfang Monarchy**, a unique reform with native monarchy mechanics. **Rule of the Strongest** selects an eligible adult male Goblinkin by Military ability, with administration and age breaking ties. The rule can be changed; removing the reform restores ordinary succession if necessary.
- Voyages now reveal the Ashborn Isles to the current owners of the ports the goblins visit. Unrelated countries receive no scripted reveal.
- Every clan starts with modest capital industry and developed rural settlements: 27 village levels, two fiber-crop farms, and seven capital guilds. New clay, tar, fiber and wool sites supply production. A one-time first-month initialization adds 70 RGO capacity levels.
- The old 15% tax-income penalty is removed. Cindermaw's first-month force is reduced to 1 footmen unit, 2 galleys and 3 cogs. Starting treasuries and development receive modest increases; unnecessary stockades in minor capitals are removed.
- The introductory lore event now has one **The Ashborn rise.** button. Its former two options had identical gameplay results.

## Installation

Download **Goblins_Ashborn_Isles_0.5.0.zip**, extract it, close EU5 and run **Install-Goblins.cmd**. Enable only this mod for the first test and start a new campaign. The installer checks the game version through terrain hashes and backs up the prior mod outside the mod scan folder. Steam's game files are not edited.

The source package contains authored code and assets. Building requires a local EU5 installation, Python, NumPy and Pillow. See README.md and TESTING.md.

## Verification and remaining tests

The release includes static build, map, terrain and feature reports. Checks cover map connectivity, ports, untouched native geography, population totals, script references, terrain tile seams, height coverage, area ratios, river paths, scenery placement, province-independent terrain, reciprocal discovery and guarded RGO initialization. ZIP integrity and terrain reconstruction hashes are checked before publication.

**This is a test release.** The new visual biome must still be checked in the engine. Succession, reciprocal discovery and actual monthly budgets require playtesting; increased production is not a claim of a measured positive balance. Other terrain shaders or map/startup mods can conflict. See TESTING.md for focused acceptance steps.

No Steam Workshop publication is included.


## Culture-based portrait test pass (main only)

All five Ashborn cultures now select their own portrait ethnicity and deterministic
appearance modifier. The rules follow the character's culture, not their employer,
country, sex, or office. This targets ruling families, cabinet members, other
characters and culture-generated population portraits. Existing character DNA gets
the visible modifiers without a save-edit migration. Newly generated DNA also uses
the culture's ethnicity. Human cultures receive none of these modifiers.

The pass uses the native animated portrait faces and clothing, with custom rigged
pointed ears, jaw-bound tusks, goblin facial proportions, and matching head/body skin
colour. It does not reuse the infantry's whole-body mesh as a portrait. Adult male,
adult female, boy, girl, both adolescent types and infant are configured; infants
have smaller ears without tusks. Clan colours match the infantry art palette.

**Status: static checks passed; in-game appearance has not been verified.** Native
rig bindings, skin weights, geometry, asset references, all seven portrait types,
and all five culture routes are checked by `tools/verify_goblin_portraits.py`.
Clothing fit, expressions, child scaling and population portrait selection still
need a game test. Restart EU5 after installing a fresh main download; the published
0.5.0 ZIP does not contain this pass. Compare a ruler, relative, cabinet member,
woman, child and infant from each culture, plus a human character as a control.
Check skin on neck/hands, eyes, ear placement, tusks during animation, save/reload,
and a newly generated character. Send a screenshot and fresh error.log if wrong.

The separate infantry integration currently fails in-game with `Invalid entity
graph [cm_goblin_cindermaw_schematic]`, producing invisible infantry. Its repair is
deferred while portraits are prioritised; this portrait pass does not claim to fix it.


All five Ashborn cultures have 16 male and 16 female name entries, six house names and six lowborn names each. Four additional royal families and 15 adult courtiers are authored. Drogg Cindermaw bears the nickname "the Stone Fletcher"; Jaima Shatterfin bears "the Mare-Mother". Cabinet appointments remain native, drawing on culture-specific names and the available court.
# 0.5.3 integrated infantry illustrations

- Original goblin regiment artwork for all five Ashborn cultures, including levies.
- Preserves native recruitment, stats and human artwork; no custom regiments required.
- Includes the latest shared-pose infantry attachment repair and companion contact event.
- One medieval painting is shared across infantry types and ages in this first pass.
- Prepared installer updated and checksum-verified; in-game acceptance pending.
