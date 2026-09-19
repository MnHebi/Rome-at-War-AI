# Rome at War AI current handoff

Candidate: `T58B-ALLIED-LANDING-FALLBACK.md`; replay: `T58A-RUNTIME-REPLAY-ASSESSMENT.md`. Cold: `context/archive/HANDOFF-through-T52.md`.

## Workspace

- Canonical: `G:\Projects\Codex\Rome at War AI\.trade-work\T30-trade-cap-civ-fix`
- Branch: `t59/age-operand-and-test-suite-cleanup`; HEAD `git rev-parse HEAD`.
- PR: https://github.com/MnHebi/Rome-at-War-AI/pull/12 (PR11 merged)
- PR11 holds earlier508 source/tests and507 evidence; uncommitted Age fixes preserved. One owner; no new branch/worktree.

## Deployment

2026-09-19T17:20Z: `RAWAI-P3B44T58B:509`109 runtime files installed and hash verified; first 509 match accepted at the engine boundary.
SHA256 `2e9144ea6c2920a469e027713300bd5f38df34a6a794e5f30bd213f3df77a58a`.
Source: `ff30967bca69749846814bb343a331d1943ff702 + deployed marker509; T63-DEPLOYMENT.md`. Counter1 is NOT STOP proof.
Manifest/registry/508 backup `.analysis/deployment-t63-509-20260919T172057Z/`.
507 replay133042 failed: rawP1 exposes Green-owned locals; Age/goal floods. Keep `.analysis/deployment-t58a-507-20260912T102708Z/`.

## Active task

- Node `task.t52-runtime`; capsule `context/tasks/t52-runtime.json`.
- Entry: `py -3.12 tools/context_pack.py task.t52-runtime --role runtime-analyst`.
- Installed508: initializer, Age facts, TC-independent migration admission, cap4, allied landing (`T58B-MIGRATION-TC-ADMISSION.md`).
- Allied fallback: exhausted plan -> allied TC on objective landmass -> shoreline/danger + mobile witness -> same enemy/manifest dispatch;120s local within360.
- Preserve507 registry. Candidate9312/10000,1498/1500. Protocol `T58-FILE-TRACE.md`; Age probe not installed.
- 508 caps TC targets/colony4; lineups unchanged. `T58A-BACKLOG-SWEEP.md`: Shipyards late; no ROW/help verification.

## Tests

- `TEST-EXECUTION-POLICY.md`, `T59-TEST-SUITE-CLEANUP.md`: -17 default tests; history via `RAWAI_HISTORICAL_OVERLAY_TESTS=1`. Open: `my-player-number` fact-id misuse; `test_validators.py` split.

## T61/T62 correlator + 508 follow-up

- Contracts from the AIRef (`command_contracts.py`): point/object, Option0/1, type-based, unclassified. v4 run: 196,154 no-direct-packet, 2,199 candidates, 1,651 empty-input, 32 ambiguous; 0/38,259 `706` in brackets.
- `706`: four boarding runs + one unloading =85.0%; hulls move inside bursts; garrison calls 1-2 each; writers farm-staffing1205/1202/1196; cohort 369/42/7/5.
- Migration: p2 retask->release+7,135 WORK; p7 DROPSITE-FAILED from the literal-0 `up-can-build` at `rawai-military.per:4833`; p1/3/4/8 masks0 in293/299.
- Assault p8/7645: 573 boards/232 unloads/259 WORK after. 269 MAKE records, none p6.
- 509 runtime (`T64-509-RUNTIME-RESULTS.md`): identity match; repaired error families 86277/3001/24490 -> 0, controls intact, sites36/63 exercised; shipyard reason64 .8665->.5118, reason63 now3415; 706 38259->4631 (no attribution).
- 509 defects (unfixed): taunt31 site1829 re-fires184x/101s (`acknowledge-taunt this-any-ally` fails to clear `taunt-detected any-ally`; taunt48 shows per-player pattern); ROW hold/issue625-637=0 in508/509 (stall counter never2, merchants0).
- T66 (`T66-ORDER-STORM-ATTRIBUTION.md`): p2 7806/34426 and p4 34824 gather-order storms, no traced producer; Promisory `actionid-enter` guard missing here; ambiguous, no fix.

## Defects retained

17 findings live in `context/project-state.json` (render via the entry command above).
T60/T61 boundaries: 706 producer unresolved; shipyard repaired pending runtime; migration p2 ready/retask kept.

Preserve land trade, migration launch/landing, landed combat, three assault slots, partial loads, shoreline/danger gates, ownership, relic separation; no native gathering replacement.

## Validation / next action

509: capacity PASS; engine-boundary acceptance PASSED, gameplay open (`T64-509-RUNTIME-RESULTS.md`).
Maintenance: `MAINTENANCE-CONSISTENCY.md`; preserve Dacian/Syracusan lineups.

Next: dropsite status-ready observation, 706 issuer observation, allied unload/land advance.
