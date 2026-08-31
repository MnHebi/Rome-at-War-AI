# Task ownership / threat preemption recovery

## T11 source-first implementation — current status

**OWNERSHIP IMPLEMENTED FOR SOURCE-PROVEN PATHS — NATIVE BOUNDARY REQUIRES ONE DISCRIMINATING TEST.**

Worktree: `G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-transport-only`,
branch `recovery/p3b44-transport-only`, implementation parent `a5de7d85`.
Plain runtime **RAWAI-P3B44T11:456**; deployment identity and final validation
are in HANDOFF.md. This is a behavioral patch, not another writer-trace build.
No new attribution is claimed for Blue Scout 4608's historical STOP packets.
The immutable P3B44 attack control is untouched.

### Evidence and earliest causal faults

- **B:** routine land/naval defense and strategic convenience callers invoked
  global reset/retreat with no task compatibility check. R1/R2 ferry/Relic
  passengers and T8 Red's boarding soldiers were included in these orders.
  Ownership flags could remain set while the command changed.
- **B:** native exploration remained admitted while reserved Scouts boarded;
  R1 records exploration order 705 replacing their boarding orders.
- **A:** migration, assault, stranded recovery, relic ferry and naval scouting
  reused live group slots; several exact-object/delayed writers only checked
  eligibility in an earlier selector. Distinct groups plus command-time
  self/owner checks repair these source faults, not merely the old flag-4 case.
- **A/B:** direct worker cleanup/staffing/repair/build-support/retirement paths
  did not share a complete ownership exclusion. T7 establishes WORK conflicts,
  but does not identify every native versus direct writer. The direct unsafe
  paths are repaired without pretending all WORK packets have one cause.
- **A:** routine land dispatch could use `up-target-objects 1` without selecting
  the current hostile first; the selected-object pointer could still name a
  local asset. Dispatch now explicitly selects/revalidates the live enemy.

### Shared contract and compatibility

FREE is a self-owned object with negative group flag, plus the caller's role,
zone, activity and exact-ID exclusions. A negative flag alone does not prove
that a native task has ended. Ordinary military acquisitions also require
idleness where they might otherwise seize an active native attack. Civilians
do not share the engine's reliable military-idling predicate.

| Owner / group | Ordinary economy | Exploration | Routine defense | Severe home defense | Release |
|---|---|---|---|---|---|
| Temporary worker cleanup / 0 | Same-pass only | No competing explicit claim | No | Not preempted | End of same-pass loop |
| Siege objective / 1 | N/A | No | No | Kept protected | Objective refresh/terminal |
| Juggernaut + Octeres / 2 | N/A | No | No | Kept protected | Shared capital-siege controller; intentional alias |
| Assault hull / 3; passengers / 4 | No | No | No | Cancel passenger owner only if **every surviving member** is ashore in home zone within 24; then release and acquire bounded responders | Abort/loss/landing; full/partial departure retains hull |
| Naval response / 5 | N/A | No | Its own refresh only | No land preemption | Response refresh/terminal |
| Land response / 6 | N/A | No | Its own owner | Explicit replacement by severe response | Quiet release; no move-home order |
| Route screen / 7 | N/A | No | No | Protected | Route terminal/screen refresh |
| Raid / 8 | N/A | No | No | Cancel only a wholly local, ashore group | Existing raid terminal/explicit severe cancel |
| Transport escort / 9 | N/A | No | No | Protected | Hull/escort refresh; own-owner STOP only |
| Migration hull / 10; passengers / 11 | No while boarding; native colony work deliberately resumes after departure | No | No | Protected in this policy | Abort/loss/mission terminal; partial departure releases non-cargo |
| Recovery hull / 12; passengers / 13 | No | No | No | Protected | Existing bounded landing/abort/quarantine |
| Relic hull / 14; Priest/Brahmin / 15 | No | No | No | Protected | Whole relic round trip/abort/loss |
| Naval Scout / 16 | N/A | Its own naval DUC controller only | No | Protected; same-owner danger evasion allowed | Scout refresh/terminal |
| Allied relief / 17 | N/A | No | No | Cancel only a wholly local ashore group | Verified target gone/converted, 90-second release, or severe cancel |
| Active native attack (no DUC flag) | N/A | Mature-game native exploration off | Moving/fighting units excluded by idle selection | Bounded nearby compatible responders; native queued-order boundary remains below | Native completion; no global reset |
| FREE compatible unit | Yes by role | Early exploration only when no conflicting land mission | At most 8 nearby idle responders | At most 16 nearby same-zone responders | Explicit task claim |

