# Ashborn goblin model prototypes

**First body and skin pass. These are editable 3D art sources, not EU5-ready mesh files.**

![Five clan model variants](preview/clan_lineup.svg)

The common body is short (1.12 metres in the first Idle frame) with a large head, a broad lower jaw, a hooked nose, longer pointed ears, narrow slanted eyes, uneven tusks and a crooked mouth. Skin is matte. Clan differences are deliberately modest and concentrate on green pigmentation.

| Clan | Country | Culture | Skin | sRGB |
|---|---|---|---|---|
| Cindermaw | CDM | cm_cinderkin | Warm olive | #71834B |
| Brackmaw | QBR | cm_brinekin | Sea green | #56856B |
| Reefhook | RHK | cm_reefkin | Yellow moss | #82965B |
| Shatterfin | SFK | cm_shatterkin | Blue green | #537B76 |
| Sootwake | SWK | cm_sootkin | Dark forest green | #51634B |

## Models

Each file is self-contained binary glTF 2.0, suitable for import into a 3D editor that supports GLB. No external textures are needed.

- [Cindermaw](variants/cindermaw.glb)
- [Brackmaw](variants/brackmaw.glb)
- [Reefhook](variants/reefhook.glb)
- [Shatterfin](variants/shatterfin.glb)
- [Sootwake](variants/sootwake.glb)

All five share the same sculpt and original 23-joint skeleton. Each has 2,476 triangles and retains 17 source animations: Death, Defeat, Idle, Jump, PickUp, Punch, RecieveHit, Roll, Run, Run_Carry, Shoot_OneHanded, SitDown, StandUp, SwordSlash, Victory, Walk and Walk_Carry. The upstream spelling of RecieveHit is preserved.

The nose is new geometry weighted to the existing Head joint. The head, ears, eyes, jaw, mouth and teeth were reshaped; body topology and original skin weights are retained. A parent transform sets stature and ground height without rewriting animation tracks. This is an unarmoured adult male body prototype. Clothing, weapons, additional bodies, portrait facial animation and EU5 materials remain to be made.

[Animation pose inspection](preview/animation_poses.svg) shows sampled middle keyframes, not a video. Both previews render the actual skinned geometry.

## Source and credit

Base: **Goblin_Male** from Quaternius's **Ultimate Animated Character Pack, November 2019**.

- [Creator's pack page](https://quaternius.com/packs/ultimatedanimatedcharacter.html), which identifies this pack as CC0.
- [Original embedded source](source/Goblin_Male.gltf)
- [Upstream license text](source/License.txt)
- [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/)
- Exact retrieval location and Git blob are recorded in [clans.json](clans.json).

The source was retrieved from a public mirror of the original pack. Its license file agrees with the creator's pack page. The unmodified upstream source is retained for reproducibility. No Paradox meshes or textures are included.

## Rebuild

With Node.js installed, run from the repository root:

```powershell
node art/models/goblins/tools/build.mjs
```

The script verifies the upstream Git blob hash, applies the common sculpt, assigns the five skin palettes, generates GLB files and regenerates the geometry contact sheet. It uses only Node built-ins. Geometry preparation, encoding and preview functions were executed in the available JavaScript environment; the filesystem CLI itself has not been run on the local Windows machine because its command runner could not start.

Edit clans.json to change the palette or target height. The checked-in variants are the result of the checked-in sculpt and generator. EU5's final world scale must be calibrated against a native unit; 1.12 m here is an art-source measurement.

## Verification and next integration step

[validation.json](validation.json) records checks performed on the generated files: GLB header/chunk round trip, every accessor's bounds and finite values, triangle indices, skin weights, joint indices, animation timestamps/quaternions, preserved original animation metadata/skin topology, common ground/height and 51 sampled animation poses. The five skin variants and representative action poses were visually inspected through a CPU skinning renderer.

Not yet performed: Blender import, Khronos's official validator, native EU5 mesh export, an EU5 launch, local installation, or animation playback in the game. The v0.4.0 mod and its installer do not use these files.

The next integration work is to inspect the installed EU5 unit and portrait assets and choose the native skeleton, shader and entity definitions. Then retarget/export a goblin unit, assign the five clan variants through the game's actual graphics selection rules, and verify idle/movement/combat/death and world scale. Portraits need a separate facial rig/morph pass; these unit sources must not be treated as drop-in portrait heads. The general io_pdx_mesh tool has not been verified for this EU5 build.
