# Cindermaw — The Ashborn Isles

A fantasy **Europa Universalis V** mod introducing five goblin countries on a newly risen volcanic archipelago in the Atlantic. Begin in **1337** with the city of Hooktooth, rival island clans, a shared faith, and ambitions that reach beyond the islands.

**Current version: 0.2.0.** Targets EU5 **1.3.11 (Pavia)**, Steam build **24187685**.

[Repository](https://github.com/stonefletcher/eu5-cindermaw)

The current demo and authored-source packages include the geographic preview, lore and testing checklist. Source-file and artwork upload to this repository is pending; the overview below documents the prepared local build.


## The islands that brought their own people

In the early 1300s, fire rose from the Atlantic. When the smoke cleared, new islands stood above the water—and goblins already walked their shores. No fleet had brought them. Whether the mountains birthed them or opened a passage from beneath the world remains disputed.

Fishing camps became villages. Mines opened in the volcanic ridges, and rival crews fought over sheltered harbors. By 1337, Hooktooth has grown into Cindermaw's capital city. Its captains now look toward the neighboring islands, and beyond them to the wealthy coasts of Europe and North Africa.

The Ashborn Isles are a fictional addition to the historical world. Their emergence and peoples are the mod's fantasy premise.

## Cindermaw

The largest island belongs to the **Cinderkin**. Its eight locations hold **320,117 people**, with **63,973** in the capital, **Hooktooth**. The capital starts as a city with a marketplace, naval-supplies guild and stockade. Cindermaw has roughly **2.66 times** the land area of the original demo.

A captains' confederation governs the country through a custom election tied to its government reform. The starting treasury is only **20 gold**. Cindermaw's opening fleet is scripted to appear once on its first monthly country pulse; its runtime behavior and affordability still need playtesting.

The volcanic interior supplies a rugged heartland, while lower coastal districts provide harbors and farmland. Uniting the archipelago is a natural opening ambition, rather than a scripted guarantee of conquest.

## Brackmaw and the smaller clans

**Brackmaw** is the principal rival: a separate country of **Brinekin**, with five locations and **183,197 people**. Its capital, **Brackhaven**, starts as a town. Brackmaw's land area is **60% of Cindermaw's**; its dimensions and position scale with changes to the main island.

Three smaller countries each control a two-island chain. Their capitals are towns, and their distinct cultures share the same wider heritage.

| Country | Culture | Capital | Rank of settlement | Population |
|---|---|---|---|---:|
| Cindermaw | Cinderkin | Hooktooth | City | 320,117 |
| Brackmaw | Brinekin | Brackhaven | Town | 183,197 |
| Reefhook Clan | Reefkin | Reefhook | Town | 30,492 |
| Shatterfin Clan | Shatterkin | Shatterfin | Town | 30,819 |
| Sootwake Clan | Sootkin | Sootwake | Town | 29,022 |

Together they occupy **eight physical islands and 19 land locations**, with **593,647 people**. Population counts are deliberately uneven and fixed in the source, so rebuilding does not reroll them. The setup includes 6,000 enslaved Cinderkin within Cindermaw's total. No vanilla population is removed.

## Goblinkin and the Hunger Below

All five cultures belong to the **Goblinkin** cultural group, speak **Cinder Tongue**, and follow **The Hunger Below**. Their shared faith remembers the fire beneath the islands and the mystery of their arrival.

A common origin has not produced a single state. Each country answers to its own captains; detailed clan diplomacy and species-specific mechanics remain future work.

## Atlantic placement and volcanic terrain

The archipelago lies **between the Azores and Portugal**, putting Portugal and Castile nearby, with France, England and the Maghreb as further coastal targets. A new navigable basin replaces part of the previously impassable Azores-Biscay ridge. Existing vanilla land and navigable sea-lane pixels are preserved.

Internal boundaries use irregular curves instead of rigid straight divisions. Every location remains connected. The terrain generator uses the same boundaries: mountain districts receive volcanic cones and crater rims, hills receive rolling relief, and flatland districts remain lower. Coastal slopes taper toward sea level.

The build patches EU5's native heightmap, material and index tile caches, including mip levels and tile borders. This addresses the original demo's reliance on an unbaked decal. It is a programmatic cache patch; **close-up rendering and combat terrain still require an in-game check**.

## Starting economy

Hooktooth provides the archipelago's new market center. Every country has an urban capital, and every physical island has a port into the connected coastal basin. The climate is oceanic and the principal food crop is wheat.

The initial demo's population and building setup was rejected because of BOM-prefixed starting-world keys. Version 0.2.0 writes setup scripts without that prefix while retaining the required localization encoding. New-campaign population display, construction access, staffing, food balance and market membership must still be verified in EU5.

## Changelog

| Version | Changes |
|---|---|
| 0.2.0 | Enlarged and relocated Cindermaw to the Atlantic; added Brackmaw and three clan chains; uneven populations, urban capitals, shared culture group and religion; curved internal borders; native terrain cache patch; setup encoding repair; lore, geographic preview and embedded thumbnail. |
| 0.1.0 | Initial single-island goblin demo, followed by playtest reports of missing population/buildings and invisible close-up terrain. |

These entries describe local builds. They do not imply Steam Workshop publication.

## Build and install

The source requires Python 3.11+, NumPy and Pillow. Build against your own installed game:

```powershell
python -m pip install -r requirements.txt
python tools/build.py --game "E:\SteamLibrary\steamapps\common\Europa Universalis V\game"
python tools/package.py
```

The builder creates the mod under `build/cindermaw_demo`, validation reports, and packaged demo/source ZIPs under `dist`. Generated game-derived overrides and caches are excluded from source control.

For the packaged demo:

1. Extract `Cindermaw_Demo_0.2.0.zip` into a writable folder and close EU5 completely.
2. Run the included `Install-Cindermaw.ps1`. It locates EU5, checks original cache hashes, reconstructs the terrain files and verifies their checksums. It backs up an existing Cindermaw installation outside the mod scan directory.
3. If discovery fails, supply `-GamePath` with your installation's `game` directory.
4. Restart EU5, enable only Cindermaw in a dedicated playset, and begin a **new 1337 campaign**.

The compact ZIP contains terrain deltas: **do not copy its unprepared mod folder directly**. Installation needs no Python and requires roughly 4 GB free for preparation plus the installed copy. It never writes to the Steam installation. For manual copying, run the installer with `-PrepareOnly` first, then place the complete prepared folder in the EU5 user-data `mod` directory.

## Testing and compatibility

Static validation and installer reconstruction passed for 0.2.0. Checks cover population totals, city/town setup, connected locations and sea access, preserved vanilla routes, island scale, script encoding and native cache integrity. **The updated build has not yet passed an in-game playtest.**

Use `TESTING.md` to check terrain at close zoom, displayed terrain tags, construction, the first monthly tick and save/reload. Small clans currently use vanilla AI behavior and have no scripted opening invasion fleet.

Other mods overriding the map or starting-world setup may conflict, including Crusader States without a compatibility build. Rebuild after game updates; the installer rejects mismatched terrain caches. Long-term balance, achievements and multiplayer remain untested.

To disable, choose a Vanilla playset, restart EU5 and use a vanilla campaign. Keep modded saves separate.

## Artwork and source

The placeholder Workshop thumbnail is embedded at **`mod/.metadata/thumbnail.png`**, beside the metadata file: **512 × 512 pixels, 525,305 bytes**, under 1 MB. Builds and installation preserve it. No Steam upload has been performed.


The geographic preview reflects the generated map. The thumbnail was created with image generation. Geometry, cultures, countries and populations are configured in `data/island.json`; `tools/archipelago.py` builds the islands and setup, and `tools/terrain_cache.py` handles native terrain tiles.

Future work includes goblin portraits, richer clan relations, invasion behavior, settlement/army locators and gameplay balancing. EU5 and its existing assets belong to Paradox.

