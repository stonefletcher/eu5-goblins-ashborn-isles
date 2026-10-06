# Unreleased terrain pass (branch based on 0.5.0)

- Wider Cindermaw–Brackmaw and Brackmaw–Sootwake channels; land area reduced 12%.
- Individual coast profiles with broad bays, headlands and restrained coastal erosion.
- 15 Cindermaw, 12 Brackmaw, four Reefhook, three Shatterfin and two Sootwake playable tiles. Province groupings remain unchanged.
- National populations and total starting RGO expansion are preserved when subdividing locations.
- Wider crater bowls and raised rims; dark lava aprons, exposed rock and reduced woodland on dry volcanic ground.
- New raster checks enforce channel clearance, island continuity and playable tile size.
- Static validation passed: 36 connected land tiles, 31 coastal ports, all settlement anchors, navigable sea graph, population totals, rivers and scenery; terrain cache shared-border error is zero. Final shoreline gaps are 40.79 pixels (Cindermaw–Brackmaw) and 26.93 pixels (Brackmaw–Sootwake), up from 5.00 and 5.39.
- Full game rendering and navigation acceptance require a new campaign. This branch is not published or installed automatically.

---

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
