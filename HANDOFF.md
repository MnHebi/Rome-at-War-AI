# Rome at War AI handoff

## Workspace and Git identity

The single canonical development workspace remains:

`G:\Projects\Codex\Rome at War AI\.pr-work\Rome-at-War-AI`

- Git root: same path.
- Branch: `codex/replay-economy-build-order`.
- Recorded HEAD: `fbaaae134fb74e46ff0872d4747a3654c7b64d1c`.
- Pull request: <https://github.com/MnHebi/Rome-at-War-AI/pull/4>.
- Working-tree exception on 2026-08-29: `AGENTS.md` is the user's modified
  replacement project-rules file and matches the workspace-root copy. Preserve
  it; do not discard or silently normalize it.

This handoff belongs to the dedicated transport-development worktree:

`G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-transport-only`

- Git root: same transport path.
- Branch: `recovery/p3b44-transport-only`.
- Starting/base commit: exact P3B44
  `8ec870075d08fcac98bad55b4ff045bf7abbc42e`.
- Causal implementation commit: `94fceb4` (`Clear friendly transport departure
  congestion`).
- Project-rules synchronization commit: `bcd484f` (`Adopt evidence-first
  project rules`).
- Purpose: one transport-only patch for a loaded assault Transport obstructed
  at departure by friendly idle Transports.
- Status: experimental P3B44-derived development worktree. It does not replace
  the canonical workspace.
- Future ordinary development must use the canonical workspace. Continue this
  exact runtime experiment only in this transport worktree.

Other controls:

- `G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-attack-baseline`,
  branch `recovery/p3b44-attack-baseline`, exact commit `8ec8700`: immutable
  attack-capable control. Never edit, regenerate, or relabel it.
- `G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-friendly-fire-defense`,
  branch `recovery/p3b44-friendly-fire-defense`, HEAD `92b3cf9`: isolated
  P3B44D1 allied-friendly-fire diagnostic. It is preserved but is no longer the
  installed test runtime.
- `G:\Projects\Codex\Rome at War AI\Rome-at-War-AI-main` is an obsolete
  noncanonical extracted snapshot and must not be used.

## Installed runtime identity

- Marker: `RAWAI-P3B44T1:442`.
- Runtime files: 68.
- Source and installed target SHA-256:
  `9C5860AA19D40627A0FF170570484BFEA9C889B92D5E8554797273AC395DE97A`.
- Deployment check: no missing, different, or unexpected runtime files.
- Only `rawai-customconstants.per`, `rawai-init-goals.per`, and
  `rawai-military.per` differed from the previously installed P3B44D1
  diagnostic, and exactly those three files were replaced.

## Current objective and preserved behavior

Run a fresh preserved-lobby replay that places several empty friendly
Transports around a loaded assault Transport and proves that the mission hull
detects non-progress, orders eligible blockers away, makes measured progress,
leaves the embarkation area, and continues its original route.

P3B44 Gray/Blue combined attacks are the known-good behavior at regression
risk. This patch must preserve ordinary land attack dispatch, superiority,
timing, target selection, home defense, escalation, and every non-transport
attack owner. Do not backport P3B46-P3B50 attack changes into this branch.

## Defect ledger

### Friendly Transport departure congestion

- **Status:** FIXED-PENDING-RUNTIME.
- **User-visible symptom:** Purple had a loaded mission Transport that could not
  get underway because Purple's own idle Transports physically blocked it. The
  loaded hull remained stuck.
- **Direct evidence:** user visual observation in
  `SP Replay v101.103.48987.0 @2026.08.29 110101.aoe2record`.
- **Proven failure mechanism:** P3B44's
  `TRANSPORT-ROUTE-WAYPOINT-WAIT/CHECK` treated `distance > 8` as sufficient to
  reissue the identical waypoint every eight seconds. It had no previous/best
  distance, progress threshold, stall count, clearance attempts, or terminal
  bound. Both independent transport-clear entry rules require
  `TRANSPORT-ROUTE-IDLE`; they cannot run during an active route and are
  designed for stale partial loads or empty idle Port/Shipyard obstruction.
- **Contradictory/unknown evidence:** replay data does not expose hull collision
  geometry or arbitrary per-hull path progress. Runtime escape remains to be
  demonstrated visually and through the public telemetry.
- **Implementation:** P3B44T1 initializes best/current waypoint distance from
  the exact reserved hull, requires two tiles of improvement, resets the stall
  count on progress, and checks the saved embarkation point after three
  non-progress samples. Only a loaded hull still within twenty tiles of origin
  can enter congestion handling.
- **Blocker safety:** the active route can select at most three nearby own
  Transport Ships. It excludes the exact mission ID, quarantined ID, every
  loaded, attacked, non-idle, grouped, or different-water-zone hull. It does
  not start the independent transport-clear controller.
- **Movement proof:** blockers move to the exact position of another known own
  ship 28-200 tiles away in the same water zone. No arbitrary geometric water
  coordinate is invented. Issuance is logged as `blocker clearance ordered`;
  only measured mission-hull progress can log `departure resumed`.