Groups are cooperative metadata, **not engine locks**. At pass start, group
references are rebuilt from self-owned members still carrying that owner's
flag, without changing foreign/other-owner flags. This makes subsequent
legacy clear/reset operations act on current members, including after conversion.
Claims recheck FREE; commands recheck self and expected owner, including
evasion's captured owner. Exact hull targets are checked on boarding retries.
Terminal releases issue no movement/STOP. Failed ashore migrants are released
on partial departure while actual cargo keeps group 11.

### Controller fault matrix

This is the owner-level causal matrix. The accompanying
[complete rule-site inventory](OWNERSHIP-SOURCE-INVENTORY.md) lists every
relevant source rule, file/line, actual selector/unit type, command/delegation,
reservation mutation and concrete permission checks. Its D classification is
limited to cooperative ownership, not path safety or engine behavior.

| File / family / states | Acquisition and affected units | Fault classification before patch | Correction / command-time check | Release / preemption |
|---|---|---|---|---|
| military: ordinary age/periodic/percentage/town-size attack | Native soldier/boat selection | C | Type exclusions published after DUC claims and before native dispatch; no global pause of ordinary attacks | Native lifecycle; residual queued-order test |
| military: attack preparation / LOAD-SELECT | Near-home land army, excluding Palintonons | A | Self, FREE, idle, nongarrisoned, home zone; native exploration disbanded before claim | Group 4 contract |
| military: LOAD-ISSUE / retries / diagnostics | Stored passenger group + exact hull | A/B | Distinct hull 3/passengers 4; recheck self and owner at every command | Partial/full keep 3; abort releases 4 |
| military: migration mining BOARDING | Eligible idle/depleted noncritical workers | A/B | Exclude all reservations and active boar-lurer ID before cap; staged claim 11; native worker admission hold | Partial cargo-only reservation; terminal releases 10/11 |
| military: migration Scout BOARDING | One same-zone Scout | B | Zero native explorer budgets **and reset existing explorers before claim**, hold while reserved | Group 11 terminal, then early exploration may resume |
| military: migration route/landing/recall | Exact hull / reserved passengers | A | Separate 10/11 and command-time permission; geometry unchanged | Existing bounded mission terminals |
| military: migration colony work / deposit | Mission passengers and supported native construction | A/C | Direct commands retain owner; colony work explicitly releases native admission hold | Productive work/native handoff; engine worker boundary below |
| military: stranded recovery FIND / LOADING / landing | Idle same-zone stranded soldiers + exact hull | A | Separate 12/13; staged claim; expected-owner guard on all commands | Existing full/partial/wrong-zone bounded terminals |
| military: relic outbound / return / WAIT-CARRIER | Exact Priest/Brahmin, then relic carrier | A/B | Separate 14/15; passenger now explicitly reserved for round trip; no unrelated recalls | Mission terminal releases both |
| military: local asset detection / COMMAND | Owned attacked assets, then enemy military | B | Damage only starts a search; live hostile selected explicitly; no global retreat | Routine state machine |
| military: LOCAL-RESPONSE-REBUILD / DISPATCH | FREE idle nearby military | B | At most 8, same zone, no protected tasks; command reselects verified hostile | Quiet release, no army recall |
| military: perimeter builder evacuation | Nearby active wall/gate builders | A | Self/FREE; excludes active boar lurer; stop own work, same-zone safe TC garrison | One-shot safety intervention, no passenger preemption |
| military: naval HOME response | FREE idle ships near attacked coast | A/B | At most 8; keep all other naval owners; no global land recall or severe latch | Group 5 refresh |
| military: naval FIND-SHIP / FIND-THREAT | FREE idle same-water/coastal responders | A | Bound to 8; live exact enemy-player filter; ownership guard at command | Direct response, not whole navy |
| military: siege escalation (old recall source 3) | Global army formerly recalled for fortifications | B | Removed reset/retreat; retain force/siege composition and dispatch requirements | Ordinary attacks continue |
| military: loss regroup (old source 4) | Global army formerly recalled for losses | A/B | Removed reset/retreat; retain larger-force planning | No task cancellation for convenience |
| military: periodic loss recovery (old source 5) | ALL units formerly reset/stopped | A | Removed all-unit reset and global retreat; retain loss accounting | No task ownership mutation |
| military: defense leash / home interruption | Native defenders, loaded hull, raid/screen | A | Removed broad move-home and low-threshold mission cancellation | Central severe policy only |
| severe-defense: per-player scan / acquire | Live enemy military within home 24, same zone, >=8 for one enemy | New explicit preemption | Enemy stance + ready military + zone + severity; capture exact enemy; cancel old owner -> release -> cap-16 acquire -> command | 45-second severe latch; loaded/split/remote missions protected |
| taunts: 45 retreat | Self FREE military in home zone | A | Bounded explicit selection instead of global reset/retreat | Active reservations retained |
| taunts: 31 / 61–68 attack | Native attack manager | A/C | Uses current native type exclusion list; refresh after newly acquired relief | Same native boundary as ordinary attack |
| taunts: 48 help / SCAN-THREAT | Actual enemies around retained original ally TC | A | No allied under-attack check or arbitrary villager; live exact enemy within 48, same zone | Persistent anchor retained after TC death |
| taunts: 48 DISPATCH / OWNERSHIP-COMMAND | Up to 12 FREE idle same-zone responders within 96 | A | Claim 17, revalidate target/player/status/zone, actual responder count before promise | Target loss/90 seconds/explicit severe cancel |
| home-anchors: players 1–8 | First reliably observed ready TC | New required information model | Record coordinate/zone once; never overwrite or clear on destruction | Permanent match knowledge |
| military: land raid | FREE idle native-compatible land soldiers | A | Command-time self/owner; no naval-scout slot collision | Group 8 contract |
| military: Palintonon/ram objective | Available siege family | A | Group 1, FREE admission, delayed command permission | Objective refresh; existing pack API defect separately deferred |
| military: capital siege | Juggernaut/Octeres shared controller | D/A | Intentional shared slot 2 retained; command-time self/owner reinforced | Shared family lifecycle, not competing owners |
| military: native sea exploration | Unrestricted engine boat selection | D | Already suppressed; remains zero | No native boat owner |
| military: naval Scout | Allowed Scout Ship types | A | Dedicated slot 16 rather than raid 8; command-time owner | Scout refresh; same-owner evasion |
| military: transport screen | Screening ship + reserved hull | A | Slot 7 no longer shared with relic ferry; owner checks | Route terminal; no convenience recall |
| military: transport escort | FREE compatible warships | D/A | Slot 9 retained; protect explorers/screens/response and recheck at each paired guard | Escort-only refresh release |
| military: capital escort / naval opportunity | FREE compatible ships, activity exclusions | D/A | Preserve working opportunity selector; reinforce command-time permission | Direct task; routine defense excludes moving/fighting units |
| military: ship evasion | Own naval Scout or FREE vulnerable ship | A | Capture expected flag; refuse command after another owner acquires it | Same-owner safety move, not ownership theft |
| military: Port clearance / quarantine / repair | Exact hull or eligible empty FREE hull; nearby repair workers | A | Permission checks including exact-ID quarantine exclusion; workers exclude reservations/lurer | Existing bounded routine; no congestion/geometry redesign |
| general: temporary worker cleanup | Eligible villagers, temporary group 0 | B | Exclude **all** owned groups and active lurer; recheck self/group 0 before STOP | Same-pass temporary release |
| homebase: farm staffing / fisherman / fallback | Same-zone eligible villagers | A/B | Selector + command-time reservation exclusion, lurer exclusion | Direct one-shot assignment; native gathering remains C |
| homebase: drop-site/TC/build assignments | Native builders, foundations; colony supporters | A/C | Native build admission gated during boarding; direct commands check self/owner | Existing construction lifecycle; no drop-site-race redesign |
| economy: retirement / trade transition | Population-blocked eligible idle workers | A | Direct deletion rechecks self/FREE/lurer | One-shot deletion; current retirement limits retained |
| hunt: lure/rescue/support | Exact lurer + eligible supporting villagers | A/C | Common reservation checks; other direct systems exclude lurer ID; clear stale ID when hunt ends | Existing hunt states; boar-after-garrison behavior deferred |
| economy/init/civ/homebase: gatherer percentages | Native economy assignment | C | Freeze new percentage/build/hunter admissions during migration boarding, restore saved assistance/repair policy | Does not claim a native per-object lock |
| civ Germani: Dejbjerg Wagon | Exact mobile-building ID | A | Recheck self/FREE before delayed movement | Existing bounded arrival/abort |
| civ Han/Kushans/Mauryans; rush; special placement | Native builders/hunters and direct workers | A/C | Same boarding admission gate; common direct permission filters | Existing construction/production lifecycle |
| taunts: 69 deletion | Explicitly flared owned structure | D/A | Bounded structure selection plus command-time self ownership | No transport/controller redesign |
| training/research/resource sensing | Production/census, not task assignment | D | No deliberate active-unit reassignment; unchanged unless actual build admission | N/A |

