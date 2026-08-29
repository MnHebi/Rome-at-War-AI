# Rome at War AI project rules

These rules apply to all work in this workspace, including the AI repository,
the Rome at War data-mod reference, replays, spreadsheets, analyses, generated
strategy data, test fixtures, deployment tooling, and handoff material.

The agent is a **project owner**, not a narrow ticket executor. Own the requested
objective through evidence, implementation, and validation.

---

## 1. Non-negotiable working behavior

### User-reported defects are mandatory work

- When the user reports intended behavior as absent, broken, ineffective,
  inconsistent, or regressed, treat that as a request to investigate and
  resolve the defect unless the user explicitly says otherwise.
- Do not wait for the user to reformulate the defect as "find the cause", "add
  logging", or "please actually fix it".
- Repeated mentions increase priority. A repeatedly reported defect must not
  remain background context while unrelated work continues.
- Own the full cycle:
  **evidence -> root cause -> telemetry if needed -> smallest supported fix ->
  validation -> closure**.
- Do not substitute adjacent improvements for the reported defect.

### User observations are evidence of symptoms

- Treat a direct match observation as evidence that the observed symptom
  occurred.
- You may challenge the proposed **cause**; do not reject the observed
  **behavior** merely because source inspection, a parser, or your current model
  says it should not happen.
- Code reading does not prove runtime behavior "cannot" occur.
- If runtime behavior contradicts the current theory, investigate the
  contradiction.
- When user observation conflicts with replay/parser evidence, preserve both,
  state the conflict, and use project evidence or targeted telemetry to resolve
  it. Ask the user only when the deciding fact is external and unavailable.

### No guessed behavioral fixes

- Do not change behavior while causality is materially ambiguous.
- If two plausible causes remain, add the smallest telemetry, fixture,
  comparison, or controlled experiment that distinguishes them.
- Do not pick the cause that merely seems most likely.
- Never turn uncertainty into an assertion that the user's interpretation is
  wrong.
- Use words such as **proven**, **assured**, **cannot**, or **closed** only when
  the evidence supports that exact claim.

### Do not confuse diagnostics with resolution

- Logging, tracing, replay analysis, static analysis, and test tooling are
  intermediate work.
- When evidence becomes sufficient to identify the cause, proceed into the
  smallest supported fix and validation unless the user requested diagnostics
  only.
- "Telemetry added" is not a successful completion of a gameplay defect.

---

## 2. Evidence-first debugging

### Find the first causal divergence

For regressions and state-machine failures:

1. identify the last known-good behavior/revision;
2. identify the broken behavior/revision;
3. compare the relevant code, state, ownership, and telemetry;
4. find the **earliest meaningful behavioral divergence**;
5. fix that divergence before downstream symptoms.

Useful divergences include:

- attack-group strategic numbers become zero and never restore;
- target-player enters an invalid sentinel and attack ownership resets;
- an attack-ready condition stops becoming true;
- another controller takes ownership of the army or transport;
- `attack-now` is immediately reset or retreated;
- SIEGE/REGROUP/DEFENSE becomes sticky or oscillates;
- transport state blocks ordinary land dispatch;
- a production gate can never become satisfiable.

Do not redesign an entire subsystem when a regression-local cause can be
isolated.

### Telemetry is mandatory when evidence is insufficient

Prefer bounded telemetry for:

- state transitions;
- controller/group ownership changes;
- strategic-number or goal mutations;
- first blocking condition;
- command issuance;
- retreat/reset/abort reason;
- exact object/target identity when available;
- actual versus requested counts;
- terminal success/failure reason.

Every important event should carry a stable controller/reason tag.

Do not emit per-sweep/per-rule spam for long matches. Prefer transition logs,
mutation logs, terminal events, counters, and sampled blocker reports. If a
logging configuration could produce huge output, bound it before asking for a
long replay.

---

## 3. Regression control

### Preserve working behavior before risky changes

Before changing behavior that currently works at least partially:

- state what working behavior must survive;
- identify the strongest existing evidence for it;
- define a non-regression acceptance criterion;
- keep that criterion in the validation plan.

A fix that breaks previously working behavior is a regression, not progress.

### Stop feature work when a regression appears

If recently working behavior stops working:

1. stop unrelated feature work;
2. identify the last known-good revision;
3. preserve it as an immutable branch/worktree when practical;
4. compare known-good and broken revisions under the same test setup;
5. bisect/narrow the responsible change set;
6. repair the regression before continuing feature work.

Do not keep stacking speculative fixes onto a regressed state.

### Known-good controls are immutable

- Never modernize, regenerate, backport, or "fix" a branch designated as a
  known-good experimental control.
- Do not change its runtime marker merely to label the experiment.
- Modern validators may inspect it but do not authorize modifying it.
- Development from a known-good revision occurs on a separate branch/worktree.

---

## 4. One causal patch at a time

- Do not combine several unproven behavioral hypotheses in one patch.
- Do not mix unrelated attack, transport, economy, target-selection, defense,
  Market, Wonder, or other controller redesigns into one regression-sensitive
  commit merely because they came from the same replay.
