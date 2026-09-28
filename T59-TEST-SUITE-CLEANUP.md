# T59 test-suite cleanup (RAW-test-suite-audit application)

Date: 2026-09-17. Canonical checkout
`G:\Projects\Codex\Rome at War AI\.trade-work\T30-trade-cap-civ-fix`, branch
`fix/trade-cog-cap-dacian`, base `e84cec9` plus preserved user edits. No
gameplay/per-file source change, no commit, no push, no deployment.

Objective: fewer obsolete test obligations and fewer repeated whole-payload
checks, without dropping protection against real project failures. Test count
is not a model-usage metric; the reductions below are specific and justified.

## Removed (28 test methods, plus nonfunctional assertions inside retained tests)

Method-count deltas verify the arithmetic: `test_validators` −1,
`test_pre_backlog` −1, `test_command_boundary` −9 (13 removed, 4 added),
`test_agent_routing` −4, `test_context_pack` +1 (1 removed, 2 added),
`test_t51_diagnostics` −2, `test_writer_trace` +5, `test_boarding_sampling`
−6 → 28 removed / 11 added / net −17, which matches the 690 → 673
full-suite difference.

| Location | Why it did not protect project behavior |
|---|---|
| `test_validators.ReplayMetadataTests.test_nonfinite_number_is_rejected` | Calls `json.dumps(..., allow_nan=False)` on `float("nan")`; stdlib behavior, never exercises the project `json_default` callback. Serializer/metadata tests retained. |
| `test_pre_backlog.ConcreteHeavyRemeTests.test_family_upgrade_and_queued_units_do_not_double_allowance` | Pure integer arithmetic simulating a `count < 4` loop; never reads or executes the production rules. Concrete census, selector and capped-producer contracts retained in the same class. |
| `test_command_boundary.test_source_bridges_preserve_ordered_original_actions_and_are_tamper_evident` | Permanently retired legacy bridge; `skipTest` under schema 2. Every physical bridge action order and hash is checked in `test_command_boundary_file`. |
| `test_command_boundary.test_no_list_mutators_shared_writers_or_new_strings_in_observer` | Same retired schema-1 path; file-mode private state, mutators and empty-string budget are checked in `test_command_boundary_file`. |
| `test_command_boundary` legacy chat-emitter suite (11 tests: pair/quota/pointer/rotation/traversal/stale-object/actual-target/duplicate-tracked/natural-traversal) | Executed the retired chat library via `Observer`; they froze scheduler internals rather than decoded evidence. Replaced by record-level fixtures (below). |
| `test_agent_routing.test_only_scout_pins_a_lightweight_model` | Exact personal model/effort pins; model choice is an editable preference, not correctness. |
| `test_agent_routing` model/effort pins in `test_project_config_limits_default_fanout_without_disabling_user_control` | Same; concurrency ceiling, absent `service_tier` and absent default subagent model retained. |
| `test_agent_routing.test_metadata_and_agent_files_are_valid`, `test_specialists_leave_shared_state_to_primary`, `test_representative_escalation_is_specific_and_sequential` (3 methods), plus the literal-prose assertions in the remaining methods (`Complete with the worker and stop`, `worker -> economy_`, role/description phrases) | A phrase occurring in instructions proves nothing about behavior, and the duplicated `validate_metadata()` call is covered once in `test_context_pack`. Structured topology, capability references, nested-delegation limits, output contract and the explicit no-subagent constraint remain. |
| `test_context_pack.test_task_packet_preserves_order_and_runtime_boundary` (hardcoded six-topic backlog order) | The backlog list is task data. Replaced by a controlled-graph `node_closure` order/depth test plus a runtime-vs-source identity test. |
| `test_maintenance_consistency` literal ban on `marker 500/502` in every finding `next_action` | Historical marker mentions are legitimate. Candidate/deployed marker identity and provenance checks retained. |
| `test_command_boundary_file` no-op `replace('gl-cbf-kind','gl-cbf-kind',1)` equality | Repeated the preceding comparison on identical input. All real bridge/hash/tamper checks retained. |
| `test_t51_diagnostics.test_generated_sources_are_synchronized` | Aggregated four generators already compared one-to-one in `test_shipyard_coast`, `test_naval_right_of_way`, `test_expedition_admission`, `test_assault_missions`, `test_assault_plans`. |
| `test_t51_diagnostics.test_changed_sources_pass_per_validation` | Forwarded `validate_file` over a static file list; the runtime gate `py -3.12 tools/validate_per.py` validates every root `.per`. Negative validator fixtures retained. |
| `tools/test_boarding_sampling.py` (whole module, 6 tests) | Tests of the retired four-report/180-second chat scheduler. The producer is no longer generated for the current runtime; fixture, archived report and the documented `tools/boarding_sampling.py` analysis CLI remain as evidence. |