### Native API boundary — one controlled acceptance test

API source inspected: the project's saved AIRef snapshot
`.analysis/airef-reference-20260830.js`, including `up-modify-group-flag`,
`up-reset-scouts`, `fe-exclude-from-attack-group`, `up-target-objects`,
`sn-disable-defend-groups`, builder assistance/repair and civilian caps.
The current DE group domain is **0..19**, not UserPatch's 0..9.

- Native exploration: zero budgets alone do not release an existing explorer.
  Both zeroing and `up-reset-scouts` now precede explicit Scout-capable claims;
  positive budget writers stay gated while ownership is active.
- Native TSA defense and ungrouped-soldier scattering have no compatible
  passenger predicate, so they are disabled. Scripted bounded/severe defense
  replaces their unscoped admission. This must still preserve working attacks.
- Native attacks: `fe-exclude-from-attack-group` is documented to exclude
  **unit types** from attack-now and automatic attack groups. The exclusion list
  is rebuilt from all 17 active owner slots before dispatch, including taunts.
  A free unit of the same type waits too; this is explicit collateral admission
  suppression, not a per-object lock. No global reset cancels current attacks.
  Already queued native orders and native membership while idle remain an
  engine boundary, not statically closed.
- Native workers: direct selectors and new build/hunter/percentage admissions
  are protected. During boarding, builder assistance is disabled and ordinary
  automatic repair is suppressed, then exact prior settings are restored.
  Existing native gather/build assignments may still retask a reserved worker.
  The API does not provide a documented per-villager lock; builder caps do not
  eliminate the minimum builder, civilian percentage caps do not implement a
  lock, and repair level zero has a Wonder exception. We do **not** freeze the
  entire economy or claim these settings prove complete native protection.

