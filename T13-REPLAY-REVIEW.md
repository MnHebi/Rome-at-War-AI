# T13 replay review — 2026-08-31 002333

## Evidence correction after T17, 2026-08-31

The old drop-site telemetry's `position-target` coordinates identify an enemy
building, not the point passed to `up-set-target-point`. Therefore the distant
158,211 diagnostic does NOT by itself prove a clobbered migration request. That
runtime attribution below is withdrawn; the persistent-point source safeguard
is retained. T17 independently records actual misplaced BUILD coordinates and
exposes the expanding `place-point` queue versus exact foundation-verifier
mismatch. See `T17-REPLAY-REVIEW.md`; historical observations below remain intact.

## Identity, scope and limits

- Replay: `SP Replay v101.103.48987.0 @2026.08.31 002333.aoe2record`,
  65,629,473 bytes, SHA-256
  `3106EDB647E64D12752788F1C6E4D1A281E6E130BE64ED8B14260EA6C429E70D`.
- Ends at **121:55**, with player 1 resignation; no crash attribution.
- Recorded marker **RAWAI-P3B44T13:458** (players 2–8; recorder chat asymmetry).
  All 80 installed runtime files were byte-compared to source commit
  `fb54ae46ed1ea35f2590157d5abb7bb1606e1802`: zero mismatches. Installed payload
  remains `A260148B2998E72203883BF34578D96B9AD6B72A561857C89ADBB28F23C96FB6`.
  No audit patches have been deployed. Marker has not been changed.
- Validated selected-color fields, not lobby row/internal body colors:
  replay player 1 Red, 2 Green, 3 Yellow, 4 Purple (Roman Empire, user team 1);
  5 Orange Picts, 6 Cyan Britons, 7 Blue Germani, 8 Gray Gauls (user team 2).
  Scoreboard/chat color number “2” is not replay player 2.
- Parsed terrain is **220×220**; population 400, Extreme, speed 2.0, shared
  exploration. Do not apply the old lobby's nominal 240 dimension as the terrain
  array stride. No claim that every old lobby setting is newly verified.
- Full-stream sequence and exact packet-length decoders: zero failures.
  1,052,651 retained events. Raw ERROR actions are not parser errors or crashes.
  Orders show requests, not damage, actual construction, arrival or profitability.
  Private chat is not uniformly available for every player; missing private
  messages are not negative evidence.

## All-player transport and command census

134 boarding windows: **74 assault, 35 migration, 25 unresolved/recovery/relic**.
Every reconstructable window was included, not only the reported Red incidents.

| Color | Assault windows | Useful load terminals | Boarding abort | Screen/safety recall | Landing timeout | Empty-hull completion log | STOP706 packets | PACK packets |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Red | 17 | 17 | 0 | 13 | 1 | 3 | 48,213 | 58 |
| Green | 1 | 0 | 1 | 0 | 0 | 0 | 1,199 | 21 |
| Yellow | 0 | 0 | 0 | 0 | 0 | 0 | 200 | 0 |
| Purple | 1 | 0 | 1 | 0 | 0 | 0 | 27,015 | 100 |
| Orange | 0 | 0 | 0 | 0 | 0 | 0 | 251 | 0 |
| Cyan | 6 | 6 | 0 | 6 | 0 | 0 | 3,078 | 21 |
| Blue | 20 | 18 | 2 | 7 | 2 | 9 | 17,519 | 29 |
| Gray | 29 | 26 | 3 | 26 | 0 | 0 | 97,549 | 0 |

“Useful load” means a full/partial boarding terminal, not successful delivery.
Zero identified assault windows does not mean zero transportation. The 35
migration windows end in 12 full loads, 16 partial loads, six empty aborts and
one loaded abort; these are not 28 economically successful colonies.

