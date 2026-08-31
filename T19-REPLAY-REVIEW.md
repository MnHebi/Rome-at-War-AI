# T19:467 replay — voyage progress and completion ordering

Replay `2026.08.31 204847`, SHA256
`ED6963FB76DB551C9A05828F70E04847F72FF5F241AC966752DAC5442CA9C726`.
Duration157:24; manually resigned because progress stalled, not a crash.

## Identity and attribution

- Active recovery exception: `G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-transport-only`,
  branch `recovery/p3b44-transport-only`, HEAD
  `387eccab36a3311ca90d9e39bea6d73013584a8b` plus preserved intentional pending work.
- T19:467 startup markers for players2–8; recorder self-marker not recorded.
  All91 installed/source runtime files matched
  `35526EFC8E958DB8BBC7C366B4126B123D676763287E890EA66BCA597D7B58DF`
  before edits. No mixed deployment or inference from an old marker.
- Selected-color fields, not player-slot/internal-color ordering: p1Red,
  p2Green, p3Yellow, p4Purple (Romans); p5Orange, p6Cyan, p7Blue, p8Gray.
  Britannia,400 population, replay speed2/Fast; preserve this actual fixture,
  not the much older Normal-speed pending fixture.
- **User interventions are not AI successes.** Red's two assisted unloads on
  Blue and its larger land attacks were user-organized. Earlier Red attacks
  against Gray also included manual direction. User confirmed Purple was silent
  to31, and Yellow later became silent too; do not redefine this as merely idle
  troops after acknowledgment.
- Exact command decoder retained537299 events, zero decode failures. Commands
  are requests, not a simulation of execution, position, death or damage.

## All-player transport sweep

All48 command-linked hulls,225 passenger snapshots,53 partial/abort terminal
records, all planner reason reports and all41 slot lifecycles were indexed.
The figures below are **scripted three-slot missions**, not every native/manual
transport or a census of ships physically present.

| Visible color | Hulls in command census | Slot commits | Slot terminal/current results |
|---|---:|---:|---|
| Red |9|4|1 landing event;3 return-empty |
| Green |10|6|3 landing events;1 missing hull;1 quarantine;1 return-empty |
| Yellow |7|28|25 return-empty;2 missing hulls;1 still underway |
| Purple |3|0|3 preparation underfill aborts;no accepted/committed slot |
| Orange |1|0|No slot commit before elimination |
| Cyan |6|3|2 missing hulls;1 return-empty |
| Blue |10|0|27 normal-ready reports plus1 partial;planner failures, no commit |
| Gray |2|0|No slot commit before elimination |

Totals:4 landing events,30 return-empty,5 missing hulls,1 quarantine,1 underway.
"Missing hull" is the controller's exact-ID/ownership lookup failure, not proof
of destruction. Event8 is cargo-empty near the accepted beach, not proof of
unassisted unloading or sustained combat. Partial acceptance and ready reports
are not the same counter:21 partial acceptances,63 normal-ready reports and32
underfill aborts were observed across all players.

Thirty missions recorded no-progress: Red2,Green1,Yellow26,Cyan1. Five had already
issued an outbound unload (Red2,Green1,Yellow1,Cyan1);25 Yellow failures had not.
**The landing-leg fix below does not explain those25 waypoint failures.**
Only4 obstruction-clearance events, all Yellow, were recorded; their absence is
not evidence that other hulls were unobstructed.

Planner memory reports show alternatives being evaluated, but not universal
participation. Blue records362 reason11 landing-danger reports,303 reason21
topology reports,17 reason7,1 reason10,1 reason8; terminal reasons27/26 occur16/12
times. Counts are candidate/terminal reports, not distinct loaded missions.
Next-enemy reports share the hull prefix and are separated, never counted as
null failures. Safe alternative beaches are not proven by these aggregates.

## Causal patch A — compare progress within the same voyage leg

**Status: FIXED-PENDING-RUNTIME.**

