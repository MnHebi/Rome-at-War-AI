# T55B causal investigation — 2026-09-07

## Identity and evidence-to-change gate

Replay `SP Replay v101.103.48987.0 @2026.09.07 121439.aoe2record`,
SHA256 `632D89F42B339B06E6B83EF9A58F1FE7855EED9DB22DD3A200B2DDDA4A005858`,
114:19, marker T55:503, runtime source `1f87ef0`. Analysis started at
`6f1d31a` on `fix/trade-cog-cap-dacian`. Installed runtime is untouched.

External artifacts below are under `G:\Projects\Codex\Rome at War AI\.analysis`.
`t55b-causal-extract.json` and `t55b-extended-extract.json` use the exact
`audit_task_ownership.read_stream` decoder, preserving milliseconds, byte offset,
raw payload and actor arrays. The broad summary's AI_ORDER fields and shifted
UNGARRISON interpretation are NOT suitable for these joins. Corrected hull
commands use length-checked payload arrays. No decoder failures were reported.

### Shipyard gate

**OBSERVATION:** Red 47:13: desired6/completed0/total0/pending0, two Ports,
affordability1/can-build1, tech-hold0/worker-hold0. Cyan 34:38: desired2,
completed1/total1/pending0, two Ports, the same four gate values. Both then
execute retained batches, not a persistent admission hold.

**CAUSE:** Individual rejected candidate footprints include unsuitable terrain
and occupied/too-close sectors. The unresolved *delay* cannot be assigned to a
wrong buildability predicate: `up-can-build-line 0 gl-shipyard-x c: shipyard`
uses valid consecutive goals137/138, actual type1251, and documented
without-escrow mode. Reason64 conflates resources with spatial failure; a prior
minute's affordable snapshot cannot prove affordability at every rejection.

**CORRECTION:** No gameplay change justified. Add a time-bounded rejection
snapshot with candidate, anchor coordinates, tier and contemporaneous resource
availability, without changing the query, search, sampler or admission policy.

**UNCERTAINTY:** Initial terrain plus issued construction does not reconstruct
live occupancy, survival, exploration or engine foundation rules. Do not mark
visually plausible alternatives as engine-buildable.

### Voyage gate

**OBSERVATION:** Cyan35241 receives ORDER(59,132) at43:24.261 and43:32.437;
first recovery UNGARRISON(197,187)45:00.188. Repeat48:14.140/48:22.315 ->
49:50.115. Cyan35302 repeats the same destination46:12.156/46:20.290 ->
47:48.520, and49:31.621/49:39.252 ->51:07.418. No intervening commands to
these exact actors appear between movement and recovery.

**CAUSE:** Earliest demonstrated failure is a no-progress decision on the
waypoint leg, not absent dispatch or a demonstrated overwrite. The exact hull
positions and watchdog distance/best updates are absent. The map places59,132
in water(type1), at the inner end of a southern mainland inlet; it is not a
land tile. The nominal straight line from home crosses mainland and is NOT
an engine trajectory. Geometry, blockage and accounting remain distinguishable
hypotheses, not established causes.

**CORRECTION:** No timer or routing change. Broadcast existing private position,
cargo, distance, best and deadlines at initial leg sample and no-progress
decision, without extra search or object selection.

**UNCERTAINTY:** Orders are destinations, not position samples. No evidence
identifies merchant obstruction. A longer timer is not a causal repair.

### Worker gate

**OBSERVATION:** Worker43834 was ordered onto hull39461 at92:23.621 and
92:28.052 in a20-worker SPECIAL order5 group. At92:29.578 a single-actor
AI_ORDER706 stream begins:8,823 packets =8,823 actor incidences, target-1,
coordinates(-1,-1), ending96:10.911. At96:10.936 (25ms later), ordinary ORDER
targets42875 at184,190; then96:23.625 targets7759 at189,204.

**CAUSE:** Boarding is the immediate antecedent, not the earlier House build.
The recording does not expose43834's action/group/carry at onset, nor the
issuing PER/native boundary. Missing private economic telemetry cannot exclude
a writer. Cross-player observability is a source-proven defect:640–657 use
`up-chat-data-to-self`, while the relevant floods are not Blue.