Red's 13 preflight recalls split into six reason 3 (no free route-screen ship),
four reason 11 (defended landing), two reason 9 (landing beach unreachable),
one reason 5 (route waypoint unreachable). Its remaining reason 12 is a landing
timeout, **not departure congestion**. Gray: 18 no-screen and eight no-safe-approach
recalls; Cyan: three scout defensive-fire recalls and one each no-screen,
unreachable waypoint and screen lost. Do not relax danger screening on this basis.

All 12 empty-hull completion messages have subsequent ground orders involving
reserved passengers. They do **not** all establish useful assaults:

- Red 59:37: ten members, unload `(105,85)`, target `(84,66)`, same reconstructed
  main land component. Actual combat/path completion remains unproven.
- Red **64:07**: nine members ordered toward enemy TC `(67,53)` after unload
  at `(43,39)` on the small resource island. Offline terrain components differ;
  this is not a useful arrival at the objective.
- Red 80:03: ten members, unload/target `(77,69)`, main island; combat unproven.
- Blue has positive follow-through: the 39:23 landing is followed by an attack
  packet 2.7 seconds later; the 56:21 landing by one about 15 seconds later.

The legacy reducer's route-screen-clear value is a **scout ID**, not a hull ID.
It is excluded from hull-only joins. Offline flood-fill components are evidence
of disconnected terrain, not invented engine map-zone identifiers.

## Causal patches and independent boundaries

All statuses below are **FIXED-PENDING-RUNTIME**, not CLOSED. New patches are
intentional local changes on `recovery/p3b44-transport-only`, based on `387ecca`.
They contain no added telemetry strings, deployment or change of runtime marker.
Each numbered behavior can be reverted without reverting the others; shared test
helpers and the generated inventory are supporting artifacts, not coupled policy.

### 1. PACK recipients — existing local commit 387ecca, expanded evidence

**Symptom/evidence:** 229 PACK packets across five players. Red 53:14/53:39
recipients include verified Ports 29931/34665, matching the 53:31 Packing48%
screenshot. Purple 70:11 packs `[4486,31814,59421,63747]`; 109:23 also includes
73662. Initial TC 4486 and other villager producers corroborate the reported TC
packing. Blue also issues PACK to TC producers. Not every recipient is classified.

**Cause/change:** the land-siege FALLBACK consumer trusted a shared local search
from an earlier pass without checking unit type. The newly functional PACK action
exposed that stale list. `rawai-military.per` now reacquires immediately and permits
only self-owned, FREE, exact unpacked Palintonon42; fallback additionally checks
idle, ungarrisoned, unthreatened and intended scope. It recomputes the count.
The exact intervening writer in each replay incident is not attributed.

**Validation/acceptance:** six actual-rule tests failed original T13 and pass the
fix; the clobbered-list fixture now includes a TC. Fresh game must show zero
non-Palintonon PACK and retained legitimate Palintonon recovery. No repair of
already-packed buildings is claimed. Purple's jitter may be downstream, but Gray
has a huge STOP flood without PACK, disproving PACK as the universal spam cause.

### 2. First demanded military building blocked behind two TCs

**Evidence:** Red has initial TC4459 and no TC BUILD request in the entire match.
Fortress admission and its placement recovery both require two completed TCs.
Range/stable admission has the same gate at Middle Antiquity+, except defense/rush.
Red issues no range/stable BUILD. User-built fortresses at 107:44,107:57,117:52
are interventions, not AI placement successes.

**Change:** four `rawai-homebase.per` rules allow the first *already demanded*
Fortress/range/stable with one completed TC. Later copies retain the original
policy. Age, demand, affordability, ownership, pending/placement checks remain.
This repairs an admission policy that blocks first construction; it does not
prove the island has valid space or that every other gate was open historically.

**Tests/acceptance:** four first-building tests; initial admission failures now
pass, expansions and worker holds preserved. Require autonomous foundations and
completion in a one-TC start, not merely a build request.

### 3. Trade proof renews against an obsolete producer census

