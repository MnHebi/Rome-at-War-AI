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
- Current documentation/context HEAD at last update: inspect with
  `git rev-parse HEAD`; runtime source commit remains `e7031f9`.
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

- Node: `task.t52-runtime`
- Capsule: `context/tasks/t52-runtime.json`
- Detailed acceptance: `T52-RUNTIME-ACCEPTANCE.md`
- Load compact task context with:
  `py -3.12 tools/context_pack.py task.t52-runtime --role runtime-analyst`

Ordered runtime gates:

1. prove multi-player Shipyard recovery from T51's one-order regression;
2. attribute the first Villager order-706 onset using class-reserved writers;
3. resolve close active assault passengers that still fail to board;
4. prove autonomous migration foundation, gather and deposit productivity;
5. exercise Merchant right-of-way in a real late-game choke;
6. only then reassess expeditionary commitment.

## Installed runtime

- Marker: `RAWAI-P3B44T52:500`
- Runtime source commit: `e7031f9`
- Installed/source files: 99/99 byte-identical; no overlay or unexpected files.
- Aggregate SHA-256:
  `387913EFC902E0DF796532F16F31A4B05F7F265962B8AE43C39C7033433C28B5`
- Target:
  `C:\Users\LostSoul\Games\Age of Empires 2 DE\76561198053747760\mods\local\Rome at War AI\resources\_common\ai`

## Current defect ledger

| ID | Status | Immediate boundary / next action |
|---|---|---|
| `shipyard.sampler.t51` | FIXED-PENDING-RUNTIME | `ec3ee78` restored the T50 full X/Y candidate domain while retaining all safety/capacity gates. Fresh replay must show multi-player concrete foundations. |
| `villager.order706` | INVESTIGATING | Start at first 706 tuple; correlate exact actors with separately re-armed migration STOP writers and command counters before changing behavior. |
| `assault.preparation.close-boarders` | INVESTIGATING | T51 passengers were 2-7 tiles away with exact hull/group/enter intent yet eight Gray cycles terminated. Reconstruct physical blockage/reissue/ownership at each abort. |
| `migration.productive-dropsite` | OPEN | Launch/landing works. Require autonomous exact foundation -> ready -> retask -> gather -> deposit, without manual intervention. |
| `merchant.row.real-choke` | INVESTIGATING | T52 diagnostics arm only on an actual priority-hull episode. Require one-at-a-time yield, hull progress, then native trade resumption. |
| `expedition.commitment` | INVESTIGATING | Observation only until all earlier gates are judged; do not tune yet. |

Runtime-confirmed behavior to preserve: landed-assault target acquisition and
combat continuation; T50 land trade; T51 autonomous migration launch/landing;
three independent assault slots, useful-partial manifests, shoreline/path and
danger validation, migration/relic separation and bounded naval cooperation.

## Validation baseline

- Focused T52 controller tests: 192 PASS.
- Agent routing/context tests: 18/18 PASS.
- Full Python 3.12 discovery: 547/547 PASS (the sandboxed run hit the known
  Windows Temp permission boundary; the approved unrestricted rerun passed).
- PER structure/operand validation: PASS.
- Strategy execution: 1,156 matchups, zero errors.
- Naval doctrine, generated synchronization, ownership contract (27), replay
  benchmark metadata (42), and `git diff --check`: PASS. Line-ending warnings
  are expected for legacy PER files.
- `validate_good_units.py` has a known frozen-provenance mismatch at
  `source_provenance/AI RAW.per_sha256`; do not silently rebaseline it.

## Exact next action

Analyze the next marker-500 replay against `T52-RUNTIME-ACCEPTANCE.md`, beginning
with Shipyard episode reconstruction. Do not call any runtime-sensitive defect
closed from static tests or from the presence of telemetry alone. Persist new
accepted findings in `context/project-state.json`, update the T52 capsule, and
replace this handoff's active/result sections rather than restoring append-only
history.
