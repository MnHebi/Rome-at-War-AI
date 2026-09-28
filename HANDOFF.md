# Rome at War AI current handoff

Cold: `context/archive/HANDOFF-through-T52.md`.

## Workspace

- Canonical: `G:\Projects\Codex\Rome at War AI\.trade-work\T30-trade-cap-civ-fix`
- Branch: `t59/age-operand-and-test-suite-cleanup`; HEAD `git rev-parse HEAD`.
- PR: https://github.com/MnHebi/Rome-at-War-AI/pull/12 (PR11 merged)
- PR11 holds earlier508 source/tests and507 evidence. One owner; no new branch/worktree.

## Deployment

2026-09-26T14:42Z: `RAWAI-P3B44T58B:515`109 runtime files installed and hash verified. 515 = 514 + the T91 lift fixes (abort returns the hull, entering soldiers barred from the lift list) and the T97-T108 id alignment with raw-datamod-uplifted.
SHA256 `da21805229ae4cad69ee732e705724e1d7dc0712ebac6cc66ea470fa30499e73`.
Source: `b0f8af9c5ce639d168b9a37f38f5f72c9d41db1e + deployed marker515; T91-ASSAULT-LIFT-DEPARTURE.md`.
Manifest/registry/514 backup `.analysis/deployment-t109-515-20260926T144209Z/`; 514 kept at `.analysis/deployment-t88-514-20260920T170428Z/`.

## Active task

- Node `task.t52-runtime`; capsule `context/tasks/t52-runtime.json`.
- Entry: `py -3.12 tools/context_pack.py task.t52-runtime --role runtime-analyst`.
- Installed508: Age facts, TC-independent migration admission, cap4, allied landing (`T58B-MIGRATION-TC-ADMISSION.md`).
- Preserve507 registry. Protocol `T58-FILE-TRACE.md`; Age probe not installed.

## Tests

- `TEST-EXECUTION-POLICY.md`: -17 default tests; history via `RAWAI_HISTORICAL_OVERLAY_TESTS=1`. Open: `my-player-number` misuse; `test_validators.py` split.

## T61/T62 correlator + 508 follow-up

- Correlator v4 (`command_contracts.py`): 2,199 candidates, 1,651 empty-input, 32 ambiguous. `706`: five heavy runs =85.0% of packets; writers farm-staffing1205/1202/1196; p7 DROPSITE-FAILED from the literal-0 `up-can-build` at `rawai-military.per:4833`; p2 retask->release+7,135 WORK.
- 509 runtime (`T64-509-RUNTIME-RESULTS.md`): repaired error families -> 0; 706 38259->4631 (no attribution). taunt31 fixed in 510; ROW hold/issue625-637 never executed; taunt48 open.
- T66-T71 (`T66-ORDER-STORM-ATTRIBUTION.md`): entering guard at 17 sites, unproven; 510 crashed, no stack; enemy scans require `player-in-game`.
- T84/T91 (`T84-LADEN-BOARDING-ADMISSION.md`, `T91-ASSAULT-LIFT-DEPARTURE.md`): 514 (deployed, marker 514) bars laden passengers from 11 boarding sites; the 515 candidate returns an aborted attack lift home and bars entering soldiers from its 7 boarding sites.

## Defects retained

18 findings live in `context/project-state.json` (render via the entry command above).
T60/T61 boundaries: shipyard pending; migration p2 ready/retask kept.
`villager.order706`: ROOT-CAUSE-PROVEN, fixed pending runtime by 514; residual population = unladen work-task batch boarders.

Preserve land trade, migration launch/landing, landed combat, three assault slots, partial loads, shoreline/danger gates, ownership, relic separation.

## Validation / next action

509: capacity PASS; engine-boundary acceptance PASSED, gameplay open (`T64-509-RUNTIME-RESULTS.md`).
Maintenance: `MAINTENANCE-CONSISTENCY.md`; preserve Dacian/Syracusan lineups.

Next: run 514 and compare the predicted storm split, departures and partial loads; then dropsite status-ready and allied unload/land observation.
