# Goblins of the Ashborn Isles

**0.6.0 staging candidate — branch `staging/0.6`.**

This combined 0.6.0 candidate includes the earlier portrait material, wardrobe,
hair and Drogg fixes, nine holy sites with varied importance, and the five-crown
standings panel alongside all 0.5.9 gameplay and optimization work. The initial
0.6.0 staging package accidentally used an older base for those features; this
replacement restores them without reverting Harbor Bargains, Compact talks,
opening projects, Covenant stories, voyage controls or the 100-gold starts.
Ear attachments again use the native skin material and head-decal routing.
Static and packaged regression checks cover both generations of changes;
in-game ear colour and panel layout still require visual confirmation.
Reinstall this corrected 0.6.0 package with EU5 closed. Portrait fixes apply after
restart; use a new campaign to test starting gold and the complete starting setup.

Included gameplay:

- 100 starting gold for every Ashborn clan; a new campaign is required for the new treasury.
- Three opening projects per clan, distinct opening benefits and story-specific Covenant tradeoffs.
- Paid Harbor Bargains and negotiated Compact charters with eligibility checks and safe replies.
- Homeland progress, clearer diplomacy requirements and exploration status/manual voyage controls.
- Event-work reductions, script and model registration fixes, and a cleaned player package.

Source and the bundled installer use the same 0.6.0 version. The release gate checks
the exact Git export, isolated installation and delivered file hashes. These checks
do not establish in-game performance, visual acceptance or actual save/reload behavior.
GitHub releases, the default branch and Steam Workshop are separate from this staging branch.


Loading cleanup: register all seven action prices and their cost labels; resolve
the Covenant language to the existing Cindermaw dialect; register the
Harbor Bargains AI actions with eligibility and reserve checks; repair unavailable-target icons and longevity text;
deduplicate shared character names. Opinion bonuses now use their stated
fixed durations (supplies five years, pacts/oaths ten) without conflicting
annual decay. Legacy opinion modifiers remain available for existing saves.

All five Ashborn clans now start with 100 gold in new campaigns, replacing
Cindermaw's 50, Brackmaw's 35 and the other clans' 20. This uses the explicit
100-gold setup of small vanilla countries such as Oneida, Onondaga and Cayuga as
a benchmark; it is not a claim that every vanilla country starts with 100.
Project prices, AI reserves, recurring income and war actions are unchanged.
Existing saves retain their current treasury; start a new campaign for this change.

Exploration now shows preparation, pending decisions, the route at sea with a
remaining-time range, crew rest and completed charts on both Ashborn situation
panels. Review Ashborn Voyages reopens available routes, including from ended
panels. Offers show the price, duration, destinations and reciprocal discovery
before payment. Choose a six-month reminder or stop reminders and commission
manually. Stops persist across voyages; choosing a six-month reminder restores
automatic offers. Arrival reports record the current owners of visited ports.
Discovery and the 12-month rest now begin on arrival, without waiting for the
report to be dismissed. Prices (5/10/10 gold), travel (4/6/6 months), first offer
(36 months) and limited coastal discovery remain unchanged. Duplicate and stale
replies cannot charge again or alter a later voyage. Older paid voyages still
complete; an already-open older return message settles when acknowledged.
Generated-script regression checks pass; GUI and real save/reload playtests remain.

Covenant stories now offer two competing approaches and a neutral defer option.
Each story has specific costs and effects instead of the repeated gold/Favor/prestige
template. Funded approaches cost 5 gold; AI retains 20. Practical alternatives may
cost Favor or carry temporary estate, tolerance or military drawbacks. Effects last
three years and replace earlier story consequences. There are no story prestige
rewards. Defer changes no resources or modifiers and schedules no follow-up; the
existing three-year cooldown and event frequency remain. Major rites, religious
traditions and the Moot settlement are unchanged. Old pending popups without a new
session token can only be deferred safely. In-game balance and save/reload need testing.

All five clans now receive three mutually exclusive projects plus a free keep-the-gold
option in their existing introduction. Every project costs 10 gold and lasts five
years; AI buyers keep 20 gold. Cindermaw chooses army morale, diplomacy or army
upkeep. Brackmaw chooses storage, production or fort defense. Reefhook chooses
naval recovery, fleet upkeep or diplomacy. Shatterfin chooses monthly sailors,
naval morale or diplomacy. Sootwake chooses fort defense, production or storage.
Benefits are shown on each choice. Existing project rewards and already-seen
introductions remain unchanged; choosing one project blocks the other two.

Situation progress: both panels now show your qualifying realm's live homeland
location count out of 72, using the same ownership rules as unification. The
Gathering explains the Compact route. Its partner selector keeps existing crowns
visible when they fail requirements and explains bargain history, alliance age,
opinion, strength, rank, peace, pending offers and cooldowns. Annexed crowns and
your own crown are excluded. This changes presentation, not eligibility or balance.
History checks show whether the full term has been recorded; they are not an exact
days-remaining countdown. UI layout and responsiveness still need an engine test.

