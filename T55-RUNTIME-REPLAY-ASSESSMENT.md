# T55 runtime assessment — 2026-09-07 11:43:51

## Identity and scope

Replay: `SP Replay v101.103.48987.0 @2026.09.07 114351.aoe2record`.
SHA-256: `D8C435519F009C470C45B241FB36FE07629ED50DEA7F12B36D0C996A247FDAC2`.
Duration **34:11**, no parser errors. Marker **RAWAI-P3B44T55:503** appears at
startup. Installed runtime matches source `1f87ef0`: 99/99 files, no overlay,
aggregate `6EE2AC23972B252500C62F9961D51E6C0C42956F4DA52125C5B487F87229D86C`.
Analysis checkout HEAD: `6f1d31a`; no gameplay changes or deployment in this audit.

Decoded replay and spatial outputs remain outside Git under workspace `.analysis`:
`replay-20260907-114351-t55-full.json` and `t55-shipyard-sites/`.
Reproduction uses `tools/analyze_replay.py`, `tools/analyze_shipyard_sites.py`,
and `tools/audit_task_ownership.py` (`read_stream`, `economic_retask_correlation`).
The initial terrain grid is 220x220. Nominal settings match the preceding setup,
but this is not an identical-seed controlled experiment.

## Shipyards: partial improvement, acceptance not complete

All three issued Shipyard builds produced concrete foundations and ready events:

| Player | Build order | Coordinates | Foundation / appearance | Ready |
|---|---|---|---|---|
| Cyan (5) | 26:27 | 205.5,66.5 | 35503 / 26:28 | 27:32 |
| Green (3) | 31:16 | 6.5,106.5 | 36556 / 31:17 | 32:13 |
| Cyan (5) | 33:07 | 153.5,11.5 | 36970 / 33:08 | 33:51 |

Blue, Red, Yellow, Purple, Gray and Orange issued no Shipyard build in this replay.
At the same 34:11 cutoff T54 had one Shipyard (Cyan); T55 has three, including
Cyan's second. T54's full 48:03 match had three across three players, so comparing
only full-match totals would obscure the different observation lengths.

Initial-terrain inspection places the three T55 sites on coastal water, with
Green near an inlet opening and Cyan on the outer east/north coasts. This is not
proof of dynamic congestion clearance, builder movement or naval egress.

### Rejected placement coordinates

404 complete rejection records include 373 reason-64 buildability rejects:

| Spatial classification | T55 count | T55 share |
|---|---:|---:|
| Land center | 120 | 32.2% |
| Water with no nearby shore in 5x5 | 96 | 25.7% |
| Coastal/mixed, unresolved | 157 | 42.1% |

Noncoastal rejects fell from **84.4% of 2,497** in T54 to **57.9% of 373** in
T55. This supports an improved sampled-candidate distribution, not a controlled
causal success-rate estimate: seeds, duration and admitted episodes differ, and
these are rejected samples rather than every random draw. Coastal rejects still
require dynamic placement/occupancy evidence; terrain alone cannot explain them.

### Earlier admission boundary: available wood

Of 194 periodic deficit admission snapshots, **190 report can-afford-building
false**, and four true. All 194 report worker-hold zero. Affordability-false counts:
Blue 23/23, Red 23/25, Green 24/25, Yellow 24/24, Cyan 24/24, Purple 25/25,
Gray 25/25, Orange 22/23. Cyan nevertheless built twice between snapshots:
these samples cannot establish continuous poverty or continuous gating.

Current authoritative DAT gives Shipyard 1251 a **150 wood** cost for every
civilization in this replay. Cached AIRef says `can-afford-building` excludes
escrow and does not test civilization/technology availability. Therefore these
false samples identify a resource-admission boundary, not a missing prerequisite.
They do not distinguish low total wood, escrow reservation, or competing spending.
Tech-up holds occur in some snapshots, but cannot alone explain the many false
affordability checks with tech-up hold absent.

**Result: broad Shipyard acceptance NOT PASSED; sampler FIXED-PENDING-RUNTIME.**
Retain the bounded sampler and safety gates. Next investigate wood/escrow and
spending at the earliest persistent deficit before changing economic policy.
Do not weaken placement safety or globally bypass tech-up saving on this evidence.

## Other acceptance gates

- **Assault shore egress: INCONCLUSIVE / not exercised.** No recorded RAW3,
  RAW-plan or assault-ready episodes. No candidate-witness/unload lifecycle to
  validate the exact mobile-witness query. Generic SPECIAL/UNGARRISON packets
  are not evidence of assault missions. No-witness and actual-unload gaps remain.
- **Help: INCONCLUSIVE.** No 312–317 exact help-episode diagnostics; this is not
  proof that overwhelming attacks were correctly handled.
- **Migration productivity: INCONCLUSIVE.** No code-579 ready lifecycle proves
  autonomous remote foundation, completion, gathering and deposit.
- **Merchant ROW: INCONCLUSIVE.** No 631–637 clearance episode establishes a
  real choke yield/progress/trade-resumption success.
- **Expedition: unchanged.** Do not tune commitment before upstream acceptance.

## Villager command experiment

There are 4,625 AI_ORDER packets, including **1,482 subtype 706 packets**.
Subtype is decoded from packet bytes, not inferred from the separate ORDER name.
There are also 457 ORDER and 163 STOP packets; these are distinct packet families
and must not be combined into a claim that the historical flood is fixed.

The exact-stream correlation reconstructs five instrumented retasks, all Blue:

| Actor | Time | Writer | 706 in preceding 30s | 706 in following 30s |
|---|---|---:|---:|---:|
| 33992 | 05:26 | 3 | 0 | 0 |
| 34214 | 15:39 | 4 | 0 | 0 |
| 34182 | 21:00 | 4 | 0 | 1 |
| 34388 | 26:45 | 4 | 0 | 0 |
| 34135 | 32:47 | 3 | 0 | 0 |

Writer 3 is free-economic-villager-to-farm; writer 4 is fisherman-to-resource.
None sampled an active preceding flood. Actor 34182 was observed targeting 35102
after the requested target 33167, so assignment persistence is not universal;
this alone does not establish why it changed. The largest individual 706 totals
are 58 each (Purple 7777, Gray 7788), spread across the match and unsampled.
**Experiment remains INCONCLUSIVE**, not a runtime acceptance or causal closure.

## Next actions

1. Trace Shipyard available-wood/escrow/spending at persistent admission deficits.
2. Keep coastal/mixed rejection causes separate from admission starvation.
3. Exercise assault exact-witness validation in a replay with actual missions.
4. Obtain an active-flood retask sample; retain all protected-behavior criteria.
5. Keep help, migration productivity and real-choke ROW explicitly open.

This assessment changes documentation only. Static tests cannot close any of
the unexercised runtime criteria above.