**Evidence:** Red has ten AI MAKE17 requests, last at 28:24. A second Port is
requested at 29:09/32:14 and produces from 41:51. Trading-action proof continues
to renew. Training requires current Port count to equal the stored source count;
the live-proof shortcut renewed the deadline without refreshing that count,
preventing the endpoint census from running after producers changed.

**Change:** water and land live-proof entry rules in `rawai-economy.per` require
matching producer counts; otherwise the existing endpoint-validation scan runs.
They do not blindly bless the new count. Caps, affordability and probes remain.

**Tests/acceptance:** two producer-epoch tests pass, including the formerly failing
stale-count case. Fresh game must resume bounded AI production after producer
change. Red used only one bounded probe: do not blame its inactivity on exhausting
three probes. Route danger, profitable delivery and general failure recovery are
separate OPEN issues; an action named trade is not a completed profitable trip.

### 4. Assault lateral destination on the wrong island

**Evidence:** Red 64:07 above. The two ±28-tile candidates were screened for
hostile fortifications but not for sharing the enemy objective's land zone.
An empty hull then generated “completed” regardless of passenger reachability.

**Change:** lateral-target rules in `rawai-military.per` capture target/left/right
terrain zones, reject mismatched/unknown candidates before the existing two-sided
safety choice. Three persistent goals in `rawai-customconstants.per` (14200–14202).
No boarding, escort ownership, threat exemption or route timeout changes.

**Tests/acceptance:** five actual-choice fixtures, four failing before the guard,
all pass. Preserve a valid alternate side and bounded no-safe-side recovery.
Fresh engine must deliver passengers on the objective's landmass and allow useful
combat. Empty-hull-only terminal verification remains OPEN. Reason 1 now includes
disconnected candidates as well as defended candidates: describe it as no safe
approach, not necessarily enemy presence.

### 5. Heavy-ship production rotation never initialized

**Source/runtime evidence:** all 125 recorded naval snapshots across seven players
have `ship-train=-1` (Orange has no qualifying snapshots). Active transitions all
require an existing roster choice. `rawai-init-goals.per` initialized its timer,
not the choice. The disabled legacy switcher previously supplied implicit entry.
The prior T12 audit correctly found a rotation chain but missed its absent entry.
No MAKE1870/1750/1884 appears in this replay.

Roman masks: Red Q32×9/Q38×9, O32×1/O38×17; Green Q32×1/Q38×13/Q103×7,
O38×14/O103×7; Yellow103×17 both; Purple38×17 both. Bits:1 unavailable,
2 no trainable family,4 base untrainable,8 fleet cap,16 family cap,
32 wrong roster choice,64 Advanced Weaponry incomplete. Mask32 is direct evidence
that availability/trainability/prerequisite/cap checks pass but selection does not.
At **101:41**, Red Q/O both32: phase7, COMPETITIVE role2, fleet16/cap32,
family allowance4, wood811/gold238/headroom90, six Shipyards, escrow0. Earlier
eight Red Q32 samples also exclude insufficient resources as a universal cause.
Other masks do show prerequisite/resource/trainability blockers; do not erase them.

**Change:** one startup assignment `ship-train SCOUTSHIP`, in the existing one-shot
timer initialization. No production cap, roster policy, research, concrete ID,
unique-family or resource threshold changes. No extra instrumentation.

**Tests/acceptance:** all four actual-rotation tests fail before and pass after:
one-shot entry, PRIMARY/COMPETITIVE full roster including Q/Oct, limited SUPPORT
cycle and stable 12-second choices. Fresh game must show bounded actual Roman
heavy hull production when trainable, without regressing existing Juggernauts.

### 6. Migration placement point survives only in global scratch state

