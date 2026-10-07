# 0.5.3 release acceptance status

The user confirmed visible infantry and no recurrence of the reported crash on October 6, 2026. That check is passed; the broader checks below remain useful for regressions. Package validation is performed against a fresh source export, including reconstructed terrain hashes and exact runtime overlay contents.

Check the release version **0.5.3** and enable only one copy. The 0.5.4 demographics/economy/lifespan work and 0.5.5 expansion prototype are excluded. Preserve separate saves and use a new 1337 campaign.

## 0.5.3 infantry attachment repair — user tested

Native fallback infantry were visible and did not reproduce the crash in the user's test. Custom goblin infantry are now re-enabled through the native attachment workflow: the base graph supplies the skeleton, transform and animation machine; a named shared_pose_entity attachment supplies the visible mesh. The direct root MeshType is removed.

The user confirmed on October 6, 2026 that the repaired infantry no longer crashes and appears properly. The precise engine fault is not proven, and exhaustive state coverage is not claimed. Visual refinement is deferred in issue #4: make the units less goofy while preserving this working attachment route. Continue regression checks for movement, combat and save/reload.

## 0.5.3 appearance acceptance - pending

- Inspect all five clans: rulers, family, cabinet, other courtiers, both sexes and every age. Clothing and skin must follow culture, not employer.
- Check ears and small teeth during idle and jaw movement; check female outfit fit, child coverage and single infant swaddling.
- Verify crowns/court finery are absent on Ashborn and unchanged elsewhere.
- Compare infantry height with native units; exercise idle, movement, attack and retreat.
- Inspect fresh logs for missing accessories, gene errors and texture-array failures.
- Compare compact torso proportions and mild stoop on adult men and women. Check head/hand/clothing alignment, portrait crop and preserved child growth. Exact full-body height is not certified.
- Verify the repaired graph no longer logs Invalid entity graph for any of the five clans, and that infantry are visible before accepting the fix.

# Goblins of the Ashborn Isles 0.5.3 verification

## Build checks

- Require a fresh 0.5.3 validation report against EU5 1.3.11.
- Check 36 connected land footprints, six islands and preserved vanilla geography.
- Verify thirteen registered sea zones, connected to each other and native Atlantic lanes.
- Verify 36 settlement anchors within their own land, fleet/combat anchors and coastal ports.
- Check population totals, capital ranks, braces, law/policy IDs and monarchy succession registration.
- Validate native terrain caches and compact-package reconstruction checksums.
- Probe all six island centres from 32 directions at radius 0.0001 map units. Height spread must be at most two uint16 units (quantization); the 0.4.0 formula had jumps of 244-1596 units.
- Decode the final height cache independently at mip 2. Check above-water coverage of each location, a Cindermaw peak above 12 world units, smaller mountain-island peaks above 7, and Reefhook above 4. Peaks follow geology rather than requiring one in every administrative location.
- Inspect `Goblins_Cache_Relief.png`; this is a diagnostic of encoded terrain, not a substitute for an engine screenshot.
- Check the renamed metadata, installer, packages and 512 x 512 thumbnail.

## New-campaign playtest

Fully restart EU5. Enable only **Goblins of the Ashborn Isles** and start a new 1337 campaign; do not use an earlier save.

1. Find five goblin countries between the Azores and Portugal. Check six physical islands: Reefhook has four playable tiles, Sootwake two, and Shatterfin three across two islands.
2. Check populations: Cindermaw 320,117; Brackmaw 183,197; Reefhook 30,492; Shatterfin 30,819; Sootwake 29,022. Hooktooth is a city with 63,973 people; other capitals are towns.
3. Zoom into every island. Inspect coasts, mountains, craters, less-green materials, visible settlements and cache seams. Check armies and docks.

   Specifically repeat the 0.4.0 screenshots at Hooktooth/Cinder Crown and the two Shatterfin islands, at close and medium zoom. Check that the larger relief appears in geometry and not merely in texture shading. Compare with mainland mountains in the same session. If the islands still look unchanged, the rendering path remains unresolved; do not mark this build terrain-verified based on the numerical report. Verify that Graphics > Disable 3D Terrain is unchecked and compare in a terrain map mode.
