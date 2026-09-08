# T56 resource, overseas utilization and counter-production audit

## Identity and limits

Replay `SP Replay v101.103.48987.0 @2026.09.07 144755.aoe2record`,
98:21.33; SHA256 `708AF267E74E6E77F5984F8FAE2AB9E8C94D15BA82683768185BE51F01491B5A`.
Recorded marker T56:504; installed 103 files were byte-identical to documented
runtime `FB515FA0A52859BCC677353D7B06B38792DC6DAF4C03604AA793EBF30D707730`
before this audit's edits. New changes are NOT deployed.

Selected colors validated against DE lobby metadata: Blue1, Red2, Green3,
Yellow4 (first team), Cyan5, Purple6, Gray7, Orange8. Civilizations 6/22/26/28
versus16/17/4/7. Do not use internal-color fields for attribution.

External artifacts in workspace `.analysis`: `t56-full.json`, `t56-exact.json`,
`t56-episodes.json`; extraction scripts `t56_extract.py`, `t56_summary.py`.
Corrected command decoder: zero layout failures. Commands and controller state
are not simulation acknowledgments; MAKE is a production request, not completion.

## 1. Missing productive migration — INVESTIGATING

User observation: Blue/Yellow exhausted island resources without effective migration.
The state sweep distinguishes non-admission from unsuccessful admitted missions:

- Blue mining hull35736: boarding35:09, observed2 passengers on partial departure
  about36:15; two sailing/shore-rejection cycles; returning37:47, idle38:32.
- Blue hull38342: subsequent mining admissions43:04 and47:57; observed4 and6
  passengers respectively; shoreline refinement/candidate selection goes directly
  to returning at43:41 and48:43. No productive-colony state in these episodes.
- Yellow hull35010: mining admission36:46; observed9 passengers37:20; sailing,
  then dropsite placement37:59, wait38:00, confirmation38:01; idle38:49.
  This is evidence of a dropsite attempt, NOT proof of completion/gather/deposit.
- Red/Green also admitted loaded resource missions that returned. Gray admitted
  one late mission around95:17. No migration lifecycle records for5/6/8.

Late first admission snapshots repeatedly show128 or128 plus another blocker
for Blue/Yellow. Source assigns128 to `up-pending-placement town-center`, and
both actual admission and diagnostic admission refuse that condition. Other
snapshots show route/clearance ownership. A native pending Town Center can thus
block the resource escape path even with an idle colony controller.
CAUTION: the diagnostic accumulator adds again on subsequent triggered sweeps;
do not decode arbitrary later accumulated values as an independent bitmask.
Exact pending-TC request lifetime and the resource/candidate admission sequence
remain to be reconstructed before altering placement ownership protections.

Next: isolate first pending-TC requests and their terminal state; evaluate each
failed mining shoreline candidate using existing geometry evidence. Protect
Yellow's demonstrated placement attempt. Acceptance requires autonomous landing,
exact completed dropsite and sustained gathering/deposit, not merely loading.

## 2. Idle armies / few assaults — INVESTIGATING

This is not universally absent admission:

- Blue: 21 rendezvous-start and21 board-ready event records;12 slot handoff
  events0;14 unload-to-combat events8;71 new combat-target events13.
  These are event counts, NOT14 proven distinct successful invasions.
- Yellow:9 rendezvous-start/9 board-ready records, but no slot handoff event0.
  Explicit loading aborts include64:52 (terminal value0),69:27 (value1).
- Gray:8 start/5 ready records; other players no corresponding RAW3 records.
- Blue planner repeatedly reports38 (shore water unreachable),21 (topology),
  then26 (no alternative enemy). Yellow also reports11 (screening family),
 41 (no land egress),21 and26. These need candidate-level physical verification;
  they do not prove the whole enemy coastline impossible.
- Yellow expedition snapshots grow from45 soldiers59:07 to123 at85:07. The
  safety exception alternates among allowed0, quiet-period4 and no-seed-enemy5;
  at sampled transitions all three slots remain0. Blue has119 soldiers62:03,
  with exception allowed and preparation at rendezvous66.

No reserve/timer/slot expansion implemented: preparation/planning is demonstrably
active and fails before Yellow hands off a mission. Next reconstruct exact
passenger/hull commands and candidate geometry per terminal, not broaden policy.

## 3. Reactive Skirmishers — source repair, FIXED-PENDING-RUNTIME

All four first-team MAKE inventories lack Skirmisher7/Elite6 and mounted
2465–2468 requests. Gray requests7; Purple requests2465 and2467. This supports
the reported asymmetry without proving every request completed.

Concrete source fault in both common production files: reactive rules use
`players-unit-type-count any-enemy archery-class/cavalry-archer-class >= 3`.
Cached AIRef `cPlayersUnitTypeCount.description` explicitly disallows counting
enemy classes. The old strategy validator required these invalid expressions.

Repair: `rawai-reactive-ranged-threat.per`, generated by
`tools/generate_ranged_threat.py`, performs a five-second read-only census.
Each living hostile player/class is independently searched up to3; there is no
pooling of allies, separate players or separate classes. No cheating cc facts.
Restore focus and clear search afterward; private contiguous search outputs
avoid gameplay totals. Four production rules consume its Boolean.

Boundary intentionally differs from the broken fact: remote unit search finds
recently sighted enemies (AIRef says within5seconds), not a five-minute stale
explored-object count. Threat expires on next census. Existing age,5% cap,
food>150, escrow and actual trainability/train rules are unchanged. Ordinary
focus composition and unique-unit production remain unchanged. DAT availability,
producer contention and resource starvation may still suppress individual civs;
this repair is not a claim that all production gates now pass in game.

Tests: five executable PER-fixture tests cover both classes, threshold, allies,
non-pooling, refresh, focus restoration, private output layout, no orders and
unchanged production limits. PER and strategy validation pass. Full-suite result
is recorded in HANDOFF. Two stale T55 marker assertions updated to installedT56;
no runtime marker change. Runtime acceptance requires observed ranged threat ->
bounded Skirmisher requests/completion without draining normal production.

## 4. Boarding Ctrl experiment — NOT a flood resolution

79 captured issuance records across players1/2/3/4/7;11 delayed representative
observations, four showing garrisoned1. These are samples, not all actors.
17,429 native order706 packets persist (multi-actor packets can affect multiple
workers). Yellow34730 has Ctrl2 writer20 observation36:58 and a706 stream from
37:19; Green34564 is observed approaching hull40020 with Ctrl2 at60:21 and its
large706 episode starts60:28. The wrapper therefore does not universally remove
the symptom. Carry can remain nonzero and boarding can still occur. Native
producer attribution remains open; do not change other command families based
on this correlation alone. Existing experiment left unchanged.

## Scope / next work

Only reactive threat detection and its validation were repaired. Migration,
assault, modifier experiment and runtime installation were left unchanged.
Transport investigation is incomplete, with explicit next boundaries above;
none of those gameplay defects is CLOSED by this report.
