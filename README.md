# Rome-at-War-AI

An AI for the Age of Empires II: Definitive Edition mod *Romae ad Bellum*
(*Rome at War*), built on the AIBuilder AI included with AoE2: DE.

All 34 playable civilizations now have difficulty-specific unit-composition
priorities, opening affinities, and strategic specialties. Below Extreme, the AI
uses historically informed combined-arms profiles that may include units outside
the focus workbook. Extreme uses the max-return profiles in
`civ-strategy-data.json`, constrained by the agreed unit-focus workbook for its
generic planned composition. Civilization-specific unique units and bounded
reactive counters such as Skirmishers are exempt from those category
restrictions. The audited unique-family roster and its mod-data provenance are
stored in `unique-unit-production.json`. Lower-difficulty differences are stored in
`civ-strategy-historical-overrides.json`, and the model is explained in
`HISTORICAL_STRATEGY.md`.

Opening affinities are executable on Moderate and above. Enemy civilization
profiles adjust the configured openings according to their early army,
specialties, and battlefield counters; tied top-tier choices can produce a
combined-arms rush. Matchups never add a rush that is absent from the active
difficulty profile.

Bundled AI validation and maintenance tools live in the `tools` directory:

- `sync_civ_strategies.py` validates both difficulty profiles and updates every
  civ PER;
- `validate_per.py` checks PER structure, preprocessor balance, constants,
  technology/training operands, TargetAction/ActionId/OrderId domains, DUC
  group IDs, and guarded research alignment;
- `validate_strategy_execution.py` checks unit-role coverage, unit-line actions,
  rush activation/execution, every manifest-listed unique production path,
  calibrated Roman/Briton technology escrow, the enemy matchup matrix, and every
  difficulty preprocessor branch;
- `test_validators.py` provides synthetic regression cases for multiline PER
  operand errors, research ambiguity, role leakage, finite family bounds, and
  late-phase reachability; and
- `evaluate_good_units.py` reconstructs fully upgraded per-civilization unit
  statistics from an external Rome at War DAT/tech-tree export and writes the
  reviewable AI-side `good-unit-evaluations.json` knowledge artifact;
- `validate_good_units.py` rejects blank, malformed, or incomplete unit-rating
  matrices and unique-unit leakage;
- `validate_good_units_workbook.py` reads the generated ODS back and requires
  every rating and unique-unit type to match the JSON knowledge artifact;
- `validate_replay_benchmarks.py` requires source hashes, separates direct
  observations from inferences, and rejects path-bearing replay metadata; and
- `sync_test_ai.py` hash-checks or copies only the top-level `.ai`/`.per`
  runtime payload into an explicit `resources/_common/ai` test-mod directory,
  reports an aggregate payload hash, and reports obsolete runtime files without
  deleting them; and
- `read_ods.py` provides read-only inspection of the two AI planning workbooks.

Replay-derived runtime observations, implementation inferences, acceptance
criteria, and unresolved engine limitations are kept separately in
`replay-benchmarks.json`. Replay files themselves are never committed.

The Rome at War data mod and DAT maintenance utilities are intentionally not
part of this repository.

Special thanks: Leif Ericson from the AI Scripters Discord; Promiskuitiv and
Archon for shipyard placement code derived from the Definitive Edition AI; and
Promiskuitiv for help with taunt commands.
