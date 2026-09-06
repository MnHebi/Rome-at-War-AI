# T51 runtime replay assessment

## Scope and identity

This is a replay-only assessment. It makes no gameplay, generated-source or
deployment change.

Replay:
`SP Replay v101.103.48987.0 @2026.09.06 131504.aoe2record`

- SHA-256: `5AB54B6F92B686842BABBE454049B278A1FA709FF631EC66AF4C0C425927A7EC`;
- duration: 71:33;
- game build: `101.103.48987.0`;
- map: Iberia (RMS id 49), 400 population, speed 1.69, Extreme, no treaty,
  shared exploration;
- parser result: complete stream, 375,007 decoded commands and zero decoder
  failures;
- runtime attribution: the startup marker is not present in the captured chat
  stream, but T51-only diagnostic ids 500 and above are present. Before this
  match the installed/source payload was independently verified byte-identical
  at marker `RAWAI-P3B44T51:499` and aggregate SHA-256
  `DB736F6EED6D526A4B9907A82D152C9977235BD9A1844B4479336EDBC7DA2B65`.
  This is strong T51 attribution, with the absent visible startup marker noted
  rather than silently ignored.

Validated player mapping is Blue/Dacians, Red/Pontus, Green/Seleucids and
Yellow/Syracusans on team 2, versus Cyan/Nubians, Purple/Numidians,
Gray/Carthaginians and Orange/Egyptians on team 3. Player 1 resigns at 71:33 to
end the recording; the resignation does not establish an ordinary match result.

## Result summary

- **Landed assault target acquisition and command issuance: runtime PASS.**
  Cyan and Gray reach landed handoff, select only literal live-hostile owners,
  issue the instrumented `up-target-objects` command, change targets and retain
  their groups until the groups disappear. All three independent slots are
  exercised by Cyan. No reconstructable group merely expires at its combat
  lease.
- **Shipyards: severe runtime regression.** Only one Shipyard build order
  appears in 71:33, from Yellow at 21:04. T50 produced 15 orders across seven
  players. The regression boundary is the T51 deterministic sector sampler in
  `d20386a`; its one-sector/eight-point admission is substantially narrower
  than the T50 runtime-proven full near-anchor domain. The later capacity commit
  cannot explain failure to leave zero Shipyards.
- **Land trade: runtime PASS preserved.** Seven players produce 35-81 Trade
  Carts and Orange produces one Cart plus four Merchant Ships. Every land-trade
  player except Orange exceeds the three-Cart proof ceiling.
- **Automatic migration: materially improved/runtime-supported.** Twelve
  path-clear migration landings are reconstructed for Purple, Gray and Red;
  every one has a same-second unload and none is a wrong-zone/path-rejected
  candidate. No preloaded/quarantine-adoption writer is observed.
- **Assault preparation remains inefficient.** Cyan lands four missions and
  Gray three, but Gray also cycles through eight abort/partial preparation
  outcomes. Yellow readies one hull without committing before replay end.
- **STOP/order-706 flood remains OPEN.** There are 21,431 decoded order-706
  packets and 60,977 actor incidences, dominated by Gray migration Villagers.
  The explicit partial-load STOP at 36:56 addresses five different shore
  leftovers, while order 706 floods twelve other manifest Villagers. Several
  flooded long before migration reservation. The T51 writer budget expires on
  routine boarding renewals and does not attribute the flood.
- **Right-of-way and several lifecycle diagnostics fail their own runtime
  acceptance.** Their finite budgets are consumed at startup or before the
  relevant late-game behavior, so absence of a later sample is not evidence
  that no event occurred.

## Shipyard regression

Only one Shipyard construction order exists in the complete command stream:

| Player | Shipyard build orders | Port build orders |
| --- | ---: | ---: |
| Blue | 0 | 5 |
| Red | 0 | 10 |
| Green | 0 | 3 |
| Yellow | 1 at 21:04, `(133.5,155.5)` | 2 |
| Cyan | 0 | 6 |
| Purple | 0 | 5 |
| Gray | 0 | 9 |
| Orange | 0 | 3 |

