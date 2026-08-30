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
- Current canonical status observed before the P3B44T4 transport session:
  `AGENTS.md` and `HANDOFF.md` are modified and
  `tools/clean_smx_magenta.py` / `tools/test_smx_magenta.py` are untracked.
  Those are concurrent DeepSeek/user changes; do not alter or absorb them from
  this experimental worktree.

This handoff belongs to the dedicated transport-development worktree:

`G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-transport-only`

- Git root: same transport path.
- Branch: `recovery/p3b44-transport-only`.
- Starting/base commit: exact P3B44
  `8ec870075d08fcac98bad55b4ff045bf7abbc42e`.
- Initial departure implementation commit: `94fceb4` (`Clear friendly
  transport departure congestion`).
- Landing-clearance implementation commit: `f6ac4fb` (`Clear friendly Scouts
  from transport landings`).
- Verified exact-blocker implementation commit: `3ee2002` (`Verify transport
  blockers before departure retry`). This is the runtime-validated P3B44T3
  implementation.
- Exact-passenger implementation commit: `19c0beb` (`Verify relic ferry
  passenger before departure`). P3B44T4 runtime-closed that defect in the
  21:43 replay.
- Same-zone migration landing implementation: `2a08a2b` (`Screen migration
  landing candidates by zone`). This is the deployed P3B44T5 behavior commit.
- Safe partial assault / passenger diagnostics implementation: `14fd09c`
  (`Depart with safe partial attack lifts`). This is the deployed P3B44T6
  behavior commit and the recorded experimental HEAD before this handoff-only
  documentation successor.
- P3B44T6 evidence handoff: `f25f5bd` (starting HEAD for the T6 replay audit).
- Migrant reservation implementation: `9d0c87b` (`Preserve migrant reservation
  through villager cleanup`). T7 runtime validates the specific flag exclusion.
- T7 audit starting HEAD: `e17a4edf74919cdf85bab360610612aa216de612`.
- Salvage D/offline analyzer: `9b3dded` (`Backport replay retreat analysis
  tooling`). No runtime changes or marker-specific analyzer dependency.
- Current runtime/diagnostic commit: `d10f33e` (`Trace competing recall callers
  during transport boarding`), P3B44T8. Its evidence/handoff successor is
  `16213f8b06da9d791fca527ec18d6fb6b7fcac86`, the starting HEAD for the
  architectural ownership investigation.
- Architectural audit commit: `e86ab8035a9abacb2ff7b632bebf2afe6802db4e`
  (`Audit task ownership across all T7 players`). Audit tooling, tests and
  evidence only; no runtime changes. Its documentation-only successor records
  this handoff. Resolve exact checkout HEAD with `git rev-parse HEAD`.
- The user explicitly authorized committing the intentional investigation-
  breadth amendment in `AGENTS.md` on 2026-08-30. It is included in this branch
  and PR #5; do not continue treating it as an expected uncommitted exception.
  Its content matches the workspace-root rules. The canonical checkout is
  unchanged by this rules-only publication.
- Project-rules synchronization commit: `bcd484f` (`Adopt evidence-first
  project rules`).
- Purpose: P3B44-derived transport-only development. P3B44T1 introduced loaded
  departure congestion handling; P3B44T2 fixed final-landing obstruction by
  route-screen and escort Scouts; P3B44T3 corrected T1's replay-proven
  group-and-assume blocker clearance by moving and verifying one exact safe
  blocker at a time; P3B44T4 directly verifies the reserved relic-ferry
  passenger after P3B44T3 proved two load-recognition failures; P3B44T5
  replaces migration's replay-proven water/wrong-island diagonal candidates
  with close, same-zone, exact-hull-path-screened candidates. The 23:25
  P3B44T5 replay runtime-closed that exact landing-candidate defect.
  P3B44T6 addresses the separately proven exact-full assault abort while
  preserving the unknown upstream passenger failure for discriminating
  telemetry: useful five-to-nine-soldier hulls depart through the unchanged
  screened route, and assault/migration boarding publish bounded exact
  candidate command state before the first retry and at a terminal.
- Status: experimental P3B44-derived development worktree. It does not replace
  the canonical workspace.
- Future ordinary development must use the canonical workspace. Continue this
  exact runtime experiment only in this transport worktree.
- T6 audit scope exception: P3B44T7 touches `rawai-general.per` only to exclude
  transport-reserved passengers from the proven generic-cleanup flag mutation.
  This is a demonstrated dependency of transport ownership, not a general
  economy redesign. No military controller or other behavior was changed.
- T7 audit scope exception: T8 adds event-bound diagnostics to military/taunt
  recall callers only. It does not change their conditions, commands, action
  ordering, searches or ownership. No new worktree was created or canonical
  directory switched in this session.
- Architectural scope exception, 2026-08-30: the user's TASK OWNERSHIP /
  PREEMPTION directive supersedes the earlier prohibition on ownership/recall
  changes in this worktree. It authorizes a shared task contract, explicit
  emergency transfer, bounded routine defense and persistent original-TC
  allied-help anchors, while forbidding concurrent transport micro-fixes.
  See `TASK-OWNERSHIP.md` for the complete requirements and evidence state.
  No runtime changes were made under this new directive yet.

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

- Marker: `RAWAI-P3B44T8:449`.
- Runtime files: 68.
- Source and installed target SHA-256:
  `0166808361591E65F29FA4B0770DB90A1C68D1F4A200F220C28C76F13A6D2F92`.
- Deployment check: all 68 runtime files are byte-identical, with no missing,
  different, or unexpected runtime files. Relative to T7, exactly
  `rawai-military.per`, `rawai-tauntcommands.per` and `rawai-init-goals.per`
  were copied from this worktree by `tools/sync_test_ai.py --apply`.
- Installed directory:
  `C:\Users\LostSoul\Games\Age of Empires 2 DE\76561198053747760\mods\local\Rome at War AI\resources\_common\ai`.
- Before editing, the full T7 source/deployment hash was verified as
  `69C30C50661D3E1E8A1F8DC081C63E80D0C899D8E695B16D3E02F95B910B7738`.
  T8 is diagnostic only; it has no fresh-match behavioral acceptance yet.

## Current objective and preserved behavior

P3B44T6 runtime-closes the exact-full assault abort: five useful partial loads
completed enemy-shore landings with exact passenger membership, while below-five
loads retained abort behavior. P3B44T5 landing-candidate screening also remains
CLOSED. The broader queued-passenger defect remains INVESTIGATING, with several
distinct observed failure classes rather than one universal explanation.

P3B44T7 runtime-validates the specific mining-passenger reservation exclusion:
generic villager cleanup was overwriting group 4 with temporary group 0 and
clearing it. All twelve T6 mining-passenger snapshots showed unassigned flag
-2; all 39 identified T7 mining snapshots retain flag 4. This closes only the
specific flag mutation, not exclusive command ownership or successful migration.

The immediate objective is now the user's architectural task ownership /
threat-preemption recovery directive, recorded repository-locally in
`TASK-OWNERSHIP.md`. Completion state is **ROOT CAUSE NOT FULLY PROVEN —
OWNERSHIP TELEMETRY REQUIRED**. The audit covers all 378 recorded loads and
202 retreats, with 132 boarding windows and exact command-stream ordering.
It identifies 83 pre-boarding conflicts with task-owner evidence, including
67 WORK packets, but does not establish every producing script/native writer,
continuous ownership at the instant of overwrite, or a verified per-unit
native economy lock. See the report for successes and unresolved outcomes;
83 is not a count of failed missions.

T8 labels the six existing global-recall callers. It does not trace all worker
writers, acquire/release/preemption boundaries, or native task delegation.
No shared selection contract, emergency-transfer patch, routine-recall
replacement or persistent allied-home anchor has been implemented. The
section-H gameplay contract tests and fresh architectural runtime acceptance
are also pending. Do not mistake the new audit-tool tests for those tests.

Purple's proven drop-site race remains open for its own patch. Salvage A-C and
Port placement remain authorized but are held outside this diagnostic runtime
to avoid mixing changes into caller attribution. They are not canceled or
user-deferred. Salvage D was useful to the audit and is already implemented.

P3B44 Gray/Blue combined attacks and the successful T1-T5 transport outcomes
are the known-good behavior at regression risk. Preserve ordinary attack
dispatch and effective genuine defense while replacing only ownership-
violating acquisition/preemption. The new directive explicitly allows changing
routine global recalls; preserving those exact calls is not an acceptance
requirement. Do not backport P3B46-P3B50 attack redesigns into this branch.

## Authorized post-T7 work (2026-08-30)

The user authorized proceeding with SAFE POST-P3B44 SALVAGE INTEGRATION once
the P3B44T7 replay is supplied, and also authorized the previously requested
dock strategic-number work. This expands the permitted work in this recovery
worktree after T7; it does not replace the canonical workspace. The T7 replay
has now been audited across all players. Starting/pre-salvage HEAD is
`e17a4edf74919cdf85bab360610612aa216de612`. D is implemented in `9b3dded`;
A-C and Port behavior are pending, with no claim of runtime validation. The
user was informed that these runtime changes are held outside T8's isolated
caller-attribution experiment, prioritizing the repeated boarding defect.

1. Audit T7 across all reasonably reconstructable transport events and players,
   verify runtime identity, and evaluate reservation survival plus complete
   mission outcomes. If a regression appears, follow the regression-first
   rules before adding features. Record the accepted pre-salvage HEAD.
