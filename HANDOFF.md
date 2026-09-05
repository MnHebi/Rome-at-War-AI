# Rome at War AI handoff

## CURRENT — T42:490 SHIPYARD PROBE RECOVERY, SOURCE ONLY, 2026-09-05

- **Canonical workspace:** `G:\Projects\Codex\Rome at War AI\.trade-work\T30-trade-cap-civ-fix`;
  branch `fix/trade-cog-cap-dacian`. Runtime/source commit `280ae40`; this
  handoff-only commit follows it. No branch/worktree/clone was created.
- **Shipyard zero/one stagnation — ROOT-CAUSE-PROVEN /
  FIXED-PENDING-RUNTIME.** The user observed most long-Imperial players at one
  Shipyard and Green at zero despite ample wood. The T40 resolver made every
  admitted candidate depend on a warship, Transport, or fishing ship within 64
  tiles. This circularly blocked the first yard, blocked later yards after the
  fleet sailed away, and excluded active Trade Cogs as valid mobile probes.
- **Bounded correction:** mobile discovery now covers the supported 255-tile
  standard-map radius and includes Trade Cogs. If no probe exists, only the
  already-admitted first/second yard can continue, retaining buildability,
  separation, worker path, affordability/escrow, pending-placement, foundation,
  completion, and failed-site checks. Third/later yards still require four exact
  mobile-water path probes. Diagnostic 410 reason 8 identifies no mobile probe
  after minimum capacity.
- **Validation PASS:** the pre-fix executable fixture reproduced all three
  no-build cases. Fourteen post-fix Shipyard fixtures cover zero/one recovery,
  distant Trade Cog validation, and the later-yard proof boundary. Generated
  synchronization and PER validation pass; full Python 3.12 discovery is
  508/508; `git diff --check` passes.
- **Deployment:** not deployed. The installed test copy remains exact T41:489,
  aggregate SHA-256
  `AB2271FA659CC47F6471CA950006FF73F986918D71057C12DD90BED099A858F2`.
  T42 marker `RAWAI-P3B44T42:490` is reserved in source. Full cause, boundary,
  tests, and runtime acceptance: `T42-SHIPYARD-PROBE-RECOVERY.md`.
- **Next action:** when authorized, deploy T42 from this checkout and verify the
  marker/hash. A fresh replay must show first yards and persistent second-yard
  deficits becoming concrete completed foundations, while later yards retain
  coast quality. Current T40 naval right-of-way and expeditionary objectives
  remain FIXED-PENDING-RUNTIME.

## T41:489 PARSE RECOVERY — DEPLOYED, 2026-09-05

- **Canonical workspace:** `G:\Projects\Codex\Rome at War AI\.trade-work\T30-trade-cap-civ-fix`;
  branch `fix/trade-cog-cap-dacian`. Runtime commit `31d86f5`; this handoff-only
  commit follows it. The worktree was clean before the reported regression and
  no branch/worktree/clone was created.
- **Release blocker — FIXED-PENDING-RUNTIME.** The first T40 launch emitted
  `rawai-military.per`, line 1620, `ERR2005: Invalid Identifier`. The source
  cause is four T39 predicates that called project goal `villager-count` as if
  it were an engine fact. All four now use `up-compare-goal`; the first bad
  expression was line 1620 and the other three would have failed after it.
- **Regression prevention:** the PER domain validator now identifies writable
  goal storage from `set-goal`, `up-modify-goal`, `up-get-fact`, and
  `up-get-player-fact` destinations and rejects bare fact-call syntax for those
  identifiers. It explicitly accepts the correct `up-compare-goal` form.
- **Validation PASS:** empty PER report; 128 validator, 23 migration, 3
  transport-lane, and 27 ownership tests; full Python 3.12 discovery 505/505;
  `git diff --check`.
- **Deployment identity:** 99 source/installed files, marker
  `RAWAI-P3B44T41:489`, aggregate SHA-256
  `AB2271FA659CC47F6471CA950006FF73F986918D71057C12DD90BED099A858F2`.
  The repair copied only `rawai-init-goals.per` and `rawai-military.per`.
  Independent postcheck reports zero missing/different/unexpected files; the
  installed marker-file SHA-256 is
  `926867FBC56C1312473934F906AAD251BAD2258E66F944AF97D3AB4359D9A5E8`.
- **Next action:** start a fresh match and require visible `T41:489` with no
  `ERR2005` before closing the parser regression. T40 gameplay objectives remain
  FIXED-PENDING-RUNTIME and should then be tested normally. Full detail:
  `T41-PARSE-RECOVERY.md`.

## T40:488 NAVAL HARDENING — SUPERSEDED DEPLOYMENT, 2026-09-05

- **Canonical workspace:** `G:\Projects\Codex\Rome at War AI\.trade-work\T30-trade-cap-civ-fix`;
  branch `fix/trade-cog-cap-dacian`. This is the explicit current user authority;
  repository `AGENTS.md` now agrees. No branch/worktree/clone was created and no
  obsolete extracted copy was synchronized. Start was clean `4d9c519`; latest
  behavioral HEAD `2c46488` (the documentation/marker commit follows it).
- **Objective:** the requested three naval/overseas improvements are implemented,
  statically validated, and deployed after the user's explicit authorization;
  fresh-match acceptance remains open. Full causes, file/commit map, focused tests,
  adversarial findings and acceptance criteria: `T40-NAVAL-HARDENING.md`.
- **Shipyards — FIXED-PENDING-RUNTIME.** Source allowed first-yard policy but its
  final desired-zero gate could suppress issuance; all later yards waited on
  tech saving. Random newest-building offsets had no open-water quality or
  concrete-foundation confirmation. Preserve first-yard priority, add a 90s
  deficit exception only below minimum operational count two (bounded by desired),
  and retain actual affordability/escrow and ordinary later expansion. A finite
  multi-sector/four-water-point search uses real mobile path queries, own/allied
  naval-building separation and a compatible worker path. Verify foundation then
  completion, with bounded failure memory. Native builder assignment and actual
  usable exits remain engine acceptance boundaries. Commits `f8df20d`, `ac8b606`,
  `2c46488`; 11 focused PER fixtures PASS. Diagnostic 410 is the blocker reason.
- **Merchant right-of-way — FIXED-PENDING-RUNTIME.** Legacy berth/waypoint
  clearers excluded active traders and mid-route straits. The new observer
  requires two stationary eight-second samples with stable live movement intent
  before yielding one nearby free self-owned merchant. It observes Transports
  before mission warships, checks same-zone/exact-path/lateral safety and known
  sea/town defenses, permits at most three sequential fresh interventions with
  remeasurement, holds each at most 32s and three renewals, and applies merchant
  and hull cooldowns. No STOP or priority-hull order; native trade resumes at a
  still-valid allied Dock. Owned/distant traders are untouched. Commits `9c0b3fe`
  and `e4ad548`; 11 focused fixtures PASS, including a five-active-merchant choke.
  Diagnostic 420 names merchant, 421 priority hull. Collision causality and
  trade reacquisition between bounded samples remain runtime questions.
- **Expedition surplus — FIXED-PENDING-RUNTIME.** Fresh admission was blocked by
  aggregate land superiority even for safe isolated homes; three slots already
  release preparation one second after dispatch. Add only a leased safety
  exception plus a same-pass eligible-home-army reserve. Require quiet home,
  known overseas seed, real worker reachability checks, useful navy and hulls.
  Keep minimum 12/one-quarter at EQUAL sea control, minimum 20/half and five-unit
  lift cap at TOLERABLE; retain one free siege specialist and existing Palintonon
  protection. No new planner/slot/cadence/recall. All migration/relic/ownership,
  screening, failed-shore and independent mission gates remain. Commit `3110251`;
  11 focused fixtures PASS. Diagnostic 430 reports exception availability.
  Bounded/visibility-limited search is not complete map-connectivity proof.
- **Validation PASS:** 503/503 Python 3.12 discovery tests, including the
  compiler fixture in its required permitted temporary environment; PER operands
  and structure; ownership 960 sites / zero permission failures; generated
  ownership/mission/plan/migration/coastal/ROW/expedition/naval synchronization;
  strategy execution, naval doctrine, 42 existing replay benchmark definitions
  and diff whitespace. No new replay can yet validate T40.
- **Existing synchronization conflict — DEFERRED, not passed:** civ generator
  still proposes six baseline file updates. In-memory inspection finds four
  newline-only changes and semantic Dacian Bowman / Syracusan Spearman reversions
  conflicting with audited release repairs. No real `--write` was performed and
  those source/config files remain byte-identical to baseline. Repair that
  generator/data alignment separately; do not overwrite the verified choices.
- **Identity/deployment:** source and installed test copy both contain 99 runtime
  files, `RAWAI-P3B44T40:488`, SHA-256
  `C90F78EB90DBA119DA6DC0373B8D9B5A703B3161A0D31267A7F5504409CE22E2`.
  Deployment copied 14 changed/new files from this checkout, including the six
  new T40 modules, with no unexpected files and no remaining mismatch. A second
  independent read-only synchronization check reports zero missing/different/
  unexpected files. The installed marker file SHA-256 is
  `FC2D287ECBFF242DB1EA88DE48CBC7D9A29247A1F8DF19B40E48DFB31FC4C281`.
  Conservative literals 1470/1500; no new engine timers or DUC groups. This
  deployment also advances the test copy from T36 through all pending committed
  T37/T38/T39 fixes; it does not include data-mod or replay files.
- **Next actions:** start a fresh match using the documented Iberia lobby and
  confirm the replay-visible T40:488 marker. Audit every player's
  Shipyard lifecycle, congestion episodes and repeated slot use, including safe
  home reserve, native trade recovery and CPU/late-match lag. Recheck siege
  boarding, land trade, migration/relic and landed combat. Keep broader ordinary
  military inactivity/type-wide native exclusions and shared preparation-lane
  starvation explicit if they remain; do not attribute them all to the repaired
  aggregate-strength gate. Mark CLOSED only after the item-specific runtime PASS.

## CURRENT - T39:487 MIGRATION ADMISSION, LANDED ASSAULT CONTINUATION, AND EARLY GATES, SOURCE ONLY, 2026-09-05

- **Workspace:** `G:\Projects\Codex\Rome at War AI\.trade-work\T30-trade-cap-civ-fix`,
  branch `fix/trade-cog-cap-dacian`; pre-change HEAD `982e496`. The working
  changes are deliberately separated into independently revertible commits:
  `e9053a7` landed visibility handoff, `058991d` crowded-island migration
  admission, `ba2ef5b` first-gate sequencing, and `f1bba96` landed cross-zone
  ownership. T36:484 remains installed while its live test is running; T37,
  T38, and T39 are source-only and must not be injected into that match.
- **Migration admission — FIXED-PENDING-RUNTIME / bounded behavior change.** The
  user directly observed hundreds of villagers waiting on beaches while
  manually loaded Transports still executed migration voyages. The current T36
  replay independently proves the upstream gate failure: Blue had four
  Transports but repeatedly reported `migration gate idle bucket: 0` from
  32:06 through 34:07. At those early samples it had 44–49 villagers, so the new
  high-population policy deliberately does not rewrite that opening behavior.
  At 60 villagers, the migration gate can now admit one bounded manifest even
  when native economy assignments keep the idle fact at zero. Its selector
  protects builders, repairers, grouped/garrisoned units, the boar lurer,
  prey/livestock workers, and all established food roles; it remains capped by
  the exact Transport capacity. The threshold is policy tuning, not a claimed
  engine constant. Runtime PASS requires a high-population/idle-zero island to
  emit an AI-owned passenger candidate and board/depart without manual loading,
  while protected workers remain untouched.
- **Empty landed handoff — ROOT-CAUSE-PROVEN / FIXED-PENDING-RUNTIME.** T36
  repeatedly serialized `RAW3 event 8 -> event 12` only eight displayed seconds
  apart for Blue slots. Eight seconds cannot exhaust the 300-game-second combat
  lease; it is the first combat sample finding an empty group. Source rebuilt
  the mission group in the same sweep that the hull first reported zero cargo,
  when newly unloaded passengers can still be engine-visible as garrisoned.
  The voyage now retains its sealed group for one eight-second sample before
  the landed rebuild, and starts combat on the following bounded sample. The
  executable fixture reproduces cargo-zero-before-passenger-visibility and
  proves all passengers survive the handoff.
- **Landed members crossing engine zones — ROOT-CAUSE-PROVEN /
  FIXED-PENDING-RUNTIME.** Yellow missions reached event 8, survived until the
  full combat lease expired, but emitted zero landed target/issuance records.
  Enemy 7 objective 47510 remained alive and trained units from 49:31 through
  at least 62:42, covering Yellow's first 56:23 handoff and 59:27 release. Thus
  the controller had a nonempty owned group and a live sealed-target-zone
  building, but never passed its local-member selection. That selection removed
  exact mission members as soon as their inland movement crossed away from the
  landing zone. T38 separately proved Iberia's engine zone labels do not denote
  traversable-land boundaries. T39 removes only the zone veto from the exact
  sealed landed manifest; foreign/free troops remain excluded, garrisoned units
  remain excluded, and hostile targets still must be in the sealed target zone.
  Runtime PASS requires Yellow-style landed groups to emit target/issuance and
  continue fighting after crossing a local engine zone boundary.
- **First gate before wall closure — FIXED-PENDING-RUNTIME / requested
  sequencing change.** Both first-gate rules and their availability poll were
  gated on 25% wall completion, allowing a perimeter to close before a gate was
  requested. The first stone or palisade gate is now requested as soon as
  `can-build-gate-with-escrow 2` reports a replaceable wall span. The second
  gate remains at 75%; all danger, worker, escrow, availability and retry bounds
  remain unchanged. Runtime PASS requires the first viable gate to precede a
  closed perimeter without preventing wall completion.
- **Broader army idleness remains INVESTIGATING.** T39 fixes both source-visible
  landed-group first divergences; it does not claim that every ordinary army
  idle episode shares those causes. Native attack protection is type-wide and
  the T36 replay has substantial writer-91 exclusion activity, so free soldiers
  sharing a type with a protected mission can wait. Removing that shield would
  let native attack ownership steal active mission members and is not supported
  without a discriminating replay. If ordinary unlanded armies remain idle in
  T39, correlate their exact types with live owner groups and attack dispatch
  gates before changing that protection.
- **Validation PASS:** assault generation synchronization; 44 focused landed /
  mission / historical-fingerprint tests; migration and wall focused tests;
  PER validation; ownership audit 842 sites with zero permission failures; and
  `git diff --check`. Full discovery passes all 470 tests, including the
  compiler fixture in its required permitted temporary environment.
- **Runtime identity/deployment:** source marker `RAWAI-P3B44T39:487`; no new
  replay strings beyond replacing the marker. No deployment has occurred;
  installed runtime remains verified T36:484.

## CURRENT - T38:486 LAND TRADE ZONE-VETO REPAIR, SOURCE ONLY, 2026-09-05

- **Workspace:** `G:\Projects\Codex\Rome at War AI\.trade-work\T30-trade-cap-civ-fix`,
  branch `fix/trade-cog-cap-dacian`; pre-change HEAD `84429f5`. T36:484 remains
  installed while its live test is running. T37 and T38 are source-only and
  must not be silently deployed into that match.
- **Status: ROOT-CAUSE-PROVEN / FIXED-PENDING-RUNTIME.** The user directly
  observed that multiple allied players had viable land routes but no land
  trade. A read-only 125:00 snapshot of live T36 replay
  `SP Replay v101.103.48987.0 @2026.09.04 223434.aoe2record` has zero parse
  errors. Blue/P1 built Markets at 14:00 and 39:12; its allied P2, P3 and P4
  had built Markets by 11:45, 13:07 and 14:19 respectively. Despite that, Blue
  emitted no `trade land candidate ally` event and all eight players produced
  zero Trade Carts (engine `trade-cart` ID 128) through 125:00. Water discovery
  and proof remained live, repeatedly identifying allied Dock targets.
- **First causal divergence:** after finding the local and allied Markets, the
  land topology scan removed every Market whose `object-data-map-zone-id` did
  not equal the chosen home/colony zone. That is the only remote-Market veto
  before the land-candidate event. The runtime result proves this zone equality
  did not represent the user-visible traversable Cart routes on Iberia, so the
  bounded reachability probe was never admitted. T31 removed the invalid path
  query against an immobile Market but retained this second invalid pre-proof
  gate.
- **Implementation:** remove only the local and remote land Market map-zone
  filters. A completed own Market and a living ally's completed Market now
  create a candidate irrespective of their engine zone labels. The existing
  limit of at most three candidate-only Trade Carts remains the actual bounded
  path experiment. Normal Cart growth, the larger growth limit and villager
  retirement still require a live Cart with `actionid-trade`; an unreachable
  candidate therefore cannot unlock full trade. Water candidate filtering,
  proof and growth are unchanged.
- **Preserved contracts:** per-ally masks; independent land/water discovery;
  completed producer census and producer-epoch invalidation; three-Cart probe
  ceiling; live target-player proof; `wait-techup-requirements`; `can-train`;
  desired/growth caps; water same-zone candidacy; and all transport, economy,
  military and naval controllers.
- **Validation PASS:** focused trade topology 8/8; general validators 126/126;
  full Python discovery 468/468 (the first sandboxed compiler-fixture run hit
  the established temporary-directory permission boundary; the approved full
  rerun passed); PER validation; naval doctrine; ownership audit 841 sites with
  zero permission failures; and `git diff --check`.
- **Runtime acceptance:** in a fresh T38 replay, each AI with its own completed
  Market and at least one allied Market must produce no more than three Cart
  probes until a Cart begins `actionid-trade`; a real traversable route must
  then produce `merchant land proof ally` and unlock bounded normal Cart growth.
  An unreachable cross-zone candidate must stop at three Carts and must not
  unlock growth or villager retirement. Water trade must remain independent.
- **Deployment:** none. Source marker is `RAWAI-P3B44T38:486`; installed runtime
  remains verified T36:484.

## CURRENT - T37:485 INDEPENDENT SIEGE-PASSENGER BOARDING, SOURCE ONLY, 2026-09-04

- **Workspace:** `G:\Projects\Codex\Rome at War AI\.trade-work\T30-trade-cap-civ-fix`,
  branch `fix/trade-cog-cap-dacian`; pre-change HEAD `f72e541`. T36:484 remains
  installed and must not be silently replaced while its live test is running.
- **Status: ROOT-CAUSE-PROVEN / FIXED-PENDING-RUNTIME.** During the T36 test the
  user directly observed a Yellow Pummel stop en route to its assault Transport,
  and repeatedly observed all other siege engines stop when one engine in the
  boarding group was obstructed. The current replay snapshot is
  `SP Replay v101.103.48987.0 @2026.09.04 223434.aoe2record`, duration 62:31,
  with zero parse errors and T36 marker 484.
- **Replay evidence:** Yellow completed two earlier assault landings. Its next
  preparation terminated at 59:22 with only 4/10 aboard while the sampled
  reserved passenger still had action 617/order 717, exact hull target 35963,
  group flag 4, and distance 9. The following preparation sealed 7/10 at 62:30
  while its sampled reserved passenger still had that same valid boarding state
  only distance 2 from hull 35963. No reservation, target, or ownership loss
  explains those simultaneous stops.
- **First causal divergence:** every assault boarding and retry site issued one
  multi-object `action-garrison` command to the entire mixed manifest. Siege
  engines therefore shared a formation-coupled command; one obstructed engine
  could halt its siege peers even though each still retained the right hull
  target and mission group.
- **Implementation:** the six assault boarding/retry sites retain the existing
  group command for non-siege passengers but exclude `siege-weapon-class`.
  During rendezvous/load wait, a bounded ID-sorted round-robin gives exactly one
  reserved, ungarrisoned siege engine its own `action-garrison` command per game
  second. At most ten accepted passengers exist, so every surviving siege
  member is renewed within ten seconds without sharing a formation command.
- **Preserved contracts:** passenger-first manifest selection, nearest eligible
  hull, exact hull and group ownership, 120-second rendezvous lease, 30-second
  local boarding deadline, 5-unit useful-partial threshold, partial/abort
  diagnostics, three dispatched mission slots, all non-siege boarding, and all
  migration behavior are unchanged. No new chat strings were allocated.
- **Validation PASS:** focused rendezvous fixture including two Pummels
  proves independent one-member commands, one-second cadence, and no multi-unit
  siege command; 49 assault preparation/acquisition/ownership tests; 134 marker,
  topology and validator tests; 19 physical-line/task-ownership tests; PER
  validation; ownership audit 841 sites with zero permission failures; and
  `git diff --check`; and full Python 3 discovery, 468/468 tests. The first
  sandboxed discovery exposed one deliberately strict ownership fixture that
  lacked `object-data-class`; the fixture now models the existing infantry
  class field. Its only other error was the established Windows Temp permission
  boundary for the compiler fixture; the permitted full rerun passed.
- **Runtime acceptance:** in a fresh T37 replay, obstruct one reserved siege
  passenger and verify another reserved siege passenger continues and boards;
  there must be no more than one scripted siege boarding renewal per player per
  game-second, no loss of the exact hull/group target, normal non-siege boarding,
  and no regression in departure/landing. Until then this defect is not CLOSED.
- **Deployment:** none. Source marker is `RAWAI-P3B44T37:485`; installed runtime
  remains the verified T36:484 payload.

## CURRENT - T36:484 BOUNDED ASSAULT/MIGRATION SHORELINE RESOLUTION, DEPLOYED, 2026-09-04

- **Workspace:** `G:\Projects\Codex\Rome at War AI\.trade-work\T30-trade-cap-civ-fix`,
  branch `fix/trade-cog-cap-dacian`; pre-change HEAD `a378710`. The active HEAD
  is the T36 commit containing this entry. Do not create a parallel worktree or
  deploy from another checkout.
- **Status: ROOT-CAUSE-PROVEN / FIXED-PENDING-RUNTIME.** T33 replay
  `SP Replay v101.103.48987.0 @2026.09.04 151001.aoe2record` proved that assault
  hulls repeatedly received inland corridor `(155,108)` and unload `(86,61)`
  geometry before dispatch. Three completed missions followed event
  `0 -> 4 -> 9`, a fourth was still repeating that route at replay end, and no
  assault landed. The six migration voyages likewise rejected all 30 resource
  anchor/plus-or-minus-two candidates. No native hull overwrite or global
  target change preceded these failures.
- **First causal divergence:** assault offset the inland enemy-objective point,
  while migration tested the inland resource anchor and four adjacent points.
  Neither planner searched for the land/water boundary. T34's exact-hull
  reasons 36/37 could reject the resulting geometry, but could not generate a
  usable coast.
- **Implementation:** the shared generator model marches from the inland anchor
  toward the exact reserved Transport in at most 24 sixteen-tile steps, detects
  the first departure from the target map zone with `up-get-point-zone`, and
  refines the bracket in at most four four-tile steps. It then probes a five
  sector fan (`0`, `+/-8`, `+/-16`) with `up-cross-tiles`. A sector is eligible
  only when its land point remains in the objective/resource zone, its water
  point is a different valid zone, the sector is not in bounded failure memory,
  and both stored exact-hull path queries are finite. No terrain IDs or map
  coordinates are hardcoded.
- **PER primitives:** `up-get-point`, `up-bound-point`, `up-lerp-tiles`,
  `up-get-point-zone`, `up-cross-tiles`, `up-set-target-object`,
  `up-get-path-distance`, and the existing final `up-path-distance` gates.
  Cached AIRef semantics were checked before implementation: interpolation
  mutates its first point toward the second; point-zone writes the queried map
  zone; exact-hull path distance returns `65535` when unavailable, with option
  1 requiring the exact water point and option 0 accepting the legal nearby
  unload vicinity.
- **Sharing/ownership:** `tools/shoreline_resolver.py` supplies the common
  mechanical geometry and constants. Assault remains generated in
  `rawai-assault-plans.per`; migration has its own generated
  `rawai-migration-shoreline.per`. Their goals/state are intentionally separate
  (`gl-ap-*` versus `gl-msr-*`), so migration cannot corrupt preparation or any
  of the three dispatched assault slots.
- **Hard budget:** per objective/anchor, at most 24 coarse zone samples, four
  refinement samples, five candidate zone-pair checks, and ten resolver path
  queries (two per eligible sector). Failure-memory skips occur before path
  queries. A successful assault candidate can then consume the unchanged T34
  final path gate; migration likewise retains its final exact-hull landing
  gate. Exhaustion is terminal for that bounded objective/zone attempt and
  retains cargo for existing replan/recovery behavior.
- **Corridors:** assault and migration lateral corridors now derive from the
  selected water-side shoreline point, not the inland objective. The direct
  midpoint remains a danger sample. If an arbitrary lateral midpoint is
  unreachable, the exact validated water approach is rechecked and may be used
  only when that direct danger sample is clear. T34 reasons 36/37 and final
  exact-hull validation remain mandatory; danger screening is not weakened.
- **Failure memory:** failed assault sectors use the existing enemy/objective
  memory and rotation. Migration now has a separate four-entry, 300-second
  shoreline-sector ring. Wrong-zone, final path rejection, and post-arrival
  failure remember the sector and advance the fan instead of regenerating the
  old inland candidates.
- **Preserved contracts:** full and accepted-partial manifests, three private
  assault slots, hull/passenger ownership, same-landmass checks, opponent and
  objective rotation, Scout screening/fallback, positive-danger vetoes,
  voyage/congestion watchdogs, migration resource-anchor meaning and final
  dropsite flow, relic ferrying, trade, ordinary military/naval behavior, T34
  reasons 36/37, and T35 mode-2 native Watch-Tower garrison suppression.
- **Validation PASS:** 45 focused shoreline/planner tests; 165 current
  assault/transport/migration tests; generated assault/migration synchronization;
  PER structural/operand validation; 840-site ownership source audit with zero
  permission failures plus 40 ownership tests; all 1,156 strategy matchups;
  naval doctrine and generated naval sync; 42 replay benchmarks;
  `git diff --check`; and full Python 3 discovery, 467/467 tests. The full run's
  compiler fixture required its established Windows Temp permission. Fixtures
  model state/geometry and supplied path answers; they are not AoE2 engine
  pathfinding proof.
- **Runtime/string/deployment:** marker is
  `RAWAI-P3B44T36:484`. This patch allocates no new replay-chat strings beyond
  replacing the marker; the conservative project budget is 1,485/1,500 PER
  literals. On explicit user request, `tools/sync_test_ai.py --apply` deployed
  T35+T36 from source commit `5b42491573277f163828e235194a8d836bf8876e` to
  `C:\Users\LostSoul\Games\Age of Empires 2 DE\76561198053747760\mods\local\Rome at War AI\resources\_common\ai`.
  Exactly seven pending files were copied: `rawai-assault-plan-defs.per`,
  `rawai-assault-plans.per`, `rawai-customconstants.per`,
  `rawai-init-goals.per`, `rawai-migration-shoreline.per`,
  `rawai-military.per`, and T35's `rawai-sn-defines.per`. A post-apply read-only
  check proves all 93 runtime files byte-identical, with no missing, different,
  or unexpected files. Source/install aggregate SHA-256 is
  `4E18B8AA59FBD5FD6468242E15DE207209A259C3F8BB08D8CB71EA29BEF87857`;
  installed marker is T36:484 and installed `sn-disable-villager-garrison` is 2.
- **Fresh replay acceptance:** use an authoritative fresh replay. PASS requires
  old inland/cliff routes rejected before dispatch, a materially different valid
  shore selected, at least one successful loaded assault landing, migration
  reaching shoreline beyond its former five local candidates where topology
  permits, no unsafe route admitted to force success, and no
  T34/T35/manifest/ownership regression. Until then:
  **SHORELINE RESOLVER IMPLEMENTED — FIXED-PENDING-RUNTIME**.

## CURRENT - T35:483 NATIVE VILLAGER WATCH-TOWER GARRISON SUPPRESSION, DEPLOYED WITH T36, 2026-09-04

- **Workspace:** `G:\Projects\Codex\Rome at War AI\.trade-work\T30-trade-cap-civ-fix`,
  branch `fix/trade-cog-cap-dacian`; starting HEAD `a9d000c`. The pre-existing
  uncommitted `HANDOFF.md` update records the completed T34 deployment and T33
  replay flood audit below.
- **ROOT-CAUSE-PROVEN / FIXED-PENDING-RUNTIME:** T33 replay classification
  proves that the dominant 13-ms Villager-to-drop-site `ORDER` flood is exactly
  bracketed by engine-native Watch Tower garrison/ungarrison episodes. No PER
  garrison writer targets a Watch Tower, and the explicit economic-building
  writers cannot emit that relationship at simulation-frame cadence.
- **Mode semantics:** cached AIRef
  `.analysis\airef-reference-20260830.js` documents strategic number 291 as a
  four-mode value: 0 normal; 1 ignores Gaia but permits any enemy-triggered
  garrison; 2 ignores Gaia and permits enemy-triggered garrison only when a
  Town Center can be entered; 3 disables all native Villager auto-garrison.
  Mode 2 is the narrow causal boundary: it excludes native Watch Tower refuge
  while retaining native TC assistance and therefore has less worker-survival
  risk than mode 3.
- **Implementation:** `rawai-sn-defines.per` sets
  `sn-disable-villager-garrison` to 2 once in the existing global one-shot
  initialization rule. No economy percentage, worker tasking, defense
  threshold, tower, Transport, or explicit `action-garrison` rule changed.
  T35's behavior is retained unchanged under the superseding local T36:484
  marker recorded above.
- **Non-regression contracts:** new
  `tools/test_villager_garrison_mode.py` proves mode 2 is the only writer and is
  one-shot, and proves that boar-rescue TC garrison, wall/gate-builder TC
  evacuation, migration Transport boarding, and assault Transport boarding
  remain in source. Existing executable migration and assault rendezvous tests
  still prove their exact `action-garrison` commands.
- **Validation PASS:** `tools/validate_per.py`; 13 focused native-garrison,
  assault-rendezvous, and migration-rendezvous tests; full 457-test discovery
  suite. The writer-trace case required its established unsandboxed temporary
  directory permission and passed there. `git diff --check` passes.
- **Deployment:** now deployed with T36:484 on explicit user request. The
  installed 93-file runtime and aggregate SHA-256 are recorded in the T36
  section above.
- **Strict runtime acceptance:** PASS requires no large 13-ms
  Villager-to-TC/Mill/Lumber Camp streams; no corresponding native Watch Tower
  garrison episodes; healthy ordinary gathering/deposit; working explicit TC
  safety garrison, boar rescue, wall/gate-builder evacuation, assault boarding,
  and migration boarding; and no new worker death/passivity regression under
  attack. Until a fresh deployed replay proves every item, status remains
  FIXED-PENDING-RUNTIME.

## CURRENT - T34:482 ASSAULT SHIP-PATH GEOMETRY GATE, DEPLOYED, 2026-09-04

- **Workspace:** `G:\Projects\Codex\Rome at War AI\.trade-work\T30-trade-cap-civ-fix`,
  branch `fix/trade-cog-cap-dacian`; current HEAD `a9d000c` was clean before and
  after deployment. T33 commit `1460d58` remains the runtime represented by the
  replay audited below; T34 commit `a9d000c` is the current installed runtime.
- **ROOT-CAUSE-PROVEN / FIXED-PENDING-RUNTIME:** replay `SP Replay
  v101.103.48987.0 @2026.09.04 151001.aoe2record` (SHA-256
  `E96FCBDEBF84E000054F0A47E6A954AE27AA3D1DBBF7F717C92997DCF8150DE0`)
  records Blue hulls 37482 and 35604 following the same private assault route,
  failing the outbound progress watchdog and then emptying only during recovery.
  Hull 37482 was commanded to corridor `(155,108)` at 41:01, unload `(86,61)`
  at 41:57, recovery `(184,186)` at 43:41, and terminated event 9 at 45:25.
  Hull 35604 repeated those points at 44:01, 44:57, 46:41 and 48:41. There is
  no native `AI_ORDER` overwrite for either Blue hull in those intervals.
