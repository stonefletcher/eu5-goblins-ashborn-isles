# Combined 0.6.0 handoff

Checkout: C:/Users/alexa/Documents/Codex/2026-10-07/0/work/goblins-059
Branch: staging/0.6. Combined package commit: a58117fa27c8455321d25d72789cd76f8a2513d3.
Source binding: 992ed124f81977cc0b0249519f791dc488bd927e.
Remote: https://github.com/stonefletcher/eu5-goblins-ashborn-isles.git
Only staging push/local installation authorized; no main merge, published release or Workshop update.

## Integration correction
User reported blue ears after installing initial 0.6.0. Audit proved the old local
0.5.9 and initial 0.6.0 candidates had identical 1,664 files except version metadata.
The older candidate itself omitted subsequent released portrait, holy-site and
standings changes. Promotion had preserved the incomplete integration.
Restored origin/main portrait generators, native-contract checks and full runtime:
native skin/head-decal ear material, SSAO/ear-base assets, UVs, morphology,
weathering, wardrobe suppression, hair and Drogg. Portrait files match upstream.
Merged nine varied holy sites into newer Covenant generator without reverting
story choices, cleanup optimizations or corrected language/price registration.
Restored five founding-crown standings with shared current ownership counter,
both Compact types, newer diplomacy explanations and active/ended voyage buttons.
Combined-candidate guards run against built AND packaged files.

## Preserved gameplay
All five clans start 100 gold in new campaigns; project costs 10 and AI reserve 20.
Three one-off projects per clan, distinct openings, paid Harbor Bargains and
consensual Compact charters, history gates, cooldowns and stale/legacy guards.
12 Covenant stories each have two approaches plus neutral defer, 3-year effects.
Exploration keeps status, timers, manual reopening and arrival-owner reports;
36-month start, 5/10/10 gold, 4/6/6-month voyages and 12-month rest unchanged.
Event optimization, model texture registration and cleaned player archive remain.

## Verified state
Full script simulations/native art checks pass. Clean exact Git export and
isolated installation: E:/CodexScratch/Goblins060Combined20261007/source and /profile.
Bundle CRC/source/overlay checks, stale-source rejection and all 1667 hashes pass.
Locally installed same candidate with EU5 closed; playsets unchanged.
Backup verified byte-for-byte: C:\Users\alexa\Documents\Paradox Interactive\Europa Universalis V\goblins_backups\goblins_ashborn_isles_20261007_222137_427.
Previous 0.5.8 backup remains goblins_ashborn_isles_20261007_220606_592.
ZIP: Goblins_Ashborn_Isles_0.6.0.zip, 213040607 bytes, SHA256 d55fc3766a9ecac3b92f09625daa18ca71f5a8a6fec47921218accc95ef28ed9.
Updated ZIP and receipts in chat outputs. No engine launch or visual acceptance.
Next: user checks ear/face colour, Drogg/clothing, standings and nine shrines.
Verify pushed remote head/README before final handoff.

## Remaining work and tools
Approval queue: subjugation access/clarity, overseas consolidation, foreign reactions.
No unapproved project discounts, AI reserve reduction or war-action changes.
Other log leads: ambiguous map location, sea-effect bounds, reserved Covenant state.
Python: C:/Users/alexa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe
Game: E:/SteamLibrary/steamapps/common/Europa Universalis V/game (1.3.11).
build/ junction -> E:/CodexScratch/Goblins059Scripts20261007/build.
Helpers outside repo: verify_060_combined.py, check_combined_local.py.
Historical staging/0.5.9 and archive/0.6-prepublication retained locally.
Never bypass running-game gate. Earlier scratch cleanup denied; preserve old scratch.
No subagents. Apply eu5-modding release/clean-export workflow before future pushes.
