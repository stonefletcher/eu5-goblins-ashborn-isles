# Goblins 0.6.1 — city/wharf/starting-trade follow-up

Branch staging/0.6.1; previous deployed/pushed candidate e569e60.
New work: Brackhaven city; all ten coastal urban locations have one wharf;
remove inland Netjaw's invalid wharf (confirmed in game error.log).
Native startup effects seed CDM silver imports Chainhaven -> Hooktooth and
GTF lumber imports Hooktooth -> Chainhaven, desired merchant capacity 1,
locked. Require distinct markets, merchant/capacity and path; confirm route
before once-only flag. Retry monthly until 1338.12.1; never recreate a completed
route after cancellation. Internal market allocation uses access, not routes.

Full static candidate and economy checks passed. Terrain unchanged/reused with
native/final hash checks. New coast/wharf and trade registration checks pass.
Regenerated sources/manifests and matching player package are being prepared.
Next: bundle, commit, empty clean export, PrepareOnly + isolated installation,
verify every file, update README validation and push. EU5 was running PID26500;
ask for closure once candidate is concrete, never kill it. In-game trade volume
and rendering remain untested. A new campaign applies city/wharf setup changes.

Active local mod is the previous 0.6.1 candidate, verified in
build/active-install-061.json. Preserve any local fixes before replacement.
Previous 0.6.0 rollback exists outside mod/; no new backup needed until deploy.
Earlier successful scratch E:/CodexScratch/goblins-061-20261009-review remains
because automatic cleanup was denied; do not bypass denial. Retain receipts.
Game: E:/SteamLibrary/steamapps/common/Europa Universalis V/game (1.3.11).
Active mod: Documents/Paradox Interactive/Europa Universalis V/mod/goblins_ashborn_isles.
No main merge, GitHub release or Workshop publication requested.