- Symptom/evidence: Red44797 commits81:02, issues beach unload82:38 at(141,217),
  no-progress83:42, return-empty86:22. Next commit90:38, beach unload92:54 at
  (119,215), no-progress93:58. Yellow34951 similarly changes leg61:58 and is
  recalled63:02. Replay positions between orders are unavailable, so traffic
  versus actual movement is not inferred solely from these timings.
- Source cause: `tools/generate_assault_missions.py::missions()` stores the
  minimum waypoint distance minus2 in private `best`. At waypoint arrival it
  changes state1 to2 and starts60s, but never resets `best`. Distance to the
  new, often distant beach must beat the old near-zero waypoint minimum to
  refresh progress. A moving ship therefore fails the watchdog.
- Deterministic reproduction: execute the actual emitted PER with an80-tile
  landing leg, advance the hull4 tiles per8s. All three slots FAIL before the
  patch (state RETURN despite continued motion), PASS afterward.
- Implementation: only at the waypoint-to-landing transition, reset private
  `best=99999` and `stalls=0`; next8s sample establishes the new-leg baseline.
  No change to target, manifest, three-slot ownership, damage veto or total
  voyage deadline. No extra order or telemetry writer.
- Acceptance: long second-leg movement refreshes progress; a true stall remains
  bounded; no repeated movement commands while moving; unrelated slots unchanged.
  Fixture PASS. Fresh engine/replay result NOT RUN.

## Causal patch B — completed unloading precedes cancellation

**Status: FIXED-PENDING-RUNTIME.**

- Runtime evidence: Red44797 emits event4 then event9 in the same93:58 sample.
  It had issued unload92:54 and93:50. The controller saw cargo already empty,
  but called it a failed return rather than a landing. The event stream does not
  establish that all passengers were on the intended landmass.
- Source cause: timeout/emergency checks ran before the state2 cargo-empty
  completion rule. A simultaneous deadline switches to RETURN; the later
  return-empty rule releases the group without its landing handoff.
- Implementation: move existing owned-leg distance sampling and the unchanged
  cargo-empty/near-beach completion rule before policy cancellation. Its existing
  member filters still require own mission flags, ungarrisoned passengers and
  the accepted target zone. This is NOT the requested permission to unload a
  still-loaded hull under enemy fire.
- Tests: cargo becomes empty on exactly the progress or total deadline while at
  the beach. Both FAIL before, PASS after: event8, passenger order, no recall.
  The leg-reset patch alone did not resolve this race.
- Acceptance: an actual completed landing cannot be relabeled as a return by
  the same tick's timeout. Invalid beach and real loaded-hull danger protections
  remain. Fixture PASS; engine confirmation NOT RUN.

A and B are independently reversible generator edits: A adds two goal writes to
the transition; B reorders existing sampling/completion blocks. Regenerate the
same runtime file after either revert. They do not require each other to exist.

## Follow-up: upstream formation and mainland-to-overseas handoff

Diagnostic audit requested after the user reported Purple/Yellow largely idle
after the mainland cleared and Green later unresponsive to31. **No behavioral
edits/deployment in this follow-up.** The six inspected runtime modules (military,
economy, taunts, assault admission, native exclusion and owner release) still
hash-match installed T19. T20's two voyage fixes do not address these gates.

### Distinguish the observed failure stages

- Purple attempts boarding at56:17,59:07,62:10, then underfill-aborts at56:49,
  59:39,62:42 with0,0,3 aboard. Hull53956 receives recovery unloads through63:28;
  no later actor commands target the three linked Purple hulls. No accepted load
  or slot commit follows. Other AI logs continue: not global script termination.
- Yellow continues forming/committing missions after the mainland fighting:
  28 commits total, including132:15,138:29,143:48,149:06,155:00. Its observed
  ineffectiveness is not evidence of zero formation.26 no-progress events,
  including25 before any outbound unload, remain the dominant recorded failure.
  User-reported silence to31 remains a separate symptom.
- Green commits six missions, last122:21. Nine troops landed98:42 receive no
  later actor orders after99:13 through157:24 despite subsequent acknowledgments.
  Successful formation/landing does not prove continued combat ownership.

### Source-proven blocking paths; exact Purple runtime gate still unknown

