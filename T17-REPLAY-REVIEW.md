# T17A1 replay review — 2026-08-31 183134

## T19 follow-up — failed approaches remembered, loaded mission retained

**Status: FIXED-PENDING-RUNTIME. T19:467 deployed on user request.** Full91-file
installed/source hash `35526EFC8E958DB8BBC7C366B4126B123D676763287E890EA66BCA597D7B58DF`
matches; independent read-only deployment recheck PASS. Startup not yet observed.
Historical replay
results and T18 migration analysis below remain evidence of465, not proof of467.

### Established defect and authorized policy

The source immediately recalled after hard screening failures and stored no
failed opponent/approach. T17 Red repeated beach(137,137) after a reported attack;
the following missing-Scout event again terminated its accepted load. All-player
evidence below also contains11 two-candidate planner failures. Absence of memory
and narrow search is source-proven; availability of a safe alternative is NOT.
The user explicitly authorized remembering failures, expanding bounded search and
retaining the loaded mission while trying another plan. This implements that
policy, not a claim that all three Red assaults had a viable route.

### Implementation and bounds

- `tools/generate_assault_plans.py`, invoked by `generate_assault_missions.py`,
  produces `rawai-assault-plan-defs.per` and `rawai-assault-plans.per`. Storage is
  private goals15000–15333; it does not alias slot goals14600/14700/14800.
- A16-entry ring retains saved opponent, objective object ID, landing x/y, failure
  class and retry-after. Cache lookup excludes the same enemy's beach within12
  tiles on each axis even if another objective points at that beach. Lifetime300s;
  bounded ring eviction, not permanent blacklisting. Cache hits do not manufacture
  more failures or emit repeat failure logs.
- Accepted hull/manifest planning tries anchor, +/-28 and +/-56 lateral candidates.
  Same-island validation remains mandatory. Then up to three distinct enemy-owned
  objectives on that landmass, at least24 tiles from the current anchor; then
  another living enemy.
  Three exhausted objective plans or180s without dispatch deprioritize the enemy
  for300s. Finding no other objective also exhausts the bounded plan. At most
  three opponents and360s total; alternatives cannot refresh the total deadline.
  These are maxima, not promises to try every candidate before a deadline.
- Admission persists a preferred eligible overseas enemy separately from the
  ordinary global selector. Explicit replan alone changes the saved preparation
  enemy. Dispatched slots, their saved enemies and voyage watchdogs are unchanged.
  No rule writes `sn-target-player-number` or any `gl-am*` slot from this planner.
- Hard screening failures2/4/6/7/8/10/11 now enter AP-FAIL, record the candidate,
  release only the exact owned Scout and advance without unloading the hull or
  releasing passengers. Missing Scout is not asserted to mean death. Damage is
  detected by current attack status OR HP loss since acquisition, including damage
  whose transient attack flag already cleared.
- Every new candidate gets all-eight literal-hostile static defense checks at
  landing and waypoint before screening, and again after successful screening.
  Positive danger vetoes that candidate. A new candidate may acquire a free
  replacement Scout; absent/late screening uses the existing fresh-validation
  reasons3/5/9 only. Failure/loss at A never authorizes unscreened departure to A.
  Fallback denials for danger, geometry or invalid Scout enter candidate replanning;
  malformed enemy-scan state and invalid hull/manifest still recover.
- Full and already-accepted useful partial manifests (including5–9) are retained.
  Each pass revalidates exact hull ownership and accepted cargo. Lost ownership
  yields without commanding another controller's hull. No cargo growth requirement
  is introduced. Actual hull emergency/invalid manifest or exhausted search ends
  in the existing bounded recovery, not an indefinite planner loop.
- `AI RAW.per` loads the new definitions; `rawai-military.per` replaces only its
  small landing selector, admission seed and screening failure transitions;
  `rawai-assault-screen-fallback.per` redirects appropriate denials. The runtime
  marker changes in `rawai-init-goals.per`. All other pre-edit runtime files are
  byte-identical, including the three-slot controller and T18 migration routines
  outside the changed military section. Data mod and production policy untouched.

### Evidence and telemetry

Transition-only `RAW plan` fields report hull, original enemy, objective, landing
coordinates, failure reason and retry-after; explicit enemy changes also report
next-enemy. No per-rule/per-sweep chatter. Codes retain screening meanings:

