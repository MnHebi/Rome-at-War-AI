# T16A2:463 replay — transport dispatch audit

## Scope and identity

User request: find what prevents transport dispatch, preserving the progress in
the current runtime. This is a diagnostic/source audit. **No runtime change or
deployment was made.** Source defects below are not claims of gameplay closure.

- Working directory and Git root:
  `G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-transport-only`.
  Branch `recovery/p3b44-transport-only`, HEAD
  `387eccab36a3311ca90d9e39bea6d73013584a8b`, with preserved intentional pending
  T13–T16 work. This is the documented recovery exception; no workspace switch.
- Replay `SP Replay v101.103.48987.0 @2026.08.31 162617.aoe2record`, 72,115,206
  bytes; SHA256
  `F8D75EC49C2FF9DA206B872CAD697E98DF56F9C17FCE559F012F90BE130859E7`.
  Duration 97:06; final replay-player1 RESIGN. User ended the stalemate; no crash.
- Seven startup markers, players2–8: **RAWAI-P3B44T16A2:463**. Recorder self-marker
  asymmetry persists. Independently checked all87 source/installed runtime files:
  identical, zero missing/different/unexpected. Full payload SHA256
  `3A246F56182BAEAF2EE4D3C0FA93844B48E8A8A35992791628B2D8C6CD7C7558`.
- Decoded selected colors, not internal colors or slot order: replay players1–8
  are Red, Green, Yellow, Purple, Orange, Cyan, Blue, Gray. First four are Roman
  Empire; the others Picts, Britons, Germani, Gauls. Resolved teams2/3 agree with
  the preserved user teams1/2. Britannia, Extreme, population400; header speed2.0,
  shared exploration. Do not assert a decoded map dimension from nominal Huge.
- Used the compatible local `replay_parser_kjir` header parser and existing exact
  command decoder. Final header/parser errors0; exact decoder failures0;
  1,158,622 retained command/chat events. The older `replay_parser` failed header
  decoding and was not used for final player/color claims.

## 1. Missing hull-acquisition postcondition — ROOT-CAUSE-PROVEN source fault

### Earliest divergence

T16 added native transport/unload order exclusions to the actual ownership claim,
but not to the preceding empty-hull selection, and did not check that the claim
succeeded before entering boarding. The same defect exists in three claim rules:

| File/rule in unchanged T16 source | Relevant lines |
|---|---|
| `rawai-military.per`, mining hull claim | 1903–1923 |
| `rawai-military.per`, scout hull claim | 1930–1950 |
| `rawai-military.per`, assault LOAD-FIND claim | 5556–5573 |
| Assault candidate selection without the new order exclusions | 5530–5552 |
| Assault LOAD-READY exact-hull rebuild and wrong-owner reset | 5448–5507 |
| Migration route commands require the migration ownership flag | 2559–2605 |

The reproducible sequence is:

1. Select an own, empty, idle, unflagged Transport.
2. Rebuild that hull for acquisition. Exclude order714 (`orderid-transport`) and
   order721 (`orderid-unload`), even though the candidate search admitted them.
3. Create an empty group if the selected hull was excluded; nevertheless advance
   into boarding/passenger selection. A scout attempt is also consumed.
4. Boarding/cargo checks can still address that saved hull ID and report a useful
   load without confirming hull ownership.
5. Migration movement removes the hull because its flag is not group10. The
   command consequently has no recipient, but the route timer/state advances.
   Assault FIND retries acquisition and then silently returns to IDLE if the hull
   still is not group3, leaving a loaded hull without a committed voyage.

This is not evidence that every passenger was taken by a competing controller:
the mission can fail to acquire the **hull in the first place**. Nor is the
resulting migration timeout necessarily evidence of a blocked physical route.

### Controlled source reproduction

Executed the actual claim rule bodies with the existing PER fixture interpreter,
not a Python rewrite of intended behavior. Compared unchanged T16 against
`rawai-military.per` read directly from the immutable T15 runtime ZIP. Same own,
empty, idle, flag-2 hull inputs; three mission types; orders0/714/721:

