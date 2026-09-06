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
- Current source/deployed behavioral HEAD: `ea3e146`; inspect
  `git rev-parse HEAD` for the following deployment-record commit.
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
- No game-runtime source or installed test runtime changed for this agent-suite
  work.

## Active task

- Node: `task.t53-villager-keystates`
- Capsule: `context/tasks/t53-villager-keystates.json`
- Source audit: `T53-VILLAGER-KEYSTATES-AUDIT.md`
- Load compact task context with:
  `py -3.12 tools/context_pack.py task.t53-villager-keystates --role runtime-analyst`

T53 is a controlled order-706 experiment, not a root-cause claim. Commit
`e359ea5` adds separately rearmed actor diagnostics and offline correlation.
Commit `5ece337` wraps only four owned home-economy `action-default` commands in
Ctrl with immediate reset and excludes carrying workers at selection and
command time. It is independently revertible. T53 is now installed for fresh
runtime testing.

## Installed runtime

- Marker: `RAWAI-P3B44T53:501`
- Runtime source commit: `ea3e146`
- Installed/source files: 99/99 byte-identical; no overlay or unexpected files.
- Aggregate SHA-256:
  `F2674593C563590092BA1ACEF977D88B5BD148E1186604B7491FF886D87CA3CE`
- Target:
  `C:\Users\LostSoul\Games\Age of Empires 2 DE\76561198053747760\mods\local\Rome at War AI\resources\_common\ai`

## Current defect ledger

| ID | Status | Immediate boundary / next action |
|---|---|---|
| `shipyard.sampler.t51` | FIXED-PENDING-RUNTIME | `ec3ee78` restored the T50 full X/Y candidate domain while retaining all safety/capacity gates. Fresh replay must show multi-player concrete foundations. |
| `villager.order706` | INVESTIGATING | T53 tests four ordinary home-economy writers with Ctrl persistence; exact cause remains unproven. Correlate codes 640-657 to the same actor's pre/post/later 706 stream. |
| `villager.keystates.t53` | EXPERIMENTAL / FIXED-PENDING-RUNTIME | Retain only if verified runtime shows a material actor-level 706 reduction with persistent assignments and no worker/transport/garrison regression; otherwise revert `5ece337` only. |
| `assault.preparation.close-boarders` | INVESTIGATING | T51 passengers were 2-7 tiles away with exact hull/group/enter intent yet eight Gray cycles terminated. Reconstruct physical blockage/reissue/ownership at each abort. |
| `migration.productive-dropsite` | OPEN | Launch/landing works. Require autonomous exact foundation -> ready -> retask -> gather -> deposit, without manual intervention. |
| `merchant.row.real-choke` | INVESTIGATING | T52 diagnostics arm only on an actual priority-hull episode. Require one-at-a-time yield, hull progress, then native trade resumption. |
| `expedition.commitment` | INVESTIGATING | Observation only until all earlier gates are judged; do not tune yet. |

Runtime-confirmed behavior to preserve: landed-assault target acquisition and
combat continuation; T50 land trade; T51 autonomous migration launch/landing;
three independent assault slots, useful-partial manifests, shoreline/path and
danger validation, migration/relic separation and bounded naval cooperation.

## Validation baseline

- T53 focused tests: 9/9 PASS; key-state validator: PASS (exactly four bounded
  Ctrl wrappers); ownership inventory: 1,028 sites, zero direct failures.
- Full Python 3.12 discovery: 556/556 PASS (the sandboxed run hit the known
  Windows Temp permission boundary; the approved unrestricted rerun passed).
- PER structure/operand validation: PASS.
- Strategy execution: 1,156 matchups, zero errors.
- Naval doctrine, ownership, replay benchmark metadata (42), context metadata,
  and `git diff --check`: PASS. The read-only strategy synchronizer reports six
  pre-existing generated civ files it would update; T53 changed none of them.
- `validate_good_units.py` has a known frozen-provenance mismatch at
  `source_provenance/AI RAW.per_sha256`; do not silently rebaseline it.

## Exact next action

Analyze the next verified marker-501 replay. Reconstruct each 640-657 episode with
`tools/analyze_economic_retasks.py`: compare the exact actor's 30-second pre/post
706 rate, assignment/role/target persistence and later recurrence; enumerate
major unsampled actors. Accept or revert `5ece337` from runtime evidence, keep
`villager.order706` INVESTIGATING until causality is established, then resume
the remaining ordered T52 runtime gates.
