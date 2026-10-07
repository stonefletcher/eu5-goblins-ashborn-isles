# Goblins of the Ashborn Isles - 0.5.4

![Goblins of the Ashborn Isles](art/Goblins_Banner.png)

Five rival goblin kingdoms occupy six volcanic islands between the Azores and Portugal. They share the Ashborn heritage, Cinder Tongue and the Hunger Below faith, with distinct cultures, ruling houses and clan identities.

**Release branch:** [release/v0.5.4](https://github.com/stonefletcher/eu5-goblins-ashborn-isles/tree/release/v0.5.4).
**Game version:** EU5 1.3.11 (Pavia). Restart the game and use a **new 1337 campaign**.

[Download 0.5.4](https://github.com/stonefletcher/eu5-goblins-ashborn-isles/releases/tag/v0.5.4) | [Release notes](RELEASE_NOTES_0.5.4.md) | [Testing](TESTING.md) | [Workshop upload](WORKSHOP_UPLOAD.md) | [Lore](LORE.md)

## Districts and Dynasties

Built on tested staging/0.5.3. EU5 1.3.11; a new 1337 campaign is required.

- 1,294,755 goblins. The initial +15% pass is followed by at least another +50% for every clan; smaller clans receive a larger uplift. Location and population-class shares are preserved with whole-person rounding. Shatterfin is the largest smaller clan.
- 36 → 72 inhabited locations and 15 → 30 provinces. Every original location and province is subdivided. Stable country tags, original location IDs, capitals, coastlines and thirteen sea zones remain.
- Starting building levels rise from 47 to 114: stronger capital markets, five granaries, tools/cloth/pottery guilds, rural villages, wheat windmills and smelters on iron/copper RGOs.
- Once-only, ownership-checked first-month RGO expansion rises from 70 to 387 levels across the larger map.
- New RGOs: 2 gold, 3 silver, 2 dyes, 2 saffron, 1 silk, 1 pearls and 2 alum. New food/timber/material districts support basic demand; original districts retain their resources. Native gold ID: goods_gold.
- Ironfang: strongest eligible adult Ashborn man within the ruling dynasty inherits. Military ability decides, with Administration and age breaking ties. Unrelated courtiers cannot inherit through this law; no eligible dynasty member means no eligible heir.
- Native country naming follows the reigning house after a takeover or dynasty reassignment; succession hooks and monthly reconciliation cover changes. Regents do not rename the country. Shatterfin keeps maternal seniority.
- Starting ruler ages vary: Cindermaw 38, Brackmaw 36, Reefhook 27, Shatterfin 39 and Sootwake 29. Consorts and courtiers also have varied birthdays. Family birth dates retain plausible parent ages and adult dynastic heirs (brothers for the younger rulers). Shatterfin keeps four eligible adult women and maternal seniority.
- A native character auto modifier gives all five Ashborn cultures +15 years of life expectancy, including future characters and goblins employed abroad; human characters receive no species bonus.
- Retains 0.5.3 human portrait isolation, working shared-pose infantry, recruitment art and first-contact events.

| Clan | Starting population | Increase over first 0.5.4 pass |
|---|---:|---:|
| Cindermaw | 552,739 | 50.15% |
| Brackmaw | 318,463 | 51.16% |
| Reefhook | 108,437 | 209.23% |
| Shatterfin | 213,487 | 502.36% |
| Sootwake | 101,629 | 204.52% |

Installed Europe reference medians: 520 map pixels/location, 2,626 pixels/province and 5 locations/province. The new districts use this spatial scale as a reference while preserving the islands' smaller political units.

Volcanic/hydrothermal seams explain gold, silver and alum; reeds/lichens supply dyes; drained sheltered volcanic plots grow saffron. Knifeback has a small cultivated silk grove and Reefhook has pearl-diving grounds. These are fictional resources appropriate to the setting.

Extra production capacity is not guaranteed profitability. Food, employment, balance and succession require gameplay acceptance. Use the matching 0.5.4 package and installer.



## Install

1. Download `Goblins_Ashborn_Isles_0.5.4.zip` and extract it into a fresh writable folder.
2. Close EU5 and double-click **Install-Goblins.cmd**. The installer reconstructs and verifies terrain, backs up the previous installation and installs the full mod.
3. Enable **Goblins of the Ashborn Isles** alone for initial testing, restart EU5 and start a **new 1337 campaign**.

The normal installed folder is `Documents\Paradox Interactive\Europa Universalis V\mod\goblins_ashborn_isles`. If game detection fails, run `Install-Goblins.ps1 -GamePath "YOUR EU5 GAME DIRECTORY"`. A custom user-data location can be selected with `-UserDataPath`. Allow roughly 4 GB of working space.

GitHub **Code > Download ZIP** on the release branch also works: extract it and run the same installer. The compact payload requires terrain reconstruction; do not manually copy the authored `mod` directory. Use `-PrepareOnly` to prepare full content without installing it.

## Clans

| Clan | Culture | Capital | Population | Ruler age |
|---|---|---|---:|---:|
| Cindermaw | Emberblood | Hooktooth | 552,739 | 38 |
| Brackmaw | Brineward | Brackhaven | 318,463 | 36 |
| Reefhook | Reefstrider | Reefhook | 108,437 | 27 |
| Shatterfin | Stormfang | Shatterfin | 213,487 | 39 |
| Sootwake | Ashveil | Sootwake | 101,629 | 29 |

King Drogg Cindermaw bears the nickname **the Stone Fletcher**. Jaima Shatterfin, **the Mare-Mother**, leads the Tidemothers. All five cultures have their own personal, house and lowborn name pools and authored royal families.

## Succession

Four clans use Ironfang Monarchy and Rule of the Strongest: the strongest eligible adult Ashborn man in the reigning dynasty inherits. Unrelated courtiers are excluded. An exhausted eligible dynasty requires the native crisis or alternative-law path; the law does not silently admit outsiders.

Shatterfin uses Tidemother Monarchy and maternal dynastic seniority. The oldest eligible adult Stormfang woman of the ruling dynasty inherits; her mother must belong to the same dynasty. Skritcha is the initial eligible successor. Children born to women of that house inherit the maternal dynasty while the law is active. Normal monarchy law controls remain available.

Country names follow the reigning dynasty after a takeover or reassignment; regents do not rename a country.

## Art and exploration

Goblin portraits and infantry follow the five Ashborn cultures, including goblins employed abroad. Human cultures remain isolated. The 0.5.3 infantry shared-pose attachment repair passed the user's visibility/crash test on October 6, 2026; visual refinement remains tracked in [issue #4](https://github.com/stonefletcher/eu5-goblins-ashborn-isles/issues/4). Portrait fit and wider animation coverage still require testing.

Each clan starts with knowledge of the Ashborn land and sea areas. Optional eastern, northern and southern voyages reveal coastal routes and ports. Current owners of visited ports discover the islands and receive a once-per-country first-contact event. The 0.5.5 expansion chain and dedicated foreign invasion ambitions are not included.

## Steam Workshop

Use the package and installer above, then upload the **installed full mod folder** to the [existing Workshop item](https://steamcommunity.com/sharedfiles/filedetails/?id=3814944518). Paste `STEAM_DESCRIPTION.txt` and `STEAM_CHANGELOG.txt`; select `.metadata/thumbnail.png` for the preview. See [WORKSHOP_UPLOAD.md](WORKSHOP_UPLOAD.md). GitHub publication does not upload to Steam.

## Build and validation

Python 3.11+, NumPy and Pillow are required for a full build against a licensed matching EU5 installation:

```powershell
python -m pip install -r requirements.txt
python tools/build.py --game "YOUR EU5 GAME DIRECTORY"
python tools/package.py
```

Generated content goes to `build/goblins_ashborn_isles`, reports to `build/reports` and packages to `dist`. Game-derived full terrain caches are excluded from authored source tracking.

`python tools/verify_prepared_bundle.py` verifies the transported package without EU5: archive hashes/CRC, version/config agreement, terrain payloads, actual packaged populations and ruler ages, and authored art. Release publication refreshes package documentation without changing gameplay assets and repeats this verification.

Static checks do not establish long-term economic balance, engine rendering, succession edge cases, multiplayer or achievement compatibility. Other map, terrain-shader and starting-world mods may conflict, including Crusader States without a compatibility build. Follow [TESTING.md](TESTING.md).

Historical changes are retained in [RELEASE_NOTES.md](RELEASE_NOTES.md). Previous versions remain on their own release branches and tags. Europa Universalis V and its assets belong to Paradox; infantry sources and licensing are documented under [art/models/goblins](art/models/goblins/README.md). Banner and thumbnail were created with image generation.
