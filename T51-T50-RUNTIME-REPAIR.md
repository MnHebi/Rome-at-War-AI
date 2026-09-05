# T51 — T50 runtime repair and self-diagnosing lifecycle instrumentation

Date: 2026-09-05  
Branch: `fix/trade-cog-cap-dacian`  
PR: <https://github.com/MnHebi/Rome-at-War-AI/pull/11>  
Source marker: `RAWAI-P3B44T51:499`  
Installed marker: `RAWAI-P3B44T50:498` (unchanged; this work was not deployed)

## Scope and evidence order

T50 is the completed 69:18 Iberia replay
`SP Replay v101.103.48987.0 @2026.09.05 173048.aoe2record`, SHA-256
`1B796446E790221433F14DBF1AA65AED2246933905267B667F466DD0E083CC1C`.
The detailed pre-change evidence is in `T50-RUNTIME-REPLAY-ASSESSMENT.md`.

Instrumentation was committed first in `954c8dd`. It covers every open
lifecycle named by the task without changing ownership, timing, targeting,
pathing or economy decisions. The first behavioral commits were then made:

- `f96da71` — literal hostile gates for landed assault target acquisition;
- `d20386a` — deterministic, rotating Shipyard coastline sectors;
- `134b22f` — bounded sustained Shipyard-capacity tier.

Later commits complete diagnostics or preserve their regression guards:

- `936dbf7` — complete bounded right-of-way rejection/issuance diagnostics;
- `8471c1d` — make immutable historical fingerprints ignore diagnostics;
- `3701a5b` — complete migration outer-admission and preloaded-adoption
  diagnostics.

No migration, merchant-yield or expeditionary behavior was changed without
runtime attribution. T37 individual siege boarding remains protected and was
not redesigned.

## 1. Landed assault continuation

**Status: ROOT-CAUSE-PROVEN / FIXED-PENDING-RUNTIME.**

### Cause and correction

T50 proves that transport formation, voyage, shoreline resolution and landing
are not the first failure: Blue reaches event 8 five times and Yellow three
times. No mission then emits event 13, a landed target, or an issuance sample;
seven leases later expire at event 12.

The earliest source-visible divergence was the first post-landing hostile gate.
The landed selector used the mutable `focus-player` goal in `player-in-game`,
`stance-toward` and the remote-owner filter. That runtime player expression did
not yield a usable target after event 8. The correction generates literal
player gates for Players 1–8, first preferring the mission's sealed enemy and
then another live hostile. Same-zone, dead-player and failed-target filtering
remain. Transport formation, shoreline geometry, voyage watchdogs and landing
were not changed.

### Diagnostic map

Each assault slot owns an independent budget of 24 lifecycle samples and four
terminal samples. Budgets are initialized once and never replenished.

| Event/reason | Meaning | Emission boundary | Maximum frequency |
|---|---|---|---|
| 500–505 | slot, raw group count, owned count, usable count, sealed enemy, target zone | landed group reconstruction/search entry | 24 per slot for the whole match |
| 506–510 | slot, owned count, representative actor, current action, current target | post-command persistence sample | within the same 24-per-slot budget |
| 511–516 | slot, literal candidate player, raw/owner/live/same-zone search counts | each bounded literal hostile candidate search | within the same 24-per-slot budget |
| 517, 520–523 | writer slot, selected target, combat tries, target owner/type | immediately before the actual `up-target-objects` writer | within the same 24-per-slot budget |
| 518/519=1 | terminal slot / group empty or disappeared | landed lease termination | four per slot for the whole match |
| 518/519=2 | terminal slot / lease expired while still reconstructable | landed lease expiration | four per slot for the whole match |

### Runtime acceptance

A fresh marker-499 replay must show event 8 followed by a non-empty literal
candidate search, a writer fingerprint, and a persistent combat action for each
used slot. A living group must not expire idle while a valid same-zone hostile
target exists. Dead/invalid enemy rotation and all three independent slots must
remain functional.

## 2. Shipyard admission, capacity and coast selection

**Placement status: ROOT-CAUSE-PROVEN / FIXED-PENDING-RUNTIME.**  
**Capacity status: source-supported bounded policy change / FIXED-PENDING-RUNTIME.**