2. Manually backport the corrected aid tiers from
   `81ce73d22438750adb0ce77f6c13bbec90b7ca63` plus the relevant compiler fix in
   `90287ea6106dace6fe043309ad5b73e3773f3831`. Stockpile below 100 gates requests;
   lifetime collected totals select 100 / 500 / 1000 at bank thresholds 500
   and 1000. Preserve independent 120-second resource deadlines, the ten-second
   global minimum gap, donor reserves, recipient identification, and immediate
   acknowledgment of unaffordable requests. Use `gl-self-player-number`
   comparisons for every donor self-exclusion and port the validator rejecting
   direct `(player-number != N)` predicates.
3. Extract only the six independent Imperial Market purchases and standalone
   Wonder controller from `0e1169f54a3d06fe1cd6c1f76e32714e3e835ec7`, adding the
   two Wonder purchases/sale guards only with that controller. Retain source
   price/resource bounds and one shared 15-second portfolio deadline. Exclude
   the transport-wood rule and any added `gl-land-target-needs-transport`
   dependency. Existing recovery relocation-Market rules remain unchanged.
   Wonder must be late-Imperial/Standard-victory gated, require three five-minute
   no-progress windows accounting for both teams, reset for meaningful losses,
   stagger allied candidates, yield to an allied Wonder, retain the 60-villager
   threshold and resource reserves, and bound retries with cooldown. It may
   read home-defense state but must not write protected controller state.
   Source inspection found a missing Standard-victory gate, negative baseline
   sentinel reuse with one/two enemy buildings, and net-count sampling that can
   mask losses. Resolve these isolated Wonder gaps and strengthen lifecycle
   tests; do not copy the source blindly or import later military dependencies.
4. Port only offline DE_RETREAT retention, `retreat_actions`, generic compact
   chat categories, and independent analyzer tests from
   `91ea476f779f41c2cde858f7cca1cd3c06fbcd59`. No RAW49 runtime instrumentation.
5. Then investigate and implement the Port-placement work in its own causal
   patch, using the three requested controls and acceptance criteria below.
   Do not fold it into the salvage commits or alter protected transport logic.

Never cherry-pick the source commits wholesale. Preserve ordinary attacking,
timers, superiority, target selection, ownership/recall, home defense,
escalation, siege, and every recovery transport selection/loading/routing/
ownership/screening/recovery/readiness/landing/clearance rule, including T7's
general-cleanup exclusion. Stop a conflicting backport rather than importing
P3B46-P3B50 military/transport behavior. Keep the baseline immutable.

Historical salvage goal IDs collide with current transport goals. The original
selected features need 27 new goals; 1163 onward was free at scoping HEAD
`e17a4edf74919cdf85bab360610612aa216de612`. Recheck and allocate fresh IDs;
Wonder corrections may need additional state. Prefer three separable salvage
commits: corrected aid; independent Market/Wonder; offline analyzer. Port work
is separate. Expected salvage runtime files are customconstants, init-goals,
trade, and homebase only. Run focused tests, structural/domain validators,
relevant synchronization checks, the full recovery regression suite, adversarial
review and a complete protected-symbol/semantic diff audit against the recorded
pre-salvage HEAD. Use a unique recovery marker and verified runtime hash, update
this handoff, and require fresh replay acceptance; static success is not runtime
closure. Do not import historical markers or later handoffs wholesale.

## Defect ledger

### Friendly Transport departure congestion

- **Status:** CLOSED.
- **User-visible symptom:** Purple had a loaded mission Transport that could not
  get underway because Purple's own idle Transports physically blocked it. The
  loaded hull remained stuck.
- **Direct evidence:** user visual observation in the 11:01 P3B44 replay, plus
  two systematic Green failures in the 13:10 P3B44T2 replay.
- **Initial proven failure mechanism:** P3B44's
  `TRANSPORT-ROUTE-WAYPOINT-WAIT/CHECK` treated `distance > 8` as sufficient to
  reissue the identical waypoint every eight seconds. It had no previous/best
  distance, progress threshold, stall count, clearance attempts, or terminal
  bound. Both independent transport-clear entry rules require
  `TRANSPORT-ROUTE-IDLE`; they cannot run during an active route and are
  designed for stale partial loads or empty idle Port/Shipyard obstruction.
- **P3B44T2 runtime result:** Green hulls 58807 and 30210 each stalled 49/52
  tiles from their waypoint with garrisoned passengers and three blockers. At
  94:39, 100:14, and 100:49 the runtime selected the same blocker IDs 30476,
  53715, and 57617 and moved all three as one group to one staging point. Both
  loaded hulls made no progress and emitted `departure congestion unresolved`.
  The identical blocker set surviving into the later mission proves command
  issuance was incorrectly treated as clearance.
- **P3B44T1 implementation:** initializes best/current waypoint distance from
  the exact reserved hull, requires two tiles of improvement, resets the stall
  count on progress, and checks the saved embarkation point after three
  non-progress samples. Only a loaded hull still within twenty tiles of origin
  can enter congestion handling.
- **P3B44T3 implementation:** select only the nearest exact eligible blocker,
  save its object ID, move it, reconstruct that same ID after eight seconds,
  and require its distance from the saved mission-hull point to exceed twelve
  tiles before logging `blocker cleared`. One retry is allowed only while the
  hull remains empty, unattacked, ungrouped, and unquarantined. A hull that
  remains blocked or becomes unsafe is excluded while another exact blocker is
  tried. Three selections are the hard bound before the existing terminal
  recovery path.
- **Safety:** initial scans continue to exclude the mission hull, quarantine,
  loaded, attacked, non-idle, grouped, and different-water-zone ships. The
  adversarial review added the same mutable safety protection to the delayed
  exact-ID retry so a newly claimed hull cannot be retasked.
- **Acceptance criterion:** a loaded hull obstructed by friendly idle
  Transports logs an exact blocker order followed by `blocker cleared` only
  after measured separation; the loaded hull then logs `departure resumed`,
  leaves origin, and continues the existing mission. Unsafe hulls are skipped,
  failures remain bounded, and ordinary P3B44 attacks remain effective.
- **Latest runtime result:** in the 15:12 P3B44T3 replay, Blue loaded hull
  31205 reported departure congestion at 44:26. Exact blocker 37204 received
  one move and one bounded retry, then emitted `blocker cleared` at 44:42; the
  source can emit that event only after the exact blocker exceeds twelve tiles
  from the mission hull. Hull 31205 resumed at 44:51, issued its remote unload
  at 45:08, completed the landing at 45:47, and withdrew home. This directly
  satisfies the scoped runtime criterion.
- **Non-regression result:** the same mission's route-screen Scout moved aside,
  no guard targeted the hull during its 45:08-45:47 unload window, and the
  landing completed. P3B44T2 remained intact.
- **Closure basis:** exact runtime blocker separation, loaded-hull resumption,
  and completed landing are all replay-visible. P3B44T4 does not alter any T3
  departure rule.

### Relic-ferry passenger load recognition

- **Status:** CLOSED.
- **User-visible symptom:** Red loaded a Priest into a Transport, the hull did
  nothing, the controller later unloaded the Priest at home, and the Priest
  retrieved a relic from Red's own island instead of completing the intended
  ferry mission.
- **Direct evidence:** exact Priest 31572 was ordered aboard hull 31206 at
  19:23 in the P3B44T3 replay. No outbound hull order followed; exactly 180
  seconds later the relic watchdog issued a home unload at 22:23. After another
  home unload at 24:25, the same Priest received an ordinary order to own-island
  relic 31456 at 25:11. The defect repeated with hull 33537: boarding at 31:11,
  no outbound order, and exact watchdog home unload at 34:11.
- **Root cause boundary:** the earliest repeated divergence is the load check,
  before sailing, pathing, landing, or relic tasking. P3B44T3 checked readiness
  indirectly through the reserved hull's `object-data-garrison-count` and had
  no CHECK-LOAD branch when the exact hull search target was absent. The replay
  proves that this recognition path failed twice; it cannot distinguish an
  absent hull result from an unobserved/stale count.
- **Engine constraint:** DE direct-unit searches exclude garrisoned units by
  default. P3B44T4 uses `fe-filter-garrisoned c: 1` before rebuilding the exact
  stored passenger ID so the lookup remains valid across boarding. Provenance:
  official AoE II DE Update 111772 scripting notes,
  <https://www.ageofempires.com/news/age-of-empires-ii-definitive-edition-update-111772/>.
- **Implementation:** commit `19c0beb` changes only the relic-ferry LOADING and
  CHECK-LOAD transition. It verifies the exact reserved Priest/Brahmin's
  `object-data-garrisoned == 1`, then rebuilds the unchanged reserved hull and
  issues the existing target/home unload. The existing 180-second watchdog and
  hull group reservation remain. One pending-or-missing event per boarding
  attempt and exact outbound/return unit/hull records provide bounded evidence.
- **Regression risk:** T3 attack-Transport departure and T2 landing-screen /
  escort behavior. No corresponding rules were changed; the existing focused
  tests remain and must be reconfirmed in the fresh replay.
- **Acceptance criterion:** exact boarding is followed by `RAW44R relic ferry
  outbound unit/hull/target` and the same hull's remote unload before the
  180-second watchdog. The carrier acquires the off-home relic, emits exact
  return unit/hull records, unloads at home, and receives the unchanged home
  Monastery task. Pending/missing logging remains one-shot.
- **Latest runtime result:** the 21:43 P3B44T4 replay contains two independent
  complete round trips. Orange carrier 33139 used exact hull 31942 to visit
  relic 4656 and returned to Monastery 33023; Cyan carrier 34011 used exact
  hull 33693 to visit relic 4662 and returned to Monastery 33653. Red carrier
  33314 and Green carrier 33487 independently advanced from boarding to exact
  outbound hull/target commands before the watchdog, although neither return
  completed before later mission outcomes.
