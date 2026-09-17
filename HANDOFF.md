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
Manifest/registry/507 backup `.analysis/deployment-t58b-508-20260912T200909Z/`. No options changed.
507 replay133042 failed: rawP1 exposes Green-owned locals, not Blue; Age/goal floods. Keep registry `.analysis/deployment-t58a-507-20260912T102708Z/`.

## Active task

- Node `task.t52-runtime`; capsule `context/tasks/t52-runtime.json`.
- Entry: `py -3.12 tools/context_pack.py task.t52-runtime --role runtime-analyst`.
- Installed508: initializer, native Age facts, TC-independent migration admission, cap4, allied landing (`T58B-MIGRATION-TC-ADMISSION.md`).
- Allied fallback: exhausted plan -> ready allied TC on objective landmass -> shoreline/danger checks + mobile witness -> same enemy/manifest dispatch;120s local within360.
- Preserve507 registry. Candidate9312/10000 rules,1498/1500 literals. Protocol `T58-FILE-TRACE.md`; Age probe not installed.
- 508 caps TC targets/colony expansion4; lineups unchanged. `T58A-BACKLOG-SWEEP.md`: all8 Shipyards ready but late; no ROW/help verification; all8 Skirmisher queues. No closure.

## Tests

- `TEST-EXECUTION-POLICY.md`, `T59-TEST-SUITE-CLEANUP.md`: 17 fewer default tests, 6.6s. Retired `test_boarding_sampling.py` + legacy chat-emitter tests; frozen history via `RAWAI_HISTORICAL_OVERLAY_TESTS=1`.
- Open: `rawai-init-goals.per` `my-player-number` as `up-get-fact` fact-id (unfixed); no-escrow goal absent; `test_validators.py` split pending.

## T59 replay 231130

- Identity: markers508 + registry words all8 + 109/109 hashes; file trace 1,130,143 complete records, 0 malformed, all8 startup/entry/boarding.
- Operands: `up-can-build`86277 + `up-can-build-line`3001 + `up-get-point-distance`24490 = Invalid goal used(0); fix = agreed no-escrow goal + `gl-shipyard-x` operand (`rawai-specialplacement.per:792-843`); reason64=6186/7139 is that verdict.
- Migration: admission463x all8; p2 CONFIRM-DROPSITE2950s with colony-TC0 (508 fix confirmed) but 579=0, never status-ready; p7 aborted3683s; p1/3/4/8 IDLE.
- 706:38259 packets/46850 incidences; all5 dense onsets <=4s after scripted boarding; 0 inside traced brackets. Help300-317=0. Detail `T59-REPLAY-231130-ANALYSIS.md`.

## Defects retained

| ID | Status | Next boundary |
|---|---|---|
| villager.order706 | INVESTIGATING | Onset <=4s after scripted boarding; issuer unknown (T59). |
| diagnostics.command-boundary.t57 | INVESTIGATING | Delivery/identity runtime-verified all8; operand floods = separate operand item. |
| villager.keystates.t53 | INVESTIGATING | Ctrl experiment inconclusive; policy constant. |
| shipyard.sampler.t51 | FIXED-PENDING-RUNTIME | Reason64 decisions use `up-can-build-line 0`; operand fix pending (T59). |
| help.exact-episode.t53 | FIXED-PENDING-RUNTIME | Exact312–317 request/silence outcome. |
| assault.shore-egress.t53 | INVESTIGATING | Actual unload path; no-witness gap. |
| assault.voyage.t55b | INVESTIGATING | Commands vs positions, private680–690. |
| assault.preparation.close-boarders | INVESTIGATING | Blockage/reissue/ownership at abort. |
| migration.productive-dropsite | INVESTIGATING | Admission confirmed (p2 CONFIRM-DROPSITE2950s, colony-TC0); dropsite never status-ready (579=0). |
| merchant.row.real-choke | INVESTIGATING | Yield → hull progress → native trade. |
| expedition.commitment | INVESTIGATING | No tuning before upstream acceptance. |
| production.reactive-skirmisher.t56 | FIXED-PENDING-RUNTIME | T57 all8 queue counters; births/threat matching/live bounds unproven. |

Preserve land trade, migration launch/landing, landed combat, three assault slots, partial loads, shoreline/danger gates, ownership, relic separation; no native gathering replacement.

## Validation / next action

508: PER/generators/capacity PASS; cleanup cut 17 default tests (T59). Deployment verified; runtime acceptance pending (`T58B-AGE-OPERAND-AUDIT.md`).
Maintenance: `MAINTENANCE-CONSISTENCY.md`; preserve Dacian/Syracusan lineups.

Next: operand fix (no-escrow + point operand), dropsite status-ready observation, 706 issuer observation, allied unload/land advance.
