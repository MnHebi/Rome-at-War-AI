# T63 deployment — operand-repair candidate `RAWAI-P3B44T58B:509`

Deployed on user authorization ("(1) deploy"), 2026-09-19T17:20:57Z, from the
canonical checkout `.trade-work\T30-trade-cap-civ-fix`, through the established
process used for the 505-508 payloads (`deploy-t63-509.py`, modelled on
`deploy-t58b-508.py`). No game launch, no option change, no marker in any other
file, and no installed file outside the AI payload touched.

## Identity

| Item | Value |
|---|---|
| Marker | **`RAWAI-P3B44T58B:509`** (number bumped from 508; label unchanged) |
| Payload aggregate | `2e9144ea6c2920a469e027713300bd5f38df34a6a794e5f30bd213f3df77a58a` (SHA256 sorted filename + NUL + file hash + LF) |
| Source identity words | `[-1841858553, 271991160, -517365673, 424529343, -638624529, 1292396916, 1560141061, -1844389435]` |
| Files | 109 runtime `.ai`/`.per`, 99 identical to the installed 508 payload |
| Source | HEAD at deploy time `bfb309b` plus the disclosed marker bump 508 → 509; the deployed tree is committed as **`ff30967`** (recorded in `project-state.json` and `HANDOFF.md`) |
| Manifest | `.analysis\deployment-t63-509-20260919T172057Z\manifest.json` (+ `before-manifest.json`, `command-boundary-registry.json`, `before/` backup of all installed files) |
| Prior payload | `.analysis\deployment-t58b-508-20260912T200909Z\manifest.json` |
| Engine options changed / game launched | `false` / `false` |

## Files installed (10)

`rawai-customconstants.per` (new `gl-no-escrow-state` = 396),
`rawai-init-goals.per` (one-shot `without-escrow` init + marker 509),
`rawai-homebase.per`, `rawai-military.per`, `rawai-wonder.per`,
`rawai-fishing.per`, `rawai-civ-kushans.per`, `rawai-tauntcommands.per`
(136 named escrow operands: 68 `up-can-build`, 18 `up-can-build-line`,
50 `up-build`), `rawai-specialplacement.per` (3 shipyard escrow operands +
4 `up-get-point-distance` point operands), and
`rawai-command-boundary-coverage.per` (regenerated source-map identity words).
Everything else, including `changelog.txt`, is byte-identical to the previous
install.

## Verification performed

| Check | Result |
|---|---|
| Candidate gates before install | `validate_per` no findings; generator `PASS 579 rules 817 commands`; capacity 9,312/10,000; strings 1,498/1,500 |
| Installed bytes vs manifest | identical (109/109) |
| Source bytes vs manifest | identical (guards against a source change during deployment) |
| Backup vs pre-deployment hashes | identical (rollback available from the recorded `before/` directory) |
| Installed marker line | `(up-chat-data-to-all "RAWAI-P3B44T58B: %d" c: 509)` |
| Unchanged vs 508 | 99 of 109 files |
| Extras preserved | `changelog.txt` (hash unchanged) |

## Status and next boundary

**DEPLOYED AND HASH VERIFIED; ENGINE STARTUP PENDING.** Startup, in-game load and
any gameplay result are unproven: no match has been played with 509, so the
operand repair has **no runtime evidence yet** and nothing may be attributed to
it. The next step is an authorized launch and one logged match, followed by
`tools/verify_operand_runtime.py` on that match's engine log, file-trace records
and replay (acceptance criteria: the three repaired error families at zero, the
control families still present, repaired sites exercised, shipyard reason-64
share below the 508 baseline of 0.8665, and the migration/706 evidence reported
without attribution).

Rollback: restore `before/` over the target, or copy the 508 payload from the
recorded 508 manifest; the marker would then need the same deliberate treatment.
