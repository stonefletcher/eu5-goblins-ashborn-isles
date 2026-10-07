# 0.5.4 Workshop upload

Use the standard package and installer.

1. Extract `Goblins_Ashborn_Isles_0.5.4.zip` into a fresh folder. Close EU5 and run **Install-Goblins.cmd**.
2. The installer reconstructs all three terrain caches and installs the full mod. The normal upload folder is:
   `C:\Users\alexa\Documents\Paradox Interactive\Europa Universalis V\mod\goblins_ashborn_isles`
   If your Documents or EU5 user-data folder is redirected, use the actual installed path printed by the installer.
3. Open EU5 **Mod Tools > Uploaded mods**, choose the [existing listing](https://steamcommunity.com/sharedfiles/filedetails/?id=3814944518), and upload content from that installed folder. It must directly contain `.metadata`, `in_game` and `main_menu`.
4. If asked specifically for metadata, select `.metadata` within that folder. Preview: `.metadata/thumbnail.png`.
5. Paste `STEAM_DESCRIPTION.txt` as Steam BBCode and `STEAM_CHANGELOG.txt` as the update notes. Check version **0.5.4** and the retained listing after upload.

Do not upload the repository, ZIP or compact unprepared payload. The full installed folder contains the reconstructed terrain `.bin` files and their `.info` companions. The installer verifies the matching game caches and backs up previous content.

Target game: **EU5 1.3.11 (Pavia)**. Test using a **new 1337 campaign** and one active copy. See `TESTING.md` for map, population, lifespan, economy, succession and regression checks.

GitHub release publication does not upload the Steam item.
