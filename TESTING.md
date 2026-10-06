# Goblins of the Ashborn Isles 0.5.0 verification

## Build checks

- Require a fresh 0.5.0 validation report against EU5 1.3.11.
- Check 26 connected land footprints, six islands and preserved vanilla geography.
- Verify thirteen registered sea zones, connected to each other and native Atlantic lanes.
- Verify 26 settlement anchors within their own land, fleet/combat anchors and coastal ports.
- Check population totals, capital ranks, braces, law/policy IDs and monarchy succession registration.
- Validate native terrain caches and compact-package reconstruction checksums.
- Probe all six island centres from 32 directions at radius 0.0001 map units. Height spread must be at most two uint16 units (quantization); the 0.4.0 formula had jumps of 244-1596 units.
- Decode the final height cache independently at mip 2. Check above-water coverage of each location, a Cindermaw peak above 12 world units, smaller mountain-island peaks above 7, and Reefhook above 4. Peaks follow geology rather than requiring one in every administrative location.
- Inspect `Goblins_Cache_Relief.png`; this is a diagnostic of encoded terrain, not a substitute for an engine screenshot.
- Check the renamed metadata, installer, packages and 512 x 512 thumbnail.

## New-campaign playtest

Fully restart EU5. Enable only **Goblins of the Ashborn Isles** and start a new 1337 campaign; do not use an earlier save.

1. Find five goblin countries between the Azores and Portugal. Check six physical islands: Reefhook and Sootwake each have a single two-province island; Shatterfin has two islands.
2. Check populations: Cindermaw 320,117; Brackmaw 183,197; Reefhook 30,492; Shatterfin 30,819; Sootwake 29,022. Hooktooth is a city with 63,973 people; other capitals are towns.
3. Zoom into every island. Inspect coasts, mountains, craters, less-green materials, visible settlements and cache seams. Check armies and docks.

   Specifically repeat the 0.4.0 screenshots at Hooktooth/Cinder Crown and the two Shatterfin islands, at close and medium zoom. Check that the larger relief appears in geometry and not merely in texture shading. Compare with mainland mountains in the same session. If the islands still look unchanged, the rendering path remains unresolved; do not mark this build terrain-verified based on the numerical report. Verify that Graphics > Disable 3D Terrain is unchecked and compare in a terrain map mode.
4. Advance one month as Cindermaw: its opening force and introduction should appear once. Advance another month and save/reload to check they do not repeat.
5. Sail around Cindermaw through its distinct north, west and east waters and the southern channel. After exploration, sail out into the Atlantic. Dock at each island and test embarkation and landing. No sailing through land or invisible bridges.
6. Move armies over internal borders. Inspect combat terrain, buildings, construction, workers, food and market membership.
7. Test Ironfang succession, ordinary monarchy law changes, raiding and budgets for at least a year. Highest Military ability must win among eligible adult male Goblinkin; administration then age break ties. Save/reload with the rule changed and verify it stays changed.
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

## Limits

Static checks do not prove in-game rendering, pathfinding, construction or balance. Terrain uses a native cache patch, not an engine-editor export. This version awaits user playtesting. Dedicated foreign desire/fear mechanics and goblin portraits are not implemented. No Steam Workshop upload has been performed.

## Version 0.5.0 integration acceptance

- Confirm Cindermaw has 12 locations/6 provinces; Brackmaw 8/4; three minor clans still have two locations each. Population totals remain unchanged.
- Compare `feature_verification.json`: about 1.25x old land area on five islands, 1.50x on Reefhook. Reefhook is about 1.2x either small rival clan.
- In terrain mode, inspect Cindermaw across province borders: continuous rocky spine and foothills, not province-shaped surface swatches. Zoom close enough for native vegetation layers; inspect trees, rocky outcrops, shorelines and streams on every island.
- Compare native Madeira/Sao Miguel in the same session. Confirm no native island's materials changed. Review shader/parser logs for the added biome.
- Open each capital and rural location: verify appropriate village types, one/two capital guilds, wharves, and actual workers. Confirm no unsupported building IDs or missing production methods.
- Record RGO capacity before and after the first monthly pulse; it should receive the configured one-time expansion. Advance another month and save/reload: it must not be granted again.
- At months 3, 6 and 12, record income, expenses, treasury, food, prices, employment, control and market membership for all five clans. The production setup is not evidence of a positive budget by itself. Check naval-supply inputs (lumber, fiber, tar, cloth) and tools/pottery inputs before raising industry further.
- Confirm the starting force is 1 footmen unit, 2 galleys and 3 cogs after the first pulse. No repeated grants. The introduction has one option and grants nothing independently.
- Ironfang reform must be removable and Rule of the Strongest changeable. Compare eligible candidates' Military ability, exclude children/women/foreign rulers, and test an actual succession. Ordinary monarchy alternatives must remain available after the change.