**CORRECTION:** Broadcast the existing bounded economic sample, make modifier
explicit, and count command-site invocations separately from sampled details.
Keep the four Ctrl wrappers, immediate resets and every filter unchanged.

**UNCERTAINTY:** Do not label706 an explicit STOP. Do not infer a native
producer, successful boarding, productive retasking, or a Ctrl PASS.

## Detailed spatial cases

`t55b-site-cases.json` contains full sampled sequences, 3x3 terrain windows,
anchor construction joins and prior own/allied BUILD records. Map crops:
`t55b-sites-p2.png`, `t55b-sites-p5.png`. Red crop covers the eastern anchor;
its other anchor is outside the crop. Red rectangles are nominal3x3 footprints,
not an engine placement simulator; white dots are prior builds, not survival.

Red anchors34662 Port(46.5,16.5),38299 Port(125.5,31.5) rotate between batches.
At47:15 candidate(58,11) reaches reason67: buildability and spacing have passed,
but every tested water orientation fails. (49,9)47:16 reaches own-clearance65.
At(58,11), east W5=(64,17) is land0; south W1/W2 are land0; west
W6=(52,17) is land0; north W2=(58,-1) is outside the map. Thus every
orientation has an independently visible failed aperture/bounds sample.
This is evidence for retaining that check, not weakening it. The map does
not prove the other water samples were dynamically unoccupied or reachable.
At47:19–47:23 the38299 batch tries (113,30),(113,28),(134,30),(133,22),
(126,20),(136,32),(134,40),(124,30), all64. (134,30)'s nominal3x3 is all
shallow water; (136,32) rows are water/beach/land. These are different
geometries hidden by the broad coastal/mixed label. Later first successful
foundation53179 is(137.5,31.5),55:16, ready55:58: nearby, but neither the same
point nor the same runtime occupancy/resources. No proof that47:22(136,32)
was buildable. Subsequent expansion to four ready records must survive.

Cyan anchors34661 Port(199.5,186.5),35738 Port(174.5,184.5),36188
Shipyard(186.5,185.5). At34:38–34:42 the34661 batch tries (188,183),
(192,201),(203,183),(207,196),(191,176),(206,179),(204,185),(211,185).
All64 except(204,185)65. The next35738 batch tries(164,183),(183,186),
(187,187),(179,179),(181,183),(179,182),(180,199),(186,183), all64.
(188,183) mixes water/beach/land next to the existing yard; (186,183) is
all-water in its nominal3x3 and immediately north of that yard. (164,183)
mixes shallow water/beach; second yard later appears(163.5,182.5),81:00,
ready81:32. Again, nearby is not identical. All eight attempts0–7 occur;
there is no evidence of the previous sparse-sampler regression here.

Classification: A unsuitable proposals demonstrated; B wrong query input NOT
demonstrated; C repeated sectors demonstrated but dense batches remain active;
D some admission/resource restrictions demonstrated, not every affordable delay;
E no issued-without-foundation gap among24 builds; F Blue's exact ready event
missing, but completion corroborated below. Purple's51 unaffordable snapshots
and zero builds establish sampled resource limitation, not continuous poverty.

Blue49162 at51:22.166 receives build702 from38510, then38876,39025,35986
within90ms. Fingerprint539 selected38510, matching one native builder (not
proof that build-line explicitly assigns that worker). Foundation541/542=1
at51:22.663; no542=2. At52:50.326 snapshot527=1,528=1,529=0 while only this
yard had been built. That corroborates completed construction by52:50, despite
the missing exact ready event. It also becomes anchor49162 at51:50. Later706
packets include49162 in a four-building array through88:49; these are not
explicit destruction evidence. Preserve the distinction:23 ready-event records,
24 foundations, and independent completion evidence for the remaining one.
The next builder packets are706 at51:49.407 (35986/38876/39025) and
51:49.418 (38510). They do not themselves prove completion or cancellation;
the later completed-count observation supplies the independent corroboration.

## Voyage comparison and recovery

