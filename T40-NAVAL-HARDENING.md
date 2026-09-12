# T40 naval / overseas hardening — deployed, runtime validation pending

Canonical checkout: `G:\Projects\Codex\Rome at War AI\.trade-work\T30-trade-cap-civ-fix`,
branch `fix/trade-cog-cap-dacian`, baseline `4d9c519` (T39). Source marker
`RAWAI-P3B44T40:488`. Deployed after explicit user authorization on 2026-09-05.
The latest explicit user instruction supersedes the obsolete `.pr-work` path
in the general project rules. No branch or worktree was created.
Repository-local `AGENTS.md` now records that explicit canonical-workspace change.

## Shipyards — FIXED-PENDING-RUNTIME

**Evidence / boundary.** User reports late/missing yards and congested inlets.
The original 155-line `rawai-specialplacement.per` bypassed tech saving only
for the first yard. Its final build gate also required `total < desired`, so
the apparent first-yard priority could not actually issue when the current
civilization phase still requested zero yards. Later yards had no persistent
minimum-capacity escape from `wait-techup-requirements`. Placement randomly
offset the newest naval building by roughly 14 tiles, checked buildability and
7-tile building clearance, then reset to IDLE on `up-build-line` issuance.
There was no water-exit test or concrete-foundation/completion check.

**Change.** Preserve early-age/Port/250-wood first-yard admission, including its
intended one-yard exception to a zero phase target. A 90-game-second deficit
below `min(desired, 2)` can bypass only tech saving, never affordability or
escrow. Later expansion retains ordinary saving policy. Lake 4 / Rivers 6 caps
and all civilization phase targets remain unchanged. No escrow is released.
Twenty-four deterministic coastal offsets extend to 40 tiles, with rotating
naval anchors and four exit orientations. Each accepted orientation requires
four open exact-path water points in the real nearby ship's water zone, ten
tiles from existing own/allied naval buildings, plus a free nearby worker with a bounded
vicinity path. Queries use mobile ships/workers, never buildings. Four failed
sectors expire after 180 seconds. A build remains pending for 24 seconds until
the actual own Shipyard object appears within two tiles, then is watched for
completion for at most 180 seconds. Failure is not counted as completion.
One rate-limited reason transition (diagnostic ID 410) distinguishes cost,
pending placement, foundation loss, worker hold, tech hold and coastline failure.

**Authority.** Cached AIRef `airef-reference-20260830.js`: `up-path-distance`
option 1 requires an open exact tile; option 0 allows vicinity. Point pairs are
bounded without substituting a clipped point. `up-build-line` is an issuance,
not a guarantee that a foundation exists. Native `up-assign-builders shipyard 4`
is preserved; the eligible worker path is admission evidence, not a promise
that the native engine assigns that particular worker. No worker is stolen
from a protected DUC group and no global task/reset/percentage is changed.

**Validation.** PASS: 11 executable-PER fixtures and the full validation below.
Tests cover high-priority first yard, persistent second yard, later saving/caps,
no false foundation success, four-probe crevices, building separation, missing
or owned/unreachable worker, and finite distributed candidate enumeration.

**Runtime acceptance / uncertainty.** Still required: first yard completion,
minimum operational count despite prolonged tech saving, actual open exits and
adequate sector coverage on Iberia and islands, ordinary expansion restraint,
native worker assignment/completion, pending-queue behavior and no regression in
transport/fishing/Port traffic. Four sampled open points are a bounded quality
heuristic, not a proof of a wide corridor everywhere. Rejected candidates/no
nearby probing ship may still delay placement; the reason remains observable.
Pending/ready queries explicitly reset the same-type search cursor while
preserving accumulated results, so changing the status filter cannot reuse an
exhausted Shipyard index and miss the other status.

## Merchant right-of-way — FIXED-PENDING-RUNTIME

**Source boundary.** Legacy berth clearing requires idle ships around a producer;
the three-slot clearance also requires idle blockers, a waypoint leg and a hull
within 20 tiles of origin. Active traders blocking a mid-route strait cannot
qualify. This is a demonstrated coverage gap, not a claim that every abort is
caused by merchant congestion.

**Change.** Independent observer, no mission redesign: loaded/reserved moving
Transports before moving mission-owned warships. Intent, endpoint and physical
position are sampled every eight seconds. Two stationary samples, stable intent
and at least six tiles still to travel are required. One nearby self-owned,
ungrouped merchant (active trading included) is sent to a lateral point only
after its exact path, water zone, bounds and nearby enemy defense are checked.
The priority hull is never ordered. Three merchant records hold for at most
32 seconds with up to three bounded renewals against native reacquisition;
one sideways command per sweep, 120-second per-merchant cooldown. Up to three
different merchants can clear a saturated choke, with a fresh hull measurement
between them. Four non-evicting hull cooldown records prevent immediate repeats
for 180 seconds. Progress/intent change releases early; original valid allied
Dock targets resume once, and already-trading merchants are left alone. No STOP,
native economy SN change, permanent group ownership or timer extension exists.
Legacy clearance writers pause while this temporary clearance lease is active.

