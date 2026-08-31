# T15 replay audit and isolated T16S1 STOP experiment

## Identity and limits — 2026-08-31

- Replay: `SP Replay v101.103.48987.0 @2026.08.31 134755.aoe2record`,
  SHA256 `46367A652B0823505591B6997E3A8E71B847F2C74F14361C4DE00CC2EB8F1F79`.
  Duration157:27; the final RESIGN packet belongs to replay player8 Gray.
  No crash attribution. Seven serialized startup markers identify T15:460;
  recorder Red has the established self-marker asymmetry.
- All83 installed/source runtime files were independently identical to
  `8C9DF5B2B90E69656627ED1ACC5174EC22C16A47E8EEE83A519E8DD76FEF664B` before edits.
  Selected colors and resolved teams validate Red/Green/Yellow/Purple Romans
  versus Orange Picts/Cyan Britons/Blue Germani/Gray Gauls. No row/color inference.
- Full parser errors0; exact command decoder failures0;787,809 retained events.
  The542 ERROR action packets are game records, NOT parser failures.
- All-player command/boarding audit includes successes, recalls, underfill,
  congestion and unresolved episodes. A command is not proof of execution,
  a load acceptance is not arrival, and an empty-hull terminal is not useful combat.
  Private AI chat principally exposes Red. No invented object-ID offsets.
- Editing directory/Git root is the documented recovery exception:
  `G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-transport-only`, branch
  `recovery/p3b44-transport-only`, HEAD `387eccab36a3311ca90d9e39bea6d73013584a8b`
  plus intentional pending work. Canonical `.pr-work\Rome-at-War-AI` and immutable
  P3B44 baseline are untouched. No commit, push, PR update or deployment here.

## STOP — acceptance FAIL, causal attribution still INVESTIGATING

| Color | T15 STOP706 packets | T14 STOP706 packets | T15 Imperial |
|---|---:|---:|---|
| Red |38515|24647|25:40|
| Green |1072|629|33:17|
| Yellow |1030|355|40:45|
| Purple |5089|2179|34:11|
| Orange |266|36371|39:41|
| Cyan |687|8881|40:00|
| Blue |3866|7993|35:59|
| Gray |1989|351920|never|
| Total |52514|432975| |

The aggregate fell87.9%, but these are different matches of different duration
(T14=105:36), not a controlled causal result. Red worsened. Gray's improvement
cannot be credited to reaching Imperial: it never did. Do not call the flood fixed.

Red's dominant recipients are migration workers, identified by boarding/build/work
history. Group `[4619,32401,32420,32649,32823,32938,33738]` receives5,113 identical
STOPs67:06–70:12; its six-member predecessor3,431 in65:19–67:05. Worker34127 receives
4,813 singleton STOPs89:24–100:48; another thirteen-worker group3,567 in91:54–95:23.
Packets repeat on roughly20–50ms intervals. Per-object totals must not be summed
as packet totals: one group order targets several workers.

The first large episode already floods before the65:21 useful-partial terminal.
That partial lift reaches the waypoint66:38 and logs ten landed settlers67:06;
Mining Camp attempts68:42,69:04,69:25,69:47 yield failure70:07. Hull46911 later
unloads at home70:13 through71:14; the worker STOP sequence ends around71:28.
This is temporal association, not proof that every recipient stayed aboard.

Source-first audit enumerated every explicit `action-stop` site in all runtime
PER files: general cleanup, explorer retirement, escort release, migration
partial/abort/scout handling, assault stragglers, recovery and relic cleanup.
Existing RAW12 per-minute counters were summed, not treated as cumulative maxima.
Red's generic missing-target STOP writer1 ran only twice (37:00/46:00 reports),
writer2 only49 times, migration partial writer5 three times. Writer5 cannot cause
the earlier onset at65:19 by its65:21 call. These writers do not directly account
for38,515 packets. A script-triggered native persistent loop remains possible;
absence of a matching counter does not identify one particular engine controller.
Counters90/91 count native attack-exclusion maintenance, not movement orders.

### T16S1:461 — EXPERIMENTAL, NOT a causal fix

User previously authorized reversible single-hypothesis STOP experiments. The
next test changes only `sn-consecutive-idle-unit-limit` from0 to5 seconds for
Moderate/Hard/Hardest/Extreme; lower difficulties retain10. This SN is documented
as the delay before an all-idle attack/retreat/scouting group is reset. The test
asks whether immediate native group recycling sustains repeated STOPs. Applicability
to these worker groups is unproven. The five-second value is a test parameter,
not measured optimal policy and not a guarantee about engine command cadence.