1. **ROOT-CAUSE-PROVEN for conditional preparation starvation; replay attribution
   INVESTIGATING.** `rawai-military.per` recovery CHECK with cargo>0,
   unload-attempts>=3 and an occupied quarantine ID rearms60s and returns WAIT
   indefinitely. No deadline/detachment releases the shared preparation lane.
   Empty hulls farther than12 from their original boarding point likewise repeat
   return movement without a terminal budget. New admission requires route IDLE
   (around5475); taunt31 requires the same (tauntcommands start). Thus one old
   preparation can prevent all new preparations and suppress the response.
   Reused the existing actual-PER `Missions` harness in memory, adding only timer
   facts/actions: hold another quarantine occupied for3660 simulated seconds ->
   still RECOVERY-WAIT, zero commands, both idle gates false. Free quarantine
   control -> IDLE. Empty immobile hull30 tiles away ->61 return commands and
   still WAIT. **Reproduction PASS; no fix/runtime acceptance claimed.** Purple's
   final recovery/no-later-command pattern is consistent with the occupied-slot
   path, but its quarantine ID/cargo/state after63:28 were not broadcast. Neither
   that path nor target selection can be claimed as Purple's established cause.
   Next/acceptance: bounded per-hull recovery must release the preparation lane
   without losing passengers or stealing any active voyage; an unrelated empty
   hull must then form a new mission and31 must acknowledge/defer explicitly.

2. **SOURCE-PROVEN cross-target coupling; replay occurrence unproven.** Empty-hull
   boarding (military5594+) checks `gl-land-target-needs-transport` and the global
   scan/current player, although its saved opponent comes from `gl-ap-seed-enemy`
   (preferred overseas enemy first). It never verifies that those enemies match.
   Actual-PER predicate fixture: saved enemy6/global+scan7,60 soldiers, superior,
   no ally-help job; global needs-transport NO blocks, YES permits the same gate.
   FIND has a20s no-hull cleanup at6058: do NOT claim a stuck FIND state.
   Next: evaluate transport need for the proposed mission's opponent/objective
   and the army's origin, not an unrelated global target. Preserve valid local
   attacks and persistent overseas opponent selection. Runtime gate values needed
   to attribute this particular mechanism to Purple remain unavailable.

3. **SOURCE-PROVEN postlanding dispatch gap; individual ownership INVESTIGATING.**
   Economy1072+ unconditionally sets `gl-land-transport-ready NO` for an overseas
   global target. Ordinary land dispatch requires YES even if some eligible troops
   already share the enemy's landmass. New scripted boarding (military5684+)
   selects only idle, free, unattacked, ungarrisoned home-zone soldiers, excluding
   Palintonons. Previously landed troops outside that zone cannot be recruited.
   Landing gives one point order and releases ownership; no persistent offshore
   combat continuation exists. These gates deny new dispatch, not proof that an
   already-running native attack is forcibly stopped. Taunt31 bypasses transport
   readiness when accepted but still invokes native attack with type-wide reserved
   exclusions; it is not a specific landed-group command. Next: distinguish
   per-landmass combat eligibility from new ferry recruitment, using exact landed
   IDs/flags before any takeover. Acceptance is sustained autonomous combat after
   landing/target death and effective31 or explicit defer, not acknowledgment alone.

These are separate mechanisms, not one proven explanation for all three players.
No new tracing runtime, policy change, full-suite rerun, commit or push was made
for this diagnostic question. Existing command/counter evidence was reused;
full simulated recovery is not an engine/pathfinding test.

## Remaining defects — not silently attributed to these patches

### Stranded troops and taunt31

**INVESTIGATING; high priority.** Green33645 lands nine troops98:42. Exact members:
`80245,75330,71626,75880,77949,76992,70244,75452,72011`.
Their last commands occur98:49–99:13; none receives another recorded actor command
through157:24. They initially attack47141/other nearby objects. No later STOP
targets this group. This is distinct from patchB: this group received its initial
handoff successfully. User confirms the same pictured idle group at101:32 and
122:15, unaffected by31; screenshot-to-ID equality is a likely correlation, not
an independently decoded screen selection.

