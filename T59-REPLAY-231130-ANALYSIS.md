# T59 replay/log analysis — 2026-09-12 231130 (508 runtime)

Analysis only: no gameplay edit, no deployment, no instrumentation, no test
suite run. Offline scripts added under `<project>\.analysis\t59_*.py` (outside
this repository); no repository tool was modified for this analysis.

## 1. Artifacts and executed payload

| Item | Value |
|---|---|
| Replay | `SP Replay v101.103.48987.0 @2026.09.12 231130.aoe2record`, 56,685,524 B, SHA256 `9c7cdc2d…5ed459` |
| Log | `logs\2026.09.12-2310.43\MainLog.txt`, 383,231,179 B, 29,156,832 lines |
| Game build | 101.103.48987.0 (180059), Retail 2026-06-25 (log header) |
| Replay length | 3,993,996 ms simulation = 66:34 |
| Players | 8, all `ai_name = AI RAW`; numbers 1-8 = colors Blue, Red, Green, Yellow, Cyan, Purple, Gray, Orange; teams 1-4 = team 2, 5-8 = team 3 |
| Payload identity | replay chat markers `RAWAI-P3B44T58B: 508` (players 6, 7, 8) + RAW58 file-trace identity words for all 8 players equal the 508 deployment manifest words; `registry_matches_manifest = true`, `identity_mismatch_players = []` |
| Installed bytes | 109/109 files still match `.analysis\deployment-t58b-508-…\manifest.json` (0 missing, 0 mismatched) |

What ran is the 508 payload with the deployed registry; current source equals
that payload for every runtime `*.per` (no gameplay file was touched after
deployment). The declared 508 changes (TC-independent migration admission,
four-TC cap, allied-base landing) are therefore live in this match, and their
absence in older replays is not evidence against them.

Log/replay alignment: the log spans 20:10:43Z-20:52:17Z wall (41.6 min) while
the replay is 66:34 simulation; simulation time is not wall time. RAW58 records
carry `game_seconds`, which is what all cross-artifact joins used.

## 2. Evidence quality (RAW58 file trace, all 8 players)

- 1,130,143 complete framed records; **0** incomplete, 0 abandoned, 0 orphan
  tokens, 0 oversized, 0 invalid-length, 0 truncated tails, 0 record gaps,
  0 checksum/serial/tail errors (stats counters absent = zero).
- `startup_players`, `multi_actor_entry_players`, `boarding_entry_players` =
  [1..8]; `missing_players` = [].
- 200,051 PRE→INVOKED correlation rows; `incomplete-inputs` = 0, so no paired
  bracket lost its PRE/INVOKED identity. 196,168 rows are
  `indirect-recipients-unknown` (group/list commands: the trace records the
  site, not the recipients), 2,145 `candidate-not-causation`, 1,711
  `unmatched-not-native-proof`, 27 `ambiguous`.
- Replay side: 255,227 ORDER, 246,229 WORK, 49,468 AI_ORDER (38,259 of order
  706), 946 UNGARRISON, 1,746 SPECIAL, 93 STOP — decoded with the
  repository decoder for the current build; no decode failures (`failures []`).
- Log cost: 28,638,869 RAW58 token lines, 9.2 MB per wall minute (≈1.66 GB per
  3 wall hours). Presence of a record is evidence the writer ran, not that the
  engine accepted or completed the command.

## 3. Active issues — decision table