- Behavior file: `rawai-sn-defines.per`, four one-shot initialization rules.
- Identity only: `rawai-init-goals.per`, marker `RAWAI-P3B44T16S1:461`.
- No STOP site, worker search/ownership, loading acceptance, route, economy,
  fishing, native gather quota, defense or target selector is otherwise changed.
- The exact83-file T15 control was archived BEFORE editing at
  `G:\Projects\Codex\Rome at War AI\.analysis\p3b44t15-runtime-control.zip`.
  Extracted payload hash equals the installed T15 hash above. This is an immutable
  diagnostic archive, not another development directory.
- T16S1 source hash:
  `91F8328EC2782301CDDE9295BF9248E3AE0CAB8AA109A98EDAB866734FD22955`.
  Exact archive comparison proves only those two runtime files differ. The SN
  file's non-comment executable difference is precisely the four0→5 operands.
- Non-regression: preserve actual gathering, construction, useful full/partial
  boarding, route progress, early scouting, Imperial retirement, productive fishing,
  screened departures and combined attacks. A quieter AI caused by inactivity FAILS.
- Test comparable migration boarding/voyage/landing exposure, repeated-identical
  STOP run lengths and recipient-seconds, not only total match counts. Prefer the
  same starting scenario/seed when practical; never rerun an old replay with new
  source and call that a live test. Existing counters remain unchanged.
- If there is no material reduction in repeated STOP bursts or useful work
  regresses, revert this one-SN experiment before testing a different mechanism.
  Restore only its four operands and assign a fresh marker; do not restore entire
  files over unrelated changes. No additional tracing overlay is introduced.
- Two focused configuration tests PASS. PER/operand, strategy, naval doctrine,
  counter synchronization and694-site ownership checks PASS. Full-suite result
  and final test status are recorded in HANDOFF. Runtime acceptance NOT RUN;
  T15 remains installed. STOP remains INVESTIGATING, not FIXED/CLOSED.

Read-only adversarial review: ACCEPTED that the mechanism is only a hypothesis;
ACCEPTED that group reset delay can delay legitimate native retasking and requires
the above non-regression test; REJECTED attributing the flood to writer1/5 based
on mismatched counts/onset; DEFERRED unrelated behavior changes until this trial.

## All-player transport evidence

### Follow-up correction: Purple's native multi-hull wave

The SPECIAL-derived census below is not an exhaustive mission count. The exact
command stream additionally contains Purple ENTER717 passenger assignments to
eight hulls around1:15:14–1:15:19 and TRANSPORT714 orders toward Gray's shore
1:16:01–1:17:45. Hulls34536/33348/33056 receive714 at1:16:36/1:16:43/1:16:46.
Assigned passengers later receive Gray-targeted attack/work orders. Do not label
this three successive executions of the custom singleton controller.

Hull33348's Gray-bound714 at1:16:43 is followed by custom `assault hold reason:1`
and home UNGARRISON at1:18:37. This establishes an overlapping command path,
not the cause of every Red abort or actual native group membership. Orders alone
do not prove every hull arrived. The private exact stream already contains this
evidence; future lifecycle reducers must include717/714, not only SPECIAL and
UNGARRISON. T16A1's independent voyages/native-takeover guard are pending fresh
runtime validation; see HANDOFF.md.

256 reconstructable boarding windows:157 assault,61 migration,38 unresolved/
recovery/relic. Their961 load commands cover all players. The window census
is not exhaustive of every native/manual-loaded hull or maritime movement.

| Color | Assault windows | Accepted | Recall | Boarding abort | Completion log | Landing timeout | Unresolved |
|---|---:|---:|---:|---:|---:|---:|---:|
| Red |24|13|12|10|1|0|1|
| Green |23|22|19|1|0|0|3|
| Yellow |37|36|35|1|0|1|0|
| Purple |14|13|13|1|0|0|0|
| Orange |0|0|0|0|0|0|0|
| Cyan |0|0|0|0|0|0|0|
| Blue |19|19|18|0|0|0|1|
| Gray |40|37|37|3|0|0|0|

Red completion log75:33/hull46911 precedes the reported late manual assistance;
useful surviving troop combat is not independently established. Yellow times out
at147:51. Orange/Cyan each have three other boarding windows: zero assault
windows is not zero transport activity. Broad assault participation still FAILS.