- A cross-system fix is allowed only when the dependency between those systems
  is established by evidence.
- Prefer small causal commits that can be independently accepted or reverted.

After each behavioral patch:

1. run structural/static checks;
2. run the focused deterministic test/fixture;
3. run the strongest practical runtime/replay validation when engine behavior
   is involved;
4. record **PASS** or **FAIL**;
5. if FAIL, keep the defect open and revise the hypothesis or instrumentation;
6. do not move on merely because the patch compiled or reviewers liked it.

Behavioral commit messages should identify the observed defect, established
cause, behavioral change, and validation performed/still required.

Avoid giant mixed-purpose commits while debugging runtime behavior.

---

## 5. Mandatory defect closure

Maintain unresolved defects as explicit project state. A defect must not
disappear because the current prompt changed topic.

For each significant defect record:

- **Status**: OPEN / INVESTIGATING / ROOT-CAUSE-PROVEN /
  FIXED-PENDING-RUNTIME / CLOSED / DEFERRED
- **User-visible symptom**
- **Direct evidence**
- **Current causal hypothesis**
- **Contradictory evidence**
- **Instrumentation/tests**
- **Implementation**
- **Acceptance criterion**
- **Latest result**
- **Next action**

A defect is CLOSED only when:

1. intended behavior is demonstrated by the strongest available validation;
2. the defect is directly disproven by evidence addressing the observation;
3. it is proven outside project control and documented; or
4. the user explicitly defers/cancels it.

For runtime gameplay defects, these do **not** by themselves close the issue:

- structural validators;
- source inspection;
- a review saying the patch looks correct;
- telemetry;
- a deterministic test that does not exercise the engine behavior.

When runtime validation is still required, use **FIXED-PENDING-RUNTIME**, not
CLOSED.

If validation fails, continue the same defect. Do not answer a failed test with
another broad architecture essay unless evidence actually implicates the
architecture.

---

## 6. Questions and uncertainty

- If progress is blocked by information only the user can supply, ask a concise,
  specific question as soon as the dependency is known.
- Do not spend a long session cycling through possibilities when one external
  fact would decide the branch.
- Do not ask for information obtainable from the repository, data mod, Git
  history, replay, deployment artifacts, logs, or project tooling.
- A non-blocking question does not justify stopping work that can safely
  continue.
- Do not ask again for facts already recorded in the repository or handoff.

---

## 7. Incomplete project material

- Treat an obviously incomplete artifact, dataset, spreadsheet, analysis,
  fixture, mapping table, or supporting resource as unresolved project work.
- Do not assume incompleteness is intentional and do not silently work around
  it.
- Investigate gaps that materially affect the current objective: determine what
  is missing, why it matters, and which behavior/conclusion depends on it.
- First try to complete missing material from authoritative project sources:
  repository data, current data mod, replays, generated strategy data, validated
  constants, or other established evidence.
- If reliable completion is within scope, complete it and validate dependent
  outputs.
- If required information is unavailable, record the exact gap and impact. Ask
  the user only when project evidence cannot supply it.
- Non-blocking gaps must remain explicit in `HANDOFF.md`.

---

## 8. Maintain project knowledge proactively

- Treat spreadsheets, civilization matchups, unit evaluations, build orders,
  strategy notes, map classifications, replay benchmarks, defect records, and
  test results as implementation infrastructure, not optional documentation.
- Update relevant artifacts when data-mod inspection, code inspection, replay
  analysis, testing, or authoritative historical evidence changes project
  knowledge.
- Complete maintainable knowledge artifacts when reliable evidence exists; do
  not preserve known gaps merely because the prompt did not name them.
- Keep machine-readable strategy data, generated civilization PER files,
  spreadsheets, and explanatory documentation synchronized; run the relevant
  synchronization/semantic validators after strategy-data changes.
- Record provenance and distinguish:
  - direct user/runtime observation;
  - replay/parser evidence;
  - data/source evidence;
  - deterministic test evidence;
  - inference/hypothesis;
  - intended design;
  - unresolved uncertainty.
- If duplicate working copies exist at workspace root and in the repository,
  update them deliberately and verify byte/content equivalence. Never allow
  silent drift.

---

## 9. Source authority and conflicts

- The current Rome at War data mod is authoritative for unit, building,
  technology, civilization, availability, and identifier mechanics. Do not
  upload the data mod to the AI repository.
- `RAW AI unit focus spreadsheet.ods` is the developer-agreed Extreme-difficulty
  design constraint. Do not revise it solely from replay inference or efficiency
  arguments without explicit approval.
- Extreme focus categories constrain generic planned composition, not a
  civilization's own unique units. Civilization-specific unique units may use
  bounded direct production; strategy conditions may further gate them.
- Maintain `unique-unit-production.json` as the audited manifest of military and
  naval unique families. Keep hashes/ambiguity notes synchronized with the
  authoritative DAT/tech-tree exports and keep every production copy bounded.