- **Non-regression result:** five assault unload windows in the same replay had
  zero GUARD commands on the active landing hull. Two completed and three reached
  the unchanged bounded timeout.
- **Closure basis:** exact garrison recognition, outbound identity, remote
  unload, relic acquisition, same-hull return, home unload, and exact Monastery
  task are replay-visible for two independent players.

### Friendly Scout obstruction at attack-Transport landing

- **Status:** CLOSED.
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
- **Latest runtime result:** the systematic P3B44T2 audit found eighteen
  landing-screen events across all players and an exact same-timestamp Scout
  move for every event. Fifteen missions reached unload windows and none had a
  guard action targeting the active hull during that window. Both Purple
  missions completed at 62:59 and 88:41. This directly satisfies the scoped
  screen/escort acceptance criterion.
- **Closure basis:** runtime replay evidence demonstrates exact screen-Scout
  clearance, guard suppression, and completed landings. The nine other
  timeouts are a distinct repeated-landing-selection defect with zero
  unload-window guard actions.

### Queued passenger blocks Transport route start

- **Status:** CLOSED for the exact-full assault route gate (T6 runtime PASS);
  INVESTIGATING for the upstream reason an individual queued passenger does
  not board.
- **User-visible symptom:** several queued units remained outside their
  Transport. Manually loading the assumed passengers caused the hull to enter
  its route.
- **Direct replay evidence:** the systematic P3B44T5 boarding audit found 48
  detailed Red scripted episodes: 31 full/ready, 13 aborts, 3 partial, and 1
  unresolved. At 51:14, 55:04, 57:38, and 59:46 ten-passenger assault
  manifests shrank to a one-passenger retry list and still reached the
  exact-full abort. Passenger 39672 was the sole serialized retry candidate in
  the latter three episodes. At 281:51, a separate migration load record
  uniquely included exact hull 31558 in its selected objects, identifying a
  human load action; `migration depart full: 11` followed at 282:05 and the
  hull immediately received route movement. This independently corroborates
  the user's direct observation.
- **Proven downstream root cause:** the assault loader required the exact
  selected count at the thirty-second terminal. Any one nonboarding passenger
  therefore discarded the useful loaded remainder. Simply lowering the count
  was unsafe because the original `attack-boarding-group` still contained
  shore stragglers that would later receive the remote landing order.
- **Unknown upstream cause:** passenger 39672 has repeated replay-visible
  SPECIAL garrison commands to hull 31558 and no serialized ORDER, AI_ORDER,
  WORK, GUARD, or PATROL command that visibly transferred it to another owner
  in the bounded 55-to-60-minute audit. The replay does not expose whether
  shoreline geometry, internal/unserialized command replacement, object state,
  or an engine loading failure stopped it. Preserve this uncertainty.
- **Instrumentation:** P3B44T6 publishes one bounded candidate before the first
  assault or migration retry and another at a partial/abort terminal. Each
  sample includes exact object ID, action, target ID, order, command ID,
  distance from the stored embarkation origin (not a moving hull's current
  position), land zone, controller group flag,
  move coordinates, and idling state. A land-to-water path query was
  deliberately rejected because it cannot distinguish shoreline boarding
  reachability.
- **Implementation:** commit `14fd09c` retains the ten-passenger maximum and
  thirty-second assault window. With five through nine exact garrisoned
  soldiers, it stops every shore straggler, reconstructs
  `attack-boarding-group` from garrisoned members only, updates the target to
  actual occupancy, and continues through unchanged target revalidation,
  route screening, and landing. Fewer than five retains the existing bounded
  unload/recovery abort. Migration receives diagnostics only; its full,
  partial, and abort thresholds are unchanged.
- **Regression risk / control:** full assault lifts, low-strength abort,
  home-defense interrupt, target invalidation, P3B44T2 final-landing Scout
  clearance, P3B44T3 exact departure-blocker verification, P3B44T4 relic
  ferries, P3B44T5 same-zone migration landings, and Gray/Blue ordinary attack
  behavior.
- **Acceptance criterion:** the fresh replay contains marker
  `RAWAI-P3B44T6:447` and exact installed hash. Every still-underfilled first
  retry emits a candidate snapshot. A hull with five through nine actual
  garrisoned soldiers emits `RAW44B attack partial departure`, enters the
  existing screened route, and gives the remote order only to passengers that
  were aboard; a hull below five retains bounded recovery. Candidate action
  and target evidence establishes the first upstream divergence before any
  further passenger-behavior fix.
- **Latest result:** T6 runtime PASS for safe partial assault. Orange's six
  partial terminals at 43:11, 51:37, 56:44, 59:48, 63:22, and 67:12 retained
  9/8/8/8/8/6 soldiers. The first five completed landings at 46:40, 54:15,
  58:42, 61:41, and 65:26. Each completed remote-order set exactly equals the
  original manifest minus the stopped shore stragglers. The sixth received a
  home-recovery unload at 68:50; its later route rejection is not publicly
  diagnosed. Four below-five terminals aborted with 0/4/0/0 passengers.
- **New upstream evidence / next action:** 56 snapshots show distinct cases:
  all twelve mining samples lost group ownership (causal fix below); three
  scout samples resumed exploration; most other samples retained enter orders
  toward the correct hull, sometimes still approaching from far away. Orange
  soldier 40673 was idle with no target at 51:22 and 51:37, but later belonged
  to the successful 58:42 landing, so it is not inherently untransportable.
  Exact geometry/internal command causes for the close military stalls remain
  unknown. The nominal four-second assault retry and thirty-second terminal
  use `gl-game-time`, refreshed only every fifteen seconds; observed early
  snapshots can occur up to fifteen seconds after loading. Keep that timing
  defect separate from the T7 reservation patch.

### Generic cleanup strips mining-passenger reservation

- **Status:** CLOSED for the specific cleanup flag mutation, T7 runtime PASS.
- **User-visible symptom:** queued migrant villagers lose their transport
  reservation flag while boarding; this is one established sub-defect of the wider
  passenger failure report, not a universal explanation for military stalls.
- **Direct evidence:** twelve RAW44B mining snapshots across Purple, Cyan and
  Gray show flag -2, including Purple 31871 at 66:38 and 31787 at 67:05. All
  27 military and 17 scout snapshots retain flag 4.
- **Root cause:** `rawai-general.per` selects non-exploring villagers with a
  non-tree target, puts them into group 0, sets their flag to 0, then clears
  it. Migrants targeting their hull match that selector. The original group-4
  search membership can still retrieve them, but their ownership flag is gone.
  AIRef documents that the flag is per-object and -2 means unassigned:
  <https://airef.github.io/commands/commands-details.html#up-modify-group-flag>.
- **Contradictory/limiting evidence:** retaining enter orders in these samples
  does not prove every worker was stopped or that flag loss explains every
  loading failure. Soldiers are not selected by this villager cleanup.
- **Implementation:** `9d0c87b` excludes `migration-boarding-group` before
  temporary group creation. Existing unreserved-villager cleanup remains.
  `rawai-military.per` is byte-identical to T6; no thresholds, routes, attack
  owners, hunt rules, or Port settings changed.
- **Instrumentation/tests:** existing transition-bounded RAW44B group/command
  snapshots are retained. A focused selector/flag model reproduces old flag
  4 -> 0 -> -2 behavior and proves reserved exclusion under the patched
  selector; a mutation removing the filter reproduces the failure.
- **Acceptance criterion:** early and terminal mining samples retain flag 4
  while reserved, with the general-cleanup exclusion retained. Broader command
  exclusivity, boarding/landing/work progress and other STOP writers are
  separate acceptance criteria, not consequences of preserving a flag.
- **Latest result:** T7 all-player audit finds 39/39 identified mining-worker
  snapshots retaining flag 4, versus 12/12 flag -2 in T6. Deterministic selector
  and non-regression tests PASS. T7 military and identified migration samples
  also retain flag 4. Command interference nevertheless occurs: see next entry.
- **Next action:** preserve this exclusion and its test; do not reapply it as
  the fix for subsequent STOP/recall events or close overall transportation.

### Reserved passengers receive competing recall, STOP and work orders

- **Status:** INVESTIGATING. Interference is directly demonstrated; exact
  producing callers and the complete safe ownership mechanism are unresolved.
  Directive completion state: ROOT CAUSE NOT FULLY PROVEN — OWNERSHIP
  TELEMETRY REQUIRED. The shared architectural requirement is in
  `TASK-OWNERSHIP.md`; this is not a collection of isolated micro-fix tickets.
- **User-visible symptom:** queued soldiers are pulled away from Transports;
  armies accumulate at Town Centers. Manual loading can release pending routes.
- **Direct evidence:** T7 all-player audit, 103 boarding snapshots and 202 raw
  DE_RETREAT packets. Red reserved scout 44331 has a flag-4 enter-order snapshot
  at 54:57, then appears in recalls to TC 4538 at (82,35) at 55:02.350 and
  55:08.354, before any unload. Gray at 61:08.762, Blue at 68:42.820 and Purple
  at 80:42.502 also have selected passengers recalled before recorded unload.
  Nineteen load-record/retreat overlaps include repeated loads and some later
  post-unload recalls; do not present all nineteen as stolen boarding groups.
- **Distinct STOP evidence:** Orange's 61:36-62:06 boarding window contains
  749 identical AI_ORDER packets selecting scout 4638 and soldier 30434 with
  order 706 (STOP). Both are selected passengers with flag-4/no-active-target
  snapshots. Nine passengers depart; the scout stays ashore. Orange's only
  DE_RETREAT is 67:46.218, so this is not an overlapping recorded retreat.
  Cyan scout 4639 receives explore order 705 between boarding retries, and
  Green worker 47605 receives repeated TC-target orders starting at 83:01.
