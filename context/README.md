# Agent context architecture

This directory routes agents to the smallest authoritative context needed for a
task. It does not replace source, tests or evidence reports.

## Temperature and authority

| Tier | Contents | Normal use |
|---|---|---|
| Hot | Root `AGENTS.md`, root `HANDOFF.md`, current fields and accepted findings in `project-state.json` | Primary reads for substantial tasks; specialists receive relevant invariants and a task capsule. Keep concise and current. |
| Warm | `nodes.json`, `roles.json`, active task capsules, and the specific source/tests/reports named by a context packet | Load only for the selected task/subsystem/role. |
| Cold | `archive/`, old T-series reports, raw replay metadata, full ownership inventories, writer-site maps, generated outputs and complete traces | Retain and index; open only when a relevant claim is challenged or provenance is required. |

Authority is category-specific:

- Git/source files: implementation truth.
- Tests and validators: mechanical invariants, not engine-runtime proof.
- `project-state.json`: current accepted findings and defect status.
- Root `HANDOFF.md`: current workspace, runtime identity and exact next action.
- Task capsule: current objective, scope, dependencies and stopping conditions.
- Detailed reports/replay metadata: provenance. Newer accepted state wins unless
  direct contradictory evidence formally reopens it.

The archived AGENTS and HANDOFF files are historical records, not competing
current authority. Paths inside the archived handoff are repository-root
relative unless explicitly absolute.

## Selective context assembly

List available nodes and roles:

```powershell
py -3.12 tools/context_pack.py --list
```

Build a bounded packet:

```powershell
py -3.12 tools/context_pack.py subsystem.shipyard --role implementer
py -3.12 tools/context_pack.py task.t52-runtime --role runtime-analyst
```

The tool emits summaries, direct dependencies, relevant accepted findings,
authoritative paths and evidence references. It deliberately does **not**
concatenate referenced files. Open only the references needed for the current
hypothesis or action. Validate metadata with:

```powershell
py -3.12 tools/context_pack.py --check
```

## Economy-first agent routing

The current primary agent owns ordinary tasks; `worker` in route output names
that primary, not another spawned agent. Planning, research and review requests
alone do not require delegation. Project-scoped
agents under `.codex/agents/` are optional read-only capabilities, not stages.
Inspect the deterministic route for a representative task class with:

```powershell
py -3.12 tools/context_pack.py --route trivial-edit
py -3.12 tools/context_pack.py --route architectural-change --mode high-assurance
```

`context/agent-routing.json` defines the delegation gate, modes, task classes,
capabilities, escalation order and compact result contract. It deliberately
does not auto-spawn anything. A parent that decides one capability is justified
passes only a task delta plus one role-filtered context packet. Use
`context/task-capsule-template.json` for ad-hoc delegation; existing active task
capsules may retain richer project-specific fields.

Repository `.ignore` keeps the archive, replay reports and largest generated
evidence artifacts out of ordinary broad ripgrep discovery. They remain tracked
and can be searched by explicit path or with `rg --no-ignore` when a packet
identifies them as relevant.

## Maintenance

- Replace the root handoff's current state; never resume append-only history.
- The primary owns shared-state edits; specialists return findings. Routine
  questions and trivial edits need no new capsule or handoff ceremony.
- Update existing finding IDs rather than duplicating conclusions. A finding is
  reopened only when new direct evidence contradicts it; record that evidence
  and change status/next action.
- Add task capsules only for substantial active work. Keep objective, direct
  dependencies, authoritative files, constraints, validation and stopping
  conditions concise. Archive or supersede completed capsules explicitly.
- Add graph edges only when they affect context selection (`depends_on`,
  `related_to`, `validates`, `evidence`, `supersedes`); do not model every file.
- An optional agent receives the selected packet for its role plus the exact
  patch or evidence it must inspect—not the full repository history. The parent
  remains responsible for routing, global instructions and current state.
- Convert stable mechanical invariants into tests. Keep explanations linked,
  but do not make future agents reread the historical proof for each run.

## Measured baseline

Before this layout, routine entry points alone were approximately 49,900 words
and 410 KB (`AGENTS.md` plus append-only `HANDOFF.md`). The 28 T-series reports
added about 379 KB, while the ownership inventory and writer-site map added
hundreds of kilobytes more when broadly searched.

The guarded target is under 30 KB for global AGENTS + current HANDOFF + current
state, with a narrow subsystem packet remaining under 12 KB. Tests enforce
those ceilings. The expected routine reduction is roughly 85-95%, depending on
the selected task. Detailed evidence remains on demand, so this is reduced
rereading rather than discarded knowledge.

Deliberately not implemented: a database, vector store, service,
repository-wide dependency graph, automatic source summarization, agent queue,
or auto-spawning orchestrator. The current scale does not justify their
maintenance or recurring context cost.