This is not a small throughput miss. T50 produced 15 Shipyard orders across
seven players, including 14 before 60:00. T51 produces one and leaves seven
players at zero despite 43 Port orders proving widespread coastal
infrastructure and demand context.

No foundation/completion lifecycle events 536-542 occur. The finite lifecycle
budgets expire before later Imperial/high-capacity behavior:

- Blue samples 04:00-21:00;
- Red, Green and Yellow sample approximately 01:00-21:00;
- Cyan, Purple, Gray and Orange generally exhaust their samples by about 19:00.

Blue is representative: completed, completed-plus-pending and pending remain
zero in every snapshot; Port count is one; desired/minimum reaches two;
`can-build` remains zero; affordability is true in only one sample. The current
reason remains zero, so the observer does not expose the actual blocker after
its early budget is gone. Diagnostic acceptance therefore fails even though
the runtime regression itself is unambiguous.

The first causal revision boundary is `d20386a`, not the later sustained
capacity tier in `134b22f`. `d20386a` changed
`tools/generate_shipyard_placement.py` and generated
`rawai-specialplacement.per` from T50's random full `[-14,+14]` coordinate
domain to four global cardinal sectors. A placement lane tests only one sector
of eight fixed offsets, all 8-14 tiles from its Port/Shipyard anchor, before
rotating the sector after exhaustion or success. For example, the east sector
is:

```text
(12,0), (10,4), (10,-4), (14,4), (14,-4), (8,7), (8,-7), (14,0)
```

The other sectors are cardinal rotations. This is not detected coastline
orientation; it is a fixed cardinal ring. It removes every near-anchor point
inside eight tiles and most arbitrary directions that T50's 29-by-29 domain
could reach. Every downstream buildability, separation, water-aperture,
worker-path and foundation gate remains present, but it cannot evaluate
positions that candidate discovery never supplies.

Runtime and source therefore localize the regression to the sampler boundary.
They do not prove which individual candidate rejected after the observer
expired. The next causal patch should restore a sufficiently dense near-anchor
search (or make sector selection follow proven water/coast orientation) while
preserving T49 admission retention, T50 aperture validation, failed-site memory
and concrete foundation verification. The sustained capacity tier should not
be removed as an attempted cure for a zero-to-one placement regression.

## Land trade and merchant right-of-way

Production totals are:

| Player | Trade Carts | Merchant Ships |
| --- | ---: | ---: |
| Blue | 81 | 0 |
| Red | 76 | 0 |
| Green | 60 | 0 |
| Yellow | 35 | 0 |
| Cyan | 61 | 0 |
| Purple | 11 | 0 |
| Gray | 65 | 0 |
| Orange | 1 | 4 |

Growth beyond three Trade Carts requires observed live `actionid-trade` under
the current contract. Land trade is therefore runtime-established for seven
players, while Orange demonstrates that independent water trade remains
available. T50's land-trade acceptance survives T51.

The right-of-way diagnostics do not assess the intended late-game scenario.
Every player spends its entire 32-sample budget at startup, between 00:00 and
about 02:00. Every sample is a warship scan with no selected hull and no
eligible merchant. Orange's Merchant Ships do not appear until about 39:43.
There are no yield commands 420/421. This is a diagnostic design failure, not
evidence that active merchants did or did not yield. The next diagnostic must
be armed by a real priority-hull/no-progress transition or an actual nearby
merchant rather than by empty startup sweeps.

## Landed assault lifecycle

Cyan records four event-0 commits, four event-8 landed-combat handoffs, eleven
event-13 target changes and four event-12 terminals. Seventeen actual writer
samples exercise slots 1, 2 and 3. Every recorded target owner is hostile
(Player 2 or 3), with target types 38, 70, 79, 93 and 1995 and combat tries
0-2. All four terminal reasons are 1 (group empty/disappeared), with no
reason-2 combat-lease expiry.

