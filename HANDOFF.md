# Integrated 0.5.3 test build

Checkout: goblins-0.5.3; branch: feature/0.5.3-goblin-pirate-portraits.
Base before illustration integration: d15c54f. Artwork source: 6c4cb1c in
feature/0.5.3-infantry-art; selectively integrated without replacing later fixes.

Includes latest goblin portrait anatomy, shared-pose infantry body attachments,
and companion first-contact event. Adds original culture-specific regiment art
for 137 light/heavy infantry definitions across five Ashborn cultures. Uses one
shared medieval painting in this first pass. Recruitment/stats are unchanged.

All 160 prior overlay entries were preserved byte-for-byte. Art validation and
prepared-bundle verification passed (1540 overlay entries). Clean source-style
installer PrepareOnly completed successfully, including reconstruction/checksums
for all three terrain caches. Build and overlay regeneration retain the new art.

Prepared package: dist/Goblins_Ashborn_Isles_0.5.3.zip. No active installation,
game launch, GitHub push or Workshop publication in this integration turn.

Next: install with EU5 closed and inspect recruitment/levy/army illustrations for
all five cultures, with human cultures as negative controls. Test infantry spawn,
movement/combat/retreat and save/reload for the shared-pose candidate; engine
acceptance remains pending. Test Portugal's event on the next eastern voyage
return. Already-completed voyages are not replayed.