- **Architectural replay-wide evidence:** 132 windows / 1,053 passenger-window
  instances: 65 corroborated successful without observed conflict (56 full,
  nine exact partial landing), 83 pre-boarding conflicts with owner evidence,
  905 unresolved. Per-color conflict counts: Red 9, Green 9, Yellow 0,
  Purple 4, Orange 3, Cyan 2, Blue 12, Gray 44. Among the 83 first conflicts,
  67 are WORK; therefore recall-only changes cannot cover the demonstrated
  failure surface. Continuous ownership and exact native/script attribution
  remain open rather than inferred from sparse flags. All 202 retreats retain
  exact members, previous commands and applicable boarding-window links.
- **Current causal hypotheses:** scripted global recall/all-unit reset,
  native attack/scout ownership, or another local command writer can overwrite
  boarding without changing the reservation flag. Five military rules and
  taunt 45 call global recall; two also reset all units. Local defense/leash
  selection does not exclude every reservation. Source existence alone does
  not identify which path produced the replay commands.
- **Contradictory/limiting evidence:** group 4 persists in all 101 identified
  snapshots, so flag loss is not the general cause. Some stalled units retain
  correct enter orders. Red eventually boards despite the two recalls. Orange
  has a separate STOP mechanism. Snapshot timing can miss between-retry orders;
  the new full-stream audit corrects packed-ID/second-resolution limitations,
  but cannot supply missing simulation acknowledgments or owner-change logs.
- **Instrumentation/tests:** T8 `RAW44O` logs immediately before each scripted
  global recall: source, assault state/hull, migration state/hull. Sources:
  1 land defense; 2 naval defense; 3 siege escalation; 4 loss regroup;
  5 periodic losses/all-unit reset; 6 allied taunt 45/all-unit reset. Five logs
  per invocation; no new sampling loop, search mutation or goal allocation.
  Tests verify all six callers and hash the entire military/taunt executable
  program back to T7 after removing only the added logs.
- **Implementation:** diagnostic commit `d10f33e`, deployed T8. No behavioral
  ownership fix implemented. Salvage D retains offline retreat events and
  generic compact chat categories. New `tools/audit_task_ownership.py` and its
  packet/lifecycle tests retain replay-wide command evidence; raw artifacts
  remain external. No new runtime marker or deployment in this session.
- **Acceptance criterion:** shared ownership lasts until explicit complete,
  abort, loss, release or verified emergency preemption; ordinary military and
  economic selectors respect it; routine defense acquires bounded free units;
  severe hostile defense cancels old owners cleanly; allied relief uses live
  hostile presence near persistent first-TC coordinates, even after TC loss.
  Pass the nine section-H contracts plus all-player fresh runtime validation,
  preserving ordinary attacks, partial/full lifts, relics and screened landings.
- **Latest result:** T7 interference PASS as evidence; exact caller attribution
  unresolved. T8 deterministic/structural checks and deployment identity PASS;
  fresh T8 runtime PENDING. Telemetry is not defect resolution.
- **Next action:** instrument the missing ownership/worker command boundaries
  with bounded, explicit coverage and acquire/release reasons, then distinguish
  script-selected, script-delegated and autonomous native orders in a controlled
  engine test. Use T8 for the six recall writers but do not claim it alone can
  settle worker attribution. Establish the minimum protection mechanism, then
  implement the shared contract, threat preemption and allied-anchor requirements.
  Do not reapply the closed generic flag fix or guess that flags lock native work.

### Repeated attack-Transport landing timeouts

- **Status:** INVESTIGATING.
- **User-visible symptom:** assault Transports often load, fail to land, and
  later unload at home or remain loaded.
- **Direct evidence:** of seventeen P3B44T2 semantic assault missions, fifteen
  reached unload windows; six completed and nine timed out. Orange timed out
  six and Cyan three. Orange repeatedly reused candidates near 182,119 and Cyan
  near 116,1. No window contained a guard action targeting its hull.
- **Current hypothesis:** failed or inaccessible candidate coordinates are not
  remembered/rejected, allowing later missions to repeat the same terminal
  landing choice.
- **Contradictory/unknown evidence:** command records prove unload issuance and
  terminal outcome but not terrain collision, passability, hostile obstruction,
  or actual passenger state. A coordinate timeout is not by itself proof that
  the tile is permanently invalid.
- **Instrumentation/tests:** existing public screen, landing-staged, completed,
  and timed-out events reconstruct mission lifecycles but do not publish the
  selected/rejected coordinates or exact remaining garrison at terminal.
- **Implementation:** none in P3B44T3 or P3B44T4; deliberately excluded from
  both narrow causal patches.
- **Acceptance criterion:** after a terminal unload failure, the exact failed
  landing and local offsets are rejected for a bounded period; a later mission
  selects a distinct viable candidate and passengers disembark.
- **Latest result / next action:** add bounded public landing-coordinate,
  remaining-garrison, and rejection telemetry before selecting a behavioral
  fix.

### Migration blind landing offsets

- **Status:** CLOSED.
- **User-visible symptom:** Purple performed odd scout-Transport actions around
  14 and 24 minutes in P3B44T2. Green later performed the same conspicuous
  twenty-passenger migration around 1:22 in P3B44T4 and returned home without
  landing anyone.
- **Direct replay evidence:** Green hull 32009 tried resource anchor 134,196 at
  80:42, followed by the exact source-generated eight-tile diagonals 142,204,
  126,204, 142,188, and 126,188 at twenty-second intervals. No passenger
  landed; five home unloads followed from 82:23 through 83:24. Purple T2 had
  already reproduced the same five-point sequence twice.
- **Authoritative terrain evidence:** the P3B44T4 replay header identifies
  134,196 as terrain 0, the first two diagonals as terrain 1, and the southern
  diagonals as terrain 0 on landmasses separated from the target island by
  continuous water. The Rome at War DAT names terrain 0 `Grass` and terrain 1
  `Water, Shallow`. Thus two retries were water and two were different islands.
- **Root cause:** `up-bound-point` only shifts coordinates into map bounds. The
  migration state treated that as sufficient validation, issued unloads to
  four fixed eight-tile diagonals without reading their zone or testing the
  exact hull's path, and exhausted the sequence into home recall.
- **Implementation:** P3B44T5 replaces the diagonals with four close two-tile
  cardinal candidates around the exact resource anchor. Before the initial or
  any alternate unload, it reads the candidate point zone, requires equality
  with the stored resource-anchor zone, rebuilds the exact reserved hull, and
  requires `up-path-distance ... 0 != 65535`. Wrong-zone and unreachable
  candidates emit bounded public reason/identity telemetry and advance after
  one second without an unload command.
- **Non-regression risk:** previously successful migration landings, the
  P3B44T4 relic ferry, T3 departure clearance, and T2 assault landing screen.
  The patch changes only the shared migration landing-candidate transition.
- **Acceptance criterion:** each migration unload is preceded by a same-zone
  exact-hull path-clear event; no unload follows a wrong-zone or path-rejected
  candidate; a small-island mission either lands in its selected resource zone
  or terminates with bounded explicit reasons without targeting water/another
  island. At least one previously successful migration remains successful.
- **Latest runtime result:** P3B44T5 supplied 48 public migration candidate
  missions across seven players. All 95 `landing path clear` events had an
  exact same-second unload by the reported hull; all 4 wrong-zone and 36
  path-rejected events had no same-second unload. Four all-invalid missions
  skipped all five invalid candidates and recalled home. Red independently
  landed ten settlers in zone 3, completed a Mining Camp, and retasked them.
  Previously working assault and relic transport behavior remained present.
- **Closure basis:** every behavioral acceptance criterion was demonstrated by
  the byte-identified runtime replay. No further landing-candidate patch is
  authorized without new contrary runtime evidence.

### Migration escort ownership overlap

- **Status:** INVESTIGATING.
- **User-visible symptom:** a loaded migration hull can have friendly warships
  crowding it during approach, landing retries, or recall.
- **Direct evidence:** Green warships repeatedly received GUARD orders on exact
  migration hull 32009 throughout both 77:58-83:24 and 84:40-88:00 episodes,
  including every refresh across the first remote unload/retry window.
- **Current causal boundary:** the generic escort selector excludes only the
  assault controller's `TRANSPORT-ROUTE-RETURN-WAIT`; it does not exclude a
  Transport reserved by `migration-transport-group` or any migration landing
  state. This proves overlapping ownership policy. Replay commands do not
  serialize collision polygons, so they do not prove which unload physically
  failed because of an escort.
- **Implementation:** none in P3B44T5. Removing protection for the whole
  civilian voyage would risk a transport-survival regression without proving
  the necessary clearance window.
- **Acceptance criterion:** targeted telemetry or direct visual evidence ties
  a specific guard/ship position to a stalled migration approach; the eventual
  patch stages owned escorts clear only for the proven window and preserves
  voyage protection.
- **Latest result / next action:** 30 of 48 P3B44T5 public migration candidate
  windows contained guard commands on the exact hull, totaling 62 guard
  events. Guards also overlapped successful or partial Red landings, so they
  are not universally fatal. Preserve INVESTIGATING status until position or
  targeted clearance evidence ties a specific guard to a specific stall.

### Migration drop-off establishment and premature recall

- **Status:** ROOT-CAUSE-PROVEN for Purple; INVESTIGATING for Orange.
- **User-visible symptom:** Purple and Orange delivered villagers to an island
  but established no resource drop-off.
