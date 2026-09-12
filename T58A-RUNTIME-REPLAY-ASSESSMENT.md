# T58A/507 completed match: transport admission and trace identity

2026-09-12. Gameplay defects **INVESTIGATING**; diagnostic player identity
**FIXED-PENDING-RUNTIME**, local only. No deployment, commit or push this turn.

## Identity and reproducible evidence

- Canonical `.trade-work/T30-trade-cap-civ-fix`, branch `fix/trade-cog-cap-dacian`,
  HEAD `a635d5598a6d292a9571d14abd178b669189b345` plus preserved working changes.
- Replay `SP Replay v101.103.48987.0 @2026.09.12 133042.aoe2record` under the
  user's AoE2 DE savegame directory. SHA256
  `ff2dba2e61952b3cf4ed630901188d73e63b9a4f04ae57be674f7b484e20280e`.
- Duration 87:53.404. Replay-visible507 markers recovered for players6–8;
  do not invent missing startup messages for the other players.
- All109 installed runtime hashes rechecked against
  `.analysis/deployment-t58a-507-20260912T102708Z/manifest.json`: zero mismatches.
  Aggregate `9e3823727574792e3677321a1ca07a92f2e5f80144269844f0f967b0d7ac5969`.
- Final log: `logs/2026.09.12-1328.46/MainLog.txt`,374,667,099bytes.
- Corrected packet extraction has no parse failures. External artifacts under
  `G:\Projects\Codex\Rome at War AI\.analysis`: `t58a-exact.json`,
  `t58a-broad.json`, `t58a-file-log.json`, `t58a-file-log.records.jsonl`,
  `t58a-results.json`. Reducers: `t58a_extract.py`, `t58a_results.py`.
  Original replay, log, raw packet data and caches remain outside the repository.
- Header selected colors identify Blue=p1, Yellow=p4, Green=p3. Internal color
  metadata is a separate field. Match settings: Extreme,400population,
  normal1.69speed, shared exploration; preserve these for comparison.

## User observations and what is actually reconstructed

The user observed Yellow gathering an army at a strait without transportation,
and Blue/Yellow failing to migrate for exhausted/missing island resources.
These visible failures remain evidence. Finding an attempted mission is not a
successful delivery and does not disprove a separate native army stuck ashore.

### Yellow: loaded assaults reach planning, but repeatedly fail there

- Hull35296 entered an assault slot at **56:28.997**, saved enemy8. Replay
  ORDER765608 at56:29.024 sends it to(73,189). UNGARRISON781431 at57:08.347
  requests(89,137); another requests(85,137). Commands are not proof of unloading.
- At **57:56.123**, RAW3event2 records the source's hostile-damage recovery
  branch. Subsequent unload commands point to recovery(24,200). Event6 at
  **58:12.518** means the exact owned/group-filtered hull could not be selected;
  it does not alone distinguish death, ownership change, or group loss.
- Hull50457 has **eight full-ready records**, all target manifest10, at
  60:38.569,63:21.936,67:07.701,69:51.804,77:11.820,80:08.604,82:52.494,
  and87:34.095. It has no recorded slot-commit event. The last attempt is
  right-censored by match end, not counted as another completed abort.
- Exact SPECIAL870400 at **60:06.870** orders ten actors to garrison50457:
  53608,52692,47441,51114,48107,35134,7723,35235,35251,54748. Thus this subset
  of the shore gathering was explicitly transport boarding, not simply an
  attempted native land attack. It does not identify every shore-bound soldier.
- For50457, replay contains12 ORDER and15 UNGARRISON packets; recovery repeats
  at(42,209). Across Yellow's planner, reason counts are21:151,11:46,41:11,
  26:9,39:2,6:1,10:1. These are candidate/terminal records, **not distinct
  mission counts**. Source meanings:11 detected landing defenses;41 mobile
  land-egress witnesses could not reach the candidate;26 no remaining eligible
  opponent in the bounded search.21 is overloaded between coarse shoreline
  exhaustion and invalid candidate land/water zones; do not assign one meaning
  to all151 occurrences.