Representative Cyan lifecycles are:

- hull 38971, slot 1: commit 47:27, land 48:47, target at 49:03 and 49:19,
  terminal 49:35;
- hull 35788, slot 2: commit 48:15, land 49:35, repeated targets 49:51-50:55,
  terminal 51:11;
- hull 34697, slot 3: commit 48:55, land 50:15, repeated targets 50:31-51:35,
  terminal 51:51;
- hull 37803, reused slot 1: commit 54:39, land 55:51, targets at 56:07 and
  56:55, terminal 57:27.

Gray records three event-8 handoffs, fifteen target changes, sixteen writer
samples and three terminals. Slots 1 and 2 are exercised. Every target owner is
hostile Player 4, with target types 4, 84, 93, 562 and 1258 and combat tries
0-2. All terminals are reason 1, not lease expiration. Gray's first two landed
groups continue targeting for approximately 3:28 and 1:20 respectively; its
late group is reconstructed as raw/owned but has zero usable members and
terminates promptly.

This satisfies the intended runtime boundary of `f96da71`: literal hostile
selection yields a target, the actual command writer fires, all three slots
remain independent, and groups do not merely sit until lease expiry. The
replay does not directly prove damage or strategic effectiveness, so those are
separate combat-quality questions rather than part of this target-acquisition
closure.

## Migration and Transport activity

The command stream reconstructs twelve path-clear migration landings:

- Purple: 15:30, 23:10, 32:12, 41:16 and 47:27;
- Gray: 19:29, 20:06, 20:59 and 37:27;
- Red: 52:45, 63:29 and 67:27.

All twelve have a same-second unload command. There are no wrong-zone or
path-rejected candidates in this set. Terminal telemetry reports five Red
useful partials; four Purple full loads and one partial; and one Gray full, one
partial and one empty abort. No writer-33 preloaded/quarantine adoption is
observed, supporting ordinary autonomous migration rather than manual-load
adoption.

Low-level Transport activity totals 18 hulls, 393 load actions and 104 unload
actions. Red has three active hulls, Purple one, Gray eight, Cyan four and
Yellow two. This is strong runtime evidence that automatic migration is no
longer globally absent. It does not establish productive remote drop-site
completion; that remains a separate acceptance boundary.

The migration admission observer is not reliable enough to explain silent
players. Its shared 40-sample budget is consumed by paired admission/rejection
snapshots around 01:30-12:00, well before most actual migration events. Code 556
also describes reaching the immediate pre-gate fingerprint, not a committed
mission state transition, so it repeats for players that never launch. Future
admission telemetry should be transition-conditioned and preserve budget for a
real accepted/rejected mission boundary.

Assault transport activity is successful but wasteful. Cyan lands four
instrumented missions with one load abort/partial. Gray lands three but records
eight load abort/partial cycles. Yellow has one ready hull at 47:31 but no
commit/land before the replay ends. This keeps assault preparation OPEN even
though the post-landing target-acquisition defect passes.

The expedition observer mostly reports blocker 7 (fewer than two warships);
Yellow first reports blocker 2, then 7. All slot states are zero during its
early sample window, and the budget expires around 40:00-43:00, just before the
first assault commits. With only one Shipyard construction order in the match,
the naval-strength gate is causally upstream of early expedition admission.
Expedition tuning should wait until the Shipyard regression is repaired.

## High-frequency STOP/order-706 episodes

The exact stream contains 21,431 order-706 packets and 60,977 actor incidences.
Gray contributes 43,522 actor incidences, Red 7,938, Blue 3,217 and Green
2,810. The dominant actors are Villagers, established both by their presence in
the 20-settler Gray migration manifest and by independent build commands.

Top episodes include:

