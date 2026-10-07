# 0.5.8 holy-site variance handoff

Checkout: C:/Users/alexa/Documents/Codex/2026-10-07/for-2/work/holy-sites
Branch: feature/0.5.8-holy-site-variance; base bbe03e0 (staging/0.5.8).
Goal: replace uniform importance 3 and one shrine per island with lore-led variance.
Implemented: existing six sites use importance 5/3/2/4/1/2; added Blackwood
Oathstones (2), Ashfield Hearth (1), Miregrove Witness (1). Island counts 3/2/1/1/1/1.
Generator and focused validator updated; religion reference and README updated.
Native installed game documentation confirms importance 1-5 and scaled local effects.
Checks: focused religion validator, generated holy-site script parser and whitespace check.
Gameplay: pending fresh-campaign site counts, importance and modifier tooltip review.
Build/install/publish: partial religion generation only. No full package, install,
push or Workshop upload. Inherited installer excludes this change. Portrait chat
has concurrent uncommitted changes in its own staging checkout; left untouched.
Next: integrate this feature commit into the next staging build, then perform full
package/clean-download/isolated-install gates before shipping an installer.
