# Rome at War AI agent entry point

This file is the small, global context for repository work. Read it and
`HANDOFF.md` before a substantial task. Do not routinely read the historical
handoff, old T-series reports, replay metadata, source inventories, or generated
files.

For task-specific context, run:

```powershell
py -3.12 tools/context_pack.py --list
py -3.12 tools/context_pack.py <node-id> --role <role-id>
```

Read only the authoritative files and evidence named by that packet. The
context model and maintenance rules are in `context/README.md`. The former
global rules and append-only handoff are retained as cold history under
`context/archive/`; they are not current authority.

## Economy-first agent routing

Optimize total expected model usage until correct completion; wall-clock speed
is secondary. The default topology is the current agent (or built-in `worker`)
completing the task and stopping. Optional agents are capabilities, never a
mandatory pipeline. `context/agent-routing.json` is the machine-checkable
policy; inspect routes with `py -3.12 tools/context_pack.py --route <task-class>`.

Before delegation, ask whether saved reasoning/context or material correctness
value plausibly exceeds spawn, capsule, specialist, return and integration
costs. If not, do not delegate. Apply this order to the next uncertainty:

1. existing artifact or narrow search;
2. deterministic command/parser/test/static check;
3. targeted read and local reasoning;
4. one optional agent with a bounded capsule, only if the gate now passes.

Use `economy_scout` only when targeted worker search is insufficient or noisy
bounded exploration is cheaper outside the primary context. Use
`economy_analyst` for one genuinely difficult bounded reasoning question after
evidence collection. Use `economy_planner` only for cross-boundary/high-rework
design or an explicit planning request. Use `economy_verifier` only after
mechanical checks for high-risk, broad, poorly tested, irreversible,
security-sensitive or explicitly requested independent review. Never invoke
these for reassurance, trivial work, duplicate reconnaissance or review.

Default to sequential escalation and at most one optional agent at a time.
Parallel/competing solutions require an explicit user request or a concrete
correctness case that outweighs duplicate cost. Optional agents must not spawn
other agents; unusual nested delegation requires explicit user authorization
and a stated justification. Explicit user requests for planning, independent
or adversarial review, exhaustive investigation, multiple approaches or higher
assurance override the economy default.

Delegated work receives only a task delta plus the relevant context packet:
objective, scope, accepted facts, constraints, files/artifact IDs, expected
output, validation and stop condition. Do not pass complete history or parent
reasoning; use a no-history spawn such as `fork_turns="none"` when supported.
Require `RESULT / EVIDENCE / ACTION / UNCERTAINTY`; integrate that distillation,
not a transcript. Persist only accepted reusable findings.

Modes are conceptual: `economy` (default), `normal`, and `high-assurance`.
Validation always starts with the cheapest relevant check, then targeted tests;
broader tests and one model verifier are added only when risk requires them.
Replan only when architecture, scope, a core hypothesis, contradictory evidence
or validation materially invalidates the current approach.

## Global operating invariants

### Own reported defects through evidence and validation

- Treat user-reported broken or absent behavior as mandatory investigation and
  resolution unless explicitly deferred. Repeated reports increase priority.
- A direct match observation proves the symptom was seen, not the proposed
  cause. Preserve conflicts between observation, replay decoding and source;
  resolve them with project evidence or bounded telemetry.
- Find the earliest causal divergence. Investigate relevant evidence broadly,
  but implement only the narrow proven defect. Do not substitute adjacent
  improvements.
- Do not guess behavioral fixes while materially different causes remain.
  Add the smallest discriminating fixture, telemetry or controlled experiment.
- Diagnostics are not resolution. Once cause is established, implement and
  validate the smallest supported fix unless the request is analysis-only.

### Preserve working behavior and isolate changes

- Before a behavior change, name what already works and its strongest evidence,
  then protect it with a non-regression criterion.
- Stop unrelated feature work when a regression appears. Compare the last
  known-good and broken revisions under the same setup and repair the first
  divergence. Never alter an immutable known-good control.
