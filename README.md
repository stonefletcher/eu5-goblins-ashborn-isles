# Goblins of the Ashborn Isles

Five goblin kingdoms share six volcanic islands in the Atlantic. Unite their rival crowns, chart the waters beyond your homeland, and claim a foothold on Europe's coast in **Europa Universalis V**.

![The five Ashborn clans gather beneath their banners](art/events/sources/gathering.png)

**Current build: 0.5.5 — The Gathering of the Five (testing prototype).** This update is an add-on for the **0.5.4 base mod**, built for **EU5 1.3.11**. It requires a **new 1337 campaign**. English text is included.

## Install and play

The base mod supplies the islands, countries and goblin characters. The prototype adds the Gathering campaign, expanded clan stories, mixed populations and new artwork. You need both.

### 1. Install the 0.5.4 base

If you already have a working 0.5.4 installation, skip to step 2.

1. Open the [0.5.4 release branch](https://github.com/stonefletcher/eu5-goblins-ashborn-isles/tree/release/v0.5.4) and choose **Code → Download ZIP**.
2. Extract the ZIP into a writable folder and close EU5 completely.
3. Run **Install-Goblins.cmd** from the extracted folder. Let it finish preparing and installing the mod.

Use the installer rather than copying the mod folder by hand: it prepares the terrain for your game installation. Allow roughly 4 GB of working space. It installs under your EU5 user-data folder and leaves Steam's game files alone.

### 2. Install the 0.5.5 prototype

1. Open the [0.5.5 staging branch](https://github.com/stonefletcher/eu5-goblins-ashborn-isles/tree/staging/0.5.5) and choose **Code → Download ZIP**.
2. Extract it into a separate folder. Keep EU5 closed.
3. Run **Install-Prototype-055.cmd** from that folder.
4. In your EU5 playset, enable **Goblins of the Ashborn Isles** and **Goblins 0.5.5 - Gathering Prototype**. Place the prototype after the base mod in load order so its changes take precedence.
5. Restart EU5 and start a **new 1337 campaign** as any of the five goblin kingdoms.

Use **Install-Prototype-055.cmd** for this update. The regular **Install-Goblins.cmd** on the staging branch still carries the older base package; it does not install the 0.5.5 update by itself. The prototype installer requires the installed base to report version 0.5.4.

## Choose your clan

All five kingdoms can lead the Gathering. Their courts, cultures and starting positions give each a different story.

| Kingdom | Ruler | What defines it |
|---|---|---|
| **Cindermaw** | Drogg, the Stone Fletcher | The largest kingdom. Emberblood forges, muster yards and volcanic defenses support Drogg's claim to lead the Isles. |
| **Brackmaw** | Murgash, the Sluice-King | Brineward marsh engineers and harbor workshops. Murgash builds influence through provisions, waterways and carefully remembered debts. |
| **Reefhook** | Skrezz, the Wreck-Taker | Reefstrider pilots, fishing households and pearl divers. Skrezz balances rescue obligations, salvage and foreign friendships. |
| **Shatterfin** | Jaima, the Mare-Mother | Stormfang crews and a maternal royal house spanning two islands. Jaima bargains for security while preserving her family's succession. |
| **Sootwake** | Snikh, the Blackbough | Ashveil woodland settlements, charcoal hearths and guarded forest paths. Snikh defends the groves that sustain his people. |

The Isles begin with **1,618,696 goblins across 72 districts**. All five Ashborn cultures live throughout the archipelago, alongside each kingdom's majority culture. Port communities, free workers and enslaved populations reflect generations of migration and raids.

Four kingdoms use **Ironfang Monarchy**: the strongest eligible adult Ashborn man within the ruling dynasty inherits, with administration and age breaking ties. Shatterfin follows **maternal seniority**, with Jaima's sister Skritcha initially next in line. Kingdom names can follow a new ruling dynasty.

For the families, rivalries and origins behind each crown, read the [Ashborn lore](LORE.md).

## Your campaign

### Gather the Five

Early in the campaign, **The Gathering of the Five** brings the kingdoms into a shared struggle for leadership. Offer alliances, send paid aid, negotiate voluntary vassalage, or pursue conquest through normal EU5 warfare. Other rulers can refuse your offers.

To complete the Gathering, all **72 homeland districts** must belong to your realm through direct ownership, qualifying vassals or a union in which you hold the senior crown. An alliance alone does not unite the Isles, and occupying a district during a war does not count as owning it.

Each kingdom receives its own introduction. Shatterfin also has a family council event about the maternal house. These stories accompany your decisions; they do not automatically settle treaties or change succession laws.

### Explore the Atlantic

Your country initially knows the Ashborn homeland and its surrounding waters. Optional voyages open routes east toward Iberia, north toward Biscay and the English Channel, and south toward northwest Africa.

Expeditions cost gold and take time. Each kingdom develops its own charts. When your explorers reach a foreign coast, its owners also discover the Ashborn Isles.

### Pursue the Eastern Hunger

Once the homeland is united, **Eastern Hunger** turns your attention to Europe. Pay to prepare your fleet, then select a discovered European coastal province as a conquest objective.

The preparation costs **20 gold** and temporarily improves transport construction costs and naval morale. Choosing an objective costs **10 gold** and grants a temporary conquest casus belli (a reason to declare war) for use through the normal declaration and peace process. You must build your fleet, fight the war and secure the harbor yourself.

Holding a qualifying European coastal foothold completes the situation. Keep the homeland united: losing that unity blocks further eastern actions and use of the special casus belli.

## What is new in 0.5.5?

- **Two connected situations:** the Gathering and Eastern Hunger, with seven diplomatic and military actions.
- **Expanded clan stories:** five distinct introductions, revised ruler identities and Shatterfin's maternal-house follow-up.
- **Mixed populations:** 323,941 additional goblins from minority Ashborn cultures spread across the Isles.
- **Custom artwork:** 17 original paintings cover all 21 authored events. Both situations have their own headers and icons.
- **Five matching clan flags:** a black volcano on rust orange, ivory reeds on olive, a curling wave on teal, a shark and waves on blue, and a spiked helmet on charcoal.

The base mod also includes custom goblin portraits and infantry, volcanic terrain, coastal settlements, local industries and exploration events.

## Compatibility and troubleshooting

**This is a testing build.** Automated script, artwork and installer checks have passed for the prototype. In-game acceptance of its situation UI, new artwork, AI behavior and balance is still pending. Achievements and multiplayer have not been verified.

Other mods that change the map, starting world or terrain shaders may conflict. For a first test, use a playset containing just the base mod and this prototype. A game update may require a matching mod build.

| Problem | What to check |
|---|---|
| The prototype installer says the base is missing or has the wrong version | Install the 0.5.4 base first. The add-on requires that exact base version. |
| The Gathering, new flags or updated populations are missing | Enable both mods, place the prototype after the base, restart EU5 and start a new campaign. |
| Installation fails when run from a ZIP | Extract the complete download first, then run its installer from the extracted folder. |
| The map or terrain looks wrong after an update | Check the game version and reinstall the matching base through its installer. Avoid manually copying unprepared terrain files. |

To return to 0.5.4, disable the prototype and use a base-only save or start a new campaign. To play vanilla, switch to a playset without either mod and restart EU5. Keep prototype saves for use with the prototype enabled.

Report problems through [GitHub Issues](https://github.com/stonefletcher/eu5-goblins-ashborn-isles/issues). Include your game and mod versions, enabled mods, chosen clan, campaign date, and the steps that caused the problem. A screenshot, relevant save and EU5 `logs/error.log` help reproduce it.

## More information

- [Origins, cultures and royal families](LORE.md)
- [Release history](RELEASE_NOTES.md)
- [Detailed prototype rules and installation options](PROTOTYPE_055.md)
- [Playtesting checklist](TESTING.md)
- [Event artwork sources and export details](art/events/README.md)
- [Clan flag sources and export details](art/flags/README.md)

Europa Universalis V and its game assets belong to Paradox. This is an unofficial fantasy mod. Event paintings were created with image generation; editable clan emblems and artwork provenance are included in the linked art documentation.