| Source | Cases | Acquisition contract |
|---|---:|---|
| T15, all three orders and mission types | 9 | PASS: hull acquired before advancing |
| T16, ordinary order0 | 3 | PASS: hull acquired before advancing |
| T16, order714 or721 | 6 | **FAIL: empty owner group, flag-2, boarding state entered** |

The reproduction succeeded in exposing all six failures. It does not simulate
engine persistence of an old order ID, pathfinding, or an actual game departure.
T15's unconditional acquisition is a comparison control, not a proposed blanket
reversion of protection for genuinely active native/manual voyages.

### Runtime corroboration and limits

T16 has28 migration terminal samples: outbound phase1 has11 flag-2 and one flag10;
return phase2 has12 flag-2 and four flag10. Thus23/28 samples report an unowned
hull. Comparable T15 terminal group logs were all24 flag10. These are terminal
samples, not28 unique migrations or an exposure-matched performance comparison.

| Player/hull | Accepted load and terminal evidence |
|---|---|
| Red31477, scout | Full at17:03;18:35 idle, cargo1, flag-2, position185,177 versus origin184,178; return fails19:52. Reused24:25, repeats25:57/27:14. User later ferried the scout manually. |
| Red40804, resource | Accepted16/20 at67:27;68:59 idle, flag-2, cargo16, position equals origin194,168, best/current distance45; return fails70:16. |
| Red31594, resource | Full20 at90:39;92:11 idle, flag-2, cargo20, distance47, position204,167 near origin208,165; return fails93:28. |
| Purple31750 | Repeated outbound/return failures75:51/77:07,82:12/83:29,88:29/89:46,94:30/95:47; flag-2 with4,6,10,10 passengers respectively. |
| Yellow33093 |92:28/93:45 idle, flag-2, cargo11, position equals origin88,166, distance40. |
| Gray31558 / Cyan32023 | Initially fail with flag10 after movement; later reuse fails with flag-2. This also preserves evidence of a separate, genuinely owned failure class. |

**Limit:** the replay does not log the exact order/flag at every acquisition
instant. The source defect is established and fits the repeated-reuse failures;
it is not proven that714/721 at acquisition caused every unowned hull, or that no
later writer can also lose ownership. Do not claim all congestion or assault
aborts are explained by this one patch.

### Smallest corrective action — proposed, not implemented

Align candidate and acquisition eligibility; make successful exact-hull
ownership a prerequisite for passenger selection, boarding, and consuming a
scout attempt. A rejected claim must not advance. Preserve active native/manual
voyages; distinguish genuinely active voyages from completed idle hulls before
changing reuse policy. Add a bounded explicit owner-lost terminal/recovery path
after boarding rather than silently abandoning loaded cargo. Never recover by
commandeering another active owner's hull. Test these acquisition failures and
their ordinary-order controls against the actual rules before a fresh replay.

## 2. Eleven code401 cancellations — observed blocker isolated

Every detailed fallback cancellation in this replay is **401**, not enemy death,
global target replacement, underfill, or detected defensive fire:

- Gray5, Blue4, Green1, Cyan1.
- All stage2; initial/first iterator result-1; zero enemies scanned.
- Saved enemy remains valid; checked enemy equals saved enemy, liveness failure0,
  live gate1, current global target equals saved enemy.
- Gray's saved enemy4=Purple; Blue's3=Yellow; Green's7=Blue; Cyan's4=Purple.

`rawai-assault-screen-fallback.per:66–97` passes the accepted hull check, calls
`up-find-player enemy find-ordered`, receives-1, and cancels before the fresh
route/landing danger scan can run. The finer T16 diagnostics have answered what
the old generic code4 could not.

Checked the cached primary AI reference and constants: `find-ordered`=3 is
correct; output goal14205 is within DE's1–16000 range. A guessed wrong method
constant or unsupported extended goal is not an established explanation. Why
the engine lookup returns-1 in these circumstances remains **INVESTIGATING**.

The narrow proposed replacement is bounded literal player1–8 hostile/liveness
enumeration, reusing the literal-player approach in admission, while preserving
the all-enemy danger scan. Do not treat iterator failure as permission to skip
danger checks or infer that the saved opponent was defeated. No extra broad
telemetry build is necessary to identify this cancellation branch.

## 3. All-player census: failures are mostly before independent voyage commit

