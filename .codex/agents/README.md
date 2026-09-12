# Economy-first Codex capabilities

The primary Codex thread is the general worker. It owns
ordinary tasks end to end and does not delegate merely because these custom
agents exist.

The four project-scoped agents are optional capability leaves:

```text
worker
  |-- economy_scout      bounded discovery after targeted search is insufficient
  |-- economy_analyst    one difficult, evidence-backed reasoning question
  |-- economy_planner    justified design delegation or a requested separate planner
  `-- economy_verifier   independent review when risk justifies its cost
```

Edges mean **may invoke**, never **must run next**. `AGENTS.md` owns the routing
policy; `context/agent-routing.json` is its machine-checkable representation.
Each delegated prompt consists of a compact task delta plus one relevant
`context_pack.py` packet. Agent results use `RESULT / EVIDENCE / ACTION /
UNCERTAINTY`, and optional agents must not delegate again.

`worker` above means the primary, not a spawn. Ordinary planning/research/review
requests specify an output; independent-agent requests and the delegation gate
determine whether a specialist is needed. Specialists never edit shared state.

Project defaults: `gpt-6-astra`/`medium`; planner `medium`, analyst/verifier
`high`, scout explicitly `gpt-5.6-luna`/`low`. The three unpinned specialists'
effective models depend on configuration layers and spawn/session overrides;
do not infer them from role names or self-reports. Fast/service tier is unset
here, not guaranteed disabled. No usage savings or live agent discovery are
claimed by file validation.

The [official subagent schema](https://developers.openai.com/codex/subagents)
supports project-local custom agents and a child-thread concurrency ceiling.
Two slots are a ceiling, not a target. No paid specialist test calls are needed
for TOML validation; confirm discovery/effective settings in a fresh task.
