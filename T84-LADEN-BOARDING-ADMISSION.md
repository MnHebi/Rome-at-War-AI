# T84 - laden passengers are not admitted to transport boarding (514)

## Objective

Exclude villagers carrying resources from the migration transport boarding
command. No STOP, reset or idle; no strategic-number or percentage change: the
carried load stays with ordinary economy behaviour, and the existing boarding
retry reconsiders the worker once `carry` reaches 0.

## Cause evidence (read-only, from the 513 replay and its autosave)

* The autosave decodes to a live-object table (1,323 records, 54-byte stride,
  ids sorted, 19,230,236). Every sustained ORDER storm target resolves to the
  ordering player's own drop-off building: Mining Camp (584) 73,160 packets,
  Lumber Camp (562) 51,749, Town Center (109) 17,864, Temple (104) 644.
* Onset alignment over all 43 sustained storms: the first storm packet lands
  +0.3..+1.4 s after the last `617/717` enter sample, and the actor's recorded
  state flips to `gather/709` or `hunt/713` with **target -1** while
  `garrisoned=1` at that same second, still carrying its load.
* Boarding episodes with a 300 s horizon: laden boarders (n=63) emit a median
  1,852 ORDER packets, 47 of them >=150, and only one produced no packet at all.
  Read as 62/63 non-zero; the stricter 61/61 figure belongs to the subgroup that
  both stayed inside and kept a work task (median 1,905). Unladen boarders
  (n=61) are median 0. The earlier "laden boarder that does not storm" controls
  turned out to be boarding failures that un-garrisoned one second later.
* The emission is co-extensive with the boarded episode: p2 actor 34151 has
  packets only in 2718-2902 s, the same seconds the trace shows `garrisoned=1`
  (0 of the preceding 708 gap seconds are garrisoned).

Accepted caveat: Temple (644 packets, 0.4 %) is treated as an outlier; the
drop-off reading rests on Mining Camp, Lumber Camp and Town Center.

## Change

Eleven migration boarding admission sites in `rawai-military.per` gain the
established zero-carry eligibility idiom immediately after their existing
eligibility removals:

```
(up-remove-objects search-local object-data-carry > 0)
```

Sites: 1375/1378 (RENDEZVOUS-START), 1388/1391 (RENDEZVOUS-PASSENGER),
1397/1401 (ISSUE-BOARD), 1416/1418 (LOAD-DIAG-APPLY), 1510/1512 (CHECK-LOAD
retry), 1614 (DROPSITE-FAILED -> RECALL-LOADING). At 1614 the filter sits before
`up-get-search-state local-total`, so the derived load target also counts only
admissible passengers.

The same `object-data-carry > 0` removal is already the reviewed T53 zero-carry
eligibility boundary at the economy retask sites in `rawai-homebase.per`; 514
closes the gap where the passenger lists never applied it. Nothing else changes:
no `up-reset-unit`, `action-stop`, retreat, ungarrison or delete is added, the
`sn-keystates 2` wrappers are untouched, and `MIGRATION-RETURN-DEPOSIT` (carrying
settlers depositing at home) keeps its deliberately opposite semantics.

## Protected behaviour

* Departure still happens through the existing bounded paths: the 30/45 s
  `t-island-migration` window with partial-load acceptance (`depart partial
  target`, >= 2 passengers) covers a hull that can no longer reach a load target
  inflated by laden workers.
* 512 load-wait latch, 513 native hunter floor, `300dac4` taunt fix and the 509
  operand repair are unchanged.
* Boarding-group release (`MIGRATION-IDLE`) still returns unboarded workers to
  the economy, which is how an excluded laden worker deposits and becomes
  eligible again.

## Validation (static; engine acceptance still required)

| check | result |
|---|---|
| `tools/generate_command_boundary.py --file-write` | PASS 578 rules, 816 commands (in-sync on re-run) |
| `tools/validate_per.py` | `{}` (no findings) |
| `tools/validate_rule_capacity.py` | PASS 9,394/10,000, headroom 606 |
| string budget (`writer_trace.string_budget`) | 1,498/1,500, unchanged |
| `villager_command_policy.py` | PASS (74 entries; rule hashes refreshed for the 11 sites) |
| `tools/fixtures/boarding-ctrl-contracts.json` | regenerated, and the regeneration reproduces the HEAD fixture exactly |
| `test_boarding_ctrl` (9) | OK, incl. new `test_passenger_task_selections_bar_laden_villagers` |
| `test_migration_foundation`, `test_transport_acquisition`, `test_transport_lane_fairness`, `test_t51_diagnostics` (35) | OK |
| `test_command_boundary_file`, `test_file_trace_capacity`, `test_command_boundary` (31) | OK |
| `test_writer_trace` | OK (17 historical tests opt-in) |
| `git diff --check` | clean |

Generated diff: `rawai-military.per` +15 lines (11 filters, one extra
continuation rule); registry hashes/line numbers, coverage source-map identity
and the DUC policy refreshed.

## Status and predicted runtime result

Status `FIXED-PENDING-RUNTIME`. Deployed 2026-09-20T17:04Z as
`RAWAI-P3B44T58B:514`, aggregate
`b6e24bf7d8ad17077e1aa0b4fe79e31d821afbd2eee708ad02f277ca39d872d0`, 109 runtime
files hash-verified against `.analysis/deployment-t88-514-20260920T170428Z/`
(513 backup in the same record). The 514 baseline is the 190351 replay on 513:
149 laden boarding episodes, 5,946/10,298 laden garrisoned samples, 103
sustained storms. Predicted 514 result: the laden subset of the storms largely
disappears, the residual storms concentrate in the known unladen +
persistent-work-task batch boarders with an unchanged frame cadence, the 511
load-state oscillation does not return, and successful departures are not
materially reduced.

Residual scope, deliberately not bundled: eleven passenger **move** sites
(rendezvous/recall) still walk laden workers away from their economy task. If
the runtime shows stranded laden migrants or under-strength departures, that is
the next bounded target rather than a wider economy change.

Unrelated note: `tools/writer_trace.py` run directly recurses on this checkout
because it decodes raw bytes (CRLF `;CB BEGIN` markers) before `rule_blocks`;
the same happens untouched at HEAD, so it is not a 514 effect. The string budget
was read through `writer_trace.string_budget` instead.
