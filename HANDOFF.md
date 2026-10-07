# 0.5.5 mixed populations handoff

Branch: feature/0.5.5-mixed-goblin-populations, based on staging/0.5.5 at 294d5f2.

All 72 districts across all six islands and five nations now contain all five Ashborn cultures. Adds 323,941 goblins, including 231,332 slaves, without changing any existing population entry. Total 1,618,696. Cindermaw receives 159,949 newcomers, including 133,351 slaves; every other nation has both slave and free minorities. Fixed seed 1337055, weighted by country, capital and resource. Authored distribution: data/mixed_populations.json; generator: tools/generate_mixed_populations.py.

Full source setup and the small prototype installer share the same distribution. Installer appends rows to a copy of the installed 0.5.4 population setup, preserving BOM and leaving the base untouched. Prototype must load after base. Reinstall prototype and start a new campaign. Regular prepared release remains 0.5.4; no full 0.5.5 terrain bundle is claimed.

Checks: native classes, complete culture coverage, original entries unchanged, source-generated setup and prototype setup. Gathering static checks pass. Clean-export preparation and isolated installer checks recorded in the PR. Gameplay, load-order behavior and economy acceptance remain pending. No active installation, game launch, main merge or Workshop publication.
