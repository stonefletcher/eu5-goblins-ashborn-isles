# 0.5.5 complete-release preparation

Checkout: work/repo, staging/0.5.5. Art/flag/player-guide PR #9 merged at e5539c4.
Goal: replace the 0.5.4 bundled payload with a full, installable 0.5.5 release.

Full build against installed EU5 1.3.11 passed static validation: 72 districts,
1,618,696 goblins, Gathering/Eastern Hunger, all clan identities and succession.
Event/situation art and all five clan flags are integrated. The full build
preserves the earlier infantry/portrait pipeline. Gameplay acceptance remains
pending; no game launch or active installation has been performed.

Player README, release notes, Workshop description/changelog and test guidance
now describe one full mod and regular installer. The earlier prototype guide is
marked historical; disable that add-on when using the complete 0.5.5 mod.
Package verification now checks all 39 Gathering/art/flag files and current docs.

Next: bundle the new build with matching overlay/config hashes, verify the exact
Git export through the regular PrepareOnly installer and isolated installation,
then publish the matching source/bundle on staging. GitHub/Workshop release
publication is not part of preparation. Record final gate results in outputs.
