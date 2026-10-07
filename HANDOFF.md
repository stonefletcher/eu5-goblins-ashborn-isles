# 0.5.5 clan identity handoff

Checkout: work/brackmaw; feature/brackmaw-sluice-king-055, extending c541748. Base staging/0.5.5 at 294d5f2. PR #7 targets staging/0.5.5 and now covers three clans.

Implemented: Murgash Brackmaw, The Sluice-King (84/78/90 ADM/DIP/MIL); Skrezz Reefhook, The Wreck-Taker (62/88/90); Snikh Sootwake, The Blackbough (80/54/90). Each has shared authored data, expanded culture text, lore and Gathering introduction. Reefhook's dynasty has rescue-beacon/pilotage obligations and a salvage saying; Sootwake's dynasty has firebreak/cutting-right obligations and a rootwood-table tradition. Existing brothers and consorts have narrative interests, without new appointments or mechanics. House names, family relationships, ages, succession, population, geography and situation costs remain intact.

Shared tools/clan_identity.py feeds full-build generators and the prototype manifest. Installer derives two overrides from the installed 0.5.4 base and preserves all entries outside the three rulers and intended culture/nickname text. No native game-derived setup is committed. tools/verify_brackmaw.py now checks all three identities and full-build/add-on agreement.

Checks: 0.5.5 static native references and 14 ownership scenarios; clan preservation and generator comparison. Exact-tree clean preparation/isolated installation results recorded in PR #7. In-game names, override precedence, UI and balance remain pending; TESTING.md has acceptance steps. No active mod installation, game launch, merge or Workshop upload performed. Regular installer is the prior release; this branch uses the small prototype add-on to 0.5.4.