Counts below are public-log checkpoints joined to command-linked hulls, **not
distinct mission totals**. Reused hulls can log several accepted loads. Zero
public assault checkpoints does not mean a player has no other transport tasks.

| Color | Command-linked hulls | Full-ready | Approved partial | Underfill abort | Landing hold1 | Denial401 | RAW3 commits |
|---|---:|---:|---:|---:|---:|---:|---:|
| Red |8|18|4|4|1|0|1|
| Green |7|6|1|4|3|1|0|
| Yellow |5|11|4|2|1|0|0|
| Purple |2|0|0|0|0|0|0|
| Orange |1|0|0|0|0|0|0|
| Cyan |10|7|10|5|2|1|0|
| Blue |10|7|1|4|0|4|0|
| Gray |9|17|6|3|0|5|0|

Total52 command-linked hulls;66 full-ready and26 partial checkpoints;22 underfill
aborts. The existing ownership reducer found153 boarding windows and522 loading
commands. Window boundaries and intervening orders alone do not prove a foreign
controller stole a passenger; terminal/recovery/manual actions must be separated.

Only **one** new RAW3 voyage commit occurred: Red hull41383, slot1, saved
enemy5=Orange,52:38; event8 landing53:58. No other RAW3 commit/event was recorded.
Green's accumulating fleet is therefore not explained by three occupied slots.
The immediate bottleneck is before preparation hands a hull to those slots.

Preserved successes: user observed Yellow's assault onto Blue around49 minutes.
Yellow hull34105 receives native transport order714 at49:12 toward50.5,139.5;
there is no RAW3 commit. This is a successful **native-path** observation, not
proof that Yellow exercised the new independent slots. Red's observed53-minute
success agrees with the explicit RAW3 commit and landing.

Green detail: hull31481 ready52:33, screen waypoint timeout then401 at54:12;
48445 ready62:28 then hold1;31653 ready64:34 then hold1/home unloads, ready again
68:27 with no commit/hold afterward;32303 ready69:20 then hold1, ready again71:27
without commit/hold;33004 accepts partial8 at77:55 without a RAW3 commit. Hulls
32480 and49372 also have underfill aborts. This corroborates repeated loading and
non-departure without pretending the screenshots identify every individual hull.

Red hull38121: ready71:32/hold1 at71:33; repeated ready73:48,74:54,76:52,77:44,
78:55 without a RAW3 commit. Interspersed home unload requests are not departures.

### Separate landing-plan and physical-blockage classes

Seven hold1 events follow the landing planner (`rawai-military.per:5990–6112`).
It checks the target anchor and two lateral points28 tiles away; both candidate
failure paths combine known static defenses and wrong-land-zone rejection.
Two rejected candidates do not exhaust the coastline. Current telemetry cannot
distinguish those causes for every Green hold. Keep real-danger and same-island
vetoes; do not solve this by making every loaded Transport sail into known fire.
Broader bounded candidate search/plan failure rotation is a separate follow-up.

Remaining public hold classes are also accounted for: nine no-screen-ship holds3
(Gray5/Blue4), one Green waypoint timeout5 and one Cyan beach-approach timeout9
feed the11 code401 denials above. Yellow hull34105 has hold8 at47:35: the landing
scout's `object-data-under-attack` check fired. That is not an allowed soft-failure
fallback and does not by itself identify the attacker. Its later native49:12
departure must not be misclassified as an earlier successful screened commit.

User's Yellow migration at~79 minutes was assisted by deleting blocking
Shipyards; do not count it as autonomous collision recovery. Hull48634 accepts
partial10 at77:58, then landing/unload candidates78:44 at71,111 and79:04 at73,111.
User saw no drop-site afterward. Existing own-ship clearance is not proof of
recovery from friendly land units or another player's building. This class and
the multi-allied Trade Cog bottleneck remain open and are not disproven by the
ownership finding.

## 4. Observation/manual-intervention ledger and separate open defects

- Red~20-minute loaded scout versus debug `loaded transports:0`: prior source
  inspection established this label counts eligible escort candidates, not all
  loaded hulls; it must not be used as a cargo census.