**Validation.** PASS: 11 executable-PER fixtures, including five active merchants
in a choke, three sequential interventions, no-progress/intent gates, moving
warship vs firing ship, native reacquisition bound, ownership loss, hostile Dock,
same-zone/exact path/danger checks and restored trade. Existing assault history
fingerprints normalize only the three added legacy-clearance interlocks, not
the rest of the immutable voyage baseline.

**Runtime acceptance / uncertainty.** Fresh replay must show stalled priority
hulls resume through Gibraltar, active merchants remain aside long enough,
trade resumes, and unrelated merchants remain untouched. This observer cannot
prove physical causality from proximity, and intentionally does not move units
with no valid movement intent or within the six-tile near-endpoint margin.
Native trade may reacquire between bounded samples; the fixture exercises that
case but engine proof is still required. Owned merchants are never commandeered.

**Adversarial follow-up.** The holding-point check initially omitted the
Town Center and concrete Sea Tower checks used by the existing assault danger
validator. Those are now included, with hostile-point fixtures for both. The
coastal fixture now enforces the documented 240-local/40-remote list limits and
ready-vs-pending search semantics instead of allowing unlimited synthetic lists.

## Expedition throughput — FIXED-PENDING-RUNTIME

**Source cause / boundary.** The three slots already release preparation one
second after dispatch. Empty-slot admission separately protects migration,
relic, recovery, repair, home defense, hull availability, target seed and timer
ownership. Those guards remain. The first fresh-manifest rule nevertheless
requires aggregate land superiority >= TOLERABLE, computed from team/enemy land
strength, even when a safe island has surplus idle soldiers. Loaded intake does
not have that additional gate. This is a source-visible utilization boundary,
not proof that it explains every player in a replay. Type-wide native attack
exclusions and the shared preparation lane remain separate potential blockers.

**Change.** Only that fresh-admission condition gains a safety/reserve exception.
A 30-second read-only census uses a real home worker for up to four cross-zone
path queries per living enemy; all candidates returned in the bounded remote
search are first checked for the conservative home-zone veto. A stale census
expires after 35 seconds. Initial/home-attack/near-coast naval threat requires
180 quiet game seconds. Existing verified-home-threat flags veto immediately.
The exception also requires an existing viable enemy seed, a Transport, two
warships and naval superiority >= TOLERABLE. No new target, beach or mission is
invented and no dispatched hull is recalled by this module.

Every actual manifest separately counts eligible free, idle, ungarrisoned,
unthreatened home troops by class (up to the documented 240 local search results
per class). It retains at least 12 or one quarter of that census at EQUAL or
better sea control. At merely TOLERABLE sea control it retains at least 20 or
half, and caps the lift at five. Existing useful-partial admission still applies;
fewer than five surplus troops cannot produce an accepted assault. One eligible
siege engine is retained; existing Palintonon exclusions also remain. Already
owned, busy and overseas soldiers are not treated as free home reserves.
Ordinary admission remains available when the exception is off. Thresholds are
explicit requested policy tuning, not engine constants or replay-proven optima.

**Reinforcement / preserved behavior.** Freed slots use the existing one-second
preparation reuse, persistent preferred enemy, failure rotation and fresh
shore/screen/danger validation. There is no cached successful beach that bypasses
those checks, no fourth slot and no broadened commandeering of busy troops.
Migration/relic sharing, useful partials and sealed mission records are unchanged.
Diagnostic ID 430 reports rate-limited exception eligibility transitions only.

**Focused validation PASS:** 11 executable-PER/integrated fixtures cover the
inferior-land-strength admission difference, quiet dwell and immediate threat
veto, reachable enemies across engine zones, the fifth home-zone candidate,
expired census, missing workers/hulls, naval inferiority/pressure, large-army
reserve accounting, mixed/siege manifests, protected passengers, three-slot
independence/reuse and unchanged failed-shore planning.

**Runtime acceptance / unresolved boundary.** Demonstrate repeated AI-owned
surplus lifts from a safe isolated home, all three slots used/reused when demand
and ships permit, useful reserves left home, no threatened-home drain, continued
migration/relic participation and no dangerous-route bypass. Searches remain
visibility-limited and bounded: remote lists hold at most 40 objects and four
cross-zone probes do not establish complete map connectivity. A missing worker
or no suitable known objective closes this exception. The source gate is fixed;
three-slot productive saturation and the share of real idleness attributable to
other ownership/preparation gates remain unproven until a fresh replay.

## Files and independent commits