- **Purple direct evidence:** hull 30184 landed twenty builder-capable
  passengers at 82:57/83:17. Passenger 30667 issued Mining Camp build 584 at
  94,161 at 83:36. At 83:37 nineteen passengers were ordered to reboard and at
  83:39 the hull began home unloads.
- **Purple root cause:** `MIGRATION-WAIT-DROPSITE` advances on the global
  `up-pending-objects mining-camp >= 1` condition. Assignment then searches for
  a concrete pending foundation within eight tiles and the target zone. A
  queued build command can satisfy the global count before such a foundation
  is searchable; the no-target assignment branch immediately sets
  `MIGRATION-DROPSITE-FAILED`, bypassing the intended twenty-second/four-offset
  placement retries. The one-second build-to-reboard cadence follows only that
  source path.
- **Orange direct evidence:** hull 34221 landed twenty builders at
  83:36-84:16. No passenger issued a Mill/Lumber/Mining Camp build within
  twenty-four tiles during the rest of the replay. Fifteen were told to
  reboard at 86:02 and never unloaded again before the replay ended.
- **P3B44T5 evidence:** Red completed one full landing/drop-off lifecycle at
  52:33-54:28: ten settlers landed, exact builders were assigned, the Mining
  Camp completed, and the settlers were retasked. Three later Red zone-14
  landings delivered 2, 6, and 11 settlers but each then emitted an explicit
  `migration mining camp resource wait:14` for 60 seconds before drop-site
  failure and home recall. Those are resource-starvation terminals, not the
  earlier Purple one-second global-pending race.
- **Contradictory/unknown evidence:** only each local AI's self chat is private;
  Orange's exact anchor, affordability, placement-owner, and watchdog state is
  not serialized. Purple has a build command but the replay does not prove a
  placed foundation or engine rejection reason.
- **Instrumentation/tests:** action cadence plus source-state comparison proves
  Purple's transition; Orange needs public first-blocker/terminal telemetry.
- **Implementation:** none in P3B44T3 or P3B44T4.
- **Acceptance criterion:** a landed migration waits for and assigns a concrete
  same-zone drop-site foundation, completes it, and uses it before passengers
  can be recalled; unavailable placement reaches bounded retries and a precise
  terminal reason.
- **Latest result / next action:** fix Purple's premature global-pending
  transition as a separate causal patch. Preserve the successful Red lifecycle
  as the non-regression control. Add or retain bounded public affordability and
  first-blocker evidence for Orange and the late Red resource-wait cases before
  changing their distinct pre-drop-site paths.

### Orange delayed assault activation

- **Status:** INVESTIGATING.
- **User-visible symptom:** Orange performed no observed assault transportation
  until Blue and Gray were effectively defeated.
- **Direct evidence:** Orange's first public assault-screen event was at 42:26
  and first completed assault landing at 53:41. The user's visual timing is
  preserved as authoritative observation.
- **Contradictory/unknown evidence:** the replay contains no serialized
  defeat/resignation notice for Blue or Gray and does not publish Orange's
  private attack-ready, army ownership, passenger, or target gate before 42:26.
- **Instrumentation/tests:** current public telemetry begins only after a route
  screen exists, too late to identify the first blocked activation condition.
- **Implementation:** none.
- **Acceptance criterion:** Orange activates an eligible cross-water assault
  based on its own readiness/target state rather than allied collapse, or
  bounded telemetry proves which legitimate prerequisite is absent.
- **Latest result / next action:** add public transition-only telemetry for the
  first blocked assault-activation gate; do not guess a gate from timing alone.

### Command-volume anomaly and deferred crash

- **Status:** DEFERRED by the user until transport defects are handled.
- **User-visible symptom:** the 15:12 P3B44T3 match crashed before its natural
  end. The user believes this is the already known crash class.
- **Direct evidence:** the decoded replay ends at 59:33 without a resignation
  action and has zero parser errors. Cyan serialized about 586,260 AI_ORDER
  records; Green, Yellow, and Blue also produced unusually high WORK volumes.
  The non-crash 21:43 P3B44T4 replay independently contains 1,256,052 ACTION
  operations: 580,574 ORDER, 372,491 AI_ORDER, and 194,037 WORK. Several
  garrisoned Green migration passengers each received roughly 5,400-10,100
  repeated ORDERs toward object 4561 at the exact home point; large repeated
  streams also occur for other players and objects.
- **P3B44T5 evidence:** the 5:11:04 replay contains 3,260,167 ACTION
  operations: 1,830,452 AI_ORDER, 916,162 ORDER, and 235,131 WORK. The largest
  repeated ORDER stream is Yellow object 52175 to target 57803 at 139,121:
  49,780 orders from 180:10 through 311:03. Replay BUILD evidence identifies a
  Yellow Town Center at that coordinate, but the producing rule remains
  unproven. Separately, Yellow hull 32151 produced 792 and Green hull 59397
  produced 412 repeated home unloads. Source inspection proves
  `TRANSPORT-ROUTE-RECOVERY-CHECK` can reissue a home unload every 15 seconds
  indefinitely while garrison count remains positive; these 1,204 unloads are
  a proven sub-loop, not an explanation for the millions of other commands.
- **Current causal boundary:** the Green streams begin as individual passengers
  disappear from the three-second unboarded retry list and stop around their
  home unload, strongly correlating this instance with garrisoning. Other
  repeated streams prove the subsystem is broader than migration or relic
  ferry. The replay does not identify which script/built-in owner generated
  every engine ORDER or prove that command volume caused the earlier crash.
- **Unknown evidence:** the replay does not contain an exception code, faulting
  module, corrupting writer, stack, or linked dump. High command volume and the
  crash coexist but causality is not established.
- **Implementation:** none. Do not mix an unproven command-spam change into the
  same-zone migration P3B44T5 patch.
- **Acceptance criterion / next action:** after the user resumes crash work,
  correlate an exact ProcDump/Windows exception with this runtime and identify
  the first command-volume producer or corrupting writer before proposing a
  fix.

### Boar gathering abandoned after emergency Town Center garrison

- **Status:** INVESTIGATING; separate hunting/economy defect, not part of the
  transport-only behavioral patch.
- **User-visible symptom / direct evidence:** while P3B44T6 was running on
  2026-08-30, the user observed Yellow abandon gathering a boar at approximately
  22-24 minutes after its villagers garrisoned in the Town Center during an
  enemy attack. Color and approximate time were explicitly confirmed by the
  user. The supplied T6 replay does not expose Yellow's private hunt-state
  chat; remaining food and exact post-exit worker assignments remain unknown.
- **Source evidence / causal hypotheses:** `rawai-hunt.per:467-491` requires
  at least one hunter for the normal support retry. At `:497-571`, retry
  validation removes the original lurer if its current target is no longer
  the saved boar, then disables hunting and releases ownership if either the
  lurer lookup or boar lookup fails. A changed worker assignment is therefore
  conflated with target loss in that branch. Zero hunters can instead leave
  the ordinary retry ineligible. Neither branch is yet tied to this event.
- **Contradictory/alternative evidence:** built-in worker reassignment, a
  continuing threat, resource exhaustion, or a different hunt state remain
  untested; source inspection does not establish the in-engine transition.
- **Instrumentation/tests / latest result:** the all-player chat and relevant
  order sweep does not establish Yellow's hunt transition. WORK payloads lack
  worker/target fields in the current parser; absence of decoded boar orders
  does not contradict the user's observation. Initial-object metadata proves
  repeated target 4475 is Yellow's Town Center. Red's own logs show three
  active-to-released transitions at 07:34,18:57,29:08, which are separate
  evidence and not proof of Yellow's cause.
- **Implementation:** none for hunting; `rawai-hunt.per` is unchanged.
- **Acceptance criterion / next action:** improve the missing WORK decoding if
  reliably possible, or add bounded public owner/lurer/boar/threat transition
  diagnostics in a separately scoped hunting patch. A safe surviving carcass
  should regain gatherers after the threat ends
  without premature ungarrison, a second lure, or disruption of sheep/transport
  ownership. Do not merge a guessed hunting fix into the transport experiment.

### Port placement: opposite island shores and open-water access

- **Status:** OPEN; explicitly authorized on 2026-08-30 for the development
  cycle after the P3B44T7 replay is supplied, separate from salvage integration.
- **User-visible symptom / direct evidence:** the user reports Ports being
  placed in narrow crevices, causing problems for trade ships.
- **Requested behavior:** for an island start, place the two Ports on opposite
  sides of the island and avoid narrow crevices that obstruct ship traffic.
- **Requested controls / causal hypothesis:** investigate and adjust
  `sn-dock-placement-mode`, `sn-minimum-water-body-size-for-dock`, and
  `sn-dock-proximity-factor`. Their exact semantics and sufficiency for these
  requirements are not yet verified; do not treat parameter tuning alone as
  proof of shoreline clearance or opposite-shore placement.
- **Contradictory evidence / instrumentation/tests:** no new placement analysis
  or tests in this note-only session; exact sites and failure mechanisms await
  replay/source investigation.
- **Implementation / latest result:** none; documentation only. No runtime
  changes, deployment, full test suite, commit, or PR update.
- **Acceptance criterion / next action:** in the next development cycle,
  inspect Port placement across all players and verify the controls before
  choosing values. Validate opposite-side placement on island starts with
  suitable buildable shores, accessible builders, and clear ship approaches,
  including sustained trade traffic without crevice congestion. Preserve
  functioning early Port construction and existing transport behavior.

### Deliberately unchanged defects

This one-cause patch does not change or claim to fix:

- cliff-bound or otherwise unreachable landing points unrelated to friendly
  Scout obstruction;
