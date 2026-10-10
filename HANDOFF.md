# Introduction and Covenant tooltip fixes ready

Branch: staging/ashborn-intro. Combined payload 4fd6365; tooltip source c57abae. Published main/tag/Workshop and active install remain unchanged at released 0.6.3.

All six crowns receive the Ashborn introduction once per country. Existing saves catch up; Cindermaw does not repeat an old introduction or starting-unit grant. The Moot rewards now display The Local Covenants and The First Oathkeeper. Three major Covenant rites also have native modifier names/descriptions. Reward values and saved IDs are unchanged.

Passed source regressions, native Covenant checks, all 60 custom modifier name/description checks, rejection of original broken labels, prepared-bundle validation and stale-config rejection. Clean committed export PrepareOnly and isolated installation passed. All 1,977 installed files match the candidate, including reconstructed terrain.

Receipt: reports/ashborn-intro-candidate.json. Current clean source: E:/CodexScratch/goblins-intro-review/tooltip-source. Isolated target: E:/CodexScratch/goblins-intro-review/tooltip-user. Reuse this passing gate for documentation-only follow-ups. Earlier source/ workspace is superseded reproducible scratch; no need to rebuild it.

No remaining installer blocker. No active installation or publication performed. Next: deploy/release when requested and verify in game. The tooltip correction should apply to saved modifiers after restart; runtime appearance remains untested.