Harbor Bargains replace the cheap alliance offer with paid provisions or pilots.
A supplier can accept 10 gold, counter once with the other service for 15,
or refuse. Signed five-year contracts grant the buyer +10% food storage or
+5% naval morale recovery, while committing 5% storage or 2.5% recovery
from the supplier. Payment transfers only at signing. Both crowns need
25 mutual opinion and one free contract slot. AI retains 20 gold.
Talks expire after 180 days; pairs wait five years between approaches,
with a two-year quiet period for each crown. Hostilities, rivalry or a
vanished partner end the contract on the next monthly check, without refund.
No alliance is created; existing alliances remain. Saved old pact offers
close with their five-gold fee returned.

Compact talks now require a completed five-year Harbor Bargain with that crown
and three years of an alliance observed by the monthly check. These can overlap.
Both crowns must be independent and at peace; the prospective subject needs
150 opinion, no higher rank, and no more than 65% of the patron's strength.
In the Gathering situation, select Open Compact Talks and the eligible crown.
The smaller crown chooses its charter, the patron accepts or refuses, and the
smaller crown explicitly ratifies or withdraws. There is no negotiation fee,
instant prestige or loyalty reward. Ordinary alliance remains a valid alternative.

- Autonomy Charter: half normal base tribute, a 20-year minimum before annexation,
  then half normal integration speed. Normal offensive military obligations.
- Protection Charter: normal tribute and 10-year annexation minimum; exemption
  from offensive wars, +10% defensiveness, and protection against external attacks
  and fellow subjects. The patron bears -5% army maintenance efficiency.

Both charters retain the ruling house and succession customs, count toward
unification, and lock normal subject-type switching to preserve their terms.
They still impose limited diplomacy and the normal -20% subject cabinet efficiency.
Talks expire 180 days after invitation. Both crowns have a two-year quiet period;
the pair waits five years between approaches, restarted on a live refusal.
All eligibility conditions are rechecked before each agreement and ratification.

Existing alliances remain, but their three-year observation starts with this update.
Only new bargains carrying the full tracking record can earn completion credit;
older contracts are not credited retroactively. Monthly sampling can miss a brief
alliance break or hostility that begins and ends between checks. Old pending
Compact requests close with their ten-gold fee returned once, without submission.
Script and installation checks are separate from pending in-game acceptance.


Reefhook can restore its rescue beacons in its existing introduction: pay
10 gold for +5% naval morale recovery for five years, or keep the money.
The paid choice requires at least 10 gold. Already-seen introductions do
not replay, and no additional popup is added.

Brackmaw can now repair its sluices in its existing introductory event: pay
10 gold for +10% food storage capacity for five years, or keep the money.
The paid choice requires at least 10 gold. No additional popup is added.
Campaigns that already received the introduction will not receive it again.

The five goblin infantry bodies now register with EU5's native fixed-texture
attachment list. This addresses the missing texture-variation registration reported
by the engine. Geometry, palettes, animations and the shared-pose attachment route
are unchanged. Static checks pass; a fresh engine test must confirm the errors stop.

Approved opening-choice update: leadership grants +5% army morale, cooperation
+0.5 diplomatic reputation, and independence +10% defensiveness. Each lasts five
years and grants +5 prestige. Existing saves keep already-granted legacy modifiers
until expiry; the new benefits apply when choosing the opening event.

The Gathering monthly introduction pass now visits only the five goblin crowns.
The Covenant skips its 72-location ownership test after its one-time Moot;
conversion cleanup runs once instead of repeating monthly. Eastern actions use
a compact ownership tooltip and no redundant Crossing eligibility check.
All territory, vassal and union requirements remain in force.

The player ZIP includes runtime files, terrain patches, the installer, four player
guides and one validation receipt. Source paintings, proposals, Workshop publishing
files, previews and developer reports stay in the source checkout. The prepared
bundle is rebuilt cleanly, without obsolete archive entries or old transport chunks.

Includes the 0.5.8 portraits and tribal leather wardrobe. Art checks cover all 49
events, both situations, flags, infantry illustrations, portraits and native model
bindings. Static validation does not establish engine appearance or measured FPS.

Use `Goblins_Ashborn_Isles_0.6.0.zip`, extract into a fresh folder, close EU5 and run
`Install-Goblins.cmd`. Requires the matching EU5 1.3.11 installation. Enable one mod
copy. Test inherited world changes in a new 1337 campaign. Source-download installation
also uses the matching bundled 0.6.0 payload. Installation validation uses an isolated
profile; the active game profile is unchanged.