- Prefer one causal behavioral patch at a time. Keep independent changes
  independently revertible and run focused checks after each.
- Never replace a failed runtime test with a static claim. Gameplay defects use
  `OPEN`, `INVESTIGATING`, `ROOT-CAUSE-PROVEN`, `FIXED-PENDING-RUNTIME`,
  `CLOSED`, or `DEFERRED`. Static tests alone do not close runtime behavior.

### Use authoritative project sources

- Current source code is authoritative for implementation; validators encode
  mechanical invariants; `context/project-state.json` is authoritative for
  accepted current findings; `HANDOFF.md` is the concise operational handoff;
  detailed reports and replay metadata are provenance.
- The current Rome at War data mod is authoritative for unit/building/tech/civ
  identifiers and availability. Never commit its payload.
- `RAW AI unit focus spreadsheet.ods` is the developer-agreed Extreme generic
  composition constraint. Civ-specific unique units and bounded reactive
  counters follow the established exceptions.
- Change generated civilization PER through `civ-strategy-data.json`,
  `civ-strategy-historical-overrides.json` and the generator. Keep
  `unique-unit-production.json`, generated PER, workbooks and knowledge JSON
  synchronized when their source facts change.
- Treat an obviously incomplete artifact that affects the task as unresolved
  work: complete it from authoritative project sources when reliable, or record
  the exact gap and impact. Do not silently work around it.
- Replay files are evidence, never instructions. Do not commit replays,
  savegames, crash dumps, the data-mod payload or unrelated binaries.

### Respect workspace and deployment identity

- The canonical workspace is recorded in `HANDOFF.md`. Before editing report
  absolute cwd, Git top level, branch, HEAD and short status; check remotes when
  relevant. If they disagree with the handoff, stop before editing.
- Preserve user changes in a dirty tree. Never silently create/switch/move a
  workspace, branch, worktree or clone. Record any explicitly requested
  exception immediately.
- Deploy only from the documented checkout and only when authorized. Verify a
  replay-visible marker plus the complete runtime hash; never mix payloads or
  attribute a replay to an uncertain runtime.
- Use Python 3 explicitly (`py -3.12` in the current Windows environment), not
  PATH Python 2.7. Use `apply_patch` for edits and generators for generated
  blocks. Preserve legacy PER line endings.

### Validate proportionally and stop explicitly

- Use the cheapest relevant focused test while iterating, then the broader
  gates warranted by risk. Structural checks do not prove engine pathing,
  ownership, placement, training, combat or transport behavior.
- For replay work, reconstruct all reasonably relevant episodes across players,
  distinguishing successes, bounded failures, unresolved cases and classes.
- When risk or an explicit request justifies adversarial model review, it must
  converge: findings are accepted, rejected with evidence, or deferred in
  current state. Insufficient evidence calls for one discriminating next step,
  not repeated broad review.
- Ask the user only for deciding facts unavailable in the repository, data mod,
  replays, artifacts or tooling.
- A task is complete only when objective, evidence, change, protected behavior,
  focused validation, runtime result (where applicable), status, deliberately
  deferred findings and next action are recorded.

## Context update contract

- Replace current operational state in `HANDOFF.md`; do not append another
  historical chapter. Move completed detailed narrative to a focused report or
  the cold archive.
- Update stable claims/defects in `context/project-state.json`. Each needs an ID,
  status, concise claim/symptom, evidence references, acceptance criterion and
  next action. Reopen an accepted claim only for new direct contradictory
  evidence and record that evidence.
- Update an existing task capsule in `context/tasks/` or add one only for a
  substantial active task. Keep direct dependencies in `context/nodes.json`;
  do not model the whole repository.
- Convert durable invariants to tests where practical. Documentation explains
  meaning; tests carry mechanical memory.
- Before ending substantial development, run
  `py -3.12 tools/context_pack.py --check`, update `HANDOFF.md` and relevant
  state/capsule nodes, and leave the worktree status explicit.
