# 0.5.8 portrait pass

Checkout: C:/Users/alexa/Documents/Codex/2026-10-07/le-2/work/goblins-058
Branch: feature/0.5.8-portrait-art-pass; base ec4e006 (integrated 0.5.7 source).
Goal: court, noble and character portraits closer to Gathering artwork: short,
ugly, believable goblins. No publishing or active-profile installation requested.

Implemented: restrained face ranges, smaller hooded/recessed eyes, lean cheeks,
shorter necks, compact torso 0.42/stoop 0.24, 60% skin tint, cupped smooth closed
ears with rounded outlines and mild asymmetry, smaller teeth, no beards, more
covered male clothing. Preserves culture selection, native rigs, infant handling
and the working infantry pipeline. See RELEASE_NOTES_0.5.8.md for visual checks.

Passed: full EU5 1.3.11 build, five-culture/seven-type portrait checks, native
male/female facial attribute audit, closed/wound ear topology and positive shell
volumes, DDS compatibility and native binding/reference checks. No game launch.

Packaging: full build complete; archive/source bundle and clean-export isolated
installation verification in progress. Active installed mod untouched.
Next: finish package gates, then user-run in-game visual review. Do not describe
the technical mesh preview or static checks as proof of portrait quality.

Inherited generated religion/exploration text was refreshed to its current
0.5.7 generators. Full build overwrites LORE.md and drops its authored Ashen
Covenant section; the authored file was restored before packaging. Avoid losing
that section during future rebuilds. Historical release notes retained.