**Evidence:** Red's second mining landing at116:35 has six correct-zone settlers.
Existing diagnostics record requested point `(158,211)`, zone5, one attempt;
sample settler31166 is gathering stone29347 in zone5 with group11. That stone's
initial position is near `(32,51)`. At116:55 the request remains pending and
affordability is now false; no concrete foundation, later failed at117:57.
This is distinct from Red's earlier no-resource-anchor failure.

**Cause/change:** four PLACE rules set a shared target point. ISSUE can wait
across passes for affordability/pending/worker admission, then read whichever
target another controller left. Preserve each bounded offset in existing
`gl-migration-build-x/y` during PLACE and restore it immediately before each
Mining Camp/Lumber Camp/Mill `up-build`. Preserve diagnostics, four offsets,
timers, ownership and concrete-foundation checks. No additional goals/strings.
The exact clobbering controller is not necessary to reproduce this lifetime fault
and is not claimed to have been identified.

**Tests/acceptance:** the delayed actual-rule fixture reproduces the erroneous
`(158,211)` request before correction; all six foundation tests pass afterwards,
including 12 type/offset combinations and immediate requests. Fresh engine must
place, complete and use a correct-zone camp. This fix alone does not close migration.

## Unresolved defects and contrary evidence

### STOP flood — INVESTIGATING, highest remaining attribution priority

195,024 AI_ORDER706 packets, plus 914 separate literal STOP actions. Red's exact
group `[29908,30068,30489]` receives **36,017** identical STOPs from80:30–100:56.
The stream stops at the user's concrete Mining Camp request at100:56.846.
For29908 the flood starts during boarding, before the82:16 landing/failure;
therefore the missing camp cannot by itself explain the initial trigger.

Every explicit source STOP writer was inspected (two general, fourteen military,
plus reset/native-exclusion boundaries). Existing RAW12 direct STOP counters for
Red total267 invocations (sites1/2/3/5/14 =4/23/238/1/1), versus48,213 packets;
reset-scouts site4 fires once. This rules out one counted script call per packet,
not a script-triggered persistent native task. Native gather/idle/garrison
handling and repeated exclusion boundaries90/91 remain discriminating leads.
Counter activity alone is not producer attribution. No blanket native disable,
guessed STOP suppression or new tracing runtime was added.

Next: use unit29908's first boarding-to-STOP boundary and the Gray36096/Purple67104
counterexamples to isolate native task state versus scripted delegation, reusing
existing exact packets/counters. A controlled engine comparison is still needed
where those callbacks are not serialized. Acceptance: exclusive passenger task
ownership, no tick-rate repeated STOP, retained ordinary worker/defense recovery.

### Juggernaut stopping / wall fixation — INVESTIGATING

User confirms several types, including Juggernauts, visibly stop/stutter. Nine
Red naval-siege hulls identified by source-tagged bombardment packets have zero
AI_ORDER706 and one literal STOP, but144 ORDER,71 AI_ORDER700 and44 MOVE packets.
This does not disprove the visual symptom or classify every Juggernaut. It
distinguishes their recorded command churn from the settler STOP706 flood.

Wall43240 at `(87.5,61.5)` receives25 tagged attacks, 58:21–60:55 and80:46–88:27.
User clarifies **manual ground fire at nearby in-range tiles caused no wall
damage**. Do not record successful alternate-position targeting. The expanded
48/96/192/255 radius enlarges candidate discovery but does not prove a reachable
firing position or reject the same no-progress wall. Damage/position evidence is
still needed to separate ineffective firing geometry from interrupted approach.
No speculative range/weapon fix. Preserve improved overall Juggernaut use and
the user's positive Palintonon observation. Acceptance: no repeated ineffective
target lock, useful firing, and stable approach orders without invalid targets.

### Red first mining landing — INVESTIGATING

At82:16 ten settlers land, then “recovery no resources:5” and drop-site failure
occur before any construction attempt. Source discards the earlier mining anchor,
searches global capped lists (gold10/stone10/tree40/food10), then filters zone.
Earlier selection searched20 stone. Cap/visibility/zone lifetime are unresolved;
the exact rejected list is not serialized. Four gold and four stone initial
objects plus later manual mining disprove an actually resource-free island.
Do not conflate this with the proven later placement-coordinate fault.