| Item | Runtime/generator files | Focused tests | Commits |
|---|---|---|---|
| Shipyard capacity/coast/foundation | `rawai-specialplacement.per`, `rawai-shipyard-defs.per`, `tools/generate_shipyard_placement.py` | `tools/test_shipyard_coast.py` (11) | `f8df20d`, cursor correction `ac8b606`, allied clearance `2c46488` |
| Merchant right-of-way | `rawai-naval-right-of-way.per`, `rawai-naval-row-defs.per`, `tools/generate_naval_right_of_way.py`; legacy interlocks in `rawai-military.per`, `rawai-assault-missions.per`, `tools/generate_assault_missions.py` | `tools/test_naval_right_of_way.py` (11), historical assault fingerprints in `tools/test_assault_cancellation_details.py` | `9c0b3fe`, defense coverage `e4ad548` |
| Expedition exception/reserve | `rawai-expedition-admission.per`, `rawai-expedition-budget.per`, `rawai-expedition-defs.per`, `tools/generate_expedition_admission.py`, admission/manifest integration in `rawai-military.per` | `tools/test_expedition_admission.py` (11) | `3110251` |

Shared infrastructure: `AI RAW.per` loads the modules, `rawai-init-goals.per`
labels the source, `tools/per_coastal_fixture.py` executes actual generated PER
with supplied geometry, and `tools/audit_ownership_source.py --write` regenerates
the large mechanical inventory while refusing permission failures. Runtime marker
assertions in `tools/test_trade_topology.py` and `tools/test_validators.py` were
updated only for T40. No civilization composition or data-mod payload changed.

## Final validation and review

- **PASS:** 503/503 full Python 3.12 repository tests, including 33 new focused
  tests, migration/relic coverage, siege boarding, trade topology, ownership,
  shoreline, landed combat and historical three-slot fingerprints. The sandbox
  first denied the compiler fixture's temporary directory; the permissioned
  rerun passed. Latest complete run: 44.201 seconds.
- **PASS:** PER structural/operand validation; ownership audit (960 relevant
  sites / zero direct permission failures); generated ownership, assault mission,
  assault plan, migration shoreline, coastal, ROW, expedition and naval-source
  synchronization; strategy execution (1,156 matchups), naval doctrine (34 civs),
  all 42 existing replay benchmark definitions and `git diff --check`.
- **NOT PASS / pre-existing:** `sync_civ_strategies.py` still proposes six
  existing-file updates. A write-intercepted in-memory preview proves that four
  are line-ending-only, while Dacian quaternary Bowmen and Syracusan Spearman
  choices/training would be removed or replaced. None of these files, their
  strategy JSONs or the generator changed from `4d9c519`. The prior handoff
  already records the conflict with audited release-aligned production. Do not
  run `--write` against real files until that source-data alignment is repaired
  in its own scoped change; do not silently undo those working choices.
- **Adversarial review, ACCEPTED and tested:** same-type foundation status cursor;
  allied naval-building clearance; Town Center/Sea Tower holding danger; native
  search-list capacities; large-army census truncation; fifth home-zone enemy
  omitted by a four-path-query limit. All accepted findings were implemented.
- **REJECTED for this patch:** more than three slots, broad cadence/watchdog
  increases, busy/owned troop acquisition and unsafe-route relaxation. Existing
  one-second preparation reuse and independently owned missions already provide
  the intended pipeline; no evidence establishes slot count as its limit.
- **DEFERRED / explicit boundaries:** actual engine site acceptance/worker choice,
  sufficient width beyond sampled water points, collision causality, native trade
  reacquisition between hold samples, complete unknown/cross-zone connectivity,
  type-wide native military exclusions and shared-lane throughput. Record their
  exact events in the next replay instead of treating static fixtures as closure.

## Identity and next runtime acceptance

Source: 99 runtime files, marker **T40:488**, aggregate SHA-256
`C90F78EB90DBA119DA6DC0373B8D9B5A703B3161A0D31267A7F5504409CE22E2`.
String budget: 1,470 / 1,500 conservative all-file literals; no new timers or
DUC groups. Installed runtime is independently unchanged: 93 files, **T36:484**,
SHA-256 `4E18B8AA59FBD5FD6468242E15DE207209A259C3F8BB08D8CB71EA29BEF87857`.

Deployment used only this checkout and the read-only post-check verifies all 99
installed runtime files match source at the aggregate hash above, with no
missing, differing, or unexpected runtime files. Preserve the Iberia
Huge/400/Extreme/RaW-data-fix lobby comparison and record any intentional change.
Audit all players, not only a successful example. Each of the three sections
above has independent runtime PASS criteria. Include path-query/late-match cost,
productive repeated three-slot use, native trade resumption and the existing
T37/T38/T39 siege/land-trade/migration/landed-group fixes in that acceptance.
There is no fresh T40 runtime replay yet; **all three gameplay items remain
FIXED-PENDING-RUNTIME**, not CLOSED.
