# Goblins 0.6.1 — city/wharf/trade follow-up installed

Branch staging/0.6.1; source 165645c, matching bundle 35972fe.
Brackhaven is a city. All ten coastal urban locations have one wharf;
inland Netjaw's invalid wharf removed. CDM imports silver Chainhaven->Hooktooth;
GTF imports lumber Hooktooth->Chainhaven, desired merchant capacity 1, locked.
Native startup effects check distinct markets, merchant/capacity and path.
Once-only completion follows confirmed route creation; bounded monthly retry
until 1338.12.1. Cancelled completed routes stay cancelled. Same-market route
creation is not supported; internal goods allocation uses market access.

Passed: full static validation, economy/staffing/populations, coastal wharf
checks, trade script registration and prior regression suites. Reused unchanged
verified terrain. Clean export/PrepareOnly/isolated installation passed; all
1,977 files match. Receipts: build/isolated-install-061.json and validation.json.

Deployed locally while EU5 was closed: four changed runtime files only; all
1,977 installed files verified (build/active-install-061.json). Previous active
copy matched e569e60 with no local changes. Rollback under user-data
/goblins_backups/goblins_061_city_trade contains two originals plus added-file
manifest, 276,582 bytes. No game launch. New campaign needed for city/wharf setup.
Actual route creation/volume and gameplay acceptance remain engine-untested.

Current clean workspace: E:/CodexScratch/goblins-061-trade-review/source.
Older review workspace retained following cleanup denial; do not bypass it.
Game: E:/SteamLibrary/steamapps/common/Europa Universalis V/game (1.3.11).
Active: Documents/Paradox Interactive/Europa Universalis V/mod/goblins_ashborn_isles.
Read remote/HEAD to confirm staging push; no release/main/Workshop requested.
