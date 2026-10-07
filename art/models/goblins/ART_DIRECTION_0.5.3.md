## 0.5.3 infantry attachment repair candidate

Native fallback infantry were visible and did not reproduce the crash in the user's test. Custom goblin infantry are now re-enabled through the native attachment workflow: the base graph supplies the skeleton, transform and animation machine; a named shared_pose_entity attachment supplies the visible mesh. The direct root MeshType is removed.

This is a focused repair candidate, not a confirmed crash root cause. Meshes, palettes, rig, animation clips and character portraits are unchanged. Validation covers five attachments, ten constructors, graph links and installer contents. Engine acceptance is pending: pass the previous spawn date, inspect goblin infantry, then move, fight and save/reload.

## 0.5.3 development: rough-clad goblins

Portrait refinement: ears now extend 9 cm from their base (previously 5.8), with longer hooked noses, smaller jaws/chins, prominent cheeks, wider mouths and smaller teeth. A culture-only special gene applies compact torso proportions and a mild stoop to adult males and females, fading out during childhood. Human cultures remain outside these modifiers. Exact stature, portrait framing and clothing fit await engine review.

Infantry repair candidate: connect the missing translation input explicitly, consume the native CustomAnimationMachineName parameter, and write graphics scripts with a UTF-8 BOM. Typed graph-link checks now complement mesh/animation validation. The prior graph was rejected in the game log; successful in-game rendering is not yet verified.

First art pass on a separate branch based on 0.5.2. Infantry stature is reduced from 1.12 m to 0.92 m, jaws are narrower and teeth smaller. Clan skin palettes are muted olive, marsh, lichen, slate and soot greens. Portrait recoloring retains 12% of underlying albedo detail.

Portraits select native plain harnesses, wraps, jackets and overcoats for both sexes and all Ashborn cultures, including rulers and courts. Crowns, normal court clothes, capes and neck ornaments are overridden. Children retain basic clothes and infants retain a single native swaddle.

Static model, animation, texture, rig and clothing-reference checks pass. In-game appearance remains unverified. Exact full-body stature and custom torn/patchwork leather-and-rag art remain pending. This branch includes a prepared 0.5.3 installer; Workshop publication is separate.

Direction: small, wiry island scavengers in worn leather, coarse cloth, wraps and simple harnesses. Maritime character should come from salvaged clothing and modest trinkets rather than elaborate captain uniforms.

Current infantry use dark brown shorts; custom ragged hems, rope belts, patches and weathered textures remain to be authored. Portrait clothing is a native fitting prototype, not bespoke goblin art. No native meshes or textures are copied.

The native female body height animation is disabled, and the head-size gene is a no-op. A later proportion pass must support both sexes and keep clothing, head attachments and portrait framing aligned.

Rebuild with `node art/models/goblins/tools/build.mjs`, then `python tools/prepare_main_overlay.py --game "PATH/TO/EU5/game"`.

Current validation: five variants, 17 animations / 51 sampled poses, byte-exact native parser round trips, BC3 1024-square 11-mip portrait decals, native head-rig bindings and clothing references. These checks do not replace an engine render.