- route-scouting, route-threat scanning, landing selection, or naval pathfinding;
- the still-unproven upstream cause of individual passenger nonboarding,
  migration passenger thresholds, migration escort ownership, or migration
  drop-site establishment outside exact landing-candidate screening;
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

P3B44T2 all-player transport replay:

- Basename:
  `SP Replay v101.103.48987.0 @2026.08.29 131027.aoe2record`.
- SHA-256:
  `932E900C02D50DD01B0FC24FF3B113F562BACE88F102B180C7316550B1412F88`.
- Duration: 1:43:19; parse errors: zero; marker `RAWAI-P3B44T2:443`
  serialized from players 2 through 8.
- Selected-color metadata independently validates the preserved lobby mapping;
  no team/color was inferred from row or slot.
- External analyses:
  `G:\Projects\Codex\Rome at War AI\.analysis\replay-20260829-131027-p3b44t2-compact.json`
  and
  `G:\Projects\Codex\Rome at War AI\.analysis\replay-20260829-131027-p3b44t2-full.json`.
- Systematic union: 28 active hulls, 393 load commands, 284 unload commands,
  108 load-to-unload phases, 10 load-only phases, and 4 unload-only phases.
  Per-player load/unload-phase counts were Red 54/17, Green 48/9, Yellow
  63/9, Purple 71/24, Orange 61/21, Cyan 65/25, Blue 13/2, Gray 18/1.
- Repository evidence entry:
  `britain-4v4-20260829-131027-p3b44t2-all-transport` in
  `replay-benchmarks.json`.

P3B44T3 all-player transport replay:

- Basename:
  `SP Replay v101.103.48987.0 @2026.08.29 151250.aoe2record`.
- SHA-256:
  `0C1C909D4BB36D3680FEDDACB7E2E74647665CA67B00F1C0F0406D093F2D95DD`.
- Duration: 59:33; parser errors: zero; no decoded resignation action; marker
  `RAWAI-P3B44T3:444` serialized from players 2 through 8.
- Selected-color metadata independently validates the preserved lobby mapping;
  no team/color was inferred from row or slot.
- External analyses:
  `G:\Projects\Codex\Rome at War AI\.analysis\replay-20260829-151250-p3b44t3-compact.json`
  and
  `G:\Projects\Codex\Rome at War AI\.analysis\replay-20260829-151250-p3b44t3-full.json`.
- External semantic audit helper:
  `G:\Projects\Codex\Rome at War AI\.analysis\audit_transport_20260829_151250.py`.
- Systematic union: 16 explicit Transport hulls, 157 load commands, 129
  point-coordinate sea unload commands, 45 alternating load-to-unload phases,
  and 4 terminal load-only phases. Generic building/siege ungarrison records
  were excluded. Per-player hull/load/unload totals: Red 4/29/23, Green
  2/18/22, Yellow 1/5/13, Purple 2/27/18, Orange 2/23/13, Cyan 1/24/2, Blue
  2/16/24, Gray 2/15/14.
- Repository evidence entry:
  `britain-4v4-20260829-151250-p3b44t3-all-transport` in
  `replay-benchmarks.json`.

P3B44T4 all-player transport replay:

- Basename:
  `SP Replay v101.103.48987.0 @2026.08.29 214328.aoe2record`.
- SHA-256:
  `36561ABA8EDCDA3B5623E491ED0222B2852C1435B4F461C713059261CF58B41B`.
- Duration: 1:49:40; parser errors: zero; no decoded resignation action;
  marker `RAWAI-P3B44T4:445` serialized from players 2 through 8.
- Selected-color metadata independently validates the preserved lobby mapping;
  no team/color was inferred from row or slot.
- External analyses:
  `G:\Projects\Codex\Rome at War AI\.analysis\replay-20260829-214328-p3b44t4-compact.json`
  and
  `G:\Projects\Codex\Rome at War AI\.analysis\replay-20260829-214328-p3b44t4-full.json`.
- External semantic helpers and terrain diagnostic:
  `G:\Projects\Codex\Rome at War AI\.analysis\summarize_p3b44t4.py`,
  `G:\Projects\Codex\Rome at War AI\.analysis\render_p3b44t4_map.py`, and
  `G:\Projects\Codex\Rome at War AI\.analysis\p3b44t4-green-migration-terrain.png`.
- Systematic union: 35 explicit/likely Transport hull IDs, 509 loads, 249
  point unloads, 120 alternating phases, 7 terminal load-only phases, and 2
  unload-only phases. Per-player hull/load/unload/phase totals: Red 10/67/70/26,
  Green 2/58/26/7, Yellow 4/61/27/20, Purple 5/47/6/4, Orange 2/50/45/21,
  Cyan 5/99/56/31, Blue 5/109/15/8, and Gray 2/18/4/3.
- Repository evidence entry:
  `britain-4v4-20260829-214328-p3b44t4-all-transport` in
  `replay-benchmarks.json`.

P3B44T5 all-player transport replay:

- Basename:
  `SP Replay v101.103.48987.0 @2026.08.29 232526.aoe2record`.
- SHA-256:
  `B12989601E59BDE4D4BE3ACA4D6C9B0F2F322E31FA7D9E97198AA3CDE61924CE`.
- Duration: 5:11:04; action-stream parser errors: zero; no decoded
  resignation action; marker `RAWAI-P3B44T5:446` serialized from players 2
  through 8.
- Selected-color metadata independently validates the preserved lobby mapping;
  no team/color was inferred from row or slot.
- External full analysis:
  `G:\Projects\Codex\Rome at War AI\.analysis\replay-20260829-232526-p3b44t5-full.json`.
- External semantic helper:
  `G:\Projects\Codex\Rome at War AI\.analysis\summarize_p3b44t5.py`.
- Systematic union: 42 explicit/likely Transport hull IDs, 1,678 loads, 2,054
  point unloads, 352 alternating phases, 5 terminal load-only phases, 5
  initial unload-only phases, and 11,437 raw transport actions. Per-player
  hull/load/unload/phase totals: Red 8/189/328/93, Green 3/167/459/40, Yellow
  3/81/837/24, Purple 1/484/64/64, Orange 9/238/92/36, Cyan 9/210/173/51,
  Blue 6/84/78/39, and Gray 3/225/23/5.
- Forty-eight public migration candidate missions yielded 95 path-clear, 4
  wrong-zone, and 36 path-rejected events. All 95 clear events had an exact
  same-second hull unload; no invalid event did. Red completed one full
  landing/drop-off/retask lifecycle and three later resource-wait landings.
- Repository evidence entry:
  `britain-4v4-20260829-232526-p3b44t5-all-transport` in
  `replay-benchmarks.json`.
- External cross-replay boarding audit helper:
  `G:\Projects\Codex\Rome at War AI\.analysis\audit_boarding_departure_20260829.py`.
  It is diagnostic material outside the repository and must not be committed.
- P3B44T6 boarding evidence entry:
  `britain-4v4-20260829-232526-p3b44t6-boarding-evidence` in
  `replay-benchmarks.json`. It reuses the same source replay for the distinct
  boarding-lifecycle acceptance target and is `fresh-replay-required`.

P3B44T6 all-player transport replay (2026-08-30 audit):

- Basename: `SP Replay v101.103.48987.0 @2026.08.30 114855.aoe2record`.
- SHA-256: `A26B08497C5168F942A6CA67903FAC61AD32CD2C8BFF2D07BDA69B2DE9512CE8`.
- Duration 75:25; zero action-stream parse errors; no decoded resignation.
  Ending cause is unknown, not assumed to be a crash or manual termination.
- Markers `RAWAI-P3B44T6:447` from players 2-8; before editing, all 68 installed
  files matched T6 hash
  `D5A2314E461603F68D5327E71BD7FB3737F0518C8969F2D5A4C45809B11598EB`.
- Use parser root `G:\Projects\Codex\Rome at War AI\.analysis\replay_parser_kjir`
  with repository `tools/analyze_replay.py`. The older `replay_parser` fails
  this header; do not fall back to inferred colors. The supported parser
  validates the original selected colors and resolved teams independently.
  WORK target fields and some AI_ORDER coordinates remain incomplete.
- External full report:
  `G:\Projects\Codex\Rome at War AI\.analysis\replay-20260830-114855-p3b44t6-full.json`.
- External all-player semantic audit helper and outputs:
  `G:\Projects\Codex\Rome at War AI\.analysis\audit_p3b44t6.py`,
  `G:\Projects\Codex\Rome at War AI\.analysis\p3b44t6-transport-audit.txt`, and
  `G:\Projects\Codex\Rome at War AI\.analysis\p3b44t6-transport-audit.json`.
  The helper reuses `summarize_p3b44t5.py` for existing acceptance checks.
  Its CORRECTED_PLAYER_TOTAL section adds Yellow's telemetry-identified hull
  omitted by the older movement/unload-only identity heuristic.
- Systematic union: 22 hulls, 183 loads, 142 point unloads, 55 alternating
  load/unload phases and 7 final load-only phases. Empty aborted missions can
  be load-only: these counts are not interchangeable with successful voyages.
- Per-player hull/load/unload/phase totals: Red 1/4/4/4, Green 1/8/0/0,
  Yellow 1/8/0/0, Purple 2/25/28/7, Orange 4/29/30/16, Cyan 4/27/23/7,
  Blue 3/31/15/6, Gray 6/51/42/15. All 4,176 raw SPECIAL/UNGARRISON records
  were screened; non-transport Town Center garrisons remain outside that union.
- Nine public migration boarding terminals are full, six partial and seven
  empty aborts. Ten candidate missions yield 21 clear/same-second unloads,
  1 wrong-zone rejection and 26 path rejections with zero invalid unloads.