| Player | Actor | Incidences | Window |
| --- | ---: | ---: | --- |
| Gray | 35111 | 9,731 | 36:54-46:10 |
| Gray | 34071 | 5,445 | 24:12-45:59 |
| Gray | 7847 | 5,163 | 01:14-45:55 |
| Gray | 34781 | 3,607 | 36:34-45:33 |
| Gray | 34412 | 3,300 | 36:51-45:41 |
| Gray | 34291 | 2,295 | 18:09-45:28 |
| Red | 35151 | 3,562 | 52:51-63:33 |

The decisive boundary occurs at 36:56. Gray reports a 20-target useful partial
with five passengers left ashore. The explicit PER `STOP` action at that moment
targets only those five leftovers: 34762, 35057, 34215, 34449 and 34977.
Simultaneously, repeated order-706 packets target twelve different manifest
Villagers: 7847, 34071, 34103, 34291, 34412, 34477, 34781, 34804, 34841,
35079, 35111 and 35133. Several began flooding many minutes before they were
reserved for this migration.

The large order-706 stream therefore is not the one explicit T51 partial-load
shore STOP expanding across the manifest. It is a different native/controller
order path affecting Villagers before and during migration.

Writer diagnostics do not finish the attribution. Gray's 24-sample writer
budget is spent mostly on code 24 (routine subsequent boarding renewal) and is
gone before the 36:56 partial-load event. Red and Purple similarly exhaust
their budgets. The diagnostic neither observes the relevant code-5 partial
STOP nor excludes later writers. The replay contains only 622 explicit STOP
packets, further distinguishing them from order 706.

Status remains **OPEN/INVESTIGATING**. The next trace must not allow routine
boarding codes 23/24 to consume the entire writer budget. Reserve independent
budgets by writer class/transition and capture the actor's native action/target
and group ownership around the first order-706 onset. No behavioral STOP fix is
justified by this replay alone.

## Acceptance disposition

| Item | T51 result | Status after replay |
| --- | --- | --- |
| Literal landed target selection | hostile owners selected; actual writer fires | **RUNTIME PASS/CLOSED for acquisition and issuance** |
| Persistent landed continuation | target changes until group disappearance; no lease-only expiry | **RUNTIME PASS** |
| Shipyard placement/throughput | 1 order total versus 15 in T50 | **RUNTIME FAIL / REGRESSION OPEN** |
| Sustained Shipyard capacity tier | never meaningfully reached | **BLOCKED BY PLACEMENT REGRESSION** |
| Land trade | seven players exceed probe ceiling | **RUNTIME PASS preserved** |
| Merchant right-of-way | budget expires before merchants exist | **INVESTIGATING; diagnostic acceptance FAIL** |
| Automatic migration | 12 autonomous path-clear/same-second unload landings | **RUNTIME-SUPPORTED PASS for launch/landing** |
| Migration colony productivity | no complete drop-site proof | **OPEN** |
| Assault preparation | 7 landed missions, but repeated Gray abort cycles | **OPEN** |
| Expeditionary utilization | early warship blocker, observer expires before assaults | **BLOCKED/COUPLED TO SHIPYARDS** |
| STOP/order-706 flood | explicit STOP excluded as the 36:56 bulk source; exact writer unresolved | **OPEN/INVESTIGATING** |

## Exact next actions

1. Stop expedition tuning and repair the `d20386a` Shipyard candidate-sampler
   regression first. Preserve all downstream T49/T50 safety and verification
   gates.
2. Make Shipyard diagnostics arm on a real deficit/admission/placement
   transition so they survive into Imperial Age and identify the first rejected
   candidate/foundation boundary.
3. Preserve `f96da71`; do not redesign the now runtime-passing landed target
   acquisition path while addressing pre-departure aborts.
4. Rework migration writer diagnostics by writer class so boarding renewal
   cannot hide partial STOP/release/recovery writers, then correlate the first
   native order-706 onset.
5. Arm right-of-way diagnostics only after a real priority hull and local
   merchant exist; empty startup scans must not consume the budget.
6. After Shipyard recovery, reassess the two-warship expedition gate and Gray's
   repeated load-preparation aborts in a fresh runtime replay.

Raw replay and generated parser artifacts remain outside the AI repository.
