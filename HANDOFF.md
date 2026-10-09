# Goblins 0.6.1 staging

Checkout: C:/Users/alexa/.codex/.chatgpt-projects/g-p-6abf07c4fe4081919d1536ed15794d22/goblins-061
Branch: staging/0.6.1, based on main f75fe73. Read current Git HEAD/status before continuing.

Requested work: starting piracy/stats, glass/masonry and trading infrastructure,
connected provinces, town/city growth, visible Covenant Favor, varied male
portraits and tougher Drogg, capital sergeantries, +50% monthly manpower, and
flavor-only voyage reports revealing useful foreign coastal pockets/markets.
All changes are implemented. See README and RELEASE_NOTES_0.6.1.md for scope.

Economy checks pass, including staffing and unchanged kingdom population totals.
All 40 provinces pass actual-raster land connectivity. Voyage script scenarios
pass expanded discovery, reciprocal contact, payment and stale-reply checks.
Terrain rebuild and complete assembly validation passed; packaging is underway.
An earlier full build failed a stale exploration event manifest; that manifest
was refreshed. The resumed canonical build rechecks native/final cache hashes,
map metadata, terrain and every setup/candidate validator.

Next: finish matching package/bundle, export exact committed tree to a new
empty folder, run PrepareOnly and isolated UserDataPath installation, compare
all delivered hashes, then push staging and verify remote README. Do not push
before the installer gate. EU5 was running (PID 28828); do not close/launch it
without user authorization. Ask user to close it once candidate is prepared.

Active mod: C:/Users/alexa/Documents/Paradox Interactive/Europa Universalis V/mod/goblins_ashborn_isles
Game: E:/SteamLibrary/steamapps/common/Europa Universalis V/game (1.3.11)
Active 0.6.0 matched every baseline bundled file before edits. It is unchanged.
No install, release, main merge or Workshop publication has been performed.
New campaign required for starting-world edits. Visual/gameplay acceptance,
actual market trade and discovery rendering remain untested in the engine.
