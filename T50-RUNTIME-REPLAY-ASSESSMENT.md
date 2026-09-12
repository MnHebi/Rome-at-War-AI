# T50 runtime replay assessment

## Scope and identity

This is a replay-only assessment. It makes no gameplay, generated-source or
deployment change.

Replay:
`SP Replay v101.103.48987.0 @2026.09.05 173048.aoe2record`

- SHA-256: `1B796446E790221433F14DBF1AA65AED2246933905267B667F466DD0E083CC1C`
- duration: 69:18;
- game build: `101.103.48987.0`;
- map: Iberia (RMS id 49), 400 population, speed 1.69, Extreme, no treaty,
  shared exploration;
- parser result: complete stream, zero decoder failures;
- runtime marker: `RAWAI-P3B44T50:498` is replay-visible for Players 6-8.
  All eight players use `AI RAW`; the installed/source T50 payload had already
  been independently verified byte-identical at aggregate SHA-256
  `FEA37CD1D2ED54D49C1EB0D5A79608F25CD11A10CDE8C0EBFD774BC007A5B672`.

Validated selected-color/player mapping is Blue/Dacians, Red/Pontus,
Green/Seleucids and Yellow/Syracusans on team 2, versus Cyan/Nubians,
Purple/Numidians, Gray/Carthaginians and Orange/Egyptians on team 3. The
recording terminates with a Player 1 resignation packet at 69:18; that packet
does not by itself establish the test's intended outcome.

## Result summary

- **T49 Shipyard admission retention: runtime-supported PASS.** A geometric
  rejection can now be followed by another candidate and a concrete-foundation
  observation without returning through reason 1 admission.
- **Shipyard throughput: PARTIAL PASS.** Fourteen Shipyard build orders occur by
  60:00 and 15 by 69:18, across seven players. T48 had nine by 60:00 across six
  players. Six players issue at least two by 60:00 and Red reaches two at 63:15.
  Green owns two Ports but issues no Shipyard order, so the no-zero-player
  acceptance criterion fails.
- **T50 near-aperture quality: exercised but not closed.** Water-exit reason 67
  appears six times across four players, versus zero samples in T48. This proves
  the water-exit rejection path ran, but the replay does not identify whether
  W5/W6 specifically rejected a throat or prove that every accepted site opens
  onto a good sea lane.
- **Land trade: runtime PASS.** All eight players train more than the three-Cart
  probe ceiling; 343 Trade Carts are trained in total. Three players also train
  80 Merchant Ships, demonstrating simultaneous independent land/water modes.
- **Assault landing: active, but landed combat continuation fails its telemetry
  acceptance.** The three-slot controller reaches event 8 eight times (five
  Blue, three Yellow), yet records zero combat-target transitions and zero
  bounded landed-combat issuance samples. Seven of those combat leases later
  terminate at event 12; the eighth begins only 36 seconds before replay end.
- **STOP/command flood remains open.** The exact stream contains a 120-second,
  8,912-packet continuous STOP-706 burst against the same two Yellow migration
  settlers immediately after landing, plus two-frame setup packets. Ordinary
  target-order floods also affect migration settlers before/during voyages.
  T50 is not a writer-instrumented runtime, so the exact producer remains
  unresolved.

## Shipyard lifecycle

The table distinguishes build issuance from reason 7, which is the controller's
replay-visible observation that the intended local Shipyard foundation exists.
A build packet alone is not proof of foundation appearance or completion.

| Player | Shipyard build orders | Reason-7 foundation observations |
| --- | --- | --- |
| 1 Blue | 47:02, 50:23 | 47:41 |
| 2 Red | 55:37, 63:15 | 56:35, 63:16 |
| 3 Green | none | none |
| 4 Yellow | 50:02, 55:12 | 50:07 |
| 5 Cyan | 39:41, 44:55 | 40:02, 45:17 |
| 6 Purple | 20:26, 55:33 | 55:34 |
| 7 Gray | 46:25, 51:34, 54:20 | 47:01, 52:02 |
| 8 Orange | 14:14, 52:58 | none sampled |

The first-yard result is mixed rather than uniformly faster. Blue improves from
54:15 in T48 to 47:02 and Red/Gray recover from zero, while Green regresses from
51:54 to zero. Yellow, Cyan and Purple issue their first yard later than in T48.
The aggregate gain is therefore primarily minimum-capacity throughput, not a
general first-yard latency win.

Diagnostic 410 totals are:

| Reason | Meaning | Samples |
| --- | --- | ---: |
| 1 | unavailable/unaffordable | 56 |
| 4 | worker hold/unreachable | 4 |
| 5 | tech saving | 1 |
| 7 | intended foundation observed constructing | 9 |
| 62 | candidate outside map | 10 |
| 64 | exact candidate unbuildable | 79 |
| 65 | own-building clearance | 11 |
| 66 | allied-building clearance | 3 |
| 67 | water-exit validation | 6 |

Reason 64 remains dominant. Green's zero-build chain contains seven reason-64,
two reason-66 and one reason-67 samples. Gray alone accounts for all ten
map-bound reason-62 samples.

T49's retained admission is visible most clearly for Red: reason 64 at 54:27 is
followed by reason 67 at 55:35, a new build at 55:37 and reason 7 at 56:35,
without an intervening reason 1. Yellow similarly remains in geometric
rejection/foundation states from 49:07 through 67:54 while issuing two builds.
That is runtime evidence that one local miss no longer forces every retry back
through admission.

T50's exact former Orange failure coordinate `(49.5,174.5)` is not reused; the
two current Orange orders are at `(130.5,28.5)` and `(103.5,26.5)`. This avoids
the known site but is not proof that the new accepted sites are free of narrow
approaches. Visual/map-zone confirmation of accepted-site apertures is still
required before closing T50 placement quality.

