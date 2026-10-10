# Playtest fixes ready

Branch: staging/ashborn-intro. Current combined payload fc2ba4c; hover source 89c200e. Published main/tag/Workshop and active install remain released 0.6.3 without these pending fixes.

Pending changes: once-per-country Ashborn introduction for all six kingdoms, with legacy Cindermaw guards; correct names/descriptions for two Moot rewards and three Covenant rites; Beyond the Ashen Horizon option hover explains that it has no immediate cost/reward and directs the player to voyages and paid Eastern Hunger actions. Existing gameplay effects and stable IDs are preserved.

Passed source regressions, all 60 custom modifier labels, native script checks, exact event AST comparison allowing only the new tooltip, prepared-bundle validation and stale-source rejection. Fresh committed export PrepareOnly and packaged installer to an isolated user folder passed. All 1,977 installed files match, including reconstructed terrain.

Receipt: reports/ashborn-intro-candidate.json. Current clean source: E:/CodexScratch/goblins-intro-review/horizon-source. Isolated target: E:/CodexScratch/goblins-intro-review/horizon-user. Reuse this gate for documentation-only follow-ups; earlier source and tooltip-source workspaces are superseded reproducible scratch.

No blocker. No active deployment or publication performed. Next: deploy/release when requested; verify hover rendering in game. Display fixes should apply to existing saves after restart, without repeating quest rewards. Runtime acceptance remains pending.
