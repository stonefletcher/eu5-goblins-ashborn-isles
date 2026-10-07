# 0.5.3 released and merged

GitHub release: v0.5.3 (published; not a prerelease). Source tag: 0f0fe3b9370361061d2c1ee6550fee8dd3dd0b7e. Dedicated release branch: release/v0.5.3 at cd5f6d5df6b12a8d456e463c981b598f020fbc8a; staging/0.5.3 matches it. Main merge: 4b8871eb5dc26cba482533594afb40ebb88b56f6, preserving both parent histories and main's older archives/helpers.

Completed: current README/install guidance, release notes, testing status, Steam BBCode description/changelog, matching prepared installer, corrected source tag, and Workshop package preparation. 0.5.4 economy/demographics/lifespan changes and 0.5.5 expansion prototype remain separate.

Passed: prepared-bundle hashes/CRC/unique entries/current overlay; exact Git-tree export; clean PrepareOnly reconstruction against EU5 1.3.11; native portrait/model checks; full Workshop file hashes and thumbnail; isolated full staging script; compact upload-kit reconstruction and isolated staging. GitHub publish and downloadable-installer workflows succeeded. Published installer SHA-256: 54a3bd075e1586b3ff30934131f027ee4b0e69661eeab58a8058ef2da0e3dda9.

Deliverable: Goblins_Ashborn_Isles_0.5.3_Workshop_Upload_Kit.zip (215,043,266 bytes; SHA-256 6b1032aee3ea63763c955b28db01836bb2ac530d111ea11dd02d5db7c7228114). Run Stage-Workshop.cmd to reconstruct terrain and stage the full mod under the real EU5 user-data mod directory, then update existing Workshop item 3814944518 through Mod Tools. Full assembled ZIP is about 1.96 GB; the compact kit avoids the download size limit.

No active installation, game launch or Steam publication was performed. User confirmed visible infantry/no reported crash on October 6; broader gameplay checks remain in TESTING.md, and appearance refinement is issue #4. Next action: user uploads the staged content to the existing Steam listing.
