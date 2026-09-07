# Rome at War AI current handoff

Bounded hot state; replace rather than append. Findings: `context/project-state.json`.
Cold history: `context/archive/HANDOFF-through-T52.md`.

## Workspace identity

- Canonical workspace:
  `G:\Projects\Codex\Rome at War AI\.trade-work\T30-trade-cap-civ-fix`
- Branch: `fix/trade-cog-cap-dacian`
- Deployed: `1f87ef0` (T55 marker commit, followed by deployment documentation).
- Source: `b4a230b` plus the following evidence/test commit (Git HEAD authoritative).
- Undeployed observations: `66531c5`, `dd592c7`, `b4a230b`; no gameplay-policy edits.
- Existing PR: `https://github.com/MnHebi/Rome-at-War-AI/pull/11`
- Do not create another branch, worktree, clone or recovery line unless the user
  explicitly changes this instruction.

## Agent usage controls

Economy mode: one owner. Optional read-only specialists only when a specific
question saves work; no automatic pipeline. Routing/contracts live in
`context/agent-routing.json`; use a bounded task delta, not full history.

## Active task

- Node: `task.t52-runtime`
- Capsule: `context/tasks/t52-runtime.json`
- Causal assessment: `T55B-CAUSAL-INVESTIGATION.md`
- Load compact task context with:
  `py -3.12 tools/context_pack.py task.t52-runtime --role runtime-analyst`

T55B causal audit: yard batches are active; reason64 is not terrain-only.
Blue49162 completion corroborated by52:50 count, despite missing ready event.
Cyan gets correct-hull waypoint orders; physical progress remains unobserved.
43834's706 flood follows boarding39461 and ends after home-unload attempts.
Undeployed diagnostic corrections only; no speculative gameplay repair.

## Installed runtime

- Marker: `RAWAI-P3B44T55:503`
- Runtime source commit: `1f87ef0` (deployed 2026-09-07)
- Installed/source files: 99/99 byte-identical; no overlay or unexpected files.
- Aggregate SHA-256:
  `6EE2AC23972B252500C62F9961D51E6C0C42956F4DA52125C5B487F87229D86C`
- Target:
  `C:\Users\LostSoul\Games\Age of Empires 2 DE\76561198053747760\mods\local\Rome at War AI\resources\_common\ai`

## Current defect ledger

| ID | Status | Immediate boundary / next action |
|---|---|---|
| `shipyard.sampler.t51` | FIXED-PENDING-RUNTIME | Expansion survives; inspected Red/Cyan sites leave exact buildability input gap. New per-minute rejection inputs pending runtime. |
| `villager.order706` | INVESTIGATING | 43834: boarding ->706 ->TC orders; producer unknown. Broadcast640–658 and coverage659–665 prepared, Ctrl unchanged. |
| `villager.keystates.t53` | EXPERIMENTAL / INCONCLUSIVE | T55B: 15 Blue samples missed active Cyan/Gray floods. |
| `help.exact-episode.t53` | FIXED-PENDING-RUNTIME | `0e1a83b`: persistent exact episode plus fresh local balance. Require 312-317 and correct help/silence. |
| `assault.shore-egress.t53` | INVESTIGATING | T54 failed. Exact witness query corrected; no-witness and actual-unload gaps remain. |
| `assault.voyage.t55b` | INVESTIGATING | Correct-hull orders precede96sec stalls; physical positions/accounting absent. Private680–690 observations prepared; no timeout change. |
| `assault.preparation.close-boarders` | INVESTIGATING | T51 passengers were 2-7 tiles away with exact hull/group/enter intent yet eight Gray cycles terminated. Reconstruct physical blockage/reissue/ownership at each abort. |
| `migration.productive-dropsite` | OPEN | Launch/landing works. Require autonomous exact foundation -> ready -> retask -> gather -> deposit, without manual intervention. |
| `merchant.row.real-choke` | INVESTIGATING | T52 diagnostics arm only on an actual priority-hull episode. Require one-at-a-time yield, hull progress, then native trade resumption. |
| `expedition.commitment` | INVESTIGATING | Observation only until all earlier gates are judged; do not tune yet. |

Runtime-confirmed behavior to preserve: landed-assault target acquisition and
combat continuation; T50 land trade; T51 autonomous migration launch/landing;
three independent assault slots, useful-partial manifests, shoreline/path and
danger validation, migration/relic separation and bounded naval cooperation.

## Validation baseline

579/579 Python3.12 tests PASS (normal Windows Temp access); PER operands,
strategy1156 matchups, naval doctrine, four Ctrl wrappers, ownership1031 sites,
42 replay benchmarks and source synchronization PASS. Detailed results in the
causal report. Six pre-existing generated-civ differences and the good-units
frozen `AI RAW.per_sha256` mismatch remain; do not regenerate/rebaseline them.

## Exact next action

Do not deploy without authorization. Review T55B-CAUSAL-INVESTIGATION.md.
Pending observers: Shipyard666–676, voyage680–690, economic640–665.
Next ordinary match must distinguish actual movement from watchdog accounting,
candidate resource holds from geometry, and actor-level worker writer coverage.
579/579 tests PASS; baseline six-civ drift/frozen hash unchanged. No gameplay
closure inferred; help, colony productivity, land egress and ROW remain open.
