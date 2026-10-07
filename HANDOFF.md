# 0.5.6 economy development handoff

Checkout: work/eu5-goblins, staging/0.5.6, based on GitHub main.
Economic pass commit: d776785. Staging branch published to GitHub. README now
describes the economic pass and distinguishes staging source from the 0.5.5 bundle.
Goal: lore/geography-based economies with vanilla-scale infrastructure and viable
small crowns. See ECONOMY_056.md for decisions, comparisons and campaign checks.

Completed: distinct capital industries, wooded charcoal chain, population-aware
rural buildings, restrained resource investment, native-reference audit and
focused setup verifier. All 72 location IDs, geography, resources, population
classes and 1,618,696 people are preserved. RGO bonuses fall from 387 to 126.

Passed: focused setup generation against installed EU5 1.3.11, native building
ranks/resources, exact generated levels/population, production staffing,
specialization/relative scale and ownership-guarded once-only initialization.
Existing Hooktooth stockade has no seeded soldiers; runtime garrison is untested.

Build state: build/economy-check is a partial validation tree, NOT an installable
mod. No full build, install, launch or release publication. Staging source is
intended for origin/staging/0.5.6; verify remote tracking before continuing.
The bundled installer
and release metadata deliberately remain 0.5.5 until a complete 0.5.6 release is
prepared. Do not mistake the old bundle for the new economy.

Next: continue 0.5.6 work, then full build/package and fresh-campaign balance
acceptance (food, employment, trade, debt and starting-force affordability).