Green acknowledges31 at110:04,116:20,125:14,151:05. Yellow acknowledges at109:11,
115:33,125:26,151:39; user reports later silence. Purple acknowledges none; its
other logs continue through157:10, so it did not stop executing globally.
Incoming user31 packets are not available in CHAT; these are response timestamps.

Source: `rawai-tauntcommands.per` puts acknowledgment AND `attack-now` behind
`gl-home-defense-state NO` and `TRANSPORT-ROUTE-IDLE`. Either gate can suppress
the entire response, with no deferred-request record. Exact blocking snapshot
for Purple/late Yellow is not recorded. Do not assert one specific gate won.
The severe-defense latch has a time-based clear; it is not source-proven sticky.

Postlanding source issues a single `up-target-point ... action-default` (a MOVE
for point targets), then releases flags. Subsequent native `attack-now` uses the
type-wide exclusion list: reserved copies of a type can exclude free same-type
troops too. Existing scripted opportunistic raids are LAND-map-only. There is no
persistent offshore combat follow-through. Exact flag/type-exclusion state of the
stranded group is missing; do not call retained reservation flags proven.

Next: separate receive/acknowledge from safe dispatch; preserve a pending request
and emit its exact blocking state once. At an idle landed group's first failure,
reuse ownership/command-boundary instrumentation for actor IDs, flags, current
orders/targets and native type exclusions. Implement bounded offshore target
continuation after resolving whether these troops are free or still owned; do
not add broad STOP/reset/retreat commands or steal other mission members.
Acceptance: both acknowledgment/explicit defer and actual eligible troop action,
not an acknowledgment-only success.

### Other Red loaded hulls and congestion

**INVESTIGATING.** Assisted unload commands near Blue at120:26 (49166) and120:42
(46594) are not active RAW3 slot commits. Both have earlier underfill/recovery and
mixed manual/native histories. Do not credit these as autonomous landings, or
claim patchA/B fixes their exact final-tile cancellation. Need correlate the
recovery owner/command boundary, not silently apply the slot explanation.

User-requested policies remain **OPEN, not implemented by T20**:

- Friendly traffic: distinguish congestion from unusable geometry; retain the
  accepted load/mission while bounded wait/yield/alternative routing and eligible
  own-blocker clearance proceed. A timer alone should not force repeated recall.
  Current clearance covers idle empty own free hulls near departure, not the
  crowded route, allies' traffic or all trade ships.25 Yellow waypoint failures
  still need this separate treatment.
- Near-landing danger: a still-loaded hull only a few tiles from a validated
  correct-island beach should get a bounded emergency unload attempt rather than
  immediate recall. Current enemy-identity+HP-loss veto runs regardless of distance.
  Preserve danger veto elsewhere and invalid-island rejection.
- Yellow's repeated tower beach versus safe alternative: inspect exact candidate
  memory, positive danger, coast geometry and alternatives, not aggregate counts
  alone. T19 alternatives exist; source presence is not acceptance.

### Migration drop sites

**INVESTIGATING, mixed result.** Red49166 reports20 settlers ashore61:40; house
BUILD for manifest member34146 at61:58(110,43). Camp584 requested65:30(71,38),
builders assigned65:31 and complete66:28. Camp is near the eventually selected
stone32240(68.5,35.5), but far from the initial landing(66,84).
The user saw no nearby camp64:23 and eventual completion after a distant house.
Source waits for global pending house/Market to clear before starting drop-site
placement; alternate resource search can choose another anchor in the same large
land zone without a short landing-distance bound. Exact gate during the3:49 wait
is not sampled. The requested T18 exact placement did produce a matching camp;
this does not resolve anchor choice, builder interference or delay.

Red41396 later lands7 at117:36, resource-wait117:37, dropsite-failed118:38,
then reboards. Another2 settlers at138:45 repeat resource-wait138:46 → failure
139:46. Here `can-afford-building mining-camp` failed and the60s resource wait
expired before any placement attempt. Three settlers124:16 fail a separate
zone7 recovery. Do not merge all these into the old expanding-point failure.
Source/API affordability is not a recorded exact stockpile/escrow balance.
Next: close the matching prerequisite/reservation/anchor defect separately,
verify local foundation AND productive gathering. Keep T18 placement protection.

