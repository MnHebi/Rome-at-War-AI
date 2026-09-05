# T50 Shipyard throughput and near-aperture validation

## Status

**ROOT-CAUSE-PROVEN / FIXED-PENDING-RUNTIME / DEPLOYED**, 2026-09-05.
Source and installed marker `RAWAI-P3B44T50:498`; their aggregate SHA-256 is
`FEA37CD1D2ED54D49C1EB0D5A79608F25CD11A10CDE8C0EBFD774BC007A5B672`.

The two corrections are independent commits:

- T49 `9ca1a6a`: retain one admitted Shipyard placement lane across bounded
  local candidate misses;
- T50 `0bfce18`: reject a locally narrow approach throat even when the older
  far-water proof can route around it.

Deployment was explicitly authorized from canonical HEAD `312fac5`. Preflight
found exactly `rawai-init-goals.per`, `rawai-shipyard-defs.per` and
`rawai-specialplacement.per` different from installed T48. All three were
copied. A separate read-only check reports all 99 runtime files identical, with
no missing, different or unexpected files, and independently finds the
marker-498 line in the installed `rawai-init-goals.per`.

## Completed T48 replay

Replay:
`SP Replay v101.103.48987.0 @2026.09.05 162415.aoe2record`, SHA-256
`E09783EF66D897DB7AF5ED6B3B486916FFD547D36A6A858F55F0EDBC151560E6`.
It runs 60:00 on Iberia (map 49, size 220) with zero parser errors. The replay
contains the T48 marker for the observed players.

T48 issued nine Shipyard build orders across six players:

| Player | Shipyard build orders |
| --- | --- |
| 1 Blue | 54:15, 57:44 |
| 2 Red | none |
| 3 Green | 51:54, 59:51 |
| 4 Yellow | 41:16 |
| 5 Cyan | 37:03 |
| 6 Purple | 14:44 |
| 7 Gray | none |
| 8 Orange | 23:15, 38:54 |

This is a material recovery over T47's two orders across two players, but it
does not meet the intended prompt/minimum-capacity behavior. The T36 runtime
control on the same map family had approximately 28 orders across all eight
players by 60 minutes. T48's first-yard latency extends to 54:15, and Red and
Gray never issue one.

Bounded diagnostic 410 samples contain 64 exact-candidate-unbuildable reason
64 transitions, six own-clearance reason 65 transitions, one allied-clearance
reason 66 transition and three map-bound reason 62 transitions. No water-exit
reason 67 was sampled. Reason 64 remains the dominant placement boundary.

## T49 source cause and correction

Every local geometric rejection (62 through 67) entered the terminal reset
path. That released the builder/placement state and discarded the already
admitted lane after only one candidate. A later sweep had to satisfy admission
again before trying another point. The completed replay's repeated
candidate-failure-to-admission gaps explain the long latency and the two
zero-build players without implicating affordability, desired counts or the
foundation verifier.

T49 adds `gl-sy-attempt` and a bounded eight-candidate loop around the same
ready anchor. A geometric miss now rotates to another exact candidate while
preserving the admitted lane. Exhaustion still releases the lane and records
failed-site memory. Actual worker, availability and affordability failures
continue through their existing terminal paths.

Files/rules changed:

- `tools/generate_shipyard_placement.py`: bounded local retry state;
- generated `rawai-shipyard-defs.per` and `rawai-specialplacement.per`;
- marker in `rawai-init-goals.per`;
- focused assertions in `tools/test_shipyard_coast.py` plus marker assertions
  in `tools/test_trade_topology.py` and `tools/test_validators.py`.

## T50 source cause and correction

Orange's second Shipyard was visibly placed in a narrow strait at replay
coordinate `(49.5,174.5)`. The replay map tiles show why the existing proof
accepted it: the west-facing checks at `(43,174)`, `(37,174)`, `(37,170)` and
`(37,178)` are all water, but the near lateral point `(43,180)` is beach. The
old W1/W2/W3/W4 shape sampled the forward centerline and only the far lateral
aperture. It could therefore skip over, or path around, a throat immediately in
front of the building.

T50 retains W1 through W4 and adds W5/W6 at W1 plus/minus six lateral tiles.
Both near-aperture points must be in bounds, in the same water zone and
path-connected. This rejects the proven narrow-throat geometry while retaining
the existing far-open-water proof.

Files/rules changed:

- `tools/generate_shipyard_placement.py`: near-aperture point construction and
  checks;
- generated `rawai-shipyard-defs.per` and `rawai-specialplacement.per`;
- marker in `rawai-init-goals.per`;
- focused geometry and marker tests.

## Preserved behavior and risk boundary

Both patches retain T48's recovered candidate domain, anchor wrap, exact
`up-can-build-line`, own/allied separation, far-water proof, worker
reachability/ownership, affordability, desired map caps, failed-site memory and
concrete-foundation verification. They do not change Ports, trade, transports,
naval combat, economy percentages or Shipyard desired counts.

The runtime non-regression criterion is that T48's six-player/nine-order
recovery survives while first-yard/minimum-capacity latency improves and the
observed Orange-style throat is rejected. Candidate retry must remain bounded;
closed water, crowding, unaffordability and missing workers must remain vetoes.

## Validation

- Shipyard lifecycle/geometry: **PASS**, 18 tests.
- Trade topology: **PASS**, 10 tests.
- Migration fixtures: **PASS**, 23 tests.
- Ownership contract: **PASS**, 27 tests.
- Task ownership: **PASS**, 13 tests.
- Naval right-of-way: **PASS**, 13 tests.
- Transport lane fairness: **PASS**, 3 tests.
- Validators: **PASS**, 128 tests.
- PER structure/operand validation: **PASS**, empty report.
- Strategy execution: **PASS**, all 1,156 matchups.
- Naval doctrine: **PASS**.
- Replay benchmark metadata: **PASS**, 42 benchmarks.
- Ownership source audit: **PASS**, 972 relevant sites, zero failures.
- Generated Shipyard source synchronization: **PASS**.
- Full Python 3.12 discovery: **PASS**, 516 tests. The sandboxed attempt reached
  only the known Windows Temp permission boundary; the identical authorized
  run passed.
- `git diff --check`: **PASS**.

The deployed source/install aggregate SHA-256 is
`FEA37CD1D2ED54D49C1EB0D5A79608F25CD11A10CDE8C0EBFD774BC007A5B672`.
All 99 runtime files are byte-identical after deployment.

## Fresh-runtime acceptance

A fresh marker-498 replay must demonstrate:

1. T48's multi-player Shipyard recovery is retained;
2. admitted placements try bounded alternate candidates without returning to
   admission after every reason 62-67 miss;
3. first yards and minimum operational capacity arrive materially sooner, with
   no viable Port-owning player left permanently at zero;
4. Orange-style near throats fail water-exit validation while open sites still
   produce concrete foundations;
5. own/allied clearance, economy discipline, desired caps, failed-site memory,
   worker ownership and foundation verification remain effective.

Until that replay exists, T49 and T50 remain **FIXED-PENDING-RUNTIME**.
