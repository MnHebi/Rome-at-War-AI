# T57 replay assessment — 2026-09-08

## Outcome

**706 remains INVESTIGATING. Command-boundary runtime acceptance FAILS.**
No gameplay correction is supported by this replay alone. The earlier mining
writer fingerprints remain useful; the new paired frames do not.
No runtime files changed or deployed during this assessment.

## Identity and reproducibility

- Replay: `SP Replay v101.103.48987.0 @2026.09.08 140205.aoe2record`.
- SHA-256: `a725e6b6d72a2d900344c5df2f0c5ae6f33e7e634efd0e9264f14e7852d16011`.
- Duration: 1:49:44.862. Selected colors validated independently of internal colors.
- Players1–4 share a team; players5–8 share the other. Extreme,400 population,
  normal speed1.69, shared exploration, map ID49.
- Raw replay records contain `RAWAI-P3B44T57: 505` for players6,7,8.
  Do not claim eight recorded marker messages: players1–5 lack them.
- Current installed108 files all match the T57 manifest; installed aggregate
  `8bb2b763162f4eabf726131774164127996f1f01d4634fc185a2b12884c9a949`.
  Source2254038 plus505 marker and two preserved installed exceptions are
  documented in `T57-DEPLOYMENT.md`. Counter1 remains NOT evidence of STOP.
- Corrected length-verified actor-array decoding: zero failures. Broad decoder
  supplies lobby/MAKE data only; it does not supersede corrected actor arrays.
- External artifacts under `G:\Projects\Codex\Rome at War AI\.analysis`:
  `t57-exact.json`, `t57-onset-audit.json`, `t57-matched.json`,
  `t57-boundary.json`, `t57-broad.json`, `t57-supplement.json`,
  `t57-shipyard-candidates.json`. External scripts `t57_extract.py` and
  `t57_supplement.py` reproduce extraction/reduction. No replay/map payload is
  added to the repository.

## Flood episodes and earlier divergence

23,516 distinct AI_ORDER706 packets contain51,256 actor incidences. These are
not explicit STOP packets: the replay contains250 explicit STOP packets across
all classes. With the existing >=100-packet, <=1-second gap definition there
are18 sustained episodes affecting15 actors across Red,Yellow,Purple,Orange.
Every episode has zero explicit actor STOPs in the preceding30 seconds/during.
That does not exclude internal/native stopping or an earlier command effect.

| Player / actors | Sustained706 onset | Evidence boundary |
|---|---|---|
| Red36013 | 31:11.915 |299 packets; last recorded garrison28:24.580, not a close renewal. |
| Orange34329,35048 | 34:48.977 |5,198 packets each; dense ORDER/WORK already running. |
| Orange34134,33901,34455 | 34:53.253–34:54.752 |Garrison hull36118 at34:53.044 shortly precedes these onsets; earlier economic command repetition for33901/34455. |
| Orange34455 | 41:46.542 |1,208 packets; same-hull retry41:45.792. |
| Purple66040,46919 | 86:54.773 /87:23.248 |1,052 /743 packets; earlier WORK on initial Gaia objects2253/2231, type350. |
| Orange33901 | 102:17.714 |951 packets; hull34585 garrison102:15.167. |
| Yellow34908,35218,35304,36371,36510,37716,62221 | 106:17.542 |477 each; preceding repeated ORDER to7763, initially Yellow Town Center109. |
| Orange33901 | 109:35.437 |234 packets, end-censored; hull134956 garrison43ms earlier. |

The strongest new lead is **before** the Orange706 onset. Consecutive same-target
ORDER runs with gaps <=100ms and at least100 packets begin:

| Actor | First dense ORDER | Target / packets | Last preceding garrison |
|---|---|---|---|
|35048|33:24.508|34365 /5,521|33:23.042, hull36118|
|34329|33:26.344|34365 /5,401|33:26.311, hull36118;33ms earlier|
|34455|33:29.518|35071 /5,198|33:26.311, hull36118|
|33901|33:29.604|35071 /5,193|33:29.589, hull36118;15ms earlier|

The old700–705/719 fingerprints match these garrison packets to **writer24,
modifier2**, with exact hull/count/actor arrays. Example34329 first ORDER:
sequence392097, byte offset13703680; preceding garrison sequence392057,
offset13699555. Example33901 first ORDER: sequence393258, offset13746365;
preceding garrison393250, offset13746040. Thus boarding renewal is not excluded
from investigation. This remains temporal association, not proof that the
renewal was unnecessary or the sole producer of the repeated ORDER/WORK.

During the30 seconds before34329/35048's706 onset, each has1,955 ORDERs to34365
and245 WORKs to33024. Initial header identifies33024 as Gaia type102 and33602
as Gaia type69. Dynamic targets34365/35071 are absent from the initial object
table; their exact type/owner remains unproven. Header identities are initial
state, not automatic ownership-at-onset proof. No invented Mill/Lumber Camp
classification is used for these dynamic IDs.

The matched30-second cohort contains99 actors/78 distinct garrison packets and
1,043 actor-contact windows. Same-hull renewals:778 no706-in-window,5 sustained
onsets,2 already-active,126 censored. Different-hull contacts include2 onsets.
This outcome-selected/old-mining-site-selected cohort is NOT population
incidence, independent trials, proof of boarding success, or a controlled
comparison with T56. The existing706-only classifier misses the earlier ORDER
divergence above; do not use its negative category as "no command flood".

