# T61 — corrected correlation contracts and the bounded 508 analysis

Offline analysis only. The operand repair from `77e05ae` is preserved and
unchanged: **OPERAND REPAIR — IMPLEMENTED, PENDING RUNTIME.** No runtime PER,
generator, registry, instrumentation, installed file or gameplay policy was
touched, and no new match was run. Artifacts: original 508 replay
`9c7cdc2d…5ed459` (66:34, marker `RAWAI-P3B44T58B: 508`), log
`2026.09.12-2310.43`, frozen 508 registry and source
(`.analysis/deployment-t58b-508-20260912T200909Z/`). New outputs:
`.analysis/t61-508-correlations-v3.jsonl` + summary, `.analysis/t61-508-make.jsonl`;
v1/v2 outputs are preserved.

## 1. Verified command contracts (cached AIRef, `.analysis/airef-reference-20260830.js`)

| Command + action | Recipient source | Target source | Compatible packet families | Unavailable |
|---|---|---|---|---|
| `up-target-point` + default/guard/follow/**garrison** | local list | the point | move, order (reference: these actions "will perform as action-move") | per-unit point resolution inside a second |
| `up-target-point` + move / patrol / attack-move | local list | point | move/order, patrol/order, attack-move/order | same |
| `up-target-point` + stop | local list | point | STOP, AI_ORDER 706 | — |
| `up-target-point` + unload | local list (transports) | the point | UNGARRISON (point form) | — |
| `up-target-point` + delete | local list | point | DELETE | — |
| `up-target-objects` Option 0 + default | local list | **remote list** | work, order, garrison, guard, follow, move (documented right-click) | which right-click result the engine chose |
| `up-target-objects` Option 0 + garrison | local list | remote list | SPECIAL order 5 | — |
| `up-target-objects` Option 0 + guard | local list | remote list | GUARD, FOLLOW | — |
| `up-target-objects` Option 0 + unload/gather/none | local list | remote list | **none** (documented as action-none / gather-point set) | later villager work is not this command's packet |
| `up-target-objects` Option 1 + default/garrison/… | local list | **selected object** (`up-set-target-object`) | as above | — |
| `up-set-group` | — | — | — | bookkeeping: loads a group into a search list; no hidden selection |
| type-based (`up-garrison`, `up-ungarrison`, `up-reset-unit`, `delete-unit`, `delete-building`) | every object of a type | type | garrison/unload/stop/delete | recipients are not list-anchored |
| global (`up-retreat-now`, `up-send-scout`, `up-reset-scouts`, `up-delete-idle-units`) | global | — | retreat/scout/delete | recipients not recorded |
| state/settings/group writes; engine-side admission (`up-build`, `build*`, `attack-now`, `up-request-hunters`) | — | — | none directly attributable | later native packets are separate |
| anything else | **unclassified** | — | none claimed | — |

The previous helper conflated `up-target-point … action-garrison` with object
boarding, treated `up-target-point … action-unload` as object-directed, and let
`up-target-objects … action-default` match AI_ORDER 706. All three are corrected
in the shared contract module `tools/command_contracts.py`, which now also backs
`audit_writer_trace.compatible()` so the two matchers cannot drift.

## 2. Corrected recipient-gap and matching counts (v3, 200,051 rows)

| Category | Rows | Meaning |
|---|---|---|
| `no-direct-packet-expected` | 196,154 | 192,634 state writes, 3,263 engine-side admissions, 240 group writes, 17 reads |
| `candidate-not-causation` | 2,199 | one compatible packet in the labelled window |
| `empty-input-recorded` | **1,651** | complete PRE declares the consumed list empty (1,628 local, 23 remote) |
| `ambiguous` | 32 | more than one compatible packet retained |
| `type-based-recipients` | 14 | `up-reset-scouts` (global set) |
| `unsupported-contract` | 1 | `up-target-point … action-pack` (documented action, no attributable family) |

The T60 statement "1,628 recipient gaps" was wrong: none of those rows is a
missing observation. They are complete PRE frames whose declared local list was
**empty**. The named sites behave exactly that way — `1303`
(`position-self-x action-stop`) declared 0/0 in 333 rows and 1/0 in 57, `1706`
declared 0/1 in 298 and 1/1 in 57, `1738/1740` 0/0 in 154/134, `1739/1741` 0/1
in 79/80 with 57 rows at 0/2. Site 1303 sits directly after
`(up-full-reset-search)` + `(up-add-object-by-id search-local
g: gl-island-migration-transport-id)` in the rendezvous rule, so the recorded
empty list means that hull lookup resolved nothing at that moment; the only
object the stop command could address is the hull itself, never a passenger.

Also corrected: Option-1 `up-target-objects` rows (14 sites) are now anchored on
the recorded selected object; the 94 rows v2 reported as
`unmatched-not-native-proof` were such rows whose remote list was empty.

## 3. Order-706 flood, recomputed

| Measure | Value |
|---|---|
| distinct 706 packets | 38,259 |
| actor incidences | 46,850 |
| the five sustained runs (packets as counted per run) | 37,977 |
| **union of those runs by sequence id** | **32,534 = 85.0 %** (the 99.3 % figure double-counted 5,443 packets shared between the two p6 runs) |
| 706 packets inside a traced bracket | **0** (the v2 "9" were `action-default` right-click sites matched through the old contract) |
| scripted commands addressing a flood actor inside its burst | 1513 ×2 (p2 33923), 1398 ×1 (p6 33901), 1398/1419 ×1 (p6 42361), 1614 ×1 (p7 7674) — all `up-target-objects 0 action-garrison` |

Actor timelines (traced type-21 state, plus type-22 hull state and replay packets):

| Actor | Pre-onset | Onset and burst | Hull motion inside burst | Burst end |
|---|---|---|---|---|
| p6 42361 (14,692 pkts, 3265-3787 s) | walk to hull 34434 (action 617 / order 717 / target 35559→36537) | same second: `garrisoned 0→1`, action 609 / order 709, position frozen at 950,12135 | 2,875 records, 235 positions, 32 tiles — **not stationary**, slow drift | 7 UNGARRISON + 6 ORDER on the hull inside the window; nothing after |
| p6 33901 (11,636, 3264-3666 s) | walk to hull 34434 | same second: garrisoned 0→1 | 2,886 records, 237 positions, 32 tiles | 7 UNGARRISON + 6 ORDER |
| p2 33923 (9,044, 2871-3122 s) | walk to hull 34898 (targets 34655/35544) | same second: garrisoned 0→1 | 1,323 records, 69 positions, 10 tiles | 1 UNGARRISON + 2 ORDER; no packets after 3122 s |
| p7 7674 (2,471, 3678-3723 s) | walk to hull 50556 | same second: garrisoned 0→1 | 326 records, 49 positions, 8 tiles | hull ORDER at 3732/3735 s and **UNGARRISON at 3775 s** (52 s later) |
| p2 33889 (134, 2926-2928 s) | garrisoned in hull 34898 from 2864 s | unload transition 2926 s; then gathering (carry 0→8, target 33234) → new action 602/order 702 at 2950 s → gathering target 33235 | 31 records, 1 position, 0 tiles | unload itself |

Boarding cohort with censoring (first boarding per actor, 120 s window):
423 actors boarded; **42 censored** (fewer than 120 s of recording left),
**369 with zero** 706 packets, 7 with 1-4, and the 5 flood actors. So the
published "411 of 423 had no 706" was a mix of zero-packet and unknown/censored
cases; the failure rate among *uncensored* boardings is 5/381 = 1.3 %.

The dominant scripted writer of garrison-family packets is not a boarding
command at all: `up-target-objects 0 action-default` sites 1205 (417),
1202 (396), 1196 (216) in `gl-farm-staffing-state` rules, i.e. right-click
assignment of farmers/fishermen (4/2/0 of them overlap the flood actors), plus
`up-target-objects 1 action-default` naval siege/response sites (114/29/22) and
migration load sites 1513 (72) / 1388 (22). Genuine transport boarding sites are
these migration/assault ones; their in-burst occurrences are the handful listed
above.

Conclusion (unchanged in substance, corrected in detail): the 706 churn is an
engine-side reaction while passengers sit inside a hull that is being re-tasked
and slowly repositioned; the script is not re-boarding them during the burst,
and no traced command's documented packet family matches any 706 packet in this
recording.

## 4. Migration, assault, merchant, production

**Migration.** p2's ready-branch result stands: at 2971 s
`MIGRATION-RETASK-DROPSITE` (cmd 1593) → CHECK/ASSIGN-RETASK-ANCHOR → RELEASE →
IDLE; the ten passengers of hull 34898 then produced 7,135 WORK, 5,924
AI_ORDER, 2,807 ORDER and 2 BUILD packets between 2971 and 3300 s, and their
traced carry cycles ramp and reset (e.g. actor 33889: carry 0→20 then 0) which is
consistent with gathering and dropping off, though **the deposit site itself is
not observed**. p7's failure predicate is now exact: at `rawai-military.per:4833`
(frozen cmd 1567) the state goes `MIGRATION-DROPSITE-FAILED` when the anchor is a
gold/stone class, `gl-island-migration-placement-attempts >= 3`,
`(can-afford-building mining-camp)` and the build test fails — and that build
test is the literal-`0` `up-can-build …`, the operand family the 508 engine logs
as `Invalid goal used (0)` and that the T60 repair replaced. The chat
`"migration rejected mining point: %d"` accompanies it. p7's PRE frames at 3680 s
(site 1567) show a valid selected object (38161) with empty local/remote lists.
For p1/p3/p4/p8 the T60 hypothesis is **withdrawn**: their admission masks were
0 in 64/84/54/91 samples (293 of 299) and the `256` bit (route-timer/all-channel
veto) appeared only once for p3, three times for p4 and once for p8 — the
admission gate was *open*, so the route-timer hypothesis is not supported. What
remains is that no migration lifecycle record exists for them, which is either a
sampler artefact (state leaving and returning inside the 16-per-episode lifecycle
budget) or an immediate abort at the first transport/ownership gate.

| Category | Count | Bit meaning (source) |
|---|---|---|
| admission masks with no blocker | p1 64, p3 84, p8 91, p4 54 | mask 0 |
| relic-ferry busy (+1) | p7 9, p6 7, p8 6, p5 2 | `not gl-relic-ferry-state RELIC-FERRY-IDLE` |
| route state busy (+8) | p5 10, p7 5 | `not gl-transport-route-state TRANSPORT-ROUTE-IDLE` |
| clear state busy (+16) | p6 10, p2 7, p4 5, p1 4 | `not gl-transport-clear-state TRANSPORT-CLEAR-IDLE` |
| all assault-channel veto (+256/257/272) | p5 7, p4 3, p2 2, p3 1, p8 1 | route timer triggered + admission open + home defense NO + transport ≥ 1 + enemy seed ≥ 1 |

**Assaults.** Boarding sites classify cleanly by their rule gate: migration
(1513 `MIGRATION-CHECK-LOAD`, 1388 `MIGRATION-RENDEZVOUS-PASSENGER`), assault
(1698 `TRANSPORT-ROUTE-LOAD-CHECK`), and home/economy right-click sites. Hull-keyed
episodes: hull p8/7645 (573 boarding packets, 1425-3382 s, 232 unload packets)
with the unloaded actors producing 259 WORK + 2 BUILD in the following 180 s —
OBSERVED SUCCESS at the unload-and-work boundary (per-mission manifest and
land-combat outcomes remain unreconstructed); hull p6/46455 (435 boarding packets
3858-3979 s, no unload — recording ends at 3994 s: CENSORED); hull p6/34251
(22 boarding packets 661-795 s, no unload: a retried load that never departed).
An `UNGARRISON` packet is a hull-side command, not a landing; 946 unload packets
do not imply 946 landings.

**Merchant right-of-way.** Executed mapping (source hash equals the installed
508 file): the accepted selection is logged as 580 kind, **581 = selected hull**,
582 = its action, 583 = its group, 584 = candidates, 585 = eligible; the rejected
candidate is logged as 617 kind, 618 = rejected hull, 619 = its **action**,
620 = its group, 621/622 = its **destination x/y**, 623 = constant 8, 624 =
candidates. The T60 description ("618 selected hull, 619 hold reason, 621-622
merchant counts") was wrong. Observed: p2 1450-1560 s accepted hull 34325
(action -1 idle, group -2, 6-7 candidates, 1-2 eligible); p8 2180-2300 s eight
consecutive rejected candidates (hulls 34468/34297, action 621, group -2,
destinations like 48,16) — a persistent-rejection case. The merchant-side
yield → progress → resumption chain is **not reconstructable** from this
diagnostic family: it records the hull selection and counts, not the merchant's
own path or the priority hull's progress.

**Reactive skirmishers.** The command cache omits the production family
(`MAKE` is decoded but not retained by the command extractor), so a targeted
extraction of only that family was added (`.analysis/t61_train.py`,
4,017 packets with `unit_id`). Skirmisher (unit id 7, `rawai-unitconstants.per`)
production per player: p1 43, p2 67, p3 41, p4 42, p5 20, **p6 0**, p7 30,
p8 26 (elite id 6: 0 everywhere). These are **births**, not queues or threats;
requests/threat response are not observable, and unit-ids beyond the mod's own
constants are unverified names.

## 5. Remaining evidence gaps (with why the recording cannot close them)

1. **Group/selection contents for group-scoped commands**: only what the trace
   reads from the search lists is recorded; the 1,651 empty-input rows show the
   lists *were* empty, so no hidden selection is needed for them. Missing
   observation for any group command that does act: the group membership at
   command time (a group loaded but not enumerated would look like an empty
   list).
2. **Transport-route timer status**: no registered command arms
   `t-transport-route`; the arm (`rawai-assault-missions.per:108`, `c: 1`) is not
   traced, so admission-timer state cannot be reconstructed.
3. **Dropsite identity/status**: the ready branch is visible, but the dropsite
   object's `status-pending → status-ready` transition and the assigned builder
   are not recorded per actor; deposits are unproven.
4. **Merchant path/progress**: no merchant-side state in the ROW family.
5. **Queues vs births**: production packets are births; AI queue/request state is
   not in the replay and has no 508 diagnostic.
6. Whole-second trace timestamps define intervals, log record ids and replay
   sequence ids are different orderings, and packet presence never proves a
   task's success.

## 6. Corrections recorded against earlier reports

| Earlier claim | Correction |
|---|---|
| "1,628 recipient gaps / 34 sites" (T60) | recorded **empty inputs** from complete PRE frames |
| "196,168 indirect-recipients-unknown" (T59/T60) | state/admission/group writes with no directly expected packet |
| "99.3 % of 706 packets in five runs" | **85.0 %** after de-duplicating shared packet sequences |
| "9 of 38,259 706 packets inside traced brackets" | **0** with the documented contracts; the nine came from a right-click site matched as stop |
| "411 of 423 boardings had no 706" | 369 zero + 42 censored + 7 with 1-4 (5 sustained); 1.3 % of uncensored boardings flood |
| "p1/p3/p4/p8 blocked by the t-transport-route timer" | admission masks were 0 in 293 of their 299 samples; the blocker hypothesis is withdrawn |
| "p7 aborted unexplained" | explicit `MIGRATION-DROPSITE-FAILED` after 3 placement attempts, decided by the literal-0 `up-can-build` test repaired in T60 |
| "618 = selected hull, 619 = hold reason, 621-622 = merchant counts" | 581 = selected hull; 618/619/621/622 = rejected hull, its action and its destination |
| "hull waits stationary during the burst" | hulls move slowly inside the bursts (10-32 tiles); the passenger's frozen position is not hull stationarity |

## 7. Validation

`tools/test_command_boundary_log.py` (11 tests, table-driven) covers the
contract table, empty versus incomplete inputs, Option-0 versus Option-1
targets, selected-object anchoring, genuine target mismatches, documented packet
families only (AI_ORDER 705 matches nothing), the labelled post-invocation
second, ambiguity, exact versus subset recipients, and unclassified commands;
`tools/test_command_boundary_log.py` + `test_writer_trace` (tool tests),
`test_command_boundary_file`, `test_t51_diagnostics` and `test_command_boundary`
were re-run for the shared `compatible()` change (55 tests, OK, 17 historical
opt-in skips). Real-recording spot checks for the corrected matcher: p2 hull
34898 boarding episodes, p8 hull 7645 unload with follow-up work, p2 1450-1560 s
ROW selection, and the p7 3680 s dropsite PRE frames.