`t55b-voyage-endpoints.png` overlays failed and successful command endpoints on
THIS map. Red/white straight lines deliberately do not claim engine paths.
Failed early candidates target Green TC7741(28,120), sampled landing(55,131),
witness35456; the landing point is land(type0), the waypoint(59,132)water.
Candidate diagnostics precede final commitment and are sampled, so they do not
prove every sealed-plan field retained that value. Movement proves59,132 was
actually commanded. Different hulls repeat this objective/waypoint relationship.

35241 receives no further recorded command after49:50 recovery until79:11;
the79:04 empty-return event establishes controller-observed empty cargo, not
the exact time/place of unloading.35302 has no later command after51:07 in
the inspected recording. At97:46 all Cyan slot states are4 (quarantine).
Quarantine intentionally holds ownership without issuing a continuing recovery
loop. Physical completion of those recoveries remains unobserved. Do not infer
that slot release or a home-directed unload command physically rescued cargo.

Successful Cyan49916: rendezvous ORDER(191,190)108:19/108:22; waypoint
ORDER(182,148)109:15.059; UNGARRISON(141,144)109:39.372/109:39.949;
home ORDER(184,186)110:11.508; landed event110:19. Latest sampled accepted
candidate109:09 is objective91285, landing141,144, witness-1. Thus a no-witness
path also reaches cargo-empty/handoff; this does not prove terrain egress or
productive combat. Preserve candidate -> command -> empty cargo -> handoff ->
target activity as separate evidence levels.

## Worker history and terminal context

`t55b-actor-43834.json` has14 compressed command groups. Initial targets7419,
7470,6871,7691,7717 are Gaia type351 trees, verified against the header.
50:22.774 House70 construction identifies a worker role, not a flood trigger.
86:32.051 WORK targets94020 at206.5,189.5: Farm50 built86:09, corroborated
by first construction702 at86:09.791. Boarding follows92:23/92:28.
The20-person manifest includes43834, but92:31's action617/group11/target39461
sample is actor91744, NOT43834. At92:58 the load has18/20; the sampled remaining
actor42268 is617/group11. Do not transfer either observation to43834.
At92:58.395 diagnostics560=5,561=42268,562=2,563=39461 identify the partial
release. The explicit STOP at92:58 targets only42268 and43118.43834 is NOT
among them. The source removes garrisoned passengers before this STOP and
retains cargo in the migration group. This supports a cargo-context inference
for43834, but does not directly reveal its engine task at flood onset.

Hull39461 starts moving(219,156)92:58.976, then alternates approach/unload
commands:93:29.807(188,128),94:22.861(196,126),95:15.636(204,124).
It receives home unload(189,204)95:37.219,95:52.662,96:08.153. Flood cessation
96:10.911 follows this return sequence, then43834 receives the two TC-directed
orders.7759 is header-confirmed Cyan TC109.42875 is coordinate/build-correlated
to Cyan TC109 built41:15 at184,190; no direct creation702 identity was found,
so that type attribution is inferred, unlike7759. No explicit STOP targets
43834 during the flood. Its earlier explicit STOP was62:25.503.

This is consistent with a boarding/return task interaction, but does not identify
which controller or native task emits706. The currently sampled economic fields
do not cover43834. All15 Blue Ctrl samples are irrelevant to causal exclusion
for this Cyan episode. Exact actor action/garrison/group at onset and the first
producer boundary remain missing. No gameplay repair is claimed for this flood.

Source-writer audit reused `T53-VILLAGER-KEYSTATES-AUDIT.md` and the ownership
inventory, then checked the implicated families: the four free-worker economy
writers; general stale enter/build cleanup (counters1/2); migration boarding,
partial STOP/release (counter5), return/deposit, dropsite and owner recovery;
TC safety/boar rescue. Transport escort counter3 targets its vessel group.
Counters90/91 are native attack exclusion-list reset/type exclusion, NOT
STOP packet counts. Their93:00–96:00 activity does not identify a706 producer.
`MIGRATION-RETURN-DEPOSIT` can issue the observed TC relationship for carrying
home-zone settlers; its private boolean message and missing exact actor/carry
sample prevent definitive attribution of96:10.936 to that writer. Ordinary
ORDER does not encode that policy distinction. No new Ctrl wrapper is justified.

