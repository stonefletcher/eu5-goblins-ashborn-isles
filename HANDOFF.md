# 0.5.3 infantry attachment repair candidate

Branch: feature/0.5.3-goblin-pirate-portraits. Remote parent 97b49325ca1fbef68d21891872de6dacbe100184.

Evidence: user confirmed native fallback is visible with no crash observed. Prior custom graph had direct root MeshType; native infantry base graph owns the skeleton while visible meshes use unit-graphics shared_pose_entity attachments. Unit repaint shader consumes per-unit instance/material data. The unsymbolized crash does not establish the precise faulting component.

Change: remove root MeshType and its link; create five shared-pose body attachments; route all ten clan constructors to their custom skeleton plus one body attachment. Preserve mesh, rig, 17 animation clips and portraits. Add attachment file to checksum overlay. Validator rejects root meshes and missing body attachments.

Checks: native attachment syntax, typed graph links, five clans, 51 sampled poses, native round trips and prepared bundle. Clean-export PrepareOnly gate before publishing. No game launch or active installation.

Next: test previous spawn/crash date, visible goblin models, idle/movement/combat/retreat and save/reload. Engine acceptance pending. Stable fallback: remote commit 97b49325ca1fbef68d21891872de6dacbe100184.
