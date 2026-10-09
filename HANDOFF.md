# Goblins 0.6.1 — awaiting isolated installation

Checkout: this repository; branch staging/0.6.1.
Source: e2de3a8. Validated bundle: 757cc08. Not pushed or installed live.
All requested gameplay changes are implemented; see README and 0.6.1 notes.

Passed: complete static/terrain validation, staffing/population, 40 connected
provinces, portraits/models and 10 voyage scenario groups. Bundle verified.
Clean export at E:/CodexScratch/goblins-061-20261009-review/source passed
PrepareOnly; all 1,975 runtime files match the build. Receipts are under build/.

Remaining: EU5 was running (PID 28828); closure requested once, no reply yet.
After verifying closure, run the exported installer with a fresh isolated
-UserDataPath E:/CodexScratch/goblins-061-20261009-review/user and compare
files using .local/compare_install.py. Do not use or replace the active mod.
Then update validation wording, commit task changes, push staging and verify
remote README. Do not release, merge main or publish Workshop.

Efficiency update: skills now permit reusing receipts for unchanged relevant
inputs; unembedded README/HANDOFF-only edits do not require another full export.
The player payload is unchanged. package.py now makes source ZIP optional via
--source; check relevant input changes before deciding which stages to repeat.
Redundant source archives were removed; retain current player ZIP and pending
clean-test workspace. No active mod, saves, authored assets or rollback removed.

Game: E:/SteamLibrary/steamapps/common/Europa Universalis V/game (1.3.11).
Active 0.6.0 under Documents/Paradox Interactive/Europa Universalis V/mod/
goblins_ashborn_isles remains unchanged. New campaign required for starting
world edits. Actual trade, discovery/UI and portrait rendering remain untested.
