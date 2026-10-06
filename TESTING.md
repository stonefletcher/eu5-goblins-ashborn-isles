# Goblins of the Ashborn Isles 0.4.1 verification

## Build checks

- Require a fresh 0.4.1 validation report against EU5 1.3.11.
- Check 19 connected land footprints, six islands and preserved vanilla geography.
- Verify thirteen registered sea zones, connected to each other and native Atlantic lanes.
- Verify 19 settlement anchors within their own land, fleet/combat anchors and coastal ports.
- Check population totals, capital ranks, braces, law/policy IDs and republic election registration.
- Validate native terrain caches and compact-package reconstruction checksums.
- Probe all six island centres from 32 directions at radius 0.0001 map units. Height spread must be at most two uint16 units (quantization); the 0.4.0 formula had jumps of 244-1596 units.
- Decode the final height cache independently at mip 2. Check above-water coverage of each location and peaks above 10 world units in mountainous locations and 2.5 in hilly locations, allowing small coastal coves to taper toward the sea.
- Inspect `Goblins_Cache_Relief.png`; this is a diagnostic of encoded terrain, not a substitute for an engine screenshot.
- Check the renamed metadata, installer, packages and 512×512 thumbnail.

## New-campaign playtest

Fully restart EU5. Enable only **Goblins of the Ashborn Isles** and start a new 1337 campaign; do not use an earlier save.

1. Find five goblin countries between the Azores and Portugal. Check six physical islands: Reefhook and Sootwake each have a single two-province island; Shatterfin has two islands.
2. Check populations: Cindermaw 320,117; Brackmaw 183,197; Reefhook 30,492; Shatterfin 30,819; Sootwake 29,022. Hooktooth is a city with 63,973 people; other capitals are towns.
3. Zoom into every island. Inspect coasts, mountains, craters, less-green materials, visible settlements and cache seams. Check armies and docks.

   Specifically repeat the 0.4.0 screenshots at Hooktooth/Cinder Crown and the two Shatterfin islands, at close and medium zoom. Check that the larger relief appears in geometry and not merely in texture shading. Compare with mainland mountains in the same session. If the islands still look unchanged, the rendering path remains unresolved; do not mark this build terrain-verified based on the numerical report. Verify that Graphics > Disable 3D Terrain is unchecked and compare in a terrain map mode.
4. Advance one month as Cindermaw: its opening force and introduction should appear once. Advance another month and save/reload to check they do not repeat.
5. Sail around Cindermaw through its distinct north, west and east waters and the southern channel. After exploration, sail out into the Atlantic. Dock at each island and test embarkation and landing. No sailing through land or invisible bridges.
6. Move armies over internal borders. Inspect combat terrain, buildings, construction, workers, food and market membership.
7. Test captain elections, raiding under vanilla conditions and budgets for at least a year.
8. Review fresh logs for invalid sea targets, mixed sea/land areas, election mismatches, missing advances, parser errors and locator errors. Compare unrelated errors against vanilla. An empty religion-modifier warning remains a known content limitation.
9. Confirm the renamed mod appears once and the previous installation is backed up outside the mod scan directory.
10. Switch to vanilla and start an unmodded campaign to confirm normal geography.

## Exploration acceptance

- In a NEW 1337 campaign, each goblin country sees only the archipelago and its thirteen waters; Portugal, France and Britain begin as terra incognita. Old saves retain old discoveries.
- At approximately the fourth monthly pulse, the first voyage offer appears. Postpone: no cost or reveal; the offer returns six months later.
- Fund the eastern voyage for 5 gold: no immediate reveal, no duplicate offer while pending. After four months the result reveals only the western Iberian route and Porto/Lisbon/Setubal.
- After twelve more months, fund a northern or southern voyage for 10 gold. Six months later, verify only the chosen coast is revealed. The other voyage remains available after the next cooldown.
- Save/reload during a voyage: it still returns once. Insufficient gold disables funding but always permits postponement. Test a smaller clan too.
- European countries receive no scripted knowledge of the islands. Discovery alone does not guarantee an AI invasion.

## Limits

Static checks do not prove in-game rendering, pathfinding, construction or balance. Terrain uses a native cache patch, not an engine-editor export. This version awaits user playtesting. Dedicated foreign desire/fear mechanics and goblin portraits are not implemented. No Steam Workshop upload has been performed.
