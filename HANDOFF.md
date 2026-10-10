# Ashborn introduction patch

Branch: staging/ashborn-intro. Source e929537; matching package 59b49c9. Published main/tag/Workshop remain 0.6.3 without this patch.

All six goblin kingdoms receive the introductory lore popup once per country. Existing saves catch up; legacy Cindermaw introductions and unit grants are not repeated. Gathering behavior is unchanged.

Passed actual-script regressions for six kingdoms, repeated monthly pulses, saved flags, lost Hooktooth, old Cindermaw and foreign countries. Package validation and stale-config rejection passed. Clean committed export PrepareOnly passed; all 1,977 prepared files match the candidate.

Receipt: reports/ashborn-intro-candidate.json. Clean workspace: E:/CodexScratch/goblins-intro-review/source; isolated target: E:/CodexScratch/goblins-intro-review/user.

Blocked only at isolated installation: EU5 process 30564 is running and the installer correctly refuses. Asked user once to close EU5; do not bypass guard or interrupt game. No active installation or publication performed. Next: when game is closed, run the exported Install-Goblins.ps1 with GamePath and isolated UserDataPath, compare all files, then update this receipt. Gameplay remains untested.