- Six assault landing windows complete with zero active-hull guard refreshes.
  Five are Orange's safe partial lifts; Purple completes a full lift. Seven
  exact relic outbound and three return-readiness events preserve the T4 check.
- Migration escort overlap recurs (7 guards across 2 Purple candidate missions).
  Gray's 19 settlers reboard at 57:16 and 71:29 after remote landings; successful
  economic settlement is not established. The existing drop-site defect stays
  separate from reservation loss.
- 727,415 ACTION records include 355,625 ORDER and 135,582 AI_ORDER records.
  Yellow worker 31642 targets its initial TC 4475 in 27,669 repeated ORDERs
  from 17:52 to 47:50. This identifies the destination, not its producing
  controller or a crash cause; broad command-volume work remains deferred.
- Repository benchmark: `britain-4v4-20260830-114855-p3b44t6-all-transport`.
  T6 partial acceptance is runtime-confirmed; this entry's next T7 ownership
  acceptance is fresh-replay-required.

P3B44T7 all-player transport replay (2026-08-30 audit):

- Basename: `SP Replay v101.103.48987.0 @2026.08.30 131412.aoe2record`.
- SHA-256: `04AB5E6664F9DBE0284E320A99AB16070DBC00DE67FE876AC8C5512176E7DDB5`.
- Duration 98:29; zero parse errors; Red resigns at 98:28. Markers from players
  2-8 identify T7:448; full source/deployment hash was checked before editing.
  Decoded selected colors/resolved teams agree with preserved fixture
  `britain-4v4-lobby-20260827-6969d5e2`: Red/Green/Yellow/Purple Romans versus
  Orange Picts/Cyan Britons/Blue Germani/Gray Gauls. No slot-color inference.
- Screened all 5,390 SPECIAL/UNGARRISON records: 25 hulls, 378 loads, 205 point
  unloads, 119 alternating load/unload phases and five final load-only phases.
  Command phases are not completed missions. Per-player hull/load/unload/phase:
  Red 4/96/50/28; Green 1/42/21/8; Yellow 1/1/3/1; Purple 4/45/24/22;
  Orange 3/58/43/24; Cyan 1/28/1/1; Blue 7/39/35/11; Gray 4/69/28/24.
- 103 candidate snapshots: 43 military flag 4, 58 identified migration flag 4,
  two missing migration candidates. All 39 identified mining snapshots retain
  flag 4. Ten safe partial assault departures; three Purple completed landing
  windows and zero active-hull guard refreshes. Twelve migration-candidate
  missions produce 20 clear events (18 same-second unloads, Red's other two
  next-second), two wrong-zone and sixteen path rejections, with zero rejected
  same-second unloads. Two relic outbound/return readiness pairs survive.
- Purple's 90:44 partial lift completes at 93:47. Exactly nine boarded IDs
  receive the land order, excluding stopped straggler 40008. The older audit
  falsely required the army order's destination to equal the ship unload point;
  RETURN-CHECK actually orders toward the enemy target. The corrected offline
  comparison passes exact manifest-minus-stopped membership. No gameplay
  regression or behavioral patch was needed for this audit false negative.
- DE_RETREAT counts: Red 36, Green 35, Yellow 31, Purple 22, Orange 1, Cyan 23,
  Blue 53, Gray 1. All 202 raw payloads satisfy the observed `<IffII` prefix
  (target, x, y, count, mode), followed by count object IDs at offset 20.
  This validates extraction for these packets, not every replay version.
- Exact overlaps and separate STOP evidence are in the competing-orders
  defect ledger above and benchmark
  `britain-4v4-20260830-131412-p3b44t7-ownership`.
- External artifacts under `G:\Projects\Codex\Rome at War AI\.analysis`:
  `replay-20260830-131412-p3b44t7-full.json`,
  `p3b44t7-transport-audit.txt`, `p3b44t7-transport-audit.json`,
  `p3b44t7-ownership-audit.json`, `p3b44t7-packet-evidence.json`.
  Helpers: `audit_p3b44t6.py` (all-player audit, corrected partial comparison),
  `audit_p3b44t7_ownership.py`, and `inspect_t7_packets.py` (all retreats plus
  targeted AI_ORDER IDs 4638/4639/53368/40008). The latter output has 48,912
  targeted packets; adapt watch IDs for another replay rather than assuming
  these IDs recur. The ownership helper takes the full report as argv[1].
- Reproduction tools: use Python 3 at
  `C:\Users\LostSoul\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`;
  PATH Python is version 2. `tools/analyze_replay.py` arguments are parser root,
  replay path, `--output` full report. Audit helper arguments are full report
  and output `.txt`; packet helper takes replay path. Reuse `replay_parser_kjir`.
- Decoder limits: stock parsing omits retreat members and misaligns several
  AI_ORDER fields. Targeted raw parsing keeps bytes and length/count checks;
  AI_ORDER order is at offset 16 in the inspected packets, not the decoded
  floating-point x field. Packed-ID heuristics and coarse episode windows
  require care; a post-unload order is not automatically boarding interference.

### Architectural ownership audit of the same T7 replay

- Requirement/aggregate record: `TASK-OWNERSHIP.md`. This preserves the new
  user directive without requiring access to the conversation or attachment.
- New external artifact:
  `G:\Projects\Codex\Rome at War AI\.analysis\p3b44t7-task-ownership.json`.
  Generated by repository-local `tools/audit_task_ownership.py`; its complete
  reproduction command is in `TASK-OWNERSHIP.md`. Use the same Python 3 and
  `replay_parser_kjir` paths recorded above.
- Prior hull/color/partial-landing evidence input:
  `p3b44t7-transport-audit.json`, SHA-256
  `C0D7CD60350628E7AEDEBA16D5304E74C4D97C45EC84AB9C3085813F216DEB08`.
  This older artifact has no embedded replay hash; its T7 association is
  recorded here, not automatically proven by the new tool. The new report
  fingerprints both inputs and explicitly records the dependency.
- Full-stream decoding uses exact packet lengths for SPECIAL/UNGARRISON,
  WORK, AI_ORDER and every DE_RETREAT. It retains raw bytes, file offset,
  millisecond time, stream sequence, all selected IDs and actual target/order.
  No object-ID magnitude shifts or arbitrary task timeout. Zero decoding
  failures for this replay; no claim of universal version compatibility.
- All 378 load commands are represented in 132 evidence-delimited windows
  (33 assault, 41 migration, 58 unresolved/recovery/relic), alongside all 202
  retreats. The 1,053 passenger-window instances split 65 corroborated
  successful without observed conflict / 83 pre-boarding conflicts with owner
  evidence / 905 unresolved. The unresolved group includes 323 conflicts with
  uncertain timing or ownership. No individual deaths or unavailability are
  proven, not a claim that none occurred.
- Source inventory retains 247 command/build-delegation rules and 248 selection
  rules with facts/actions/line numbers. It is not a complete certification of
  native strategic-number behavior or all permission/release paths. Source
  gaps and every global-recall source are classified in `TASK-OWNERSHIP.md`.
- T8 remains installed unchanged. No shared ownership, threat-preemption or
  allied-anchor implementation is present. Required section-H gameplay tests
  and architecture runtime acceptance remain pending.

Replay/savegame files, compact parser output, crash dumps, and Rome at War data
mod files remain external and must never be committed to the AI repository.

## Validation performed

- Moving normally: PASS.
- Stalled near origin: PASS.
- Ownership safety: PASS.
- Clearance success: PASS.
- Clearance failure: PASS.
- Landing screen/escort clearance and refresh gate: PASS.
- Relic-ferry exact-passenger load recognition: PASS (focused deterministic
  test, including the required DE garrison-inclusive filter and removal of the
  indirect hull-count CHECK-LOAD condition).
- Migration landing candidate screening: PASS (focused deterministic test;
  the initial and all four alternate candidates pass through exact-hull zone
  and path screening, while wrong-zone/path-rejected branches issue no unload).
- P3B44T6 boarding diagnostics: PASS (one bounded pre-retry sample and one
  terminal sample where applicable for both assault and migration; command,
  target, movement, zone, idling, and group fields are all required).
- P3B44T6 safe partial assault: PASS (five-to-nine versus below-five terminal
  split, shore-straggler stop, garrison-inclusive exact manifest rebuild,
  actual-count update, home-defense interrupt, target revalidation, and prior
  abort recovery are covered).
- Full P3B44-derived regression suite: PASS (134 tests, including T8 and the
  twelve new ownership-audit packet/lifecycle tests).
- PER structural/operand validation: PASS.
- Naval-doctrine validation: PASS.
- Strategy execution: PASS (1,156 total matchups; 1,149 historical and 1,152
  Extreme matchups with adjustments).
- ODS workbook round trip: PASS (34 civilizations, 680 unit-evidence rows, 340
  naval-class rows).
- Replay benchmarks: PASS (29 entries).
- `git diff --check`: PASS; only expected CRLF notices.
- Adversarial P3B44T2 comparison: PASS. P3B44T3 changed only the active
  transport departure state, goals/constants, marker, bounded telemetry,
  deterministic tests, and replay evidence. It does not alter the T2
  screen/escort landing rules or any ordinary attack owner.
  `up-target-objects`, `up-retreat-now`, `up-reset-attack-now`, `attack-now`,
  and `up-find-player` counts are identical to P3B44T2.
- Every new departure state has a producer and consumer. Exact blocker movement
  is verified after eight seconds; one safe retry and three blocker selections
  are hard bounds. The adversarial review found and fixed delayed-retry
  ownership safety: loaded, attacked, grouped, or quarantined blockers are
  skipped rather than retasked.
