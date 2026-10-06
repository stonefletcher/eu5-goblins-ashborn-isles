# Goblins of the Ashborn Isles 0.3.0 verification

## Build checks

- Require a fresh 0.3.0 validation report against EU5 1.3.11.
- Check 19 connected land footprints, six islands and preserved vanilla geography.
- Verify three registered sea zones, connected to each other and native Atlantic lanes.
- Verify 19 settlement anchors within their own land, fleet/combat anchors and coastal ports.
- Check population totals, capital ranks, braces, law/policy IDs and republic election registration.
- Validate native terrain caches and compact-package reconstruction checksums.
- Check the renamed metadata, installer, packages and 512×512 thumbnail.

## New-campaign playtest

Fully restart EU5. Enable only **Goblins of the Ashborn Isles** and start a new 1337 campaign; do not use an earlier save.

1. Find five goblin countries between the Azores and Portugal. Check six physical islands: Reefhook and Sootwake each have a single two-province island; Shatterfin has two islands.
2. Check populations: Cindermaw 320,117; Brackmaw 183,197; Reefhook 30,492; Shatterfin 30,819; Sootwake 29,022. Hooktooth is a city with 63,973 people; other capitals are towns.
3. Zoom into every island. Inspect coasts, mountains, craters, less-green materials, visible settlements and cache seams. Check armies and docks.
4. Advance one month as Cindermaw: its opening force and introduction should appear once. Advance another month and save/reload to check they do not repeat.
5. Sail through Cindermaw Roads, Ashborn Channel and Brackmaw Sound, then out into the Atlantic. Dock at each island and test embarkation and landing. No sailing through land or invisible bridges.
6. Move armies over internal borders. Inspect combat terrain, buildings, construction, workers, food and market membership.
7. Test captain elections, raiding under vanilla conditions and budgets for at least a year.
8. Review fresh logs for invalid sea targets, mixed sea/land areas, election mismatches, missing advances, parser errors and locator errors. Compare unrelated errors against vanilla. An empty religion-modifier warning remains a known content limitation.
9. Confirm the renamed mod appears once and the previous installation is backed up outside the mod scan directory.
10. Switch to vanilla and start an unmodded campaign to confirm normal geography.

## Limits

Static checks do not prove in-game rendering, pathfinding, construction or balance. Terrain uses a native cache patch, not an engine-editor export. This version awaits user playtesting. Dedicated foreign desire/fear mechanics and goblin portraits are not implemented. No Steam Workshop upload has been performed.