4. Advance one month as Cindermaw: its opening force and introduction should appear once. Advance another month and save/reload to check they do not repeat.
5. Sail around Cindermaw through its distinct north, west and east waters and the southern channel. After exploration, sail out into the Atlantic. Dock at each island and test embarkation and landing. No sailing through land or invisible bridges.
6. Move armies over internal borders. Inspect combat terrain, buildings, construction, workers, food and market membership.
7. Test Ironfang succession, ordinary monarchy law changes, raiding and budgets for at least a year. Highest Military ability must win among eligible adult male Ashborn; administration then age break ties. Save/reload with the rule changed and verify it stays changed.
8. Review fresh logs for invalid sea targets, mixed sea/land areas, election mismatches, missing advances, parser errors and locator errors. Compare unrelated errors against vanilla. An empty religion-modifier warning remains a known content limitation.
9. Confirm the renamed mod appears once and the previous installation is backed up outside the mod scan directory.
10. Switch to vanilla and start an unmodded campaign to confirm normal geography.

## Exploration acceptance

- In a NEW 1337 campaign, each goblin country sees only the archipelago and its thirteen waters; Portugal, France and Britain begin as terra incognita. Old saves retain old discoveries.
- At approximately the fourth monthly pulse, the first voyage offer appears. Postpone: no cost or reveal; the offer returns six months later.
- Fund the eastern voyage for 5 gold: no immediate reveal, no duplicate offer while pending. After four months the result reveals only the western Iberian route and Porto/Lisbon/Setubal.
- After twelve more months, fund a northern or southern voyage for 10 gold. Six months later, verify only the chosen coast is revealed. The other voyage remains available after the next cooldown.
- Save/reload during a voyage: it still returns once. Insufficient gold disables funding but always permits postponement. Test a smaller clan too.
- Each completed route reveals the Ashborn land and waters to the current owners of its visited ports. Confirm Portugal on the eastern route, the current northern port owners on the northern route, and Iberian/Maghrebi owners on the southern route. Unrelated countries should not be revealed by the event. Conquered ports must use their new owners. Discovery alone does not guarantee an AI invasion.

## Main development: models and culture names

- Use a fresh download of `main`, extract it and run Install-Goblins.cmd after closing EU5. This includes development model files; the published 0.5.0 ZIP does not. Current running tests are not modified automatically.
- Verify the culture group is Ashborn. Cultures should display Emberblood (Cindermaw), Brineward (Brackmaw), Reefstrider (Reefhook), Stormfang (Shatterfin) and Ashveil (Sootwake), including succession descriptions and lore.
- Inspect light and heavy infantry from each clan. Confirm short goblin anatomy and the five skin palettes, correct ground contact, sensible scale against a vanilla infantry unit, shadows, selection highlights and normal lighting.
- Check idle, walking, attack, retreat and charge. Confirm animation progresses instead of restarting each frame. Save/reload and retest movement. The death clip is exported but its game trigger remains pending; report actual casualty behavior.
- Confirm vanilla countries still use their original infantry. Cavalry and artillery crews are not converted. Portraits have a separate development pass described below. Inspect fresh logs for mesh, shader, skeleton, schematic, unit-constructor or state-machine errors.
- Rebuild art with Node, then run `python tools/prepare_main_overlay.py --game "PATH/TO/EU5/game"`. This checks native asset round trips, skinning against 51 source poses and all five palettes, and refreshes the install manifest. A normal full build also exports and verifies the models.

## Runtime limits

Static checks do not prove in-game rendering, pathfinding, construction or balance. Terrain uses a native cache patch, not an engine-editor export. This version awaits user playtesting. Dedicated foreign desire/fear mechanics are not implemented. Goblin portraits now have an unverified development pass. No Steam Workshop upload has been performed.

## Version 0.5.0 integration acceptance