Run one fresh preserved-lobby T11 match. Check all players, not only an observed
failure. For every reconstructable lift correlate claim/manifest, first boarding,
early ashore sample, full/partial/abort terminal and later landing. Existing
RAW44B samples include object ID, action/order/target/group and are rearmed per
mission; no lifetime RAW44W quota is deployed. Verify: no exploration/native
WORK/STOP interruption of still-ashore reserved passengers; distinguish STOP
after garrison from a harmful cancellation. If only native reassignment remains,
use that same controlled setup to discriminate existing native assignment from
new admission. Do not reopen source-safe writers merely because an old packet's
exact writer is unknown.

Acceptance additionally requires ordinary P3B44 combined attacks, T1–T7 full
and partial lifts, bounded routine defense, a verified severe response, allied
help at living/destroyed original TC anchors, and no own-TC or shoreline-fishing
flood. Static/fixture PASS is **not** runtime closure. Fresh engine acceptance
remains required; status is not CLOSED.

### Adversarial review disposition

- ACCEPTED: alias collisions, unscoped recalls, missing command-time guards,
  exploration reset/admission ordering, permanent TC anchors, actual responder
  count before a promise, selected-target pointer, converted group references,
  and partial-migration ashore reservation leaks. Implemented and tested.
- ACCEPTED: a first draft's severe transfer could release a split/loaded group.
  Now every surviving member must satisfy the local ashore eligibility before
  that owner can be cancelled.
- ACCEPTED: a first draft's native-exclusion jump `-1` repeated the jump itself.
  Corrected to `-2`; a source-executed program-counter fixture now covers the
  exact RuleDelta semantics with 40 distinct types and a finite-step bound.
- REJECTED: use group flag as engine lock, zero all native gathering, or hold
  ordinary attacks until every unrelated mission ends. None is a supported
  minimum fix; documented type exclusion and bounded admission are used instead.
- DEFERRED / one runtime boundary: native queued orders and worker reassignment
  as described above. Source fixes are implemented now, not contingent on
  identifying every historical STOP packet.
- KNOWN ISSUE — POST-RELEASE: congestion, landing geometry, unload spam,
  Port placement, boar resumption, drop-site race, salvage/Market/Wonder, crash,
  assault landing memory. Source inspection also found the existing Palintonon
  `action-pack` used through `up-target-objects`, which the reference does not
  support; no unrelated siege-pack behavioral patch is included here.

## Historical diagnostic-stage record (superseded by T11 above)

The following sections retain the evidence and limitations from before the
source-first implementation; statements saying ownership is not implemented
describe that historical checkpoint, not the current branch.

R2-arrival release priority completed first: R4:455 is installed and all 68
files verified. Only hunt distance changed 28 -> 16; food 12 and all eight
self-target fallback guards were already present. Eight new regression tests
protect both invariants; all 163 tests pass. No ownership or military runtime
change. The directive's premise that these guards were lost is contradicted
by current source/history; do not use it to explain away the observed own-TC
or passenger behavior. See HANDOFF.md for hashes, separate commits and pending
fresh-runtime acceptance. R2 ownership analysis resumes with the archived R2
map, not the current R4 map.

