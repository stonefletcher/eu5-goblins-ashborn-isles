# 0.5.7 religion handoff

Checkout: C:/Users/alexa/Documents/Codex/2026-10-07/le/work/goblins-057.
Branch: feature/0.5.7-ashen-covenant; base fe82a46 (merged 0.5.6 staging).
Goal: implement Oaths of Ash and Salt, the approved religion-focused proposal.

Completed first pass: source generator and full-build integration for the Ashen
Covenant display name (stable cm_hunger_below ID), six local holy sites, eight
native aspects, two initial aspects per kingdom, Covenant Favor, three scaled-price
rites with one shared cooldown, twelve initial religious stories, and the Moot of
Six Fires after Gathering. Includes monthly conversion cleanup and AI rite list.
Expanded LORE.md; README and RELIGION_057.md distinguish source from bundled release.
Exploration correction: removed starting Iberia-region and 24 coastal-province
discovery grants. Nearby sea areas remain known; all foreign land ports start
undiscovered and are revealed by voyage returns. Updated event prose and checks.
Exact coastal-silhouette rendering against the user screenshot remains untested.

Passed: verify_ashen_covenant.py against installed EU5 1.3.11; existing exploration
and economy validators; generated faith-name/description integration; diff whitespace
check. No game launch. Staging output under build/religion-check is partial.

Next: differentiate event outcomes and scale their current 5-gold payments; add
custom art; design council cooldown without native-action bypass; pilgrimage and
damaged-site restoration remain unimplemented. RELIGION_057.md lists current
effects, limits and fresh-campaign acceptance. Then full build, package and the
mandatory clean-download gate before recommending installation.

Build/install/publish: no full 0.5.7 build, package, installation, push or Workshop
upload. Bundled installer, payload and metadata remain 0.5.5. Existing 0.5.6 economy,
population, exploration timings and reciprocal contact retained; the 0.5.6 land
visibility grants are superseded. This branch is local development.

Diplomacy follow-up: tools/gathering.py now routes both Harbor Pact responses and
both Compact responses to named sender popups (existing Compact acceptance reward
retained). Harbor Pact removed from the AI list with negative desirability; player
price unchanged. Art reused through tools/event_art.py. Focused generation to
build/diplomacy-check and verify_055.py pass, including response-routing checks.
No generated mod payload, package, install or publication for this follow-up.
Gameplay checklist added to TESTING.md. Concurrent exploration edits preserved.