### Gray age-up, STOP/lag, boarding ships and walls

- **Gray age-up INVESTIGATING:** Age2 at10:14, Age3 at31:09; first camp BUILD32:41.
  Blacksmith request11:06, Market18:12, Temple40:17, University40:48. No Imperial
  advance before elimination. Requests do not prove building completion.
  Source permits first Mining Camp in Age2, but requires positive gold demand;
  phase3 economy restores gold only after both Market/Blacksmith exist. This is
  a bootstrap dependency to audit, not proof that an Age3 restriction exists.
  The earlier Imperial-prerequisite/Workshop fallback remains separate and open.
- **STOP/lag INVESTIGATING:**52213 explicit STOPs including AI_ORDER706 and native
  STOP; Red10082,Green17216,Yellow1690,Purple972,Orange4620,Cyan4411,Blue5808,Gray7414.
  This does not identify a writer or prove the reported TC-loss lag cause.
  Green's stranded nine have no later STOPs, so they are not that symptom.
- **Boarding Ships:** user observed a successful Blue conversion. Retain as a
  positive control, not universal closure of Red's earlier attachment failure;
  exact converting variant/target/manual status still needed for comparison.
- **Walls OPEN:** Gray's excessive enemy-adjacent placement/age priority still
  needs its own placement/threat evidence; no wall policy changed here.

## T21 follow-up — prompt Age 2 gold and first Mining Camp

**Status: FIXED-PENDING-RUNTIME.** User explicitly requested early gold camp
priority. This is a separate economy-allocation patch, not a change to migration,
transport, placement geometry, age technology prerequisites or wall policy.

All-player first BUILD requests (not completion times):

| Color | Age 2 | First Mining Camp request | Age 3 |
|---|---|---|---|
| Red |09:28|15:04|16:11|
| Green |09:08|17:34|16:49|
| Yellow |09:09|09:10|20:49|
| Purple |09:28|09:28|22:55|
| Orange |10:14|20:56|21:28|
| Cyan |09:43|27:00|17:15|
| Blue |10:14|10:14|20:31|
| Gray |10:14|32:41|31:09|

The immediate Yellow/Purple/Blue requests are controls showing that the existing
Age2 source gate can work. They contradict a universal Age3 building restriction,
not the user's observed delayed camps. Source evidence identifies a concrete
upstream blocker: phase3 resets gold demand to0 while Market AND Blacksmith are
missing; with only one building present none of the allocation branches fires.
The first-camp rule in homebase requires a positive gold allocation. Also, when
both buildings appear while food is700–900, the existing hysteresis band may
preserve zero indefinitely. Replay does not expose Gray's exact allocation/
affordability at every instant; this does not explain every minute of its delay.

Implementation in `rawai-economy.per`:

- Missing either prerequisite ->20 food/70 wood/10 gold/0 stone. This preserves
  the existing10% opening gold share, taking10 points from the former80% wood.
- Both present -> initialize80 food/10 wood/10 gold/0 stone if food<=900 and
  gold share<10. Existing low-food and40%-gold modes keep their700/900 hysteresis.
- No additional construction controller, command, diagnostic string, resource
  escrow change, troop/worker takeover or camp-placement bypass was added.
  Existing home-zone visible-gold search, affordability, pending-work checks,
  duplicate prevention and four-offset placement remain intact. No new assertion
  that map-zone equality proves path safety or foundation completion.

`tools/test_early_gold_bootstrap.py` executes actual allocation rules and the
actual first-gold-camp admission predicate. Before patch:17 failing subcases,
zero harness errors. After:all6 tests PASS, including all missing-prerequisite
combinations across food thresholds, cold deadband initialization, stable
hysteresis, building loss, phase/worker/depletion guards, and admission denial
for Age1/no wood/existing camp/pending work/migration/unknown home zone.

