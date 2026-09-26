# T64 — first runtime results for the operand-repair payload (509)

Match: `SP Replay v101.103.48987.0 @2026.09.19 202909.aoe2record`
(sha256 `94c810b49127e6325263fad2aad2ddb5d67cdbce02fb3645be91672e29789743`,
66:48 simulation) with the engine log `logs\2026.09.19-2026.52\MainLog.txt`
(378 MB, 28,952,641 lines). Eight AI RAW players, teams 1-4 vs 5-8, same
civilization slots as the 508 recording. Analysis only; no runtime file was
changed after the deployment.

## 1. Payload identity — the deployed candidate ran

| Check | Result |
|---|---|
| Replay marker chats | **`RAWAI-P3B44T58B: 509`** (players 6, 7, 8) |
| Log source-identity words | all 8 players equal the installed 509 manifest words; `registry_matches_manifest = true`, `identity_mismatch_players = []` |
| File trace completeness | 1,127,416 complete records, 0 malformed/truncated/abandoned; all 8 players in startup, multi-actor and boarding entries |
| Decoder | replay decode with no failures; 364,787 events, 81,667 paired diagnostics |

## 2. Operand-repair acceptance — **PASSED at the engine boundary**

| Family | 508 (broken) | 509 (deployed) |
|---|---|---|
| `(up-can-build): Invalid goal used (…)` | 86,277, all operand `0` | **0** |
| `(up-can-build-line): Invalid goal used (…)` | 3,001, all `0` | **0** |
| `(up-get-point-distance): Invalid goal used (…)` | 24,490, all `0` | **0** |
| controls: `up-get-object-target-data` / `up-remove-objects` / `up-find-remote` / `up-set-offense-priority` | 44,076 / 12,302 / 4,273 / 896 | 45,276 / 4,273 / 3,978 / 896 — all still present |
| repaired sites exercised | 37 of 63 reached (5,886 invocations) | 36 of 63 reached (3,260 invocations) |

The three repaired error families are gone while the unrelated families remain,
so the log is comparable and the script ran its normal workload. The **shipyard
sampler also changed behaviour in the expected direction**: reason 64 ("cannot
build here") fell from 6,186/7,139 samples (86.65 %) to 4,150/8,112 (51.18 %),
and **reason 63** — the remembered-site freshness branch that depends on the
repaired `up-get-point-distance` — now fires 3,415 times after never appearing in
the 508 top codes. Shipyard foundations/ready confirmations and the remaining
placement questions still need the dedicated placement assessment.

Other observations from the same match, reported without attributing them to the
repair (different match, different conditions): order-706 packets **38,259 → 4,631**;
migration reached `MIGRATION-MISSION-MINING`/`HULL-VERIFY`/`OWNERSHIP-CLAIM`
states and issued 7 `ISSUE-DROPSITE` diagnostics (0 `CHECK-DROPSITE`); the
dropsite-failed boundary (command 1567) was **not exercised** in this match, so
the p7 failure boundary from 508 remains open.

Unexercised repaired sites (27 of 63 in this match, 26 in 508): ids 1042, 1174,
1181-1190, 1194, 1208, 1218, 1221-1223, 1226-1227, 1231, 1240, 1253, 1567-1569 …
— an unexercised call is not evidence of success.

## 3. Reported defect: Yellow repeated the attack-taunt response 184 times

Evidence (player 4 = Yellow):

* `chat-to-allies "39 Yes my liege, attacking now"` (`rawai-tauntcommands.per:60`)
  appears **184 times**, all between **3906 s and 4007 s**, gap median **1 s**
  (min 0, max 1) — i.e. every AI tick for the last 101 s of the match.
* The handler's own trace site **1829 was invoked 184 times** (368 PRE/INVOKED
  records, one pair per tick, seconds 3906-4007 with 1-second spacing), all for
  player 4 — so this is a rule re-firing, not repeated taunts being answered.
* `chat-local-to-self "land attack, response to taunt 31"` never appears in the
  replay (self-chats are not delivered to the recorded chat stream), so the
  visible spam is the ally chat from the same rule body.

Root cause (source): the handler detects and acknowledges with **different
scopes** —

```
(taunt-detected any-ally 31)          ; gate (rawai-tauntcommands.per:6)
...
(acknowledge-taunt this-any-ally 31)  ; action (line 13)
```