- **Replay-wide lifecycle sweep:** all three admitted assaults with enough
  remaining replay time to terminate failed identically: Green hull 36678
  (enemy 8) emitted event 0 at 39:51, event 4 at 42:07 and event 9 at 42:39;
  Blue hull 37482 (enemy 7) emitted 0/4/9 at 41:01/43:41/45:25; Blue hull
  35604 (enemy 7) emitted 0/4/9 at 44:01/46:41/48:41. Blue hull 36264 was
  admitted at 46:54 and was still attempting the same `(155,108)` -> `(86,61)`
  route when the replay ended at 49:15. Thus the recording contains zero
  successful assault landings and three reproducible outbound-progress aborts;
  it is not merely the two user-observed Blue episodes.
- **First causal divergence:** the planner derived landing candidates from the
  enemy objective's land coordinate and perpendicular offsets; the corridor
  controller derived another geometric point, but neither proved that the
  selected Transport could path to those points. The decoded map proves Blue's
  corridor center is terrain 0 (land/grass) and its unload center is terrain 3
  (land; no water in the 7x7 sample). Green's only admitted mission likewise
  used a terrain-12 unload point and ended event 4 -> event 9. Native ship
  projection toward a nearby shore therefore occurred only after mission
  admission and could select a cliff-side dead end instead of the observed
  clear beach.
- **Implementation:** new state `AP-PATH` rebuilds the exact selected, owned,
  `attack-transport-group` hull after corridor construction. It requires a
  finite `up-path-distance` to the unload vicinity with option 0 and to the
  exact corridor waypoint with option 1 before screening or dispatch. Failure
  reason 36 means unload vicinity unreachable; 37 means exact corridor
  unreachable. Either records the failed approach and returns to the existing
  bounded approach -> objective -> enemy search with the accepted cargo still
  aboard. Existing logs expose the reason without allocating new strings.
- **Preserved behavior / non-regression criterion:** safe full and accepted
  partial manifests, same-island zone validation, defense vetoes, Scout
  screening and fallback, three private mission slots, positive-danger policy,
  and the event-4 voyage watchdog are unchanged. A reachable candidate must
  still depart; an unreachable point must choose another bounded candidate
  without unloading or changing the accepted manifest.
- **PASS:** generated planner/source synchronization; 32 planner/landing tests;
  132 assault/transport/landed-combat tests; PER structure; strategy execution;
  naval doctrine; generated naval synchronization; `git diff --check`.
  Repository run passed 453/454 in the sandbox; the sole Windows Temp
  writer-trace permission case passed separately with Temp access, covering all
  454 tests. Current project string allocation is 1489/1500 literals; this
  patch adds no runtime strings.
- **Runtime deployment:** explicitly deployed from commit `a9d000c` with
  `tools/sync_test_ai.py --apply`. Exactly four installed files changed:
  `rawai-assault-plan-defs.per`, `rawai-assault-plans.per`,
  `rawai-init-goals.per`, and `rawai-military.per`. An independent read-only
  check proves all 92 runtime files byte-identical with zero missing, different,
  or unexpected files. Source/installed aggregate SHA-256 is
  `55454FF4A19BC79EE4653366EE102CCE28ABD8BD577820491F009E324E97F70D`;
  installed marker is `RAWAI-P3B44T34:482`.
- **Runtime acceptance:** run a fresh Huge Iberia match under the recorded T33
  lobby settings. PASS requires reasons 36/37 to reject land/cliff geometry
  before hull dispatch, another approach/objective/enemy to be tried while
  cargo remains loaded, and at least one finite-path route to preserve normal
  dispatch. Runtime acceptance is pending in the user's fresh T34 match. The
  attached replay marker is T33:481, so this recording cannot establish whether
  deployed T34:482 rejects these routes or still admits them.
- **Diagnostics:** decoded replay products and route rendering are outside the
  repository under `G:\Projects\Codex\Rome at War AI\.analysis\T33-iberia-*`.
  The native first-writer/heap-corruption investigation remains open and is not
  claimed fixed by this independent transport patch.

## CURRENT - T33 REPLAY ECONOMIC ORDER FLOOD CLASSIFICATION, 2026-09-04

- **ROOT-CAUSE-PROVEN / FIX NOT IMPLEMENTED:** the dominant flood is not STOP
  and not landed-assault combat. It is an engine-native conflict involving
  garrisoned Villagers and their economic return-to-drop-site task. The five
  named targets account for 37,150 of 43,130 replay `ORDER` packets (86.1%).
- **Actor classification:** initial objects 7774 (Green/player 3) and 7784
  (Purple/player 6) are replay-header object type 293, class 70: Villagers.
  Dynamic objects 34920 and 34717 (Gray/player 7) and 34713 (Green/player 3)
  repeatedly issue `BUILD` and `WORK`, positively identifying the Villager
  class; the action stream cannot recover their runtime male/female variant.
- **Target classification:** 34898 is Gray's Mill at `(117,39)`, created by the
  type-68 build at 05:07; 7712 is Green's starting type-109 Town Center at
  `(166,77)`; 7739 is Purple's starting type-109 Town Center at `(28,120)`;
  35056 is Purple's type-562 Lumber Camp at `(39,118)`, created by the 07:44
  build; and 34725 is Gray's type-562 Lumber Camp at `(124,36)`, created by the
  00:32 build. Every actor and target in these tuples has the same owner.
- **Exact packet classification:** all repeated packets are enum `ORDER`, action
  opcode 0, with one selected Villager, the friendly building instance as
  `target_id`, and the building's exact center coordinate. The hidden six-byte
  field is identically `00000100ffff`. Unlike `SPECIAL` and `AI_ORDER`, this
  packet format serializes no finer `order_id`; the exact replay-level subtype
  is therefore generic object interaction. The Villager/drop-site relationship
  and interleaved `WORK` packets identify economic return/deposit behavior, not
  STOP, WORK, repair, guard, attack, or transport boarding.
- **Causal lifecycle:** the main 34920 -> 34898 and 34717 -> 34898 bursts contain
  5,161 and 4,934 byte-identical packets, median interval 13 ms, while Gray's
  Villagers are under `SPECIAL` order 5 (garrison) to type-79 Watch Tower 35099;
  both runs end exactly at the 39:19.485 `UNGARRISON`. Purple's equivalent runs
  use Watch Tower 35098 and end at the 33:17.062/34:19.311 ungarrisons. Green's
  runs use Watch Tower 35111 and end at 41:35.822/42:40.705/46:37.543
  ungarrisons. Order-5 is the replay's explicit garrison subtype.
- **Source-first writer audit:** no PER garrison writer targets a Watch Tower.
  Existing explicit garrison writers target a Transport Ship or a bounded Town
  Center (boar rescue and perimeter wall/gate-builder evacuation). The only
  `action-default` Villager writers capable of targeting an economic building
  are bounded pending-foundation/colony/migration taskers: colony Town Center
  assignment exits to a 180-second timer, Lumber Camp assignment targets the
  new pending foundation and exits to a 90-second timer, and migration drop-site
  assignment is restricted to `migration-boarding-group`. Purple and Gray emit
  no migration telemetry; Green's large flood episodes occur after its observed
  migration attempt has terminated. Farm staffing targets Farms/resources, not
  drop sites. These rules cannot produce the ready-drop-site relation at 13 ms.
- **Source-visible native boundary:** `sn-disable-villager-garrison` is mapped
  as strategic number 291 in `rawai-constants.per` but is never set by this AI.
  Native Villager garrison therefore remains the only source-visible owner
  compatible with the Watch Tower commands and exact garrison/ungarrison flood
  bracket. Writer IDs 90/91 in the replay are unrelated native attack-group
  exclusion maintenance; positive counts there do not attribute an `ORDER`.
- **Next causal patch:** test the smallest native-garrison suppression at that
  boundary as its own revertible change. Before deployment, preserve explicit
  boar-rescue, wall/gate evacuation, migration and assault boarding as
  non-regression criteria; runtime acceptance requires eliminating the
  garrison-bracketed 13-ms drop-site floods without preventing commanded
  Transport/Town Center garrison. Do not mix this with transport-route changes.
- **Diagnostics:** the replay and parsed products remain outside Git under
  `G:\Projects\Codex\Rome at War AI\.analysis\T33-iberia-*`. This audit changed
  no gameplay source and did not redeploy after the user's T34 match began.

## CURRENT - T33:481 LANDED-COMMAND ISSUANCE TRACE DEPLOYED, 2026-09-04

- **Workspace:** `G:\Projects\Codex\Rome at War AI\.trade-work\T30-trade-cap-civ-fix`,
  branch `fix/trade-cog-cap-dacian`; T32 commit `a84360a` is the immediate
  behavioral baseline. T33 source commit `1460d58` is diagnostic-only.
- **REPLAY RESULT:** in the 73:38 replay `SP Replay v101.103.48987.0
  @2026.09.03 114314.aoe2record`, every terminal ORDER for object IDs 35259,
  42698 and 59295 has `player_id: 3`, which is visible Green. IDs 35259 and
  59295 are positively Villagers because the replay records them issuing BUILD
  actions earlier (17:59/33:06 and 64:58 respectively). ID 42698's concrete
  unit type is not serialized; it was explicitly ungarrisoned at 69:50.
- The replay does **not** serialize current DUC group flags or controller/slot
  ownership. Green emits no `RAW3`/landed-assault lifecycle chat anywhere in
  this recording, so none of the three IDs can be proven to belong to assault
  slot 1, 2 or 3. Preserve player ownership and controller ownership as
  separate conclusions.
- **Terminal pattern:** 42698 begins repeated orders against target 62438 at
  73:36; 35259 joins at 73:37; 59295 joins at 73:38. Their terminal counts are
  37, 21 and 7 respectively. The growing actor set is consistent with native
  ORDER expansion/reacquisition but is not sufficient to prove it rather than
  repeated PER issuance.
- **DIAGNOSTIC ONLY:** immediately before each slot's actual landed
  `up-target-objects` action, the generated controller now emits one
  replay-visible triplet: assault slot, combat target ID, and the current
  pre-increment combat-tries value. It adds no goals, searches, selections,
  commands, timers, ownership changes or gameplay predicates. T32's existing
  post-issue sample-10 latch bounds the triplet to one record per slot per
  logical 16-second combat sample.
- **Acceptance interpretation for the next replay:** one triplet followed by a
  large/mutating packet burst supports native command expansion/reacquisition;
  multiple triplets matching the packet cadence proves multiple PER
  issuances. Correlate by player, slot, target, tries and replay sequence.
- **PASS:** assault tests 108/108; landed-assault tests 11/11; validator tests
  126/126; assault generator synchronization; PER structure; strategy
  execution; naval doctrine; generated naval synchronization; full repository
  suite 451/451 outside the sandbox. Project string budget is 1469/1500
  literals (an allocation guard, not proof of engine compilation). The
  sandboxed full run reached the known
  Windows Temp permission-only writer-trace error after all other tests passed.
- **Runtime deployment:** explicitly deployed from commit `1460d58` with
  `tools/sync_test_ai.py --apply`. Five installed files changed:
  `rawai-assault-mission-defs.per`, `rawai-assault-missions.per`,
  `rawai-economy.per`, `rawai-init-goals.per`, and
  `rawai-unitconstants.per`. An independent post-apply check proves all 92
  runtime files byte-identical with zero missing, different, or unexpected
  files. Source/installed aggregate SHA-256 is
  `E4B6281AEA133A5C56A90CAABB4BDF8F3DD2351B5DAB2DB89635F15EA087E79B`;
  installed marker is `RAWAI-P3B44T33:481`.
- **Fresh T33 test setup (direct user screenshot evidence; replay pending):**
  `RaW data fix`, Chronicles civilization set, Random Map / Iberia, Huge (240),
  Extreme, Standard resources, population 400, Normal speed/reveal, Standard
  starting and ending ages, no treaty, Standard victory. Lock Teams, Team
  Together, Shared Exploration and Record Game are enabled; Team Positions,
  Handicap and all shown advanced variants are disabled. Team 1 is Blue
  Dacians, Red Pontus, Green Seleucids and Yellow Syracusans; Team 2 is Cyan
  Nubians, Purple Numidians, Gray Carthaginians and Orange Egyptians. At 00:01,
  Team 1's shared-exploration minimap shows Green north, Red west/southwest,
  Yellow south and Blue east/southeast. The live chat visibly confirms
  `RAWAI-P3B44T33:481` for players 2-8 with no startup script-error dialog;
  player 1's marker is not visible in the supplied frame and is therefore not
  claimed from screenshot evidence.
- The native first writer and
  `STATUS_HEAP_CORRUPTION (0xc0000374)` remain INVESTIGATING; telemetry is not
  resolution.

## CURRENT - T32:480 LANDED-COMBAT POST-ISSUE LATCH, LOCAL ONLY, 2026-09-04

- **INVESTIGATION RESULT:** the proposed ordinary rule-reentry mechanism is
  not reproduced by the generated state machine. Each slot has one object
  attack-command rule; the next complete rule pass resets its sample to zero,
  and only the 16-second clock gate can reopen combat sampling. No later rule
  re-enters sample 7. `combat-tries >= 3` is not an intra-sample guard: it marks
  the target failed after the third separately sampled command. The observed P3
  subsecond object-order burst could also involve multiple independent assault
  slots converging on one target; source evidence cannot map the reported
  object IDs to mission slots.
- **CANDIDATE MITIGATION / FIXED-PENDING-RUNTIME:** despite that unresolved
  native first writer, the object-command rule no longer leaves itself eligible
  in persistent PER state. Immediately after its one command it changes sample
  7 to post-issue sample 10. The existing third-try `combat-failed` update now
  consumes sample 10, preserving failed-target exclusion. The next full rule
  pass resets the sample normally, and the existing clock deadline still
  permits another command only at the next legitimate 16-second sample.
- The authoritative change is in `tools/generate_assault_missions.py`; all three
  copies in `rawai-assault-missions.per` were regenerated. No transport,
  landing, lease, target-selection, ownership, zone, cadence, or telemetry
  policy changed. A delayed `object-data-action == actionid-attack` is no longer
  relevant to same-sample command eligibility.
- **Regression coverage:** the actual-PER fixture leaves unit action state
  unchanged after issuance, directly reevaluates the command rule four times,
  and proves only one object command. It then proves a later 16-second sample
  can command again. Structural checks require equivalent sample-10 latches and
  third-try transitions for slots 1-3. Existing retarget and failed-target
  fixtures remain green.
- **PASS:** all assault tests 108/108; landed assault 11/11; validator tests
  126/126; PER structure; strategy execution; naval doctrine; generated naval
  synchronization; generator synchronization; full repository suite 451/451
  outside the sandbox. The sandboxed full run passed 450 tests and hit only a
  Windows Temp permission error in the writer-trace fixture.
- **Runtime identity:** source marker `RAWAI-P3B44T32:480`. No deployment was
  performed. Do not claim that this fixes AoE2DE
  `STATUS_HEAP_CORRUPTION (0xc0000374)` without a fresh runtime test/replay;
  rapid duplicate orders correlate with the crash, but the native first writer
  remains unresolved.

## CURRENT - SEA TOWER PHYSICAL IDENTIFIER CORRECTION, LOCAL ONLY, 2026-09-04

- The user-authorized pending `rawai-unitconstants.per` correction changes
  semantic `sea-tower` from 1921 to 1919. Direct inspection of the authoritative
  `empires2_x2_p1.dat` confirms unit 1919 is `STWR` (class 52, type 80), while
  unit 1921 is `PLACEHOLDER2 (WATER)` (class 30, type 20). The generated
  CivTechTrees files expose a stale UI/building alias naming 1921 "Sea Tower";
  runtime searches must use the physical DAT object.
- Every runtime consumer already uses the semantic `sea-tower` constant, so the
  correction applies consistently without editing the assault, screening,
  military or generated landing-plan rules. A regression test now requires
  1919 and rejects 1921. `unique-unit-production.json` records the re-audited
  constants hash and the DAT/export distinction.
- No runtime deployment was performed. The correction was authored under
  `RAWAI-P3B44T31:479`; current source is superseded by T32:480. Runtime
  confirmation of Sea Tower detection remains pending alongside land-trade
  validation.

## CURRENT - T31:479 LAND TRADE CANDIDATE REPAIR, LOCAL ONLY, 2026-09-04

- **Workspace identity:** development was explicitly moved to
  `G:\Projects\Codex\Rome at War AI\.trade-work\T30-trade-cap-civ-fix` on
  branch `fix/trade-cog-cap-dacian`, starting from
  `dc81448571bc4c49d97a3c5574b26c321de209e0`. The pre-existing uncommitted
  `rawai-unitconstants.per` sea-tower identifier change is user-owned and was
  preserved outside this patch.
- **ROOT-CAUSE-PROVEN / FIXED-PENDING-RUNTIME - land candidate rejection:**
  T29 selected the allied remote Market and then used `up-path-distance` to
  test that selected object against the local Market coordinates. A Market is
  immobile, so this was not a valid Trade Cart reachability test. Runtime
  observation found allied land Markets but produced no Cart probes, while the
  independent water branch continued to qualify Docks and produce Merchant
  Ships.
- **Implementation:** all eight land-player candidate rules now accept a
  same-map-zone allied Market without the invalid Market path predicate. The
  matching `65535` rejection rule was removed. The bounded three-Cart probe,
  live `actionid-trade` proof requirement, modality-specific masks/epochs and
  independent water scan are unchanged. This supersedes T29's statement below
  that a finite Market path check was useful candidate evidence.
- **Regression protection:** `tools/test_trade_topology.py` requires eight
  same-zone land candidate rules, rejects reintroduction of the Market path
  test/rejection message, and preserves the no-target advance. The general
  validator enforces the same contract. It also scans source/data inputs for
  the invalid plural `ETHIOPIANS-CIV` symbol and requires the singular
  `ETHIOPIAN-CIV` preprocessor gates. The Ethiopian correction itself was
  already committed in the starting T30 revision `dc81448`.
- **PASS:** trade topology 8/8; validator tests 126/126; release regression
  8/8; release backlog 8/8; pre-backlog 7/7; PER structure; naval doctrine;
  `git diff --check`. The broad mechanical run passed 447 tests and reached one
  environment-only error when the sandbox denied the writer-trace fixture
  access to the Windows user Temp directory. Strategy-execution validation
  reaches the existing manifest provenance guard and fails only because the
  user-owned dirty `rawai-unitconstants.per` no longer matches
  `unique-unit-production.json`; this patch deliberately does not absorb or
  revert that separate change.
- **Runtime identity:** T31 source marker `RAWAI-P3B44T31:479`, now superseded
  locally by T32:480. No test-copy or runtime deployment was performed, per
  explicit instruction. Acceptance
  requires a fresh replay showing same-zone allied Markets create no more than
  three Cart probes until actual `actionid-trade`, after which normal land
  growth may begin; water trade must remain independent.

## CURRENT - T29:477 INDEPENDENT TEAM TRADE TOPOLOGY, 2026-09-02

- **FIXED-PENDING-RUNTIME - land discovery suppressing water trade:** the team
  trade scanner now completes a bounded pass over every living ally for land and
  then every living ally for water. Candidate partner identity is retained in
  P1..P8 bitmasks; a successful land candidate cannot terminate the water pass.
- Same-zone endpoint equality is candidate evidence only. Land candidates also
  require a finite `up-path-distance` from the selected own Market. Water path
  geometry is deliberately not inferred from land path semantics.
- Final permission remains engine execution: normal Trade Cart/Trade Cog growth,
  large-game trade transition and villager retirement require live
  `actionid-trade`. Candidate-only routes can create at most three probes of the
  relevant merchant type. The historical no-candidate aquatic fallback remains
  capped at three Trade Cogs and can become productive only after live trade
  action is observed.
- Market and Dock producer epochs, active counts, growth limits and proof state
  are modality-specific. Water production has no `gl-land-trade-route NO` gate,
  so land and water trade may coexist.
- Proof records the observed target player as a one-bit proof mask; topology
  masks preserve all candidate allies. A topology pass is bounded to eight
  inspected allies per modality even if diplomacy changes during iteration.
- **Static acceptance:** dedicated topology tests plus updated producer-epoch and
  validator contracts; full repository validation still required locally before
  commit. Engine/path semantics and actual mixed land+water trading remain
  runtime-pending.
- **Runtime identity:** `RAWAI-P3B44T29:477`.

## CURRENT ? T28:476 LANDED ASSAULT COMBAT FIX, 2026-09-02

User runtime testing produced at least four independently successful assault
unloads whose landed passengers then remained inert, including troops that did
not react while under attack.

- **FIXED-PENDING-RUNTIME ? landed assault inertia:** state-6 target acquisition
  required an idle, not-under-attack mission member merely to obtain the search
  anchor, and combat/probe commands repeated the same exclusions. A stale MOVE
  or incoming attack could therefore exclude the entire privately owned landed
  manifest from continuation.
- The generated mission controller now accepts any self-owned, ungarrisoned,
  same-zone mission member as the target-search anchor. When a hostile is found,
  stale/moving and under-attack mission members can receive the combat order,
  while units already performing `actionid-attack` are left alone.
- Landed hostile acquisition now includes the established land military classes
  plus Tower, Building and Villager targets instead of only Building/Villager.
- `tools/test_landed_assault.py` covers stale movement, under-attack recovery,
  preservation of already-attacking troops, ownership/zone/garrison guards and
  hostile infantry acquisition.
- The immutable T16A1 fingerprint remains unchanged; its historical normalizer
  strips only this independently tested landed-combat delta before comparison.
- **PASS:** 438/438 regression tests; focused landed assault/mission/screen
  fixtures; generated assault synchronization; PER structural/physical-line,
  naval-doctrine and strategy-execution validation.
- **Runtime identity:** `RAWAI-P3B44T28:476`. Static/deterministic validation does
  not close engine behavior; require a fresh match/replay showing landed assault
  groups autonomously acquiring and fighting hostile units.
- Escort-behind-transport behavior, shore passengers chasing departed hulls and
  intermittent loaded-departure stalls remain separate observations and are not
  claimed fixed by this patch.

## CURRENT — RELEASE BACKPORT CORRECTED, T27 DEPLOYED (2026-09-02)

The explicitly authorized recovery workspace remains
`G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-transport-only`, branch
`recovery/p3b44-transport-only`. Release tip
`ea11d3823467c0b7317ec4c810ca527e0da49e53` is authoritative for runtime
behavior; `8118dd8` remains the auditable first backport, and this follow-up
corrects its stale release decisions in `da83807` (`Align backport behavior
with release authority`).

- **Release corrections:** `rawai-economy.per` now clamps
  `max-hunt-distance` to 28 (food remains 12). The duplicate role-independent
  Falx Warrior, Imitation Legionary, and Roman Empire/Republic baseline
  producers were removed from their civ files. Shared/common production remains
  responsible for the concrete unit families; Dacian/Syracusan, phase,
  progression, homebase/bootstrap, ownership, transport-unload, generator and
  other accepted backports remain intact.
- **Diagnostics retained:** Roman availability/trainability rules retain their
  `up-chat-data-to-self` actions, and the transport/assault/migration/ownership
  telemetry from the transport-only branch remains. Release telemetry stripping
  (`914d5dd`) was not applied to this debug-friendly branch.
- **Tests/validators:** stale hunt-16 recovery assertions were updated to the
  release cap 28. Validator tests now require common concrete Legionary/Falx/
  Imitation paths and reject reintroduced civ-local duplicate producers. The
  strategy validator accepts a bounded shared production path where the release
  architecture moved a family out of a civ file.
- **Validation:** focused release-regression and validator suites, unique/common
  production, civ/phase, transport/generator, PER, strategy-execution and naval
  doctrine checks pass. Full mechanical suite `437/437` PASS (elevated Windows
  rerun); `validate_good_units.py` still reports the pre-existing
  `source_provenance/AI RAW.per_sha256` mismatch. No replay or runtime deployment
  was performed for this source-only correction.
- **Synchronization note:** the read-only `sync_civ_strategies.py` check reports
  six existing civ-file updates would be generated; no `--write` was run, so
  this correction did not overwrite the explicitly audited release-aligned
  source or introduce unrelated generated strategy changes.
- **Runtime deployment:** source and installed test-mod payload `T27:475` contain
  92 runtime files with aggregate SHA-256
  `D4B4E9F4CC5D8DCA0EA77D3DA922459F5D9963FE7802BAD67308E1C8BF5098D6`.
  `tools/sync_test_ai.py --apply` copied only the new marker file after the
  initial source deployment; an independent read-only check reports zero
  missing, different, unexpected, or remaining-mismatched files. The installed
  replay marker is `RAWAI-P3B44T27: 475`.
- **Workspace hygiene:** the pre-existing untracked
  `release_transport_unload.patch` artifact remains untouched. No PR or push was
  made.


## CURRENT — T26:474 DEPLOYED, 2026-09-01

User supplied the T25 replay after ending a 112-minute Britannia stalemate and
reported continued assault aborts, a Red hull boxed by merchants/Transports,
near-shore migration oscillation, partial loads leaving nearby passengers,
an unexplained Yellow Transport and late inert armies. Read
`T26-REPLAY-REVIEW.md` and benchmark
`britain-4v4-20260901-155609-p3b44t25-assault-fairness` before further work.

- **Workspace identity:** the explicitly authorized recovery exception remains
  canonical for this branch:
  `G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-transport-only`;
  Git root is the same path, branch `recovery/p3b44-transport-only`, pre-session
  HEAD `44fbf7e1f8db849641136444f696aa907cef6c43`. Runtime/evidence commit is
  `b6ba6dd8e6d7e9bca80cef17f861b8dce6fef40a`; this HANDOFF commit follows it.
  No checkout/branch switch occurred. The normal project canonical path remains
  `.pr-work\Rome-at-War-AI`; do not copy selected files between checkouts.
- **Replay identity:**
  `SP Replay v101.103.48987.0 @2026.09.01 155609.aoe2record`, SHA-256
  `70003C7FD3CFCA8079CB1FE388AF8B89E385DE461E0CE12FF6FEF6304C5B400E`,
  duration112:09, zero action-stream errors and T25:473 marker. Selected
  colors/resolved teams match the preserved lobby. Replay and `.analysis`
  payloads stay outside Git.
- **Broad all-player audit:**47 command-linked hulls,220 transport samples,38
  assault partial/abort terminals and191 boarding windows. Hull/window/load:
  Red6/55/215, Green3/11/89, Yellow7/17/151, Purple1/1/18, Orange6/33/215,
  Cyan7/15/110, Blue7/15/126, Gray10/44/320. These are command lifecycles, not
  proof that every engine action completed.
- **Runtime control and divergence:** Gray owns31 assaults and confirms23
  landing/combat handoffs; Orange15/6. Red owns9 and confirms zero landings:
  six encounter hostile damage and three reach the90s no-progress terminal.
  Green/Purple publish no assault stage. Yellow accepts five useful loads but
  owns no voyage. The same map can support frequent success, so do not classify
  every failed player as a map-wide pathing failure.
- **FIXED-PENDING-RUNTIME — all-opponent planning:** Yellow's accepted loads
  repeatedly check only three opponents and reason-27 before living Blue.
  Commit `6ce427f` raises the fixed opponent cap3 to the engine maximum7 while
  preserving target validation, danger vetoes, cooldowns and mission deadline.
- **FIXED-PENDING-RUNTIME — local boarding grace:** correct group-4 candidates
  still garrisoning the exact hull at1-4 tiles reach the fixed30s terminal.
  Commit `04ff4ca` grants one12s grace only with exact group/hull/action/order and
  distance<=12. Wrong-hull, retasked and distant members keep original bounds.
- **FIXED-PENDING-RUNTIME — near-waypoint migration:** Red hull38985 improved to
  ten tiles, then oscillated at10/11 until the strict8-tile gate recalled it.
  Commit `84add70` sends only the four-stall <=12 terminal into the existing
  same-zone/path validator; it neither unloads nor weakens geometric vetoes.
- **FIXED-PENDING-RUNTIME — vanished foundation request:** Red's first18-settler
  colony issued Mining Camp point(131,199), then had no pending placement/object,
  worker emergency or foundation. A later voyage reused the identical point and
  completed foundation67503. Commit `a7a6584` revalidates/reissues the exact point
  once only when no live request/object or worker emergency exists.
- **FIXED-PENDING-RUNTIME — idle Trade Cog blockers:** departure clearance did
  not search `trade-cog-class`. Commit `d326f6a` adds merchants to the same
  bounded blocker scan but can move only self-owned, idle, empty, ungrouped,
  safe, same-water-zone ships. Active trade and owned/unsafe ships remain intact.
- **FIXED-PENDING-RUNTIME — shared-lane fairness:** Green forms nine full failed
  migrations after76:06. Its rejected-zone ring works, but the earlier migration
  intake wins whenever both migration and assault timers are due. Commit
  `a24d379` yields one pass only when assault timer, slot, defense, hull and live
  enemy prerequisites are ready; a rejected assault resets its timer and leaves
  migration eligible next sweep.
- **INVESTIGATING — Green/Purple upstream assault silence:** commit `e1c9dde`
  adds transition-only one-minute diagnostics using existing strings. IDs400-402
  publish blocker mask, last stage and stage time. Mask bits:1 route,2 slots,
  4 migration,8 relic,16 recovery,32 repair,64 berth clear,128 defense,256 no
  Transport,512 no live seed enemy,1024 timer waiting. Stages0-9 are documented
  in `T26-REPLAY-REVIEW.md`. This is DIAGNOSTIC ONLY and issues no gameplay order.
- **Still OPEN — visible late army inertia:** after90:00 Yellow has zero decoded
  AI attack orders, while Green has1303 and Purple756. This corroborates Yellow
  silence but prevents treating every visible Green/Purple idle formation as
  global command silence. Exact group owner/target remains unresolved.
- **Still OPEN — remaining voyage/congestion classes:** idle Trade Cog detection
  does not cover active merchant traffic, allied hulls, buildings or every
  migration obstruction. Red hostile-damage and no-progress terminals are
  distinct; no known-danger veto was relaxed. The large STOP/order flood remains
  separately open and is not claimed fixed here.
- **PASS:**437/437 complete regression tests. Focused all-opponent, boarding
  grace, waypoint, foundation, blocker and lane-fairness fixtures pass. PER,
  assault mission/plan generation, strategy execution, naval doctrine,42 replay
  benchmarks, civ synchronization and825 ownership sites/zero direct permission
  failures pass. `git diff --check` reports only existing line-ending warnings.
  The first sandboxed full run hit the known Windows temporary-directory access
  error; the authorized rerun passed. Historical T16A1 guards normalize only the
  independently tested diagnostic initializer and six Trade Cog selectors.
- **Installed/source T26:474:**91 files, full SHA-256
  `8DD15E63C954C7434D5AA8816F5F4EC74C2F5FCDDA5FE6B5436FB07127FD26F2`.
  Deployment replaced exactly assault admission/definitions/missions/plans,
  custom constants, init goals and military. Independent read-only verification
  reports zero missing/different/unexpected files and marker
  `RAWAI-P3B44T26:474`.
- **Next acceptance:** use the user's planned more-open map, verify474/hash, and
  audit every player/hull. Require fourth-opponent evaluation, at most one local
  boarding grace, bounded <=12 landing validation, one-shot lost-foundation
  retry, safe idle-merchant yielding and an assault admission opportunity
  between failed migrations. Preserve Gray's successful landing control, three
  independent missions, useful partials, active trade and all danger/zone/path
  vetoes. Read IDs400-402 for every player still silent; do not call telemetry a
  fix.
- **Publication:** local branch remains ahead of
  `origin/recovery/p3b44-transport-only`; existing PR8 is the publication target.
  No push/PR mutation was requested in this replay turn.

## PREVIOUS — T25:473 DEPLOYED, 2026-09-01

User supplied the T24 replay after reporting frozen partially loaded Red
Transports, a temporarily motionless Red fleet, failed productive migrations,
and landed assault units stopping after their first target. Read
`T25-REPLAY-REVIEW.md` and benchmark
`britain-4v4-20260901-141200-p3b44t24-transport-recovery` before further work.