Next isolate saved anchor and postlanding candidate list; prefer revalidating
the exact known resource over unproven enlarged global search. Acceptance requires
autonomous foundation, completion and actual resource drop-off, not landing alone.

### Trade safety and autonomous retry — OPEN

Red dangerous-versus-safer route choice remains user-observed. Fifteen manual
DE_QUEUE17 records at64:08–117:28 follow the ten AI MAKE17 requests ending28:24;
do not credit these as AI recovery. Live activity is not delivered profit, and
generic training does not bind a particular safe Port pair. The producer-census
patch addresses one deadlock, not route selection or successful future retry.
Next bind each merchant to endpoints/losses and distinguish safe candidate
rejection from native assignment. Acceptance: safe viable route, AI re-probing
after danger clears and sustained positive returns before large growth.

### Cyan unsafe resource work — INVESTIGATING

71:00–77:00 has1,035 WORK orders from112 distinct workers toward trees around
`(125..129,69..73)`, near Purple Fortress request `(114,76)` at68:29. User observed
villager sacrifices around74:00;112 is not a death count. Explicit homebase
resource retasking checks resource/same zone, not fortification corridor danger;
native gathering can also generate WORK. Do not attribute every packet to the
five-second scripted retask rule. Next tie exact victims and earliest tasking
boundary to fortified approach geometry. No guessed broad gatherer rewrite.

### Other retained OPEN work

- Loaded route-screen acquisition/progress: current first-ten/80-tile then FREE
  filtering can omit alternatives, but exact eligible ownership/path evidence is
  needed before changing it. Preserve working Blue attacks and useful loads.
- Build placement: first-building admission fix does not prove geometry. Repeated
  BUILD requests include Purple TC194/workshop122 and Cyan workshop342; these
  are not completed buildings. Investigate layout/placement separately.
- False/missed allied claims: no numeric300-series claim snapshots in this replay;
  therefore no runtime closure of the T13 victim/hostile verification repair.
  Cross-water relief remains unimplemented.
- Interrupted Yellow boar collection, broad Port channel quality, Wonder stalemate
  completion, existing crash cause and previous ledger items remain open. No crash
  occurred/was attributed here. Military losses can postpone the current quiet-window
  Wonder policy even without territorial gain; no unrequested policy relaxation.

## Manual interventions / acceptance exclusions

- User ground fire near the wall: **no damage**; not an AI success.
- Red camp584 at100:56.846 `(38,47)`, workers29908/30068/30489. Subsequent mining
  cannot validate autonomous drop-site construction; it does bound the STOP burst.
- Fifteen Red manual merchant queues, all type17, Ports29931/34665.
- Red's three Fortress requests after107:44 are user-assisted; missing other
  military structures remain visible evidence, not successful autonomous placement.

## Validation, review and next runtime

PER/operand and naval doctrine checks PASS;672 ownership sites, zero direct
permission failures. **265 regression tests PASS**, zero failures/errors/skips.
34 replay benchmark metadata checks and generated counter/inventory consistency
PASS. Focused tests demonstrate source faults, not physical engine outcomes.
Initial full-suite run had one sandbox temporary-directory permission error;
rerun with approval, not treated as a gameplay regression.

Adversarial read-only self-review triage:

- **ACCEPTED:** reject candidate zones before the existing assault safety choice;
  persist/restore placement coordinates at their actual command boundary; initialize
  roster once, not every pass; require a fresh trade census instead of blessing a
  changed count; preserve first-only building demand/caps and genuine worker holds.
- **REJECTED:** all STOPs come from PACK; all Red landings are successes; three
  probes explain Red trade; the old Q alias explains Octeres; manual construction
  validates the AI; initialization alone guarantees production despite poverty.