|Code|Meaning|
|---|---|
|2|Both bounded corridor alternatives defended|
|4 /8|Scout attacked or lost HP during waypoint /beach screening|
|6 /10|Exact owned Scout unavailable during waypoint /beach screening; not proof of death|
|7 /11|Known defended waypoint /landing|
|21|Unknown target land zone or candidate on another zone|
|22 /23|Total preparation /per-enemy deadline exhausted|
|24|Hull/accepted manifest invalid, or hull reports attack|
|26 /27|No eligible other enemy /three-opponent limit reached|
|28 /29|Saved enemy unavailable /no longer hostile; original identity logged|
|32 /33 /35|Fallback rejected danger /landing geometry /Scout validity|

Existing code4 detailed cancellation reporting is retained and remains diagnostic
only; no diagnostic subcode is used as a behavior gate. A missing Scout never
becomes proof that the army disappeared.

### Regression control, adversarial review and results

Immutable pre-edit archive and full hashes are in `HANDOFF.md`. This patch is
independently reversible against that T18 control, preserving the separate
migration fix. No new worktree, Git commit or push was performed. Deployment was
authorized separately after implementation; no runtime source changed for it.

Read-only adversarial self-review (no delegated agent):

- **ACCEPTED/fixed:** source ordering initially let SCREEN-FIND execute before
  the new all-enemy check on the same pass; explicit admission gate now prevents it.
- **ACCEPTED/fixed:** alternate corridor search must explicitly focus the saved
  opponent; prior Scout cleanup restores a different focus. Generator now sets it.
- **ACCEPTED/fixed:** new release metadata must rebuild from filtered owned Scout
  IDs before releasing flags, so converted/reassigned Scouts cannot be affected.
- **ACCEPTED/fixed:** keep cancellation diagnostics observational; use live-state
  validation rather than diagnostic codes for enemy replan decisions.
- **REJECTED:** treating Scout loss as permission to sail to the failed beach;
  existing soft fallback is only used for a fresh, independently validated candidate.
- **DEFERRED to engine test:** navigability, real coastal geometry, hidden danger,
  actual unloading, scenario-specific safe alternatives and tactical effectiveness.
  The bounded candidate sampler is not a complete coastline/path planner. Memory
  currently covers preparation failures; dispatched voyage behavior is unchanged.

**PASS:**80 focused assault tests execute actual generated planner, corridor,
screening and fallback rules against object fixtures. They cover5/9/10 cargo,
expiry, same-beach exclusion, failure-count semantics, both Scout loss/damage
stages, replacement Scout, all-enemy danger veto, same-island alternatives,
objective and persistent opponent rotation, fixed deadlines, ownership loss,
and two active slots while a third is planned/committed. Original landing tests
were updated for five candidates, retaining zone/danger/bounded-recovery checks.
Existing unchanged admission behavior and all dispatched-slot rules retain their
previous gameplay fingerprints. Fixture geometry is NOT an engine simulation.

**PASS:** final full suite **378 tests**; PER structural/operand checks;
generator synchronization; ownership
audit762 sites/zero direct guard failures; strategy and naval validators;
38 historical replay benchmarks. String budget1434/1500; longest runtime physical
line215. One full-suite attempt hit sandbox permissions for historical temporary
compilation; the permission-approved writer tests passed17/17. Marker expectation
was updated from466 to467 before the final full-suite rerun.

**Fresh engine/replay result: NOT RUN.** Acceptance is same accepted load surviving
A's failure, exclusion of A until expiry, visible B/objective/opponent adaptation,
known-danger vetoes, bounded recovery if no plan, no slot interference, and actual
valid landings when a usable approach exists. Inspect all players, not just Red.

## Identity and scope

- Replay `SP Replay v101.103.48987.0 @2026.08.31 183134.aoe2record`:
  SHA256 `608B6681C240FC681E5C883A0CA9A138F3934FAE56DB40445B0AEDA45ECA5499`.
  Duration60:43; Red RESIGN60:42. No crash attribution.
- Public startup markers: **T17A1:465**, players2–8. Recorder self-marker
  asymmetry persists; do not claim a captured Red startup marker. Source and
  installed89-file runtime independently matched
  `B7BBA84A58914C4B8F650FCF183B5CAA79C1A4579DFE1F023E92B02A5AC08EC6`.