This is the user's 2026-08-30 architectural recovery objective. It supersedes
the earlier narrow restriction against changing ownership/recall in this
experimental worktree. It does not authorize navigation, landing-coordinate,
route-scoring, recovery-unload, Mining Camp resource-wait, escort-geometry,
unrelated command-flood, salvage, or Port-placement changes in the same patch.
No runtime behavior was changed in this investigation. T8 now identifies the
recorded global-recall callers, including a proven siege-escalation overwrite
of Red's boarding orders; worker/native attribution and the shared protection
mechanism remain unresolved. See the T8 update below, not the older T7 limits,
for current caller evidence.
T10:451 passenger-writer telemetry FAILED engine compilation (ERR6003 at
rawai-init-goals.per:362). T10R1:452 reused 12 string constants and produced
visible RAW44W output in the user's running match, but misclassified generic
villager cleanup as a reservation change and logged it while no mission existed.
T10R4:455 is now installed: retains R2's actual-mutation classification and
adds delayed, staggered, bounded identity announcements after R1's startup
marker/map loss was established. All 351 source sites are retained;
R3 engine/replay acceptance remains pending. The R1 replay map is preserved at
`G:\Projects\Codex\Rome at War AI\.analysis\p3b44t10r1-writer-trace-sites.json`.
The user explicitly restored this as the priority over congestion investigation.

R1 18:10 replay now establishes SCOUT-ferry interference (not worker migration):
source-1 land-defense recall interrupts Green twice and Orange twice; Purple
and Orange receive exploration order 705 during boarding while group flag 4
remains visible. R1's writer quota is exhausted for all players at 05:40-05:41,
before first boarding at 10:05. No startup map/marker survives, so zero players
pass fingerprint validation. Missing trace data cannot identify other writers.
All 15 scout episodes across eight players are recorded in HANDOFF.md and the
new R1 benchmark: five full-load confirmations, ten empty aborts (five with
recorded preemption, five still approaching at timeout), no assault episodes.
Root-cause evidence is sufficient to name the scout preemptors; the controlled
native exploration release/protection mechanism and wider worker ownership
remain unresolved. Do not substitute another congestion investigation for them.

## Required invariant

### R2 all-player evidence update

After the release-blocking recovery was deployed, R2 was audited: 282,006 exact
events, 20 identified hulls, 160 load packets and 58 raw loading windows.
Missing boundaries mean those windows are not 58 fully proven lifecycles.
All 76 retreat packets have existing source labels. Orange's priests 33235
and 34388 receive land-defense recall during relic boarding at 27:37 and
37:18. Their assault/migration goals are both idle: those goals alone cannot
represent every passenger owner. Preserve this as a common-contract requirement.

Purple's 48:32 siege recall is route-stage SCREEN-FIND, after partial departure;
Green's 55:24 recall is WAYPOINT-WAIT. They include prior passenger rosters but
are not proof of boarding interruption or forced disembarkation. Blue scout
4608 has repeated STOP 706 (283 and 276 packets in two short boarding intervals),
with later idle/ashore/distance-1/group-4 samples. Producer remains unresolved:
Blue's trace budget was already exhausted. STOP for an already-garrisoned unit
must not be confused with harmful ashore cancellation. The late 20-unit worker
load has insufficient occupancy evidence to label every STOP a lost passenger.

R2 contains no complete marker/map identity; new writer-site attribution remains
withheld. R4 preserves R3's delayed identity fix, which this earlier replay
cannot validate. Keep the known recall cause distinct from the unidentified
STOP/native boundary. Full evidence, limits, positive outcomes and exact
artifacts are in HANDOFF.md and the R2 benchmark. No further runtime change was
made during this audit; common ownership implementation remains pending.

### Contract

A deliberately reserved unit remains owned by its task until that owner
completes, aborts, loses the unit, explicitly releases it, or accepts a verified
higher-priority emergency. Issuing a newer command is not an ownership transfer.

- Ordinary acquisition must exclude incompatible task-owned units, including
  assault/migration boarding, active expeditions, relief, scouts and siege.
- Apply the same rule to worker selection, builder/repair assignment, drop-site
  and idle-worker retasking, hunting support, retirement and resource pressure.
- Revalidate permission at command time, not only at initial selection; other
  controllers can run between selection and dispatch.
- An emergency must establish hostile identity, live presence, relevant
  distance and severity, then cancel/release the old owner before acquiring
  units. Damage flags alone cannot authorize strategic recall.
- Routine/local threats acquire a bounded free pool. They do not cancel active
  attacks or passenger tasks. Global recall is only a verified severe strategic
  emergency with explicit owner cancellation, not a regrouping convenience.
