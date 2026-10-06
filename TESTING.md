# Cindermaw 0.2 verification

## Static checks

- Setup scripts have no UTF-8 BOM; localization retains BOM.
- All original population, country, city, market and geographic lines remain in order.
- 19 land locations have one connected footprint each; locations on each island connect over land.
- Every island has a port into one connected coastal basin, itself bordering vanilla navigable sea locations.
- Only the existing impassable ocean area is repainted. Existing land and sea lanes remain unchanged.
- Brackmaw rasterized land area is within 1% of 60% of Cindermaw; dimensions and offsets derive from the main radius.
- Each country owns exactly its assigned locations and has a valid capital, culture and shared religion.
- Population totals use decimal arithmetic: CDM 320,117; QBR 183,197; RHK 30,492; SFK 30,819; SWK 29,022; total 593,647, including 6K enslaved Cinderkin.
- Hooktooth is explicitly city rank; the other capitals are towns. Every capital has a port.
- Native terrain-cache tile indexes parse, appended PNGs decode, island samples are above sea level, and unmodified tile pixels are preserved.
- Compact-package reconstruction is checked against the fully assembled build.

## New-campaign playtest

Fully exit and restart EU5 after installation. Use only Cindermaw in a dedicated playset. Do not load a 0.1 save.

1. Select CDM in a NEW 1337 campaign between the Azores and Portugal. Confirm Hooktooth is the capital **city**, its local population is the configured uneven population, and the country total is 320,117. Confirm the other four countries exist independently.
2. Inspect population culture/religion: Cinderkin, Brinekin, Reefkin, Shatterkin and Sootkin must all belong to Goblinkin and follow The Hunger Below.
3. Inspect Hooktooth's existing marketplace, naval-supplies guild and stockade. Check construction requirements; a poor treasury can still prevent purchases, but missing population/city setup should not. Verify food, workers and market access.
4. Zoom into all eight islands in 3D. Check dry land, coastlines, volcanic elevation, materials and seamless terrain across cache-tile boundaries. The packaged terrain preview is a technical heightfield, not an in-game screenshot.
5. Advance one month: Cindermaw's fleet/army and opening lore event should appear once. Advance another month and save/reload to check they do not repeat.
6. Move armies across Cindermaw and Brackmaw. Sail out of the archipelago, dock at each island, embark and land. Confirm no sailing through land and no invisible land bridges between islands. Check existing routes toward Portugal, France and the Maghreb.
7. Check captain elections, raiding availability under vanilla conditions, budgets and population for at least a year. Record any imbalance separately from parser/load errors.
8. Review fresh logs for `cm_`, the five country tags, setup parser errors and navigation/locator errors. Compare widespread vanilla errors with a mod-free baseline.
9. Load a mod-free playset/new campaign to verify ordinary vanilla geography remains available.

## Limitations

Static validation and decoded cache inspection do not prove rendering, AI pathfinding, locators or construction work in the running game. No editor cache export or new in-engine test has been completed for 0.2. Terrain is patched directly in the native cache format. Any further terrain/navigation errors need the next game log and screenshot.
