# Goblins 0.6.0 - clan flag repair

Checkout: C:/Users/alexa/Documents/Codex/2026-10-07/0/work/goblins-059
Branch: staging/0.6; origin stonefletcher/eu5-goblins-ashborn-isles.
User authorized implementation, local installation and staging push.
No main merge, Workshop publication, game launch or subagents.

The full 0.6.0 update was installed and pushed as 02f77a9: Giltfang/Tolltooth,
two markets, mutual discovery, six-crown events, tooltip cleanup, 25-gold
starting projects, clear food storage text, Lantern Cay and the Quiet Road.
Nine islands, 97 districts, 28 coastal cells, 75 ports, 12 holy sites.
All exact-source and installation hashes passed. Main remains 0.5.8.

Latest user screenshot: Giltfang displays a blue circle on yellow.
Active playset and all seven installed flag files match the tested build.
All six country setup blocks omitted explicit flag assignments. The native
setup uses flag = "ID"; the native save repair effect is change_country_flag.
Source now assigns each flag explicitly and adds a guarded, once-only monthly
repair for existing saves. Other files and flag artwork are preserved.
The new regression check failed on the previous build and passes on the repair;
full verify_059 passed. Rendering still requires gameplay confirmation.

User confirmed EU5 closed for installation. This is the pre-package record:
package the prepared candidate, commit the matching bundle, export that exact
tree to a NEW empty directory, run PrepareOnly and isolated install/hash gate,
then install with backup verification and push staging. Check fresh remote
state and task output receipts before treating those steps as outstanding.
Do not bypass a running-game guard or overwrite unrelated local fixes.
An existing 0.6.0 save can use the flag migration after restart and next month;
the wider geography update still requires a new campaign.

Game: E:/SteamLibrary/steamapps/common/Europa Universalis V/game (1.3.11)
Active mod: C:/Users/alexa/Documents/Paradox Interactive/Europa Universalis V/mod/goblins_ashborn_isles
Python: C:/Users/alexa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe
Task helper/output root: C:/Users/alexa/Documents/Codex/2026-10-07/gobl
Final delivery receipts: outputs/Goblins-0.6.0-flag-fix-*.json
