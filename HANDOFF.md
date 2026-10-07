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
population and exploration source retained. This branch is local development.