The taunt fact is therefore not cleared, and the rule re-fires every tick while
its other two guards hold (`gl-home-defense-state NO`,
`gl-transport-route-state TRANSPORT-ROUTE-IDLE`), which is exactly the 3906-4007 s
window. The same file already shows the project's working convention for taunt
48: detect **per player** and acknowledge the same player —
`(taunt-detected 1 48) … (acknowledge-taunt 1 48)` (lines 133-155).

**Status: ACTIONABLE DEFECT (source side, not fixed here).** Smallest justified
change: detect and acknowledge taunt 31 per player 1-8 as taunt 48 does (or use
the identical scope in `acknowledge-taunt`), optionally with a one-shot latch so
a pending taunt cannot re-assert the attack posture every tick. Nothing was
changed: this needs its own authorization, and the fix should be re-verified in
a match.

## 4. Reported defect: Yellow's loaded transports never yielded to a blocking transport

Evidence: the naval right-of-way pipeline in this match
(`rawai-naval-right-of-way.per`, executed 509 source):

| Stage (diagnostic ids) | 508 | 509 | Yellow (p4) in 509 |
|---|---|---|---|
| selection of a transport (580-585) | 1,317-1,326 | 1,530-1,532 | 63 samples |
| stall samples (586-590: hull, moved, turned, distance, stalls) | 114-115 | 189 | **36 samples**, hulls 35202 (15), 35255 (10), 35164 (8), `moved = 0` in 23 of 36 |
| merchant-lane stage (591-596) | 18-19 | 14 | — |
| rejected candidate (617-624) | 1,232-1,307 | 1,347-1,403 | 24 |
| **hold (625-630)** | **0** | **0** | — |
| **issue (631-637)** | **0** | **0** | — |

Two gates upstream of the hold stage both fail in practice:

1. **The consecutive-stall counter never reaches 2.** Every one of the 189 stall
   samples prints `gl-row-stalls = 0` (Yellow: 36 of 36), i.e. each sample is a
   *first* stall of a fresh monitoring window; the counter is reset when a
   candidate is selected (`rawai-naval-right-of-way.per:248-260`). The gate that
   would continue towards the yield decision is
   `(goal gl-row-stage 4) (up-compare-goal gl-row-stalls c:< 2) => stage 0`
   (lines 1411-1416).
2. **The merchant-lane check finds nothing.** In every sample that reached the
   merchant stage, all five merchant counts (592-596: raw, owned/free, safe,
   same-zone, eligible) are **0**, so the stage-5 transition
   (`up-set-target-object search-local c: 0`, line 1558) cannot select a merchant
   and the pipeline cannot reach stages 6-7.

So the observed behaviour is reproducible from the current design: the
right-of-way code watches *transport* hulls for stalls but only ever yields to
**merchant** traffic, and even that path never engaged in either recording
(0 of the hold/issue diagnostics in 508 and 509). Yellow's transport pair *was*
detected as stalled (`moved = 0`, repeat hulls 35202/35255) — the stall detector
works; there is simply no active transport-versus-transport yield to trigger.

**Status: BOUNDED HYPOTHESIS / possible design gap (not a broken assertion).**
Because the hold path has never executed in either recording, its behaviour is
unverified code. Two discriminating next steps, in order: (a) confirm whether
transport-versus-transport yielding is a requirement (it is not implemented —
the hold branch keys off merchants), and (b) if it is required, add the blocked
hull's own lane check before the merchant stage (a stall counter that survives
candidate rotation plus a transport-blocker test), keeping the existing
merchant-lane behaviour intact. No gameplay change was made here.

## 5. Status summary

* OPERAND REPAIR — **IMPLEMENTED AND RUNTIME-CONFIRMED at the engine boundary**
  (three error families at zero, controls intact, shipyard reason-64 share
  halved, dead reason-63 branch now live). Gameplay-level placement and
  migration outcomes still need their own assessment.
* Logging delivery / player identity — verified again in this match.
* Order-706 — reported (4,631) with the corrected tools; no attribution.
* Yellow attack-taunt spam — root-caused, fix pending authorization.
* Transport right-of-way yield — hold/issue path never executed in either
  recording; requirement question raised with the two upstream gates named.
* Migration dropsite-failed boundary (command 1567) and the 27 unexercised
  repaired sites remain unverified.