### Cause and correction

T50 issues 15 Shipyard orders across seven players, yet Green owns two Ports
and issues none; reason 64 (exact candidate unbuildable) dominates. Source
candidate discovery was still an anchor plus blind XY sampling, so validation
spent most of its budget rejecting land/water points near already congested
infrastructure. This also repeatedly sampled the same narrow sector.

Candidate discovery now rotates through four deterministic sectors around each
rotating ready Port/Shipyard anchor, with eight dense candidates per sector and
a hard eight-attempt placement lane. A successful or exhausted sector rotates.
Every candidate still must pass exact buildability, own/allied separation,
mobile-water same-zone verification, the W1–W6 open-water aperture, worker
ownership/reachability, failed-site memory and concrete foundation verification.
A synthetic open coast wins over a Gibraltar-like narrow throat. The bounded
implementation does not claim to be a global coastline graph; an open coast
outside every anchor search radius remains a runtime/architecture boundary.

The previous protected capacity ended at `min(desired, 2)`. The new tiers are:

1. 0 → 1: bootstrap-critical;
2. 1 → `min(desired, 2)`: after a 90-second persistent deficit, protected
   minimum capacity;
3. minimum → `min(desired, 4)`: after a 180-second persistent deficit, only
   with more than 600 wood and ordinary affordability/build/worker checks;
4. sustained → full desired: unchanged ordinary `wait-techup-requirements`
   expansion discipline.

No global tech-up saving or escrow discipline is disabled.

### Diagnostic map

The lifecycle observer has a finite 24-sample match budget; reason reports are
transition-latched and have a 60-second cooldown.

| Event/reason | Meaning | Emission boundary | Maximum frequency |
|---|---|---|---|
| 524–529, 543 | age, desired, minimum, completed, completed+pending, pending, sustained tier | deficit lifecycle snapshot | 24 for the whole match |
| 530–535, 544 | Port count, wait-tech state, worker hold, affordability, can-build, current reason, sustained deadline | deficit blocker snapshot | within the same 24-sample budget |
| 536–540 | selected build XY, anchor, worker and candidate attempt | immediately before build issuance | within the same 24-sample budget |
| 541/542=1 | concrete foundation ID / foundation observed | bounded post-issuance verification | within the same 24-sample budget |
| 541/542=2 | building ID / Shipyard completed | completion observation | within the same 24-sample budget |
| 410 + reason | transition-latched admission/geometry/foundation reason | reason change, no sooner than 60 seconds | finite transitions separated by 60 seconds |

### Runtime acceptance

Marker 499 must show viable naval players recovering from zero/one Shipyard,
progressing toward the sustained tier only when its resource gates hold, and
verifying real foundations/completions. Accepted sites should prefer open coast
and avoid narrow throats when a viable sector exists. Low counts must now have
a concrete diagnostic reason rather than being inferred from source.

## 3. Migration STOP flood and automatic migration

**Status: INVESTIGATING. No behavioral fix.**

T50 contains 8,912 continuous STOP-706 packets to Yellow settlers 32825 and
33303 over about 120 seconds immediately after landing. The replay cannot name
the writer. Instrumentation now fingerprints every plausible explicit migration
STOP, boarding, movement, unloading, drop-site, retask, release and recovery
writer. If none executes at the packet cadence, the next replay can positively
implicate native task expansion rather than another uninstrumented RAW writer.

The outer admission observer also distinguishes relic/recovery/repair/route/
clearance/colony holds, Transport availability, enemy seed and the deliberate
one-pass yield to a fully viable assault. It separately records adoption of a
manually preloaded/quarantined hull. No timer, ownership or admission fact is
changed by these observers.

### Diagnostic map

Migration has a 40-sample state/admission budget and a separate 24-sample
writer budget, each initialized once and never replenished.