| Issue | Match evidence | First failure boundary | Evidence sufficiency | Narrow next action | Runtime confirmation still needed |
|---|---|---|---|---|---|
| `diagnostics.command-boundary.t57` (all-player delivery / attribution) | All 8 players emitted complete startup/entry/boarding frames; identity words match; 0 incomplete correlations | none observed — the previous "all-player delivery open" symptom is absent in this family | **OBSERVED SUCCESS** for file-trace delivery + player identity; the old chat-attribute path is retired | none | none for this family; keep it distinct from the operand floods below |
| `villager.order706` | 38,259 distinct 706 packets / 46,850 actor incidences (p6 21,578, p2 9,770, p7 2,943); 5 dense runs (≤1 s gaps, ≥100 packets); biggest p6 actor 42361 = 14,692 packets over 8.7 min; peak ≈3,000 packets/min at 50-61 min; every player's first 706 at exactly 25.024 s | all 5 dense-onset actors were boarded (`SPECIAL` order 5, target = hull) 0.01-4.0 s before their 706 run; 0 of 38,259 packets fall inside any traced bracket, and no traced stop/reset writer is nearby | **EVIDENCE GAP** for producer identity + timing-only link to boarding | One discriminating observation: capture recipient/actor identity for the same-second group garrison/unload site (indirect args stay -2 today), or suppress the repeat garrison for already-garrisoned passengers for one match and compare 706 onsets | yes — the log cannot name the issuer of an unbracketed packet |
| `shipyard.sampler.t51` | 7,139 sampler fingerprints; reason codes 64 (6,186), 62 (599), 65 (256), 66 (60), 67 (38); reason 64 is produced by `(not (up-can-build-line 0 gl-shipyard-x c: shipyard))`; that call plus 4 `up-get-point-distance <mem-x> 0 <dest>` calls produced 24,490 + 3,001 engine "Invalid goal used (0)" errors | the rejection decision itself is computed from an operand the engine rejects: the literal `0` point/goal operand | **ACTIONABLE CORRECTION** (operand), independent of map geometry | `rawai-specialplacement.per:792,809,826,843`: replace the literal `0` point operand with the current candidate point (`gl-shipyard-x`, which the preceding `up-set-target-point` already selects); audit the `up-can-build-line 0` site under the agreed no-escrow goal | yes — placement/completion after the operand fix |
| `migration.productive-dropsite` | Admission condition true 463× across all 8 players; admission mask nonzero in 85/547 samples; episodes only for p2/p5/p6/p7. p2: RENDEZVOUS 2857 → LOADING → SAILING 2907 → PLACE-DROPSITE 2926 → VALIDATE/WAIT 2927-2949 → CONFIRM-DROPSITE 2950 → IDLE 2971, with a 584-class dropsite placement at (170,135) 2928 s and (176,129) 2949 s; `gl-colony-towncenter-state` (574) = 0 for every player; p7 placed a dropsite 3679-3682 then went RECALL-LOADING 3683; p6 twice ended SHORE-CANDIDATE → RETURN-FAILED → QUARANTINED (3014, 3484); p5 twice RETURNING → IDLE | dropsite never reached `status-ready`: the CHECK-DROPSITE diagnostic (579) never fired, so the confirmed foundation was never observed complete; p1/p3/p4/p8 never left MIGRATION-IDLE | **ACTIONABLE (TC-independent admission confirmed) + EVIDENCE GAP (dropsite completion)** | the 508 TC-independent admission fix is confirmed working (p2 confirmed a dropsite with colony-TC state 0). Next observation: dropsite object id, `status-pending → status-ready` transition and the assigned builder for p2 2928-2971 s and p7 3679-3683 s | yes — placement existed; completion/productive gathering is not established |
| Operand floods (engine log) | `up-can-build` 86,277 all operand `0`; `up-can-build-line` 3,001 all `0`; `up-get-point-distance` 24,490 all `0`; `up-get-object-target-data` 44,076 return -2; `up-remove-objects` 12,302 return -2; `up-find-remote` 4,273 focus -1; `up-set-offense-priority` 896 across 28 unit ids | the literal `0` goal/point operands (all three call families) | **ACTIONABLE CORRECTION** — same class the user already attributed to `up-can-build`; not rediscovered here, only quantified and extended to `up-can-build-line` and `up-get-point-distance` | implement the agreed immutable no-escrow goal for `up-can-build`/`up-can-build-line` and correct the point operand; keep `up-find-remote` focus -1 (4,273) as a separate bounded item | yes — engine error count and behaviour after the fix |
| `help.exact-episode.t53` (312-317 request/silence) | diagnostics 300-317 observed **0** times; only resource requests ("Critically low on gold/wood/food/stone", 75/45/26/34) occurred | not exercised | **NOT EXERCISED** in this match | none from this match | a match with the ally-help request/silence episode |
| `merchant.row.real-choke` | ROW sampler ran continuously (ids 580-585 ≈1,320 each, 617-624 ≈1,250 each); land-trade chats "merchant land proof ally" 215 and "trade land candidate ally" 103 | not yet reconstructed | **INSUFFICIENT FOLLOW-UP** | reconstruct one yield → hull progress → native trade chain for the player with 215 proofs | yes |
| `assault.shore-egress.t53`, `assault.voyage.t55b`, `assault.preparation.close-boarders` | boarding/unload heavily exercised: p6 692 board / 415 unload (661-3993 s), p8 722/284, plus `RAW plan` objective/enemy/retry and "empty transport no staging point" (82) | not yet reconstructed per mission | **INSUFFICIENT FOLLOW-UP** | reconstruct one loaded mission per player with manifest → dispatch → unload → land activity | yes |
| `production.reactive-skirmisher.t56` | not identified in this pass | — | **INSUFFICIENT FOLLOW-UP** | locate the queue-counter diagnostic family and count per player | yes |
| `villager.keystates.t53`, `expedition.commitment`, allied-base landing fallback | no Ctrl experiment; no observed ally-base/allied-mode diagnostic | — | **NOT EXERCISED / NOT OBSERVED** | none from this match; do not infer absence of the fallback from non-triggering conditions | — |

## 4. What can be fixed now / what needs one more observation / what was not established

1. Fixable from this evidence: (a) the literal `0` point operand at
   `rawai-specialplacement.per:792,809,826,843` (24,490 engine errors and a
   sampler decision computed from an invalid point); (b) the already-agreed
   no-escrow goal for `up-can-build` (86,277) and `up-can-build-line` (3,001),
   where the shipyard generator's dominant rejection code 64 is itself a
   `up-can-build-line 0` verdict.
2. Needs one bounded observation: dropsite `status-pending → status-ready` plus
   the assigned builder for p2 2928-2971 s and p7 3679-3683 s (migration
   productivity); recipient/actor identity for the same-second group
   garrison/unload site (order-706 producer).
3. Not established here: whether order 706 is scripted or native; that the
   migration colonies gathered or deposited; landing and land-combat outcomes of
   individual assault missions; merchant right-of-way chokepoint behaviour;
   reactive-skirmisher queue coverage; the ally-help episode; allied-base
   fallback; and all engine-internal claims. Diagnostics, packet counts and
   issued commands are not completion proof.