- **Workspace identity:** the same explicitly authorized recovery exception is
  canonical for this branch:
  `G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-transport-only`;
  Git root is the same path, branch `recovery/p3b44-transport-only`, pre-session
  HEAD `8a0cc4b6c7952eed1d92eac7b5a9ac7d6dcf3eeb`. Runtime/evidence commit is
  `e5ce4e738b761006f593c984a26bac39235dd028`; this HANDOFF commit follows it.
  No directory/branch switch occurred. The normal project canonical path remains
  `.pr-work\Rome-at-War-AI`; do not copy selected files between these checkouts.
- **Replay identity:**
  `SP Replay v101.103.48987.0 @2026.09.01 141200.aoe2record`, SHA-256
  `075741E0A60BFA02CCD089B37960A4F1988C1B617334CAAC461783405D6B6B85`,
  duration95:05, zero action-stream errors, T24:472 markers players2-8; Red
  resigns95:05. Selected colors/resolved teams match the preserved lobby. Replay
  and parsed `.analysis/replay-20260901-141200-t24-full.json` remain outside Git.
- **Broad transport audit:**39 hulls,596 garrison orders,216 unload orders and11
  terminal load-only phases across all players. Per-player hull/load/unload:
  Red8/161/64, Green3/53/0, Yellow3/27/5, Purple2/13/12, Orange5/101/33,
  Cyan8/61/14, Blue5/128/73, Gray5/52/15. These are reconstructed command
  lifecycles, not claims that every engine action completed.
- **T24 rendezvous CLOSED/runtime-confirmed:**60 phase-3 starts, zero phase-4
  timeout,17 full departures,3 useful partial departures and7 local empty aborts.
  Remote travel no longer consumes the30s local boarding deadline. Preserve this
  behavior; later orphaned cargo and colony construction are separate defects.
- **Migration drop site FIXED-PENDING-RUNTIME:** both completed Red worker
  landings report a live lumber cluster, then resource wait, then failure without
  a foundation. Source checks spendable affordability while wood is held in
  building escrow, creating a circular dependency for stranded choppers; landing
  also discarded the voyage's original resource anchor. Commit `9baaf33` first
  exact-ID/class/zone revalidates the original anchor, and releases wood escrow
  only when the matching Camp/Mill is affordable with escrow. Require a concrete
  nearby foundation, completion and resource work in a fresh replay.
- **Orphaned loaded Transports FIXED-PENDING-RUNTIME:** preparation recovery can
  clear hull/group/route ownership while cargo remains aboard, and an occupied or
  terminal quarantine slot previously left no owner to rescan free idle cargo
  hulls. Commit `9728568` adds a bounded exact-hull orphan scanner, excluding
  moving, damaged, grouped, under-attack and recently terminal hulls; one terminal
  grace interval rotates the scarce slot. Active missions must not be stolen.
- **Landed assault continuation FIXED-PENDING-RUNTIME:** four16s no-target samples
  released a landed group despite its300s lease; Red's second landing releases
  about88s later without another combat target. Commit `3c4426d` preserves live
  hostile priority and the hard lease but gives idle same-zone members twelve
  bounded same-landmass probes around the sealed objective before release.
- **Diagnostic label corrected:** `loaded transports:0` was never a total cargo
  count; the escort scan deliberately removed idle hulls. Commit `b574da0` labels
  it `active loaded escort targets` with no selection/behavior change.
- **Adversarial review:** active grouped/moving/attacked hulls remain protected;
  migration wrong-zone/path vetoes remain hard; only matching resource-building
  escrow is released; probe commands touch only self-owned, idle, ungarrisoned,
  same-zone, not-under-attack mission members. Historical T16A1 fingerprinting
  strips only the independently tested T25 probe state; unrelated mission logic
  still matches its immutable baseline. All changes are independently revertible.
- **PASS:**420/420 full regression tests; focused migration-foundation, bounded
  recovery, assault-preparation and landed-combat fixtures; PER structure and
  operand domains; generated assault sync; strategy execution; naval doctrine;
  41 replay benchmarks;824 ownership-relevant sites with zero direct permission
  failures; `git diff --check` has line-ending warnings only. Initial full run's
  Windows temporary-directory permission error passed on authorized rerun.
- **Installed/source T25:473:**91 files, full SHA-256
  `5DBA1CB89BE98F58B9E954E628E6E5040C0907C113FC916EC816B4D1DAB95405`.
  `tools/sync_test_ai.py --apply` replaced exactly assault missions, custom
  constants, init goals and military. Independent post-apply check reports zero
  missing/different/unexpected files and installed marker
  `RAWAI-P3B44T25:473`.
- **Still INVESTIGATING — temporary naval non-progress:** replay disproves a
  permanently orphaned Red fleet: the visible ships receive new assignments
  four to six minutes later. Naval opportunity has no progress watchdog, but the
  replay does not prove the exact target/writer or unreachable geometry. No
  guessed naval behavior patch was included.
- **Still OPEN — repeated command flood/lag:** large identical ORDER floods remain,
  including more than11,000 copies for one player/unit-target pair. This replay
  does not attribute the source writer. Do not conflate it with the three causal
  transport/colony fixes or claim a lag/crash fix.
- **Publication:** local branch is ahead of
  `origin/recovery/p3b44-transport-only`; existing PR8 remains the publication
  target. No push/PR mutation was requested in this replay turn. Do not create a
  replacement PR; update PR8 only on explicit publication request.
- **Next runtime acceptance:** confirm473 and exact installed hash; audit every
  player's Transport lifecycle. Require productive original-anchor drop-site
  construction with escrowed wood, bounded adoption/recovery of every eligible
  orphaned cargo hull without mission theft, and landed groups acquiring another
  hostile or advancing through same-island probes within the existing300s lease.
  Preserve T24 rendezvous, useful partial/full lifts and landing safety.

## PREVIOUS — T24:472 DEPLOYED, 2026-09-01

User supplied the T22 replay and reported hundreds of villagers waiting on
beaches with nobody migrating. Read `T24-MIGRATION-RENDEZVOUS.md` and benchmark
`britain-4v4-20260901-112916-p3b44t22-migration-rendezvous`.

- Same authorized recovery working-directory/Git-root exception:
  `G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-transport-only`;
  branch `recovery/p3b44-transport-only`, pre-session HEAD
  `8854015037aed2e0d879a4d5796db221a2eadcd9`. No workspace/branch switch. Normal
  canonical directory remains `.pr-work\Rome-at-War-AI`; do not edit or copy
  selected files into the obsolete root extraction.
- Replay SHA-256
  `02E96FAE79D42D3F9BA276AFEA503374F2DE21738F026D0854AF7F1B0EFB7F59`;
  duration85:19, zero action-stream parse errors, T22:470 markers players2-8,
  Red resigns at85:19. Replay and all raw analysis stay outside Git.
- **Evidence conflict preserved:** user directly observed no migration during the
  beach pile-up. Replay commands also record full Gray worker departures at71:48
  and84:05 and Red at81:42; Red's twenty settlers are detected landed at83:19.
  Clarify whether “nobody” meant no departures during the observed pile-up or no
  sustained productive colony. Do not override either account meanwhile.
- **ROOT CAUSE — source/runtime proven:** the migration controller selected a
  hull and passengers, issued exact-hull garrison, and immediately started its
  30s load timer. It had no rendezvous state or distance gate. Across26 migration
  boarding windows, distant Yellow/Purple/Orange/Blue Scouts retain the correct
  order and close distance with no command conflict before empty aborts. Worker
  missions show the same boundary; Red/Gray full loads depart when they happen
  to beat it.
- **FIXED-PENDING-RUNTIME:** preserve existing targets/hulls/passenger eligibility,
  but save the closest reserved passenger as an anchor and give both sides a
  separate120s exact-hull rendezvous lease. Commands renew every8s. The unchanged
  30s local boarding window begins only at <=12 tiles, after full boarding, or
  when no reserved passenger remains ashore. Phase3=start, phase4=timeout; timeout
  flows once into existing full/partial/abort recovery.
- **Separate admission defect remains INVESTIGATING:** Red's29:53 snapshot says
  idle bucket0, transports2, defense0, depleted0, pressure0. Ordinary worker
  migration needs two engine-idle villagers unless depletion/pressure is active;
  visually waiting workers with stale orders therefore do not qualify. Pressure
  becomes5 at50:52 and Red's worker mission begins52:58. Equivalent outer-gate
  state is not exposed for every player, so T24 does not add speculative worker
  stripping or claim that every no-admission case is fixed.
- **PASS:** five focused actual-PER migration rendezvous tests; **414/414** full
  regression tests; PER, naval, strategy, generated assault, forty replay
  benchmarks and ownership checks;821 relevant ownership sites, zero direct
  permission failures; `git diff --check` has only line-ending warnings.
- **Installed/source T24:472:**91 files, SHA-256
  `09DFDC3781921B5E1A95E8181274D86B8EDCEE0E9BE84B2A5FA95E96AD740BEA`.
  Deployment replaced exactly four files: assault mission defs, custom constants,
  marker/init goals and military. Independent post-apply check reports no missing,
  unexpected or mismatched files; installed marker is `RAWAI-P3B44T24: 472`.
- Causal/evidence commit `d7e634508b98abf8d05918e0d7a1be92fa7e6338`
  is pushed to `origin/recovery/p3b44-transport-only`. Existing PR8 was updated,
  not replaced: `https://github.com/MnHebi/Rome-at-War-AI/pull/8`.
- Outside-repository diagnostic artifacts:
  `.analysis/replay-20260901-112916-t22-full.json`,
  `.analysis/p3b44t22-transport-audit.{txt,json}`,
  `.analysis/p3b44t22-task-ownership.json`, and
  `.analysis/p3b44t22-migration-admission.txt`.
- Next: fresh T24 replay, all-player lifecycle audit. Require phase3 remote travel
  to reach local full/partial boarding or one phase4 timeout. Separately enumerate
  any player never reaching phase3; add the smallest outer-gate discriminator if
  existing evidence still cannot name its blocker. Productive remote drop-site
  construction remains OPEN and is not resolved by rendezvous.

## PREVIOUS — T23:471 DEPLOYED, 2026-09-01

User reported that assault preparation selected a Transport before selecting its
passengers, regardless of their separation, then charged the approach against the
30-second boarding timer. User explicitly authorized correcting the architecture
before receiving the replay; use that replay to decide whether further measures
are needed. Read `T23-ASSAULT-RENDEZVOUS.md`.

- Same authorized recovery working-directory/Git-root exception:
  `G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-transport-only`;
  branch `recovery/p3b44-transport-only`, pre-session HEAD
  `2cbfe523f6c3b27a641f4b9769a8e35d0fc5db3d`; the T23 causal/evidence commit
  follows it. No workspace or branch switch. Normal canonical directory remains
  `.pr-work\Rome-at-War-AI`; do not edit the obsolete root extraction.
- **ROOT CAUSE — source proven:** empty-lift admission searched for an idle hull
  nearest `gl-home-anchor-x`, then selected soldiers nearest that hull with no
  distance bound, and entered `LOAD-ISSUE`, which immediately started the 30s
  boarding deadline. Distant rendezvous travel was therefore counted as local
  boarding failure.
- **FIXED-PENDING-RUNTIME:** T23 reserves the existing eligible 5–10-member
  combat manifest first, persists its representative point, chooses the closest
  eligible empty hull from that point, and gives both sides a separate bounded
  120s rendezvous. Commands renew every 8s. The existing 30s boarding timer begins
  only at <=12 tiles, when the manifest is already aboard, or when no reserved
  passenger remains ashore and exact cargo must be classified. Event23=start,
  24=local boarding, 25=rendezvous timeout. Timeout enters bounded recovery.
- Exact hull ownership remains guarded during all new phases. The immutable T17
  generated lease was restored unchanged after adversarial regression caught an
  initial extension there; T23 uses a separate narrow guard and existing
  OWNER-LOST recovery. Verified severe home defense remains valid preemption.
- Migration, voyage screening/fallback, approach planning, useful partial loads,
  three independent voyage slots, target persistence/rotation, and landed combat
  continuation are unchanged. Preserve Green/Gray/T22 successes.
- **PASS:** five new actual-PER rendezvous tests; **409/409** full regressions;
  generated assault/command-map sync; 39 replay benchmarks; 813 ownership sites,
  zero direct permission failures; `git diff --check` has only the two already
  documented generated-comment trailing-space warnings against `origin/main`.
- **Installed/source T23:471:**91 files, SHA-256
  `72A073D5FCC4DD15B33399942AF1CC4B7F4EA64F1AB55FC09E3B9D858BA6BE26`.
  Exactly five files replaced: assault mission defs, command-counter defs,
  custom constants, marker, military. Independent post-apply check reports no
  missing/unexpected/mismatched files; installed marker is
  `RAWAI-P3B44T23: 471`. No replay/data mod/dump was copied or committed.
- Runtime acceptance is pending. Audit every player and distinguish preparation
  rendezvous from downstream loaded-hull dispatch. Cyan never reaching admission
  and a loaded Red hull never departing are not declared fixed by this patch.
  PR8 remains the publication target and must be updated, not replaced.

## PREVIOUS — T22:470 DEPLOYED, 2026-08-31

User ordered: deploy/test the two T20 voyage fixes, bound preparation recovery,
remove global-target admission coupling, add bounded landed combat, then revisit
traffic/emergency unloading/landing quality. Read the T22 section of
`T19-REPLAY-REVIEW.md` for separate causes, limits, review and acceptance.
User then explicitly requested deploying T22 on top without waiting for a
separate T21 comparison replay. That deployment is complete and hash-verified.

- Same authorized working-directory/Git-root exception:
  `G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-transport-only`;
  branch `recovery/p3b44-transport-only`, runtime source commit
  `46d06c1fa74170d980b7ea207bf4073f0b8729ec`; publication/evidence commits follow.
  Resolve the current documentation-inclusive HEAD with `git rev-parse HEAD`.
  User requested a new PR after deployment; pending work is now committed in
  separate policy/causal groups, including separate T22 A/B/C commits. No
  workspace/branch switch. Normal canonical directory remains
  `.pr-work\Rome-at-War-AI`; do not edit/synchronize the obsolete root extraction.
- **Replaced T21:469**,91 files/hash
  `9B0F1E15A4B928B4AB93FACAB065B7D100761D73097D8ABAFC9CC179C6609A09`.
  Explicitly deployed from this checkout using `sync_test_ai.py --apply`, replacing
  only assault-missions, economy and marker from T19. Contains both T20 voyage
  fixes AND the immediately preceding requested Age2 gold fix. Full manifest
  independently reverified after T22 edits. No separate T21 replay was supplied.
- **Installed and local T22:470**,91 files/hash
  `7B6F61153B5FD927BFC8847008A82E19BD84650D3C50A8C362F4D7504DF89D79`.
  Deployed from this checkout using `sync_test_ai.py --apply`; independent check
  confirms all91 files match with no unexpected files. Installed marker verified
  as `RAWAI-P3B44T22: 470`. Seven runtime files replaced: assault admission/defs/
  missions/plans, customconstants, military, marker. No economy change after469;
  T20 voyage fixes and T21 Age2 gold fix remain included. No code changes or full
  test rerun during this deployment-only turn; payload matches the tested hash.
  Fresh startup/replay NOT YET OBSERVED.
- Immutable comparison/rollback archive, NOT a development workspace:
  `.analysis/p3b44t21-before-upstream.zip` outside the repository, SHA256
  `3EECE88D96763B73F1CCCB541839A10F4724800CB7AADA820863D10AB45BC140`.
  Its91 runtime entries reproduce the previous469 payload; includes pre-edit tools.
- **T22 A FIXED-PENDING-RUNTIME:** preparation recovery has a90s lease, preserving
  the three unload attempts. Exhaustion with occupied quarantine releases the
  lane without another order; empty stranded return cannot loop forever. Preserve
  old quarantine ID/cargo and prune converted/other-owner group references.
  The most recently relinquished hull is excluded from assault intake for300s
  (single recent-failure record, replaced by a later failure). This is explicit
  relinquishment to native/manual/utility recovery, NOT successful unloading or
  permanent quarantine. No active voyage slot is consumed.
- **T22 B FIXED-PENDING-RUNTIME:** empty-lift admission checks a known asset of its
  saved enemy outside the home/boarder land zone, retains exact objective across
  boarding, revalidates ownership/zone at planning. Missing objective logs plan
  reason30 and uses bounded overseas replan. Global target/scan/transport flag no
  longer decides admission. Existing team-wide strength/army/defense guards stay.
- **T22 C FIXED-PENDING-RUNTIME:** successful cargo-empty landing transfers exact
  troops to state6 combat in the existing mission group; empty hull/screen released.
  Every16s command only idle owned same-zone ungarrisoned members to a live hostile
  same-zone building/villager. Prefer saved enemy, then other living enemies.
  Three idle retries skip that target; four no-target checks or300s total releases
  ownership without STOP/retreat. Busy units untouched. IMPORTANT capacity limit:
  landed combat occupies its existing assault slot for up to300s; still at most
  three simultaneous owned assault lifecycles, not three voyages PLUS land groups.
- **PASS:**404 regression tests, including94 assault tests and6 landed-combat
  tests; PER/generation/strategy/naval/39 benchmarks;801 ownership sites/zero
  direct permission failures. Writer-trace sandbox temp-file failure was resolved
  by authorized rerun. Runtime acceptance remains NOT RUN, not CLOSED.
- PR publication audit: the working and installed91-file runtime still matches
  the tested470 hash above; no runtime edits or full-suite rerun for publication.
  Source/fixture history through469 was recovered into the index from the
  hash-verified T21 archive, without replacing any working/deployed files.
  T22 A/B/C commits: `2427dd4`, `6d38b06`, `46d06c1` respectively.
  Prior PRs5/6 are merged. Publication2026-09-01: PR7 is OPEN against `main`
  from this same branch: https://github.com/MnHebi/Rome-at-War-AI/pull/7 .
  The PR includes the pending runtime, tests and evidence; it is not merged.
  Full-branch `git diff --check origin/main` reports two trailing spaces in
  generated command-map comments (`rawai-command-counter-defs.per`, lines8/52).
  Kept the tested/deployed payload unchanged; this is not a gameplay failure.
  No replay, DAT, dump, archive or external binary is included in publication.

Next: start a fresh470 game and confirm marker470; audit all-player replay and
manual interventions against T20/T21 and A/B/C acceptance criteria in the report.
The user waived a separate469-first comparison. Congestion, near-beach emergency
unloads and landing-plan quality were revisited but NOT changed in470; neither were migration dropsites,
taunt31 receive/defer gates, STOP flood, naval production or other backlog issues.

## PREVIOUS — T21:469 Age 2 gold bootstrap LOCAL ONLY, 2026-08-31

User prioritized a Mining Camp near gold promptly in Age 2. Read the T21 section
in `T19-REPLAY-REVIEW.md`. **FIXED-PENDING-RUNTIME**, not a migration-placement fix.

- Working directory/Git root remains the authorized recovery exception:
  `G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-transport-only`.
  Branch `recovery/p3b44-transport-only`, HEAD
  `387eccab36a3311ca90d9e39bea6d73013584a8b` plus preserved intentional changes.
  No workspace/branch switch, commit or push.
- Source cause: phase3 (Age2) set gold to0 while both Market/Blacksmith were
  absent, then left that allocation unchanged when only one existed. Positive
  gold demand gates the existing first-camp search. Both buildings appearing at
  700–900 food could also leave zero gold unchanged in the hysteresis band.
- Small independent economy patch: while either prerequisite is missing use
  food20/wood70/gold10/stone0. Initialize the food-recovery allocation only when
  both exist, food<=900 and gold share<10. Preserve existing40% gold hysteresis,
  worker ownership/depletion guards, Age1 opening and all placement code.
- **PASS:**6 new actual-PER allocation/admission tests;387 full regression tests,
  PER, strategy, naval and39 replay-benchmark validations. Sandbox run had one
  temporary-file permission error; authorized rerun passed all387. No gameplay
  proof claimed. All-player camp timings and review triage are in the report.
- **Installed remains T19:467**,91 files, full hash
  `35526EFC8E958DB8BBC7C366B4126B123D676763287E890EA66BCA597D7B58DF`.
  **Local T21:469**,91 files, full hash
  `9B0F1E15A4B928B4AB93FACAB065B7D100761D73097D8ABAFC9CC179C6609A09`.
  Includes prior T20 voyage fixes unchanged. Only economy, assault missions and
  marker differ from installed T19. No deployment; install on explicit request.
- Next acceptance: with affordable wood and visible home-zone gold, start the
  camp placement cycle within its existing <=10s idle retry cadence in Age2,
  without waiting for Market/Blacksmith; verify a nearby completed camp and
  actual gold deposits. Blocked geometry/construction can still fail and must
  remain explicit. Gray's full age delay is not declared closed. Transport
  upstream/traffic/landed-combat and overseas drop-site defects below remain open.

## PREVIOUS — T19 audited; T20:468 voyage fixes LOCAL ONLY, 2026-08-31

Read `T19-REPLAY-REVIEW.md` first. Latest replay204847 SHA256
`ED6963FB76DB551C9A05828F70E04847F72FF5F241AC966752DAC5442CA9C726`,
157:24, manually resigned for stalled play. User organized Red's larger land
attacks against Blue and assisted two unloads; those are NOT autonomous successes.
User additionally confirmed Purple was silent to31, then Yellow later was silent.

- **Working directory/Git root:**
  `G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-transport-only`.
  **Branch:** `recovery/p3b44-transport-only`; **HEAD:**
  `387eccab36a3311ca90d9e39bea6d73013584a8b` plus intentional pending changes.
  Same documented recovery exception; no workspace/branch switch. Preserve all
  preceding changes; do not synchronize the obsolete workspace-root extraction.
- **Installed remains T19:467**,91 files/full hash
  `35526EFC8E958DB8BBC7C366B4126B123D676763287E890EA66BCA597D7B58DF`.
  **Local T20:468**,91 files/full hash
  `02F378ACB020A471A9B5B45492894E5A75AF21F561658F831128B1D88DBD67D7`.
  Only `rawai-assault-missions.per` and marker differ in runtime. Nothing deployed,
  committed, pushed, or changed in the data mod. Install only on explicit request.
- Immutable pre-edit `.analysis/p3b44t19-runtime-control.zip`, SHA256
  `9DC862F1BEC8988EAE34D81D643837644915562211B0FD71EE9AE89EA1307A0C`;
 91 runtime entries independently match installed467; generator/test copies
  included. Archive for rollback/comparison, not another development workspace.
- **T20 causal A — FIXED-PENDING-RUNTIME:** landing leg inherited near-zero
  waypoint best distance, so real beachward motion did not refresh progress.
  Reset only private best/stall history on state1→2. Actual-PER moving-hull fixture
  FAIL in all3 slots before / PASS after; total voyage budget unchanged.
- **T20 causal B — FIXED-PENDING-RUNTIME:** timeout before completion suppresses
  passenger handoff. Red44797 logs no-progress then return-empty in same93:58
  sample. Move existing distance read and completed-unload rule before policy
  cancellation. Progress/total deadline coincidence fixtures FAIL before/PASS
  after. No permission added to unload a still-loaded hull under enemy fire.
  A/B are independently reversible generator edits, not a transport redesign.
- **PASS:**381 full regression tests;19 actual-PER voyage fixtures; generation,
  PER, strategy, naval and ownership762-site checks. Historical fingerprint was
  explicitly adjusted only for the authorized transition/order changes, marker
  test updated. Temporary-file sandbox failure cleared on authorized full rerun.
  Runtime acceptance for468 NOT RUN. Do not call the gameplay defects closed.

### Current priority and next actions

**Latest diagnostic follow-up:** read the upstream-formation section in
`T19-REPLAY-REVIEW.md`. Source/actual-PER checks prove conditional unbounded
preparation recovery when quarantine is occupied (3660s still WAIT; free-slot
control IDLE), and an empty hull unable to regain origin also retains the lane.
Both block new admission and31; Purple's exact post63:28 gate remains unrecorded,
so do not assert that this explains its whole stall. Also found mission/global
target mismatch in empty-hull boarding and home-zone/global-readiness coupling
that denies ordinary dispatch for already-landed troops. Yellow continues to
commit through155:00, so do not classify its28 failed/unfinished missions as no
formation. No runtime edits/deployment in this follow-up; T20 remains local only.
These upstream issues need separate bounded fixes/acceptance, not a claim that
T20's voyage changes resolve them.

1. Validate T20's long landing leg and deadline-coincident emptying in a fresh
   replay when authorized, preserving3 concurrent missions/partial loads. All-player
   T19 census:48 linked hulls,41 slot commits,4 landing events,30 return-empty,
   5 missing hulls,1 quarantine,1 underway. Five no-progress cases had issued an
   outbound unload; **25 Yellow cases failed before that** and are not explained
   by the landing-leg fix. No new telemetry or broad policy bundled into T20.
2. **OPEN requested traffic and emergency-unload policies:** user wants loaded
   missions to wait/yield/reroute through friendly traffic rather than expire and
   recall; and bounded immediate unloading when under attack a few tiles from a
   validated target beach. Neither was implemented by T20. Keep safety elsewhere.
   Red assisted hulls49166/46594 at120:26/120:42 were not active RAW3 missions;
   investigate their recovery/native owner separately, do not claim these fixed.
3. **INVESTIGATING landed idle/31:** Green nine landed98:42; last actor commands
  98:49–99:13 then none through157:24, despite4 acknowledgments. No later STOPs
   to those exact units. Purple no acknowledgments, Yellow4 then user-reported
   silence. Taunt acknowledgment is behind defense/preparation gates; exact gate
   snapshot missing. Postlanding gives one point-MOVE then releases; native
   type-wide exclusions may block free same-type soldiers. Source is not proof
   of retained flags. Separate receive/defer/dispatch and inspect exact ownership
   before adding bounded offshore combat continuation. Acceptance requires actual
   action, not merely an acknowledgment. Full IDs and next diagnostic in report.
4. **INVESTIGATING migration:**20 Red settlers land61:40, reserved member receives
   distant house BUILD61:58; camp65:30 near a different stone anchor, completed
  66:28. Global pending-house/Market wait and distant alternate-anchor choice
   remain suspect; T18 exact placement did produce a matching foundation. Later
  117:36 and138:45 landings fail after60s unaffordable-camp waits before any build.
   Do not reapply the old point-placement fix to these different failure classes.
5. **INVESTIGATING** Gray Age2→3 delay (10:14→31:09, first camp request32:41),
   Imperial/Workshop prerequisite failure; STOP52213 and TC-loss lag; Yellow tower
   beach choice; enemy-adjacent walls; old Boarding Ship failures. Blue conversion
   success is user-observed positive control, not universal closure.

External `.analysis/p3b44t19-*` contains full/exact/command stream, transport
audit, dispatch, evidence and followups;225 passenger snapshots/53 partial-abort
records, zero decoder failures. `audit_t19_evidence.py` separates stored/terminal
plan reasons from next-enemy bundles and preserves exact member IDs. The report
and new replay benchmark preserve failures, intervention provenance and limits.

## PREVIOUS — T19:467 loaded-assault replanning, DEPLOYED, 2026-08-31

The user's latest directive replaces immediate recall after failed screening with
failed-approach memory and bounded approach -> objective -> opponent replanning.
Read the T19 follow-up in `T17-REPLAY-REVIEW.md` for scope, reason codes, review,
acceptance criteria and remaining engine uncertainty. **FIXED-PENDING-RUNTIME**.

- **Working directory and Git root:**
  `G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-transport-only`.
  **Branch:** `recovery/p3b44-transport-only`; **HEAD:**
  `387eccab36a3311ca90d9e39bea6d73013584a8b` plus intentional pending changes.
  This remains the documented recovery exception; no workspace/branch change.
  Preserve all preceding T13–T18 work. Do not synchronize the obsolete root copy.
- **Installed and local T19:467**, 91 files, independently verified SHA256
  `35526EFC8E958DB8BBC7C366B4126B123D676763287E890EA66BCA597D7B58DF`.
  Deployed on explicit user request using `tools/sync_test_ai.py --apply` to
  `C:\Users\LostSoul\Games\Age of Empires 2 DE\76561198053747760\mods\local\Rome at War AI\resources\_common\ai`.
  Seven files copied (five replacements, two additions); read-only recheck PASS,
  no missing, differing or unexpected runtime files. Installed marker467 verified.
  Replaced T17A1:465 (89 files, hash `B7BBA84A...EC6` recorded below); its existing
  `p3b44t17a1-runtime-control.zip` remains available for rollback.
  T18 migration placement is still included and still untested in the engine.
  No code changes, full-suite rerun, commit or push during deployment; source hash
  still matches the payload which passed378 tests. Fresh game startup not yet observed.
- Pre-edit archive:
  `G:\Projects\Codex\Rome at War AI\.analysis\p3b44t18-before-approach-replan.zip`,
  SHA256 `6E4C6E29193BB7F542A8A90D89A31520A4074ADD99B679F2FD4BD4DD9A405FF2`.
  Its 89 runtime files reproduce T18 hash `7CD27F5B...905` recorded below.
  Contains runtime and tools for comparison/reversal, not a development directory.
- Memory: 16 expiring opponent/objective/landing/reason/retry-after records;
  failed beaches within 12 tiles on each axis excluded for 300 game-seconds.
  Up to five candidates (anchor, lateral +/-28 and +/-56), three distinct
  objectives on the same landmass, then explicit opponent rotation. Three
  exhausted objectives or 180s per enemy trigger 300s deprioritization; no other
  objective also exhausts that bounded plan. At most three opponents /360s total.
  Budgets start at accepted-load planning, not every retry.
- Positive danger/lost Scout vetoes that candidate. Another candidate needs fresh
  same-island/all-hostile defense checks and a replacement free Scout or existing
  reason3/5/9 fallback. Accepted 5–9 partial loads remain eligible. Hull, manifest
  and passenger ownership survive replans. Global target SN is not modified and
  cannot overwrite the preparation choice. Three dispatched slots are unchanged.
- `tools/generate_assault_plans.py` is integrated into the existing assault
  generator/check. New generated runtime files are `rawai-assault-plan-defs.per`
  and `rawai-assault-plans.per`. Main loader, admission, screening/fallback and
  marker are the only other runtime edits relative to the T18 archive.
- Validation: **378 full regression tests PASS**, including80 focused assault
  tests; PER, generation, ownership762 sites, strategy, naval and38 historical
  replay benchmark checks PASS. String allocations1434/1500
  project budget; max physical runtime line215 characters. These are not engine
  acceptance or an engine string-limit measurement. Ownership inventory refreshed.

### Immediate next actions and open defects

1. Start a fresh test game and confirm467. Audit all-player approach episodes:
   A excluded, same hull/load tries B,
   bounded objective/opponent changes, no known-danger dispatch, useful partial
   load preservation, no interference with ongoing slots, then actual landings.
   Cached same-island points do not prove navigable coastline or a safe route.
2. Validate T18's separate drop-site fix: correct nearby foundation, reserved
   builders construct, resource gather/drop-off, no premature recall. Preserve
   separate causal attribution and reversibility from the T19 planner change.
3. Boarding Ship nonconversion remains **INVESTIGATING** (next section), not
   silently resolved by this transport work. STOP flood, Gray age-up/Workshop
   fallback, trade congestion and older ledger defects remain open.

## PREVIOUS inquiry — Boarding Ship nonconversion, diagnostic only, 2026-08-31

