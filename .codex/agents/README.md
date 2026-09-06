# Economy-first Codex capabilities

The primary Codex thread or built-in `worker` is the general worker. It owns
ordinary tasks end to end and does not delegate merely because these custom
agents exist.

The four project-scoped agents are optional capability leaves:

```text
worker
  |-- economy_scout      bounded discovery after targeted search is insufficient
  |-- economy_analyst    one difficult, evidence-backed reasoning question
  |-- economy_planner    cross-boundary design or explicit planning
  `-- economy_verifier   independent review when risk justifies its cost
```

Edges mean **may invoke**, never **must run next**. `AGENTS.md` owns the routing
policy; `context/agent-routing.json` is its machine-checkable representation.
Each delegated prompt consists of a compact task delta plus one relevant
`context_pack.py` packet. Agent results use `RESULT / EVIDENCE / ACTION /
UNCERTAINTY`, and optional agents must not delegate again.

Models are not pinned for the reasoning-heavy capabilities, so they inherit a
user/session-compatible model. The scout uses the locally supported lightweight
model and low reasoning because its job is mechanical, bounded discovery.

