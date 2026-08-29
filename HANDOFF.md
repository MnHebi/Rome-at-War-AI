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
- Landing-clearance implementation commit: `f6ac4fb` (`Clear friendly Scouts
  from transport landings`). This is the current code HEAD before this handoff
  documentation commit.
- Project-rules synchronization commit: `bcd484f` (`Adopt evidence-first
  project rules`).
- Purpose: P3B44-derived transport-only development. P3B44T1 addresses loaded
  departure obstruction by friendly idle Transports; P3B44T2 addresses the
  separately proven final-landing obstruction by route-screen and escort
  Scouts discovered in the T1 runtime replay.
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

- Marker: `RAWAI-P3B44T2:443`.
- Runtime files: 68.
- Source and installed target SHA-256:
  `748790B54F55893D7150B7272B67F6323AEB507EA92BEE16AFA28A560171B133`.
- Deployment check: no missing, different, or unexpected runtime files.
- Relative to installed P3B44T1, only `rawai-init-goals.per` and
  `rawai-military.per` differed, and exactly those two files were replaced.

## Current objective and preserved behavior

Run a fresh preserved-lobby P3B44T2 replay that proves the exact route-screen
Scout leaves the selected landing, the active escort stays clear during the
unload window, passengers land before timeout, and the assault continues. If
possible, also exercise P3B44T1's still-pending departure-congestion case by
placing empty friendly Transports around a loaded mission hull.

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
- **Latest runtime result:** the 12:27 P3B44T1 replay did not exercise this
  departure-stall case. Transport 32174 made normal waypoint progress, so no
  `RAW44T` departure event fired. The original acceptance remains pending.
- **Next action:** retain the P3B44T1 congestion acceptance in the P3B44T2 test
  when a suitable departure obstruction occurs.

### Friendly Scout obstruction at attack-Transport landing

- **Status:** FIXED-PENDING-RUNTIME.
- **User-visible symptom:** near the end of the P3B44T1 replay, Purple's loaded
  Transport aborted instead of having a friendly Scout Ship move out of the
  way.
- **Direct evidence:** user visual observation plus decoded actions from
  `SP Replay v101.103.48987.0 @2026.08.29 122745.aoe2record`.
- **Root cause:** Purple Scout 32389 guarded the future route hull, then the
  route-screen owner ordered it to waypoint 28,182 at 49:24/49:54 and landing
  72,185 at 50:10. The success branch released its group and erased its exact
  ID without issuing another order, leaving it stationary on the landing.
  Purple Transport 32174 reached waypoint 28,182, issued its unload at that
  exact landing at 51:29, remained loaded, and was recalled home at 52:15 by
  the fixed forty-five-second landing timeout. A second Scout, 32970, also
  received guard orders on Transport 32174 every twenty seconds during the
  approach/window. No P3B44T1 departure-stall event fired because departure
  progress was normal.
- **Implementation:** P3B44T2 moves the exact route-screen Scout eighteen tiles
  to one side of the screened approach before releasing `transport-screen-group`.
  Immediately before unload, it moves the already-owned transport escort group
  eighteen tiles to the opposite side while retaining that ownership. The
  periodic escort selector cannot reissue guard during
  `TRANSPORT-ROUTE-RETURN-WAIT` and resumes immediately after the landing owner
  exits that state.
- **Instrumentation:** public bounded events identify the exact cleared screen
  Scout, staged landing route, completed landing, or terminal timeout.
- **Acceptance criterion:** `RAW44T2 route-screen landing cleared` is followed
  by visible screen-Scout clearance; `RAW44T2 transport landing escort staged`
  occurs once; no guard is reissued to that loaded hull during the unload
  window; passengers disembark; `RAW44T2 transport landing completed` occurs
  before forty-five seconds; and no timeout occurs for that mission. Ordinary
  P3B44 attack behavior remains unchanged.
- **Latest result:** replay causality, focused deterministic validation, full
  regression validation, deployment, and byte verification PASS. Fresh engine
  acceptance is required, so this defect is not CLOSED.
- **Next action:** run the preserved lobby with P3B44T2 and attach the replay.

### Deliberately unchanged defects

This one-cause patch does not change or claim to fix:

- cliff-bound or otherwise unreachable landing points unrelated to friendly
  Scout obstruction;
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

P3B44T1 final-landing replay:

- Basename:
  `SP Replay v101.103.48987.0 @2026.08.29 122745.aoe2record`.
- SHA-256:
  `D891771AA04A4EA626A42B9F5353C495314E033FC00D312DECDB413C397B82D2`.
- Duration: 54:03; Red manually resigned. The replay parsed cleanly and
  contained the P3B44T1 marker from players 2 through 8.
- Preserved lobby mapping: Red/Green/Yellow/Purple Roman Empire versus Orange
  Picts, Cyan Britons, Blue Germani, and Gray Gauls.
- External compact analysis:
  `G:\Projects\Codex\Rome at War AI\.analysis\replay-20260829-122745-p3b44t1-compact.json`.
- Repository evidence entry:
  `britain-4v4-20260829-122745-p3b44t1-landing-escort` in
  `replay-benchmarks.json`.

Replay/savegame files, compact parser output, crash dumps, and Rome at War data
mod files remain external and must never be committed to the AI repository.

## Validation performed

- Moving normally: PASS.
- Stalled near origin: PASS.
- Ownership safety: PASS.
- Clearance success: PASS.
- Clearance failure: PASS.
- Landing screen/escort clearance and refresh gate: PASS.
- Full P3B44-derived regression suite: PASS (116 tests).
- PER structural/operand validation: PASS.
- Naval-doctrine validation: PASS.
- Strategy execution: PASS (1,156 total matchups; 1,149 historical and 1,152
  Extreme matchups with adjustments).
- ODS workbook round trip: PASS (34 civilizations, 680 unit-evidence rows, 340
  naval-class rows).
- Replay benchmarks: PASS (22 entries).
- `git diff --check`: PASS; only expected CRLF notices.
- Adversarial P3B44T1 comparison: PASS. P3B44T2 changes only the transport
  escort selector, safe route-screen landing-success rule, and successful
  waypoint-to-unload rule, plus bounded terminal telemetry. All behavior is
  scoped to transport escort or `gl-transport-route-state`.
  `up-target-objects`, `up-retreat-now`, `up-reset-attack-now`, `attack-now`,
  and `up-find-player` counts are identical to P3B44T1. The added move orders
  target only the exact screen group and the already-owned escort group.
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
   `RAWAI-P3B44T2: 443` appears near startup.
3. Observe an attack lift through its route screen and landing. Preserve the
   `route-screen landing cleared`, `transport landing escort staged`, and
   `transport landing completed` or `transport landing timed out` records.
4. Visually confirm that the screen Scout leaves the landing before the loaded
   hull arrives, the active escort stays to the other side instead of guarding
   onto the hull, passengers actually disembark, and landed troops continue
   their attack.
5. If empty friendly Transports obstruct departure, also preserve the P3B44T1
   `departure stalled` -> blocker count -> clearance ordered -> `departure
   resumed` sequence or the single bounded unresolved terminal.
6. Confirm Gray/Blue ordinary combined attacks remain comparable to immutable
   P3B44, attach the replay, and analyze exact IDs, orders, event cadence, and
   mission outcome. Close only the runtime criteria that actually PASS.
7. Keep the separate P3B44D1 friendly-fire failure and all non-transport
   defects out of this causal patch/worktree.
