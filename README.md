# Cindermaw — Goblin Invasion Demo

Version **0.1.0**, built against EU5 **1.3.11**, Steam build **24187685**.

**Development demo: generated and statically validated, not yet tested in EU5.**
The island terrain is authored as a terrain decal. The terrain cache has not been baked in the map editor. Do not treat this package as a verified playable release until the checks in `TESTING.md` pass.

## What is implemented

- Eight entirely new land locations northeast of northern Madagascar, south of the Seychelles.
- Three provinces in a new Cindermaw area within the existing Madagascar region.
- A volcanic northern interior, forested shipbuilding districts, food-producing lowlands, and three ports.
- Cindermaw (`CDM`), a new playable-country definition with Hooktooth as capital.
- Cinderkin culture, Goblin culture group, Cinder Tongue language and fictional name pools.
- The Hunger Below religion with its own religious group.
- A captains' republic with a custom election derived from the game's pirate election.
- Native privateering and slave-raiding permissions, plus eligibility for anti-piracy retaliation.
- **200,000 starting people**, including **6,000 enslaved Cinderkin** from the island's earlier clan wars. No existing people are removed from vanilla countries.
- **20 starting gold**, a 15% tax-income-efficiency penalty, one town and otherwise rural territory.
- Iron, copper, lumber, fish, millet, salt and livestock.
- A local market at Hooktooth, with a marketplace, naval-supplies guild and stockade.
- A one-time monthly initialization that creates four traditional galleys, eight cogs and two footmen sub-units, followed by an introductory event.
- A black, red and yellow pirate flag using existing game emblems.

The first event is an introduction with two guidance choices, not a branching reward system. It does not automatically declare a war or grant additional gold. The fleet arrives on the first country monthly pulse after starting the campaign; check again after advancing into the next month.

## Deliberately unfinished

- Goblin models, green skin and custom anatomy: characters currently use human placeholder graphics.
- A biological species system: Goblin is presently represented through culture. Human/goblin assimilation and inheritance are not separately modeled.
- Detailed captain loyalty, eruption events, captive-management choices and reform paths.
- A later-date surprise invasion mode or scripted AI invasion. Vanilla's slave-raiding casus belli is AI-disabled; enabling its mechanics does not guarantee the AI will launch raids.
- In-game budget and fleet-maintenance balancing. Starting gold and populations are specified, but actual monthly profit is unmeasured.
- Terrain-cache baking, spline/locator verification, engine logs, save/reload, naval movement and combat tests.

## Install the generated test build

1. Extract the ZIP. Close EU5.
2. Copy the complete `cindermaw_demo` folder, including `.metadata`, into your actual Documents folder under `Paradox Interactive/Europa Universalis V/mod/`.
3. Alternatively, run the included `Install-Cindermaw.ps1` in PowerShell. It discovers the Windows Documents folder, installs only this mod, and preserves an existing Cindermaw install as a dated backup. It does not edit the Steam installation or playsets.
4. In EU5, create a separate test playset containing **only** Cindermaw. Start a **new** 1337 campaign and look northeast of northern Madagascar.
5. Follow `TESTING.md`. Existing saves do not test this starting-world setup.

To disable, switch to a playset without Cindermaw. Keep demo saves separate. The Jerusalem mod is not modified by this project; running both together is not supported yet because some generated override paths overlap.

This session only built the package in its writable workspace. It did not install into your Documents mod folder or launch EU5.

## Rebuild from source

Use Python 3.11+ with Pillow and NumPy:

```powershell
python -m pip install -r requirements.txt
python tools/build.py --game "E:\SteamLibrary\steamapps\common\Europa Universalis V\game"
python tools/package.py
```

Change `--game` for another Steam library. The builder reads vanilla files and writes only into this project's `build/` folder. It does not modify the installed game. Build into a fresh extracted project for each release so obsolete generated files cannot carry forward.

`data/island.json` controls location seeds, resources, population and island position. `mod/` contains authored gameplay definitions. `tools/build.py` applies narrowly scoped additions to required full-file overrides and creates the map layer. `build/reports/validation.json` records checks and source hashes.

Authored sources belong in Git; generated map overrides and vanilla-derived assets do not. The local development snapshot is committed in Git. The source ZIP excludes `.git`, generated outputs, machine-specific settings and game assets.

## Map implementation notes

The location map is 16384 × 8192. The heightmap file directly under `gfx/terrain2/` is not the complete playable-world terrain in this installation; the real world is assembled from tiled decals. Cindermaw uses a new 1024 × 1024 terrain decal, placed with the existing terrain instance format. Its world coordinates are four times location-map coordinates, with inverted Y. Its coastline comes from the same mask as the playable map.

The new instance and decal definition are supplied, but whether the game regenerates all necessary cache data on load remains unverified. If it loads the terrain from the vanilla cache, the new land may still appear underwater in 3D until an editor bake is exported into this mod. Do not delete or overwrite the original game's terrain cache.

Map modifications also require checking navigation nodes, city/army locators and spline networks. This build does not ship newly engine-generated versions of those data sets. Their generation and verification are part of the next in-game milestone.

The entire `locations.png`, `rivers.png`, geographic definitions, location templates, ports, terrain decal definitions, and selected setup files are generated overrides. Other mods changing the same paths need a compatibility build. Rebuild and retest after game updates.
