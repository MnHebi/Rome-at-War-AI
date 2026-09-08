# Rome at War AI current handoff

Bounded hot state. Detail: `MATCHED-BOARDING-COMMAND-OBSERVATIONS.md`, `BOARDING-SAMPLING-COVERAGE.md`.
Cold history: `context/archive/HANDOFF-through-T52.md`.

## Workspace

- Canonical: `G:\Projects\Codex\Rome at War AI\.trade-work\T30-trade-cap-civ-fix`
- Branch: `fix/trade-cog-cap-dacian`; instrumentation HEAD is the commit containing this handoff (`git rev-parse HEAD`). Prior counter commit: `ab25736954b80f0a722cbcaec8ba7e49acdb4018`; original base `f6f1b5b`.
- PR: https://github.com/MnHebi/Rome-at-War-AI/pull/11
- Analysis/validation posted: https://github.com/MnHebi/Rome-at-War-AI/pull/11#issuecomment-5583165441
- All pending boarding/marker/observation work included for PR11; counter repair separate. Commit/push authorized; deployment forbidden.
- One owner; no new branch/worktree/overlay. Do not edit obsolete .pr-work.

## Three identities

A. Historical deployment: `f6f1b5b + uncommitted experiment/marker`, `RAWAI-P3B44T56:504`.
103-file SHA-256: `FB515FA0A52859BCC677353D7B06B38792DC6DAF4C03604AA793EBF30D707730`.

B. Installed user experiment, verified unchanged once on 2026-09-08:
`60E05CFF142D948134C0693674CD37F8B851EE297CD40351D9DAB27B8576895C`.
Intentional customconstants de-game/wk-game definitions; general removes counter1 STOP and DE-guards counter2. Counter1 is NOT proof of STOP. Preserve these files; do not copy the experiment into canonical as a proven repair.
Target: `C:\Users\LostSoul\Games\Age of Empires 2 DE\76561198053747760\mods\local\Rome at War AI\resources\_common\ai`.

C. Canonical:108 files, SHA-256 `0d14e9ff7eb639abc415134753ebea9d11358e6ecf891b93197ed2876f5d0bc2`; manifest in focused report. Marker504 does not identify C. Deployment needs B reconciliation, fresh identity and authorization.

## Active task

- Node `task.t52-runtime`; capsule `context/tasks/t52-runtime.json`.
- Entry: `py -3.12 tools/context_pack.py task.t52-runtime --role runtime-analyst`.
- **INSTRUMENTATION READY — PENDING RUNTIME EVIDENCE**.
- **VILLAGER ORDER706 — INVESTIGATING**.
- Prior audit:34 sustained actor bursts; no explicit actor STOP within prior30s/during. Renewal contact does not prove causality.
- Matched30s windows: T56 same-hull658 no706 /51 sustained onset /1 isolated /14 censored. T55B82 /53. Overlapping windows are not independent trials or boarding successes.
- Five boarding/13 default sites observed. Two actors; four reports/180s: early +loading12/20/28, quiet pairs between. No gameplay change. Historical timing is conditional; actor lists, carry-in and Green gap remain unresolved. See coverage report.
- Need paired movement for actual flooded actors, actual resource-writer/packet attribution and subsequent boarding/gather/deposit outcomes. Missing samples never establish native origin.

## Defects retained

| ID | Status | Next boundary |
|---|---|---|
| villager.order706 | INVESTIGATING | Ordinary-match paired command/onset attribution. |
| villager.keystates.t53 | INVESTIGATING | Existing Ctrl experiment inconclusive; policy constant. |
| shipyard.sampler.t51 | FIXED-PENDING-RUNTIME | Exact failed-site buildability inputs. |
| help.exact-episode.t53 | FIXED-PENDING-RUNTIME | Exact312–317 request/silence outcome. |
| assault.shore-egress.t53 | INVESTIGATING | Actual unload path; no-witness gap. |
| assault.voyage.t55b | INVESTIGATING | Commands vs positions, private680–690. |
| assault.preparation.close-boarders | INVESTIGATING | Blockage/reissue/ownership at abort. |
| migration.productive-dropsite | OPEN | Foundation → ready → gather → deposit. |
| merchant.row.real-choke | INVESTIGATING | Yield → hull progress → native trade. |
| expedition.commitment | INVESTIGATING | No tuning before upstream acceptance. |
| production.reactive-skirmisher.t56 | FIXED-PENDING-RUNTIME | Prior repair retained undeployed. |

Preserve land trade, migration launch/landing, landed combat, three independent assault slots, partial loads, shoreline/danger gates, ownership and relic separation. No native gathering replacement.

## Validation / next action

Fresh final discovery:625/625 PASS (57.038s), normal Windows Temp access. PER, ownership1052, generators, keystates, strategy/naval and context checks PASS. Six reserved-sampling tests execute the generated PER; existing15 observer fixtures pass. Strings1489/1500: four new load paths, no new diagnostic text.
Known pre-existing gaps: six generated-civ differences and frozen good-units provenance mismatch. Do not regenerate/rebaseline.

Next ordinary match: capture720–772 for actual actors, join corrected outgoing arrays and first706, judge boarding and gathering/deposit separately. No arranged scenario substitutes for acceptance. Conditional suppression is specified, NOT enabled; it must use functional state independent of diagnostic sampling.
