# 0.5.6 exploration handoff

Checkout: this chat's work/repo, branch feature/0.5.6-exploration-pacing,
based on staging/0.5.6 commit 3260d96. Prior economy changes remain intact.
Goal: delay first exploration by a few years and expose Iberia plus nearby
European/African coastlines under normal fog of war.

Completed: first monthly initialization gives a 36-month cooldown. Shared
starting-knowledge generator exposes Iberia, four adjacent sea areas and 24
coastal provinces in southern England, Atlantic France and Morocco for all five
crowns. EU5 discovered territory is interactable; this does not lift unit fog.
Voyage prose now describes firsthand visits and foreign contact. Existing costs,
travel times, postpone/completion cooldowns, pending guards and reciprocal
owner-scoped discovery remain intact. Existing saves are not migrated.

Passed against installed EU5 1.3.11: tools/verify_exploration.py,
tools/verify_economy.py, git diff --check. Partial generated output and audit:
build/exploration-check (not installable). Native game-concept definitions confirm
that discovery removes terra incognita while normal fog hides foreign units.

Build/install state: source-generator change only. Tracked runtime payload,
overlay manifest and bundled installer deliberately remain 0.5.5. No full build,
package, install or game launch. No runtime acceptance claimed.

Next: review source changes, full 0.5.6 build/package, then fresh-campaign checks
in TESTING.md, including visibility, early diplomacy/target selection, three-year
wait, save/reload, paid voyage returns and once-only foreign contact.
