# Demo verification checklist

## Completed outside the engine

The builder verifies the following and writes its evidence into `build/reports/validation.json`:

- Script brace balance, JSON validity and required installed identifiers.
- Every new location has one connected footprint; all eight are connected through land adjacency.
- All replaced map pixels were traversable water, never existing land.
- Each port coordinate lies on its named sea location, with Y converted to the engine convention.
- Each population total matches the source specification exactly using decimal arithmetic.
- Existing population, ownership, town, market and hierarchy content is preserved in order.
- Starting policies exist within their respective laws.
- The custom election references the Cindermaw reform rather than the vanilla pirate reform.
- The procedural terrain is above sea level on the island mask and below sea level outside it.

These checks are not an EU5 parser or gameplay test.

## Required next: engine smoke test

Use EU5 1.3.11, a separate playset with only this demo, and a new campaign. Record all failures rather than continuing an unreliable save.

1. **Discovery:** confirm the mod appears, applies, and reaches the new-campaign screen without a crash.
2. **Country:** locate Cindermaw northeast of northern Madagascar. Confirm all eight locations are owned by CDM, Hooktooth is the capital, and no neighboring country lost land.
3. **Map:** inspect flat and 3D modes at several zoom levels. The northern volcano should be on the actual island. Check coastlines, capital/army positions, borders and map labels. A correct flat map does not prove that the terrain cache was rebuilt.
4. **Identity and economy:** check Cinderkin culture, Cinder Tongue, The Hunger Below, the captains' government and election, 200K population, 6K enslaved population, 20 starting gold, seven resource types, and Hooktooth's town/market/buildings. Record the actual monthly balance and food balance.
5. **Initialization:** advance through the first monthly pulse. Confirm one event, four galleys, eight cogs, and two footmen sub-units. Advance another month and save/reload: the force and event must not repeat.
6. **Movement:** move the army between every location. Move ships out of Hooktooth, into Saltjaw/Splinter Cove, and toward Madagascar. Embark, sail and disembark. Check that fleets cannot sail through the new island and that existing sea routes still work.
7. **Raiding:** confirm privateering/slave-raiding actions are available under appropriate vanilla conditions. Run a small controlled war and verify the actual captured-population behavior; do not assume a modifier alone proves it works.
8. **Persistence:** save and reload the new campaign; play at least a year. Check treasury, food, election behavior, unemployment and fleet upkeep. Then check a mod-free playset still loads the ordinary vanilla map.
9. **Logs:** compare fresh `logs/error.log` and relevant debug logs against a vanilla baseline. Look especially for `cm_`, `CDM`, unknown fields, unresolved names, missing terrain layers, ports and spline/navigation errors. Never describe a static validation pass as an in-game pass.

## Terrain/editor gate

If the island is submerged or stale in 3D, open a separate editor session using the demo. Locate the `cm_island` terrain instance, check its transform against the location map, and export the terrain cache into the mod's matching `in_game/gfx/terrain2/terrain_cache/` path. Confirm the editor is saving to the mod, not the Steam installation. Back up generated output before replacing it.

Regenerate required locators, splines and navigation data using the installed editor tools, then repeat the movement and zoom tests. Exact editor commands and export behavior remain to be verified against this installation; no unverified console commands are automated here.

## Known limitations

- No engine launch, parser log review or editor cache export has been performed.
- No custom goblin anatomy or nonhuman inheritance/assimilation rules yet.
- The current opening choices are informational.
- AI-directed invasion and scripted captive processing are future work.
- The source builder preserves existing world content, but it does not make full-file overrides compatible with other map/setup mods.