**Boundary:** Yellow's repeated50457 failure is downstream of successful
manifest admission/boarding and upstream of slot dispatch. There is no support
here for replacing the working boarding architecture or increasing its timer.
Whether a safe usable beach was omitted, incorrectly rejected, or genuinely
unavailable requires per-candidate geometry/threat/witness evaluation. The
defense/egress vetoes must not be removed merely to force departures. The
separate native land-army interpretation remains unresolved without matching
the observed group to exact actors/targets; no blanket conclusion about all
Yellow military follows from this one transport roster.

### Blue/Yellow: scout ferries are not resource migrations

Both early migration lifecycles carry **mission2 (SCOUT)**, not mission1(MINING):

| Player | Hull | First recorded rendezvous | Outcome visible in lifecycle |
|---|---:|---|---|
| Blue |35242|15:03.468|Waypoints/shore retries, returning17:05.714, idle18:22.099|
| Yellow |35296|15:33.389|Waypoints/shore retry, returning16:35.597, return-failed17:52.014, quarantined17:53.102, idle18:23.098|

No mission1 lifecycle is recovered for either player. This is consistent with
the reported absence of resource-colonist delivery, not evidence that those
early scouts provided a remote economy. Bounded chat cannot exclude every
transient planner entry or prove that resource eligibility never became true.

The admission snapshots expose a concrete later blocker:

- Blue first records mask128 at **40:23.893**; Yellow at **39:57.647**.
  Source128 is pending Town Center placement. Later masks include136
  (placement+route),144(placement+clearance), and occasional pending-foundation
  combinations. These are samples, not continuous-duration measurements.
- Source site1312 refuses migration admission for **any** pending Town Center
  placement/foundation, not only an actively owned colony-TC operation. Ordinary
  home expansion writer1174 can issue that normal Town Center request.
- Late samples show Blue with9–16 transports and Yellow with4–8; home-defense
  is0 in the displayed late samples. This rules out literal absence of all
  transports or a continuously asserted sampled home-defense gate as sufficient
  explanations. Counts do not prove an idle unowned usable hull exists.
- There are also zero-mask windows, so pending Town Centers do **not** explain
  the whole match. Inner age/resource/map/colony-threat gates, surviving filtered
  resource candidates, and available-hull ownership remain material boundaries.

No Town Center queue reset, migration admission bypass, or resource-tasking
change was made. The record does not yet identify which Blue/Yellow pending
request was stale versus live, nor prove that bypassing it preserves shared
placement ownership. Correctly identified all-player command traces are needed
to match the first gate failure to the requesting writer, target and queue state.

## All-player comparison (bounded observations, not success counts)

| Player | Migration mission types observed | Distinct lifecycle hulls | Full-ready assault records | Slot commits |
|---|---|---:|---:|---:|
|1 Blue|Scout|1|10|18|
|2 Red|Scout, mining|3|0|0|
|3 Green|Scout, mining|3|0|0|
|4 Yellow|Scout|1|8|1|
|5 Cyan|None in lifecycle messages|0|0|0|
|6 Purple|None in lifecycle messages|0|0|0|
|7 Gray|Mining|5|0|0|
|8 Orange|Mining|1|0|0|

Full-ready messages do not include every useful-partial acceptance; Blue's18
commits therefore need not equal its10 full-ready messages. Blue emits16
landed-combat handoff events8; those alone do not prove productive attacks or
correct landmass. Gray has three rendezvous-start/ready pairs23/24 and three
terminal planner reason26 records, without a slot commit. Other players'
mining attempts are not proof of a completed drop-site plus gather/deposit.
No new acceptance of migration productivity, native land combat, or expedition
utilization is declared from these totals.

## Proven diagnostic defect: FactId/player-domain confusion

207,244 complete checksummed frames were decoded. Every prefix isRAW58P1,
session117144; however **all956 local object rows report owner3**. Hull35435
and its timing also match Green's replay migration, not Blue's35242.

The installed bootstrap is:

