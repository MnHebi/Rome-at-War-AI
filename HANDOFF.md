# Rome at War AI current handoff

This is the bounded **hot operational state**. Replace it when current work
changes; do not append historical chapters. Stable findings and defects live in
`context/project-state.json`. Task routing lives in `context/nodes.json` and
`context/tasks/`. The former 5,615-line handoff is preserved as cold provenance
at `context/archive/HANDOFF-through-T52.md`.

## Workspace identity

- Canonical workspace:
  `G:\Projects\Codex\Rome at War AI\.trade-work\T30-trade-cap-civ-fix`
- Branch: `fix/trade-cog-cap-dacian`
- Deployed: `5dd9c63`; behavioral HEAD `fc71f0e` (followed by audit docs) includes undeployed landing and Shipyard repairs.
- Existing PR: `https://github.com/MnHebi/Rome-at-War-AI/pull/11`
- Do not create another branch, worktree, clone or recovery line unless the user
  explicitly changes this instruction.

## Agent usage controls

- Default mode is `economy`: the current agent or built-in `worker` owns an
  ordinary task end to end and stops.
- Optional project capabilities are `economy_scout`, `economy_analyst`,
  `economy_planner` and `economy_verifier`. They are read-only, non-recursive,
  conditional leaves—not a pipeline or automatic fan-out.
- `context/agent-routing.json` defines 12 representative task routes, the
  delegation-cost gate, modes and compact handoff contract. Inspect one with
  `py -3.12 tools/context_pack.py --route <task-class>`.
- Delegation uses a task delta plus one role-filtered context packet and returns
  `RESULT / EVIDENCE / ACTION / UNCERTAINTY`; do not pass full task history.

## Active task

- Node: `task.t52-runtime`
- Capsule: `context/tasks/t52-runtime.json`
- Replay assessment: `T54-SHIPYARD-SPATIAL-AUDIT.md`
- Load compact task context with:
  `py -3.12 tools/context_pack.py task.t52-runtime --role runtime-analyst`

T54 Shipyards: 84.4% of 2,497 buildability-rejected samples missed plausible
coastline. Four-draw bounded shoreline preference is implemented; full gates
and unfiltered fallback remain. Landing correction also awaits deployment.

## Installed runtime

- Marker: `RAWAI-P3B44T54:502`
- Runtime source commit: `5dd9c63` (deployed 2026-09-07)
- Installed/source files: 99/99 byte-identical; no overlay or unexpected files.
- Aggregate SHA-256:
  `572BAEC05AEEE6C71E1E434EF2CB3ACA953E1157D227A8EB9CC424651EE5365A`
- Target:
  `C:\Users\LostSoul\Games\Age of Empires 2 DE\76561198053747760\mods\local\Rome at War AI\resources\_common\ai`

## Current defect ledger

| ID | Status | Immediate boundary / next action |
|---|---|---|
| `shipyard.sampler.t51` | FIXED-PENDING-RUNTIME | T54: only three yards. Spatial audit supports bounded shoreline preference; affordability/coastal rejections remain unresolved. |
| `villager.order706` | INVESTIGATING | T53 tests four ordinary home-economy writers with Ctrl persistence; exact cause remains unproven. Correlate codes 640-657 to the same actor's pre/post/later 706 stream. |
| `villager.keystates.t53` | EXPERIMENTAL / INCONCLUSIVE | Nine samples missed the active floods; no accept/revert result. |
| `help.exact-episode.t53` | FIXED-PENDING-RUNTIME | `0e1a83b`: persistent exact episode plus fresh local balance. Require 312-317 and correct help/silence. |
| `assault.shore-egress.t53` | INVESTIGATING | T54 failed. Exact witness query corrected; no-witness and actual-unload gaps remain. |
| `assault.preparation.close-boarders` | INVESTIGATING | T51 passengers were 2-7 tiles away with exact hull/group/enter intent yet eight Gray cycles terminated. Reconstruct physical blockage/reissue/ownership at each abort. |
| `migration.productive-dropsite` | OPEN | Launch/landing works. Require autonomous exact foundation -> ready -> retask -> gather -> deposit, without manual intervention. |
| `merchant.row.real-choke` | INVESTIGATING | T52 diagnostics arm only on an actual priority-hull episode. Require one-at-a-time yield, hull progress, then native trade resumption. |
| `expedition.commitment` | INVESTIGATING | Observation only until all earlier gates are judged; do not tune yet. |

Runtime-confirmed behavior to preserve: landed-assault target acquisition and
combat continuation; T50 land trade; T51 autonomous migration launch/landing;
three independent assault slots, useful-partial manifests, shoreline/path and
danger validation, migration/relic separation and bounded naval cooperation.

## Validation baseline

- Help tests: 10/10 PASS; assault planner: 31/31 PASS; shoreline resolver:
  12/12 PASS; validator suite: 128/128 PASS.
- Key-state validator: PASS (exactly four bounded Ctrl wrappers); ownership
  inventory: 1,031 sites, zero direct failures.
- Full Python 3.12 discovery: 572/572 PASS (unrestricted Windows Temp run).
- Shipyard tests: 25 PASS; spatial analysis: 3 PASS; episode diagnostics: 9 PASS.
- PER structure/operand validation: PASS.
- Strategy execution: 1,156 matchups, zero errors.
- Naval doctrine, ownership, replay benchmark metadata (42), context metadata,
  and `git diff --check`: PASS. The read-only strategy synchronizer reports six
  pre-existing generated civ files it would update; T53 changed none of them.
- `validate_good_units.py` has a known frozen-provenance mismatch at
  `source_provenance/AI RAW.per_sha256`; do not silently rebaseline it.

## Exact next action

Deploy only when requested. Compare eligible Shipyard foundation timing/counts
and coast quality; preserve safety. Then correlate landing witness records with
actual unloads. Help and 706 acceptance remain pending.