Adversarial read-only review: **ACCEPTED** the deadband case and persistent
one-prerequisite case; both are covered. **REJECTED** a second first-camp builder
or dropping placement guards: immediate Age2 control requests and source already
provide the required resource-anchored path. **DEFERRED outside this patch** the
reported migration foundation/resource-anchor failures, later construction
failures, excessive walling and Imperial prerequisite fallback. They stay open.
All gold-percentage writers were inspected; no civ/rush module later writes over
this phase3 normal-resource allocation.

**PASS:**387 full regression tests, PER structural/operand validation, strategy,
naval doctrine and39 replay benchmarks. Initial sandbox run had one writer-trace
temporary-file permission error; authorized full rerun passed. New runtime
T21:469 contains this independent patch plus unchanged pending T20 voyage fixes;
91-file hash `9B0F1E15A4B928B4AB93FACAB065B7D100761D73097D8ABAFC9CC179C6609A09`.
Installed T19 hash remains unchanged; nothing deployed/committed/pushed.

Runtime acceptance **NOT RUN**: affordable camp/visible home-zone gold should
enter placement within the existing <=10s idle retry cadence after Age2, without
waiting for Market/Blacksmith. Confirm a nearby completed camp AND actual gold
gathering/deposits, preserving Age1 food/lumber opening, age-research escrow and
no repeated duplicate camp requests. Geography, builder availability, safety and
overall age-up time still require engine evidence. Revert only this patch's two
economy rule edits to remove the behavior; T20 transport work is independent.

## Validation, review and artifacts (T20)

- **PASS:**381 regression tests, including19 actual-PER voyage fixtures;
  generation synchronization, PER structural/operand checks, strategy execution,
  naval doctrine, ownership762 relevant sites/zero direct guard failures.
  Initial suite found two stale expected baselines (marker and legal rule-order
  change); fixed explicitly, not by weakening mission behavior assertions.
  One sandbox temporary-file error cleared on authorized rerun outside sandbox.
- Adversarial read-only review: ACCEPTED cross-leg comparison fault and
  completion/cancellation ordering; REJECTED interpreting every no-progress event
  as collision, every event8 as independent combat success, and every silent31
  as a proven defense latch. DEFERRED no policy: remaining implementation items
  stay OPEN/INVESTIGATING above. No new wide acquisition, STOP, flag reset, target
  rotation, threshold change or diagnostic stream in T20.
- Regression controls: three simultaneous private missions, partial manifests,
  active-voyage target independence, friendly-fire identity checks, real hostile
  fire, true-stall bounds, wrong-island rejection and no repeated moving-hull
  orders remain covered. These fixtures are not an engine/pathfinding simulator.
- Immutable rollback archive outside repository:
  `.analysis/p3b44t19-runtime-control.zip`, SHA256
  `9DC862F1BEC8988EAE34D81D643837644915562211B0FD71EE9AE89EA1307A0C`.
  Its91 runtime entries independently reproduce the T19 full hash above; includes
  pre-edit generator/test copies. Not a new development directory.
- **Local T20:468, NOT DEPLOYED:**91 runtime files, SHA256
  `02F378ACB020A471A9B5B45492894E5A75AF21F561658F831128B1D88DBD67D7`.
  Exactly `rawai-assault-missions.per` and `rawai-init-goals.per` differ from T19.
  Installed remains467. No commit, push, PR or data-mod edit.
- External evidence prefix `.analysis/p3b44t19`: full, exact, command-stream,
  transport-audit(json/txt), dispatch, evidence and followups JSON. Reducers:
  `prepare_exact_replay.py`, `audit_t16_dispatch.py p3b44t19`,
  `audit_t19_evidence.py`, `audit_t19_followups.py`. Replays stay external.
- **Runtime result: NOT RUN for T20.** Test an autonomous long landing leg,
  a deadline-coincident unload, true congestion, and postlanding combat separately.
  Do not declare transport,31 or migration closed from these source tests.

## T22 follow-up — ordered upstream recovery and landed continuation