- Allied relief uses a persistent first-Town-Center coordinate per player.
  Capture the first reliable TC anchor, retain it after destruction, search
  live enemy military near that coordinate, and dispatch available responders
  toward the verified enemy position. No allied under-attack predicate and no
  arbitrary surviving-villager substitute. A current TC may be an additional
  anchor, not a replacement for the persistent original.

These are acceptance requirements, not claims about current behavior. A DUC
group flag is not a verified lock on native economy/attack/exploration tasking.

## Replay-wide audit

Source: T7 `SP Replay v101.103.48987.0 @2026.08.30 131412.aoe2record`, SHA-256
`04AB5E6664F9DBE0284E320A99AB16070DBC00DE67FE876AC8C5512176E7DDB5`.
The prior verified T7 runtime identity and original selected colors/teams are
retained in HANDOFF.md and its benchmark. The following table is historical T7
evidence; T8 was subsequently supplied and audited below.

`tools/audit_task_ownership.py` reparses the raw stream. It checks exact packet
lengths for Transport lists, all retreat members, multi-unit AI_ORDER and WORK.
It never shifts an object ID based on its magnitude. The stock SPECIAL and
UNGARRISON decoder misses a one-byte field in this replay; WORK was absent and
AI_ORDER misread the order field and omitted additional selected units.

All 378 load commands on the established 25-hull union are covered, with
132 evidence-delimited boarding windows and every one of the 202 retreat events. The
windows have 33 assault, 41 migration and 58 unresolved/recovery/relic owners.
Full-load corroboration is not an individual boarding acknowledgment. Every
passenger record retains its initial garrison, first subsequent other command,
time/target, source hypothesis, reservation samples, result and uncertainty.
Every retreat retains exact members and their preceding commands/task links.

| Player | Windows | Successful, corroborated | Pre-boarding conflict with owner evidence | Unresolved | Retreats |
|---|---:|---:|---:|---:|---:|
| Red | 31 | 35 | 9 | 185 | 36 |
| Green | 9 | 2 | 9 | 52 | 35 |
| Yellow | 1 | 1 | 0 | 0 | 31 |
| Purple | 23 | 21 | 4 | 148 | 22 |
| Orange | 26 | 2 | 3 | 215 | 1 |
| Cyan | 4 | 1 | 2 | 19 | 23 |
| Blue | 13 | 2 | 12 | 100 | 53 |
| Gray | 25 | 1 | 44 | 186 | 1 |
| Total | 132 | 65 | 83 | 905 | 202 |

Passenger columns count passenger-window instances, not distinct people or
failed voyages. Of 1,053 instances, 56 have full-load corroboration and nine
have exact partial-landing membership without an observed conflicting command;
83 have a pre-boarding conflicting command and owner evidence, and 905 remain
unresolved (323 include a conflict whose
pre-boarding timing/continuous ownership is not established). No individual
death or genuine loss of availability is proven by this command stream; do not
turn that into a claim that nobody died. Exact flags at overwrite are generally
not recorded, and uninterrupted ownership between sparse snapshots is not
directly observable. Later retries/samples establish that the unit was still
ashore; they do not identify the writer or exclude an unlogged legitimate
preemption. The tool preserves these qualifications per record.

First conflicting commands in the 83 corroborated pre-boarding cases:
67 WORK, five ORDER, seven garrison commands targeting a different object,
two AI_ORDER STOP, one AI_ORDER explore, and one STOP. These are command
categories, not a universal cause. Some units ultimately board successfully.

The Red 55:02.350 event begins with STOP before its retreat packet, so the first
divergence is earlier than the retreat itself. Orange's 61:36-62:06 repeated
STOPs remain a separate producing path: its only retreat is at 67:46.218.
Worker WORK overwrites occur across Red, Green, Purple, Orange, Blue and Gray;
Cyan also has a resource-target ORDER. The issue is therefore not limited to
military retreat, but native versus script-triggered worker attribution is open.

## T8 caller attribution and late Red obstruction

T8 `20260830-154021`, SHA-256
`C7BDFAF53DE72F03012C5AD88F4B930E9B7670A07CDC96490489F7428F2CE29F`,
matches marker `RAWAI-P3B44T8:449` and the recorded 68-file deployment hash.
All-player totals: 190 loading commands, 58 boarding windows, 354 passenger-
window instances. There are 28 full-load-corroborated successes without an
observed conflict, 34 conflicts with later ashore/owner evidence, and 292
unresolved instances (108 include a conflict with uncertain pre-boarding
timing/ownership). These remain evidence categories, not failed-mission counts.