- **Retry/failure:** after an eight-second clearance wait, a producer and its
  immediately following consumer reconstruct the exact mission hull in one
  rule sweep and reissue the unchanged waypoint. Two failed clearance attempts
  emit exactly one `departure congestion unresolved` reason and enter the
  existing loaded-lift recovery owner.
- **Acceptance criterion:** a loaded hull obstructed by friendly idle
  Transports logs the bounded stall and blocker count, one or more eligible
  blockers receive the clearance order, the exact hull's waypoint distance
  then decreases, it leaves origin, and the existing landing mission continues.
  No unsafe hull is displaced and P3B44 ordinary attacks remain effective.
- **Latest result:** all deterministic/static criteria PASS. Fresh runtime
  acceptance is still required, so the defect is not CLOSED.
- **Next action:** run the P3B44T1 congestion replay and attach it for analysis.

### Deliberately unchanged defects

This one-cause patch does not change or claim to fix:

- cliff-bound landing points or remote unloading failures;
- route-scouting, route-threat scanning, landing selection, or naval pathfinding;
- passenger policy, partial-assault departure, migration, or relic ferries;
- hostile-fire survival, enemy landing memory, Port placement, or transport
  production quantity;
- the separate allied-friendly-fire defense trigger;
- taunt 69 deletion, behind-cliff Shipyard construction, command flooding,
  Merchant Vessel growth, allied resource aid, Palintonon recovery, Market
  buying, Wonder construction, or cross-water allied relief;
- the unexplained heap-corruption crash, whose existing dumps show detection
  rather than the earlier corrupting writer.

## Replay evidence and artifacts

- Replay basename:
  `SP Replay v101.103.48987.0 @2026.08.29 110101.aoe2record`.
- SHA-256:
  `C1F85E836D59CBC2D77643D2608930DC3D7940C3ECFDC6081F0C08BBF833917F`.
- Duration: 58:51; the user manually resigned. This replay did not crash.
- Preserved lobby mapping: Red/Green/Yellow/Purple Roman Empire versus Orange
  Picts, Cyan Britons, Blue Germani, and Gray Gauls.
- External compact analysis:
  `G:\Projects\Codex\Rome at War AI\.analysis\replay-20260829-110101-p3b44-compact.json`.
- Repository evidence entry:
  `britain-4v4-20260829-110101-p3b44-transport-congestion` in
  `replay-benchmarks.json`.
- The prior immutable P3B44 deployment had 68 files and SHA-256
  `EE04DE7BFA1448E90D54E8AC592D0EEECF4E9DAD93100272D2941F0209B75846`.

Replay/savegame files, compact parser output, crash dumps, and Rome at War data
mod files remain external and must never be committed to the AI repository.

## Validation performed

- Moving normally: PASS.
- Stalled near origin: PASS.
- Ownership safety: PASS.
- Clearance success: PASS.
- Clearance failure: PASS.
- Focused suite: PASS (5 tests).
- Full P3B44-derived regression suite: PASS (115 tests).
- PER structural/operand validation: PASS.
- Naval-doctrine validation: PASS.
- Strategy execution: PASS (1,156 total matchups; 1,149 historical and 1,152
  Extreme matchups with adjustments).
- ODS workbook round trip: PASS (34 civilizations, 680 unit-evidence rows, 340
  naval-class rows).
- Replay benchmarks: PASS (21 entries).
- `git diff --check`: PASS; only expected CRLF notices.
- Adversarial baseline comparison: PASS. The only four original military rules
  changed are the transport-route screen-departure rule and three
  waypoint-check branches. All are scoped by `gl-transport-route-state`.
  `up-target-objects`, `up-retreat-now`, `up-reset-attack-now`, `attack-now`,
  and `up-find-player` counts are identical to immutable P3B44. The additional
  `up-target-point` and search resets belong only to the congestion state
  machine.
- Every new departure state has a producer and consumer. The terminal reason and
  blocker-clearance order each occur once in source, and all retry paths are
  bounded by two clearance attempts.
- `validate_good_units.py` has a pre-existing P3B44 provenance-hash failure;
  frozen unit-strategy material is outside this transport patch.
- Installed runtime byte verification: PASS.
- Fresh engine/replay acceptance: REQUIRED.

## Exact next actions

1. Verify this worktree's branch, HEAD, and clean state against this document.
2. Start the preserved Britannia 4v4 lobby and confirm public marker
   `RAWAI-P3B44T1` appears near startup.
3. Cluster several empty idle friendly Transports around an embarkation area and
   allow one assault Transport to load behind or among them.
4. Preserve the sequence `transport departure stalled`, `transport blockers
   found`, `transport blocker clearance ordered`, and `transport departure
   resumed` or the single bounded unresolved terminal.
5. Visually confirm that selected blockers are empty/idle, the loaded hull
   actually leaves, and its original assault continues. Confirm Gray/Blue
   ordinary combined attacks remain comparable to P3B44.
6. Attach the replay. Analyze exact IDs, distances, counts, order cadence, and
   final mission outcome. Mark the defect CLOSED only after runtime PASS.
7. Do not continue into another transport defect in this branch after this
   congestion result; port only the proven causal fix as a separate canonical
   change when appropriate.
