# 0.5.8 staging handoff

Branch: staging/0.5.8. Holy-site integration merge 06aabea; combined package 2dc53e2.
Checkout: C:/Users/alexa/Documents/Codex/2026-10-07/le-2/work/goblins-058.
Frozen build/test checkout: C:/Users/alexa/Documents/Codex/2026-10-07/for-2/work/holy-sites.

Completed: nine holy sites across six islands (counts 3/2/1/1/1/1), importance
1-5, three new local shrines. Existing site IDs/events preserved. Includes the
committed portrait/ear skin/clothing corrections from c672aac.
Full build passed, including religion, native portraits, map/setup and terrain.
Bundle regression rejects the old six-site payload and accepts the new one.
Exact committed Git export passed bundle verification and PrepareOnly; fresh
isolated installation matched all 1,658 files and passed religion validation.
Package SHA-256: b9b6b9a40fb10642f0d1be49e0f384c40ecc68ef0c6871c1310b37a979ab1456.
No active-profile install, game launch or Workshop upload. Gameplay acceptance
for shrine balance/tooltips and portrait appearance remains pending.
Next: review a new campaign. Preserve concurrent Gathering panel work below;
it is not part of this verified package and needs its own combined rebuild.

Gathering panel follow-up: generator, panel, localization and affected manifest hashes
now show participants immediately. Isolated fix/0.5.8-gathering-participants commit
f6c4999 has a matching verified bundle and clean installation (1,656 files).
These shared source edits must be included in the next combined 0.5.8 package.
Gameplay pending; no active install or publication from this follow-up.