- Selected-color metadata, NOT slot/color inference: p1Red, p2Green, p3Yellow,
  p4Purple Roman Empire/team1; p5Orange Picts, p6Cyan Britons, p7Blue Germani,
  p8Gray Gauls/team2. Preserved lobby; no user/parser conflict.
- Exact decode:457,946 retained events, no decoder errors. All-player census:
  **53 boarding windows /18 command-linked hulls**. This is not an idle-hull
  census, simulation replay, or proof that every issued command executed.
- User observations: Red's drop-site far from resources, settlers recalled
  before constructing it, and all Red assault transports aborted. Corroborated
  below. The reported symptoms are not reduced to parser assumptions.

## Red migration: landing works, placement contract fails

Hull32067, stone anchor30546 at(175.5,136.5), saved land zone3:

| Game time | Evidence |
|---|---|
|54:50|Resource mission requests20 settlers.|
|55:21|Existing partial-load acceptance accepts14; six shore stragglers released.|
|55:21–56:07|Waypoint(153,74); progress distance41→16; waypoint reached.|
|56:07–56:47|Three unload requests near(175,136).|
|56:54|Runtime reports14 settlers landed, recovered zone3.|
|57:55|Mining Camp584 BUILD at(154,124), worker31250.|
|58:17|BUILD at(152,126), worker31391.|
|58:39|BUILD at(154,124), worker31327.|
|58:59|BUILD at(151,113), worker31391.|
|59:20|Drop-site failure;13 still-reserved settlers ordered to board32067.|
|60:05–60:36|Home-unload requests at(204,16). Actual return completion not proven at cutoff.|

**Root cause:** `rawai-military.per` ISSUE-DROPSITE uses `up-build place-point`.
That adds an expanding-region placement request; it does NOT promise a foundation
at the exact point. `sn-placement-zone-size` is not overridden in this runtime;
AIRef documents default20 and further expansion. The later WAIT-DROPSITE search
only accepts a same-zone camp within8 tiles of both the requested point and the
resource. Recorded BUILD points were approximately24.9,25.7,24.9,34.0 tiles from
the stone, so they cannot pass that check. The reserved builders are assigned
only after a matching foundation is found. Four expired attempts invoke the
existing explicit recall. This is not evidence of a competing STOP writer.

BUILD packets are concrete construction requests, not proof all four foundations
materialized. The user's visible distant foundation is independent evidence.
No resource-wait explains these four accepted requests; do not attribute the
failure to wood shortage or lower the foundation-verification requirement.

**Diagnostic correction:** ISSUE-DROPSITE used `up-get-point position-target`.
AIRef defines this as the nearest non-wall building of the current target enemy,
NOT the point set by `up-set-target-point` (that is `position-point`). The RAW12
coordinates162,137 /172,131 therefore do not identify these BUILD coordinates.
The previous test also modeled this API incorrectly. Historical T13 coordinate
telemetry cannot establish scratch-point overwrite. Persistent mission points
remain the correct source-lifetime safeguard, but that old runtime attribution
is withdrawn; see the correction in `T13-REPLAY-REVIEW.md`.

