# Goblins of the Ashborn Isles - 0.5.3 Workshop update

## Upload the prepared package

1. Extract `Goblins_Ashborn_Isles_0.5.3_Workshop.zip` to a writable folder.
2. Close EU5 and run **Stage-Workshop.cmd**. This copies the verified full mod into your actual Documents\Paradox Interactive\Europa Universalis V\mod\goblins_ashborn_isles folder, backing up an existing copy outside the scanned mod directory. It prints the exact upload path. If your user data is elsewhere, run `Stage-Workshop.ps1 -UserDataPath "YOUR EU5 USER DATA"`.
3. Open EU5 and use **Mod Tools > Uploaded mods > your existing listing > Upload content from a folder**. Select the printed **goblins_ashborn_isles** folder. It contains `.metadata`, `in_game` and `main_menu` directly. Use the existing listing to retain subscribers.
4. If the interface specifically asks for a metadata folder, select `.metadata` inside that same staged folder. For a preview-image field, select `.metadata/thumbnail.png` (512 x 512 PNG).
5. Paste `STEAM_DESCRIPTION.txt` as Steam BBCode. Use `STEAM_CHANGELOG.txt` for the update notes. Confirm version 0.5.3, content and thumbnail after submission.

Existing listing: https://steamcommunity.com/sharedfiles/filedetails/?id=3814944518

The full Workshop mod includes all three terrain `.bin` files and their `.info` companions. Do not upload the repository, authored `mod` folder, ZIP itself or the compact installer payload before reconstruction. The prepared package includes a file-hash manifest; the staging script verifies it before copying and checks the staged files afterwards.

## Reproduce from source

Run `Install-Goblins.ps1 -PrepareOnly -GamePath "YOUR EU5 GAME DIRECTORY"` from a fresh source export. This reconstructs the matching prepared mod and verifies the native terrain base/final caches. The full content root is `.prepared-release-0.5.3/goblins_ashborn_isles`.

Alternatively run a full build against EU5 1.3.11 and then `python tools/prepare_workshop.py`. The tool creates a new `dist/Workshop_0.5.3_TIMESTAMP` candidate, verifies copied files and records their SHA-256 hashes. Stage that full content root under the EU5 user-data `mod` directory before using Mod Tools.

## Listing and acceptance

- Title: **Goblins of the Ashborn Isles - Demo**.
- Version: **0.5.3**; target game: **EU5 1.3.11 (Pavia)**.
- Start a **new 1337 campaign**, with one mod copy enabled.
- User-tested infantry visibility/crash repair is recorded in TESTING.md. Portrait fit, recruitment art, event behavior, succession edge cases and longer gameplay checks remain there.
- Gallery images should be actual gameplay screenshots; concept/diagnostic art is not an engine capture.

The package prepares an update to the existing item. Steam publication must still be performed in Mod Tools; no upload is implied by GitHub release publication or ZIP preparation.
