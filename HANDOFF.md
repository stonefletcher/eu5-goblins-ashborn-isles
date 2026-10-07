# 0.5.5 integrated handoff

PR #8 combines the population update with staging/0.5.5 at 51c01d8 (merged PR #7 clan identities). All 72 districts contain all five goblin cultures. Adds 323,941 goblins, including 231,332 slaves; total 1,618,696. Home clans retain approximately 78–84% of national populations. Existing population entries remain intact.

Preserved all four clan identity profiles, ruler abilities, nicknames, culture text, lore and Gathering introductions from PR #7. The prototype installer now derives population, character and localization overrides from the installed 0.5.4 base. The generated manifest contains both population additions and identity hashes. Full source generation uses both systems.

Validation: mixed-population preservation and majority checks, clan identity checks, Gathering static checks and clean committed-source prototype preparation. Gameplay, override order and balance still need acceptance. No active installation or game launch. Use the small prototype installer with the 0.5.4 base and a new campaign; the regular prepared release remains 0.5.4.
