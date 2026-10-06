# 0.5.3 infantry crash containment

Branch: feature/0.5.3-goblin-pirate-portraits. Remote parent 54f05151d94c2318c43c2930b4e66d5c56d2970d.

User reproduced an access violation near infantry spawn. Read crash Europa Universalis V20261006_214334; active mod metadata is 0.5.3 and installed schematic matches the latest graph patch. Prior invalid entity graph error is absent. Unsymbolized stack cannot establish a precise cause.

Containment: ten culture-specific light/heavy infantry constructors select the complete native rig, animation machine and attachment lists. Custom assets are retained but not selected. This temporarily restores human map soldiers; goblin portraits remain. Validator prevents accidental custom constructor reactivation.

Packaging: regenerate overlay and matching bundled payload, verify clean source export with PrepareOnly, push on the existing feature branch. No active installation or game launch. Next user check: load prior save and pass spawn/crash date; test recruitment, marching and combat. Custom goblin renderer remains unresolved and needs controlled in-game isolation.