Read `BOARDING-SHIP-AUDIT.md`. Status **INVESTIGATING**, not a proven conversion
fix. Audited DAT task/target/enablement/range/charge fields, source command writers,
and all-player T16/T17 packet evidence (43/23 Boarding Ship train requests).
Normal1880 has zero conversion range; positive-range reference ships provide a
controlled-test lead, not proof. Siege-escort acquisition lacks a busy/converting
exclusion and can issue GUARD to an ungrouped converter, but the early Red
candidate has no explicit actor command25:59–58:32, so this does not establish the
reported29min failure's cause. Candidate32227's trained type is not proven.
No runtime/DAT/deployment/commit changes in this inquiry. Installed465 and local
466 below remain unchanged. Asked user whether direct manual conversion ever
succeeded; otherwise a small human-vs-AI/range0-vs1 engine comparison is needed.
External artifacts: `.analysis/audit_boarding_ship.py`,
`boarding-ship-dat-audit.json`, `p3b44t16-boarding-audit.json`,
`p3b44t17-boarding-audit.json`. Do not claim absent704 packets mean no conversion.

## PREVIOUS — T17A1 replay audited; T18:466 migration placement LOCAL ONLY, 2026-08-31

Read `T17-REPLAY-REVIEW.md` before further work. Latest replay is183134,
SHA256 `608B6681C240FC681E5C883A0CA9A138F3934FAE56DB40445B0AEDA45ECA5499`.
Red's distant camp / premature settler recall and three aborted assaults are
corroborated. The whole transport subsystem was audited across all eight players,
not just the reported event. No deploy, commit, push, branch or directory change.

- **Working directory AND Git root:**
  `G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-transport-only`.
  **Branch:** `recovery/p3b44-transport-only`; **HEAD:**
  `387eccab36a3311ca90d9e39bea6d73013584a8b` plus intentional pending work.
  Continue this documented recovery exception. Do not silently switch to the
  ordinary canonical `.pr-work\Rome-at-War-AI` or overwrite the pending T13–T17 work.
- **Installed remains T17A1:465**,89 files, independently verified full hash
  `B7BBA84A58914C4B8F650FCF183B5CAA79C1A4579DFE1F023E92B02A5AC08EC6`.
  Local source now **T18:466**,89 files, full hash
  `7CD27F5BA9D50C1ABA51B5B0C7C1D0829A6CD9F3568B7F522879B3E6F5D1C905`.
  Only `rawai-military.per` and `rawai-init-goals.per` differ from the pre-turn
  runtime; tests/knowledge/inventory also updated. Do not claim466 is installed.
- New immutable pre-edit archive:
  `G:\Projects\Codex\Rome at War AI\.analysis\p3b44t17a1-runtime-control.zip`,
 89 files, verified payload hash B7BBA84A...EC6 above. Purpose: comparison/rollback,
  not a replacement development directory. Existing controls remain untouched.

### Current defect state

1. **Migration drop-site misplacement: FIXED-PENDING-RUNTIME.** Red32067 lands14
   settlers56:54 at stone30546/zone3. Four camp BUILD requests57:55–58:59 are
   24.9–34.0 tiles from the resource; none can satisfy the8-tile foundation check.
   Failure59:20 explicitly recalls13 settlers before the construction phase.
   Cause: `up-build place-point` submits an expanding-region placement request,
   while its consumer requires an exact nearby foundation. T18 uses validated
   same-point `up-build-line` for migration Mining Camp/Lumber Camp/Mill. Existing
   owner, pending, generic resource/escrow, exact foundation/zone, partial-load
   policy, four attempts and genuine-failure recovery stay. No contradiction
   showing an acceptable nearby foundation was found in this replay.
   Diagnostics now copy persistent build coordinates: old `position-target`
   read an enemy building. The old T13 coordinate-based runtime attribution is
   withdrawn in the T13 report; source point-lifetime protection is retained.
   Acceptance/next: actual appropriate nearby foundation, reserved builders
   construct, then gather/drop off; no premature recall or invalid/unsafe builds.
   Engine result NOT RUN; exact-point terrain/hostile-fire behavior is a specific
   regression risk, not presumed equivalent to native queue placement.
2. **Red assault participation: INVESTIGATING.** Three normal accepted10-person
   loads, zero commits, holds8/8/10. Two exact scouts reported under attack;
   third exact ID missing. No captured attacker identity or proof of death.
   Scouts repeat the(137,137) beach. These are not old401 or slot exhaustion.
   Failure-aware overseas plan/target rotation remains unimplemented;90s recovery
   has no failed-plan memory. No proof an available safe alternative existed in
   this replay. No assault behavior changed this turn. Next scoped work: distinct
   failures/~180s ready-without-plan, ~300s opponent/plan deprioritization, persistent
   preparation choice, preserve already-dispatched slot identities and all hard
   danger vetoes. Do not count rule sweeps or weaken reasons8/10 for participation.
3. **T17 ERR2005 startup: CLOSED for reported symptom.** User confirmed startup;
  465 replay continues60:43. Physical-line wrapping was token-identical; exact
   engine parser limit remains unmeasured. Historical notes below are superseded.
4. **Dispatch ownership/validator T17 acceptance: partial, NOT CLOSED.** All six
   sampled migration terminal hulls retain group10; no401; Cyan/Gray each commit2,
   and Gray has two active independent slots. But zero slot landing successes:
   one fire-status recovery, three no-progress recoveries (last unresolved at end).
5. **Other unresolved work stays open:** STOP706 total69,741 (Orange58,862), no new
   writer attribution; Boarding Ship attachment without conversion; Gray Imperial
   prerequisite/placement failure and the requested bounded Workshop fallback
   plan; trade congestion; older ledger defects. Generic home-base drop-site
   controllers also use place-point, but were not changed by this colony patch.

### Validation, artifacts, next action

- **PASS:**11 focused migration tests;357 full regression tests; PER validation;
  assault generator synchronization; strategy execution; naval doctrine; ownership
  guard audit758 sites;38 replay benchmarks. Initial new benchmark lacked its
  acceptance list, corrected before the successful benchmark validation.
- Three focused new regressions FAIL against archived T17A1 source as expected
  under the corrected API fixture. That fixture models placement drift from API
  semantics/replay evidence; it is not an engine simulation or pathfinding proof.
- Read-only adversarial review: accepted queue/verifier mismatch, wrong enum and
  escrow/bounded-unavailability protections; rejected distant-foundation acceptance,
  removing recovery bounds and relaxed screen danger. Deferred engine acceptance
  only, as above. Full review/results and all-player episodes in T17 report.
- External artifacts under `G:\Projects\Codex\Rome at War AI\.analysis` use
  prefix `p3b44t17`: full, command-stream, exact, transport-audit(json/txt),
  task-ownership, summary, dispatch.53 windows/18 hulls;23 accepted preparations,
 19 holds/4 commits. `audit_t16_dispatch.py p3b44t17` reuses the existing reducer;
  default T16 input/output preserved. No mismatched writer-map attribution.
- Source is ready for a **scoped T18 engine test**, not runtime-validated.
  Install only from this checkout when authorized, independently verify466/full
  hash, and test an unobstructed resource landing plus blocked/unsafe candidates.
  Keep the migration patch independently reversible; do not silently merge a
  target-rotation redesign into its validation. Then continue failed-plan selection
  and the explicit unresolved ledger, rather than declaring transport fixed.

## PREVIOUS — T17A1:465 startup-format correction DEPLOYED, 2026-08-31

T17 startup **FAIL**: user screenshot at about00:09 reports Player1,
`rawai-transport-preparation-ownership.per2`, line8, ERR2005 Invalid identifier.
Source/deployment identity before the correction was the89-file T17:464 payload
`E060FC4BF5B4ABCC71DCA63C29B00E88988346654149D1E125EAB73CE9A11C3D`.
No T17 gameplay validation can be inferred from that failed startup.

- Continue the documented recovery exception below: working directory/Git root
  `G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-transport-only`, branch
  `recovery/p3b44-transport-only`, HEAD `387eccab36a3311ca90d9e39bea6d73013584a8b`
  plus preserved intentional pending work. No workspace/branch switch or commit.
- **Startup defect status: INVESTIGATING; formatting correction deployed for
  engine confirmation.** Every identifier on the reported line is defined before
  load. That physical line was727bytes, as were lines16/25;100/108/117 were600.
  All other executable lines were at most179. Physical-line parsing is the
  isolated hypothesis, NOT a source-proven engine capacity or confirmed closure.
- Smallest correction: generator `preparation_ownership()` emits the exact same
  binary OR trees on multiple short lines. Whole-module whitespace-token SHA256
  remains `17f2e0c44a172bcd4a4b0888ac727be9a248bbaab7a2759bc6eb34ea757341d7`.
  No condition, action, ordering, ownership or dispatch policy changed. Only this
  generated module and the marker differ in the installed runtime.
- `tools/validate_per.py` now rejects executable physical lines over240UTF-8
  bytes: a conservative PROJECT formatting guard, not an asserted engine limit.
  `tools/test_per_physical_lines.py` covers the exact old727-byte condition,
  token preservation, wrapped module, boundary, comments and string bytes.
  Initial fixture extraction incorrectly included the defrule header; corrected
  before final validation. **PASS: all352 regression tests**, PER structure,
  assault generator synchronization, strategy execution, naval doctrine and37
  replay benchmarks. String budget unchanged1447/1500. Ownership inventory
  regenerated,758 sites. These are NOT in-engine startup or gameplay results.
- Read-only adversarial review: **ACCEPTED** token-identical correction and
  prevention of oversized generated lines; **REJECTED** removing valid states or
  weakening ownership to silence a parser error; **DEFERRED** exact parser limit/
  alternative parser causes until fresh startup evidence. Conditions remain under
  the existing32-element rule limit. No new telemetry/STOP writer introduced.
- Immutable failing control (never edit/regenerate):
  `G:\Projects\Codex\Rome at War AI\.analysis\p3b44t17-startup-failure-control.zip`,
 89 runtime files, verified payload hash E060FC4B...11C3D above. T15/T16 controls
  remain untouched. Screenshot source is the user's Temp file
  `codex-clipboard-571a3f5a-852a-4df9-85b5-8cb2146336bc.jpg`, SHA256
  `BEF8A2B8E620C5E9C3314B96C0909774AE31CCA41B11B82538077721F4E8B7B4`.
- Deployment independently verified2026-08-31 18:29+03:00:
  **RAWAI-P3B44T17A1:465**,89files, source AND installed full-runtime SHA256
  `B7BBA84A58914C4B8F650FCF183B5CAA79C1A4579DFE1F023E92B02A5AC08EC6`.
  Target: `C:\Users\LostSoul\Games\Age of Empires 2 DE\76561198053747760\mods\local\Rome at War AI\resources\_common\ai`.
  No missing/different/unexpected runtime files after independent read-only check.
- **Next acceptance:** restart the failed test as a fresh game; confirm465 and
  all players load without AI errors. If ERR2005 persists, retain the failed
  evidence and inspect the newly localized line; do not claim line length proven.
  Then perform the T17 dispatch/non-regression acceptance below. Existing
  dispatch defects remain FIXED-PENDING-RUNTIME; unrelated backlog remains open.

## PREVIOUS — T17:464 dispatch fixes deployed; subsequent startup FAILED

User authorized implementation of the T16 audit's two dispatch corrections and
deployment after validation. Gameplay status: **FIXED-PENDING-RUNTIME**, not
CLOSED. No fresh T17 replay exists yet. No unrelated backlog policy was changed.

- Working directory AND Git root:
  `G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-transport-only`.
  Branch `recovery/p3b44-transport-only`, HEAD
  `387eccab36a3311ca90d9e39bea6d73013584a8b`, plus preserved intentional pending
  work and these T17 changes. Continue in this documented recovery exception;
  ordinary canonical `.pr-work\Rome-at-War-AI` is not silently substituted.
- Source **RAWAI-P3B44T17:464**,89 runtime files, full payload SHA256
  `E060FC4BF5B4ABCC71DCA63C29B00E88988346654149D1E125EAB73CE9A11C3D`.
  Installed payload independently checked identical; receipt below.
- Immutable rollback payload created before editing:
  `G:\Projects\Codex\Rome at War AI\.analysis\p3b44t16a2-runtime-control.zip`.
  It contains the87-file T16A2:463 runtime from this branch/HEAD plus its pending
  work, hash `3A246F56182BAEAF2EE4D3C0FA93844B48E8A8A35992791628B2D8C6CD7C7558`.
  Read/verified, never regenerated. It is a comparison/rollback artifact, not a
  development directory. The existing immutable T15 control is also untouched.

### Implemented causal patches, separately reversible

1. **Hull acquisition / preparation ownership — FIXED-PENDING-RUNTIME.**
   `rawai-military.per` revalidates exact self-owned, unflagged, empty, idle,
   unattacked hull eligibility. Old714/721 order values alone no longer exclude
   those reusable empty hulls; loaded/moving/owned candidates remain excluded.
   Mining and scout acquisition now use the exact saved ID, not a second broad
   nearest-hull search. Successful exact-owner acknowledgement is required before
   boarding; scout attempts are consumed only after that acknowledgement.
   `rawai-transport-preparation-ownership.per` detects later lease loss during
   loading/predeparture resource routing. It reclaims only the original idle,
   unowned, unattacked self hull for bounded terminal unloading/recovery; moving,
   foreign-owned/player and missing hulls are yielded, releasing only this
   preparation's passenger flags. No STOP action is added. Independent dispatched
   voyages are outside the handler. Failed FIND acquisition no longer silently
   resets after a useful load. New attempt clears stale script-load ownership.
   Generator: `preparation_ownership()` in `tools/generate_assault_missions.py`;
   new states in `rawai-customconstants.per`, scratch goal14909. Revert this
   function/output/load and the claim/acknowledgement hunks independently of2.
2. **Fallback player enumeration — FIXED-PENDING-RUNTIME.**
   `rawai-assault-screen-fallback.per` visits literal players1–8 once. Generated
   `rawai-assault-enemy-scan.per` admits only an active hostile player, then the
   original waypoint AND landing defense searches run for that player. No
   `up-find-player`/`up-find-next-player` dependency remains in this fallback.
   Known danger, damaged/lost scout, exact cargo/ownership, same-island landing,
   sealed opponent liveness and bounded voyage watchdogs remain enforced.
   Codes401/402 now diagnose a corrupt initial/subsequent scan cursor, retaining
   raw values/seen count;413/414/etc. still distinguish saved-enemy failure.
   Generator: `fallback_enemy_scan()`, scratch goal14910. Revert its output/load
   and fallback enumeration hunks independently of1; keep claim safety if doing so.

### Validation and adversarial review

- **PASS:**346 full regression tests. First run exposed a stale scout-attempt
  source assertion and a Windows sandbox temporary-folder permission error.
  Assertion now requires actual HULL-VERIFY ownership/ID predicates; rerun with
  required temporary-file access passed all346. Focused acquisition tests7 and
  assault tests59 include many subcases, not just string assertions.
- **PASS:**PER structure/operands, generated assault synchronization, strategy
  execution, naval doctrine,37 replay benchmarks, ownership source audit758
  sites/zero direct permission failures. Inventory regenerated. String budget
  **1447/1500** project literals; no per-sweep chat or new STOP writer.
- Actual-rule tests repair the six T16 failure inputs and preserve ordinary
  successful acquisition; rejected/raced/missing candidates cannot board or
  consume scout attempts. Test native iterator returning-1 without blocking valid
  manifests, every literal player, both danger points,5–10 accepted cargo,
  departed/nonhostile opponents, damaged scouts and unchanged independent slots.
- Read-only adversarial review **ACCEPTED**: retain loaded/native voyage
  protection; do not interpret old orders alone as activity on an empty idle
  hull; acknowledge exact acquisition; bound owner-loss recovery and never steal
  another slot; preserve all-enemy danger scanning and final revalidation.
  **REJECTED:** suppress401 or skip the safety scan; blanket-remove native-order
  protection; infer gameplay closure from tests. **DEFERRED/outside patch:**
  landing-plan coverage, real Trade Cog/shore obstruction, drop-sites, STOP,
  boarding-ship conversion, Gray placement/Imperial and reactive Skirmishers.
- **Runtime acceptance PENDING:** fresh game must show autonomous useful full/
  approved-partial departures, no loaded-but-unowned preparation loops, and
  fallback commits with valid enemies while real-danger rejections still work.
  Preserve Yellow's native-path success, Red's working committed voyage and
  three independently sealed missions. A quieter but inactive AI is a FAIL.

### Deployment receipt — 2026-08-31 18:08 +03:00

- Deployed with `tools/sync_test_ai.py --apply` from this recovery checkout to
  `C:\Users\LostSoul\Games\Age of Empires 2 DE\76561198053747760\mods\local\Rome at War AI\resources\_common\ai`.
  Two new and five changed runtime files copied atomically; no other runtime
  files removed or replaced. No writer-trace overlay or mixed-checkout payload.
- Independent subsequent read-only check: **89 files identical**, zero missing,
  different or unexpected files; full source/installed SHA256
  `E060FC4BF5B4ABCC71DCA63C29B00E88988346654149D1E125EAB73CE9A11C3D`.
  Installed `rawai-init-goals.per` directly confirms `RAWAI-P3B44T17`, value464.
  `git diff --check` passed (line-ending warnings only).
- Next action: start a fresh test, confirm **464**, then audit all-player
  acquisition/ownership terminal events, accepted loads, independent voyage
  commits/landings and code4 details. Deployment integrity is not engine startup
  or gameplay proof. No match was started by the agent. Both patches remain
  **FIXED-PENDING-RUNTIME**. No commit, push or PR in this implementation session.

## PRIOR — T16 replay dispatch audit, 2026-08-31; runtime unchanged463

User supplied `SP Replay v101.103.48987.0 @2026.08.31 162617.aoe2record` and asked
what prevents dispatch. All-player/source audit is recorded in
`T16-REPLAY-REVIEW.md` and `replay-benchmarks.json`. **No gameplay edits,
deployment, commit, push, PR or workspace switch during this audit.**

- Working directory AND Git root remain
  `G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-transport-only`;
  branch `recovery/p3b44-transport-only`, HEAD
  `387eccab36a3311ca90d9e39bea6d73013584a8b`, with preserved intentional pending
  T13–T16 work. This is the documented recovery exception to ordinary canonical
  `.pr-work\Rome-at-War-AI`; future agents continue here, not a stale snapshot.
- Installed/source **RAWAI-P3B44T16A2:463**, all87 files independently identical;
  SHA256 `3A246F56182BAEAF2EE4D3C0FA93844B48E8A8A35992791628B2D8C6CD7C7558`.
  Replay has seven matching startup markers, selected-color teams correct,
  zero final header/exact decoder failures,1,158,622 retained events. Duration
  97:06; user-ended stalemate, not a crash. Replay SHA256
  `F8D75EC49C2FF9DA206B872CAD697E98DF56F9C17FCE559F012F90BE130859E7`.

### Immediate dispatch defects and next actions

1. **ROOT-CAUSE-PROVEN source fault; runtime attribution qualified:** T16's
   assault/mining/scout claim rules exclude native orders714/721 AFTER candidate
   selection, but unconditionally advance into boarding even when the owner
   group is empty. Later movement requires the missing ownership flag. Actual
   T15/T16 rule comparison on identical inputs reproduces six T16 claim-contract
   FAILs;12 controls PASS. T16 migration terminals:11/12 outbound and12/16 return
   samples flag-2, versus all24 comparable T15 samples flag10. Red40804 accepts16
   at67:27 but is idle/unowned at its origin68:59; Red31594 accepts20 at90:39 and
   is idle/unowned92:11. Exact order at every claim instant is not logged; do not
   assert this explains every hull or excludes every later ownership writer.
   **Implementation:** none. **Next:** align selection/claim eligibility, verify
   exact-hull acquisition before boarding/attempt consumption, explicitly recover
   or terminate lost preparation ownership. Preserve genuinely active native/
   manual voyages. **Acceptance:** no loaded-but-unowned preparation loop; actual
   autonomous departure/landing; ordinary claims and prior successes survive.
2. **INVESTIGATING lookup failure; exact cancellation gate established:** all11
   code4 denials are401 (Gray5,Blue4,Green1,Cyan1). First enemy lookup returns-1,
   scanned0, while saved/checked enemy is valid and live and global target agrees.
   Not enemy death, target rotation, or detected danger. Numeric `find-ordered`
   constant3 and output goal14205 are supported by cached reference; engine cause
   is not yet established. **Implementation:** none. **Next:** bounded literal
   1–8 hostile/live scan preserving all-enemy danger checks, separate causal patch.
   **Acceptance:** eligible full/approved partial fallbacks pass and actually sail;
   dead/nonhostile targets and known dangerous routes still reject.
3. **INVESTIGATING landing/congestion:** seven hold1 events combine defended
   anchor/two lateral samples and wrong-island rejection; not proof every beach
   is impossible. Green multiple later ready loads never reach RAW3. Yellow's
   ~79-minute migration was manually freed by deleting Shipyards, then user saw
   no drop-site. Allied Trade Cog jam at1:30:20 remains separate. Do not conflate
   actual collisions with filtered-out movement recipients; do not relax real
   danger/same-island protection. No implementation or closure.

All-player52 command-linked hulls;66 full-ready+26 approved-partial checkpoints
(NOT92 unique missions),22 underfill aborts. Only one RAW3 commit: Red41383 slot1,
52:38, original enemy5=Orange; landing53:58. Yellow's user-observed49-minute Blue
assault follows native order714 at49:12, not RAW3. **Three occupied voyage slots
are not the main bottleneck.** Preserve both successes and three-slot isolation.

Other observations remain OPEN in report/earlier ledger: Red scout count label,
boarding-ship nonconversion, changing escort, Gray no University/Imperial,
Skirmisher reactive gate, missing drop-sites, repeated loading/abort and physical
congestion. STOP remains INVESTIGATING:353,691 STOP706 orders; S1 has no isolated
runtime success proof. No new STOP closure or broad backlog integration.

Timing discrepancy preserved: Red40804 logs initial loading abort59:05, before
manual moves59:53–60:00; another unload60:06. User observed an abort after moving
the hull toward boarders. Asked whether that post-input event was unloading/
returning; no answer yet. Do not blame user input for the earlier logged timeout.

### Diagnostic artifacts / validation

External `G:\Projects\Codex\Rome at War AI\.analysis\p3b44t16-*` full/exact streams,
transport/ownership audits, dispatch event bundles and claim reproduction remain
outside Git. Helpers `audit_t16_dispatch.py` and `reproduce_t16_claim_gap.py`
reuse existing exact decoder/reducers and repository actual-PER fixture engine.
Use `replay_parser_kjir`, not the incompatible older `replay_parser` header parser.
Immutable T15 ZIP was read without modification; see report for paths and hashes.
Source-bound reproduction PASS in exposing six defects; gameplay dispatch
acceptance FAIL; no fresh fixed runtime exists. Read-only adversarial review and
limits are in the report. No unnecessary full regression suite for docs/diagnosis.
Final checks **PASS**:37 replay benchmarks, `git diff --check` (line-ending
warnings only), and independent read-only runtime sync:87 files unchanged, zero
missing/different/unexpected files and the same463 payload hash. No files copied.

## PRIOR — T16A2:463 complete T16 payload DEPLOYED, 2026-08-31

User requested fine-grained code-4 reasons and original enemy identity. This is
**DIAGNOSTIC ONLY**, not a further cancellation-policy fix. The user subsequently
requested deployment of ALL T16 changes; the complete payload is now installed.

- Working directory AND Git root:
  `G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-transport-only`.
  Branch `recovery/p3b44-transport-only`; HEAD
  `387eccab36a3311ca90d9e39bea6d73013584a8b` plus preserved intentional pending work.
  This agrees with the documented recovery exception to the ordinary canonical
  `.pr-work\Rome-at-War-AI`. No workspace/branch switch, commit, push or PR.
- Source marker **RAWAI-P3B44T16A2:463**, 87 runtime files, full payload SHA256
  `3A246F56182BAEAF2EE4D3C0FA93844B48E8A8A35992791628B2D8C6CD7C7558`.
  Installed runtime independently rechecked: **T16A2:463**, all87 files identical
  to that source hash; zero missing, different or unexpected runtime files.
  T16A1's three voyage slots and the unvalidated S1 STOP experiment are retained.
  Nothing here proves the STOP flood or assault-participation defect resolved.

### Deployment receipt — 2026-08-31 16:23 +03:00

- Deployed from the documented recovery checkout above using
  `tools/sync_test_ai.py --apply`, without `--writer-trace`, to
  `C:\Users\LostSoul\Games\Age of Empires 2 DE\76561198053747760\mods\local\Rome at War AI\resources\_common\ai`.
  Four new and nine changed runtime files were copied; all87 runtime files were
  then verified by an independent read-only sync check. Installed marker source
  reads `RAWAI-P3B44T16A2: %d`, value463. No game was started by the agent.
- Includes the entire pending T16 runtime, not only A2 diagnostics: three
  independent assault voyages, sealed enemy/manifest/destination state, dispatched
  ownership protection, native-voyage takeover exclusions, code4 detail and the
  four S1 idle-reset-delay experimental changes. No new gameplay edits this turn.
- **PASS:**deployment preflight found the exact previously validated source hash;
  PER structural checks, assault generator sync and1434/1500 string budget passed.
  Reused the334-test/54-final-assault-test results below; no unnecessary full suite
  rerun for an unchanged runtime. Deployment byte/hash integrity is not gameplay
  or engine compilation proof; fresh-match startup/replay remains required.
- Existing rollback archive was verified before installation and not overwritten:
  `G:\Projects\Codex\Rome at War AI\.analysis\p3b44t15-runtime-control.zip`.
  Its83-file T15 payload hash is
  `8C9DF5B2B90E69656627ED1ACC5174EC22C16A47E8EEE83A519E8DD76FEF664B`.
  No source files, replays, data-mod payload or immutable controls were removed.

### Exact code-4 contract

Source evidence: the old `RAW44T screening bypass denied:4` conflated an invalid
enemy iterator with a rejected saved-enemy liveness snapshot. It could not identify
which branch fired. Keep that coarse record for existing replay consumers; the
new `RAW44T cancellation subcode` and short human-readable `RAW44T deny ...` line
provide the following distinctions:

| Subcode | Actual failing check |
|---|---|
| 401 | Initial enemy search returned a player below 1, before scanning any enemy. |
| 402 | Next-enemy search returned a player below 1 after one or more enemies were scanned. This is NOT proof that the saved enemy exited. |
| 411 | Checked saved-enemy ID is below 1; log the actual sentinel/value. |
| 412 | Checked saved-enemy ID is above 8; log the actual value. |
| 413 | `player-in-game` is false for the checked saved enemy. Does not distinguish defeat, resignation or disconnection. |
| 414 | Checked saved enemy is still in game, but `stance-toward ... enemy` is false. |
| 415 | The checked enemy and current saved manifest enemy differ. Preserve both identities and the original snapshot's failure code. |
| 419 | The live gate rejects despite a passing recorded snapshot; explicit internal inconsistency, not an invented enemy-death explanation. |

- Each cancellation reports stage (1=LOAD-READY, 2=unscreened bypass), hull,
  saved mission enemy, current global target, checked enemy, snapshot failure and
  live-gate value. Iterator failures additionally report current invalid result,
  first enemy, previous scanned enemy and count scanned. IDs are raw engine player
  IDs, not lobby-row/color guesses. Preserve replay identity/color evidence.
- Snapshot details are recorded alongside the ORIGINAL literal-player checks in
  `rawai-assault-admission.per`, not recomputed after cancellation. The same detail
  explains LOAD-READY enemy cancellations. Independent voyage event records now
  include their own slot's sealed enemy, never the next preparation/global enemy.
- Namespace distinction: **RAW3 event4 means voyage no-progress**, and RAW44C hold4
  is the existing screen-failure reason. Neither is the RAW44T denial4 split here.
- Terminal-only reporting: no status/sweep chats. At most16 lines including legacy
  fields for one iterator denial, 12 for another bypass code4, 9 for LOAD-READY.
  The existing same-pass cancellation consumes the reporting state. Shared string
  definitions avoid duplicating literals across eight player predicates/three slots.

### Implementation / validation / next action

- `tools/generate_assault_missions.py` owns mission definitions, admission,
  voyage event identity and new `rawai-assault-cancel-details.per`.
  `rawai-assault-screen-fallback.per` records which existing failure branch fired
  and loads the terminal report before the existing recall. Diagnostic goals
  14904–14908 do not control gameplay or alias existing goals. Runtime marker,
  focused tests and `OWNERSHIP-SOURCE-INVENTORY.md` are synchronized.
- **PASS:**334 full regression tests (first run failed only the stale T16A1 marker
  expectation; corrected and rerun). Final shortening of four diagnostic labels
  was followed by **54 assault tests PASS**. Eleven new tests execute the actual
  admission/report PER, including both circular and exhausted enemy iterators,
  all eight literal players, invalid IDs, dead/nonhostile players, stale snapshots,
  bounded terminal output, cross-slot enemy identity and diagnostic goal isolation.
- **PASS:**T16A1 predicate/action fingerprints unchanged after stripping ONLY chat
  and new diagnostic-goal writes; no new gameplay commands, searches, cancellation
  predicates, ownership mutations or timeouts. PER structural checks, generator
  synchronization, strategy/naval validators and36 historical replay benchmarks
  passed. Ownership audit:748 sites, zero direct permission failures. String budget:
  **1434/1500** literals; this budget does not prove engine compilation.
- Read-only adversarial review ACCEPTED: preserve checked versus saved identities
  so stale validation is not mislabeled as enemy defeat; distinguish first versus
  subsequent iterator failure and record the previous enemy; keep short shared
  labels; retain legacy coarse fields; keep diagnostics out of control predicates.
  No behavior change was smuggled into this telemetry request.
- **Runtime acceptance PENDING.** Underlying assault cancellations remain
  INVESTIGATING / previous implementation FIXED-PENDING-RUNTIME, not CLOSED.
  Deployment identity is now verified. In the next fresh match confirm startup
  marker T16A2:463, then inspect ALL players' transport lifecycles and cancellation records.
  Accept diagnostics only when a real cancellation identifies its branch and
  original enemy without repeated unchanged logs. Continue T16A1's concurrent
  voyage/non-regression acceptance below. Do not treat this as a STOP fix or an
  isolated STOP experiment. Existing dropsite, Market, naval-target, Port and
  Gray-Imperial defects remain explicitly open in the earlier ledger.

## PREVIOUS — T16A1:462 three independent assault voyages, LOCAL ONLY, 2026-08-31

User explicitly prioritized three concurrent assaults with independent mission
storage, persistent enemy identity and protection after dispatch. This supersedes
the next-action ordering below for this implementation. **NOT DEPLOYED.** Installed
runtime remains T15:460. No commit/push/PR, branch change or workspace switch.

- Working directory/Git root: `G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-transport-only`.
  Branch `recovery/p3b44-transport-only`; HEAD `387eccab36a3311ca90d9e39bea6d73013584a8b`
  plus preserved intentional pending changes. Documented recovery exception to
  ordinary canonical `.pr-work\Rome-at-War-AI` continues; immutable P3B44 untouched.
- Source marker **RAWAI-P3B44T16A1:462**, 86 runtime files, full payload SHA256
  `9960126E4842AC96DA69F94B9503620C17FF69F79D52CBB70310963A1A391BAA`.
  Installed T15 rechecked independently:83 files, payload
  `8C9DF5B2B90E69656627ED1ACC5174EC22C16A47E8EEE83A519E8DD76FEF664B`.
- The four pending S1 idle-reset-delay changes (0→5) are preserved, NOT newly
  validated. **T16A1 is not an isolated STOP experiment.** The T15 ZIP below plus
  those four SN changes and S1 marker still describes the separate S1 control.

### Evidence and implementation

- **CAUSAL FIX / FIXED-PENDING-RUNTIME:** T15 Purple hull33348 received native
  `AI_ORDER714` to `(195.5,42.5)` at1:16:43, then scripted hold1 and home UNGARRISON
  at1:18:37. Purple's1:16:01–1:17:45 wave contained eight distinct 714 hulls;
  multiple assigned passenger sets later received orders against Gray. This is
  not three sequential singleton missions. Existing SPECIAL-only boarding census
  omits this native717/714 path; do not treat it as a census of all voyages.
  This overlap does NOT establish the cause of every Red abort.