64 screening-fallback denials:62 code4 and two code1, **zero unscreened commits**.
Code4 by color:Red4,Green7,Yellow2,Purple2,Blue10,Gray37. Code1:Green1,Blue1.
Code4 covers no enemy at scan start OR invalid/inactive/nonhostile/zero-known-
building saved opponent at final validation. It does not prove actual danger.
The repeated denial is established; its two branches remain undistinguished.
Source checks covered manifest admission/reset/capture, sole goal writers,
bounded enemy iteration, final focus restoration and objective facts; no supported
fix yet. Do not bypass all safety validation or guess an iterator semantic.
Status INVESTIGATING; queue remains STOP → code4 → failure-aware rotation → RC.

Congestion events also occur beyond the screenshots:Blue hull35395 stalls three
times53:19–54:11, unresolved54:38. Green hull57905 has three bounded failure cycles
73:08–75:16,81:32–83:38,136:11–138:17. Red46911 stalls73:59, resumes74:08.
The user-observed1:56:45 clogged Red Port mostly contains GREEN merchant vessels
around Red's fully loaded Transport. Existing own-unit clearance is not evidence
that this allied traffic jam is handled. Cross-owner clearing needs coordination,
not issuing commands as another player. Remains OPEN, behind the release queue.

## Manual intervention and unresolved defect ledger

These observations are authoritative symptoms. They are not autonomous AI successes.

### Migration drop-sites — OPEN / runtime acceptance FAIL

- Red1:41:21 mineral-island Mining Camp was user-built. User was uncertain about
  wood at initial landing and manually sold food/bought wood/ferried workers.
- The exact stream includes Camp584 at100:48 by eight workers at(39,45), and
  another at101:16 by thirteen workers at(61,15), matching the later wooded-island
  observation. A different single-worker Camp at(130,199)101:29 matches the AI's
  exact foundation89178/complete101:40 record. Do not merge these three sites.
- Red logs two failed drop-sites70:07/92:55, three landed-settler events and one
  verified drop-site completion. Logs show attempted placement is not foundation.
- Wooded island at1:43:53 had no minerals according to the user; AI built a Mining
  Camp there after manual ferrying. Global `stone-present YES` is not a local
  resource test. Delayed old placement work is a hypothesis, not proven linkage.
- Source migration uses native `up-build place-point`, waits for a concrete
  foundation, then assigns exact workers. Foundation admission/native worker
  assignment and wrong-site pending work remain separate unresolved causes.
- Next: correlate each queued placement/anchor/point with its concrete foundation
  and worker; distinguish affordability, geometry and native assignment before
  changing it. Acceptance: real correct-island dropoff followed by resource income,
  including delayed affordability; no mineral-free island Mining Camps.

### Market food surplus / wood starvation — INVESTIGATING

- User saw >20,000 food before manually selling it/buying wood. Later screenshots
  show different post-intervention balances and do not disprove that observation.
- Replay contains259 Red food SELL packets and117 wood BUY packets over the whole
  game, including manual activity. This does not show the AI autonomously traded
  when needed. No reliable pre-intervention stockpile/price time series is decoded.
  The85–105 minute window has no food sale until a47-packet burst96:57–97:13,
  each amount5 (500 food), consistent with the user's manual surplus conversion.
  Intermittent100-wood purchases already occur before that burst; the defect is
  not literally the absence of every Market purchase.
- Ordinary Imperial food-sale gate requires gold<200; emergency wood-buy requires
  gold>=1000, and operating wood-buy>=1500. An affordability/policy gap is visible,
  but a separate resource-pressure relocation bridge can sell/buy below those
  ordinary thresholds. Red logged home resource pressure at62:57. Therefore the
  ordinary thresholds alone are not a proven explanation of this episode.
- Next: discriminate bridge demand/price/resource gates and manual transactions.
  Acceptance: fund a genuinely needed dropoff/wood purchase from surplus food,
  retaining age-up/strategic reserves rather than indiscriminate market dumping.

### Unreachable naval target — source policy gap; gameplay defect OPEN

- User saw Red/Green naval fixation1:52:57 while reachable targets existed farther
  along the beach. Red selected target59165 **170 times98:27–135:19**.