## Status and acceptance

Shipyard expansion: EXERCISED-PASS; affordable-delay cause: INSUFFICIENT-OBSERVATION.
Cyan early voyages: EXERCISED-FAIL; physical cause: INSUFFICIENT-OBSERVATION.
Cyan49916 cargo-empty/handoff: EXERCISED-PASS; egress/productive combat:
INSUFFICIENT-OBSERVATION. Worker flood: EXERCISED-FAIL; Ctrl causal assessment:
INSUFFICIENT-OBSERVATION. Help, productive colony and real-choke ROW remain open;
no new acceptance claim. No expedition tuning.

Fresh ordinary matches must show timely concrete yards with usable exits,
actual hull progress/physical recovery, passenger land egress, and productive
worker tasking without actor-level floods. Static tests cannot close these.

## Implemented observations (not gameplay repairs)

- `rawai-homebase.per`:640–657 now broadcast, preserving the existing selected
  worker/pre-target/new-target/time and delayed action-role-target sample.
 658 records modifier2 with the post episode. Four independent invocation
  counters are incremented at the four existing command sites, outside detail
  budgets.659–665 report game time, four counts, completed samples and estimated
  unsampled invocations every300 seconds. Windows can straddle an episode;
  counts are invocations, including potentially empty post-filter lists, NOT
  native packet counts. A missing actor fingerprint cannot exclude a writer.
  Routine economic samples cannot spend migration STOP/release reservations.
- Shipyard generator:666–676 report one reason64 candidate per60 seconds,
  including its anchor position/tier and current can-afford/can-build/available
  wood. This is next to rejection, not a minute-old admission snapshot. The
  first parameter remains0 (without escrow). No query or safety gate changed.
- Assault generator:680–690 record slot,hull,event,time,state,x,y,distance,
  best,progress deadline,cargo at first outbound-leg sample and at no-progress
  cancellation before recovery mutates state. Read only existing private goals;
  no new search, selected-object mutation or deadline extension. Destination
  commands remain in the replay. Quarantine emits no repeated start snapshot.

No runtime marker changed; none of these observations is deployed. Existing
T55B cannot validate their future visibility. Observation repair status:
FIXED-PENDING-RUNTIME. The three gameplay defects remain INVESTIGATING.

Validation: focused economy9, Shipyard25, assault20 and new observability7
tests PASS. Full Python3.12 discovery579/579 PASS with normal Windows Temp
access; first sandbox run hit only a writer-trace temporary-file permission
error. PER structure/operands PASS after splitting oversized diagnostic rules.
Strategy1156 matchups, naval doctrine, keystates(four wrappers), ownership1031
sites/zero direct failures,42 replay benchmarks, and generator synchronization
PASS. The six pre-existing civilization output differences remain unmodified;
`validate_good_units.py` still reports the known frozen AI RAW hash mismatch.

Read-only falsification review: command-bearing rules in all three affected
runtime files were compared with6f1d31a after removing chat and the new
diagnostic invocation increments: facts and gameplay actions are identical.
Accepted review corrections restricted initial voyage snapshots to outbound
states (prevent quarantine repetition) and split oversized observer rules.
Rejected behavioral proposals: timer increase, escrow/sampler/aperture tuning,
and spreading Ctrl, because this evidence does not establish those causes.
Deferred: exact engine task/producer attribution, physical voyage progress,
and reason64 engine occupancy/exploration. Context validation and diff-check
PASS. Full-suite tests include migration/relic/ownership and existing strategy,
naval, planner and replay regressions; no six-civ regeneration occurred.

Separable implementation commits:

- `66531c5`: cross-player economic episodes and coverage.
- `dd592c7`: contemporaneous sampled Shipyard rejection inputs.
- `b4a230b`: private voyage progress snapshots.

These commits repair observation boundaries, not the unresolved physical
defects. Do not describe any of those three gameplay causes as proven or closed.