Primary API reference: [placement types](https://airef.github.io/parameters/parameters-details.html#PlacementType),
[build commands](https://airef.github.io/commands/commands-details.html#up-build-line).
Full definitions inspected in the cached official reference
`G:\Projects\Codex\Rome at War AI\.analysis\airef-reference-20260830.js`:
`cUpBuild`, `cUpCanBuildLine`, `cUpBuildLine`, `snPlacementZoneSize`, position enums.

## Red assaults: three accepted loads, three safety recalls

| Accepted | Hold | Code | Screen command reconstruction |
|---|---|---:|---|
|45:09|46:29|8|Scout36734: midpoint(143,72), beach(143,141), then home recall.|
|48:40|49:48|8|Scout36607: midpoint(140,67), beach(137,137), then home recall.|
|51:43|53:36|10|Scout36734: midpoint(140,67), repeated beach(137,137), last order53:21.|

`TRANSPORT-ROUTE-SCREEN-LANDING-THREAT` gives8 when the exact scout has
`object-data-under-attack >0`;10 when the exact ID cannot be resolved. The source
then enters SCREEN-RECALL and home recovery. All three accepted ten-person loads
used hull32067; none reached dispatched mission slots. They did not fail old
fallback401 or exhaust the three active slots.

Limits: attack status does not identify the attacker; missing exact ID alone does
not prove destruction. No captured enemy explicit order names these scout IDs in
those windows. Preserve that distinction instead of asserting hostile damage or
another controller's overwrite as established fact.

The second and third approaches repeat the same midpoint/beach. Source recovery
waits90s without recording rejected enemy/plan/approach information. Failure-aware
overseas target rotation remains an **unimplemented policy**, previously proposed
in T14. Public preparation events omit the saved enemy for these pre-dispatch
holds, so the exact opponent must not be invented from shoreline proximity.

No safety bypass implemented in this patch. Reasons8/10 cannot become unscreened
fallback triggers; the user's explicit requirement protects observed damage,
lost screens, defended routes and defended landings. A next scoped patch should
teach plan selection about distinct failed approaches, pin the alternative only
for preparation, and leave already-dispatched slots' saved enemies untouched.

## All-player transport outcomes

Normal acceptance below counts ready events; partial acceptance is separate.
23 accepted preparations =19 holds +4 dispatched slot commits. Two other loads
failed the useful partial-manifest minimum. HOLD labels are not all hard danger.

| Visible color | Hulls | Windows | Normal / partial accepted | Recorded holds | Slot commits |
|---|---:|---:|---:|---|---:|
|Red|2|8|3 /0|8×2;10×1|0|
|Green|3|5|0 /0|None|0|
|Yellow|1|1|0 /0|None|0|
|Purple|2|7|5 /1|1×5;8×1|0|
|Orange|1|3|0 /0|None|0|
|Cyan|2|10|5 /1|1×2;9×1;4×1|2|
|Blue|3|6|0 /0|None|0|
|Gray|4|13|8 /0|1×4;3×2; two additional underfill failures|2|

- Hold1 conflates defended and geometrically disconnected candidate beaches.
  Do not report all11 such cases as actual enemy fire. Holds3/9 can enter optional
  screening fallback. Three explicit fallback denials were **reason2 known danger**
  (Cyan50:47; Gray53:25/55:20); no401 rejection occurred.
- Cyan31773 committed55:19, screen-approach timeout fallback9, saved enemy3Yellow.
  Slot event2 at55:51 means hostile-fire recovery, NOT landing; return-empty56:31.
- Gray31816 committed57:27, Gray36303 committed57:49, both no-screen fallback3,
  both saved enemy3Yellow. **Two independent slots overlapped.**36303 issued
  clearance event11 at58:05, then no-progress59:25 and return-empty59:33.
  31816 no-progress/return-empty59:35.
- Cyan45090 committed58:24, fallback9 against3Yellow; no-progress60:08,
  recovery unresolved at cutoff. **Zero slot event8 confirmed assault landings.**
- All six available migration-terminal samples retain group10 (Orange outbound,
  Cyan outbound/two returns, Blue return, Gray return), versus the earlier T16
  unflagged cases. No RAW17 ownership-rejection/loss report found. That is positive
  sampled ownership evidence, not proof all movement succeeds.
- Smaller scouting/relic/native trips and repeated home-unloads were also checked:
  Green31679/32990/31766; Yellow31728; Orange31678; Blue31734/33063/32821;
  Gray31873; Cyan31773; Red31953/32067. Remote unload requests occur in several
  of these, but without cargo/arrival confirmation they remain **unresolved**,
  not autonomous assault victories. Red's14-settler landing is separately logged.
- STOP706 remains open: total69,741 (Red5,776; Green574; Yellow406; Purple1,026;
  Orange58,862; Cyan2,053; Blue639; Gray405). These counts alone do not attribute
  a writer or establish a rate-regression against a different match. No unrelated
  STOP experiment is combined with this migration patch.

## Narrow patch and validation

Local **T18:466**, not deployed in this audit:

- `rawai-military.per`: matching `up-can-build-line` and same-point
  `up-build-line` for the migration Mining Camp, Lumber Camp and Mill only.
  Invalid points advance the existing four offsets; no expanding native queue.
  Retain `up-can-build 0` as an additional gate to protect resource/escrow policy,
  plus owner, pending-placement, type, resource, zone and foundation checks.
  Copy diagnostic coordinates directly from persistent `gl-migration-build-x/y`.
- `tools/test_migration_foundation.py`: correct position-target semantics;
  fixture models native placement drift instead of assuming exact placement.
  Test actual new rules, four blocked offsets, delayed affordability, owner and
  duplicate-job blocking, correct foundation acceptance, and wrong/far rejection.
- Marker/assertion and ownership inventory synchronized. No assault, production,
  trade, defense, market, exploration or target-selection policy changed.
- **PASS:**11 focused tests,357 full regression tests, PER validation, assault
  generator synchronization, strategy execution, naval doctrine, ownership guard
  audit758 sites. Three regression cases **FAIL as expected** against untouched
  archived T17A1 source under the corrected API fixture. This is model-based
  discrimination, not an engine re-run. Benchmark validation recorded in HANDOFF.
- Read-only adversarial review: ACCEPTED native queue/exact-verifier mismatch,
  incorrect telemetry enum, preservation of escrow and bounded generic-failure
  recovery. REJECTED accepting distant foundations, removing recall bounds,
  claiming every screen was killed, or weakening hard danger. DEFERRED to fresh
  engine validation: exact foundation placement, builder execution, terrain and
  hostile-fire behavior of the exact-point API; inherited native placement
  heuristics must not be assumed identical. No blanket gameplay closure.

### Defect state / next actions

1. **Migration placement — FIXED-PENDING-RUNTIME.** Direct symptom/evidence/cause
   above; no contradictory foundation within the accepted radius found. Changed
   only the placement contract and its diagnostic/tests. Acceptance: appropriate
   same-island foundation within8 of the live resource, reserved settlers actually
   build it, then gather/drop off; no premature recall. Preserve useful partial
   loads, bounded genuine failure, escrow and no build in invalid/unsafe terrain.
   Latest result: source/model PASS; fresh engine result **NOT RUN**. Next: test
   exact-point placement and construction; do not infer completion from BUILD.
2. **Red assault participation — INVESTIGATING.** Direct symptom/evidence and
   exact predicates above. Repeated-plan selection is source-visible, but no
   proof a safe alternative was available in this replay. Existing instrumentation
   identifies hull/reason; it does not identify the attacking object. No behavioral
   patch here. Acceptance: choose and complete a viable alternative plan while
   preserving hard danger and active-slot isolation. Next: scoped failure-aware
   plan-selection work using the documented three failures/~180s/~300s proposal,
   with distinct plan/mission outcomes, not rule-evaluation counters.
3. **T17 startup error — CLOSED for the reported symptom.** User confirmed game
   starts; this465 replay runs60:43 after token-identical formatting correction.
   Engine's exact physical-line limit is still not measured.
4. STOP flood, boarding-ship conversions, Gray Imperial prerequisites/Workshop
   fallback plan, trade congestion and prior ledger defects remain open. No
   diagnostic omission or topic change closes them.

## Reproduction and rollback

Development exception unchanged:
`G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-transport-only`,
branch `recovery/p3b44-transport-only`, HEAD
`387eccab36a3311ca90d9e39bea6d73013584a8b` plus intentional pending changes.

External evidence in `G:\Projects\Codex\Rome at War AI\.analysis`:
`p3b44t17-full.json`, `-command-stream.json`, `-exact.json`,
`-transport-audit.json/.txt`, `-task-ownership.json`, `-summary.json`,
`-dispatch.json`. Existing `audit_t16_dispatch.py` now accepts a prefix argument:
`audit_t16_dispatch.py p3b44t17`; default remains p3b44t16. No duplicate analyzer.
Byte/source-site attribution was not asserted from a mismatched writer-trace map.

Immutable pre-edit control `p3b44t17a1-runtime-control.zip`:89 files,
verified payload hash `B7BBA84A58914C4B8F650FCF183B5CAA79C1A4579DFE1F023E92B02A5AC08EC6`.
No new worktree, directory switch, commit, push or data-mod/replay upload.
T18 can be reverted independently by reversing only this turn's migration
placement/diagnostic/test hunks and marker, not the user's broader pending work.