Every one of the 100 DE_RETREAT packets maps to one of 56 tagged invocations:
land defense 28 invocations/47 packets, naval defense 16/32, siege escalation
11/19, loss regroup 1/2. Sources 5 and 6 do not occur. A single invocation can
emit adjacent land and naval packets at the same clock. A one-label-per-packet
join incorrectly leaves 44 packets unattributed; those are not evidence of
native recall. The corrected external join retains both packets and exact
source-label sequence. All labels have matching packets.

At **54:03.506**, Red's source **3 (siege escalation)** emits a 62-member land
recall toward TC 4434 `(31,136)` and a 13-member naval recall toward Port 30910
`(20.5,122.5)`. Assault state is 33, hull 31341. Passengers 40149, 43815 and
47309 received boarding at 53:56.856, then this recall, and appear in the
54:10 boarding retry. Later samples of 47309 and 40149 retain flag 4. This
establishes that the scripted fortification-escalation recall can overwrite
boarding without releasing the reservation. Its trigger is three known
fortifications, not a verified severe home emergency. Sparse flags do not
prove continuous ownership at every instant; later partial loading does not
mean this recall permanently prevented the voyage. Red's 55:04.182 source-2
recall occurs during route screening, not the earlier boarding window.

Separately, the user confirms that Red's late physical blockers were other
Transports manually moved away. Playback at 66:24 shows the migration hull
with four villagers and two adjacent empty Transports. The command stream
records moves of 48064/31880 at 66:30-32; migration hull 31691 receives its first
departure at 66:31.236 after the 30-second partial-load deadline and reports
route distances 52/30/15/0 through 67:32. T3 clearance belongs to the assault
departure state machine, not migration boarding/departure. This is a coverage
gap, but intervention overlaps the normal loading deadline: do not claim the
replay proves a failed post-departure stall detector, or that every preceding
second of waiting was caused by collision. Retain the physical symptom and
the precise timing limit together. Do not mix a congestion micro-fix into the
shared ownership patch.

The raw reports, per-player table, preserved successes, and next diagnostics
are recorded in HANDOFF.md's T8 section. This audit changes no runtime behavior;
neither physical congestion nor the broader ownership defect is resolved.

The subsequent user screenshots also establish missed Blue obstructions at
49:11 and 66:50. Correlated commands show a no-departure assault wait followed
by home unload (35026), and later exhausted migration route/return attempts
(36912). A command-linked hull census is not a census of physical blockages;
absence of a congestion tag is not success. HANDOFF.md records the screenshots,
exact windows and prepared T9 terminal diagnostics. Those diagnostics add no
ownership/navigation behavior and do not establish safe blocker eligibility.

## Script command boundaries

The audit report also inventories 247 command/build-delegation rules and 248
selection rules across runtime PER files, preserving source file, line, facts
and actions. This is a source-boundary inventory, not a completed certification
of every controller's ownership safety or native strategic-number behavior.
An omission of a filter
in a dispatch rule alone is not proof: some selectors are in preceding states.
Conversely, an earlier filter does not prove permission survives until dispatch.

| Boundary | Current source evidence / implementation obligation |
|---|---|
| Generic worker cleanup | Excludes migration group 4, not a common all-task invariant; temporary group 0 mutations must respect every owner. |
| Farm/fisherman/colony/lumber staffing | Some paths filter group 4, others do not; stored-ID retasks require command-time ownership verification. |
| Hunting support | Some selectors exclude group 4; exact lurer rescue and other task reservations need explicit compatibility. |
| Retirement | Bounded trade retirement excludes grouped workers; legacy global idle deletion has no per-unit permission gate. |
| Native economy/build/repair | Percentage settings and persistent builder assignments delegate selection to the engine. Script filters alone do not prove protection here. |
| Local/naval defense and defend leash | Unfiltered local military selection and global recall can touch incompatible tasks. Acquisition and recall must share the invariant. |
| Raid/attack preparation/recovery | Audit free acquisition against active native attacks as well as flagged groups; currently no complete shared contract. |
| Active transport/scout/siege/escort | Preserve successful T1-T5 paths; inspect acquisition, explicit terminal release and shared group-slot lifetimes, not navigation. |
| Relic ferry | Hull is flagged, but the exact priest is tracked by ID without equivalent passenger reservation; include it in the ownership design. |
| Allied relief | Already avoids allied under-attack in this branch, but searches current TCs plus villagers; no persistent original anchor or retained relief ownership. |

All six global retreat sources lack a complete explicit task-cancellation gate:

1. Land defense: one siege unit, five threats, or two threats after commitment.
2. Naval defense: two threats after commitment or four regardless.
3. Siege escalation: three known fortifications, not severe home invasion.
4. Loss regroup: repeated attack losses, not severe home invasion.
5. Periodic losses: broad all-unit STOP, attack-group reset and global retreat.
6. Allied taunt 45: broad all-unit STOP and global retreat, without threat proof.

