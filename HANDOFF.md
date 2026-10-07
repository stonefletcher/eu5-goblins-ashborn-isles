# 0.5.5 clan identity handoff

Checkout: work/brackmaw; feature/brackmaw-sluice-king-055, extending 81f0f96. Base staging/0.5.5 at 294d5f2. PR #7 targets staging/0.5.5 and covers four clans.

Implemented: Drogg Cindermaw, The Stone Fletcher (78/80/96 ADM/DIP/MIL); Murgash Brackmaw, The Sluice-King (84/78/90); Skrezz Reefhook, The Wreck-Taker (62/88/90); Snikh Sootwake, The Blackbough (80/54/90). Each has shared authored data, expanded culture text, lore and Gathering introduction. Cindermaw now has military service, forge-captain patronage, House Cindermaw's One fire, many blades saying, Drogg's nickname origin and ambitions for leadership. Existing relatives receive narrative interests without new appointments or mechanics. House names, relationships, ages, succession, population, geography and situation costs are intact.

Shared tools/clan_identity.py feeds full builds and the prototype manifest. Installer derives two overrides from installed 0.5.4 and preserves entries outside the four rulers and intended culture/nickname text. Drogg's existing nickname is checked and preserved once. No native game-derived setup is committed. tools/verify_brackmaw.py checks all four identities and full-build/add-on agreement.

Checks: static native references and 14 ownership scenarios; clan preservation and generator comparison. Exact-tree clean preparation/isolated installation results recorded in PR #7. In-game names, override precedence, UI and balance remain pending; TESTING.md has acceptance steps. No active mod installation, game launch, merge or Workshop upload. Regular installer is the prior release; this branch uses the small prototype add-on to 0.5.4.
