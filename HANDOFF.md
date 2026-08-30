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

- Marker: `RAWAI-P3B44T6:447`.
- Runtime files: 68.
- Source and installed target SHA-256:
  `D5A2314E461603F68D5327E71BD7FB3737F0518C8969F2D5A4C45809B11598EB`.
- Deployment check: all 68 runtime files are byte-identical, with no missing,
  different, or unexpected runtime files. Relative to P3B44T5, exactly
  `rawai-customconstants.per`, `rawai-init-goals.per`, and
  `rawai-military.per` were copied.

## Current objective and preserved behavior

P3B44T5 migration landing-candidate screening remains runtime-accepted and
CLOSED. The current objective is the newer queued-passenger defect. P3B44T5
proves that a selected passenger can remain outside a Transport while repeated
garrison commands continue, and the user directly observed that manually
loading such passengers caused routes to start. P3B44T6 fixes the proven
downstream exact-full assault abort and instruments the still-unknown upstream
nonboarding cause. Status is FIXED-PENDING-RUNTIME for safe partial assault
departure and INVESTIGATING for why an individual queued passenger does not
board. Purple's proven drop-site race remains the next separate transport
patch after this runtime experiment.

P3B44 Gray/Blue combined attacks are the known-good behavior at regression
risk. This patch must preserve ordinary land attack dispatch, superiority,
timing, target selection, home defense, escalation, and every non-transport
attack owner. Do not backport P3B46-P3B50 attack changes into this branch.

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

- **Status:** FIXED-PENDING-RUNTIME for the exact-full assault route gate;
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
  distance from the embarkation hull point, land zone, controller group flag,
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
- **Latest result / next action:** deterministic and structural validation is
  PASS and the byte-verified P3B44T6 runtime is installed. Runtime behavior is
  not yet demonstrated. Obtain one fresh preserved-lobby replay, audit every
  reconstructable assault and migration boarding lifecycle across all players,
  and keep the upstream passenger defect open until that evidence supports a
  causal fix.

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
- Full P3B44-derived regression suite: PASS (118 tests).
- PER structural/operand validation: PASS.
- Naval-doctrine validation: PASS.
- Strategy execution: PASS (1,156 total matchups; 1,149 historical and 1,152
  Extreme matchups with adjustments).
- ODS workbook round trip: PASS (34 civilizations, 680 unit-evidence rows, 340
  naval-class rows).
- Replay benchmarks: PASS (27 entries).
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
- Fresh P3B44T6 engine/replay acceptance: PENDING. Do not close safe partial
  departure or assert the upstream nonboarding cause from structural tests.

## Exact next actions

1. Verify this worktree's branch, P3B44T6 behavior commit `14fd09c`, installed
   marker/hash, handoff successor, and only expected user-owned `AGENTS.md`
   dirt against this document. Do not deploy from the canonical or obsolete
   snapshot; P3B44T6 is already installed from this exact transport worktree.
2. Run one fresh match with the preserved lobby. Audit every reconstructable
   assault and migration boarding lifecycle across all players, not only the
   user's visible event. Correlate candidate action/target/command/move fields,
   exact hull terminal occupancy, partial departure, route start, landing, and
   passenger membership.
3. Mark safe partial assault CLOSED only if a five-to-nine exact load begins the
   screened route and remote orders exclude shore stragglers while below-five
   loads retain bounded recovery. Keep the upstream passenger cause
   INVESTIGATING until the new candidate evidence proves the first divergence.
4. Preserve P3B44T5 migration landing screening as CLOSED. P3B44T6 adds
   diagnostics but intentionally does not change migration thresholds or route
   behavior.
5. After the P3B44T6 runtime result, implement Purple's ROOT-CAUSE-PROVEN
   premature global-pending drop-site transition as the next isolated
   transport patch. Keep Orange and the late Red resource-wait failures
   distinct pending their own first-blocker evidence.
6. Keep migration escort overlap, recovery-unload repetition, dominant command
   volume, crash work, P3B44D1 friendly fire, and all non-transport defects out
   of this causal patch unless the user explicitly redirects the experiment.