## Replaced rather than deleted

- `test_command_boundary.CommandBoundaryTests` now decodes explicit historical
  record fixtures (`pair_records()` builds one actor/hull pair with named
  overrides) instead of executing the retired chat library. Retained claims:
  actor/hull displacement and separation, per-condition negative cases
  (stale, time mismatch, identity change, hull change, passenger/hull
  ownership, non-final member, invalid position), incomplete-frame and
  missing-field handling, packet attribution (`correlate` matching /
  unmatched-not-native-proof), cross-player incomplete frames, orphan ends,
  serial/abandoned/unclosed integrity, and legacy line endings.
- `Observer` remains as the execution base for `FileObserver`
  (`test_command_boundary_file`) and `test_file_trace_capacity`, but no longer
  constructs the retired chat library it was about to discard.
- `command_boundary_file.generate` no longer builds the legacy chat library and
  its coverage source (`generate_command_boundary.support_definitions()` now
  returns only the shared defs/init). No emitted file changed:
  `py -3.12 tools/generate_command_boundary.py` reports
  `PASS 579 rules 817 commands`.
- `test_release_regressions.SelfTargetRecoveryTests` self-identity check now
  asserts the behavioral invariant (one engine-sourced initializer, in an
  unconditional one-shot rule, loaded before the fallback owners, never a
  literal assignment) rather than the exact `up-get-fact` spelling. The
  surrounding self-guard, non-self selection and guard-removal mutation tests
  are unchanged.
- `tools/test_pre_backlog.source()` is cached per process; runtime sources are
  immutable during a test run.

## Historical coverage moved to opt-in

`RAWAI_HISTORICAL_OVERLAY_TESTS=1` re-enables, explicitly:

- `test_writer_trace.WriterTraceTests` (17 tests) — frozen `a5de7d85` overlay
  compilation, jump relocation, reservation classification.
- `test_validators.FarmPolicyTests.test_recall_caller_trace_covers_every_existing_global_recall`
  and `...test_recall_diagnostic_preserves_every_t7_executable_rule` — frozen
  `a5de7d85` recall-observer and T7 fingerprint controls.

Both were executed during this task: the 17 writer-overlay tests pass in
4.694 s, so the frozen evidence remains reproducible on demand. Current-tool
coverage that no longer needs the archive is
`test_writer_trace.WriterTraceToolTests` (5 tests) built from a synthetic
control payload: compile/strip round trip, source-map fingerprint change,
string budget counting and overspend rejection, double-instrumentation and
scratch/namespace collision refusal, private-only observer actions and
template-driven trace fields, and decoder bracket/gap/identity separation.

## Retained invariants and their locations

| Invariant | Test |
|---|---|
| PER syntax, operand domains, native-Age policy, load/storage budgets | `test_validators` (`PerDomainTests`, `FarmPolicyTests`), `validate_per.py` gate |
| Command-boundary physical bridges, action order and hashes | `test_command_boundary_file.test_all_physical_bridges_preserve_gameplay_actions_and_hashes` |
| All-player bootstrap, complete actor/target lists, release tracking, record loss/interleaving, relative jumps, mode on/off state | `test_command_boundary_file` |
| Current file-mode load/capacity and failed expanded emitter | `test_file_trace_capacity` |
| Historical decoder, orphan frames, serial/player integrity, pairing | `test_command_boundary.CommandBoundaryTests` |
| Ownership/exact-hull identity, partial loads, bounded recovery | `test_ownership_contract`, `test_bounded_recovery`, `test_migration_foundation` |
| Quarantine regression (executed) | `test_t55b_observability` |
| Generator synchronization per subsystem | `test_shipyard_coast`, `test_naval_right_of_way`, `test_expedition_admission`, `test_assault_missions`, `test_assault_plans` |
| Current-payload PER validation (claim B, once) | `py -3.12 tools/validate_per.py` |

Execution policy and the change-to-suite map: `TEST-EXECUTION-POLICY.md`.

## Checks run and results

