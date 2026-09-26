# T58B engine Age operand audit - 2026-09-12

Status: FIXED-PENDING-RUNTIME. Canonical branch `fix/trade-cog-cap-dacian`,
base `e84cec97f557de501176462bfae898a91d1dff19` plus preserved user edits.
No deployment, commit or push in this audit.

## Findings and narrow correction

The user's manual replacements left two executable facts using
`early-antiquity-age`: `rawai-economy.per:3404` (`current-age !=`) and
`rawai-military.per:31047` (`players-current-age target-player >=`). Both now
use `feudal-age`. The Shipyard generator's diagnostic age-enumeration loop
still emitted all three custom aliases; its native-name list now preserves
the already-correct generated source on regeneration.

Observer metadata needed reconciliation: 32 registered originals had stale
hashes and/or incomplete Age substitutions. Each correction was checked
against HEAD with only engine-Age substitutions permitted, and emitted
bridges were checked against the same transform before refreshing hashes.
The registry and coverage identity were then regenerated. No command,
ownership, deadline, modifier or telemetry allowance changed. The frozen
installed-507 registry remains untouched.

The comment/string-stripped sweep covers all 108 root PER files, including
gitignored sources: all 463 engine Age facts use native names. Live
`generate*.py`/`sync*.py` sources have no remaining custom Age aliases.
RAW uppercase phase states, numeric `desired-age` goals, alias definitions
and `ri-*` technology identifiers remain in their separate domains.

## Validator and evidence boundary

`validate_per.py` now enforces native Age symbols for `current-age`,
`players-current-age` and `starting-age`. Only `starting-age` permits
`post-imperial-age`. Seven focused tests cover all three facts, numeric/custom
and phase operands, comments/strings, multiline nesting, separate domains,
all live PER sources and Shipyard generation. Two existing tests now expect
the corrected native names without changing their behavioral assertions.
The shared fixture interpreter now recognizes native Age names. Historical
writer-trace validation permits only the Age fact/operand pairs already
present in its immutable control (the observer duplicates guards). Its
existing round-trip test still checks original rule preservation; all other
validation remains enforced.

Cached reference: workspace `.analysis/airef-reference-20260830.js`, `pAge`
at lines 21840-21864, explicitly also lists IDs 0-3 and 105. Consequently,
native-name-only validation is a project domain policy, not evidence that
the engine rejects every numeric Age value. The user-observed log errors
remain evidence of a real symptom; their elimination by this correction is
not yet runtime-proven. The separate Invalid goal (0) issue is not closed.

## Acceptance and validation

Focused seven tests, PER validation, Shipyard/expedition generators,
command-boundary synchronization (579 rules/817 commands), Villager policy
(74 entries), and ownership audit (1071 sites, zero permission failures): PASS.
Final full Python3.12 discovery: **PASS, 690 run, 688 passed, two retired
skips (99.838 seconds)**. Rule capacity remains 9312/10000; no new runtime
rules or strings. `git diff --check`: PASS. Initial discovery exposed
temporary-file permission errors, stale test expectations and missing native
Age support in the fixture interpreter. The first approved-access rerun
isolated 38 fixture errors and the historical-policy exception. These were
corrected without modifying the historical control or live gameplay, and
full discovery was rerun.

Fresh runtime acceptance must show no Invalid age ID (0/1/2) flood while
age-gated economy, production, phase progression and transport admission
still function. Source/fixture checks do not close that runtime requirement.