- Red boarding vessel attached to an enemy Scout at29 minutes and a Fishing Ship
  earlier, without conversion: user-observed failure. DAT task eligibility alone
  does not prove successful conversion; interference/progress cause unresolved.
- Red scout ferried manually toward Gray~35 minutes; escort changed en route.
  Generic20-second escort release/reselection is a source-visible persistence
  issue, not a T16 fix. Manual movement/landing is not an autonomous success.
- Red~1-hour loading shuttle and post-intervention abort: user only moved the
  hull near waiting boarders while AI fought the orders. Hull40804 already logs
  a loading-timeout abort59:05, cargo0; manual move cluster59:53–60:00; unload
  order60:06. **Timing/meaning of the post-input abort remains unresolved**;
  asked whether the observed post-input abort was unloading/returning. Preserve
  both accounts; do not attribute the initial timeout to the user's later input.
- Red and Yellow later repeated load/abort reports remain represented by the
  all-player census, not assumed to be exclusively one cause.
- Green screenshot1:10:48, subsequent3/4 loaded hulls, a fifth abort, then six
  loaded without departure1:20–22: accepted as visible observations; exact hull
  census/membership cannot be reconstructed completely from those images alone.
- Yellow's assisted79-minute landing produced no observed drop-site. Red's earlier
  T15 missing/wrong-island Camps and economy/placement failures are still open.
- Multi-allied Trade Cog jam at1:30:20; Red later had several loaded assault and
  migration transports stationary. Physical congestion can coexist with commands
  never being issued to the unowned hull. Do not collapse those failure classes.
- Gray remained below Imperial; user saw Temple but no University. Requested
  building orders in earlier tests do not prove concrete foundations/completion.
- Skirmisher absence: earlier source audit found enemy class-count predicates in
  reactive gating unsupported by the referenced command semantics. Bounded
  Bowmen/Crossbowmen counter selection needs a separate source fix/validation.
  Mounted Skirmisher is a Numidian unique family, absent from this fixture; do
  not treat its absence here as proof that generic production failed.

STOP remains **INVESTIGATING**, not solved by the S1 experiment:353,691 STOP706
packets (Red10,859;Green158,453;Yellow35,879;Purple146,171;Orange223;Cyan983;
Blue655;Gray468). T15 had52,514, but duration/exposure/composition and other T16
changes differ. No controlled causal success claim for idle-reset-delay0->5.
Dispatch diagnosis does not silently close or erase this earlier priority.

## 5. Corrective order, review and acceptance

1. Fix the acquisition postcondition and candidate/claim mismatch as one causal
   patch. Cover assault/mining/scout, excluded orders, real competing owners,
   empty search, and ordinary successful claims. Add bounded terminal recovery
   for an already-loaded hull whose preparation ownership is lost.
2. Replace the failing fallback enumeration dependency as a separate patch;
   verify all eight player identities, live/hostile filtering, full/approved
   partial manifests and the complete known-danger/same-island checks.
3. Reassess remaining holds, underfilled loading, actual collision cases, and
   useful departures before changing landing/target policy. Preserve separately
   recorded STOP, dropsite, placement, boarding and economy defects.

Previously working behavior at risk: Yellow's native transport, Red's committed
voyage, ordinary fresh-hull acquisition, approved5–9 passenger partials, three
independent sealed voyages, and protection from known danger/foreign ownership.
Acceptance requires actual autonomous progress/landing, not merely quieter logs.

- **PASS, diagnostic reproduction:**18 actual-rule comparisons executed; all six
  expected T16 acquisition-contract failures reproduced;12 controls passed.
- **PASS, evidence/integrity checks:**37 replay benchmarks validate;
  `git diff --check` reports only line-ending warnings, no whitespace failures;
  final independent read-only sync verifies all87 source/installed files retain
  the same463 payload hash, with zero missing/different/unexpected files.
- **FAIL, gameplay objective:** repeated accepted loads still do not dispatch;
  zero unscreened commits,11 code401 cancellations. Three concurrent autonomous
  voyages are not demonstrated by this replay.
- **PASS, observed positive control:** Red's one RAW3 commit has a landing event
  and matching user observation; Yellow's native-path success is preserved as a
  separate observed success. Neither closes overall assault participation.