| Event/reason | Meaning | Emission boundary | Maximum frequency |
|---|---|---|---|
| 550–555 | state, mission, hull, target manifest, observed load, time | migration state transition | 40 for the whole match |
| 556–559 | admission entered, home-defense state, route state, seeded enemy | successful admission boundary | within the same 40-sample budget |
| 568 bitmask | admission rejection: 1 relic, 2 recovery, 4 repair, 8 route, 16 clearance, 32 colony TC, 64 TC pending, 128 TC placement pending, 256 yielded to fully viable assault | one snapshot per newly triggered migration desire | within the same 40-sample budget |
| 569–578 | exact admission state values, Transport count and assault-admission state | paired with 568 | within the same 40-sample budget |
| 560 + 5–13 | explicit STOP writers: partial shore, one-passenger abort, empty abort, lost transport, stale landed scout, wrong-zone scout, missing landing hull, uncovered timeout, Imperial scout retirement | immediately before the explicit STOP | 24 total writer samples |
| 560 + 20–25 | rendezvous, mining/scout boarding, first/subsequent renewal, unload | immediately before command issuance | within the same 24-writer budget |
| 560 + 26–32 | builder assignment, retask, release, failed-drop-site recall, Mining/Lumber/Mill build | immediately before command issuance | within the same 24-writer budget |
| 560 + 33 | preloaded/quarantine Transport adoption, with hull and garrison count | separate adoption path entry | within the same 24-writer budget |
| 561–567 | actor, group/count, hull, action, target, state, event/context | values attached to writer 560 | no independent emission |

### Runtime acceptance

For the STOP episode, correlate actor IDs and packet cadence with writer code
5–13 or demonstrate that no instrumented writer executes at that cadence. For
automatic migration, classify the first divergence as A admission, B settler
eligibility, C boarding, D accepted-load recognition, or E preloaded adoption;
then show autonomous hull selection, manifest, boarding/load growth, accepted
cargo, departure and landing. Code 33 must distinguish manual/preloaded
adoption from the normal path.

## 4. Naval merchant right-of-way

**Status: INVESTIGATING. No eligibility broadening or movement-policy change.**

T50 records substantial Merchant Ship activity but zero paired 420/421 yield
events. Current evidence cannot distinguish an ineligible military action from
a progressing hull, absent local merchant, rejected merchant or failed holding
point. The diagnostic boundary now records all of them, including the exact
pre-command fingerprint. Existing policy remains one merchant at a time, safe
same-water holding point, no STOP, cooldown and progress remeasurement.

### Diagnostic map

The ROW observer has a single match budget of 32 diagnostic samples.

| Event/reason | Meaning | Emission boundary | Maximum frequency |
|---|---|---|---|
| 580–585 | accepted priority kind, hull, action, group, raw candidate count, eligible count | accepted priority candidate | 32 for the whole match |
| 586–590 | movement, turn, distance and stall evidence | priority-hull progress sample | within the same 32-sample budget |
| 591–596 | merchant raw, eligible, owned/free, safe/not-attacked and same-zone counts | local merchant filtering | within the same 32-sample budget |
| 617–624 | rejected priority kind/hull/action/group/destination, rejection bitmask and count | sampled candidate rejection | within the same 32-sample budget |
| 625–630 | hull, merchant, attempted side/XY, holding rejection reason 1 zone, 2 bounds, 3 missing merchant, 4 path, 5 hostile | failed hold-point validation | within the same 32-sample budget |
| 631–637 | exact hull/merchant/record/hold XY/stalls/tries | immediately before yield movement | within the same 32-sample budget |
| 420/421 | existing actual merchant-yield pair | command issued | existing bounded controller policy |

### Runtime acceptance

The next replay must show whether candidates fail before eligibility, stall
proof, merchant filtering, holding validation or issuance. If 631–637 and
420/421 occur, priority-hull progress must improve before another merchant is
moved, and native trade must resume afterward. Eligibility will be broadened
only if runtime identifies a missed action class.

## 5. Expeditionary commitment

**Status: INVESTIGATING. No throughput tuning.**

The existing bounded expeditionary controller is now observable. T50 cannot
explain why players other than Blue and Yellow generated no assault events,
and the landed-combat failure may itself have occupied or expired slots. It
would be unsafe to compensate by exporting more of the home army before the
landed fix is tested.

### Diagnostic map

The observer has a 24-sample match budget and a 60-second report interval.