This proves incompatible source capability and specific runtime intersections;
it does not assign every recorded retreat or WORK packet to an exact rule.
The later policy must distinguish an explicit human strategic request from
ordinary automatic preemption while still canceling old owners cleanly.

## Remaining discriminating evidence and tests

T8 already labels the six recall sources with assault/migration states/hulls.
Use it for exact recall attribution, but do not pretend those six tags cover
every worker writer or native engine task. T10 now brackets 351 command,
reservation/group and native-policy/delegation sites with source-map-verified
IDs and pre/post assault/migration state/hulls plus selected-object identity/flag.
The map retains exact actions, including acquisition/release intent; replay
packets supply commanded members. No new ownership permission lock is implied.
The compiler adds no search/filter resets or gameplay commands, and relocates
existing jumps to the same original targets (including the guarded farm jump).

T8 directly demonstrates that command packets may arrive AFTER after-command
chat. The new analyzer preserves compatible deferred issuers, not just packets
inside brackets, and refuses to choose among multiple candidates by proximity.
Both explicit quota gaps and absent map fingerprints block unsupported caller
inference. An untagged WORK packet remains unresolved, not automatically native.
See HANDOFF.md's T10 section for bounds, hashes, source-map generation and the
`--writer-manifest writer-trace-sites.json` all-player audit invocation.

The required gameplay/deterministic contract tests are **not implemented or
passed** in this diagnostic revision: assault reservation versus ordinary
military controllers; migration reservation versus economy controllers;
complete/abort release; bounded routine defense; verified severe preemption;
friendly-fire rejection; allied help with live TC, destroyed TC and no hostile.
All-player runtime acceptance must additionally preserve ordinary P3B44 attacks,
successful T1-T5 missions, safe partial lifts and economic settlement progress.
Packet/lifecycle-tool tests are separate and cannot substitute for these tests.

No selector/global-retreat/anchor patch or navigation change was made here.
Installed runtime is T10R4:455, generated in memory from this same checkout by
`tools/sync_test_ai.py --writer-trace`; T9 was never a separate installed test.
T10:451 was rejected by the engine's string table. T10R1 reduces payload literal
occurrences from 5,665 to 1,465 and adds an occurrence-based build budget plus
a regression fixture reproducing the rejected expansion. R2 corrects the idle
trace exemption for site 41 and preserves real acquisition/release sites.
R3 sends marker/map identity three times after startup, with players staggered
and 30-second intervals independent of invocation quota. 163 regression tests
and all 68 deployment hashes pass; fresh engine/replay acceptance is pending.
First check R3 identity delivery and off-mission trace suppression. R1's replay
is audited and its exhaustion confirmed; preserve R1/R2 maps for old recordings.
Unchanged fields do not imply no competing command.
The work is open; this document, the audit
and the diagnostic additions are intermediate evidence, not resolution.

## Reproduction and audit validation

From the documented transport worktree, use the Python 3 path in HANDOFF.md:

```text
python tools/audit_task_ownership.py "C:/Users/LostSoul/Games/Age of Empires 2 DE/76561198053747760/savegame/SP Replay v101.103.48987.0 @2026.08.30 131412.aoe2record" --parser-root "../../.analysis/replay_parser_kjir" --transport-audit "../../.analysis/p3b44t7-transport-audit.json" --output "../../.analysis/p3b44t7-task-ownership.json"
```

The prior transport audit supplies the independently established hull/color
union and partial-landing evidence; it must belong to the same replay. That
older artifact has no embedded replay hash, so the new report records both
input hashes and the dependency explicitly rather than claiming an automatic
cross-file identity check. Preserve the raw report outside the AI repository.

Read-only adversarial audit findings:

- ACCEPTED: decode object arrays by exact packet length, never ID magnitude;
  retain all members and the actual AI_ORDER field.
- ACCEPTED: do not invent a 45-second task timeout; end windows only at recorded
  terminals/unloads/new starts, with replay-end cases explicitly unresolved.
- ACCEPTED: distinguish full-load corroboration, exact partial landing, conflict
  with later ashore evidence, and unresolved outcomes. A DELETE request does
  not prove execution or death.
- REJECTED: treat group 4 as an engine-task lock, attribute every STOP to global
  recall, or call a later successful lift a prevented completion.
- DEFERRED: exact writer/native-task attribution and uninterrupted reservation
  at overwrite require the missing boundary telemetry, not stronger wording.

Packet and lifecycle regression tests verify these audit properties only.
They do not implement or pass the gameplay tests required by section H.