- **DEFERRED with explicit OPEN status:** exact native STOP callback, first-landing
  anchor loss, useful post-unload reachability, wall damage/approach, safe trade
  assignment and fortified gathering. No guessed behavior changes for these.

Do not deploy this unmarked checkout as T13:458. When a next test is prepared,
give it a distinct identity, verify the full payload, and validate all six patch
acceptance criteria while preserving ordinary attacks, Blue follow-through,
partial/full lifts, legitimate safety aborts, Palintonons and useful Juggernauts.

## Subsequent user-requested optional screening

**Deployment follow-up, 2026-08-31:** the user subsequently authorized all pending
fixes. They are now installed as `RAWAI-P3B44T14:459`,81 files, SHA256
`DE6010CD8942E7D790A161FDE1A02CFC3F3C1F085E735731B16748F2A782B8A8`.
Post-install full byte comparison and287 release regression tests PASS. This
T13 replay remains pre-fix evidence, not runtime validation of the new bundle.

Subsequent user-authorized policy change (not present in this replay): the three
soft screening failures can now enter `rawai-assault-screen-fallback.per` instead
of canceling an accepted assault manifest. The user corrected the initial full-only
gate: an already-approved T6 partial5–9 qualifies too. The loading owner now seals
the accepted count and hull ID; a lowered request alone is not acceptance. Recheck
the exact hull/manifest, original live hostile player, all-enemy known defenses at
waypoint/landing and target land zone before one-way departure without a Scout.
Reason3 starts validation immediately; reasons5/9 retain bounded scouting attempts.
Timed-out scout damage/loss also vetoes after the scan. Existing hard recall and
screened success rules remain unchanged. No voyage edge returns to screening.
Unscreened travel has a300s deadline plus60s without at least2 tiles of net waypoint
progress; retries cannot refresh it. Unloading retains its45s deadline.
T13 contains30 soft-reason recalls (3:25,5:2,9:3), not30 guaranteed improved outcomes.
22 focused actual-rule/state tests and the full287-test suite PASS; T14 deployment
is verified but fresh-game acceptance NOT RUN. See HANDOFF for tags, limits and exact
acceptance. This is **USER-REQUESTED BEHAVIOR CHANGE**, not another claimed causal
pathfinding fix or closure of the native STOP flood.

## Reproduction artifacts (outside Git)

Base: `G:\Projects\Codex\Rome at War AI\.analysis`.

- `replay-20260831-002333-t13-full.json`, `p3b44t13-command-stream.json`,
  `p3b44t13-exact.json`, `p3b44t13-task-ownership.json`.
- `p3b44t13-transport-audit.json/.txt`, `p3b44t13-summary.json`,
  `p3b44t13-findings.json`, `p3b44t13-incident-evidence.json`.
- `p3b44t13-supplementary.json` (MAKE, DE_QUEUE, UNKNOWN109),
  `p3b44t13-initial.json` (4,476 objects and terrain; body colors excluded).
- Existing parser wrapper `audit_writer_replay.py`; reducers `summarize_t13.py`
  and `inspect_t13_evidence.py`; primary cached API data `airef-reference-20260830.js`.
  Native MAKE payload sequence is not full-stream sequence; use supplementary
  global sequence for joins. UNKNOWN109 is not assumed to be decoded research.
- Python3: `C:\Users\LostSoul\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`.
  PATH `python` may be Python2. Use repository `tools/audit_task_ownership.py`
  and `.analysis/replay_parser_kjir`; do not create another heuristic ID decoder.
- Relevant primary API: [point-based build](https://airef.github.io/commands/commands-details.html#up-build),
  [point packing](https://airef.github.io/commands/commands-details.html#up-target-point),
  [remote search](https://airef.github.io/commands/commands-details.html#up-find-remote).
  API descriptions constrain the source fix; they do not replace engine acceptance.
