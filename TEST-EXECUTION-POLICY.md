# Test execution policy (change-to-suite map)

Scope: which checks to run for a given change, and which checks are single-owner
gates rather than per-edit suites. This is a small explicit map, not an
automatic dependency-analysis or caching framework. Unknown dependency impact
widens the selection instead of guessing.

## Three different claims

| Claim | Owner | How it runs |
|---|---|---|
| A. A validator/generator behaves correctly | Unit tests of that tool, including negative fixtures | Its own test module |
| B. The current payload passes that validator/generator | The runtime gate, once per changed input set | `py -3.12 tools/validate_per.py`, `py -3.12 tools/generate_<area>.py` (no-write mode raises on stale output) |
| C. The engine accepts it | Runtime/replay evidence | Engine startup + replay, never a Python fixture |

Do not re-run B inside A's module; do not treat C as satisfied by A or B.

## Change-to-suite map

| Change | Run in the editing loop |
|---|---|
| Report, handoff or capsule text only | `py -3.12 tools/context_pack.py --check`, `py -3.12 -m unittest test_context_pack test_maintenance_consistency` |
| `.codex`, routing or context tools | `test_agent_routing`, `test_context_pack` (structured metadata, no model/prose pins) |
| Replay/log parser or matching rules | `test_command_boundary` (decoder/pairing fixtures), `test_writer_trace.WriterTraceToolTests`, `test_t11_replay_fixes` |
| File logging, command wrappers or shared PER control flow | `test_command_boundary_file`, `test_file_trace_capacity`, `test_command_boundary`, plus `py -3.12 tools/generate_command_boundary.py` |
| Command-boundary registry or generator | `py -3.12 tools/generate_command_boundary.py` (verifies every emitted file and hash), `test_command_boundary_file`, `test_file_trace_capacity` |
| Assault targeting/planning/recovery | `test_assault_plans`, `test_assault_missions`, `test_assault_screen_fallback`, `test_ownership_contract`, `test_shoreline_resolver` |
| Migration admission, boarding or colony construction | `test_migration_foundation`, `test_transport_acquisition`, `test_transport_lane_fairness`, `test_boarding_ctrl`, `test_t51_diagnostics` |
| Gate/wall/building placement | `test_validators` placement groups, `test_shipyard_coast`, `test_wonder_policy`, affected farm/migration placement tests |
| Trade, food, resource allocation, production | `test_fishing_policy`, `test_trade_topology`, `test_early_gold_bootstrap`, `test_reactive_ranged_threat`, `test_pre_backlog` |
| Unit data, civilization strategy, evaluator inputs | `test_validators` strategy/civ groups, `test_maintenance_consistency`, the affected generator plus the strategy matrix |
| Shared command contract, constants, load order, interpreter | Broad affected suites; one full current run at that completion point |

## Single-owner checks (do not duplicate in suites)

- Generator synchronization: each subsystem suite compares its own generator
  output (`test_shipyard_coast`, `test_naval_right_of_way`,
  `test_expedition_admission`, `test_assault_missions`, `test_assault_plans`).
  The aggregate copy in `test_t51_diagnostics` was removed rather than kept
  twice.
- Current-payload PER validation: `py -3.12 tools/validate_per.py` validates
  every root `.per`. Per-file forwarding tests of the same payload are not
  re-added; validator behavior is tested with negative fixtures instead.
- Current metadata validity: `context_pack.validate_metadata()` is asserted
  once, in `test_context_pack`.
- Physical command bridges: `test_command_boundary_file` covers every emitted
  site, so the retired legacy bridge test is gone.

## Opt-in historical coverage

Historical overlay/tool reconstruction validates a frozen commit, so it does
not gate current work. It stays runnable on demand:

```powershell
$env:RAWAI_HISTORICAL_OVERLAY_TESTS='1'
py -3.12 -m unittest test_writer_trace.WriterTraceTests
py -3.12 -m unittest test_validators.FarmPolicyTests.test_recall_caller_trace_covers_every_existing_global_recall
py -3.12 -m unittest test_validators.FarmPolicyTests.test_recall_diagnostic_preserves_every_t7_executable_rule
```

- `test_writer_trace.WriterTraceTests` (17 tests): frozen `a5de7d85` writer
  overlay compilation, jump relocation and reservation classification.
- `test_validators` recall-observer tests: frozen `a5de7d85` recall caller
  trace and the T7 executable-rule fingerprint.
- Current-tool coverage that replaced routine historical reconstruction:
  `WriterTraceToolTests` (synthetic control: compile/strip round trip,
  source-map fingerprint, string budget, double-instrumentation and collision
  refusal, private observer actions, decoder brackets/gaps/identity).
- Historical evidence itself is untouched: `tools/fixtures/`, archived
  reports, and `tools/boarding_sampling.py` (documented analysis CLI) remain.

## Retired artifacts

- `tools/test_boarding_sampling.py`: six tests of the retired four-report/
  180-second chat scheduler. The old producer is no longer generated for the
  current runtime; the fixture, the archived report and
  `tools/boarding_sampling.py` remain as evidence.
- Legacy chat emitter tests in `tools/test_command_boundary.py`: replaced by
  record-level decoder/pairing fixtures. `Observer`/`atoms` remain because
  `FileObserver` and `test_file_trace_capacity` build on them, and
  `Observer` no longer constructs the retired chat library.

## Cadence

Focused suites per batch; one full current discovery run per restructuring or
release candidate. Re-run a check only when its inputs, shared symbols,
interpreter or checked tool changed, or when there is a concrete failure to
investigate.
