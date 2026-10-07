# Brackmaw 0.5.5 handoff

Base: staging/0.5.5 at 294d5f2; feature/brackmaw-sluice-king-055. Goal: distinguish Brackmaw/Brineward and nickname its starting ruler.

Implemented: Murgash Brackmaw, The Sluice-King; ADM/DIP/MIL 84/78/90. Marsh engineering, supply oaths and coastal industry in culture text, lore and Gathering introduction. Shared data/brackmaw.json feeds full-build courts/localization and the prototype installer. Installer derives two overrides from installed 0.5.4 without editing that base or committing game-derived setup. Other characters, family dates, succession, population, terrain, actions and costs are preserved.

Checks: 0.5.5 native-reference/ownership checks; Brackmaw comparison against installed base and full-build generator. Exact-tree clean preparation/isolated installation results recorded in the PR. In-game override precedence, name display and event text remain user-run acceptance; no game launch, active-mod installation, main merge or Workshop publication performed.

Build/publish: small 0.5.5 prototype remains an add-on to 0.5.4, with refreshed file/data hashes; regular installer remains the prior release. Next: review PR, merge into staging/0.5.5, test a new 1337 campaign with base and add-on enabled.