| Event/reason | Meaning | Emission boundary | Maximum frequency |
|---|---|---|---|
| 600–612 | stage/blocker, total soldiers, worker, home landblock, naval pressure, safe-after, enemy, superiority, three slot states, route state | expedition admission snapshot | 24 for the whole match, at least 60 seconds apart |
| 613–616 | eligible census, free surplus, protected reserve, manifest limit | budget/manifest snapshot | within the same 24-sample budget |

### Runtime acceptance

After landed combat works, classify each inactive player as slot-saturated,
admission/cooldown blocked, hull-starved, troop-starved, reserve-limited or
naval-risk suppressed. A safe isolated home with viable enemy and real surplus
should repeatedly reuse the existing three slots without draining its adaptive
reserve. No fourth slot is added.

## Preserved behavior and regression boundary

- T34 route/path and shoreline validation remains unchanged.
- T35 Villager-garrison policy remains unchanged.
- T37 siege engines continue individual one-per-second boarding; obstructed
  engines cannot block reachable siege passengers, boarded members are not
  retasked, and retries remain bounded.
- Three assault slots, useful-partial manifests, sealed mission ownership,
  failed-coast memory, migration/relic separation and naval safety gates remain.
- Land trade remains **RUNTIME-PASS** from T50 and is unchanged.
- Current naval cooperation and native trade resumption contracts remain.

## Files changed

Runtime/generated sources:

- `rawai-assault-admission.per`, `rawai-assault-mission-defs.per`,
  `rawai-assault-missions.per`;
- `rawai-shipyard-defs.per`, `rawai-specialplacement.per`;
- `rawai-naval-row-defs.per`, `rawai-naval-right-of-way.per`;
- `rawai-expedition-defs.per`, `rawai-expedition-admission.per`,
  `rawai-expedition-budget.per`;
- `rawai-customconstants.per`, `rawai-military.per`,
  `rawai-exploration-policy.per`, `rawai-init-goals.per`.

Authoritative generators and tests:

- `tools/generate_assault_missions.py`,
  `tools/generate_shipyard_placement.py`,
  `tools/generate_naval_right_of_way.py`,
  `tools/generate_expedition_admission.py`;
- `tools/test_t51_diagnostics.py`, `tools/test_landed_assault.py`,
  `tools/test_shipyard_coast.py`,
  `tools/test_assault_cancellation_details.py`,
  `tools/test_validators.py`, `tools/test_trade_topology.py`.

## Validation

Focused validation covers diagnostic budgets/latches/side effects/string
discipline; literal landed selectors and slot independence; Shipyard open-coast
and narrow-throat fixtures; foundation verification and capacity tiers;
migration admission/writers/adoption; ROW candidate/merchant/hold/issuance
boundaries; expedition reserve/slot diagnostics; T37 siege boarding; shoreline,
ownership, migration/relic and trade-topology non-regression.

Final validation after the marker and diagnostic extensions:

- **PASS:** full Python 3.12 discovery, 528/528 tests;
- **PASS:** PER structure/operand validation;
- **PASS:** generated-source synchronization (included in the T51 tests);
- **PASS:** naval doctrine, 34 scores plus role/cap/ownership checks;
- **PASS:** strategy execution, 1,149 historical and 1,152 Extreme adjusted
  matchups across 1,156 total;
- **PASS:** ownership audit, 1,028 relevant sites and zero direct permission
  failures;
- **PASS:** 42 replay benchmark metadata records;
- **PASS:** good-units workbook round trip, 34 civilizations, 680 unit-evidence
  rows and 340 naval-class rows;
- **PASS:** `git diff --check` before the documentation commit.

One known unrelated validator boundary is retained deliberately:
`tools/validate_good_units.py` reports the pre-existing frozen provenance
mismatch for `source_provenance/AI RAW.per_sha256`; the historical artifact is
not silently rebaselined by this runtime-controller task.

## Remaining evidence boundary

No runtime-sensitive behavior in this report is called closed. Marker 499 needs
a fresh replay to accept landed combat, Shipyard placement/timeliness/capacity,
migration STOP attribution, automatic migration, merchant yielding and
expeditionary utilization. The installed test environment remains at marker
498 because deployment was expressly withheld.
