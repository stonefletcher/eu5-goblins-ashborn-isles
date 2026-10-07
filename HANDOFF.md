# 0.5.5 event and situation art handoff

Checkout: work/repo; art/events-situations-055, based on staging/0.5.5 at
51c01d8. Goal: custom art for all new events and situations.

Completed: 17 original built-in imagegen paintings with full prompts and source
hashes under art/events. Explicit native image references cover all 20 authored
events, including the 13 Gathering events and the seven older introduction and
exploration/contact events. Both situations receive headers and icons. Twenty-one
BC1 DDS textures have native dimensions and full mip chains. Related oath and
unification events intentionally share scenes. All five clan introductions have
distinct lore-based paintings. Event generators and full-build/overlay export
paths preserve art assignments. The prototype checksum manifest ships all textures
and all three event files (33 entries). Added focused art validation and CI.

Checks: DDS decoding, dimensions, mip payloads, prompt/source hashes, explicit
image references and prototype checksums pass. Existing native-reference checks
and all 14 ownership scenarios pass. Parsed event trees preserve gameplay and
localization references. Preparation against the installed 0.5.4 base preserves
unrelated character/localization entries and agrees with the full-build clan
generator. Final clean-export and isolated-install results are recorded in the PR.

State: no active game installation, launch, Workshop publication or merge. This
remains the additive prototype on 0.5.4; the pre-existing regular .release bundle
is still 0.5.4 and is not a new full 0.5.5 release. The prototype installer is the
delivery path for this art pass. In-game rendering, crop/UI scale and override
precedence remain pending; TESTING.md has the art acceptance checklist.