```lisp
(up-get-fact my-player-number 0 gl-cbf-player)
```

Cached AIRef defines the first parameter as **FactId**, not PlayerNumber.
FactIds1/2/3/4 are population-cap/population-headroom/housing-headroom/idle-farm-count;
5–8 are resource amounts. For Green, player constant3 therefore queries housing
headroom and stores1. Its initial frame label is consequentlyRAW58P1. Other
players can get values outside1–8, for which the emitter has no branch. This
also corrupts private roster ownership filtering. A valid checksum does not
validate player attribution. Historical decoded `player:1` remains the raw
wire label and must **not** be joined to Blue's replay commands as actual owner1.
Do not rewrite original logs or globally relabel them without object evidence.

### Narrow implementation

`tools/command_boundary_file.py` now emits:

```lisp
(set-goal gl-cbf-player my-player-number)
```

Generated `rawai-command-boundary-private-init.per` is the **only functional
runtime difference** from installed507 after regeneration. The separate
`rawai-init-goals.per` candidate marker becomes `RAWAI-P3B44T58B:508` so the
uninstalled correction cannot be mistaken for507. No gameplay actions, selections,
keystates, ownership, deadlines, economy or transport gates changed. The new
eight-player bootstrap test executes emitted initialization, verifies unchanged
gameplay objects/searches, correct frame prefixes and roster enrollment. Older
tests had injected player1 and missed this actual bootstrap bug.

Working behavior at risk:507's compact emitter, framing/checksum compatibility,
private-state isolation and physical rule capacity. Preserve those fixtures.
All-player output volume may increase materially once suppressed players log;
measure engine cost and file growth in a bounded smoke test, not an unobserved
long match. This correction is **not yet deployed or runtime accepted**.

## Other engine errors remain unresolved

Final exact counts: age1=3,836,427; age2=4,156,519; age0=84,255;
goal0=166,522. First lines13573/13574/13581/13725 precede first complete frame.
The player-domain correction is not claimed to explain these per-sweep floods.
The standalone17-case probe in `T58A-RUNTIME-OPERAND-ERRORS.md` remains prepared,
not installed; no blanket numeric-age/zero-sentinel changes are justified.

## Validation and next actions

- Focused file-trace suite including bootstrap:18tests PASS (temporary-file
  fixtures require execution outside the filesystem sandbox).
- PER validation and generated-source synchronization PASS. Source-vs507
  comparison confirms only the diagnostic initializer and candidate marker differ. No new rules,
  strings or goals; the9252/10000 conservative capacity bound remains intact.
- Intermediate full runs exposed hot-context size(30,034bytes), a required
  preservation sentence lost during compaction, and stale hardcoded507 markers.
  Hot state was shortened, the sentence restored, and two marker checks now
  read authoritative candidate identity. No acceptance check was removed or cap
  increased. Final Python3.12 discovery: **663run,661PASS,2retired skips**,
  96.907seconds. Context metadata and `git diff --check` PASS. Final hot state
  is below30KB. Installed109 files rechecked again: zero changes.
- Runtime:507 played a full87:53match, but trace identity/all-player coverage,
  operand-error health, Yellow dispatch and Blue/Yellow resource migration fail
  acceptance. Static passes do not close any of these gameplay defects.

Next: bounded engine validation of the corrected identity and standalone operand
probe when authorized; then correlate Blue/Yellow's first resource admission
failure and Town Center request with actual player-tagged records. Evaluate
Yellow's failed candidate coordinates/threat IDs/egress witnesses before changing
landing selection. Preserve all existing safety and installed experiments.

Read-only falsification review: a captured enemy in one local list would not
prove mislabeling, but all956 rows show owner3 and known Green hull timing also
matches. The bootstrap independently selects FactId3, explaining that result.
Conversely, a pending-TC sample does not prove uninterrupted starvation, a
landing threat count does not establish exact threat range, and an unload
packet does not prove troop delivery. Those stronger gameplay claims are
explicitly rejected; no behavioral patch follows from them.