- P3B44T3 runtime/replay acceptance: PASS. Exact blocker 37204 cleared the
  twelve-tile radius; loaded hull 31205 resumed, landed, and preserved the T2
  screen/escort behavior. Friendly departure congestion is CLOSED.
- Adversarial P3B44T4 review: PASS. The patch touches only the relic-ferry
  boarding-readiness transition, marker, one isolated goal, tests, changelog,
  and replay evidence. DE's documented default excludes garrisoned DUC search
  results, so `fe-filter-garrisoned c: 1` is set after each full search reset.
  The exact passenger controls readiness; the exact reserved hull still owns
  the unchanged unload action. Pending/missing telemetry is one-shot per
  attempt and the prior watchdog remains the hard terminal bound.
- P3B44T4 runtime/replay acceptance: PASS. Orange and Cyan completed two
  independent exact relic-ferry round trips, Red and Green independently
  advanced through exact departure before the watchdog, and all five T2 assault
  landing windows remained free of guard refreshes. Relic-ferry load recognition
  is CLOSED.
- Adversarial P3B44T5 review: PASS. Every landing candidate is rebuilt against
  the exact reserved hull; zone equality/inequality, reachable/unreachable, and
  missing-hull outcomes are exhaustive. Rejected candidates yield on a bounded
  one-second timer and retain the existing five-attempt/home-return terminal.
  The patch does not change relic-ferry, departure-clearance, assault landing,
  escort ownership, drop-site construction, or ordinary attack rules.
- Adversarial P3B44T6 review: PASS. The replay-visible manual load is preserved
  as corroboration rather than misclassified as an AI group. Early and terminal
  candidate samples are transition-bounded, so they cannot create a per-sweep
  telemetry loop. The initially proposed passenger-to-hull `up-path-distance`
  diagnostic was removed before deployment because a land unit cannot path to
  a Transport's water tile; actual action, target, command, move, distance,
  zone, group, and idling fields are recorded instead. Partial departure stops
  ashore members and rebuilds the direct-control group from garrisoned members
  before entering the unchanged target and route checks. Home defense can
  interrupt every new diagnostic/manifest state.
- `validate_good_units.py` has a pre-existing P3B44 provenance-hash failure;
  frozen unit-strategy material is outside this transport patch.
- Installed P3B44T6 runtime byte verification: PASS (68 files; aggregate
  source/target SHA-256
  `D5A2314E461603F68D5327E71BD7FB3737F0518C8969F2D5A4C45809B11598EB`; no
  missing, different, or unexpected runtime files).
- Fresh P3B44T5 engine/replay acceptance: PASS. All 95 path-clear candidates
  issued an unload, all 40 wrong-zone/path-rejected candidates issued none,
  all-invalid missions remained bounded, and Red completed a same-zone landing,
  Mining Camp, and settler retask. Migration blind landing offsets are CLOSED.
- P3B44T2/T4 runtime non-regression in P3B44T5: PASS. Eleven resolved assault
  landing windows had zero active-hull guard commands, and exact relic
  passengers continued outbound/return lifecycles. No public exact-blocker
  congestion episode independently re-exercised P3B44T3; its earlier runtime
  acceptance remains the control evidence.
- Fresh P3B44T6 engine/replay acceptance: PASS for safe partial departure.
  Five completed partial landings pass exact-manifest-minus-stopped comparison;
  low-strength aborts are preserved. Other boarding failures remain open.
- P3B44T7 focused selector/flag fixture and regression suite: PASS (119 tests).
  PER, naval, strategy, workbook and 28 replay-benchmark validators: PASS.
- P3B44T7 read-only adversarial review: ACCEPTED the demonstrated group-0
  overwrite/clear and its preselection exclusion. The earlier review rejected
  a universal command-theft explanation from the available military snapshots.
  T7 now proves specific command interference despite group 4; retained flags
  do not establish exclusive control. DEFERRED stale-clock boarding timing,
  scout exploration overrides and close military stalls to separate causal
  patches. No military, hunt, homebase or economy PER file changed from T6.
- P3B44T7 deployed byte identity: PASS, 68 source/target files matching
  `69C30C50661D3E1E8A1F8DC081C63E80D0C899D8E695B16D3E02F95B910B7738`.
  Only general cleanup and the marker differ from the tested T6 runtime.
  T7 runtime PASS for the narrow cleanup flag exclusion (39 mining snapshots).
- T7 all-player partial/relic/landing-screen non-regression: PASS for the
  reconstructable outcomes recorded above. No claim that every voyage worked.
- T8 diagnostic tests: PASS; all six caller tags precede recall/reset actions,
  and removing only logs reproduces T7 military/taunt executable fingerprints.
  The fingerprints deliberately freeze this diagnostic experiment; future
  authorized behavior patches must replace that acceptance fixture explicitly.
- T8 full validation: 122 tests, PER structure/operand domains, 34-civilization
  naval doctrine, strategy execution, ODS workbook and 29 benchmarks PASS.
  `validate_good_units.py` still reports the pre-existing
  `source_provenance/unique-unit-production.json_sha256` mismatch. Do not
  repair frozen strategy provenance as an unrelated transport change.
- T8 read-only adversarial review: ACCEPTED exact retreat-member inspection,
  separation of the Orange STOP loop, and correction of the landing audit's
  coordinate assumption. REJECTED treating reservation flags as exclusive
  ownership or a retreat-only explanation as universal. DEFERRED exact caller
  attribution and native/local STOP cause pending discriminating runtime logs.
- T8 deployment PASS: all 68 files match the installed identity above. Runtime
  caller attribution and gameplay fix acceptance remain PENDING/INVESTIGATING.
  No GitHub push or PR update was made in this session; only local commits.
- Architectural audit validation: PASS, 134 unit tests / 29 replay benchmarks /
  PER structure and operand domains / `git diff --check`. The T7 audit rerun
  covers every known load and retreat with zero decoder failures. Read-only
  adversarial findings are triaged in `TASK-OWNERSHIP.md`; accepted fixes were
  made to the audit, not the runtime. Strategy/workbook validators were not
  rerun for this audit-only change; their prior results and provenance failure
  above remain historical, not new session claims.
- Architectural gameplay acceptance: NOT RUN / NOT IMPLEMENTED. The twelve
  audit tests do not exercise the engine or implement section-H contracts.
  Installed T8 identity rechecked PASS: all 68 runtime files byte-identical,
  no files copied and no marker changes. The canonical checkout and immutable
  attack baseline were not edited; user-owned `AGENTS.md` remains untouched.

## Exact next actions

1. Verify this worktree, branch, T8 diagnostic commit `d10f33e`, audit successor,
   installed marker/hash, and current working-tree status. The intentional
   `AGENTS.md` amendment is now committed, not expected working-tree residue.
   T8 was installed from this exact experimental worktree, not the canonical
   or obsolete checkout. No GitHub push/PR update was made in this session.
2. Follow the shared architectural directive in `TASK-OWNERSHIP.md`, not the
   obsolete restriction to one recall micro-fix. Add missing owner acquire /
   release / explicit preemption and worker command-boundary telemetry before
   assigning WORK packets to a native mechanism. Distinguish direct script
   selection, persistent native builder/economy delegation and autonomous
   native tasking with a controlled engine comparison. Preserve search state;
   record exact commanded members where available and expose any trace quota
   exhaustion. Untagged packets without complete coverage prove no caller.
   T8 can identify its six recall sources in a supplied replay, but cannot by
   itself settle every worker/native boundary. Do not request a long T8 run
   while implying that it contains the missing coverage.
   Once the mechanism is established, implement the common selection/command
   permission contract, explicit emergency ownership transfer, bounded routine
   defense and persistent first-TC allied-help anchors. Add all nine section-H
   contracts and validate every player's preemption/boarding events in a fresh
   preserved-lobby replay. Keep ownership INVESTIGATING until then.
3. Preserve T6 safe partial assault as CLOSED and T5 candidate screening as
   CLOSED; preserve T7's specific cleanup exclusion as runtime-validated.
   Reject any regression to ordinary P3B44 attacks or successful full/partial/
   relic lift behavior. Broader boarding/STOP/passivity causes stay INVESTIGATING.
4. Resume the authorized selective salvage A-C above after ownership recovery,
   preserving recovery attack/transport behavior and stopping
   conflicting items. D is already committed as `9b3dded`; do not backport it
   twice. T8 allocated no new goals; recheck 1163 onward for A-C. This runtime
   work is pending, not canceled or explicitly deferred by the user.
5. Separately investigate and implement `sn-dock-placement-mode`,
   `sn-minimum-water-body-size-for-dock`, and `sn-dock-proximity-factor` for
   opposite island shores and open ship approaches. Verify their semantics and
   placement outcomes; do not assume parameter values guarantee geometry.
6. Retain the already ROOT-CAUSE-PROVEN premature global-pending drop-site
   transition for its own later patch, outside salvage and Port tuning. Keep
   resource-wait, stale-time boarding, exploration overrides, military stalls,
   escort overlap and recovery-unload repetition distinct.
7. Yellow's T6 22-24-minute interrupted hunt still needs a causal audit. The
   new WORK decoder may now assist, but was verified on T7 packets; confirm T6
   layout and associate hunt targets/state before using it as hunt evidence.
   No guessed hunting fix is included.
8. Keep broader command-volume/crash and transport micro-fixes outside the
   current directive. Friendly-fire rejection is in scope specifically for
   verified-threat preemption; preserve the separate P3B44D1 evidence/control
   without folding in unrelated targeting or navigation changes.