- **USER-REQUESTED POLICY / FIXED-PENDING-RUNTIME:** one existing boarding/screening
  preparation lane feeds up to THREE concurrently owned voyages. Preparation is
  serialized; three simultaneous boarding controllers were NOT implemented.
  `tools/generate_assault_missions.py` generates definitions, admission and voyage
  PER. Each voyage has independent goals14600+/14700+/14800+, a group0/18/19,
  hull, accepted manifest, screen, enemy, origin/waypoint/landing/target coordinates,
  zone, timing/progress bounds, obstruction count and terminal reason.
  No engine timer IDs are shared between these voyages. A full three-slot bank
  prevents starting a fourth scripted preparation; existing native voyages are
  protected, not counted as newly scripted missions.
- Seal enemy when preparation begins; subsequent FIND/screen steps use that
  saved player. Global target rotation and zero KNOWN buildings no longer
  invalidate LOAD-READY/fallback. Saved-player liveness uses literal player
  predicates, not mutable target/focus aliases. Actual player exit permits recall.
- Native transport/unload orders are excluded from loaded-hull intake and FREE
  transport acquisition/retasking; boarding selection excludes native ENTER units.
  Dispatched groups are protected by existing direct-writer ownership guards,
  conversion-safe group hygiene and native attack exclusion. Severe home defense
  does not preempt voyage groups. No global attack/retreat/reset was introduced.
- Bounded emergencies: saved enemy exits; hull takes HP loss with an identified
  hostile attacker (friendly under-attack alone is insufficient); invalid landing
  zone; no net voyage progress; total travel deadline; hull loss. Screened voyage
  cap600s, unscreened retains its300s cap; progress watchdog90s, landing initially60s.
  Return180s then quarantine retains cargo/ownership without a command loop.
  Quarantined slots are occupied until manual emptying, loss or conversion;
  three such quarantines can exhaust admission and must remain visible in testing.
- Moving hulls are not repeatedly ordered. Idle retry cadence8s; clearance may
  move only one FREE, idle, empty, unattacked same-water ship to a known same-water
  position; max3 issued clearance attempts. It cannot move another mission hull.
  Landing stages only this slot's screen and escorts whose target is this hull.
  Generic escort refresh pauses while any slot is landing; other escorts retain
  existing orders. Cargo-empty at the accepted beach issues the reserved landed
  troops an attack order, releases ownership, and orders the empty hull home.
- Group0 was also used by generic villager cleanup. That scratch work now borrows
  the preparation hull group ONLY while preparation is IDLE; its entire scratch
  lifetime is skipped during preparation. This defers generic broken-job cleanup
  during preparation and is a regression-risk item, not a STOP-resolution claim.

### Validation / review / next action

- **PASS:**323 regression tests, including16 new executed-PER voyage fixtures;
  PER structure/operand checks; generator synchronization; goal-range collision
  check; command-counter synchronization; strategy and naval validators;
  36 historical replay benchmarks. Permissioned test rerun needed for Windows
  writer-trace temporary-directory cleanup; full permissioned suite PASS.
  Historical replay benchmarks do NOT validate this new runtime.
- Read-only adversarial review ACCEPTED and corrected: scratch-group0 collision,
  per-slot admission search reconstruction, stale/foreign screen claims, native
  takeover, paired-escort staging and conversion-safe release. Old singleton
  voyage assertions were ported to executed three-slot fixtures; loading/partial
  acceptance tests remain. No new STOP writer or per-sweep chat was added.
- **Runtime acceptance PENDING; NOT CLOSED.** Test three overlapping missions;
  rotate the global enemy while they travel; defeat one saved enemy and verify
  only its mission recovers; demonstrate useful partial loads, safe landings,
  active landed armies, and congestion recovery without commandeering another
  mission. Audit ALL players, including717 ENTER and714 TRANSPORT orders, not
  merely SPECIAL/UNGARRISON. `RAW3 slot/hull/event` logs are transition/bounded
  events; code legend is in generated `rawai-assault-admission.per`.
- **Known unresolved boundary:** group flags are cooperative script ownership,
  not engine locks. Native exclusion is TYPE-wide: protecting passengers can
  delay FREE/landed units of the same type. Explicitly test continued land/native
  attack participation while other slots remain occupied. No runtime assurance
  of absence of native interference, path success or throughput is claimed.
- STOP flood remains INVESTIGATING. Code4 final building-count/target-alias gate
  changed to the requested liveness contract, but initial enemy iteration and
  real fallback participation still need replay evidence. Failure-aware target
  rotation, migration dropoffs, Market surplus handling, naval target fixation,
  Port congestion/placement and Gray's age advancement remain OPEN as below.
- Next: obtain requested deployment and fresh replay of this clearly labeled
  runtime, or test the separately described S1 control first. Do not silently
  install or treat this combined runtime as an isolated STOP comparison.

## CURRENT — T15 audited; isolated T16S1:461 STOP experiment LOCAL ONLY, 2026-08-31

This supersedes the untested-T15 status below. **T15 remains installed; T16S1 is
NOT deployed and NOT a proven STOP fix.** No commit, push, PR update or workspace
switch. Existing intentional T13–T15 changes are preserved.

- Authorized recovery editing directory AND Git root:
  `G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-transport-only`.
  Branch `recovery/p3b44-transport-only`; HEAD
  `387eccab36a3311ca90d9e39bea6d73013584a8b` plus pending changes.
  Ordinary canonical `.pr-work\Rome-at-War-AI` is unchanged; documented recovery
  exception continues. Immutable P3B44 baseline remains untouched.
- Supplied replay `SP Replay v101.103.48987.0 @2026.08.31 134755.aoe2record`, hash
  `46367A652B0823505591B6997E3A8E71B847F2C74F14361C4DE00CC2EB8F1F79`, duration157:27.
  All selected-color teams validated; full/exact decoder errors0. Final RESIGN
  player8 Gray; no crash attribution. See [T15 audit](T15-REPLAY-REVIEW.md) and the
  new `replay-benchmarks.json` entry for complete findings and provenance.
- Installed/source T15 identity independently verified BEFORE edits:83 files,
  `RAWAI-P3B44T15:460`, payload
  `8C9DF5B2B90E69656627ED1ACC5174EC22C16A47E8EEE83A519E8DD76FEF664B`.
  Exact immutable control archive created before changes:
  `G:\Projects\Codex\Rome at War AI\.analysis\p3b44t15-runtime-control.zip`.
  Extracted-entry hash matches T15. Diagnostic archive only, not a new checkout.
- Source T16S1 marker **RAWAI-P3B44T16S1:461**,83 files, payload
  `91F8328EC2782301CDDE9295BF9248E3AE0CAB8AA109A98EDAB866734FD22955`.
  Only two runtime files differ from the T15 archive: `rawai-sn-defines.per`
  (four native idle-group reset delays0→5 seconds) and `rawai-init-goals.per`
  (marker only). No other behavioral change or new tracing overlay.

### Results / current defect state

- **STOP — INVESTIGATING / T15 acceptance FAIL.**52,514 STOP706 packets, Red38,515.
  Total lower than T14, but Red worse; Gray improves without reaching Imperial.
  Red's dominant recipients are migration workers.5,113 identical group STOPs
  67:06–70:12; other long runs remain. Generic missing-target STOP writer1 runs
  only twice, so the previous simple attribution is rejected. Partial STOP at
  65:21 occurs after the flood began. Every explicit STOP site and existing
  counter boundary was audited; exact native producer remains unproven.
  **T16S1 is the authorized one-variable experiment**, not FIXED-PENDING-RUNTIME
  or CLOSED: test nonzero native idle-group recycling delay against T15.
- **Overseas fallback — INVESTIGATING / FAIL.**256 all-player boarding windows,
  157 assault.62 code4 denials, two code1, zero unscreened commits. Existing
  accepted loads still predominantly recall. Preserve queue **STOP → code4 →
  failure-aware target rotation → RC**. No code4 fix/rotation implemented yet.
- **Migration dropoffs — OPEN / FAIL.** Red two failed drop-site logs. User-built
  mineral Camp and AI-observed Camp on a mineral-free wooded island remain
  distinct from a separate confirmed AI foundation89178. Stale placement linkage
  unproven; initial wood availability unknown. Manual landings are not successes.
- **Market food surplus/wood starvation — INVESTIGATING.** User's manual sales
  and purchases are confirmed context; ordinary thresholds have a gap but a
  relocation bridge exists, so source thresholds alone do not establish cause.
- **Naval target fixation — OPEN, missing recovery policy source-proven.** Target
  59165 selected170 times over~37min after radius reached255. Expansion does not
  reject a preferred unreachable target. No naval behavioral change in this trial.
- **Allied Port congestion, manual Fortress interruption, Gray Imperial — OPEN /
  INVESTIGATING.** User confirmed127:28 Outpost was THEIR test, not AI takeover;
  no explicit STOP packet at that worker's failed Fortress attempts. Gray has
  Monastery/University build requests, which can satisfy DAT age prerequisites
  if completed; Fortress is not mandatory. Do not replace symptoms with guesses.
- Positive/limited:zero PACK packets;25 all-player Fish Trap BUILD requests and
  follow-up task orders, Red three exact foundations/ship assignments. Actual
  trap construction/food income still unproven. Cleared-Blue→Gray retargeting is
  positive user evidence, not validation of new failure-aware rotation.

### Validation and next actions

- PASS:two new configuration tests; **307 regression tests** on rerun; PER/
  operands; strategy execution; naval doctrine; command-counter synchronization;
  **36 replay-benchmark validations**;694 ownership sites/zero direct permission
  failures. Generated ownership
  inventory synchronized. Initial suite had one Windows temp-folder permission
  error in writer-trace fixture; permissioned rerun PASS. No engine test yet.
- Read-only adversarial review ACCEPTED speculative mechanism classification and
  legitimate-retasking-delay risk; REJECTED generic/partial STOP attribution from
  mismatched counter/onset evidence; DEFERRED unrelated changes. Details and
  pass/fail criteria in T15-REPLAY-REVIEW.md. No claim a configuration test models
  engine STOP generation.
- Obtain authorized deployment/fresh engine test of T16S1; T15 currently installed.
  Compare same manifest/boarding/voyage exposure, repeated STOP burst lengths and
  per-recipient rates where possible. Preserve gathering, construction, approved
  partial lifts, route progress, fishing and attacks. Inactivity is a failed test.
  Revert this one-SN experiment if ineffective/regressive before another trial.
- After this STOP trial is assessed, resolve the exact code4 branch (initial
  enemy lookup vs final saved objective), then implement the already-authorized
  failure-aware target policy. Do not bundle those into this isolation test.
- Private artifacts under `.analysis`: `p3b44t15-{command-stream,exact,transport-audit,
  task-ownership,summary,findings,inspection,episodes}.json`, transport-audit.txt,
  `replay-20260831-134755-t15-full.json`, runtime ZIP. Reducers `inspect_t15.py`
  and `reduce_t15_episodes.py` supplement existing all-player audit tooling.
  All raw replay/DAT/control payloads remain outside the AI repository.

## CURRENT — T15:460 exploration/fishing policy, DEPLOYED, 2026-08-31

This supersedes the T14 audit's no-runtime-edit statement below. **Deployed at
the user's request; in-game acceptance is still pending.**
No commit, push, PR update, branch change or new development workspace this turn.
Existing intentional T13/T14 pending work is preserved.

- Authorized recovery editing directory AND Git root:
  `G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-transport-only`.
  Branch `recovery/p3b44-transport-only`, HEAD
  `387eccab36a3311ca90d9e39bea6d73013584a8b` plus intentional pending changes.
  Ordinary canonical workspace remains `.pr-work\Rome-at-War-AI`; this is the
  previously documented recovery exception, not a silent relocation.
- Source marker **RAWAI-P3B44T15:460**, 83 runtime files, payload SHA256
  `8C9DF5B2B90E69656627ED1ACC5174EC22C16A47E8EEE83A519E8DD76FEF664B`.
- Installed **T15:460**, 83 files, from this exact checkout into
  `C:\Users\LostSoul\Games\Age of Empires 2 DE\76561198053747760\mods\local\Rome at War AI\resources\_common\ai`.
  Full installed/source SHA256:
  `8C9DF5B2B90E69656627ED1ACC5174EC22C16A47E8EEE83A519E8DD76FEF664B`.
  Installation and subsequent independent read-only sync check PASS: no missing,
  differing or unexpected runtime files. Installed marker verified as
  `RAWAI-P3B44T15:460`; no writer-trace overlay. Eleven files copied (nine updated,
  two added), no deletions. No source-code changes or repeated full suite for this
  installation-only turn: the payload exactly matches the 305-test validated build.
- Exact T14 runtime control preserved before edits at
  `G:\Projects\Codex\Rome at War AI\.analysis\p3b44t14-runtime-control.zip`.
  Its 81 extracted-entry payload hash is
  `DE6010CD8942E7D790A161FDE1A02CFC3F3C1F085E735731B16748F2A782B8A8`.
  Immutable diagnostic/control artifact only; NOT a development checkout.

### Release queue and classification

User's queue remains **STOP flood -> fallback code4 -> failure-aware overseas
target rotation -> RC**. Code4 must work before assessing target rotation.
Suggested rotation policy is three distinct opponent/plan failures or about180s
ready without a viable plan, then about300s deprioritization; pin the overseas
choice so closest-enemy selection cannot overwrite it. Neither that policy nor
code4 was implemented in this turn. Shipyard placement and reinforcement remain
behind this queue unless catastrophic.

During STOP investigation, user explicitly requested the following policy changes.
They are **USER-REQUESTED BEHAVIOR CHANGES**, not proven STOP root-cause fixes:

1. **Imperial general-exploration cutoff — FIXED-PENDING-RUNTIME.**
   `rawai-ownership.per` suspends native exploration on actual Imperial Age and
   cannot release the suspension afterward even if economic phase falls below4.
   `rawai-general.per` guards all positive native explorer quotas by actual age.
   `rawai-exploration-policy.per` stops/releases only own naval-scout-group16 once;
   `rawai-military.per` blocks new naval scout legs/scout ferry intake and
   postlanding exploratory patrols. A preexisting scout ferry can finish landing
   or recovery; retirement is restricted to its postlanding patrol states.
   Resource migration, assault screening/group7, escorts and productive fishing
   are not cancelled. The 32-element limit required splitting scout admission
   from planning; all original transport/stone/attempt predicates remain.
   Acceptance: no new general explorer admission/leg/patrol after Imperial;
   existing exploration retires once; mission screening and early exploration
   still work, with no retirement STOP loop. Engine acceptance NOT YET RUN.

2. **Fish-first / targeted Fish Trap fallback — FIXED-PENDING-RUNTIME.**
   `rawai-fishing.per` samples ships round-robin every2s, with up to40 exact-ID
   progress records (normal trained fleet remains capped at6). Known nonempty
   fish are preferred in that ship's water zone; idle/exploring ships get at most
   one direct gather command per45s. Missing fish leaves native resource-search
   exploration allowed, including after Imperial. No fish-disable SN or explicit
   STOP/EXPLORE command was added to this controller.
   Cargo change, not an issued gather order, refreshes a120s progress deadline.
   After sustained non-productivity, even with visible fish, find a completed,
   unattacked own Port in the same water zone. Reuse an unoccupied nearby trap
   first; otherwise test four cardinal positions five tiles from the Port and
   request at most one concrete Trap199 foundation with `up-build-line`.
   Global trap count is capped by existing Fishing Ship count. Missing resources,
   Port, legal position or a foundation within20s leads to180s terminal backoff.
   A real self-owned, same-zone Trap199 is assigned to the exact still-free
   Fishing Ship13 using `up-target-objects ... action-default`; this invokes its
   DAT build task for pending traps and gather task for completed traps.
   `up-assign-builders fish-trap -1` excludes automatic villager recruitment.
   No Construction Ship production is enabled. Cargo-carrying, already-building,
   attacked, converted or reserved ships are not retasked. The old untargeted
   fishing-ship deletion rules in `rawai-economy.per` were removed because they
   erased precisely the fleet that needs this fallback; training caps remain.
   Acceptance: visible usable fish produce food; without progress, an actual
   Port-side trap foundation is created, constructed by a Fishing Ship and
   produces food. No villager construction, working-ship eviction, build spam,
   excessive traps or loss of productive fishing. Engine acceptance NOT YET RUN.

These two policies have separate PER modules/load lines and can be independently
reverted against the exact T14 control. Shared marker/constants/counter changes
are supporting infrastructure; never restore whole files over unrelated pending
fixes. No claim that a STOP reduction from this combined requested policy build
would identify one exclusive engine cause.

### Evidence, review and validation

- STOP remains **INVESTIGATING**. New reducer
  `.analysis\investigate_t14_stop.py` and output `p3b44t14-stop-onsets.json`
  show dominant Gray objects alternating EXPLORE705/STOP706 tens of milliseconds
  apart before assault boarding. Exact singleton STOP totals remain in the T14
  review; per-recipient totals including group packets differ: Gray31795 has
  111321 STOP and111350 EXPLORE,31892 has110107/110113,32192 has104134/104134.
  Native exploration is implicated by the command family, but the exact native
  subcontroller/object type is not proven by source. Fishing Ship training timing
  is suggestive, not definitive identity. Other worker/garrison STOP clusters
  remain separate. Do not call this defect closed or disable productive fishing
  to manufacture a lower packet count.
- Authoritative external DAT inspected read-only:
  `RaW data fix\resources\_common\dat\empires2_x2_p1.dat`, SHA256
  `a1319be7e0d4ccf68a13e719ba2d8b4b39383d01b7d3fdd3123452f6a0d36356`.
  All34 civs' Fishing Ship13 has build action101 and gather action5 targeting
  Trap199; trap costs100wood, producer13, nominal construction40s. Private helper
  `.analysis\inspect_fish_trap.py`; no DAT/replay/dump payload added to Git.
