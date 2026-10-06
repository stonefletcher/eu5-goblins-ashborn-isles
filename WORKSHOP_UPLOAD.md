# Goblins of the Ashborn Isles — 0.5.3 demo

## Build and stage

Run a full build against EU5 1.3.11, then run `python tools/prepare_workshop.py`.
The staging tool creates a fresh `dist/Workshop_0.5.3_TIMESTAMP` folder, verifies
all copied files and records SHA-256 hashes in `workshop_manifest.json`.

The actual upload content is its **goblins_ashborn_isles** subfolder. This contains
`.metadata`, `in_game` and `main_menu` directly. Its thumbnail is
**goblins_ashborn_isles/.metadata/thumbnail.png**, beside `metadata.json`.
If the publishing interface asks for the metadata folder, select that `.metadata`
folder; if it asks for the mod/content root, select `goblins_ashborn_isles`.
For a separate preview-image field, choose the same thumbnail PNG.

Do not upload the repository, authored `mod` folder, or compact installer ZIP.
The compact ZIP omits full terrain cache binaries and reconstructs them during
installation. Workshop subscribers need the full built mod, including the three
terrain `.bin` files and their `.info` companions. The staging tool enforces this.

## Listing

- Title: **Goblins of the Ashborn Isles — Demo**
- Initial demo version: **0.5.3**
- Target game: **EU5 1.3.11 (Pavia)**
- Description: paste `STEAM_DESCRIPTION.txt` (Steam BBCode).
- Thumbnail: existing 512 × 512 PNG; no external image path is needed in metadata.
- Use actual in-game screenshots for the gallery; concept art is not a gameplay capture.

## Acceptance before public release

The build checks prove package structure and static consistency, not engine behavior.
On the exact staged candidate, enable this mod alone and start a new 1337 campaign:

1. Confirm vanilla land and all six islands render; inspect relief, coasts and settlements.
2. Select each clan; check ownership, capital, names, ruler and opening event.
3. Inspect men, women, children, cabinet members and a human control portrait.
4. Recruit/move infantry and sail between the new coastal zones and vanilla sea lanes.
   Earlier builds reported invisible infantry; require a visible-unit check here.
5. Advance several months; inspect budgets, exploration and fresh engine logs.
6. Exercise Shatterfin succession and maternal dynasty inheritance, then save/reload.

If a demo ships with known visual/gameplay defects, describe the actual defects in
the listing. Do not convert pending checks into passed checks without testing.

This branch is an isolated snapshot of active 0.5.3 work. If the art branch changes,
integrate these three Workshop preparation files into the final 0.5.3 source and
rebuild/stage again. No Workshop item has been created or published by these tools.