## Trade and right-of-way

Trade production is:

| Player | Trade Carts | Merchant Ships |
| --- | ---: | ---: |
| Blue | 71 | 0 |
| Red | 6 | 0 |
| Green | 11 | 6 |
| Yellow | 70 | 0 |
| Cyan | 34 | 25 |
| Purple | 34 | 0 |
| Gray | 61 | 49 |
| Orange | 56 | 0 |

Every player exceeds the three-Cart probe ceiling. Under the current source
contract, growth beyond three requires live `actionid-trade`; land trade is
therefore runtime-established for all players, not inferred merely from train
orders. Green, Cyan and Gray operate both modalities in the same replay.

There are no paired diagnostics 420/421. Those are emitted only when the local
right-of-way controller actually moves a Merchant Ship for a stalled priority
hull. This recording therefore supplies no positive runtime acceptance for
merchant yielding and no basis to call it failed: either no full trigger formed
or no eligible local merchant was available when a priority hull stalled.

## Migration and assault lifecycles

Migration terminal telemetry records:

- Blue: one full load, one useful partial, three empty aborts and two later
  `migration route unreachable` terminals;
- Red: one full load followed by a path-clear landing event;
- Green: one full load/path-clear landing, then one later empty abort;
- Yellow: two useful partial loads with path-clear landing events and two empty
  aborts;
- Orange: two useful partial loads followed by low-level unload phases;
- Cyan, Purple and Gray: no worker-migration terminal in this replay. Purple and
  Gray do have separate relic-ferry transport activity.

Yellow's first observed remote drop-site attempt is informative. After the
37:55 path-clear landing, the controller records ten group-11 settlers in the
correct zone, placement attempt 1, and blocker mask 4 (the requested Mining
Camp was not affordable at the pre-action sample). A Mining Camp build order is
nevertheless issued at the intended `(16,121)` point at 37:59. The replay does
not provide a later matching completion observation, so this is issuance, not
proof of a productive completed colony.

Assault preparation and mission telemetry is concentrated in Blue and Yellow:

- Blue: four load aborts, three accepted partial departures, three explicit
  full-ready hulls and five event-8 landing/combat handoffs;
- Yellow: two load aborts, three accepted partial departures, two explicit
  full-ready hulls and three event-8 landing/combat handoffs;
- one Yellow voyage records event 4 (voyage no-progress) and event 10 recovery;
- no other player emits an assault mission event.

The eight event-8 handoffs are real controller transitions into the persistent
landed-combat state. They do not prove combat success. The diagnostic added at
the actual landed `up-target-objects` issuance site never fires: there are zero
`RAW landed combat target`, zero event-13 target changes and zero issuance
triplets. Five Blue and two Yellow missions later emit event 12; Yellow's final
landing at 68:42 remains inside its lease when the replay ends. The earliest
post-landing divergence is therefore target acquisition/issuance, not transport
formation or beach handoff. Why the per-enemy target searches remain empty is
not resolved by this replay alone.

## High-frequency command episodes

The exact decoder records 13,472 `AI_ORDER` order-706 STOP packets. Normal
background samples are spread across all players, but Yellow contributes 9,496.
The dominant tuple selects exactly objects `32825` and `33303`:

- 2 setup packets at 44:07;
- 8,912 uninterrupted packets from 44:15 through 46:15;
- 11-16 ms inter-packet gaps dominate;
- both objects are settlers in Yellow's second migration manifest;
- the matching hull `34890` reports useful-partial acceptance at 42:14 and a
  path-clear landing/unload at 44:05.

Before landing, those same settlers receive high-frequency ordinary ORDER
packets toward Yellow-controlled object `32789` at `(192,194)`: object `33303`
receives 7,124 from 41:53-44:07 and object `32825` receives 8,284 from
42:01-44:07. The target object's type is not reconstructed by the command
stream.

A second independent ordinary-ORDER flood affects Blue migration settler
`34149`: 14,640 identical orders toward Blue-controlled object `33213` at
`(29,205)` from 35:20-42:56, spanning Blue's 35:32 full migration, 37:05 route
failure, 41:23 partial migration and 42:55 route failure. Orange later shows
similar migration-settler orders toward object `7733`, which is independently
identified as Orange's Villager-producing Town Center.

These episodes are not explained by the 376 explicit `STOP` action packets;
order 706 is a distinct decoded AI-order form. The replay establishes the exact
actors, timing and migration relationship, but T50 has no command-writer
fingerprint. Attribution to a particular PER rule or to native task expansion
would be speculation. Status remains **INVESTIGATING**.

## Acceptance disposition

- **T49 admission retention:** PASS in this replay.
- **T50 Shipyard throughput:** PARTIAL PASS; materially higher throughput and
  seven-player coverage, but Green remains at zero despite two Ports and first
  yard timing remains inconsistent.
- **T50 aperture quality:** FIXED-PENDING-RUNTIME; reason 67 is active, accepted
  site quality is not proven.
- **Land trade:** PASS/CLOSED for the existing T46 acceptance.
- **Merchant right-of-way:** FIXED-PENDING-RUNTIME; no intervention sample.
- **Migration:** mixed; several path-clear/full/partial missions, two Blue route
  failures and one issued-but-unconfirmed Yellow drop site.
- **Assault landing:** eight successful script handoffs, but landed combat
  continuation is an acceptance FAIL because no target/issuance telemetry fires.
- **STOP/ordinary-order floods:** OPEN/INVESTIGATING with an exact reproducible
  Yellow migration episode.

Raw replay and generated parser artifacts remain outside the AI repository.