## T57 sampling acceptance: FAIL, two separate boundaries

1. **Lost framing:** zero raw720 site headers, zero721 serial headers,609
   recorded762 ends; decoder produces zero complete frames. Default-family
   latest cumulative counters sum to at least731 selected detailed reports.
   Their tails cannot be retrospectively assigned a missing site/target.
   Maximum recorded same-timestamp chat group is50, and observed detail tails
   have missing prefixes. Synchronous default reports emit62 lines; two-actor
   boarding reports can emit142. Burst output loss is a lead, **not a proven
   engine50-message capacity or sole mechanism**; cached chat reference does
   not establish that limit. The earlier fixture captures every emitted line
   and therefore did not exercise this runtime delivery boundary.
2. **Boarding detail never selected:** latest available family1 coverage for
   Cyan,Yellow,Gray,Orange reports72 calls,65 nonempty,zero detailed reports.
   These are snapshots, not final whole-game totals. Family1 records for the
   other players are absent. This cannot be explained merely by missing frame
   headers: recorded counters themselves say zero detailed selection. It does
   not demonstrate early budget exhaustion either.

Exact missing evidence: at real boarding calls, private `reserved`, `capture`,
`b-turn`, `b-phase-valid/time`, `b-observe-due`, per-lane credits, and saved
pointer must distinguish the first failing diagnostic gate. Then demonstrate
that a compact, independently identifiable report actually reaches the replay.
Preserve command selections, pointer restoration, ownership, modifier policy,
timers and retries. Do not raise the cap or suppress renewal from this evidence.
Actual paired movement, current membership, and resource-writer identity for
the affected actors remain unavailable. Missing telemetry is not native proof.

Offline correction only: `frame_integrity()` now exposes orphan ends, abandoned
headers and serial mismatches rather than leaving an unexplained empty frame
list. Two regression fixtures cover orphan tails and interleaved players.
It does not synthesize frames or change PER/runtime behavior.

## Shipyards: functioning, still inefficient candidate discovery

30 BUILD1251 orders,28 foundation-identification records,26 ready-state records.
Ready records cover seven players; missing Cyan ready telemetry is not proof
that its foundation failed. Counts describe observed episodes, not concurrent
yard capacity: rebuilding can occur.

| Player | First build order | First recorded ready state |
|---|---|---|
|Blue|37:23|45:22 (second identified foundation)|
|Red|21:46|22:44|
|Green|21:31|21:58|
|Yellow|37:32|37:55|
|Cyan|25:03|Not recorded|
|Purple|53:02|53:43|
|Gray|41:01|41:38|
|Orange|38:08|38:31|

All11,524 complete recorded rejection tuples were evaluated against the initial
terrain grid, not just user-noticed sites. Reasons:64=10,490;65=503;62=437;
67=69;66=25. Reason64 spatial classes:3,538 inland centers,2,461 water without
nearby shore,4,491 coastal/mixed unresolved. Another437 candidates lie outside
the map. These sampled tuples are not an unbiased census of every attempted
candidate, and terrain-only analysis is not an engine placement simulator.

142 complete666–676 exact rejection-input records survive. In138, both
`can-afford-building` and `can-build` were true:39 inland,32 open-water/no-shore,
67 coastal/mixed. Two more were affordable but `can-build` false;two had both
false. Source reason64 is failed `up-can-build-line`: affordability alone does
not prove a valid site. The geometric miss rate supports continued candidate
quality work, but67 otherwise-enabled coastal records still require exact
footprint/occupancy/exploration inputs. Do not weaken safety or label this CLOSED.

## Other subsystem evidence, with limits

- Every player issued Skirmisher-family MAKE commands. Base7 queue commands:
  Blue135,Red142,Green155,Yellow186,Cyan308,Gray88,Orange38;
  Purple queued mounted2465=283 and2467=41. This disproves "no counter train
  requests" for T57; queue records alone do not prove births, threat matching,
  bounded live composition, or normal-production non-regression. Keep full
  reactive-counter acceptance FIXED-PENDING-RUNTIME.
- Every player queued Trade Carts128: Blue141,Red127,Green102,Yellow137,Cyan7,
  Purple18,Gray136,Orange129. This is not proof of profitable completed routes.
-23 recorded assault event8 handoffs: Gray19,Orange4. Source event8 follows
  the landed state/group handoff. It is stronger than merely a voyage order,
  but does not prove all groups had usable onward paths or effective combat.
- No recorded579 drop-site ready reports or312–317 help diagnostics. Some of
  these paths use self-only chat; absence cannot prove absence of gameplay.
  Colony deposit productivity, help response, real-choke ROW and expedition
  utilization remain unresolved, not accepted through adjacent progress.

## Validation and next action

- Replay identity and corrected actor-array extraction: **PASS** (limits above).
- Complete command-boundary and paired boarding evidence: **FAIL**.
- Offline decoder fixtures17/17, sampling6/6, matched-contact6/6 **PASS**;
  context metadata and `git diff --check` **PASS**.29 focused tests in this turn;
  prior625-test deployment run is not represented as a new full-suite run.
- Next: repair/verify diagnostic eligibility and delivery separately; target
  Orange33:23–33:30's first ORDER divergence, not only34:49's706 transition.
  Preserve existing installed experiments. No native gathering replacement,
  migration redesign, renewal suppression, PR mutation or deployment in this turn.