- Search radius had reached255 at61:00. `rawai-naval-siege-watch.per` expands
  search on missing progress, but has no per-target no-damage rejection/cooldown
  after hitting that limit. Expanding a search alone does not exclude its former
  preferred unreachable target. This missing recovery policy is source-proven;
  the exact target's reachability/firing geometry is not reconstructed by orders.
- Preserve observed working bombardment and Palintonons. Next after release queue:
  bounded per-source/target progress test with alternative reachable firing/target
  selection; same target must not monopolize the fleet indefinitely.

### Fortress interruptions — INVESTIGATING, no direct STOP attribution

- User's Red worker53684 receives Fort82 BUILD attempts127:08,127:18,127:23,
 127:34,127:35 around(154–162,209–216); foundations did not visibly appear until
  later intervention. User says the worker appeared stopped, then was freed.
- User explicitly confirmed Outpost598 at127:28 was also their test to unlock the
  worker. It is NOT evidence of a competing AI Outpost job. Several MOVE packets
  interleave; their issuer is not identified by these packets. No explicit STOP
  packet targets this worker in these attempts, nor matching same-second ERROR.
- This does not reject the visible interruption; it rejects prematurely naming
  a direct STOP writer. Next inspect native placement acceptance/worker state or
  a controlled exact-worker reproduction. Acceptance: valid manual construction
  can reach a foundation without AI/native job interference.

### Gray never Imperial — INVESTIGATING

- Gray reaches Early10:14/Middle37:28, never Imperial. Requests Monastery104 at
 42:18 and University209 at61:18; no Fortress82 or Siege Workshop49 BUILD requests.
  Requests are not proof those prerequisites finished/survived.
- Authoritative DAT: Imperial103 costs1000food/800gold, requires102+661;661 can
  use142;142 accepts a Fortress/Krepost or359;359 needs two qualifying completed
  building techs. Monastery tech107 plus University146 can supply two. A Fortress
  is therefore NOT mandatory. Civ25-only no-buildings bypass638 does not apply to
  Gauls8. No data-mod payload copied into Git.
- Source has a five-minute Middle-age generic `up-can-research` fallback, so
  strategic timing alone is not sufficient attribution. Actual completion,
  resources, queues and trainability remain unverified. Next discriminate those
  gates; acceptance: age advances once real prerequisites/resources are available.

### Positive observations and fishing limits

- User manually landed Red armies on Blue around1:49:53, then later on Gray.
  Red/Green's subsequent retargeting from cleared Blue to Gray before formal
  defeat is a positive observation of the existing cleared-target fallback,
  not validation of the still-unimplemented failure-aware target rotation.
- All-player PACK packet count0. This is positive T15 evidence, not universal
  proof that every packing defect is impossible.
- Fish Trap199 requests25:Red3,Green5,Yellow4,Purple5,Orange1,Cyan1,Blue2,Gray4.
  Each has nearby follow-up WORK/ORDER records to a concrete trap target; Red
  directly logs foundations36190/73369/93387 and Fishing Ships32990/71183 assigned.
  Native BUILD recipient4294967295 is an unassigned sentinel, not a villager.
  Fishing Ship construction/completion and food production still need confirmation.
- Post-Imperial EXPLORE705 packets remain; fishing is deliberately exempt.
  Command code alone cannot label every such recipient an illegal general explorer.
  Do not close the whole exploration policy from a reduction in STOP traffic.

## Reproducible private artifacts and next actions

Outside Git, under `G:\Projects\Codex\Rome at War AI\.analysis\`:
`replay-20260831-134755-t15-full.json`, `p3b44t15-command-stream.json`,
`p3b44t15-exact.json`, `p3b44t15-transport-audit.json/.txt`,
`p3b44t15-task-ownership.json`, `p3b44t15-summary.json`, `p3b44t15-findings.json`,
`p3b44t15-inspection.json`, `p3b44t15-episodes.json`, and the immutable runtime ZIP.
Reducers: `audit_writer_replay.py ... --plain-runtime`,
`summarize_t13.py p3b44t15`, `inspect_t15.py`, `reduce_t15_episodes.py`.
The trap join explicitly includes ORDER, not only WORK. Raw replay remains external.

Next: authorized deployment/fresh test of the isolated STOP hypothesis, compare
actual command behavior and productive exposure, accept/revert it on evidence;
then resolve fallback code4, then add failure-aware target rotation. Other defects
remain explicit above and in the earlier ledger, not silently closed or canceled.
