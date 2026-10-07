# Ashborn event and situation art

Seventeen original paintings cover all twenty authored events, the Gathering of
the Five and Eastern Hunger situation headers, and both situation icons.
The thirteen 0.5.5 events use eleven paintings; oath offer/acceptance and the two
unification perspectives intentionally share their matching scene. The opening
Cindermaw lore event shares Drogg's forge painting. Six exploration and reciprocal
contact events each have a separate painting.

Art direction: small, wiry goblins in patched cloth and worn leather, long ears,
hooked noses and muted green skin; basalt, sea haze and ember light. Each clan's
introduction illustrates its authored story. Shatterfin's female ruler and maternal
house remain distinct. European and African shores use late medieval vessels and
coastal architecture.

`sources/` contains the unaltered generated PNG originals. `prompts.json` records
the complete prompts, generation method (built-in imagegen), and original hashes.
`exports.json` records every runtime texture and hash. No vanilla artwork is copied.

`tools/event_art.py` is the mapping used by both event generators and the exporter.
Events use EU5's native `image` field. Situation headers and icons use the native
ID-based paths, without a GUI override. Headers/events are 1080 x 440; icons are
128 x 128 square details. DDS files use BC1/DXT1 with full mip chains.

Rebuild from the repository root with its Python requirements installed:

```powershell
python tools/export_event_art.py
python tools/gathering.py
python tools/prepare_prototype_055.py
python tools/verify_event_art.py
```

The full builder regenerates exploration events and textures as well. The small
prototype manifest includes all art and all three authored event files, so the
0.5.4 base does not supply generic pictures for the older events. The existing
regular installer remains the prior 0.5.4 release; use the 0.5.5 prototype installer
for this branch's new situations and art.

Static decoding, dimensions and packaged-file checks do not confirm engine
rendering. In-game crop, image selection, situation icons and UI scaling still
require the acceptance steps in `TESTING.md`.
