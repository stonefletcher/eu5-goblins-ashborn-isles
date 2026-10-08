# Goblins of the Ashborn Isles 0.6.0

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


Optimization candidate for Europa Universalis V 1.3.11.

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

1. Extract this archive into a new folder.
2. Close EU5 and run Install-Goblins.cmd.
3. Enable only one copy of Goblins of the Ashborn Isles.
4. Start a new 1337 campaign to test world/setup changes.

The installer verifies your game's terrain files, reconstructs the required terrain,
and preserves an existing mod in a backup outside the scanned mod directory.

This candidate includes the 0.5.8 portraits and leather wardrobe, reduces recurring
event checks, and removes development material from the player download.

Read RELEASE_NOTES.md for changes, TESTING.md for gameplay checks, and LORE.md for
the clans. Static checks do not prove in-game performance or visual acceptance.

Source and issues: https://github.com/stonefletcher/eu5-goblins-ashborn-isles

Model credit: Goblin_Male by Quaternius, Ultimate Animated Character Pack (2019),
CC0 1.0. Modified goblin geometry and clan palettes are included.