- Focused after each batch: `test_agent_routing`, `test_context_pack`,
  `test_maintenance_consistency`, `test_pre_backlog`,
  `test_command_boundary_file`, `test_command_boundary`,
  `test_file_trace_capacity`, `test_release_regressions`,
  `test_t51_diagnostics`, `test_writer_trace`, plus
  `py -3.12 tools/generate_command_boundary.py` (unchanged output).
- Historical opt-in run: `test_writer_trace.WriterTraceTests`, 17 tests, OK.
- Final focused re-run of every touched module (`test_validators`,
  `test_pre_backlog`, `test_command_boundary`, `test_command_boundary_file`,
  `test_file_trace_capacity`, `test_agent_routing`, `test_context_pack`,
  `test_maintenance_consistency`, `test_release_regressions`,
  `test_t51_diagnostics`, `test_writer_trace`): **228 run, OK, 19 skips,
  31.303 s**.
- Final full current discovery: **673 collected, 653 passed, 1 failed, 19 skipped,
  93.243 s**
  (`py -3.12 -m unittest discover -s tools -p 'test_*.py'`). The 19 skips are
  the pre-existing 2 retired skips plus the 17 now-opt-in historical tests.
  Corrected accounting: an earlier version of this report wrote
  "672 PASS plus 19 skips out of 673", which double-counts; unittest's "Ran N"
  already includes skipped tests, so 673 = 653 passed + 1 failed + 19 skipped.
  Baseline before this task: 690 run / 688 PASS / 2 skips / 99.838 s.
  Complete log: `.analysis/test-cleanup-20260917/full-run.log` (project root,
  outside the AI repository).
- Measured change: 17 fewer default tests executed, 6.6 s shorter full run on
  this machine. Remaining expected saving is model-side: fewer obsolete
  obligations to read, edit and re-run. Neither number proves lower model
  usage.
- Runtime gate on the current payload: `py -3.12 tools/validate_per.py` → `{}`
  (no findings). Generator gate:
  `py -3.12 tools/generate_command_boundary.py` → `PASS 579 rules 817 commands`.
- `git diff --check` clean. No `.per` runtime file was written by this task;
  the newest runtime source timestamps remain 2026-09-12 (pre-existing user
  Age-alias edits, preserved).

## Failures, limits and unresolved items

1. `test_context_pack.test_handoff_identity_matches_structured_current_state`
   failed in the pre-cleanup dirty tree (and in the first cleanup full run)
   because `context/project-state.json:runtime_source_commit` holds composed
   prose (`... + working Age fixes; T58B-DEPLOYMENT.md`) that the rewritten
   HANDOFF did not contain verbatim. At HEAD the composed value was present in
   HANDOFF, so this is a local-state reconciliation gap, not a cleanup
   regression. Resolved by restoring the verbatim value in HANDOFF only (the
   structured field was not edited) and trimming handoff filler to stay under
   the 30 000-byte hot-context guard; `test_context_pack`,
   `test_maintenance_consistency` and `test_agent_routing` were re-run and pass
   (26 tests). No further full run was performed: the only changes after the
   full run were documentation/state text, and `test_context_pack` is the only
   suite that reads HANDOFF.
2. `rawai-init-goals.per` still reads self identity with
   `(up-get-fact my-player-number 0 gl-self-player-number)`, i.e. a
   PlayerNumber constant in the fact-id operand position. The test no longer
   freezes that spelling, but the engine-semantics question is open and was
   NOT changed here (no replacement semantics may be guessed). Reported
   separately; runtime evidence would be required before any fix.
3. The audit's escrow item ("literal-zero escrow GoalIds replaced by a valid
   no-escrow goal") has no corresponding implementation correction in this
   checkout: every `(up-can-build 0 c: ...)` and `(up-build <place> 0 c: ...)`
   site is unchanged and no no-escrow goal exists. Those validator
   expectations were therefore left intact; correcting them would have
   reversed current, locally verified behavior without evidence.
4. `test_validators.py` remains a 245 KB module mixing PER domains, replay
   metadata, gameplay source expectations and historical tracing. Splitting it
   by concern is recommended by the audit but was not part of this bounded
   batch.
5. Gate-first walling, protected gate approaches, construction ships, sea
   walls, migration policy and assault behavior were untouched, and existing
   wall/gate safety coverage was intentionally not removed.
6. Python fixtures still cannot prove engine pathing, ownership, placement,
   delivery or acceptance; a full run does not replace startup/load and replay
   evidence.