- Existing AIRef reference cached at `.analysis\airef-reference-20260830.js`:
  fish traps use point foundations via up-build-line and explicit ship targeting,
  not generic build; remote resource searches include resource and ready statuses.
  `object-data-carry`, not `object-data-resource` (which is resource TYPE), measures
  cargo/remaining food. [Command reference](https://airef.github.io/commands/commands-details.html).
- Adversarial read-only review ACCEPTED and corrected before handoff: preserve
  command-counter IDs across new controllers; clear the local LIST as well as its
  search index; include resource-status fish; revalidate the Port at placement;
  keep foundation request separate from existence; refuse assignment/reporting
  with an empty eligible ship selection. Existing counters1-24/90-91 retain IDs;
  new once-only retirement writers are25/26. `instrument_command_counters.py`
  now preserves existing IDs and allocates only new ones. No tracing overlay.
- Focused actual-source fixtures:6 Imperial/ownership tests and12 fishing tests
  PASS. They explicitly exercise missing/delayed foundations, blocked fish,
  productive cargo, busy/converted/reserved ships, occupied traps, water-zone
  mismatch, placement failure, timeout/cooldown, all40 records and ID replacement.
  They do not simulate actual engine movement, construction or food income.
- Final full regression suite: **305 tests PASS** (26.305s).
  Structural/operand checks PASS, naval doctrine PASS, strategy sync/execution
  PASS,35 replay-benchmark metadata validations PASS,694 ownership sites with
  zero direct-permission failures. Updated generated ownership inventory.
  Literal budget1436/1500; no writer-trace overlay. An initial sandbox temporary
  directory permission error was resolved by rerunning tests with approval;
  three historical source-shape tests were updated for split scout admission.

### Exact next actions

1. Start a fresh test match and confirm replay marker `RAWAI-P3B44T15:460`.
   Installed full83-file hash is verified; all305 tests passed before installation.
   No T15 replay exists yet. Already-running games are not T15 acceptance evidence.
2. In the next authorized fresh test compare all-player actual STOP706/EXPLORE705
   episodes before/after each player's Imperial timing, productive fishing/cargo,
   targeted trap BUILD/WORK events, attack/boarding and screening participation.
   Quieter chat or fewer productive units is not STOP acceptance.
3. Continue STOP-first trials; then repair the25/25 fallback-code4 rejection,
   measure optional-screening participation, then implement failure-aware rotation.
   All other defect ledger entries below retain their previous statuses.

## CURRENT AUDIT — T14 replay115504 and target-rotation proposal, 2026-08-31

Read `T14-REPLAY-REVIEW.md` first. This supersedes the "start a fresh match"
next action below; deployment and workspace identity are unchanged. User requested
analysis/proposals, explicitly including failure-driven enemy rotation. No runtime
edits, installation, commit, push or branch change during this audit.

- Same recovery editing directory/Git root and branch below, HEAD
  `387eccab36a3311ca90d9e39bea6d73013584a8b` plus intentional pending changes.
  All81 installed/source files still match T14:459 / `DE6010CD8942E7D790A161FDE1A02CFC3F3C1F085E735731B16748F2A782B8A8`.
- Replay SHA256 `E1D8B629F1743E086AE5D9729CAB2E0B7C6D9E440ADD7E115F342E53BFE43977`;
 105:36, player1 resignation, exact decoder errors0. Selected-color teams preserved.
  All-player121 boarding windows,60 assault; Purple19 accepted/19 recalled;
  Cyan18 accepted/18 recalled; Orange13 accepted, four completion logs, one landing
  timeout, six recalls, two unresolved. Completion logs are not useful-combat proof.
- Purple15 reason1 rejections conflate defended and disconnected two-sided landing
  candidates; remaining recalls are actual scout danger/defended landing. Cyan17
  no-screen attempts all fail fallback code4. All25 global fallback attempts
  (Cyan17/Orange3/Gray5) deny4; zero unscreened commits. Optional-screening runtime
  acceptance FAIL, cause below the combined code4 still INVESTIGATING. Do not call
  this feature validated or treat all these vetoes as known route danger.
- **Target rotation source finding:** closest-enemy selection and dead/allied/
  zero-building fallback have no failed-assault feedback. Recovery retries after90s
  without opponent-specific failure memory. Proposed three distinct planning failures
  or180s ready-without-plan -> bounded alternative-enemy evaluation and temporary
  cooldown. A persistent overseas choice and pinned active mission are necessary;
  otherwise the closest-target writer can immediately undo rotation. Proposal only.
  Public target IDs absent: no claim that one exact opponent explains every episode.
- **Unresolved observed defects:** no help-call messages despite user's observed
  attacks/absent defenders; exact verifier/request blocker unresolved. Cyan has zero
  Shipyard BUILD requests; newest-anchor14-tile search/7-tile clearance and other
  admission gates require distinction. No claim that placement geometry alone is
  proven, or that lowering help cooldown repairs identity detection.
- **STOP first remains next implementation priority:**432,975 STOP706 packets,
  Gray351,920. Gray exact IDs31795/31892/32192 each exceed100,000 repeated STOPs.
  Cyan group[4649,31914,31984] receives8,395 in69:28–73:57. Reuse full T14 baseline
  and prior counters/ownership work for the already-authorized one-at-a-time,
  reversible experiment; do not quietly replace STOP work with broad transport policy.
- Evidence/reducers live outside Git under workspace `.analysis`, prefix
  `p3b44t14`; details, status/acceptance and exact next actions are in the review.
  Raw replay/data mod not copied into Git. Other existing defect ledger entries
  remain open unless specifically demonstrated otherwise.

## CURRENT — T14:459 all pending fixes DEPLOYED, 2026-08-31

### User priority override after the T14 replay — STOP flood first

User directive,2026-08-31: after the current replay, squashing STOP spam takes
priority over unrelated development. The user explicitly permits reversible
behavioral experiments based on unproven hypotheses for THIS defect, overriding
the usual no-guessed-behavioral-fix restriction within this scope. Do not require
proven attribution before trying a controlled intervention. This is not permission
to call a hypothesis proven, change unrelated systems, or hide diagnostic output.

- Keep T14 unchanged while this test runs. On receipt, establish the all-player
  STOP baseline and assess its existing acceptance checks; then focus development
  on STOP spam rather than another unrelated backlog or telemetry-only cycle.
- Preserve the exact T14 payload and use the existing command-boundary/ownership
  evidence. Make one independently reversible hypothesis-driven change per trial,
  label it EXPERIMENTAL, and state its predicted telemetry effect before testing.
- Compare actual replay STOP orders, affected object/group IDs, repetition rates
  per comparable time window and controller counters. Separate troop movement/
  attack churn from actual STOP706. Match context and exposure, not only raw
  whole-match totals.
- Revert ineffective or regressive experimental changes without reverting other
  pending fixes. A reduction caused by fewer active units, disabled productive
  behavior or suppressed logs is not successful resolution. Preserve gathering,
  boarding, attacks and legitimate defensive stops; repeat/narrow informative
  experiments until evidence supports a fix.
- STOP remains INVESTIGATING until behavior demonstrates improvement. Continue
  into a verified fix; recording hypotheses or adding telemetry alone is not closure.
  No runtime changes, deployment, full test run, commit or PR update for this
  priority-recording turn.

The user explicitly requested installation of ALL pending fixes for testing.
Deployment below supersedes the historical NOT DEPLOYED/installed-T13 statements
in the pre-deployment checkpoint. Runtime acceptance is still pending.

- **Editing directory AND Git root:** `G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-transport-only`.
  Branch `recovery/p3b44-transport-only`; HEAD
  `387eccab36a3311ca90d9e39bea6d73013584a8b` plus intentional pending changes.
  This remains the documented recovery exception. Ordinary canonical repository
  stays `G:\Projects\Codex\Rome at War AI\.pr-work\Rome-at-War-AI`.
  No new workspace, branch switch, commit, push or PR update.
- **Installed marker:** `RAWAI-P3B44T14:459`.
- **Installed target:** `C:\Users\LostSoul\Games\Age of Empires 2 DE\76561198053747760\mods\local\Rome at War AI\resources\_common\ai`.
- **Full81-file source AND installed SHA256:**
  `DE6010CD8942E7D790A161FDE1A02CFC3F3C1F085E735731B16748F2A782B8A8`
  using `tools/sync_test_ai.py:manifest_digest` / `payload_digest`.
  Both the post-install read-only sync check and direct81-file byte comparison
  PASS: no missing/different/unexpected runtime files. No writer-trace overlay.
- **Installed bundle:** exact-type/fresh-selection Palintonon PACK repair;
  first demanded military structure admission with one TC; trade producer census
  revalidation; same-target-island assault candidate checks; naval roster startup;
  persistent migration drop-site request point; one-way optional screening for
  accepted full OR useful partial manifests, with hard danger vetoes and bounded
  progress/travel. Detailed evidence, independent patch boundaries and acceptance
  criteria remain below and in `T13-REPLAY-REVIEW.md`.
- Compared with installedT13, five runtime files were replaced
  (`rawai-customconstants.per`, `rawai-economy.per`, `rawai-homebase.per`,
  `rawai-init-goals.per`, `rawai-military.per`) and
  `rawai-assault-screen-fallback.per` was added. The other75 files already matched.
  Only AI scripts were synchronized; no data mod, savegames or replays touched.
  PriorT13 remains recoverable from source `fb54ae46ed1ea35f2590157d5abb7bb1606e1802`
  and its recorded80-file hash. Immutable P3B44 control untouched.
- **Release PASS:**287 regression tests; PER structure/operands; naval doctrine;
  strategy execution (no errors);34 replay metadata checks;676 ownership sites
  (zero permission failures); command-counter and generated-inventory consistency.
  The marker change invalidated the inventory fingerprint: regenerated and
  rechecked before deployment. Literal budget1431/1500. No gameplay redesign
  occurred in this deployment turn: only marker, marker assertion and release
  documentation/inventory updates after the already-reviewed fixes.
- **Status:** all bundled gameplay repairs remain FIXED-PENDING-RUNTIME.
  Installed does not mean validated in game. Native STOP attribution, first
  migration anchor loss, path geometry, dangerous trade selection, fortified
  gathering, allied detection and ineffective wall bombardment remain OPEN.
- **Next action:** start a fresh recorded comparison match, confirmT14:459,
  preserve the authoritative lobby settings, then audit all players' relevant
  episodes. Priority: no non-Palintonon PACK; autonomous drop-site foundations;
  naval roster production; accepted partial/full unscreened departures with
  no re-screen loop, real-danger recalls and useful same-island deliveries.
  Preserve Blue screened follow-through and existing combined attacks.
  Game process was left running; user was told to wait for verification before
  starting the next fresh match. No restart/termination or existing-match claim.

## PRE-DEPLOYMENT CHECKPOINT — T13 audit and optional screening, 2026-08-31

Read [T13-REPLAY-REVIEW.md](T13-REPLAY-REVIEW.md) before resuming. It supersedes
the pre-replay acceptance and next-action text below, not the unresolved ledger.

### Latest user-requested policy: accepted manifests and one-way optional screening

**Classification: USER-REQUESTED BEHAVIOR CHANGE. Status: FIXED-PENDING-RUNTIME;
NOT DEPLOYED.** This refinement supersedes the earlier full-only
`min(capacity,10)` fallback. Scouting failure is not evidence of route safety.

- `rawai-military.per` now seals the accepted hull ID/count at normal boarding
  completion, after the existing T6 boarded-only partial-manifest rebuild, or
  after the existing native/manual loaded-hull admission. New missions clear old
  certificates/deadlines. The saved target player is captured at route selection.
- `rawai-assault-screen-fallback.per` admits the accepted normal manifest OR an
  already-approved useful partial (existing minimum5). It checks the exact owned
  hull, live cargo against the sealed count, and no current attack before and after
  the bounded scan. Lowering an unfinished request to9 does not certify it; accepted
  5–9 loads no longer need10 or literal hull capacity. Passenger ownership unchanged.
- Reason3 (no eligible free scout) starts validation immediately after the first
  search, without the former three20s acquisition retries. Reasons5/9 retain their
  waypoint/beach approach budget:30s initial approach plus four15s retries.
- Fresh known-defense scans at waypoint AND landing cover all enemies, bounded
  to eight passes. Revalidate the original live hostile player with known buildings,
  exact hull/manifest, and T13 same-target land zone immediately before committing.
  Timed-out scouts must remain owned/alive, not under attack, and at least their
  acquisition HP: damage/loss during validation vetoes fallback. Existing hard
  recall rules1/2/4/6/7/8/10/11 and successful screened landing rule remain unchanged.
- Commitment enters the existing departure/congestion controller once; source graph
  inspection across every runtime file finds no path back to screening before
  terminal recovery/new mission. A fresh arrival sample must improve the persistent
  best waypoint distance by at least2 tiles to refresh an unscreened-only60s
  progress deadline. Retries, oscillation and ordinary mid-route baseline resets
  cannot refresh it. Total unscreened travel still limited to300s; unloading retains
  its45s limit. Screened voyages do not inherit these deadlines.
- Transition pair: `RAW44T screening bypass hull/reason`. Denial retains original
  RAW44C soft reason and `RAW44T screening bypass denied`:1 invalid/attacked/
  incomplete or stale manifest;2 static defense;3 wrong/unknown land zone;
  4 invalid/finished enemy objective;5 scout loss/damage/ownership change.
  Hold13 = total unscreened travel expiry; hold14 = no net progress. Terminal logs
  occur once, not per sweep. Extend the next all-player reducer with these tags.
- Evidence: T13 has30 soft recalls (25 reason3,2 reason5,3 reason9), across Red/Cyan/
  Blue/Gray; not30 counterfactual successes. User's33 useful loads/four departures
  refers to T11. T6 accepted partials are explicitly preserved by this refinement.
- **PASS:**22 focused executable-rule/state tests (full and partial sealing, stale
  certificates, immediate reason3, scout loss/damage, target invalidation, all-enemy
  defenses, land zone, ownership, one-way graph, monotonic progress and deadlines).
  **287 full regression tests PASS**, zero failures/errors/skips after the approved
  rerun for the sandbox temp-file PermissionError. PER/naval,34 benchmark checks,
  676-site ownership audit (zero failures), counter/inventory synchronization PASS.
  Literal budget1431/1500. No subagents, new workspace, commit, push or PR update.
- Read-only adversarial review: **ACCEPTED** the user's partial-manifest objection,
  stale-token protection, post-scan target/scout checks and independent net-progress
  clock. **REJECTED** renewed screen acquisition during the same voyage and treating
  an action or passing fixture as route safety. **DEFERRED/OPEN** actual path geometry,
  hidden danger, useful post-unload reachability and native STOP attribution.
- Local81-file payload SHA256:
  `20016970910388293B5D2DD4A3FB5191499A10DF42F240A4F6924C6A45A591A8`
  (`tools/sync_test_ai.py:manifest_digest`). Installed original80-file T13 hash
  remains `A260148B2998E72203883BF34578D96B9AD6B72A561857C89ADBB28F23C96FB6`.
  Marker unchanged. Do not deploy this modified payload under T13's old identity.
- Fresh-game acceptance NOT RUN: verify eligible full and accepted5–9 loads actually
  depart and deliver useful troops after soft failures; no incomplete-load bypass,
  no re-screen loop, one bounded recovery on stalls, and no damage/defense exemption.
  Audit every player's bypass/denial/expiry/landing, preserving Blue screened
  follow-through, all earlier causal patches, group ownership and T6 partials.
  Geometry failures remain OPEN. A separately identified deployment is the next
  runtime step; none was authorized/performed in this refinement.
- Reversion boundary: only this policy module, its constants, military certificate/
  scout snapshot/progress/soft-trigger hooks and tests; preserve the independent
  PACK, migration, naval bootstrap, trade and same-island causal patches below.

- **Ordinary canonical repository remains**
  `G:\Projects\Codex\Rome at War AI\.pr-work\Rome-at-War-AI`.
- **Authorized current editing directory AND Git root remain**
  `G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-transport-only`, branch
  `recovery/p3b44-transport-only`, HEAD
  `387eccab36a3311ca90d9e39bea6d73013584a8b`. This is the documented recovery
  exception, not a new or silently replaced canonical workspace. Future agents
  must use this recovery directory for the milestone. No workspace switch.
- The tree was clean at audit entry. It now has **intentional uncommitted causal
  patches, tests and evidence** listed below. Preserve them; do not reset or
  synchronize stale copies. No commits, push, PR update or deployment in this audit.
- **Replay identity:** `SP Replay v101.103.48987.0 @2026.08.31 002333.aoe2record`,
  SHA `3106EDB647E64D12752788F1C6E4D1A281E6E130BE64ED8B14260EA6C429E70D`,
  121:55, resignation by replay player1. Selected-color mapping remains
  Red/Green/Yellow/Purple Romans versus Orange Picts/Cyan Britons/Blue Germani/Gray
  Gauls; do not infer visible colors from scoreboard numbers or body colors.
  Terrain array is220×220. Exact action decoder failures0.
- **Installed runtime unchanged:** `RAWAI-P3B44T13:458`, source `fb54ae46ed1ea35f2590157d5abb7bb1606e1802`;
  all80 installed files re-compared byte-for-byte against that commit, mismatches0.
  Existing payload hash `A260148B2998E72203883BF34578D96B9AD6B72A561857C89ADBB28F23C96FB6`.
  No writer-trace overlay. Local changes are NOT installed, and must not be
  deployed under the unchanged T13 marker.
- **Local payload:** five runtime files differ from installed T13:
  `rawai-military.per`, `rawai-customconstants.per`, `rawai-homebase.per`,
  `rawai-economy.per`, `rawai-init-goals.per`. Audit fingerprint
  `15F7A959CC9ABFE7D51BF910DCD39811B381FF728C913737223070F4B704FA8C`
  uses SHA256 of sorted root `.ai/.per` entries, each UTF8 filename + NUL + raw
  SHA256(file) bytes; this explicitly stated algorithm need not equal older
  deployment-report hash algorithms. Full file comparison is the identity check.

### Patch state and runtime acceptance

All are **FIXED-PENDING-RUNTIME**, not CLOSED. Preserve their independent
boundaries when committing/reverting; do not add unrelated policy into them.

1. Existing `387ecca` PACK selection repair now corroborated by229 packets across
   five players, including Purple/Blue TC producers. Additional TC fixture in
   `tools/test_pack_selection.py`. Require no non-Palintonon PACK, with legitimate
   Palintonon recovery preserved. Exact per-incident clobber writer unassigned.
2. First demanded Fortress/range/stable with one completed TC: four homebase gates
   admit first copy, retain expansion/need/ownership/resource restrictions.
   Red's single TC was a source-visible prerequisite blocker; geometry remains
   unproven. Tests in `tools/test_t13_gate_recovery.py`.
3. Trade census: live proof must not keep bypassing endpoint revalidation after
   a Port/Market count change. Two economy gates, same test file. Dangerous route
   selection, profitability and broader recovery remain OPEN.
4. Assault candidate geometry: compare target/left/right land zones before choosing
   a ±28-tile landing; constants14200–14202. Red64:07 unloaded on a separate island.
   Tests `tools/test_assault_landing_zone.py`. Empty-hull completion alone still
   does not prove useful delivery or actual passenger zone.
5. Naval roster bootstrap: one-shot `ship-train SCOUTSHIP` in init. All125 recorded
   navy snapshots show-1; Red101:41 had trainable Q/Oct and capacity but selection
   stayed unset. Four failing-before/passing-after actual-rotation fixtures in
   `tools/test_naval_rotation_bootstrap.py`. Preserve caps/roles/12s choice duration.
6. Dropsite point lifetime: persist bounded offset during PLACE, restore immediately
   before each camp/mill ISSUE. Red116:35 requested158,211 while six settlers were
   in the stone island's zone near32,51. Actual-rule delayed-request fixture in
   `tools/test_migration_foundation.py` fails old code/passes fix. Separate from
   first82:16 no-resource-anchor failure; no universal migration closure.

### Highest-priority unresolved state

- **INVESTIGATING — STOP flood:**195,024 STOP706; Red48,213, Gray97,549. Red's fixed
  three settlers receive36,017 until the manual camp at100:56. Explicit counter
  invocations do not account for the flood; native task/delegation cause remains
  unproven. It starts while boarding, not only after landing. Gray has no PACK.
  Reuse first-divergence packets/counters, not blanket native disabling.
- **INVESTIGATING — Juggernaut command churn/wall:** user confirms visible stopping.
  Nine identified Red siege hulls have no706, but repeated attack/move orders;
  wall43240 receives25 tagged attacks. User's manual ground fire on nearby
  in-range tiles did NO damage. This is not successful alternate-position fire.
- **INVESTIGATING — Red first migration:** ten landed82:16, immediate no-resource
  anchor/failure before a build request; cap-after-search/zone/visibility unresolved.
  Manual camp100:56 is not AI success. Later coordinate fault is separately patched.
- **RC screening blocker:** Red17 useful assault loads ->13 safety/screen recalls,
  one landing timeout, three empty-hull completions (one on wrong island).
  Blue has nine completion logs and some ensuing attack orders; preserve those.
  Gray26 recalls include18 no-screen cases. The explicitly requested soft-failure
  fallback above now addresses that policy gate locally, pending fresh runtime;
  legitimate safety checks and the unresolved geometry issue remain separate.
- **OPEN/INVESTIGATING:** unsafe trade assignment and autonomous re-probe, Cyan
  fortified gathering, geometry-limited construction, allied false/missed alerts
  (no300-series acceptance snapshots), Yellow boar interruption, Wonder completion,
  old crash attribution and cross-water relief. See report for evidence/next action.
- **Positive control:** user reports substantially better Juggernaut use and good
  Palintonon behavior. Blue useful landings/attacks, full/partial lifts, genuine
  defense and safety recalls must survive. Immutable P3B44 `8ec8700` untouched.

### Validation and exact next actions

- **PASS:**265 regression tests, zero failures/errors/skips;34 replay benchmark
  metadata checks; PER/operands; naval doctrine;672-site ownership audit with zero
  direct permission failures; command-counter/inventory generator consistency.
  The full
  suite's initial sandbox temp-directory error was rerun successfully with approval.
  Ownership inventory regenerated; no runtime correctness inferred from static PASS.
- All replay evidence, manual interventions, review triage and external artifacts
  are indexed in `T13-REPLAY-REVIEW.md`; benchmark entry is
  `britain-4v4-20260831-002333-p3b44t13-all-player`.
- Before preparing a test build: review/commit isolated causal changes if desired,
  then assign a distinct runtime marker and verify the whole payload. **No runtime
  was deployed during this audit.** Require actual camp completion/drop-off,
  heavy-ship production, trade recovery, correct-island useful assaults and zero
  erroneous PACK. Keep unmet criteria OPEN rather than calling them fixed in game.
- Continue STOP first-divergence and first-landing anchor investigation with the
  existing evidence. Do not defer them behind another general backlog or infer
  one root cause for all visible stopping.

## HISTORICAL — pre-replay Port/Shipyard PACK safety fix, 2026-08-31

At this earlier checkpoint the user was still testing original T13. The regression took priority
over further screening/backlog changes. The existing authorized editing directory
and Git root remain `G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-transport-only`,
branch `recovery/p3b44-transport-only`. This causal patch follows documentation
HEAD `4aa5d7baa4834ff55aa7b732c6b69dc9a1ff55c6`; resolve its current commit with
`git rev-parse HEAD`. Ordinary canonical path/control remain unchanged.

- **Status / symptom:** FIXED-PENDING-RUNTIME, local patch not deployed. User
  reports repeated real Packing progress on both Ports and Shipyards. Screenshot
  directly shows Red's Port, Vespasian Augustus, Packing48% at53:31; it is not
  merely an inferred animation. The completed T13 replay is now audited above.
- **Direct evidence:** screenshot outside Git at
  `C:\Users\LostSoul\AppData\Local\Temp\codex-clipboard-bedeeadf-a2ae-4c1c-af5e-103b17d49300.jpg`,
  SHA-256 `3BD2FAD15CC8F95FA29647C380EFA73BC3EA9C9D5C0343E86E8E4ED3A0EF49C7`.
  Shipyard symptom is direct user testimony. Do not infer any other player's
  color from slot order in this match.
- **Established source defect:** land siege's full-enemy-cycle producer sets
  FALLBACK below its consumer, so packing resumes next pass. The old consumer
  trusted shared `search-local`, filtering self/group flag but not unit type.
  Other controllers can replace that list with owned unreserved buildings.
  Only two explicit PACK writers exist, both in land siege. T13 commit
  `f10912c` made their formerly ineffective `up-target-objects action-pack`
  into working `up-target-point action-pack`, exposing the unsafe handoff.
  [AIRef](https://airef.github.io/commands/commands-details.html#up-target-point)
  specifies that the point action commands the local search results.
- **Causal limits / contradictory evidence:** the command-recipient defect is
  reproduced from actual PER rules, but the exact intervening list writer for
  Red53:31 and the Shipyards is not yet attributed without the replay. No
  contradictory observation is known. Port placement SNs issue no PACK action;
  they were not changed as a guessed response to this symptom.
- **Implementation:** `rawai-military.per` rebuilds the fallback search immediately
  before scope/dispatch. Both PACK sites enforce exact unpacked Palintonon42,
  self ownership and FREE status. Fallback also freshly enforces idle,
  ungarrisoned, unthreatened membership; normal fallback retains its source zone,
  emergency/no-enemy fallback explicitly uses global zone sentinel-1. Actual
  filtered count replaces the stale count. The late producer persists only state
  and zone, not a search snapshot. No new telemetry, goals or strings.
- **Tests / latest result:** all six new `tools/test_pack_selection.py` fixtures
  FAILED against original T13, including a clobbered list actually receiving
  PACK for both fixture Port4501 and Shipyard12511 (synthetic object IDs, not
  replay IDs). All six PASS after repair, including fresh Palintonon reacquisition,
  protected/busy/packed exclusion, empty-list no-command, scopes and actual count.
  Full248 tests PASS,0 failures/errors/skips; PER PASS;33 benchmark metadata
  checks PASS;672-site ownership audit PASS,0 permission failures; inventory and
  generated ownership/command-counter sources synchronized. Initial sandbox
  temporary-file error was rerun successfully with approval. No fresh engine
  acceptance is claimed.
- **Non-regression / read-only adversarial review:** every source line outside
  the land-siege controller is identical to `4aa5d7b`, including Juggernauts,
  all transports and ordinary attacks. ACCEPTED command-time role validation,
  fresh selection instead of merely filtering a stale list, emergency/global
  versus ordinary/same-zone scope, and recomputing the reported count. REJECTED
  reverting to ineffective PACK or altering Port geometry as a fix. Exact
  incident clobber attribution remains pending replay, not invented. The user
  separately reports Juggernaut use is far improved in the running T13; preserve
  that positive observation without calling the entire subsystem CLOSED.
- **Deployment identity:** no files copied, marker unchanged, no push/PR update.
  Installed original `RAWAI-P3B44T13:458` remains the80-file payload
  `A260148B2998E72203883BF34578D96B9AD6B72A561857C89ADBB28F23C96FB6`.
  Before edits it matched exactly. Afterwards only `rawai-military.per` differs
  in the checkout, intentionally; local unmarked patched payload is
  `F9C1F670BD66F1CD311C0998205F50D6F613BCDDD6C18DF26D65BBC15586E1F3`.
  Do NOT deploy this patch under the old T13 marker. Assign a distinct next-build
  identity and verify the full payload when preparing the next test after the
  running one finishes. No live-game repair is claimed.
- **Acceptance / next action:** audit all reconstructable PACK actions across
  all players in the running T13 replay and bind53:31 to exact objects/controller
  state. Then test the corrected build: no Port/Shipyard/non-Palintonon receives
  PACK; eligible idle/out-of-range Palintonons still pack and resume targeting;
  protected groups and improved Juggernaut behavior survive. Keep other defects
  in the deployed-T13 ledger below explicit; this patch resolves none of them.

## DEPLOYED — integrated T13:458; RC screening blocker, 2026-08-31

This section supersedes earlier audit pauses/integration queues below. Read
[T13-RELEASE-INTEGRATION.md](T13-RELEASE-INTEGRATION.md) for the full queue,
separate causal/policy commits, tests, limits and non-regression results.

- **Authorized editing directory / Git root:**
  `G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-transport-only`.
- **Branch:** `recovery/p3b44-transport-only`.
- **Runtime source HEAD:** `fb54ae46ed1ea35f2590157d5abb7bb1606e1802`.
  The final handoff-only commit follows this runtime commit; resolve current
  documentation HEAD with `git rev-parse HEAD`. No runtime changes follow it.
- **Single canonical ordinary repository:**
  `G:\Projects\Codex\Rome at War AI\.pr-work\Rome-at-War-AI`.
  Existing recovery-workspace exception remains authorized for this milestone;
  future agents must edit the recovery path above, not silently synchronize the
  ordinary checkout or workspace-root snapshots. No new workspace or branch was created.
- **Installed:** `RAWAI-P3B44T13:458`, 80 plain-source runtime files,
  SHA-256 `A260148B2998E72203883BF34578D96B9AD6B72A561857C89ADBB28F23C96FB6`.
  Source/install byte identity verified after the single integrated deployment;
  missing0, mismatched0, unexpected0. No writer-trace overlay.
- **Install path:** `C:\Users\LostSoul\Games\Age of Empires 2 DE\76561198053747760\mods\local\Rome at War AI\resources\_common\ai`.
- **Validation:** 242 tests PASS, zero failures/errors/skips;33 replay benchmarks
  PASS; PER/naval/strategy/evaluation/workbook/generator checks PASS;671 ownership
  sites with zero direct permission failures. Current literal budget1430/1500.
  Tests requiring temporary-directory access were rerun successfully with approval.
- **Runtime acceptance:** NOT RUN. Gameplay fixes are FIXED-PENDING-RUNTIME,
  not CLOSED. Source/fixtures detected no regression in ordinary attacks,
  ownership, full/partial lifts, migration landing, relic ferry, departure
  clearance or genuine defense; engine non-regression remains to be demonstrated.
- **Preserved control:** `8ec870075d08fcac98bad55b4ff045bf7abbc42e` untouched.
  Existing PR6/remote were not changed or pushed in this session.

### Current objective and defects

1. **RC BLOCKER — INVESTIGATING: loaded-assault route-screen acquisition/progress.**
   [T13-ASSAULT-FUNNEL.json](T13-ASSAULT-FUNNEL.json) covers all39 identified T11
   assault boarding episodes across all eight players:33 useful loads,28
   pre-departure screen recalls,4 cleared-screen/landing-command episodes,
   2 completed Purple landings,2 Orange landing timeouts,1 replay-ended case.
   Nineteen screen recalls are acquisition/progress cases;9 are danger/loss.
   Physical viability is not proven for all recalled routes. Acceptance: viable
   loaded missions obtain an owned screen, make progress and deliver useful
   troops without weakening legitimate safety checks. Next isolate exact screen
   identity/ownership and first failed movement boundary; do not steal ships or
   broaden attack changes from this aggregate alone.
2. **FIXED-PENDING-RUNTIME:** concrete1870/1750 production and family census;
   active worker builder-assistance ownership/current-animal release; exact
   victim/hostile allied verification at actual asset point; concrete migration
   foundation race; bounded recovery unloads; supported Palintonon pack action.
   Focused fixtures and causal commits are in the integration report. Next fresh
   replay must demonstrate each behavior; no claim of historical incident closure.
3. **Implemented policies, pending runtime:** 100/500/1000 need-gated aid,
   independent Imperial Market purchases, bounded Standard-victory Wonder,
   documented Port SN placement preferences. A/B/C integrated; offline D already
   present and not duplicated. Wonder resets on cumulative all-unit losses as a
   conservative proxy, not a claimed civilian-only counter. Port area/front/back
   preferences do not prove channel clearance/opposite island shores.
4. **INVESTIGATING — historical STOP flood:**152,771 STOP706 orders including
   7,561 to Red's fixed17 settlers. Earlier home-TC4503-directed task transition
   remains the lead. Builder writer correction is not historical producer proof.
   Reuse existing command counters and ownership packets; do not deploy another
   tracing-only milestone or disable all native economy/STOP behavior.
5. **INVESTIGATING — Octeres non-production:** concrete1884 source gate chain
   audited; exact runtime rejection remains unknown. Do not transfer the proven
   Quadrireme alias cause to Octeres or remove doctrine caps without evidence.
6. **INVESTIGATING — T11 Red18-settler Mining Camp missing:** no concrete
   foundation appeared. Distinct from the proven Purple pending/search race.
   Require actual foundation, correct-zone builders, completion and resource
   drop-off; preserve the T5 successful Red colony as control.
7. **OPEN — Yellow interrupted boar gathering at22–24:** ordinary retry requires
   an existing hunter; target-changed lurer is rejected. Exact Yellow branch and
   saved carcass survival are not yet established. Optional hunting behavioral
   patch was not included; inspect those identities before safe reacquisition.
8. Cross-water allied relief, historical friendly-fire ambiguity, route danger,
   command-flood causality and other previously recorded defects remain open
   unless the integration report explicitly narrows their status. No crash fix.

### Exact next actions

1. Start a fresh match using T13:458 and the authoritative comparison lobby.
   Verify marker/hash and selected colors; do not infer colors from player slots.
2. Audit all reconstructable transport episodes across all players, including
   successes, aborts, safety recalls, unresolved events and postlanding tasks.
   Prioritize the screen acquisition/progress stage rather than only boarding.
3. Validate new production, foundation, defense, recovery and policy behavior;
   preserve source-vs-engine uncertainty in the defect ledger.
4. Maintain the existing source-first STOP/Octeres/Red-foundation investigations
   without holding the completed integration hostage or adding broad speculative fixes.

Raw T11 inputs remain outside Git under
`G:\Projects\Codex\Rome at War AI\.analysis`: `p3b44t11-exact.json`,
`p3b44t11-task-ownership.json`, `p3b44t11-transport-audit.json`, related artifacts
listed in T11-REPLAY-REVIEW.md. Full T12 classification remains T12-SOURCE-AUDIT.md.
The report records every patch/provenance/commit and runtime acceptance criterion.

## HISTORICAL — T12 source-first audit checkpoint; no runtime change

The user's audit directive takes precedence over the integration queue below.
Read [T12-SOURCE-AUDIT.md](T12-SOURCE-AUDIT.md) before making the next patch.
It classifies every T12 change separately as causal, user-requested policy,
diagnostic-only, or speculative; it supersedes the earlier blanket causal label.

- Audit checkout/git root:
  `G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-transport-only`;
  branch `recovery/p3b44-transport-only`, HEAD
  `37a310872dccabc52db02962509f76f813ba4f3a`. Started clean; audit documentation
  and benchmark wording are intentional uncommitted edits. No runtime edits.
- Canonical ordinary repository remains `.pr-work\Rome-at-War-AI`; the existing
  recovery exception remains authorized. No switch, clone or replacement.
- No new telemetry, runtime deployment, commit, push or PR update in this audit.
  Installed identity remains the T12:457 payload documented below; no T12
  gameplay replay validates it yet.
- Retain: live assault clock, command-time naval identity reconstruction,
  spacing-only help cooldown, user-requested two-tile flare area and bounded
  inactivity radius growth (with converted-target guard).
- Selectively revert before the next candidate: the unproven ordered-all-enemy
  naval priority/iteration change; preserve the independent radius request and
  command-time reconstruction. No such runtime revert has been applied yet.
- Retain bounded existing diagnostics as diagnostics only. The drop-site probe
  mutates shared search/point/scratch state despite issuing no orders; do not
  call it search-neutral or add another tracing build by default.

### Audit findings / defect-state amendments

| Defect | Status / established boundary | Next action / acceptance |
|---|---|---|
| Roman Quadrireme/Quinquereme production | ROOT-CAUSE-PROVEN: `quadrireme-line = -282` selects DE Turtle Ship 831/832, not DAT 1870 -> 1750. Both common production files exclusively train the wrong line. | Concrete 1870/1750 checks/train actions and combined family cap, preserving role/rotation/fleet/resource limits. Audit other alias users. Deterministic gates then actual bounded Roman production before CLOSED. |
| Roman Octeres production | INVESTIGATING: concrete 1884 is correct; full availability/prerequisite/demand/cap/resource/producer/rotation/train gate checked. No permanent source disable found. | Existing evidence must distinguish actual research completion, cap/headroom, affordability and producer queue. Do not claim the Q alias explains Octeres or add probes before using existing ones. |
| Native boarding builder-assistance hold | ROOT-CAUSE-PROVEN competing writer: later homebase animal-food rule can enable assistance after ownership's one-shot hold, without checking hold. | Reconcile writer ownership and restoration; test load order, active hold, release, hunters present/absent. Not proven STOP attribution or Red colony cause. |
| False/missed allied attacks | ROOT-CAUSE-PROVEN query/claim defects; individual T11 incident attribution still INVESTIGATING. Proximity is labeled attack without victim check; ally relief searches original TC, not actual attacked asset/relocated home. | Verified hostile/victim/location and correct-location relief; test Yellow-only fight near Green, friendly fire, relocated colony, wrong-first-enemy miss. Cooldown does not resolve detection. |
| 152771 STOPs / 7561 identical Red group STOPs | INVESTIGATING after every explicit and native-boundary writer was inspected. First 17-member STOP precedes landing chat by122ms; earlier individual orders repeatedly target Red home TC4503. | Reuse exact packet/ownership/counter evidence at that earlier transition. No identified source writer yet; no blanket STOP/native-economy suppression. |
| Red 18-settler no-foundation landing | INVESTIGATING: native queue request is not a concrete foundation/creator. Red's 20-second waits differ from known Purple one-second failure. | Establish admission/placement rejection using existing request/timeout evidence; actual foundation/completion/drop-off required. |
| Purple global-pending foundation race | ROOT-CAUSE-PROVEN, still unfixed (existing ledger below) | Wait for exact own same-zone foundation within bounded deadline; global pending count must not trigger immediate recall. Preserve T5 Red's successful full lifecycle. |

### Exact continuation order

Complete selective T12 cleanup and the source-proven Q identifier, native
builder-hold writer, verified-attack/location, and concrete-foundation race
patches separately before broader integration. No fresh runtime deployment is
part of this audit. Continue unresolved STOP/Octeres/Red-foundation attribution
without presenting diagnostics as fixes.

Then resume **Authorized post-T7 work** below: bank-gated aid tiers, independent
Market purchases, isolated Wonder with recorded corrections, then Port SN work.
Offline salvage D is already integrated. This remains authorized, not canceled
or silently deferred; do not import unrelated military/transport changes.

Audit checks: PASS existing 14 focused T11/T12 tests, 666-site permission
inventory, 33 benchmark validations, whitespace check, and read-only 78-file
runtime identity check (no copied/missing/different/unexpected files). Full suite
not rerun because no runtime/test code changed. Runtime acceptance remains
PENDING. Detailed evidence, precise reversibility and
adversarial dispositions are in T12-SOURCE-AUDIT.md.

## CURRENT — T11 all-player audit; T12:457 installed, 2026-08-30

This section supersedes prior current-state sections, not their unresolved backlog.
Full evidence, defect dispositions, diagnostic field map, review and acceptance:
[T11-REPLAY-REVIEW.md](T11-REPLAY-REVIEW.md).
The corresponding metadata is the first entry in replay-benchmarks.json.

### Workspace and source identity

- Canonical ordinary repository remains
  `G:\Projects\Codex\Rome at War AI\.pr-work\Rome-at-War-AI`.
- Continue this authorized experimental transport/ownership recovery objective in
  `G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-transport-only`.
  This does not replace the canonical repository. No directory or branch switch.
- Branch: `recovery/p3b44-transport-only`. Started clean at
  `6350c8416c43e397b3058b88cf2d9cacb879fd56`.
- Final runtime/code HEAD:
  `47cf53f1d43c31ea20501aa6bd11a9ea27323d26`.
  A subsequent evidence/handoff-only commit records this section; use
  `git rev-parse HEAD` for the current documentation HEAD.
- Immutable P3B44 attack control remains
  `8ec870075d08fcac98bad55b4ff045bf7abbc42e` in the existing attack-baseline
  worktree. It was not edited, regenerated or deployed.
- Existing PR #6: https://github.com/MnHebi/Rome-at-War-AI/pull/6.
  This session's commits are **local, not pushed**. No GitHub/PR mutation.

### Deployment / validation

- Installed **RAWAI-P3B44T12:457**, 78 plain-source runtime files, SHA-256
  `A1757B8E758A077BE0F96C18292AF124AD1747EF1F6DBB6D04E8F730B283A345`.
- Destination:
  `C:\Users\LostSoul\Games\Age of Empires 2 DE\76561198053747760\mods\local\Rome at War AI\resources\_common\ai`.
  Independent read-only check: all 78 match; no missing/different/unexpected files.
  No historical writer-trace compilation or lifetime quota.
- An intermediate same-marker deployment briefly used minute navy snapshots
  (EE2DC7D5E1D026E4E7FE3A19BE843AA77A188DD163DE096ED58272F51D922A02).
  It was replaced before session handoff by the final five-minute interval.
  Do not attribute any replay solely by marker if it was started mid-session;
  the final full hash above is authoritative.
- **PASS:** final 204 regression tests, including 14 focused T11 tests; PER
  structure/operands; 1,156 strategy matchups; naval doctrine; workbook round-trip;
  33 replay benchmarks; 666-site ownership inventory with zero direct permission
  failures; diff whitespace check. Temporary-file tests required an escalated
  rerun; the final complete suite passed.
- **PASS:** read-only adversarial review dispositions in T11-REPLAY-REVIEW.md.
  Corrected adjacent-goal overwrite risk, stale threat diagnostic relabeling,
  converted progress target and cross-sweep command target validation.
- String budget: 1,431 literals, eight-player projection 11,448; within the
  project's conservative budget, **not measured engine string capacity**.
- **PENDING:** fresh T12 engine load and all-player gameplay/replay acceptance.
  No runtime gameplay defect is CLOSED by the tests or diagnostics.

### Current defect ledger

| Defect | Status | Evidence / implementation | Acceptance / next action |
|---|---|---|---|
| Red stone settlers without drop-site | INVESTIGATING | 18 landed 55:17; camp attempts 57:25/57:49, no foundation BUILD; failure 58:09; user supplied camp | Read T12 queue/placement/worker snapshots, prove cause, fix and demonstrate completed camp + resource drop-off |
| Idle/distance-limited Juggernaut targeting | FIXED-PENDING-RUNTIME | One-enemy 48-tile scan and cross-sweep fallback; T12 grows 48/96/192/255 after 120s without sampled progress, all enemies, exact revalidation | Distant autonomous bombardment with close attacks/escorts preserved; no unsafe-path claim |
| Assault boarding allowance shortened | FIXED-PENDING-RUNTIME | 60:00 request -> 60:19 empty abort; deadline used 15s cached clock | T12 live clock gives full 30s, preserve minimum-five/full/partial contracts |
| Other passengers not boarding / native task interference | INVESTIGATING | Some keep correct enter + reservation; others idle/no target; Red 63:29 sample work 609/709 while flag 11 retained | Correlate exact packets, candidate snapshots and bounded native-writer counters; no blanket theft or path diagnosis |
| Red loaded return around 66m | INVESTIGATING | Hull 37810 stalled at 12 tiles through four retries; 66:14 no-progress return with cargo 19 | Establish waypoint/collision cause; retain mixed-cargo observation without invented manifest classes |
| Missing Roman Quinqueremes/Octeres | INVESTIGATING | DAT availability confirmed, no Roman heavy MAKE; rejection gate unknown | Read phase/role/rotation/caps, line vs concrete train mask, tech/resources/queue evidence; then causal fix and bounded production proof |
| Taunt 69 selects unintended structure | FIXED-PENDING-RUNTIME | Search radius six tiles reduced to two; nearest one self-owned, no-candidate no-op preserved | Flare at intended center; only intended structure deleted, nearby outside-radius targets survive |
| Late repeated STOP/worker orders and lag | INVESTIGATING | 152771 STOP 706 records; identical Red settler STOP 7561; R2 already had 55148 | Nonzero minute counts of every explicit STOP/reset writer + native exclusions; identify producer and reduce repeated ineffective commands without disabling useful work |
| Help calls too close together | FIXED-PENDING-RUNTIME | Green 20:01/20:03; timer not rearmed on request | Both request paths now rearm120s; verify actual spacing |
| False/missed allied attack location | INVESTIGATING | Green false-warning observation, 253 cannot-verify replies; proximity fallback vs original-TC relief anchors | Match request kind/asset/hostile/anchor/freshness to responder anchor; no speculative radius widening |
| Cross-water allied relief | OPEN | Still unimplemented | Separate scoped design/fix after proven current blockers |
| Earlier friendly-fire, crash, boar recovery, dock placement/salvage backlog | OPEN / prior statuses retained below | This replay did not resolve or cancel earlier work | Preserve earlier evidence and recovery scope; do not mark complete due to prompt changes |

Each significant defect's direct evidence, hypothesis, contrary evidence,
instrumentation, implementation, latest result and exact acceptance are detailed
in the linked report. Failed camp, command spam, heavy production and allied
detection are **not** considered resolved by adding diagnostics.

### Historical T12 commits — mixed classifications, not all causal fixes

- 5c3a7ff: fresh clock for full assault boarding window.
- e2c43b3: two-tile taunt 69 deletion radius.
- d7400bb: expanding all-enemy capital-ship search, command-time identity rebuild.
- 8820cb0: rearm allied-help request cooldown at emission.
- 12189f6: bounded explicit STOP/scout-reset/native-exclusion invocation counters.
- 18648ce: drop-site, heavy production and allied request/response snapshots;
  T12:457 marker and converted-target progress guard.
- 47cf53f: five-minute steady production samples and current-marker test.

### Evidence / next session

External raw evidence under `G:\Projects\Codex\Rome at War AI\.analysis`:
replay-20260830-211106-t11-full.json; p3b44t11-command-stream.json;
p3b44t11-exact.json; p3b44t11-transport-audit.json/.txt;
p3b44t11-task-ownership.json; p3b44t11-summary.json. The bounded
inspect_t11.py helper queries chats/windows/unit commands/terminal events.
audit_writer_replay.py ran with --plain-runtime; obsolete writer-site IDs were
not applied to T11 source. The replay and data-mod payload are not in Git.

1. Receive a **fresh** T12:457 replay and verify its deployment identity. Keep the
   same authoritative color/team mapping; observed recorded speed in T11 is 2.0.
2. Repeat the all-player subsystem sweep; separate successful boarding/landings,
   bounded failures, unresolved lifecycles and command spam. Never reduce scope
   to the user's visible examples.
3. Decode the bounded writer and diagnostic maps in T11-REPLAY-REVIEW.md.
   Nonzero source invocation is not packet attribution; empty selections count.
   Navy masks are five-minute samples, not every attempted queue.
4. As soon as evidence identifies a cause, implement the smallest supported fix,
   run focused/full checks as appropriate, and require runtime acceptance.
5. Preserve normal combined attacks, partial/full lifts, exact ownership,
   same-water escorts and tight flare deletion. No speculative multi-controller
   redesign.
6. Push these local commits/update PR #6 only when requested.


## PREVIOUS — T11 source-first ownership implementation, 2026-08-30

This section supersedes the diagnostic-stage priorities below. User directive:
`18529df3-3d8e-4635-84a9-871e505b439d/pasted-text.txt` (source-first ownership).

- Canonical ordinary development repository remains
  `G:\Projects\Codex\Rome at War AI\.pr-work\Rome-at-War-AI`.
- Authorized **experimental recovery checkout**, and location to edit for this
  objective: `G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-transport-only`.
  It does NOT replace the canonical repository. Branch:
  `recovery/p3b44-transport-only`. Starting HEAD:
  `a5de7d85bad71f36f4c8903747908d71ac164a7e`, clean before implementation.
  Resolve current implementation/documentation HEAD with `git rev-parse HEAD`;
  deployed source identity is independently fixed by the hash below. No new
  clone/worktree, branch switch, push or PR update was performed.
- Immutable attack control remains clean at
  `8ec870075d08fcac98bad55b4ff045bf7abbc42e` in
  `.recovery-work\P3B44-attack-baseline`. Do not edit it.
- Build **RAWAI-P3B44T11:456**, **73 plain-source runtime files**, SHA-256
  `2CA656510A99D71A9C5A2CB5014FC3138904D120E806269127DEB5FF5824DABF`.
  **Installed and independently rechecked:** all 73 files match, with no missing,
  different or unexpected runtime files, at
  `C:\Users\LostSoul\Games\Age of Empires 2 DE\76561198053747760\mods\local\Rome at War AI\resources\_common\ai`.
  R4:455 was installed at session start. T11 does **not** use `--writer-trace`
  or a lifetime quota. A fresh match is required; an existing game is not T11.
- Status: **OWNERSHIP IMPLEMENTED FOR SOURCE-PROVEN PATHS — NATIVE BOUNDARY
  REQUIRES ONE DISCRIMINATING TEST**. Gameplay is not CLOSED.

### Implementation / evidence

TASK-OWNERSHIP.md contains the full owner/fault/compatibility matrix and review
dispositions. OWNERSHIP-SOURCE-INVENTORY.md enumerates **662 relevant current
rule sites**, including actual selectors, commands/delegations, reservation
mutations and permission filters. `tools/audit_ownership_source.py --patch`
and `tools/generate_ownership_policy.py` emit reviewable patches for these
generated artifacts. The one-use transformation helper was removed.

- Removed global reset/retreat/ALL-unit STOP from routine land/naval defense,
  siege escalation, loss regroup, periodic-loss recovery and taunt retreat.
  R1/R2/T8 already establish reserved-passenger intersections.
- Separate migration 10/11, recovery 12/13, relic 14/15, naval Scout 16 and
  relief 17 from assault 3/4, raid 8, screen 7 and escorts 9. Capital siege's
  Juggernaut/Octeres slot 2 remains an intentional single-controller alias.
- Direct writers recheck self/ownership. Worker selectors exclude all
  reservations and the active boar lurer. Pass-start group hygiene removes
  foreign/other-owner references before legacy release mutations. Partial
  migration releases failed shore passengers, retaining only actual cargo.
- Native exploration is zeroed AND reset before Scout-capable claims. Native
  build/percentage/hunter admissions pause during worker boarding; assistance/
  repair settings are saved/restored. No claim that a flag is an engine lock.
- Native attack type exclusions are rebuilt from reserved groups before normal
  and taunt dispatch. FREE same-type units temporarily wait too; ordinary
  attacks are not globally disabled while unrelated missions run.
- Routine defense uses <=8 FREE idle responders. Severe defense requires >=8
  live military from one enemy within home 24 and the same land zone. It may
  cancel a wholly local ashore assault/raid/relief owner, release, then acquire
  <=16 responders. Loaded/split/remote missions stay protected.
- Persistent first-reliable TC coordinates for all eight players survive TC
  destruction. Allied help checks actual live enemies around that anchor,
  claims <=12 compatible responders, checks actual count/target, then promises
  help. No arbitrary-villager or allied-under-attack substitution.
- Existing RAW44B/C/R mission evidence remains, rearmed for later missions.
  Old writer tests/maps are archival against immutable source `a5de7d85`, not
  current source with obsolete writer-site IDs. Blue's historical STOP producer
  is still unidentified; that did not block these source-supported fixes.

### Validation and limits

- **PASS:** 190 regression tests, including 27 ownership-contract tests. These
  execute actual filters, reservation/release operations, partial manifests
  and native-exclusion relative jumps, plus source invariants for enemy/zone,
  anchor persistence, actual responder count and generator synchronization.
- **PASS:** PER structure/operands/DE group domain 0..19; attack/strategy
  synchronization (1,156 matchups); naval doctrine; workbook round-trip;
  32 replay benchmarks; all 662 ownership sites audited with zero unguarded
  direct writers/global resets remaining; `git diff --check`.
- **PASS:** adversarial read-only review with accepted findings corrected:
  split/loaded severe release, exact hostile selection, converted group
  references, partial shore-passenger release, loop RuleDelta and ambiguous
  generated patch context. Tests now protect these corrections.
- Formatting-only restoration preserved original unchanged-line PER endings.
  String budget: 1,421 literals, zero writer literals, conservative eight-player
  projection 11,368 under the project's existing budget. This is not measured
  engine string-table capacity or an engine compilation claim.
- **PENDING:** fresh engine compilation and gameplay acceptance of T11.
  Existing R1/R2 and static tests cannot validate this new runtime.

### Unresolved defect ledger / next actions

| Defect | Status | Direct evidence / implementation | Acceptance / next action |
|---|---|---|---|
| Routine/convenience recall steals passengers | FIXED-PENDING-RUNTIME | Source callers + R1/R2/T8; compatible local/severe response implemented | No ordinary recall of active missions; genuine severe defense works |
| Exploration steals boarding Scouts | FIXED-PENDING-RUNTIME | R1 explore 705; budgets zero + reset before claim, positive writers gated | Reserved Scouts board; early exploration can resume after release |
| Direct worker/group conflicts | FIXED-PENDING-RUNTIME | Unsafe selectors/aliases + T7 symptoms; common guards, distinct groups, admission hold | Workers retain task; partial cargo stays owned; released units can work |
| Native worker/attack queued reassignment | INVESTIGATING | Documented suppressions/type exclusions implemented; no per-villager lock or proof of queued-order cancellation | ONE controlled T11 preserved-lobby replay, occupancy-aware early/terminal samples |
| Allied help after original TC destruction | FIXED-PENDING-RUNTIME | Persistent anchors + actual enemy/responders | Help at living/destroyed original TC; no false promise without hostile/responders |
| Historical Blue Scout STOP writer | INVESTIGATING | R2 stream established repeated STOP; old quota exhausted before event | Check recurrence in T11; not a prerequisite to implementing proven source fixes |
| Congestion, landing geometry, unload spam, Port placement, boar resumption, drop-site race, Market/Wonder salvage, crash, landing memory | KNOWN ISSUE — POST-RELEASE | Preserved observations below; deliberately no unrelated behavioral changes | Outside this ownership release unless build is fundamentally unusable |
| Existing Palintonon pack call through up-target-objects action-pack | KNOWN ISSUE — POST-RELEASE | Source/API inspection: that action is unsupported on this command | Separate supported packing correction after ownership acceptance |

1. Start a **fresh** recorded T11 match with the preserved authoritative lobby;
   identify players by selected/visible colors, never slots. Confirm T11:456.
2. Audit every reasonably reconstructable transport/migration/scout/relic/help
   episode across all players. Preserve P3B44 combined attacks and T1–T7 full/
   partial lifts. No own-TC flood, shoreline-fishing flood or routine recall.
3. Test the precise native boundary in TASK-OWNERSHIP.md: distinguish a harmful
   command to an ashore reserved unit from STOP after garrison. Existing native
   gathering/building/queued attacks may still bypass new admission controls.
4. Keep noncritical discoveries in KNOWN ISSUE — POST-RELEASE. Do not start
   another unrelated development cycle before ownership acceptance.

## Historical R4/R2 checkpoint (superseded by T11 above)

## Release-blocking recovery completed — ownership work resumes

**R4 release checkpoint, 2026-08-30:** requested invariant recovery, separate
commits, full static validation and verified deployment completed BEFORE R2
analysis. A: `3b8d534d1d1be48c1bb5a179229c353e53c37d4d`. B guard tests:
`34a53f6055ecd324d7b95368613c37871fb31fde`. The existing R3 work was preserved
in `ea8a382cb2919bed9b02fdc263f7cd3687afb886`; no new worktree or PR update.
Starting branch `recovery/p3b44-transport-only`, HEAD
`544bd843065245235227018635947e48a077f715`, installed R3:454 hash
`DD38785FB1D67813D6F9E8BF88E7D88D8B86B9C441460806C38AE10CC279CBB2`.

- Runtime diff: only hunt 28 -> 16, two operands. Food 12 and all eight self
  fallback exclusions were already present; B required tests, not duplicate
  code. Both cited historical fixes are ancestors of the pre-task checkout.
- Read-only adversarial/protected-diff review: PASS. Attack behavior changed
  beyond self-exclusion: **NO** (no attack runtime delta at all). Transport:
  **NO**. Ownership: **NO**. Migration: **NO**. Farm staffing/gather percentages:
  unchanged. All other PER files match `ea8a382` byte-for-byte. Existing T9/R3
  diagnostics are preserved, not newly implemented by this release.
- PASS: 163 regression tests (8 recovery); PER structure/operands/domains;
  attack/strategy (1,156 matchups); naval doctrine; workbook round-trip;
  31 replay benchmarks; `git diff --check`. Post-marker compiled validation
  and all 17 writer-trace tests PASS. The first sandboxed baseline run had a
  temporary-directory permission error; authorized rerun passed all 155.
- Installed **RAWAI-P3B44T10R4:455**, all **68** files independently verified,
  no missing/different/unexpected files. Source/install aggregate SHA-256:
  `C7554880AC95FE2DBB80325ABEA9130CF91C9BE9A845FC5E291A7AEDEBD57B15`.
  Plain-input SHA: `FA9E0C54BD5395B5B3EB79E19F31FE3CEE44DF008C47CCEF6124CB3C024917D1`.
  Writer-map fingerprint: `806FAFCA8EABC51B70FECA1B0F63937806BCA82A4BF1521F00B3538A9242DC90`.
  Only generated entry identity, init marker and economy file were copied.
- **FIXED-PENDING-RUNTIME**, not gameplay CLOSED. R2 predates this release and
  cannot validate hunt 16. All-player fresh-runtime acceptance remains the
  historical fish/farm and self-target/TSA flood checks specified below.
- Next: analyze supplied R2 (`20260830-182330`) with its archived R2 map, then
  continue TASK-OWNERSHIP.md. No new congestion/salvage/Port micro-fix first.

### R2 evidence audit after release — latest session

Runtime release HEAD: `4bff811431ac12de63fa1fdf7c90eccf4dcb383e` (R4:455).
This following evidence-only update does not change that runtime. Resolve
current documentation HEAD with `git rev-parse HEAD`. No push/PR update.

- Replay `SP Replay v101.103.48987.0 @2026.08.30 182330.aoe2record`,
  25,570,711 bytes, SHA-256
  `06C62FDBD658D27DDDE682FB49A8F9A90F112E7CC0D7FDD33411A935762E904E`.
  Duration 62:04. No parsed resignation; do not infer crash/end cause.
  Selected-color metadata validates the preserved Roman Red/Green/Yellow/
  Purple team versus Orange Picts/Cyan Britons/Blue Germani/Gray Gauls.
  Extreme, population 400, Fast 2.0, shared exploration; RMS id 50.
- All-player command sweep: 282,006 retained exact events, no decoder failures.
  Hull census was expanded beyond old load/unload phases using direct hull
  telemetry and passenger samples, retaining load-only failures too.

| Color | Identified hulls | Load packets | Raw loading windows |
|---|---:|---:|---:|
| Red | 4 | 24 | 7 |
| Green | 2 | 19 | 4 |
| Yellow | 2 | 16 | 2 |
| Purple | 2 | 17 | 11 |
| Orange | 1 | 14 | 7 |
| Cyan | 1 | 5 | 2 |
| Blue | 4 | 36 | 9 |
| Gray | 4 | 29 | 16 |
| Total | 20 | 160 | 58 |

- These are raw reconstructed windows, NOT 58 fully identified missions:
  19 assault-ready, 7 migration-full, 3 assault-partial, 1 migration-partial,
  3 assault-abort, 4 migration-empty-abort, 17 unload-bounded and 4 lacking a
  recorded terminal. Some missing boundary messages merge missions. Purple's
  additional partial-departure count 9 at 48:02.832 belongs inside an
  unload-bounded window because its normal hull-specific terminal is missing.
  Full/ready does not prove exact selected membership or productive landing.
- **Direct recall evidence:** all 76 retreat packets match existing RAW44O
  labels: source 1 land-defense 56, source 2 naval-defense 6, source 3 siege escalation
  12, source 4 loss-regroup 2. Orange priest 33235 starts boarding at 27:26.906 and
  is recalled at 27:37; priest 34388 starts at 37:08.684 and is recalled at
  37:18. Both attempts end in roughly three-minute recovery unloads, without
  outbound relic announcements. Routine recall must respect relic/recovery
  ownership as well as the assault/migration controller goals.
- **Corrected interpretation:** Purple at 48:32.856 is SCREEN-FIND (19),
  after reported nine-passenger partial departure at 48:02.832. Recall includes
  the original ten-unit loading roster but does NOT prove boarding interruption
  or units disembarking. Green at 55:24 includes passenger 41942 during
  WAYPOINT-WAIT (29), also route-stage evidence. The earlier user-facing
  wording calling Purple's units queued was explicitly corrected.
- **STOP stream:** Blue scout 4608 receives 283 AI_ORDER 706 packets between
  55:03.414 loading and the 55:12.050 idle-ashore sample; 276 between 57:16.740
  and 57:30.078. Both samples retain group flag 4 and distance 1 to hull 40501.
  This establishes repeated STOP plus failure of that passenger to board at
  the sample, not the exact script/native/delegated producer. Hull-ready
  messages coexist with this missing originally selected passenger. Blue's
  59:52 twenty-unit migration has STOP packets for 16 selected members and
  a partial terminal at 60:21.982 with 3 remaining; occupancy is unavailable
  for each stopped member, so normal post-garrison cleanup remains a possible
  explanation for some of those packets. Do not blanket-label them preemption.
- **Coverage:** before 09:00 each player has only one invocation each of
  setup sites 10/11/12; R1's early recurring cleanup spam is absent. Gray
  exhausts the total quota at 37:00.648, Blue at 48:29.402, Purple at 56:06.164;
  temporary rate gaps also occur. No RAWAI marker or RAW44W map survives.
  Zero players pass fingerprint verification; the new exact writer-source
  attribution remains withheld. Preserve user-reported R2 + archived map/
  deployment evidence, but do not bypass the analyzer's identity requirement.
- **Other outcomes retained:** 7 scout-candidate missions reject all five
  paths; a Green candidate mission records 3 clear points with unload commands.
  One public assault landing-completed window is present. Six relic outbound
  and four return announcements remain positive evidence. They do not close
  every landing/drop-site/route defect, and do not authorize a navigation fix
  in the ownership release.
- **Artifacts outside repository:** `.analysis\replay-20260830-182330-t10r2-full.json`
  and `.analysis\p3b44t10r2-{command-stream,exact,transport-audit,task-ownership,summary}.json`,
  plus `p3b44t10r2-transport-audit.txt`; matching archived
  `p3b44t10r2-writer-trace-sites.json`. Existing `audit_writer_replay.py` now
  includes sample/public hulls and no longer writes hard-coded R1 conclusions.
  Its raw automated classifications must be read with the boundary limitations
  above: a missing terminal does not imply ownership until match end, and a
  later sample from a different hull is not proof about an earlier mission.
- **Status/next:** ownership remains OPEN; actual recall conflicts are already
  established, harmful STOP producer/protection semantics remain unresolved.
  R4 has the delayed identity delivery introduced in R3 but not exercised by
  R2. Verify fresh R4 identity and recovered invariants, then use occupancy-
  aware evidence for the common ownership/preemption implementation. Do not
  re-open historical fallback absence as an explanation: all 8 guards were
  present. New benchmark is evidence-only; 32 benchmark validations PASS.

**Latest user instruction, 2026-08-30:** "Once you receive the R2 replay,
this directive takes all precedence before analyzing the R2 replay data."
R2 (`20260830-182330`) supplied the trigger. Recovery above is complete; the
following retained requirements document the release, not a request to repeat it.
This section overrides conflicting priority/next-action text elsewhere below.

**Pre-edit source/deployment audit:** installed R3 matches all 68 generated
files, SHA-256 `DD38785FB1D67813D6F9E8BF88E7D88D8B86B9C441460806C38AE10CC279CBB2`.
The directive's lost-fix premise is only partially applicable: food already
clamps to 12 and all eight fallback self-exclusions are present, inherited
directly from the two cited commits (both are ancestors of current HEAD).
Commit `078da6527906eec1101a9848cc1fcc4f66555b77` subsequently raised hunt 16
to 28. Restore hunt 16 as now directed, retain food 12 and existing self
guards, and add the requested focused/mutation tests in separate A/B commits.
Do not claim missing self guards caused the current runtime symptom. This
source evidence does not disprove the observed own-TC/passenger behavior.
R1-R3 intentional telemetry/evidence is checkpointed separately BEFORE causal
patches, not silently included in either restoration commit. No new T9 work.

### Recovery B — protection retained; FIXED-PENDING-RUNTIME acceptance

- Historical source: `8998cdedc1b5942ec6b93b60b1f33a0188238c94`; every explicit
  military fallback 1..8 already retains its top-level `gl-self-player-number
  c:!= N` guard. No `rawai-military.per` change is needed or manufactured.
- Historical symptom/cause: self is not ally in `stance-toward`, admitting
  self in an unguarded fallback and producing own-TC TSA orders. Current
  contradictory evidence: these guards were NOT lost; the observed ongoing
  own-TC behavior remains an ownership/runtime investigation, not proof of
  this already-guarded fallback failing.
- Tests: four additional source-executed/invariant tests cover all 64
  candidate/self combinations; valid enemy selectable, self rejected even
  when in-game/non-allied/building-owning; valid current targets retained.
  Removing each guard reproduces self selection and fails the invariant.
  Self identity is initialized once from `my-player-number` before military
  rules; automatic explicit writers are scanned across all runtime files.
  Eight focused A+B tests PASS. No attack dispatch/ranking/ownership changes.
- Audit boundary: other target writers are normal `up-find-player enemy`,
  preferred-target save/restore, and explicit user taunts 61..68. Taunts are
  not automatic fallbacks and remain unchanged. Do not generalize fallback
  exclusion into an unproved claim that no other writer can ever select self.
- Acceptance/next action: validate/deploy the recovered cap plus retained
  target invariant, then fresh all-player self-target/TSA flood acceptance.
  Existing R2 can diagnose pre-fix ownership, not validate the new cap.

### Recovery A — FIXED-PENDING-RUNTIME

- Historical source: `56959e6c45fd688710abc3f167aade7262dd4d2f`.
- Preserved pre-task checkpoint: `ea8a382cb2919bed9b02fdc263f7cd3687afb886`.
- Symptom/cause: historical shoreline-fish/farm command contention from an
  uncapped food distance. Contradictory current evidence: food already had 12;
  only the later hunt-28 deviation needed restoration to the requested 16.
- Implementation: exactly two numeric operands in `rawai-economy.per`,
  hunt 28 -> 16; existing food 12 retained. No other runtime source changes.
- Tests: four source-executed/mutation tests in `tools/test_release_regressions.py`.
  FAIL on pre-patch hunt 28; PASS after restoration. Both caps precede native
  SN publication, preserve within-limit values and mutate only their own goal.
  Protected diff preserves farm staffing, gather percentages, transport,
  migration, passengers, attack/defense and ownership.
- Acceptance/next action: full release validation/deployment after B's guard
  tests; then all-player fresh-runtime checks for historical food/hunt command
  floods. This source change does not establish that R2 contains that cause.

Authority: user attachment
`C:\Users\LostSoul\.codex\attachments\ce70220e-7f9c-4f58-a936-c6dde9510419\pasted-text.txt`,
SHA-256 `81BBF627F3AC41D9A3BD831A28EB2D537754D38EB248911E65E5736FBE0CD1EE`.
The actionable requirements are retained here for cold-agent handoff:

- **A, known historical cause / ROOT-CAUSE-PROVEN:** uncapped food/drop
  distance let native economy assign shoreline fish while the farm controller
  repeatedly retasked the same Villagers, causing command flooding. Recover
  `56959e6c45fd688710abc3f167aade7262dd4d2f`, "Cap food and hunt drop distances
  at town perimeter", in current `rawai-economy.per`: clamp
  `max-food-distance <= 12` and `max-hunt-distance <= 16`. Use rules equivalent
  to `(up-compare-goal NAME c:> CAP)` -> `(up-modify-goal NAME c:= CAP)`.
  First check current equivalent protection; retain it if complete, restore
  missing/partial semantics only. No farming, hunting, fishermen, migration,
  worker-ownership, gather-percentage or farm-staffing redesign.
- **B, known historical cause / ROOT-CAUSE-PROVEN:** explicit fallback
  candidates 1..8 tested only not-allied, which also admits self, allowing
  `sn-target-player-number = self` and native TSA orders to the AI's own TC.
  Recover `8998cdedc1b5942ec6b93b60b1f33a0188238c94`, "Exclude self from
  target-selection fallback", in current `rawai-military.per`. Audit EVERY
  current explicit fallback, not old line numbers: each candidate N = 1..8
  must require `(up-compare-goal gl-self-player-number c:!= N)` before setting
  the target. Preserve normal enemy iteration, attack cadence/strength,
  ownership/grouping, transport and ranking beyond rejecting self.
- These are known recovered fixes, NOT new INVESTIGATING items. Do not
  rediscover causes, add telemetry first, or require another replay before
  implementation/deployment. On implementation mark FIXED-PENDING-RUNTIME;
  do not claim runtime closure from static checks or the pre-fix R2 replay.
- Use two independently revertible causal commits: "Restore bounded food and
  hunt gather distances", then "Exclude self from fallback attack targets".
  Limit each to its PER change, focused tests, appropriate changelog/handoff
  and marker material. Do not blindly import historical marker/changelog
  content or neighboring P3B39/P3B40 changes. Manually reproduce invariants
  if old patches no longer apply. No ownership behavior in either commit.
- A tests: values above 12/16 clamp; values within bounds do not expand;
  unrelated gatherer percentages are unchanged. B tests: for EVERY 1..8
  candidate, in-game + non-allied + buildings still rejects self; a valid
  nonself hostile stays selectable. Add a structural invariant preventing
  any future explicit fallback from omitting self-exclusion.
- Protected diff against the pre-task recovery baseline: A changes no
  transport/migration state machine, attack/defense state, passenger selection
  or farm staffing beyond caps. B changes no dispatch, `attack-now`,
  `up-retreat-now`, `up-reset-attack-now`, military percentages, target ranking,
  transport routes, defense thresholds or task ownership. Preserve T1-T8
  recovery improvements, working attacks/lifts and TASK-OWNERSHIP.md evidence.
- Run the FULL current regression suite, PER structure and operand/domain
  validation, attack/strategy validation, replay benchmarks and
  `git diff --check`. Manually audit all occurrences of `max-food-distance`,
  `max-hunt-distance`, `sn-target-player-number`, `gl-self-player-number`.
- After both commits/static PASS, assign the next unique recovery marker,
  deploy immediately from this checkout, verify EVERY installed file and
  aggregate hash. Do not leave fixes committed but undeployed or wait for
  ownership architecture. Leave a clean tree except documented user-owned
  exceptions, while preserving preexisting work (see qualification below).
- Fresh ordinary replay acceptance is all-player: no sustained historical
  shoreline-fish/farm retask flood, no extreme Villager stream from that
  mechanism, no self target, no self-target military/TSA own-TC flood.
  Inspect repeated TC streams without misclassifying legitimate garrison,
  deposit, defense or production-related orders. R2 predates these fixes.
- Immediately resume common task ownership/preemption afterward. No new
  transport micro-fix, Port placement, boar recovery, Market/Wonder salvage,
  migration drop-site or landing-memory work first unless recovery exposes
  a blocking regression. No additional T9 diagnostic implementation in these
  commits; do not use this release recovery to expand diagnostic scope.
- Required implementation report: starting branch/HEAD/marker/install hash;
  A historical commit/current files/exact invariants/tests; B historical
  commit/all fallback audit/self-exclusion/tests; protected-diff YES/NO for
  attack beyond self-exclusion, transport, ownership, migration (all NO);
  regression count/PER/strategy/benchmarks/diff results; new marker,
  source/install aggregate SHA-256, file count and identity result. End exactly
  `P3B39/P3B40 REGRESSIONS RESTORED — FIXED-PENDING-RUNTIME — OWNERSHIP WORK RESUMES NOW`
  or, for a genuine implementation conflict,
  `REGRESSION RECOVERY BLOCKED — exact conflicting evidence`.

**Current-state qualifications, reported to user:** the attachment assumes
installed T8 and undeployed T9 diagnostics. Actual last verified installation
is T10R3:454 (identity below), compiled from input that already includes T9
diagnostics; T9 was not separately installed. Do not silently roll back the
current diagnostic runtime based on that stale premise. Preserve existing
work and isolate the two recovered behavioral deltas; if literal exclusion
requires removing already installed work, resolve that conflict explicitly.
Current HEAD is `544bd843065245235227018635947e48a077f715`; intentional R1-R3
telemetry/evidence edits remain uncommitted, including `rawai-military.per`.
Before recovery commits, establish their exact pre-task baseline and keep them
separate from the causal fixes; never absorb them silently or discard them to
obtain a clean tree. The prior directive-receipt turn changed HANDOFF ONLY;
implementation is now authorized by R2 arrival. R2's archived writer map remains
`.analysis\p3b44t10r2-writer-trace-sites.json`, outside the repository.

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
- T8 replay-audit starting/current HEAD: `544bd843065245235227018635947e48a077f715`
  (`Commit intentional investigation-breadth project rules`). Worktree was clean before
  the initial evidence-only audit. The subsequent Blue screenshot investigation
  added uncommitted T9 diagnostics. The user's subsequent priority correction
  produced and installed T10 writer telemetry from this SAME worktree. No new
  development directory, commit or PR update was made; AGENTS.md is unchanged.
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

**Current: `RAWAI-P3B44T10R4:455`, 68 files**, deployed and independently rechecked
with `tools/sync_test_ai.py --writer-trace`. Full generated/installed SHA-256:
`C7554880AC95FE2DBB80325ABEA9130CF91C9BE9A845FC5E291A7AEDEBD57B15`.
There are zero missing, different or unexpected runtime files in this mode.
The source-site map fingerprint is
`806FAFCA8EABC51B70FECA1B0F63937806BCA82A4BF1521F00B3538A9242DC90`.
R4 preserves R3 telemetry and restores only hunt 16; food 12 and all eight
self-target fallback guards were already present. Runtime acceptance pending.
T10:451 **FAILED engine compilation** with user-reported ERR6003, String table
full, at rawai-init-goals.per:362. T10R1 reuses string constants; subsequent user
screenshots show RAW44W output in a running match, but also inappropriate idle
logging. R1 replay now confirms quota exhaustion before boarding and missing
startup marker/map messages. T10R2 fixes the idle trace gate; T10R3 delays,
staggers and bounds identity announcements. R3 runtime acceptance is PENDING.
Preserved R1 map for the user's running match/replay:
`G:\Projects\Codex\Rome at War AI\.analysis\p3b44t10r1-writer-trace-sites.json`.
R2 map is likewise preserved as `.analysis\p3b44t10r2-writer-trace-sites.json`.
Use the matching historical map, NOT the current R4 map, for prior recordings.

This is an **in-memory diagnostic compilation of the documented checkout**,
not another editable workspace. Edit the existing PER sources and
`tools/writer_trace.py` here, never the generated installed copy. The checkout's
plain PER input retains the T9 marker but now includes the restored hunt cap.
Reproduce deployment with `--writer-trace`; omitting it removes writer telemetry.
Regenerate `writer-trace-sites.json` after any runtime-source change; deployment
rejects a stale map. T9 was never installed as a separate test.

### Historical T8 identity

- Marker: `RAWAI-P3B44T8:449`.
- Runtime files: 68.
- Installed T8 / pre-T9 source SHA-256:
  `0166808361591E65F29FA4B0770DB90A1C68D1F4A200F220C28C76F13A6D2F92`.
- Historical T8 deployment check: all 68 runtime files were byte-identical, with no missing,
  different, or unexpected runtime files. Relative to T7, exactly
  `rawai-military.per`, `rawai-tauntcommands.per` and `rawai-init-goals.per`
  were copied from this worktree by `tools/sync_test_ai.py --apply`.
- Installed directory:
  `C:\Users\LostSoul\Games\Age of Empires 2 DE\76561198053747760\mods\local\Rome at War AI\resources\_common\ai`.
- Before editing, the full T7 source/deployment hash was verified as
  `69C30C50661D3E1E8A1F8DC081C63E80D0C899D8E695B16D3E02F95B910B7738`.
  T8 is diagnostic only; it has no fresh-match behavioral acceptance yet.

Historical T9 plain input, **not separately deployed**, now preserved in the
R3 checkpoint `ea8a382`: `RAWAI-P3B44T9:450`, 68 files,
SHA-256 `3BB032283550D1C549431E8F3921BCCEA685747F84C8CEF9FB67D678BE4AABE1`.
The T9 preparation check identified three differences from the then-installed
T8: `rawai-customconstants.per`, `rawai-init-goals.per`, `rawai-military.per`;
no missing/unexpected files. T9 only observes terminal transport failures and
publishes previously private assault hold reasons. It is not a congestion or
ownership fix; engine compilation, log delivery and gameplay validation remain
pending. Do not attribute the T8 replay to this untested source.

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

**Priority correction:** passenger command ownership is the immediate work,
not further congestion case studies. T10 now traces competing rule calls,
group/reservation operations and native policy/delegation while assault or
migration boarding is active (plus explicit reservation boundaries and
single-use policy setup). Analyze the next T10 replay with its exact writer
map. Do not re-request the already established T8 siege-recall attribution.

T8 replay is now audited: all 100 retreat packets map to 56 tagged invocations.
Red's 54:03 siege-escalation call is established as an actual boarding-order
overwrite, not merely a capable source rule. Worker/native attribution is
still unresolved. Red's newly reported late obstruction is a migration-stage
coverage gap; manual clearance coincides with the loading deadline, so the
unassisted departure outcome is not recorded. See the T8 evidence below.
The user's Blue screenshots at 49:11 and 66:50 exposed missed physical
obstructions: a command-episode census was incorrectly treated as sufficient
obstruction coverage. Blue's first window has no issued departure; its second
contains failed migration route/recovery attempts. Both remain INVESTIGATING.

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

### Red and Blue Port crowding outside assault-clearance coverage

- **Status:** INVESTIGATING. The physical symptom is accepted; missing migration
  coverage is source-established, but the unassisted departure outcome is absent.
- **User-visible symptom:** near the end of T8, Red's loaded Transport was blocked
  by other friendly Transports; the user manually moved the blockers away.
  Blue also has user-observed blockages at 49:11 and 66:50, preserved with the
  two screenshots and exact command windows in the T8 evidence below.
- **Direct evidence:** at 66:24 replay playback shows four villagers aboard the
  migration hull and two adjacent empty Transports at Red's Port. Recorded moves
  of 48064/31880 occur at 66:30-32. Hull 31691 starts its route at 66:31.236 and
  reports distance 52 at 66:46, 30 at 67:01, 15 at 67:17, and zero at 67:32.
- **Cause/limit:** T3's exact-blocker clearance belongs to assault departure,
  not migration loading/departure. However, the first migration departure order
  coincides with its normal 30-second partial-load deadline and manual clearance.
  This does not prove an issued departure remained stuck before intervention.
  Do not dismiss the visible obstruction or silently label normal boarding wait
  as a measured departure-path stall. Keep both accounts together.
- **Instrumentation/tests:** existing RAW44B snapshots record 18 remaining at
  66:04 and 16 at 66:31; sampled passengers retain group 4 and enter orders.
  Exact hull positions/progress and eligible blocker states during this loading
  phase are not logged. The subsequent migration reaches a landing candidate
  just before the 67:33 replay cutoff, not a proven economic settlement.
- **Implementation:** prepared T9 terminal-only diagnostics, not deployed.
  No navigation, blocker selection, ownership or recovery behavior changed.
- **Acceptance criterion:** an unassisted obstructed migration records phase,
  actual no-progress condition, safe exact blocker clearance and restored
  boarding/departure; occupied, task-owned, threatened and wrong-water blockers
  remain protected, and ordinary loading deadlines/successes are preserved.
- **Latest result:** crowding/coverage-gap evidence PASS; autonomous recovery
  FAIL in the user-observed Blue cases, causal gate/blocker eligibility still
  unresolved. Orange's independent assault clearance succeeds in T8.
- **Next action:** keep separate from the architectural ownership patch. Use a
  bounded phase-aware migration observation or controlled unassisted reproduction
  to distinguish blocked passenger access, blocked departure and normal loading
  wait before extending clearance. Do not ask the user again for blocker type/time.
  The generic idle-berth utility requires all transport controllers idle; simply
  removing that gate risks retasking active owners and is not an accepted fix.

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

- **Status:** INVESTIGATING overall. T8 proves the siege-escalation boarding
  overwrite and identifies every recorded global-recall caller; worker/native
  producing paths and the complete safe ownership mechanism remain unresolved.
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
  T10 additionally traces 351 command/group/native-policy sites, selected-object
  identity/flag and pre/post boarding state/hulls, bound to a replay-visible
  exact source map. See the T10 section for limits and queued-packet handling.
- **Implementation:** diagnostic commit `d10f33e`, deployed T8. No behavioral
  ownership fix implemented. Salvage D retains offline retreat events and
  generic compact chat categories. New `tools/audit_task_ownership.py` and its
  packet/lifecycle tests retain replay-wide command evidence; raw artifacts
  remain external. T10R3:454 writer diagnostics are now installed; gameplay
  ownership decisions remain unchanged and the new tooling is uncommitted.
- **Acceptance criterion:** shared ownership lasts until explicit complete,
  abort, loss, release or verified emergency preemption; ordinary military and
  economic selectors respect it; routine defense acquires bounded free units;
  severe hostile defense cancels old owners cleanly; allied relief uses live
  hostile presence near persistent first-TC coordinates, even after TC loss.
  Pass the nine section-H contracts plus all-player fresh runtime validation,
  preserving ordinary attacks, partial/full lifts, relics and screened landings.
- **Latest result:** T8 caller attribution PASS: 100 packets / 56 tagged calls.
  Red's 54:03.506 source-3 recall interrupts passengers 40149, 43815 and 47309
  during boarding; later retries corroborate that they remain ashore. All 56
  candidate snapshots retain group 4. Broad ownership acceptance remains FAIL /
  unresolved, not fixed by the diagnostics. See TASK-OWNERSHIP.md for exact
  sequences and qualifications. Worker/native attribution is still pending.
  R1 adds scout-specific evidence: source-1 land defense recalls Green/Orange
  reserved scouts; exploration order 705 overwrites Purple/Orange boarding
  while reservation flag 4 remains visible. Do not relabel these as workers.
- **Next action:** check R3's corrected off-mission gate and delayed identity, then analyze
  writer traces using the map for that replay's actual build. R1's map is
  preserved externally; its early idle logging may exhaust coverage before
  useful boarding. Distinguish
  script-selected, script-delegated and autonomous native orders in a controlled
  engine test. Use T8 for the six recall writers but do not claim it alone can
  settle worker attribution. Use the source-map-verified T10 events and retain
  ambiguous queued issuers instead of choosing the closest log. Establish the minimum protection mechanism, then
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

### P3B44T8 replay audit (2026-08-30)

- Source: `SP Replay v101.103.48987.0 @2026.08.30 154021.aoe2record`, SHA-256
  `C7BDFAF53DE72F03012C5AD88F4B930E9B7670A07CDC96490489F7428F2CE29F`.
  Duration 67:33; zero decoder failures. No recorded resignation; ending cause
  is not inferred. Players 2-8 publish T8:449, and the complete installed/source
  runtime matches the hash above. Selected-color metadata agrees with the
  preserved Red/Green/Yellow/Purple Roman team and Orange/Cyan/Blue/Gray team.
- All 3,476 SPECIAL/UNGARRISON records were screened. Transport hull union 19,
  190 loads, 130 point unloads, 47 alternating load/unload phases and seven
  terminal load-only phases. Never-loaded empty blockers are not in that hull
  union. Boarding audit: 58 windows, 354 passenger-window instances. Command
  phases and orders are not voyage-success acknowledgments.

| Color | Boarding windows | Full-load corroborated, no conflict | Conflict + later ashore evidence | Unresolved | Retreat packets |
|---|---:|---:|---:|---:|---:|
| Red | 11 | 23 | 6 | 37 | 5 |
| Green | 4 | 0 | 0 | 31 | 16 |
| Yellow | 3 | 0 | 1 | 2 | 12 |
| Purple | 3 | 0 | 3 | 9 | 26 |
| Orange | 14 | 2 | 0 | 82 | 14 |
| Cyan | 1 | 0 | 0 | 1 | 13 |
| Blue | 18 | 3 | 22 | 128 | 1 |
| Gray | 4 | 0 | 2 | 2 | 13 |
| Total | 58 | 28 | 34 | 292 | 100 |

- Unresolved includes 108 conflicts whose pre-boarding timing/owner continuity
  is unproven. No individual death/unavailability is proven by command absence.
  The 56 candidate snapshots (26 military, 30 migration) all retain flag 4.
- All 100 retreat packets match 56 RAW44O invocations: land defense 28/47,
  naval defense 16/32, siege escalation 11/19, loss regroup 1/2 (calls/packets).
  Sources 5/6 absent. One call can emit consecutive land/naval packets at the
  same clock; do not misclassify the second packet as untagged/native. Red's
  source-3 boarding overwrite is detailed in TASK-OWNERSHIP.md.
- Orange 40825 is the only logged departure-congestion episode: blocker 40598
  ordered at 53:43, verified clear at 53:52, departure resumed at 54:00. It reaches
  landing at 54:17 but times out at 55:02. Clearance PASS is not voyage completion.
  Red's late migration has no such detection; manual intervention and phase
  timing are preserved in its separate ledger entry above.
- Seven assault landing windows have zero guard refreshes targeting the active
  hull. Orange completes at 41:49, Red at 65:33; five other windows time out.
  Nine migration landing-candidate missions yield 18 clear events with matching
  same-second unloads; one wrong-zone and 20 path rejections emit no such unload.
  All nine have zero active migration-hull guard overlap. Landing-screen and
  escort protections survive these checks; settlement/drop-off success is not
  established by them. Five exact relic outbound and four return readiness
  events occur; unmatched/pending missions remain unresolved.
- Raw artifacts stay in `G:\Projects\Codex\Rome at War AI\.analysis`:
  `p3b44t8-command-stream.json` (825,076 retained commands/chats, exact arrays),
  `replay-20260830-154021-p3b44t8-full.json`,
  `replay-20260830-154021-p3b44t8-exact.json`, `p3b44t8-transport-audit.txt/json`,
  `p3b44t8-task-ownership.json`, and `p3b44t8-recall-sources.json`.
  External `audit_p3b44t8.py` orchestrates the existing repository decoder and
  legacy lifecycle helpers with their ID-magnitude normalization disabled.
  Join recall sources by exact retreat sequence; the generic ownership report's
  historical `likely_source` text is not the authoritative T8 source attribution.
- Reproduce exact stream/ownership with `tools/audit_task_ownership.py`, the T8
  replay, parser root `../../.analysis/replay_parser_kjir`, T8 transport audit,
  and external output. For caller attribution match preceding same-player
  RAW44O labels in stream order (first packet 14-38 ms later here); allow the
  same label on its adjacent same-clock land/naval bundle only. Preserve all
  unmatched labels/packets rather than inferring native origin.
- Computer Use playback verified the Red Port scene and cargo rather than
  inferring physical positions from orders. Replay left paused at 66:50.
  That initial Red audit changed no gameplay code, marker, installed files,
  Git commit or PR; the later prepared T9 diagnostic changes are recorded below.
- Evidence validation: PASS, all 30 replay benchmarks validate and
  `git diff --check` passes. No full regression suite was run for this
  documentation-only audit. Intentional changes are HANDOFF.md,
  TASK-OWNERSHIP.md and replay-benchmarks.json; AGENTS.md remains committed
  and unchanged. No runtime defect is closed by these document checks.

### T8 missed Blue obstructions / prepared T9 diagnostics

- **Coverage correction:** every reconstructed command episode is not every
  physical obstruction. The 19 mission-linked hulls exclude never-loaded empty
  blockers. Missing congestion logs cannot establish a clear path or successful
  movement. Both user observations are accepted; the screenshot does not itself
  identify a hull ID, and enemy selection in the 66:50 image does not expose cargo.
- **49:11:** Blue hull 35026 receives an assault load of ten at 48:33.312,
  then a home unload at 49:42.634, with no intervening hull departure order.
  Similar load-to-home-unload waits recur at 29:47, 32:49, 35:43, 38:47,
  42:00 and 45:28. An unavailable route-screen Scout is a hypothesis, not a
  finding: T8's relevant hold reasons are private and absent for Blue.
- **66:50:** the corresponding migration episode is hull 36912: seven aboard
  by the partial-load terminal at 64:31.600; six orders to (134,99) from
  64:31.634 through 65:48.306; six home unloads to (204,16) from 66:03.632
  through 67:21.640. The screenshot falls within failed return attempts.
  Migration route/return retries have no active blocker-clearance hook.
- **Broader re-screen:** the same hull also issues six orders to (113,0)
  from 59:42.694 through 60:59.338 and a home unload at 61:14.666; this is an
  additional failure-pattern candidate, not independently proven collision.
  Repeated orders alone are insufficient: Red 31341 repeats nine departure
  orders at 63:47-64:54 yet lands remotely at 65:03 and completes at 65:33.
  Yellow/Purple/Cyan/Gray's unresolved boarding is not declared successful
  merely because no repeated movement orders or blockage tags were found.
- **External evidence:** `.analysis/p3b44t8-blue-4911.jpg`, SHA-256
  `4E0DF49D3E008D2F93C2EA027FC24F76B102429AFACFD15FC93536EE17156DF1`;
  `.analysis/p3b44t8-blue-6650.jpg`, SHA-256
  `EFF7EF6100410DADDFA1553979B58C2D4581BA5DFA1C61D80EAA48126C0219F9`.
  Paths are relative to workspace root, outside this AI-only repository.
  `.analysis/inspect_t8_congestion.py` reproduces exact Blue windows and the
  all-player repeated hull-command screen from the preserved command cache.
- **T9 diagnostic contract:** RAW44C migration terminal phase 1 = exhausted
  route progress; phase 2 = occupied return failure. Both record exact hull ID,
  actual position, origin, cargo, idling and group; only phase 1 records a
  distance because return checks have no established distance reference.
  Each observer uses the existing owner's selected hull and three private
  scratch goals (1163-1165); no searches, commands, timers or controller writes.
  Identical terminal conditions leave the state immediately, bounding output
  to one snapshot per failed leg. Assault ready logs identify the exact hull;
  the accompanying target value is the load quota, not an independent cargo read.
- **Public assault hold codes:** 1 no safe approach; 2 defended corridors;
  3 no screening ship; 4 screen under fire; 5 screen waypoint unreachable;
  6 screen lost; 7 defended route revealed; 8 landing scout under fire;
  9 landing unreachable; 10 landing scout lost; 11 defended landing revealed;
  12 landing timeout. Each existing terminal emits hull + reason once.
- **Adversarial read-only review:** ACCEPTED absent public hold reasons,
  misleading inherited return distance, and command-census overclaim; addressed
  as above. Moving every nearby ship is REJECTED: active/reserved/occupied
  blockers are not established safe to retask. Exact neighbor identity, task
  eligibility and unassisted physical clearance remain unresolved, not covered
  by these observers. Preserve successful Orange clearance and Red landing.
- **Validation:** PASS PER structural/operand checks, 138 regression tests,
  unchanged T7 gameplay-program fingerprints after removing observational
  additions, 30 replay benchmarks, and whitespace check. T9 runtime validation
  PENDING; blockage status INVESTIGATING. Installed T8 remains untouched; no
  new long replay is requested merely to substitute more logs for resolution.

## Validation performed

### R1 18:10 replay audit and R3 identity delivery (latest session)

- Replay `SP Replay v101.103.48987.0 @2026.08.30 181054.aoe2record`, 22:54;
  SHA-256 `FE6D9AAFF07A6478A29BAD07D4FC210F5168B11F2A116340DB4C9A2175CFA91A`.
  User identifies it as R1. Selected-color metadata maps replay IDs 1..8 to
  Red/Green/Yellow/Purple/Orange/Cyan/Blue/Gray, matching the established teams.
  Extreme, 400 population, Fast 2.0, shared exploration; resignation at 22:54.
- **Breadth:** 66,324 retained exact command/chat events, zero packet-array
  decoder failures; all 11 command-linked hulls / 15 boarding episodes. Every
  episode has one passenger and corresponds to scout-ferry selection, not
  mining-worker migration. No assault boarding occurs before cutoff.

| Color | Boarding episodes | Full-load confirmations | Empty aborts |
|---|---:|---:|---:|
| Red | 2 | 2 | 0 |
| Green | 2 | 0 | 2 |
| Yellow | 1 | 0 | 1 |
| Purple | 1 | 0 | 1 |
| Orange | 2 | 0 | 2 |
| Cyan | 1 | 0 | 1 |
| Blue | 3 | 3 | 0 |
| Gray | 3 | 0 | 3 |

- **Root-cause evidence, scout preemption:** all 20 DE_RETREAT packets match
  source-1 land-defense labels. Four intersect boarding: Green scout 4643,
  hulls 31508/31734 at 15:21.180 and 18:48.512; Orange scout 4646,
  hulls 30975/31410 at 12:34.644 and 14:38.636. Labels expose migration state 3;
  retries/samples establish still-ashore passengers. The source invokes global
  `up-retreat-now` without transport cancellation/permission. Scout interference
  subcause ROOT-CAUSE-PROVEN; common ownership implementation remains OPEN.
- **Exploration task:** Purple scout 4645 begins boarding hull 31108 at
  13:07.784; exploration orders start 13:08.876 and repeatedly replace retries.
  Orange 4646 also receives exploration during both lifts. Source constants
  identify order 705/action 605 as exploration, not ordinary move. Purple's
  13:11.760/13:38.422 snapshots show exploration with flag 4 retained. This is
  a second competing task, not proof of a worker-economy writer. Exact native
  versus script-delegated boundary/release mechanism still needs an engine
  comparison before a guessed ownership lock is implemented.
- **Separate timeout class (outside ownership patch):** five aborts have no
  competing packet and retain enter order 717 while approaching: Yellow
  distance 60->21, Cyan 58->19, Gray 82->49 / 70->44 / 74->36. The roughly
  30-second load deadline expires before boarding. Eventual reachability and
  safe replacement timing are not demonstrated. No timeout/navigation patch.
- **Result limits:** five full-load confirmations do NOT prove productive
  landing/settlement. Red's remaining self-visible diagnostics include rejected
  scout landings and return failure. Worker/assault acceptance is untested.
  Initial full-object-header parse fails in the current parser; no unit-type
  claims are based on ID magnitude. A progress update incorrectly called the
  passengers villagers; this was corrected explicitly to scout ferries.
- **Spam cause confirmed:** all players emit `RAW44W coverage gap: 0` at
  05:40-05:41; no subsequent begins/resumes, first boarding only 10:05.882.
  The user's observation of stopping around Port completion is preserved;
  source/trace establish the stop condition was quota exhaustion, not Port
  construction. BUILD packets do not establish actual completion timestamps.
- **New diagnostic defect — FIXED-PENDING-RUNTIME:** no RAWAI marker, map0..3
  or schema survived startup (also absent from raw replay bytes). The first
  recorded chat is Gray's unmatched `end:328`. All 4,118 incomplete/unverified
  brackets remain unverified; zero players pass fingerprint checks. Do not
  bypass identity validation. R1 source identity rests on user report and the
  archived deployment, not an embedded fingerprint. Exact engine loss/queue
  mechanism remains unproven.
- **R3 implementation:** retain R2 gating, all 351 sites and gameplay program.
  Send marker plus four map fragments after startup: nominal initial times
  8..29 seconds by player, three attempts, 30 seconds apart, independent of
  writer budget. Fifteen extra identity records per player total; two private
  scratch goals 13010/13011, included in collision checks. This repairs the
  startup-only delivery assumption, not gameplay ownership. Literal count
  1,466 total / 19 writer (project limits 1,500/32).
- **Validation:** PASS 155 tests (17 writer tests), compiled PER checks,
  original gameplay/jump equivalence, literal guard, bounded staggered identity;
  PASS 31 replay benchmarks and whitespace. PASS deployment and independent
  recheck of all 68 files. Read-only adversarial review ACCEPTED no startup
  delivery assumption, quota-independent bounded retries, and preserved R1/R2
  maps; REJECTED treating missing labels as native proof. R3 runtime PENDING.
- **Artifacts:** external `.analysis\p3b44t10r1-{command-stream,exact,
  transport-audit,task-ownership,summary}.json`, transport-audit.txt, and
  `replay-20260830-181054-t10r1-full.json`. Orchestration is the external
  `audit_writer_replay.py`, reusing exact decoder + established all-player audit
  with magnitude normalization disabled. `summary.json` retains every episode,
  exact recall packet/label, exploration overwrite and coverage cutoff.
- **Next:** use the matching R1/R2 historical map for existing recordings; R3
  for the next test. Verify identity and useful boarding traces. Prioritize
  native exploration handoff and reservation-aware routine defense in the
  authorized shared ownership work; do not lose the established scout causes
  while resolving the still-unattributed T7 worker WORK cases. No new workspace,
  gameplay patch, commit, push or PR update in this audit/diagnostic repair.

### T10R2 off-mission trace spam (previous session)

- **Status:** FIXED-PENDING-RUNTIME. **Symptom/direct evidence:** user screenshots
  at 04:51/04:54 show Red `RAW44W end: 41`, assault/migration state 0, hulls -1;
  04:55 shows Orange with the same site/state values. User reports repetition.
  Still images alone cannot count emissions (the first two may show retained
  chat); the compiled unconditional rule independently establishes repetition.
- **Root cause:** site 41 (`rawai-general.per:43`) excludes
  `migration-boarding-group` from generic villager cleanup, then mutates group 0.
  The compiler matched the reserved group's name anywhere in the action block,
  misclassifying an exclusion as an ownership change. The exemption bypassed
  boarding gating, generating 12 chat records each qualifying pass until the
  96/minute or 512-total invocation budgets stopped it. Not literally unbounded,
  but capable of spending coverage before the first mission.
- **Implementation:** classify only actual create/flag/reset command destination
  operands. All 351 sites audited: remove site 41's false exemption and include
  five previously omitted real hull/passenger mutations (131/132/197/233/240).
  There are now 49 genuine reservation-boundary sites. Site 41 remains traced
  during boarding; no gameplay rule, quota, context field or source ID removed.
- **Contradictory/limiting evidence:** unchanged state values do not establish
  absence of a competing command. Do not suppress invocation evidence merely
  because transport state/hull stayed the same; repeated commands can be causal.
  White `refresh check vills/update facts timer` messages come from older
  rawai-timers.per 15-second rearming logs, separate from RAW44W. Left unchanged
  in this bounded classifier repair; blanket timer-log cleanup is outside it.
- **Instrumentation/tests/review:** PASS 154 tests, including an exact site-41
  false-positive fixture, all four reservation aliases/acquire/release forms,
  all-site gating/quotas, string budgets, and original-program/jump equivalence.
  PASS generated PER checks, 30 benchmarks and whitespace. Read-only adversarial
  review ACCEPTED missing real mutation aliases and R1 map preservation;
  REJECTED deleting site 41 or logging only state changes (loses writer evidence).
- **Acceptance/latest result:** PASS all 68 deployment hashes and independent
  read-only recheck. R2 must show no recurring site-41 logs with both missions
  idle, retain that caller during boarding and retain true reservation changes.
  Gameplay decisions and working full/partial lifts/ordinary attacks must survive.
  Runtime result PENDING. The passenger-ownership defect remains INVESTIGATING.
- **R1 compatibility:** preserved map path above, fingerprint
  `316DCF71092AC28688ECFDA73F8323D2D492246B98CF2596AF526C86B921B13C`, runtime
  `D4D63605982616602778246C9ED864332E548B7883223A49ED58D49385EDD718`.
  It was regenerated/verified BEFORE editing the compiler. Do not use the R2
  map to attribute R1 packets; runtime replay fingerprints still govern identity.
- **Next:** keep the user's current R1 replay analyzable; use R2 on the next
  match. No new workspace, gameplay patch, commit, push or PR update this turn.

### T10R1 string-table compile regression (previous session)

- **Status:** FIXED-PENDING-RUNTIME. **Symptom/direct evidence:** user reports
  `rawai-init-goals.per`, line 362, `ERR6003: String table full` on T10:451.
  The referenced statement is the build-marker chat, not malformed syntax.
- **Cause:** the T10 generator repeated 12 quoted trace templates at 351 sites:
  4,219 writer literals / 5,665 total literals across the payload, versus 1,446
  in plain T9 input. Runtime emission quotas did not bound compile-time strings.
  String defconsts reuse table indexes; identical quoted operands can allocate
  repeatedly (see AI reference [defconst](https://airef.github.io/commands/commands-details.html#defconst)
  and [xs-script-call](https://airef.github.io/commands/commands-details.html#xs-script-call)).
  Exact DE capacity/sharing across players is not established; the early marker
  error location does not establish which earlier allocation exhausted it.
- **Contradictory evidence:** 150 structural/tool tests and matching installation
  hashes had passed. They did not exercise the engine compiler or string budget;
  the user's failure overrides the previous compilation-PENDING assessment.
- **Implementation:** generated prelude defines the 12 templates once, before
  their users. All 351 sites, numeric IDs, 12 fields per invocation, quotas,
  source-map checks, original actions and jump destinations are preserved.
  Corrected marker T10R1:452 distinguishes this build from failed T10:451.
- **Instrumentation/tests:** count literal occurrences, ignoring comments but
  respecting semicolons/escaped quotes in text; fail compilation/deployment
  above project budgets of 1,500 payload / 32 writer literals. These are
  conservative project caps including inactive civ files, NOT claimed engine
  limits. Current counts: 1,465 payload / 19 writer; eight-player projection
  11,720 (informational only). Regression recreates and rejects the exact
  failed 5,665/4,219 allocation pattern. String-name collisions fail closed.
- **Preserved behavior/acceptance:** no changes to military, migration or
  navigation decisions. Original-program equivalence/jump tests PASS. Engine
  acceptance requires a fresh eight-player startup without ERR6003 and correct
  marker/map/trace delivery; subsequent all-player replay must preserve attacks
  and successful full/partial transport missions.
- **Latest result:** PASS 152 tests (14 writer tests), source and generated PER
  structure/operand checks, 30 benchmark metadata validations and whitespace.
  PASS installation plus separate read-only verification of all 68 files.
  Manual adversarial review ACCEPTED occurrence-count guard, definition-before-
  use and unchanged string contents/operands; REJECTED lowering runtime quotas
  as a compile-space fix. Engine startup/delivery PENDING, gameplay defect OPEN.
- **Historical failed identity:** T10:451 payload SHA-256
  `02A76B0FCC1EDA35D85047255A1A4CA1DF7EA5913C793FC3C5A14B83B54EFFFD`;
  map `9AC4950C2744171DC0764C9A5AF25A27C2B606A6504C5E38ECCD0F0F2CD46E0B`.
  No successful T10 replay validates that build. Current map is regenerated
  in the existing `writer-trace-sites.json`; no new workspace/artifacts needed.
- **Next action:** restart the game and check a fresh normal lobby startup
  first, then use T10R1 traces for passenger-writer attribution. No congestion,
  economy, salvage, Port or ownership-behavior patch was added in this repair.

### T10 passenger-writer telemetry (initial implementation; compile failed)

- **User objective:** establish which controllers redirect reserved transport
  passengers; this takes priority over additional congestion analysis.
- **Implementation:** `tools/writer_trace.py` instruments this checkout in memory;
  `writer-trace-sites.json` maps 351 stable IDs to source rules, command APIs,
  group operations and native policy/delegation. No sites in the current
  inventory are excluded. Future unreviewed/consuming predicates are explicitly
  excluded, never silently evaluated twice. Original facts/actions/disable-self
  are retained; existing relative jumps retain their original destinations.
  The farm-building jump uses a private guarded return through its logger.
- **Recorded context:** pre/post assault and migration state and hull, current
  selected object ID/flag, and source rule begin/end. Source group operations
  expose reservation acquisition/release intent. The selected object is not
  assumed to be the commanded army; actual command members come from replay
  packets. This observes existing ownership behavior, not a new permission lock.
- **Bounds:** at most 512 recurring invocations per player, at most 96 per
  minute, plus 16 single-use initialization sites. Each invocation emits 12
  short records. Gap/resume messages identify exhausted coverage; no per-sweep
  logging after exhaustion. Ordinary tracing is active during assault/migration
  boarding; reservation boundaries and single-use setup are also traced.
- **Queued-delivery evidence:** T8's after-command `route-screen landing cleared`
  logs precede matching ORDER packets by 14 ms (40:38.024 -> 40:38.038) and
  18 ms (44:08.686 -> 44:08.704). Therefore a chat bracket is not a packet
  delivery fence. `tools/audit_writer_trace.py` retains complete brackets and
  all compatible deferred issuers within 100 ms, with exact passenger-list
  intersections. Multiple candidates remain ambiguous; unbracketed commands
  do not prove native tasking, and 100 ms is not an engine latency guarantee.
- **Build identity:** four short RAW44W map records bind every player's trace
  to the exact generated source map. Missing/wrong fingerprints refuse source
  attribution. Replay-visible build is T10:451, not the plain T9 input marker.
- **Reproduce:** from this worktree using the recorded Python 3 executable,
  run `tools/writer_trace.py --manifest writer-trace-sites.json`, then
  `tools/sync_test_ai.py <installed-directory-above> --writer-trace` to check;
  append `--apply` only to deploy. For the next replay, append
  `--writer-manifest writer-trace-sites.json` to the existing all-player
  `tools/audit_task_ownership.py` command. Use its matching transport hull audit,
  not a prior replay's hull list. The report adds `writer_trace`, including
  identity verification, exact source sites, packet candidates and quota gaps.
- **Read-only adversarial review:** ACCEPTED queued command delivery (do not
  attribute merely between chat tags), exact jump-target preservation, native
  delegation versus immediate orders, full source-map identity, and explicit
  bounds. Tests cover these, original-program equivalence and observer mutation
  restrictions. REJECTED nearest-log attribution, flags-as-native-lock, and
  treating all unmatched WORK packets as a native mechanism.
- **Validation:** PASS all 150 tests, including 12 writer-telemetry tests for
  compiled PER structure/operands, unchanged original rules/jumps, source-map
  identity, deferred delivery and predicate safety; PASS 30 replay benchmarks
  and whitespace check. Deployment and separate
  read-only verification PASS for all 68 generated files and the hash above.
  Subsequently engine compilation FAILED with ERR6003; see the T10R1 repair
  above. Log delivery and gameplay non-regression still need a fresh corrected
  match. Passenger-stealing remains INVESTIGATING, not CLOSED.
- **Next:** use T10 to locate first competing calls in all players' boarding
  windows, retaining the already proven T8 siege-escalation offender. Once the
  remaining mechanism is established, implement the authorized common ownership
  and preemption fix. Do not resume congestion, salvage or Port tuning first.

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
- Full P3B44-derived regression suite: PASS (155 tests, including R3 bounded
  delayed identity, R2 reservation
  classification, T10R1 string
  budget/constant reuse and compiled T10
  equivalence/structure, writer-map identity, deferred delivery and passengers).
- PER structural/operand validation: PASS.
- Naval-doctrine validation: PASS.
- Strategy execution: PASS (1,156 total matchups; 1,149 historical and 1,152
  Extreme matchups with adjustments).
- ODS workbook round trip: PASS (34 civilizations, 680 unit-evidence rows, 340
  naval-class rows).
- Replay benchmarks: PASS (31 entries).
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

**R2 arrival gate satisfied:** the release recovery at the top is implemented,
separately committed, fully statically validated and deployed as R4:455.
Resume R2/ownership analysis now; do not repeat recovery or use R2 as validation
of changes that postdate it. Older R3 references in historical sections are
not the current installed identity.

1. Verify this worktree, branch, T8 diagnostic commit `d10f33e`, audit successor,
   installed marker/hash, and current working-tree status. The intentional
   `AGENTS.md` amendment is now committed, not expected working-tree residue.
   T8 was installed from this exact experimental worktree, not the canonical
   or obsolete checkout. CURRENT installation is generated T10R4:455; use
   `--writer-trace` to check it against the source/map. Plain sources remain
   T9-marked input plus hunt 16, not a separately deployable equivalent of R4.
   Recovery commits and release are recorded at the top; no push or PR update.
   No new development directory exists.
2. R2 is now audited across all players (latest section above). Verify R4's
   delayed identity and recovered caps in the next test. R2 proves early idle
   spam is absent but has missing identity and late quota exhaustion.
   Preserve both external R1/R2 maps. Do not use R2 as validation of R4.
   Follow the shared architectural directive in `TASK-OWNERSHIP.md`, not the
   obsolete restriction to one recall micro-fix. Analyze T10's command/group/
   native-policy trace before assigning WORK packets to a native mechanism.
   Distinguish direct script
   selection, persistent native builder/economy delegation and autonomous
   native tasking with a controlled engine comparison. Preserve search state;
   record exact commanded members where available and expose any trace quota
   exhaustion. Untagged packets without complete coverage prove no caller.
   T8 has now identified all 100 recorded recall packets and proved Red's
   source-3 boarding overwrite, but cannot by itself settle every worker/native
   boundary. Use that established cause in the shared fix; do not repeat caller
   attribution as if it were still wholly unknown. Do not request a long T8 run
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
   twice. T9 uses private diagnostic goals 1163-1165; recheck 1166 onward for A-C. This runtime
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
