# 0.5.9 optimization and gameplay handoff

Checkout: C:/Users/alexa/Documents/Codex/2026-10-07/0/work/goblins-059
Branch: staging/0.5.9. Verified package commit: 1848630.
Source binding: 9f8abf966f08431e8b75d420f7b2a66e286ac599.
User workflow: approve or shelf one proposed change, then implement and package it.
Latest explicit authorization: raise starting gold for all clans to a vanilla benchmark, instead of project discounts. Implemented and packaged.

## Completed
- Starting gold: data/island.json gives all five clans100 instead of50/35/20/20/20.
  Based on explicit native100-gold KKA/ONY/ONO/GYO/ONN starts, not a claim about
  universal engine defaults. Regenerated via build_setup into ../gold-setup-generated;
  compared whole10_countries file and proved only five gold fields differ, then
  copied that generated file to build. No unrelated setup/runtime changes.
  Projects remain10gold/AIreserve20; war actions, incomes, other resources unchanged.
  New campaign required; no saved-campaign top-up. Bundle verifier now checks all
  five configured treasury values against actual delivered country setup/report.
  User replaced proposed project discounts and lower AI reserve with this change.
- Exploration: status and native timer ranges on active AND ended Ashborn panels;
  owncountry Review Ashborn Voyages button. Clear prices/destinations/contact warning.
  Six-month reminders or persistent manual-only mode. Paused mode survives voyages;
  choosing six-month wait restores reminders. No new events/pulses/world scans.
  36-month initial delay, 5/10/10gold, 4/6/6months, 12-month rest unchanged.
  Arrival immediate reveals fixed coasts and informs current owners; saved report
  scopes retain arrival owners after conquest. One foreign contact notice per country.
  Serial+event token guards offer/launch/return/manual effect paths. Legacy pending
  offers and paid returns settle once; already-open old returns settle on acknowledgement.
  Legacy pending display is intentionally ambiguous because older saves lack timers.
  New module exploration_progress.py; regression verify_exploration_progress.py.
  Retained native setup verifier verify_exploration.py, now has read-only rebuild=False.
  10 scenario groups plus all prior regressions/native checks pass. Real GUI/engine
  save/reload/arrival scope persistence and performance acceptance still pending.
- Covenant: all12 recurring stories have two distinct choices and neutral defer.
  Funded options cost5gold, AI retains20; alternatives spend Favor or impose estate/
  tolerance/military drawbacks. All23 temporary story modifiers last3years, replacing
  earlier story consequences. No prestige. Defer changes no resources/modifiers,
  closes current story and leaves the normal3yr cooldown. Pool/frequency unchanged.
  Rites/aspects/sites/Moot unchanged. Serial+event token blocks stale/repeat grants;
  effect rechecks faith/eligibility/funds. Old pending popup lacks token: defer only.
  Conversion cleanup removes story effects/open flag, preserves serial. Native numeric
  modifier IDs and existing event illustrations verified. New module covenant_stories.py;
  verify_covenant_stories.py executes generated event options and cleanup.
- All five clans have THREE paid project alternatives plus free decline, each10gold,
  five years, AI reserve20. CDM army morale/diplomacy/army upkeep; QBR food storage/
  production/fort defense; RHK naval recovery/navy upkeep/diplomacy; SFK monthly sailors/
  naval morale/diplomacy; SWK fort defense/production/storage. Benefits on buttons.
  Shared one-off guard blocks every other project after purchase or decline.
  Existing modifiers/intro routing/SFK follow-up and succession preserved. No new
  events/pulses. Old CDM accounts .10 retained; new audit .05 remains separate.
- Item 1: live player homeland count on both situation panels using the actual ownership
  predicate; zero for dependent claimants. One 72-location read-only display per panel.
  Compact selector now keeps existing disabled crowns visible, uses native enabled
  checks and localized reasons for history, alliance, rank, opinion, strength, peace,
  pending talks and cooldowns. Fixed five-crown source supports restored countries.
  No balance changes or exact remaining-time countdown. GUI engine acceptance pending.
- Event optimization, original art/native model checks, mesh registration, loading
  registrations, cleaner player archive; distinct opening and Brackmaw/Reefhook choices.
- Harbor Bargains: 10-gold service or one counteroffer switching service for 15;
  five-year reciprocal effects, bounded AI with 20-gold reserve, 180-day expiry,
  two-year quiet period/five-year pair lock, nonce-isolated replies, monthly health.
