# T25 replay review and causal fixes

Replay: `SP Replay v101.103.48987.0 @2026.09.01 141200.aoe2record`

SHA-256: `075741E0A60BFA02CCD089B37960A4F1988C1B617334CAAC461783405D6B6B85`

Runtime: `RAWAI-P3B44T24:472` from players 2 through 8. Duration 95:05,
zero action-stream parse errors; Red resigns at 95:05. The replay and parsed
payload remain outside this repository.

## Broad transport audit

The all-player command audit reconstructs 39 Transport hulls, 596 garrison
orders, 216 unload orders and 11 terminal load-only phases. These are semantic
command lifecycles rather than proof that every garrison or unload completed.

| Player | Hulls | Load orders | Unloads | Terminal load-only |
|---|---:|---:|---:|---:|
| Red | 8 | 161 | 64 | 3 |
| Green | 3 | 53 | 0 | 3 |
| Yellow | 3 | 27 | 5 | 2 |
| Purple | 2 | 13 | 12 | 0 |
| Orange | 5 | 101 | 33 | 0 |
| Cyan | 8 | 61 | 14 | 3 |
| Blue | 5 | 128 | 73 | 0 |
| Gray | 5 | 52 | 15 | 0 |

T24 emits 60 migration-rendezvous phase-3 starts, no phase-4 rendezvous timeout,
17 full departures, three useful partial departures and seven local empty
aborts. The old fixed thirty-second timer no longer aborts remote travel before
local boarding. T24's rendezvous defect is therefore runtime-confirmed; later
loaded-hull and colony failures are separate defects.

## Source/runtime-proven defects

### Remote migration drop sites

Red completes two worker landings: twenty settlers at about 60:17 and ten at
about 76:03. Both report a live lumber cluster, wait for Lumber Camp resources,
then report drop-site failure after sixty seconds without a concrete foundation.
The placement state checks spendable affordability while building escrow commonly
holds enough wood. Remote choppers cannot deposit the wood that would satisfy the
same check without the missing camp. The landing transition also discarded the
resource which justified the voyage and selected a new nearest anchor.

T25 first exact-ID/class/zone revalidates the original resource anchor. If the
matching Camp/Mill is affordable with escrow, it releases wood escrow before the
ordinary exact-point foundation rule. Stale-anchor fallback remains available
only when the original resource is genuinely gone.

Status: **FIXED-PENDING-RUNTIME**. Acceptance requires an actual Camp/Mill
foundation near the preserved remote resource, followed by construction and
resource work, including a case where spendable wood is initially escrowed.

### Orphaned loaded Transports

Preparation recovery can clear the exact hull, passenger and route ownership
while leaving cargo aboard. When the one quarantine slot is occupied or reaches
its terminal state, no generic owner subsequently scans free idle loaded hulls.
This directly permits the user's 5/30, 7/30 and 10/30 Red Transports to remain
loaded without a mission. The on-screen `loaded transports: 0` message was also
misleading: that counter deliberately excludes idle loaded hulls and counts only
moving cargo hulls eligible for generic escort.

T25 adds an idle-state exact-hull orphan scan. It excludes moving, damaged,
grouped, under-attack and most-recently-terminal hulls, then adopts one into the
existing bounded quarantine unload lifecycle. A terminal hull gets one grace
interval before the scarce slot rotates. The telemetry label now says
`active loaded escort targets` and does not change behavior.

Status: **FIXED-PENDING-RUNTIME**. Acceptance requires every free idle orphaned
loaded hull to enter bounded unload/recovery or be rejected for a recorded
ownership/safety condition; active missions must not be stolen.

### Landed assaults stop after destroying one target

The landed controller searches every sixteen seconds. Four no-target samples
released the group after about one minute even though its total combat lease is
five minutes. Red's second successful landing reports no subsequent combat
target and releases roughly eighty-eight seconds after landing, matching the
user's group standing around the destroyed objective.

T25 preserves visible-hostile priority and the five-minute hard lease, but uses
twelve bounded same-landmass probe points around the sealed objective before
release. Only self-owned, idle, ungarrisoned, same-zone, not-under-attack members
move; busy fighters remain untouched.

Status: **FIXED-PENDING-RUNTIME**. Acceptance requires a landed group which loses
its first target to acquire another visible target or advance through bounded
same-island probes, then release no later than the existing total lease.

## Separate unresolved evidence

- The Red naval fleet visible around 69:48 is not permanently orphaned in the
  replay. Its members receive later opportunity/combat assignments four to six
  minutes afterward. The naval-opportunity controller has no distance/progress
  watchdog, but this replay does not prove which target or controller produced
  the temporary non-progress. Status remains **INVESTIGATING**; no guessed naval
  behavior change is included.
- Several very large identical ORDER floods remain, including more than eleven
  thousand identical orders from one player/unit-target pair. This may explain
  lag but is not attributed to a source writer by this review and is not folded
  into the transport patch.
- The public migration landing planner records 17 candidate missions, seven
  clear unloads, 72 rejected candidates with no unload, and no wrong-zone unload.
  Landing safety remains intact. Productive colony construction, not landing
  screening, is the proven Red failure addressed here.

## Static validation

Focused executable fixtures pass for migration foundations, bounded loaded-hull
recovery, assault preparation and landed combat. Full release validation and
deployment identity are recorded in `HANDOFF.md`; engine acceptance of T25 is
still required.