- Adversarial read-only review **ACCEPTED**: do not blanket-remove native voyage
  protection; do not generalize terminal flag evidence to unlogged claim order;
  do not call ready checkpoints unique missions or slots full; distinguish
  genuine danger/geometry from enemy-iterator failure; preserve assisted landings.
- **REJECTED with evidence:** code401 means target resigned/global target changed;
  all failures arise from three occupied slots; wrong `find-ordered` numeric
  constant or output-goal range is established; S1 is runtime-proven successful.
- **DEFERRED beyond this diagnostic scope:** gameplay edits/deployment and broad
  backlog integration. Runtime remains463. Fixes will remain
  FIXED-PENDING-RUNTIME until a fresh engine test exercises their acceptance.

## Reproducibility and artifacts

All following artifacts are under the external workspace `.analysis`, not the
AI-only repository; raw replay and data mod were not copied into Git:

- `p3b44t16-full.json`, `p3b44t16-command-stream.json`, `p3b44t16-exact.json`.
- `p3b44t16-transport-audit.json` / `.txt`, `p3b44t16-task-ownership.json`,
  `p3b44t16-summary.json` (existing extraction/reducer pipeline).
- `audit_t16_dispatch.py` -> `p3b44t16-dispatch.json`: all-player public event
  bundles, command-linked hull lifecycles/runs, cancellations and migration
  terminals. Exact full command stream remains available for further queries.
- `reproduce_t16_claim_gap.py` -> `p3b44t16-claim-reproduction.json`: actual PER
  source comparison using repository `tools/test_assault_missions.py` interpreter.
- Immutable `p3b44t15-runtime-control.zip` was read, not modified. Its83-file
  payload SHA256 is
  `8C9DF5B2B90E69656627ED1ACC5174EC22C16A47E8EEE83A519E8DD76FEF664B`.

Runtime/tool path used:
`C:\Users\LostSoul\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`.
Header parser root: `G:\Projects\Codex\Rome at War AI\.analysis\replay_parser_kjir`.
Extraction: repository `tools/analyze_replay.py`, external
`audit_writer_replay.py --plain-runtime`, then `audit_t16_dispatch.py`.
No engine pathfinding simulation or all-player private-chat completeness claim.

## Authorized follow-up — T17:464 implementation, 2026-08-31

After the audit, the user authorized implementing and deploying its two dispatch
corrections. This does not retroactively make the T16 replay validate T17.

- Claim patch: revalidate the exact empty/idle/unowned/unattacked self hull;
  permit old native order IDs on such reusable empty hulls, but retain protection
  of moving, loaded and owned voyages. Acknowledgement of the exact group flag
  precedes boarding and scout-attempt consumption. Later preparation lease loss
  gets a bounded terminal recovery/yield, not a silent loaded-hull reset. This
  handler adds no STOP orders and does not manage committed voyage slots.
- Enumeration patch: scan literal player IDs1–8 with active/hostile predicates,
  running the existing two-point defense scan for every admitted enemy. Final
  manifest, scout, same-island, liveness and progress protections are retained.
  Codes401/402 now protect against corrupt scan cursors rather than reporting
  the removed engine iterator. The engine's original-1 result is not explained
  by inventing a wrong constant or an enemy resignation.
- Source T17:464 is89 runtime files, SHA256
  `E060FC4BF5B4ABCC71DCA63C29B00E88988346654149D1E125EAB73CE9A11C3D`.
  Immutable pre-edit T16 control: external
  `.analysis\p3b44t16a2-runtime-control.zip`,87-file payload hash as recorded above.
- **PASS:**346 full tests after correcting the stale scout-attempt assertion and
  rerunning with required Windows temporary-file access; PER, generator sync,
  strategy/naval validation,37 replay benchmarks; ownership audit758 sites with
  zero direct permission failures; string budget1447/1500. Actual-PER tests cover
  acquisition races, empty lookups, all three roles, other owners/native voyages,
  one-shot recovery, all eight player IDs, both danger points and useful partials.
- Both corrections are **FIXED-PENDING-RUNTIME**. Remaining T16 observation
  classes and the STOP defect remain OPEN/INVESTIGATING. See current HANDOFF for
  exact deployment receipt, reversal boundaries and next-match acceptance.
