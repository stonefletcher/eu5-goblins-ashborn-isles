# 0.5.3 infantry attachment repair candidate

Branch: feature/0.5.3-goblin-pirate-portraits. Remote parent 97b49325ca1fbef68d21891872de6dacbe100184.

Evidence: user confirmed native fallback is visible with no crash observed. Prior custom graph had direct root MeshType; native infantry base graph owns the skeleton while visible meshes use unit-graphics shared_pose_entity attachments. Unit repaint shader consumes per-unit instance/material data. The unsymbolized crash does not establish the precise faulting component.

Change: remove root MeshType and its link; create five shared-pose body attachments; route all ten clan constructors to their custom skeleton plus one body attachment. Preserve mesh, rig, 17 animation clips and portraits. Add attachment file to checksum overlay. Validator rejects root meshes and missing body attachments.

Checks: native attachment syntax, typed graph links, five clans, 51 sampled poses, native round trips and prepared bundle. Clean-export PrepareOnly gate before publishing. No game launch or active installation.

Next: test previous spawn/crash date, visible goblin models, idle/movement/combat/retreat and save/reload. Engine acceptance pending. Stable fallback: remote commit 97b49325ca1fbef68d21891872de6dacbe100184.

## Companion first-contact event
Added goblins_exploration.6 to tools/exploration.py and all three return-voyage owner scopes. One country flag prevents duplicate notifications across ports and clans; Ashborn tags excluded. Narrative: strange shore visitors flee, a scout ship follows to the islands. No physical scout unit is spawned. Completed voyages are not replayed.
Runtime files are included in the authored overlay and rebuilt prepared bundle. Static route/owner/flag/localization checks and bundle verification passed; engine playtest pending. No active installation or game launch. Test Portugal on the next eastern return, then repeat with another clan and test other port owners.
Installer PrepareOnly extracted and verified the overlay, then stopped copying terrain because the disk was full; incomplete heightmap copy removed. No install occurred.
