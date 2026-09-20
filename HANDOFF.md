# Rome at War AI current handoff

Candidate: `T58B-ALLIED-LANDING-FALLBACK.md`; replay: `T58A-RUNTIME-REPLAY-ASSESSMENT.md`. Cold: `context/archive/HANDOFF-through-T52.md`.

## Workspace

- Canonical: `G:\Projects\Codex\Rome at War AI\.trade-work\T30-trade-cap-civ-fix`
- Branch: `t59/age-operand-and-test-suite-cleanup`; HEAD `git rev-parse HEAD`.
- PR: https://github.com/MnHebi/Rome-at-War-AI/pull/12 (PR11 merged)
- PR11 holds earlier508 source/tests and507 evidence. One owner; no new branch/worktree.

## Deployment

2026-09-20T14:04Z: `RAWAI-P3B44T58B:513`109 runtime files installed and hash verified. 513 = 512 + the T76 native hunter floor (`sn-minimum-number-hunters` 0 by default, 2 during a boar commit, matching Promisory).
SHA256 `7b0fe74e5493ada25d7e1489862f248ee0ef0b9be9cfaadce2580d97d71ddb67`.
Source: `011f25efa472343d2e7ed053e05781b32d92649e + deployed marker513; T76-DEPLOYMENT.md`.
Manifest/registry/512 backup `.analysis/deployment-t76-513-20260920T140436Z/`.
507 replay133042 failed: Green-owned locals; Age/goal floods. Keep `.analysis/deployment-t58a-507-20260912T102708Z/`.

## Active task

- Node `task.t52-runtime`; capsule `context/tasks/t52-runtime.json`.
- Entry: `py -3.12 tools/context_pack.py task.t52-runtime --role runtime-analyst`.
- Installed508: initializer, Age facts, TC-independent migration admission, cap4, allied landing (`T58B-MIGRATION-TC-ADMISSION.md`).
- Preserve507 registry. Candidate9312/10000,1498/1500. Protocol `T58-FILE-TRACE.md`; Age probe not installed.
- 508 caps TC targets/colony4; lineups unchanged (`T58B-MIGRATION-TC-ADMISSION.md`, `T58A-BACKLOG-SWEEP.md`).

## Tests

- `TEST-EXECUTION-POLICY.md`, `T59-TEST-SUITE-CLEANUP.md`: -17 default tests; history via `RAWAI_HISTORICAL_OVERLAY_TESTS=1`. Open: `my-player-number` fact-id misuse; `test_validators.py` split.

## T61/T62 correlator + 508 follow-up

- Contracts from the AIRef (`command_contracts.py`); v4 run: 196,154 no-direct-packet, 2,199 candidates, 1,651 empty-input, 32 ambiguous; 0/38,259 `706` in brackets.
- `706`: five heavy runs =85.0% of packets; writers farm-staffing1205/1202/1196. Migration: p2 retask->release+7,135 WORK; p7 DROPSITE-FAILED from the literal-0 `up-can-build` at `rawai-military.per:4833`.
- Assault p8/7645: 573 boards/232 unloads/259 WORK after. 269 MAKE records, none p6.
- 509 runtime (`T64-509-RUNTIME-RESULTS.md`): identity match; repaired error families 86277/3001/24490 -> 0, controls intact, sites36/63 exercised; shipyard reason64 .8665->.5118, reason63 now3415; 706 38259->4631 (no attribution).
- 509 defects: taunt31 fixed in 510 (site1829 736->0); ROW hold/issue625-637 never executed in508/509; taunt48 open.
- T66-T71 (`T66-ORDER-STORM-ATTRIBUTION.md`): entering guard at 17 sites, unproven; 510 crashed, no stack; enemy scans require `player-in-game`.
- T78-T84 (`T84-LADEN-BOARDING-ADMISSION.md`): storms are the native return intent of boarded laden passengers (target = the player's own drop-off; onset = enter->`garrisoned=1` while laden; no traced producer). 514 excludes `object-data-carry > 0` at 11 boarding admission sites; no SN/percentage change, nothing deployed.

## Defects retained

17 findings live in `context/project-state.json` (render via the entry command above).
T60/T61 boundaries: shipyard repaired pending runtime; migration p2 ready/retask kept.
`villager.order706`: ROOT-CAUSE-PROVEN, fixed pending runtime by 514; residual population = unladen work-task batch boarders.

Preserve land trade, migration launch/landing, landed combat, three assault slots, partial loads, shoreline/danger gates, ownership, relic separation; no native gathering replacement.

## Validation / next action

509: capacity PASS; engine-boundary acceptance PASSED, gameplay open (`T64-509-RUNTIME-RESULTS.md`).
Maintenance: `MAINTENANCE-CONSISTENCY.md`; preserve Dacian/Syracusan lineups.

Next: run 514 and compare the predicted storm split, departures and partial loads; then dropsite status-ready and allied unload/land observation.
