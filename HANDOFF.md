# 0.6.0 staging handoff

Checkout: C:/Users/alexa/Documents/Codex/2026-10-07/0/work/goblins-059
Branch: staging/0.6. Verified package commit: 5539bb3.
Source binding: 3695698f8a4a426a49f5807ada5b1ad99e83702e.
Remote: https://github.com/stonefletcher/eu5-goblins-ashborn-isles.git
User explicitly requested pushing all current work to a0.6 staging branch.
The package uses semantic version0.6.0; the branch is staging/0.6.
Publication target is origin/staging/0.6. Verify the remote head when resuming.
No main merge, release tag, GitHub release or Workshop update is authorized.

## Included
- Current local0.5.9 candidate carried forward without gameplay changes.
- All five clans start100gold (previous50/35/20/20/20), based on explicit native
  small-country setups. New campaign required. Existing saves receive no top-up.
  Opening projects remain10gold; AI reserve20; war actions and incomes unchanged.
- Event optimizations, script/price/name/opinion fixes, native model texture
  registration, original art checks and cleaned player package.
- Three mutually exclusive5yr projects per clan plus free decline; distinct opening
  choices,110project checks. Previously received effects and intro state preserved.
- Harbor Bargains: paid10gold provisions/pilots, one15gold counteroffer, boundedAI,
  reciprocal5yr effects, one slot,180day talks, quiet/pair locks and safe replies.
- Compact: completed5yr bargain +3yr observed alliance;150opinion, strength<=.65,
  rank/peace/independence checks. Client chooses charter, patron agrees, client ratifies.
  Autonomy half tribute/min20yr integration/speed.5; Protection normal tribute/min10yr,
  no offensive calls, defence/upkeep tradeoff. Houses/succession/ownership count retained.
- Both situation panels show qualifying homeland progress out of72; Compact reasons
  remain visible for disabled crowns. Monthly history observation limits documented.
- Covenant12stories: two approaches and neutral defer; bounded costs/3yr replacing
  effects, no prestige, same eligibility/cadence; conversion cleanup and stale guards.
- Exploration: status/time ranges, explicit departure terms, six-month reminders or
  persistent manual mode, own-country review button on active AND ended panels.
  Arrival-owner reports, one foreign contact notice, no overlapping/double charges.
  Legacy pending/paid/open-return compatibility.36month initial,5/10/10gold,4/6/6month
  travel,12month rest preserved. New discovery settles on arrival, old open reports
  on acknowledgement. No new events/pulses/world scans.

## Validation and installer
All existing gameplay script simulations, native map/art/model checks pass.
10exploration groups,74Covenant groups,110project cases,28Compact,22Harbor and
16homeland progress cases. Real engine behavior/save-reload/visuals/FPS still pending.
Terrain reused only after verifying all final hashes; no terrain/setup input changed
in the version promotion. Source/metadata/overlay/terrain/report are0.6.0.
Clean exact export: E:/CodexScratch/Goblins060Staging20261007/source
Isolated profile: E:/CodexScratch/Goblins060Staging20261007/profile
Preparation, embedded install and all 1,664 file hashes PASS.
Bundle/source hash, CRC, delivered treasury checks and stale-source rejection PASS.
Archive: Goblins_Ashborn_Isles_0.6.0.zip (213,040,998 bytes)
SHA-256: 1114703f7673c0bb08efd9254b03ddc173a90d693782919ebf274ef3c377de33
Outputs contain0.6.0 ZIP, receipts and task list. Active profile unchanged.

## History and remaining work
Original development history preserved on local staging/0.5.9 and
archive/0.6-prepublication. staging/0.6 uses a snapshot of the same source tree to
avoid uploading roughly3GB of superseded intermediate installer objects.
No unapproved project discounts, AI reserve reduction or war-action changes.
Next proposals: subjugation access/clarity if desired, overseas consolidation,
foreign reactions. First playtest100gold openings and existing features.
Unresolved log leads: ambiguous map location, sea-effect locator bounds, reserved
Covenant variables. Mesh hypothesis still needs fresh engine evidence.

## Local tools
Python: C:/Users/alexa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe
Game: E:/SteamLibrary/steamapps/common/Europa Universalis V/game (1.3.11).
build/ junction: E:/CodexScratch/Goblins059Scripts20261007/build.
Install verifier: ../verify_060_install.py. Release helper: ../deliver_060.py.
verify_059.py now reads version from output metadata; its historic module/report-key
name remains to preserve existing tooling. Full build needs current0.6.0 config.
exploration_progress.FILES feeds the49-file prototype manifest; main overlay1573files.
Snapshot source and bundle must stay aligned. Follow eu5-modding clean-export gate
before future staging handoffs/pushes. No subagents. Never bypass running-game check.
Earlier scratch cleanup denied by auto-review; preserved. Use fresh E:scratch.
