## 0.5.3 development: rough-clad goblins

First art pass on a separate branch based on 0.5.2. Infantry stature is reduced from 1.12 m to 0.92 m, jaws are narrower and teeth smaller. Clan skin palettes are muted olive, marsh, lichen, slate and soot greens. Portrait recoloring retains 12% of underlying albedo detail.

Portraits select native plain harnesses, wraps, jackets and overcoats for both sexes and all Ashborn cultures, including rulers and courts. Crowns, normal court clothes, capes and neck ornaments are overridden. Children retain basic clothes and infants retain a single native swaddle.

Static model, animation, texture, rig and clothing-reference checks pass. In-game appearance remains unverified. Full portrait body stature and custom torn/patchwork leather-and-rag art remain pending. This source/art branch is not a prepared installer or Workshop release; build and package 0.5.3 before installation.

Direction: small, wiry island scavengers in worn leather, coarse cloth, wraps and simple harnesses. Maritime character should come from salvaged clothing and modest trinkets rather than elaborate captain uniforms.

Current infantry use dark brown shorts; custom ragged hems, rope belts, patches and weathered textures remain to be authored. Portrait clothing is a native fitting prototype, not bespoke goblin art. No native meshes or textures are copied.

The native female body height animation is disabled, and the head-size gene is a no-op. A later proportion pass must support both sexes and keep clothing, head attachments and portrait framing aligned.

Rebuild with `node art/models/goblins/tools/build.mjs`, then `python tools/prepare_main_overlay.py --game "PATH/TO/EU5/game"`.

Current validation: five variants, 17 animations / 51 sampled poses, byte-exact native parser round trips, BC3 1024-square 11-mip portrait decals, native head-rig bindings and clothing references. These checks do not replace an engine render.
