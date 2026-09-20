# Rome at War AI current handoff

Candidate: `T58B-ALLIED-LANDING-FALLBACK.md`; replay: `T58A-RUNTIME-REPLAY-ASSESSMENT.md`. Cold: `context/archive/HANDOFF-through-T52.md`.

## Workspace

- Canonical: `G:\Projects\Codex\Rome at War AI\.trade-work\T30-trade-cap-civ-fix`
- Branch: `t59/age-operand-and-test-suite-cleanup`; HEAD `git rev-parse HEAD`.
- PR: https://github.com/MnHebi/Rome-at-War-AI/pull/12 (PR11 merged)
- PR11 holds earlier508 source/tests and507 evidence; uncommitted Age fixes preserved. One owner; no new branch/worktree.

## Deployment

2026-09-20T11:03Z: `RAWAI-P3B44T58B:511`109 runtime files installed and hash verified. 511 = 510 + T69/T70 enemy-scan guards + the T71 native-gather experiment (`sn-intelligent-gathering 1`, both retask amounts 0; percentages unchanged).
SHA256 `3f3430a6b3e541c64c8f726458afdca1a0a2041e9b94690d81f5c7662f450360`.
Source: `7e49d173916498a2c8996b77e8fd420b9655b50f + deployed marker511; T71-DEPLOYMENT.md`.
Manifest/registry/510 backup `.analysis/deployment-t71-511-20260920T110354Z/`.
507 replay133042 failed: Green-owned locals; Age/goal floods. Keep `.analysis/deployment-t58a-507-20260912T102708Z/`.

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
- `706`: five heavy runs =85.0% of packets; writers farm-staffing1205/1202/1196.
- Migration: p2 retask->release+7,135 WORK; p7 DROPSITE-FAILED from the literal-0 `up-can-build` at `rawai-military.per:4833`; p1/3/4/8 masks0 in293/299.
- Assault p8/7645: 573 boards/232 unloads/259 WORK after. 269 MAKE records, none p6.
- 509 runtime (`T64-509-RUNTIME-RESULTS.md`): identity match; repaired error families 86277/3001/24490 -> 0, controls intact, sites36/63 exercised; shipyard reason64 .8665->.5118, reason63 now3415; 706 38259->4631 (no attribution).
- 509 defects: taunt31 fixed in 510 (site1829 736->0); ROW hold/issue625-637 never executed in508/509 (stall counter never2, merchants0); taunt48 per-player pattern open.
- T66-T71 (`T66-ORDER-STORM-ATTRIBUTION.md`, `T68-510-RUNTIME-RESULTS-AND-CRASH.md`): entering guard at 17 sites, unproven; 510 crashed, no stack; enemy scans now require `player-in-game`; 511 tests the native-gather retask bundle.

## Defects retained

17 findings live in `context/project-state.json` (render via the entry command above).
T60/T61 boundaries: 706 producer unresolved; shipyard repaired pending runtime; migration p2 ready/retask kept.

Preserve land trade, migration launch/landing, landed combat, three assault slots, partial loads, shoreline/danger gates, ownership, relic separation; no native gathering replacement.

## Validation / next action

509: capacity PASS; engine-boundary acceptance PASSED, gameplay open (`T64-509-RUNTIME-RESULTS.md`).
Maintenance: `MAINTENANCE-CONSISTENCY.md`; preserve Dacian/Syracusan lineups.

Next: dropsite status-ready observation, 706 issuer observation, allied unload/land advance.
