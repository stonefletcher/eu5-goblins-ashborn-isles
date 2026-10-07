# 0.5.6 event fixes handoff

Checkout: C:/Users/alexa/Documents/Codex/2026-10-07/cr/work/goblins
Branch: fix/0.5.6-event-performance-localization, based on staging/0.5.6 economy source.
Goal: address 0.5.5 Seat Among Five slowdown and unnamed option modifiers.

Completed: native localization keys for all six Gathering modifiers; concise custom tooltips around three situation predicates, with original conditions intact; regenerated source output and additive manifest. README and TESTING document evidence and runtime checks. Artwork compared with installed base game and installed mod: 1080x440 DXT1/11 mips/317512 bytes, identical native payload size; no image reduction justified. User confirmed the Situation Panel triggers the near-crash. Captured six rotating logs under ../diagnostics: 25,367 lines / 5,352,439 bytes, all Gathering can_end scope-description warnings. Initial snapshot had only 414 such warnings.

Checks passed: verify_055 (14 ownership scenarios, native references, six modifier names/descriptions, exact wrapped predicates); verify_event_art (21 DDS decode/hash/manifest checks). No runtime test; tooltip performance diagnosis remains a hypothesis.

Build/install/publish: source fixes only. Existing bundled installer and release metadata remain 0.5.5. No game launch, install or package. User authorized publishing this fixes branch to GitHub. Economy work retained from base. Next: integrate this branch with other 0.5.6 work, build the complete release, run required clean-download gate, then test popup responsiveness and logs in EU5.


One Fire, Many Blades now offers a shorter council scene with three five-year bonuses: Grask's drills (+5% land morale), Kragga's envoys (+0.5 diplomatic reputation), or Grakka's accounts (+10% army maintenance efficiency). This introduction is independent of the opening Gathering choice. Native personality_events.10 provides the alternative five-year reward pattern; native the_rule_of_god includes 5% land morale, and modifier definitions confirm maintenance efficiency is positive-benefit. Existing once-only monthly routing is preserved. Generator, profile, generated outputs and manifest updated. Native-reference/ownership and art checks passed. Runtime acceptance pending. Source-only branch; no install. User authorized GitHub push.


The blank Situation Panel had a separate source omission: neither custom situation had its required ID-named GUI layout. Added ga_gathering_of_five.gui and ga_eastern_hunger.gui under in_game/gui/panels/situation, authored by gathering.py. Installed native GUI readme requires these files; layouts inherit situation_panel from common.gui, retaining artwork, dates, scrolling, ended-state handling and situations_actions. Custom content adds localized description and completion requirements. Both are included in the additive manifest. Static native-template, layout presence, localization, ownership and art checks passed; engine rendering and actual action visibility remain untested.


0.5.6 packaging repair in progress: includes staging exploration pacing and starting Atlantic charts alongside economy, situation panels, tooltip fixes and Cindermaw choices. Complete installer validation pending.