- Confirm Cindermaw has 15 locations, Brackmaw 12, Reefhook four, Shatterfin three and Sootwake two; province groupings are retained. Population totals remain unchanged.
- Compare `feature_verification.json`: every island matches its normalized area target within 1.5%; land is 12% smaller than 0.5.0. Both crowded channels must exceed 24 map pixels; all other island pairs must exceed 10. Reefhook is about 1.2x either small rival clan.
- In terrain mode, inspect Cindermaw across province borders: continuous rocky spine and foothills, not province-shaped surface swatches. Zoom close enough for native vegetation layers; inspect trees, rocky outcrops, shorelines and streams on every island.
- Compare native Madeira/Sao Miguel in the same session. Confirm no native island's materials changed. Review shader/parser logs for the added biome.
- Open each capital and rural location: verify appropriate village types, one/two capital guilds, wharves, and actual workers. Confirm no unsupported building IDs or missing production methods.
- Record RGO capacity before and after the first monthly pulse; it should receive the configured one-time expansion. Advance another month and save/reload: it must not be granted again.
- At months 3, 6 and 12, record income, expenses, treasury, food, prices, employment, control and market membership for all five clans. The production setup is not evidence of a positive budget by itself. Check naval-supply inputs (lumber, fiber, tar, cloth) and tools/pottery inputs before raising industry further.
- Confirm the starting force is 1 footmen unit, 2 galleys and 3 cogs after the first pulse. No repeated grants. The introduction has one option and grants nothing independently.
- Ironfang reform must be removable and Rule of the Strongest changeable. Compare eligible candidates' Military ability, exclude children/women/foreign rulers, and test an actual succession. Ordinary monarchy alternatives must remain available after the change.

## 0.5.1 terrain integration acceptance

- Run `python tools/verify_geography.py` for district connectivity and minimum channel clearance.
- Inspect crater rims, dark lava aprons, rocky lee slopes and reduced woodland at close and middle zoom. Check moist valleys remain distinct from bare volcanic uplands.
- Sail through both widened channels and inspect the Shatterfin approach for intact vanilla sea routes.
- The source integration retains the 0.5.0 package number until the next prepared release; do not overwrite the published 0.5.0 archive. Build from source for the new terrain.


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
graph [cm_goblin_cindermaw_schematic]`, producing invisible infantry. The 0.5.3 repair candidate supplies explicit translation and the native animation-machine parameter; it requires an engine retest.


## 0.5.2 succession acceptance

- Confirm installer and mod metadata say 0.5.2; begin a new 1337 campaign.
- In SFK, inspect Tidemother Monarchy and Seniority of the Tidemothers. Jaima
  should rule and Skritcha should lead the candidate list ahead of the daughters.
- Trigger a succession in a disposable test save. Skritcha should inherit, followed
  by Morzha after a second succession if all eligible candidates remain alive.
- Test women of equal displayed age but different birthdays; the older wins.
- Exclude a high-Military male, under-18 girl, unrelated older woman, a woman
  related only through her father, a foreign ruler and a character barred from rule.
- Test a newborn of a ruling-house mother and a differently named father: the
  child should keep the mother's dynasty. Recheck her eligibility as an adult.
- Change the law and confirm the custom birth action stops; remove the reform
  and confirm the fallback law. Confirm CDM/QBR/RHK/SWK retain strongest-male law.
- Test exhausted candidates, regency and save/reload. Report the actual game
  behavior: these paths have not been certified by static tests.

All five Ashborn cultures have 16 male and 16 female name entries, six house names and six lowborn names each. Four additional royal families and 15 adult courtiers are authored. Drogg Cindermaw bears the nickname "the Stone Fletcher"; Jaima Shatterfin bears "the Mare-Mother". Cabinet appointments remain native, drawing on culture-specific names and the available court.

## 0.5.2 portrait crash-fix gate

- All five skin decals must match native 1024 x 1024 BC3/DXT5 arrays with 11 mip levels.
- Run `tools/verify_goblin_portraits.py` against the prepared 0.5.2 output and installed game. The report must pass before packaging.
- Verify the bundled archive and development overlay include the same corrected textures.
- Static validation is not an engine playtest; confirm campaign startup and portrait rendering in EU5. The reported missing land in 0.5.1 also requires a separate terrain acceptance pass.

## Companion first contact

- As Portugal, let an Ashborn eastern expedition return: confirm the islands reveal and Strange Visitors on Our Shores appears once, despite owning multiple visited ports.
- Let another clan visit Portugal: no duplicate popup. Test northern/southern routes for other current port owners, including conquered ports.
- Confirm Ashborn owners and unowned sea locations do not receive the foreign-contact event.
- Existing saves: completed voyages do not replay; a future voyage may trigger the first notification.
# Integrated 0.5.3 infantry artwork

- Fully restart after installation. Inspect infantry recruitment, levies and army cards
  for each of the five Ashborn cultures; confirm readable goblin illustrations.
- Check England and Castile retain human unit art and recruitment/stats are unchanged.
- Verify map infantry spawning and movement separately; the latest shared-pose
  attachment candidate is included and still needs engine acceptance.
- Test Portugal's companion event on the next eastern voyage return.
- Later-age infantry sharing medieval equipment artwork is expected in this first pass.
