# 0.5.5 event art and clan flags handoff

Checkout: work/repo; art/events-situations-055, based on staging/0.5.5 at
8fd0358 (initial art base 51c01d8). Goal: custom art for all events/situations and clan flags matching the supplied Gathering image.

Completed: 17 original built-in imagegen paintings with full prompts and source
hashes under art/events. Explicit native image references cover all 21 authored
events, including the 14 Gathering events and the seven older introduction and
exploration/contact events. Both situations receive headers and icons. Twenty-one
BC1 DDS textures have native dimensions and full mip chains. Related oath and
unification events intentionally share scenes. All five clan introductions have
distinct lore-based paintings. Event generators and full-build/overlay export
paths preserve art assignments. The prototype checksum manifest ships all textures
and all three event files (39 entries, including five custom flag textures and their country arms). Added art/flag validation and CI.

Checks: DDS decoding, dimensions, mip payloads, prompt/source hashes, explicit
image references and prototype checksums pass. Existing native-reference checks
and all 14 ownership scenarios pass. Parsed event trees preserve gameplay and
localization references. Preparation against the installed 0.5.4 base preserves
unrelated character/localization entries and agrees with the full-build clan
generator. Final clean-export and isolated-install results are recorded in the PR.

Flags: five hand-authored SVG/PNG emblems recreate the reference volcano, reeds,
curling wave, shark-and-waves and spiked helmet. data/clan_flags.json supplies
matching RGB fields. Native textured emblems use 384 x 256 BC3 with alpha and
nine mip levels. Full builds no longer clone Cindermaw's skull flag. Sources,
exporter, prototype manifest and CI include all five. Final clean-source and
package verification results are recorded in PR #9.

README: replaced the accumulated development/release fragments with one player
guide: separate base/add-on installation, five clan summaries, campaign goals,
current artwork/features, troubleshooting and links to detailed documentation.
Removed obsolete population totals, succession rules and installation paths.
User authorized merging PR #9 into staging/0.5.5; verify final merge state on GitHub.

State: no active game installation, launch or Workshop publication. This
remains the additive prototype on 0.5.4; the pre-existing regular .release bundle
is still 0.5.4 and is not a new full 0.5.5 release. The prototype installer is the
delivery path for this art pass. In-game rendering, crop/UI scale and override
precedence remain pending; TESTING.md has the art acceptance checklist.

Concurrent staging updates preserved: mixed-population additions (1,618,696 total),
Jaima's expanded introduction and delayed maternal-house event, and revised ruler
nickname origins. Maternal-house follow-up shares Shatterfin's council painting.
