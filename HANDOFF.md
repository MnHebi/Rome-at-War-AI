# Rome at War AI current handoff

Latest candidate: `T58B-ALLIED-LANDING-FALLBACK.md`; replay evidence: `T58A-RUNTIME-REPLAY-ASSESSMENT.md`.
Cold history: `context/archive/HANDOFF-through-T52.md`.

## Workspace

- Canonical: `G:\Projects\Codex\Rome at War AI\.trade-work\T30-trade-cap-civ-fix`
- Branch: `fix/trade-cog-cap-dacian`; current HEAD: `git rev-parse HEAD`. Publication base `a635d55`; T58B candidate and preserved maintenance are being added to PR11.
- PR: https://github.com/MnHebi/Rome-at-War-AI/pull/11
- PR11 refresh includes pending508 source/tests and507 evidence; deployment history: `T58-DEPLOYMENT.md`.
- One owner; no new branch/worktree/overlay. Do not edit obsolete .pr-work.

## Current deployment

2026-09-12: `RAWAI-P3B44T58A:507`,109 canonical runtime files installed and hash verified.
SHA256 `9e3823727574792e3677321a1ca07a92f2e5f80144269844f0f967b0d7ac5969`.
Source: `a635d5598a6d292a9571d14abd178b669189b345 + working changes; installed experiments reconciled in canonical source (T58-DEPLOYMENT.md)`. Counter1 is NOT STOP proof.
**507 MATCH FINISHED, ACCEPTANCE FAILED**. Replay133042 lasted87:53; all109 installed hashes reverified.207,244 frames labeledP1 actually expose Green-owned locals. Never join that raw label to Blue. Age/goal floods remain unresolved.
Manifest/frozen registry/506 backup: `.analysis/deployment-t58a-507-20260912T102708Z/`. No deployment this turn.

## Active task

- Node `task.t52-runtime`; capsule `context/tasks/t52-runtime.json`.
- Entry: `py -3.12 tools/context_pack.py task.t52-runtime --role runtime-analyst`.
- Local508 (not deployed): player initializer, TC-independent migration admission, cap4 and last-choice allied-base landing. Earlier fixes/uncertainty: `T58B-MIGRATION-TC-ADMISSION.md`.
- Allied fallback: exhausted enemy plan -> ready allied TC on objective landmass -> existing shoreline/danger checks + mandatory exact mobile witness -> same enemy/manifest dispatch.120-second local allowance within unchanged360 total; three slots unchanged. `T58B-ALLIED-LANDING-FALLBACK.md`.
- Preserve507 frozen registry for old logs. Candidate9312/10000 rules,1498/1500 literals; reclaim before adding strings. Protocol: `T58-FILE-TRACE.md`.
- Operand probe not installed: `T58A-RUNTIME-OPERAND-ERRORS.md`.
- 508 also caps TC targets/colony expansion at4 (all34 civs); protected lineups unchanged. `T58A-BACKLOG-SWEEP.md`: all8 Shipyards ready but mostly late; no recorded ROW/help verification; all8 Skirmisher queues; Gray20,142 order706 packets. No backlog closure.

## Defects retained

| ID | Status | Next boundary |
|---|---|---|
| villager.order706 | INVESTIGATING | Ordinary-match paired command/onset attribution. |
| diagnostics.command-boundary.t57 | INVESTIGATING | Player initializer FIXED-PENDING-RUNTIME; oldP1 label is not Blue. Operand floods/all-player delivery remain open. |
| villager.keystates.t53 | INVESTIGATING | Existing Ctrl experiment inconclusive; policy constant. |
| shipyard.sampler.t51 | FIXED-PENDING-RUNTIME | T57 foundations all8, ready7;11,524 rejected samples spatially evaluated. Late Purple53:02; coastal buildability still unresolved. |
| help.exact-episode.t53 | FIXED-PENDING-RUNTIME | Exact312–317 request/silence outcome. |
| assault.shore-egress.t53 | INVESTIGATING | Actual unload path; no-witness gap. |
| assault.voyage.t55b | INVESTIGATING | Commands vs positions, private680–690. |
| assault.preparation.close-boarders | INVESTIGATING | Blockage/reissue/ownership at abort. |
| migration.productive-dropsite | INVESTIGATING | TC-admission fix pending runtime; require resource launch, safe construction, gather/deposit; inner gates remain unresolved. |
| merchant.row.real-choke | INVESTIGATING | Yield → hull progress → native trade. |
| expedition.commitment | INVESTIGATING | No tuning before upstream acceptance. |
| production.reactive-skirmisher.t56 | FIXED-PENDING-RUNTIME | T57 all8 queue counters; births/threat matching/live bounds still unproven. |

Preserve land trade, migration launch/landing, landed combat, three independent assault slots, partial loads, shoreline/danger gates, ownership and relic separation. No native gathering replacement.

## Validation / next action

508:131 assault/PER/generator/capacity checks PASS. Full Python3.12 discovery:683run,681PASS,2retired skips(98.462s). All109 installed507 hashes unchanged; runtime acceptance pending.
Maintenance: `MAINTENANCE-CONSISTENCY.md`; preserve Dacian/Syracusan lineups.

Next: authorized508 runtime must prove allied unload/land advance and resource migration productivity. Operand probe/backlog remain separate. No deployment authorized.