- Compact: complete a new five-year bargain together plus three monthly-observed
  alliance years (overlap allowed). Both independent/peace/nonrival/nonenemy; target
  opinion150, strength<=.65, no higher rank. Smaller crown chooses charter, patron
  accepts, smaller crown ratifies. Only final ratification creates a subject.
- Autonomy: half normal base tribute (.1 vs native .2), integration minimum20years,
  speed.5. Protection: normal tribute/min10years/speed1, no offensive calls,
  +10% subject defence, -5% patron army maintenance efficiency; patron protects
  against external attacks and fellow subjects. Both retain house/customs, limited
  diplomacy/-20% cabinet efficiency, count for ownership and lock normal type changes.
- No fee/prestige/loyalty/opinion reward. Free refusal at every stage. 180-day talks,
  two-year quiet/five-year pair locks. Immutable scopes+serial prevent stale grants.
- Old event3 refunds10 once, grants no subject. Existing relations retained.
- New bargains record full term and reciprocal partner; old contracts get no history
  credit. Alliance tracking begins now. Monthly sampling can miss short break/re-form
  or hostility changes between checks; disclosed in guides.
- Generators: gathering.py, harbor_bargains.py, compact_talks.py. Generated mod/build
  runtime and 49-file prototype manifest match. Added subject_types file; 12 scripts,
  29 Gathering events, 49 total events, eight custom prices. Unchanged art/terrain.

## Validation and delivery
10 exploration scenario groups plus74 Covenant groups plus110 early-project checks plus28 Compact +22 Harbor generated-script simulations,16 ownership/progress cases pass.
Disabled crown visibility, tooltip references and generated progress equivalence checked.
Native subject/modifier/tribute fields and all49 event art refs checked; full portrait,
flag/model/Covenant checks pass. Simulations are NOT engine playtests.
Clean exact export: E:/CodexScratch/Goblins059Gold20261007/source
Isolated profile: E:/CodexScratch/Goblins059Gold20261007/profile
Top-level preparation and embedded installer PASS; all 1,664 hashes match.
Stale-source rejection PASS. Archive 213,040,892 bytes; SHA-256:
008aa6f9cf2db38f0acf7102bfe2e27d308eed0f0b1b18f76bdfdf43ac6a7805
Outputs ZIP/receipts, Starting Gold guide and approval queue updated; copied archive hash verified.
No active-profile install, game launch, push or publication performed.
Engine behavior, actual save/reload, AI pacing, visual acceptance and FPS pending.

## Next proposed approval
Subjugation access/war-action clarity, if desired; no changes authorized. Playtest100-gold openings before further economic tuning.
Other queued work: smaller-clan balance/subjugation-CB review,
overseas consolidation and foreign reactions. In-game acceptance/performance pending.
Project discounts/AI reserve reduction replaced by starting gold; war changes not approved. Unresolved log leads: ambiguous map key, sea-effect locator bounds,
reserved Covenant variables. Mesh evidence ../mesh-registration-evidence/error-before.log.

## Local build notes
Python: C:/Users/alexa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe
Game: E:/SteamLibrary/steamapps/common/Europa Universalis V/game (1.3.11).
build/ junction: E:/CodexScratch/Goblins059Scripts20261007/build.
Earlier scratch deletion denied by auto-review was NOT retried; use fresh E: scratch.
Install verifier: ../verify_gold_install_059.py. A residual native LASTEXITCODE
can be nonzero even after installer success; inspect output and run hash verifier.
Never bypass running-game gate. No subagents. Packaging must follow skill clean
export/isolated install gate after future packaged edits. Reuse unchanged terrain.

Progress generator/check: tools/situation_progress.py and verify_situation_progress.py.
Native evidence: generic_actions/readme.txt enabled/show_why_not_enabled,
localization_commands ScriptValue, io_policy save_temporary_scope_as, common GUI inheritance.

Early project generator/check: tools/early_projects.py and verify_early_projects.py.
Native global_sailors_modifier is monthly sailor gain, not maximum sailors.

Covenant files are built by ashen_covenant.build for mod and build output. Its localization
participates in main_overlay.json; refresh that entry hash after future text changes.

Exploration native evidence: generic_actions/readme.txt owncountry/action_button_default;
customizable_localization/customizable_localization.info first valid + fallback;
native event localization SCOPE.sCountry saved-name access. Native situation common.gui
hides main body when ended, so custom panel_header includes conditional ended controls.
exploration_progress.FILES feeds prototype collector (49 files), build and bundle tests.
Existing main-overlay exploration entries have refreshed hashes. Two new runtime files
are generic action and customizable localization; 1,664 installed files total.
