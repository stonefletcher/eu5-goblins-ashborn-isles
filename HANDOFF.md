# 0.5.5 complete-release handoff

Checkout: work/repo, release/v0.5.5. Art/flag/player-guide PR #9 merged at e5539c4.
Release source: 393d6badf5118a4d6884dee76eafa4da0628da17.
Verified bundled tree: 3b7861b3fdc3a940cd321d1fb1d3ebe78e8de337.

Completed: full 0.5.5 build and regular installer bundle, including Gathering,
Eastern Hunger, revised clan identities, mixed populations, all event/situation
art and all five clan flags. No 0.5.4 prerequisite or prototype add-on is needed.
README, release notes, Workshop description/changelog and test guidance describe
one full mod; the prototype installation guide is explicitly historical.

Passed: full static build (72 districts, 1,618,696 people), native reference and
ownership checks, art/flag validation, bundle reconstruction/CRC/unique members,
all 39 Gathering/art/flag file comparisons, and exact Git-export PrepareOnly.
Regular installation to isolated user data passed. Independent verification
hashed all 1,639 packaged runtime files and three final terrain caches. The
existing source/bundle version mismatch is resolved; all layers report 0.5.5.

Deliverable: outputs/Goblins_Ashborn_Isles_0.5.5.zip, 253,684,636 bytes.
SHA-256: 7fdd318f7b0346c6e6ecf082025564fed3097e1623b7b81f7da79b8f27071d93.
Evidence: outputs/Ashborn_0.5.5_Release_Validation.json and workspace release logs.
Source and matching bundle are pushed to staging/0.5.5. This follow-up changes
only this handoff; verified release content remains the tree identified above.

Pending: user-run in-game UI/art, AI and balance acceptance. Disable the earlier
Gathering Prototype add-on and start a new 1337 campaign. No active installation,
game launch or Workshop publication was performed.

Published: GitHub release v0.5.5 (non-draft, non-prerelease), tagged at e2276ec,
with the full installer and focused RELEASE_NOTES_0.5.5.md. Publishing workflow
37653002068 passed. Published asset size/digest and a fresh downloaded ZIP match
the SHA-256 above. Release URL:
https://github.com/stonefletcher/eu5-goblins-ashborn-isles/releases/tag/v0.5.5
