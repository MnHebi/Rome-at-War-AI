# T40 naval / overseas hardening — source only

Canonical checkout: `G:\Projects\Codex\Rome at War AI\.trade-work\T30-trade-cap-civ-fix`,
branch `fix/trade-cog-cap-dacian`, baseline `4d9c519` (T39). No deployment.
The latest explicit user instruction supersedes the obsolete `.pr-work` path
in the general project rules. No branch or worktree was created.

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
tiles from existing naval buildings, plus a free nearby worker with a bounded
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

**Validation.** PASS: 9 executable-PER fixtures, 126 general validator tests,
PER structural validation, ownership audit (849 sites, zero permission failures).
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