Validation: full build and clean-export/isolated-install gates are recorded in
HANDOFF.md. In-game timing and visual acceptance remain pending.

## Inherited economy and revised exploration

The first exploration offer waits **36 months after the first monthly country pulse**, roughly three years into a new campaign. All five crowns know nearby waters off Iberia, Biscay, the English Channel and northwest Africa. The 0.5.6 grants revealing Iberia and 24 coastal provinces have been removed in 0.5.7: foreign land remains undiscovered, rather than discovered beneath ordinary unit fog.

Voyages discover named harbors and establish foreign contact. The eastern journey costs five gold and takes four months; northern/southern journeys cost ten gold and take six months. Owners of visited ports learn about the Isles when the crews return. Six-month postponements, twelve-month breaks between completed voyages and once-only contact notices are retained. Existing saves do not lose discovered land or reset an initialized timer. The complete 0.5.7 payload includes these changes.

The first economic pass gives each crown a distinct role, with buildings scaled to its lore, geography and available workers. Starting infrastructure was compared with installed vanilla states including Serbia, Navarre, Scotland and Cyprus.

| Kingdom | Economic focus | Starting building levels |
|---|---|---:|
| Cindermaw | Tools, weapons and metalworking, supported by a broader rural economy | 47 |
| Brackmaw | Provisions, cloth and naval supplies | 36 |
| Shatterfin | Maritime industry, wharves and sailcloth | 16 |
| Reefhook | Fishing, pearls and harbor trade | 12 |
| Sootwake | Timber, charcoal and small repair industries | 12 |

**Hooktooth starts with one full market**, intended to support trade between the specialized island economies. Actual market membership and access still need in-game verification. Separate national markets have not been added.

Rural buildings follow local resources and vegetation. Additional extraction investment is reduced from 387 to 126 across the Isles, particularly at precious-goods deposits and previously oversized sites. These are bonuses to native capacity, not total output or treasury income. All **1,618,696 people, population classes, 72 districts, resources and geography** are preserved.

Focused checks passed for native building ranks/resources, generated buildings, population totals, production staffing, economic specialization and guarded market/investment setup. Profitability, food security and affordability of starting forces remain pending fresh-campaign tests. Building-level counts describe infrastructure, not equivalent income.

See the [0.5.6 economic design and validation notes](ECONOMY_056.md) for comparisons, trade dependencies and the playtest checklist. These economy changes are inherited by the complete 0.6.0 candidate.

## Install the 0.6.0 candidate

Extract the 0.6.0 player ZIP into a new writable folder, close EU5 and run
Install-Goblins.cmd. Enable one mod copy and start a new 1337 campaign for world
changes. The installer validates terrain and backs up an existing installation.
Allow roughly 4 GB of working space. This local candidate has not been published.

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

**This mod is still in development.** Release packaging and automated validation are separate from gameplay testing. In-game acceptance of the situation UI, new artwork, AI behavior and balance is still pending. Achievements and multiplayer have not been verified.

Other mods that change the map, starting world or terrain shaders may conflict. For a first test, enable this full mod on its own. A game update may require a matching mod build.

| Problem | What to check |
|---|---|
| The installer cannot find EU5 | Run Install-Goblins.ps1 with its -GamePath option pointing to your EU5 game folder. |
| The Gathering, new flags or updated populations are missing | Check the installed version is 0.5.5, disable the old prototype add-on, restart EU5 and start a new campaign. |
| Installation fails when run from a ZIP | Extract the complete download first, then run its installer from the extracted folder. |
| The map or terrain looks wrong after an update | Check the game version and reinstall the matching base through its installer. Avoid manually copying unprepared terrain files. |

To play vanilla, switch to a playset without the mod and restart EU5. Keep modded saves for use with their matching mod version. The installer retains backups outside the active mod folder; restore an older version only with EU5 closed and use saves from that version.

Report problems through [GitHub Issues](https://github.com/stonefletcher/eu5-goblins-ashborn-isles/issues). Include your game and mod versions, enabled mods, chosen clan, campaign date, and the steps that caused the problem. A screenshot, relevant save and EU5 `logs/error.log` help reproduce it.

## More information

- [0.5.6 economy changes and validation](ECONOMY_056.md)
- [Origins, cultures and royal families](LORE.md)
- [Release history](RELEASE_NOTES.md)
- [Gathering rules and the earlier prototype](PROTOTYPE_055.md)
- [Playtesting checklist](TESTING.md)
- [Event artwork sources and export details](art/events/README.md)
- [Clan flag sources and export details](art/flags/README.md)

Europa Universalis V and its game assets belong to Paradox. This is an unofficial fantasy mod. Event paintings were created with image generation; editable clan emblems and artwork provenance are included in the linked art documentation.
