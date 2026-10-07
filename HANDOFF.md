# 0.5.6 installation repair

Checkout: C:/Users/alexa/Documents/Codex/2026-10-07/cr/work/goblins
Branch: fix/0.5.6-installable-staging; target staging/0.5.6.
Integrates staging fe82a46 (economy and exploration) with event fixes d2573fe.

Cause: staging source configuration changed while the bundled payload remained 0.5.5. Installer correctly rejected its hash. Fixed by full 0.5.6 build/package; checksum guard retained. Generated exploration cooldown/text also refreshed (36-month delay).

Passed: full build static validation (72 locations, 1,618,696 population); archive SHA/size/CRC/unique entries; source/bundle/terrain/overlay 0.5.6 consistency; current Gathering contents; clean committed-source PrepareOnly with no build cache. Isolated installation and final clean export results are in ../isolated-056-install.log and ../final-056-prepare.log. Verify completion of these before handoff. No active mod installation or game launch. Gameplay untested.

Publish source and matching .release together. Next: runtime acceptance of panels, performance, choices, economy and exploration in a new campaign.