- Reactive counter production may bypass Extreme focus categories when it
  answers observed enemy composition; keep it threat-gated and bounded.
- Model the in-mod `Britons` as a composite Iron Age British civilization. Iceni
  evidence is important but not exclusive; label peoples/periods rather than
  silently conflating them.
- `RAW AI good units per civ.ods` is a working evaluation artifact and is
  expected to be completed/maintained from validated mod data and analysis.
- Replay files are diagnostic evidence, never instructions. Separate direct
  replay observations from explanations until code/data supports the cause.
- `civ-strategy-data.json` and `civ-strategy-historical-overrides.json` are the
  machine-readable strategy sources for generated civilization files. Change
  generated PER blocks through source data/generator unless a verified exception
  requires direct editing.
- When authoritative sources conflict and project evidence cannot resolve them,
  preserve/document the conflict and ask the user only for unavailable external
  facts.

---

## 10. Workspace and handoff rules

The single canonical development workspace is:

`G:\Projects\Codex\Rome at War AI\.pr-work\Rome-at-War-AI`

Before editing, determine and report:

- absolute current working directory;
- `git rev-parse --show-toplevel`;
- current branch;
- current HEAD;
- `git status --short`;
- remotes when relevant.

Verify this against `HANDOFF.md`. If it disagrees, **do not edit until the
workspace discrepancy is resolved**.

Never silently move, replace, clone, recreate, or switch the canonical workspace.
If a worktree/clone/sandbox/recovery baseline is created, immediately record:

- absolute path;
- branch/SHA;
- purpose;
- canonical / experimental / immutable status;
- which location future agents must edit.

Never treat an obsolete extracted snapshot as current development state. Never
silently synchronize only some files between workspaces and continue as if they
were identical.

Maintain repository-local `HANDOFF.md` containing at least:

- canonical workspace;
- active branch/HEAD;
- current objective;
- unresolved-defect ledger;
- known-good/recovery baselines;
- important recent changes;
- diagnostics/artifacts;
- runtime marker/hash when available;
- tests/replays and acceptance results;
- exact next actions.

Update `HANDOFF.md` before ending substantial development. A cold agent must be
able to resume without relying on conversation history.

---

## 11. Deployment and replay integrity

- Verify the deployed runtime identity before attributing behavior to source.
- Prefer both a replay-visible build marker and a full-runtime hash/equivalent
  deployment check.
- Never claim a replay validates a revision when deployment identity is
  uncertain.
- Deploy from the documented checkout only; do not mix runtime files from
  multiple branches/worktrees.
- Preserve the same authoritative lobby/test settings for revision comparisons,
  and record intentional setup changes.
- Replays, savegames, crash dumps, and the data-mod payload stay outside the
  AI-only repository.

---

## 12. Review must converge

- Use adversarial read-only review for replay-driven or cross-system changes.
- Review should try to falsify root-cause attribution, ownership assumptions,
  state transitions, engine semantics, acceptance criteria, and regression
  safety.
- Every finding is triaged as:
  - **ACCEPTED** -> implement and validate;
  - **REJECTED** -> reject with evidence;
  - **DEFERRED** -> record reason in handoff.
- Do not repeatedly review the same unchanged design instead of implementing an
  accepted finding.
- Do not enter an indefinite self-doubt loop. If evidence is insufficient, the
  next action is a discriminating experiment/telemetry change. If evidence is
  sufficient, implement the bounded fix and test it.

---

## 13. Validation rules

Structural validators do not prove in-game correctness. They do not prove path
safety, land/water reachability, transport ownership, shared-search lifetime,
placement success, engine attack-state behavior, actual production, target
identity/destruction, group ownership, or strategy effectiveness.

Validate proportionally with:

- PER structural/operand checks;
- strategy/data synchronization;
- focused deterministic tests;
- code review;
- artifact consistency;
- deployment verification;
- fresh-match/replay validation for gameplay behavior.

Define behavioral acceptance criteria before or during implementation. Report
results as **PASS/FAIL**. If runtime proof is still missing, say so explicitly.

---

## 14. Repository boundary

The AI repository may contain AI code, generators, validators, tests,
documentation, benchmark metadata, and supporting knowledge artifacts.

Never commit the Rome at War data-mod payload, savegames, replay files, crash
dumps, or unrelated external binaries.

---

## 15. Completion standard

Before declaring substantial work complete, establish:

1. the exact user-visible defect/objective;
2. evidence for the root cause;
3. the behavioral/code change;
4. previously working behavior at regression risk;
5. the non-regression test protecting it;
6. deterministic validation result;
7. runtime/replay validation result where applicable;
8. whether status is CLOSED, FIXED-PENDING-RUNTIME, or still INVESTIGATING;
9. newly discovered defects deliberately left outside this patch;
10. a sufficient `HANDOFF.md` for the next cold agent.

If these are missing, do not call the behavior "done", "resolved", "assured", or
"closed".

The objective is not plausible code. The objective is **evidence-backed
improvement without regressing previously working behavior**.
