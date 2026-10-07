# Clan flags from the Gathering banners

The user supplied the Gathering painting as the flag reference. Editable SVG
emblems recreate its five motifs, left to right: Cindermaw's black erupting volcano
on rust orange, Brackmaw's ivory rooted reeds on olive, Reefhook's curling wave on
teal, Shatterfin's shark above three waves on slate blue, and Sootwake's spiked
helmet on charcoal. The reference is also saved at art/events/sources/gathering.png.

data/clan_flags.json defines colors and tag routing. sources/*.svg are the
editable vector masters; the transparent PNGs are their antialiased raster exports.
These are hand-authored graphics based on the supplied reference. Small details
are simplified so the emblems remain readable in the country UI. The game supplies
the flag's cloth, lighting and shape.

Native country arms use pattern_solid.dds, explicit RGB field colors and one
custom textured_emblem each. Emblems are 384 x 256 BC3/DXT5 DDS textures with
real alpha and nine mip levels. tools/build_clan_flags.py regenerates the arms
and textures using Pillow. The full build and prototype include them. The former
build-time cloning of Cindermaw's skull flag is removed.

Rebuild: run python tools/build_clan_flags.py, then
python tools/prepare_prototype_055.py and python tools/verify_clan_flags.py.
To revise SVG masters, render with node tools/render_flag_sources.cjs (requires
the sharp Node package), then rerun the Python commands. PNG sources are committed
so ordinary builds do not require Node.

Static validation covers all five tags, native schema, decoding, transparency,
dimensions, mip payloads and prototype hashes. Country shields, map flags, naval
flags and coat-of-arms caches still need an in-game visual check.
