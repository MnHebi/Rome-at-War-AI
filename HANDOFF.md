# Rome at War AI current handoff

Candidate: `T58B-ALLIED-LANDING-FALLBACK.md`; replay: `T58A-RUNTIME-REPLAY-ASSESSMENT.md`. Cold: `context/archive/HANDOFF-through-T52.md`.

## Workspace

- Canonical: `G:\Projects\Codex\Rome at War AI\.trade-work\T30-trade-cap-civ-fix`
- Branch: `fix/trade-cog-cap-dacian`; HEAD `git rev-parse HEAD`. T58B source `5e9e548`; maintenance `4250e7f`; both on PR11.
- PR: https://github.com/MnHebi/Rome-at-War-AI/pull/11
- PR11 holds earlier508 source/tests and507 evidence; uncommitted Age fixes preserved. One owner; no new branch/worktree/overlay.

## Deployment

2026-09-12: `RAWAI-P3B44T58B:508`109 runtime files installed, hash verified.
SHA256 `0641fa7373a92e4246b8800e33d2c0ef15bbff1d6ab84e7a23e2569be4eab387`.
Source: `e84cec97f557de501176462bfae898a91d1dff19 + working Age fixes; T58B-DEPLOYMENT.md`. Counter1 is NOT STOP proof.
Manifest/registry/507 backup `.analysis/deployment-t58b-508-20260912T200909Z/`.
507 replay133042 failed: rawP1 exposes Green-owned locals, not Blue; Age/goal floods. Keep registry `.analysis/deployment-t58a-507-20260912T102708Z/`.

## Active task

- Node `task.t52-runtime`; capsule `context/tasks/t52-runtime.json`.
- Entry: `py -3.12 tools/context_pack.py task.t52-runtime --role runtime-analyst`.
- Installed508: initializer, native Age facts, TC-independent migration admission, cap4, allied landing (`T58B-MIGRATION-TC-ADMISSION.md`).
- Allied fallback: exhausted plan -> ready allied TC on objective landmass -> shoreline/danger checks + mobile witness -> same enemy/manifest dispatch;120s local within360.
- Preserve507 registry. Candidate9312/10000 rules,1498/1500 literals. Protocol `T58-FILE-TRACE.md`; Age probe not installed.
- 508 caps TC targets/colony expansion4; lineups unchanged. `T58A-BACKLOG-SWEEP.md`: all8 Shipyards ready but late; no ROW/help verification; all8 Skirmisher queues. No closure.

## Tests

- `TEST-EXECUTION-POLICY.md`, `T59-TEST-SUITE-CLEANUP.md`: -17 default tests; history via `RAWAI_HISTORICAL_OVERLAY_TESTS=1`. Open: `my-player-number` as `up-get-fact` fact-id; `test_validators.py` split.

## T61 correlator + 508 follow-up

- Contracts now come from the AIRef (`tools/command_contracts.py`): point/object targets, Option0/1, type-based, unclassified. Run `.analysis/t61-508-correlations-v3.jsonl`: 196,154 no-direct-packet, 2,199 candidates, 1,651 empty-input-recorded, 32 ambiguous, 14 type-based, 1 unsupported; 0/38,259 `706` in brackets.
- `706`: five runs =85.0% (sequence union, not 99.3%); onsets = `garrisoned 0->1` in a slowly moving hull; writers = farm-staffing sites1205/1202/1196; cohort 369/42/7/5.
- Migration: p2 retask->release with 7,135 WORK after; p7 DROPSITE-FAILED decided by the literal-0 `up-can-build` at `rawai-military.per:4833` (T60 repair); p1/3/4/8 masks0 in293/299 -> T60 timer hypothesis withdrawn.
- Assault hull p8/7645: 573 boards/232 unloads/259 WORK after. ROW ids corrected (581 hull; 618-622 rejected). Skirmisher births p6=0. Detail `T61-CORRELATOR-AND-508-FOLLOW-UP.md`.

## Defects retained

17 accepted findings (status/claim/acceptance/next action) live in `context/project-state.json`;
render with `py -3.12 tools/context_pack.py task.t52-runtime --role runtime-analyst`.
T60 boundaries: order706 = waiting-hull DUC selection; shipyard = repaired operands pending runtime;
migration = p2 ready/retask confirmed, p7 dropsite-failed, p1/3/4/8 admission timer unrecorded.

Preserve land trade, migration launch/landing, landed combat, three assault slots, partial loads, shoreline/danger gates, ownership, relic separation; no native gathering replacement.

## Validation / next action

508: PER/generators/capacity PASS; cleanup cut 17 default tests (T59). Deployment verified; runtime acceptance pending (`T58B-AGE-OPERAND-AUDIT.md`).
Maintenance: `MAINTENANCE-CONSISTENCY.md`; preserve Dacian/Syracusan lineups.

Next: operand fix (no-escrow + point operand), dropsite status-ready observation, 706 issuer observation, allied unload/land advance.
