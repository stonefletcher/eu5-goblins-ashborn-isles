# 0.5.1 terrain development (source integration)

- Wider Cindermaw–Brackmaw and Brackmaw–Sootwake channels; land area reduced 12%.
- Individual coast profiles with broad bays, headlands and restrained coastal erosion.
- 15 Cindermaw, 12 Brackmaw, four Reefhook, three Shatterfin and two Sootwake playable tiles. Province groupings remain unchanged.
- National populations and total starting RGO expansion are preserved when subdividing locations.
- Wider crater bowls and raised rims; dark lava aprons, exposed rock and reduced woodland on dry volcanic ground.
- New raster checks enforce channel clearance, island continuity and playable tile size.
- Static validation passed: 36 connected land tiles, 31 coastal ports, all settlement anchors, navigable sea graph, population totals, rivers and scenery; terrain cache shared-border error is zero. Final shoreline gaps are 40.79 pixels (Cindermaw–Brackmaw) and 26.93 pixels (Brackmaw–Sootwake), up from 5.00 and 5.39.
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

