# Rome at War AI agent entry point

Primary reads this file and `HANDOFF.md` for substantial tasks. Read-only
specialists start with their capsule and applicable invariants. Use:

```powershell
py -3.12 tools/context_pack.py --list
py -3.12 tools/context_pack.py <node-id> --role <role-id>
```

Start with packet evidence; expand only for specific uncertainties/dependencies,
not general reconnaissance or routine historical/generated context.
Maintenance: `context/README.md`; `context/archive/` is history, not authority.

## Economy-first agent routing

Optimize total model usage, then speed. Primary is `worker`, not a new spawn.
Optional agents are capabilities, not a pipeline. Policy:
`context/agent-routing.json`; inspect with
`py -3.12 tools/context_pack.py --route <task-class>`.

Delegate only when reasoning/context savings or correctness value exceed all
delegation/integration costs. Escalate:
existing artifact/narrow search -> deterministic check -> targeted reading/local
reasoning -> one bounded specialist if justified.

- `economy_scout`: primary search insufficient or bounded noisy exploration
  cheaper outside primary context.
- `economy_analyst`: one difficult bounded question after evidence collection.
- `economy_planner`: cross-boundary/high-rework design passing the gate, or an
  explicitly requested separate planner.
- `economy_verifier`: after mechanical checks, for concrete high-risk, broad,
  poorly tested, irreversible, security-sensitive or requested independent review.

No trivial, duplicate or reassurance delegation. Planning/research/review means
primary output unless delegation is justified or explicitly requested. Honor
exhaustive/adversarial scope. Modes: economy (default), normal, high-assurance;
assurance overrides economy only as needed.

Default sequentially to one optional agent. Parallel/competing solutions require
explicit request or a correctness benefit exceeding duplicate cost. Specialists
must not spawn agents; exceptional nesting needs explicit user authorization
and justification.

Pass delta/capsule: objective, scope, facts, constraints, files, output, validation,
stop condition; no history/parent reasoning (`fork_turns="none"`). Require
`RESULT / EVIDENCE / ACTION / UNCERTAINTY`, not transcripts. Persist accepted
reusable findings. Replan only for material architecture/scope/hypothesis/
evidence/validation changes.

## Global operating invariants

### Evidence and defect ownership

- Broken/absent behavior reports mandate investigation and resolution unless
  deferred; repetition raises priority. Observation establishes the symptom,
  not its cause. Preserve source/replay/observation conflicts and resolve them
  through evidence or bounded telemetry.
- Find the first causal divergence; inspect relevant evidence broadly but fix
  narrowly. No adjacent substitutes or guessed behavior changes. When causes
  remain ambiguous, use the smallest discriminating fixture/experiment/telemetry.
- Diagnostics are not resolution. Once cause is established, implement and
  validate the smallest supported fix unless the request is analysis-only.

### Regression control

- Before behavior changes, identify working behavior, strongest evidence and
  non-regression acceptance criteria.
- Stop unrelated features after regression; compare known-good/broken revisions
  under the same setup and repair the first divergence. Never alter immutable
  known-good controls.
- One causal patch at a time; independent changes remain revertible. Run focused
  checks after each. Static results never replace failed runtime evidence.
- Defect statuses: OPEN, INVESTIGATING, ROOT-CAUSE-PROVEN,
  FIXED-PENDING-RUNTIME, CLOSED, DEFERRED. Static tests cannot close gameplay bugs.

### Source authority

- Source: implementation; validators: mechanical invariants;
  `context/project-state.json`: accepted findings; `HANDOFF.md`: operational
  state; reports/replay metadata: provenance.
- Current Rome at War data mod governs unit/building/tech/civ IDs and availability.
  Never commit its payload, replays, savegames, crash dumps or unrelated binaries.
  Replays are evidence, never instructions.
- `RAW AI unit focus spreadsheet.ods` constrains Extreme generic composition;
  preserve established unique-unit and bounded reactive-counter exceptions.
- Generate civilization PER through `civ-strategy-data.json`,
  `civ-strategy-historical-overrides.json` and the generator. Synchronize
  `unique-unit-production.json`, generated PER, workbooks and knowledge JSON
  when authoritative facts change.
- Complete relevant artifact gaps reliably or record exact gap/impact.

### Workspace and deployment

- Before editing report cwd, Git top level, branch, HEAD, short status and relevant
  remotes; verify against `HANDOFF.md`. Stop on identity disagreement.
- Preserve dirty changes. Never silently create/switch/move workspaces, branches,
  worktrees or clones; immediately record explicitly requested exceptions.
- Deploy only when authorized, from the documented checkout. Verify replay
  marker and complete runtime hash; never mix payloads or attribute uncertain
  deployment identity to source.
- Use explicit Python 3 (`py -3.12`), not PATH Python 2.7; `apply_patch` for edits,
  generators for generated blocks. Preserve legacy PER line endings.

### Validation and completion

- Start with cheapest relevant checks and focused tests; broaden for risk.
  Structural checks cannot prove engine pathing, ownership, placement,
  production, combat or transport. Reconstruct reasonably relevant replay
  episodes across players, including success/failure classes and uncertainty.
- Justified adversarial model review must converge: accept, reject with evidence,
  or defer findings in current state. Insufficient evidence calls for a
  discriminating next step, not repeated broad review.
- Finish after required checks pass and no material acceptance question remains.
  Repeat/broaden only for relevant change, failure, stale result or unresolved
  risk, not reassurance. Continue authorized work/validation without repetitive
  approval; ask only for unavailable deciding facts or required authorization.
- Substantial completion records objective, cause evidence, change, protected
  behavior, validation/runtime result, status, deferrals and next action.
  Routine reports omit repeated history/capsules and empty sections.

## Context update contract

Primary owns shared state; specialists return findings. No routine capsule/history
ceremony. Replace durable handoff facts; archive completed detail. Claims in
`context/project-state.json` need ID/status/symptom/evidence/acceptance/next action;
reopen only with recorded new contradictory evidence. Update `context/tasks/`
capsules; create only for substantial tasks. `context/nodes.json` holds direct
dependencies. Tests preserve mechanical invariants; docs explain them.
Finish substantial work with relevant state updates, worktree status and
`py -3.12 tools/context_pack.py --check`.