The user authorized the ordered path: deploy/test T20 first; bounded recovery;
mission-local admission; landed combat; then revisit real congestion/near-beach
unload/landing quality. T21:469 was deployed with its requested Age2 gold
bootstrap alongside T20's two voyage fixes. The user subsequently requested T22
on top without waiting for a separate469 replay. **T22:470 is now deployed**;
all91 runtime files and the installed marker independently verified. It retains
the T20/T21 fixes. Fresh engine/replay acceptance remains NOT RUN.
Exact hashes, paths and archive identity are in the current HANDOFF section.

### A — preparation lane starvation

**FIXED-PENDING-RUNTIME; causal fix.** Source and the existing actual-PER audit
prove the busy-quarantine WAIT loop and the unbounded empty-hull return loop.
Purple's exact last gate remains unrecorded; this does not prove that every
Purple failure was this path. The all-player census above is unchanged.

Changed the recovery block and two hull-selection filters in
`rawai-military.per`; recovery deadline/recent-failure declarations and expiry
are generated by `generate_assault_missions.py`. A90s preparation recovery lease
is initialized once per recovery episode, not rearmed at every failed sample.
The existing two home-anchor and one boarding-shore unload attempts remain. A
free quarantine slot retains the exhausted loaded hull as before. When occupied,
release preparation groups and the lane, preserve the old quarantine identity,
leave cargo and the last safe return order unchanged. Empty hulls cannot keep
issuing return movement after their lease. Prune converted/other-owner references
before flag release; do not command or clear another voyage's hull flag.

The most recently relinquished exact hull is skipped by both assault intake
selectors for300s. This single recent-failure record is replaced if a later hull
fails; it is not a multi-hull permanent blacklist. Other native/manual/utility
owners may recover the relinquished ship. Relinquishment is NOT a successful
unload and does not solve every stranded-cargo problem. No finite voyage slot
is repurposed to quarantine these preparations.

Validation: old source FAILS busy-quarantine, empty-hull, other-owner release
contracts; patched actual-PER tests PASS. The normal three-attempt quarantine
and empty/dead completion controls still PASS. Acceptance in the engine: after
bounded recovery an unrelated eligible hull can prepare; preserved cargo/active
voyages are not lost/stolen; no repeated command loop on the old hull. Next:
validate these episodes across every player in a470 replay.

### B — global-target coupling at empty-lift admission

**FIXED-PENDING-RUNTIME; causal fix.** Old gate accepted/rejected the same proposed
enemy6 mission solely by changing global enemy7's needs-transport flag. Source
and the actual-PER predicate counterexample establish this fault; replay evidence
does not uniquely attribute Purple's silence to it.

`rawai-military.per` now searches ready assets of the saved mission opponent and
requires a known land zone different from the home-zone boarder pool. Store the
selected object ID through loading. `generate_assault_plans.py` revalidates that
exact object/owner/zone on initial planning rather than silently choosing the
same enemy's closest home-zone TC. A missing/invalid admitted objective emits
plan reason30 with hull and original object ID, then invokes existing bounded
alternative-objective/enemy search; scripted replanning still rejects home-zone
objectives. `rawai-customconstants.per` adds admission state61; mission generator
defines the objective goal. No global target writes were added.

Existing military-superiority is a **team-wide any-enemy strength comparison**,
not the selected global opponent's strength, so it remains. Army-size, ally-help,
home emergency, actual ownership, partial acceptance and screening gates remain.

Validation PASS: mission6/global7 local target admits an eligible overseas lift;
same-zone/unknown-zone/other-player assets and dead/allied opponents do not;
recent rejected hull does not displace another free hull; the initial admitted
objective survives loading; its loss replans without unloading the accepted cargo.
Acceptance: local global-target selection no longer vetoes a viable overseas
mission, and no same-home-island lift is admitted by an unrelated cache. Next:
fresh470 replay of mainland-cleared transitions and all-player intake outcomes.

### C — landed units losing combat continuation

