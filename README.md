# Goblins of the Ashborn Isles

**Version 0.6.0 — Giltfang, the Quiet Road and six goblin crowns.**

[Download 0.6.0](https://github.com/stonefletcher/eu5-goblins-ashborn-isles/releases/tag/v0.6.0)
| [Steam Workshop](https://steamcommunity.com/sharedfiles/filedetails/?id=3814944518)
| [Release notes](RELEASE_NOTES_0.6.0.md)

An Atlantic fantasy homeland for Europa Universalis V: rival goblin crowns,
volcanic islands, harbor diplomacy and voyages toward foreign shores.

## What changed in 0.6.0

Giltfang joins the Ashborn as the sixth crown, ruled by Vrekk the Brass-Tooth.
Its main island and Tolltooth have a combined land area about 10% smaller than
Brackmaw. Chainhaven has its own market, alongside Hooktooth's southern market.
All goblin crowns begin knowing each other's lands and the surrounding waters.

Lantern Cay is a new Cindermaw outpost with three districts and 18,000 people.
The Quiet Road links north and south through ordinary coastal water, with an
opened eastern approach and reworked current tiles. The archipelago now has
nine islands, 97 districts, 28 coastal sea tiles and 75 ports.

All six crowns take part in shared events, diplomacy, religion and unification.
Ashborn Voyages has its own situation. Harbor prompts wrap, choices show costs
and rewards on hover, requirements use readable conditions, and signed bargains
remind both partners of the payment, service, benefit, burden and duration.

All eighteen starting projects cost 25 gold, from a 100-gold starting treasury.
Food bonuses explicitly increase province food storage limits. Select a
location, hover the province food display, then hover its stockpile total to
see storage capacity and modifiers; this bonus does not increase production.

Clan flags now explicitly select their authored emblems. Giltfang's flag is a
brass fang and chain links on dark blue. A one-time monthly repair also fixes
saved procedural placeholders after restarting and loading an existing 0.6.0
save. The flag repair alone does not require another new campaign.

Giltfang has its own court, culture, names, opening story, flag and artwork.
The new Gathering painting seats six envoys. Previous portrait, skin, hairstyle,
Drogg, wardrobe and holy-site fixes remain included. The Ashen Covenant now
has twelve sacred sites across the islands.

## The six crowns

| Crown | Culture | Capital |
|---|---|---|
| Cindermaw | Emberblood | Hooktooth |
| Brackmaw | Brineward | Brackhaven |
| Reefhook | Reefstrider | Reefhook |
| Shatterfin | Stormfang | Shatterfin |
| Sootwake | Ashveil | Sootwake |
| Giltfang | Cinderweight | Chainhaven |

Unite the homeland through conquest, vassalage or senior unions in the Gathering.
Negotiate paid Harbor Bargains and Compact charters, develop specialized island
economies, and follow Ashen Covenant stories and rites. Ashborn Voyages charts
Iberian, northern and northwest African shores; the Eastern Hunger then offers
preparation and objectives for a European foothold through normal EU5 warfare.

## Install and play

Built for **EU5 1.3.11 (Pavia)**. Start a **new 1337 campaign** when upgrading
from 0.5.x. Older saves retain the previous world map and starting setup.

1. Download the complete installer ZIP from the release above and extract it.
2. Close EU5 and run **Install-Goblins.cmd** from the extracted folder.
3. Enable only one Goblins copy, disable the old Gathering Prototype add-on,
   restart EU5 and start your campaign.

The installer retains a backup outside the active mod folder. For the source
download, the same top-level installer reconstructs the matching bundled
release. If the game is not found automatically, run Install-Goblins.ps1 with
its `-GamePath` parameter pointing to your EU5 game folder.

Steam subscribers receive the same runtime through the existing Workshop item.
Other mods that change terrain, the map or starting setup may conflict. Keep
separate saves; switch to an unmodded playset and restart to return to vanilla.

## Validation and current limits

Source, metadata and installer all target **0.6.0**. Static checks cover the map,
native references, textures, six-crown event scenarios and the flag repair.
They include 132 project cases, 60 directed harbor-service cases and 575 shared
terrain borders with zero measured seam error. The release gate uses an exact
clean Git export, a fresh isolated installation and all 1,974 runtime hashes.

These checks are separate from gameplay acceptance. Sailing, actual market
trade, UI layout, flag rendering and save/reload behavior still need in-game
confirmation. Multiplayer and achievements are unverified. Dedicated foreign
invasion objectives and fear mechanics are not included.

## Source and feedback

- [Player guide](PLAYER_README.md)
- [Origins, cultures and royal families](LORE.md)
- [Release history](RELEASE_NOTES.md)
- [Playtesting checklist](TESTING.md)
- [Artwork sources](art/events/sources)
- [Report a problem](https://github.com/stonefletcher/eu5-goblins-ashborn-isles/issues)

Include your version, clan, enabled mods, campaign date and reproduction steps.
Screenshots, a relevant save and the game's error log help diagnose problems.

Original setting and development by Stonefletcher. Base goblin infantry model:
Quaternius, Ultimate Animated Character Pack (CC0). Paintings, banner and
thumbnail use AI-generated artwork. Europa Universalis V and its original
assets belong to Paradox Interactive. This is an unofficial mod.