**FIXED-PENDING-RUNTIME; user-requested bounded behavior addition addressing a
source-proven dispatch gap.** Green's nine landed troops had no later actor
orders99:13–157:24 despite taunt acknowledgments. Old source sent one point move,
released the group, and had no dedicated offshore continuation. This is not proof
that those exact units retained flags or that STOP caused their inactivity.

`generate_assault_missions.py` changes successful landing handoff: return/release
the empty hull and screen, retain only exact self-owned same-zone ungarrisoned
manifest members in their existing group, enter state6. No free-unit recruitment.
Every16s the controller may order only idle, unattacked owned members to a live
hostile building/villager on their landmass. Prefer the saved opponent, then other
living enemies. Busy units, other owners, converted units, wrong-zone troops and
garrisoned units receive no new order. A dead target is replaced; three idle
retries skip that target. Four no-target checks or a300s total lease releases
ownership without STOP, retreat or interruption of the last attack order.
Logs reuse RAW3 slot/hull/enemy tags: event12 combat release;13 new combat target,
plus exact target ID. No per-sweep unchanged diagnostic stream added.

Capacity tradeoff is explicit: state6 uses its existing slot for at most300s.
There remain three owned assault lifecycles, NOT three voyages plus unlimited
landed groups. Long battles after lease expiry revert to ordinary/native control;
there is no claim of indefinite offshore control or universal taunt31 resolution.

Validation PASS:6 actual-PER combat tests cover retained manifest/free hull,
retarget after destruction/global target change, exact actor exclusions, lease
and no-target bounds, saved enemy exit, and failed-target replacement. Existing
T20 long-leg and deadline-coincident completion tests remain PASS with the new
postlanding state. Acceptance: autonomous attacks resume after landing and target
death, without yanking busy troops or consuming transport hull ownership. Next:
470 all-player landings, target deaths, releases and repeat assaults.

### Review, reversibility, validation and remaining queue

- Read-only adversarial review ACCEPTED: stale group references before release;
  the admission proof must retain its objective through loading; missing admitted
  objectives must not fall back onto the home island; split landing handoff to
  stay within the engine32-element rule bound. Implemented and tested.
- REJECTED with source evidence: removing military-superiority as a global-target
  dependency (it uses team sums); treating every Yellow failure as no formation;
  calling a recovered/released cargo owner a successful landing. No such claims
  or changes were made.
- DEFERRED to the user's following stage: waypoint traffic handling, near-beach
  emergency unload and broader landing quality. Taunt31 receive/defer, migration
  dropsites and other open ledgers remain outside these patches.
- Each patch is independently reversible: A recovery region/intake rejection
  filters/recovery declarations; B admission search/objective capture and planner
  entry/replan filters; C generated landed handoff/state6/added private fields.
  Regenerate affected outputs, reverse the corresponding tests, and issue a new
  runtime marker after any selective reversal. The immutable T21 archive contains
  all pre-edit runtime files and generators; it is not a second edit workspace.
- **PASS:**404 full regression tests; PER/operand and generator synchronization;
  strategy/naval/39 replay benchmarks;801 ownership sites,0 permission failures;
  `git diff --check`. Sandbox writer temporary-file error cleared on authorized
  rerun. Legacy assertions were changed only for explicitly authorized recovery,
  admission and postlanding contracts; dedicated behavior assertions remain.
- **Runtime/replay result NOT RUN for470.** Deployment PASS; fresh470 startup
  and all-player replay acceptance pending. The user waived a separate469-first
  test; the immutable469 control remains available. Neither static checks nor
  these fixtures prove pathfinding/combat.

Remaining voyage source review: state1 waypoint no-progress still has its90s
watchdog and total travel remains600s (or the already accepted fallback budget).
Friendly blocker clearance still covers limited free own departure hulls, not
all allied trade traffic on the route. The identity+HP-loss danger veto still
runs before a still-loaded near-beach unload; T20 only prioritizes **already
completed** unloading. T19's25 Yellow failures before any outbound unload cannot
be attributed to the second-leg bug. These are distinct follow-up candidates,
not implemented or claimed resolved by470. Use470 state/order traces and the
retained469 source control to distinguish these before changing traffic patience
or safety policy.
