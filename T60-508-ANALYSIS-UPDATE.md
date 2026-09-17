# T60 update of the 508 recording analysis (231130 replay + log)

Analysis of the ORIGINAL 508 recording, unchanged artifacts: replay
`9c7cdc2d…5ed459` (66:34, marker `RAWAI-P3B44T58B: 508`), engine log
`2026.09.12-2310.43`, frozen 508 registry
(`.analysis/deployment-t58b-508-20260912T200909Z/`). The repaired candidate is
NOT used here for any behaviour claim. New tool outputs are separate files; the
earlier v1 outputs are preserved.

## 1. Corrections to the earlier conclusions

| Earlier statement | Corrected finding | Cause of the change |
|---|---|---|
| "196,168 correlations are `indirect-recipients-unknown`" | 196,168 rows are **`no-expected-packet`** (192,863 state writes, 3,065 native-admission, 240 group writes). Only **1,628 rows (34 sites)** are genuine recipient gaps. | the old label conflated state/settings/admission writes with unknown-recipient commands |
| "0 of 38,259 order-706 packets fall inside a traced bracket" | **9** packets do (sites 1192/1199/1202/1205 = `rawai-homebase.per` `up-target-objects … action-default`). The conclusion that the scripted stop/reset writers do not explain the stream stands, but "zero" was an artefact of the missing target/second-boundary rules. | command-contract target matching + one post-invocation second |
| "the 706 producer cannot be named" (timing only) | All five sustained runs begin in the same second the actor's traced state becomes `garrisoned=1` inside the hull; only 1.2 % of scripted boardings produce any churn, and 99.3 % of all 706 packets sit in those five runs. | actor state records (type 21) + boarding/actor join |
| "migration dropsite never reached `status-ready`; diagnostic 579 = 0 observation" | The ready branch **did** execute: p2 ran `MIGRATION-CHECK-DROPSITE` → `MIGRATION-RETASK-DROPSITE` (site/command 1593) at 2971 s, then CHECK/ASSIGN-RETASK-ANCHOR and RELEASE-COLONY → IDLE. Diagnostic 579 is quota-gated chat, not the ready path. | traced command ids 1591-1593 in the frozen registry + records |
| "p7 aborted at RECALL-LOADING" | p7 explicitly hit **`MIGRATION-DROPSITE-FAILED`** (cmd 1567) at 3682 s, then recall/return — a failed dropsite validation, not an unexplained abort. | same trace |

Correlator corrections applied in `tools/command_boundary_log.py` are minimal:
contract-aware target/recipient requirements, one labelled post-invocation
second (documented 14-38 ms deferred delivery at whole-second resolution),
recipient categories, and `recipients-unknown` only when a recipient-bearing
command has no traced recipient rows. Corrected run:
`candidate-not-causation` 2,108; `ambiguous` 53; `unmatched-not-native-proof`
94; 76 candidates in the post-invocation second.

## 2. Issue table (evidence from the original recording)

| Issue | Evidence | First failure boundary | Conclusion | Smallest next action |
|---|---|---|---|---|
| `villager.order706` | 38,259 packets / 46,850 incidences; 5 sustained runs = 37,977 packets (99.3 %): p6 42361 (14,692), p6 33901 (11,636), p2 33923 (9,044), p7 7674 (2,471), p2 33889 (134). Each onset second is the actor's `garrisoned=0→1` transition inside the hull, after a scripted walk-to-hull (action 617 / order 717 / target = hull). 411 of 423 scripted boardings produced **no** 706 packets in the following 120 s. 9 packets match traced `action-default` sites; the garrison/stop sites that fired in those seconds (1303, 1706, 1738-1741) are `recipients-unknown`. | the flood is a loaded, **waiting** transport: the engine churns `AI_ORDER 706` for passengers while the hull sits garrisoned; scripted boarding packets are 2-9 per window, not thousands | **EVIDENCE GAP** (producer identity) + **BOUNDED EXPERIMENT** | record the DUC selection for the group-scoped garrison/stop sites (1303/1706/1738-1741) for one match, or hold one loaded transport for a fixed interval and compare its 706 rate |
| `diagnostics.command-boundary.t57` | all 8 players complete framed records, identity words match, 0 incomplete correlations | none | **OBSERVED SUCCESS** for delivery/identity at the file-trace boundary | none |
| Operand floods | 86,277 `up-can-build`, 3,001 `up-can-build-line`, 24,490 `up-get-point-distance` errors, all operand 0; also 4,273 `up-find-remote` focus −1 and 896 `up-set-offense-priority` invalid unit ids | literal-0 goal/point operands and unset focus | repaired here (see `T60-OPERAND-REPAIR.md`); focus −1 and offense-priority ids are separate and unfixed | runtime confirmation of the repair; separate bounded check for focus −1 |
| `migration.productive-dropsite` | admission true 463× across 8 players; p2 full episode 2857→2971 s with dropsite placement 2928/2949 s, ready/retask at 2971 s, release → IDLE; p7 placement 3679-3682 s then `DROPSITE-FAILED` 3682 s → recall/return; p6 twice `RETURN-FAILED`→`QUARANTINED` (3014, 3484 s); p5 twice RETURNING→IDLE | after confirmation the mission **retasks the anchor and releases the colony** (p2); p7's dropsite validation failed | **ACTIONABLE**: TC-independent admission confirmed working in 508; the dropsite is not the blocker | inspect the p2 retask/release path for whether a gathered/deposited resource is ever required, and the p7 `DROPSITE-FAILED` condition at cmd 1567 |
| p1/p3/p4/p8 migration | admission timer armed and triggered (65-98 snapshots each), outer mask 0 in most samples, yet state stayed `MIGRATION-IDLE` | the admission OR-block: with `gl-assault-admission-open=1` (578), `gl-ap-seed-enemy≥1` (577) and `gl-home-defense-state=0` (575), admission requires `t-transport-route != triggered` — the one input not recorded | **EVIDENCE GAP** (one field) | record `up-timer-status t-transport-route` in the admission fingerprint; then decide whether the assault-channel veto is intended or over-broad |
| Assaults | 21 hulls have boarding retries plus a recorded unload. Hull (p8, 7645): 573 boards over 1425-3382 s, 232 unloads; first board→unload 52 s; the boarded actors then produced 259 WORK, 24 AI_ORDER, 21 SPECIAL, 15 STOP, 6 ORDER, 2 BUILD packets in 180 s → successful-looking unload with productive land activity. Hull (p6, 46455): 435 boards at 3858-3979 s with no unload (match ended); hull (p6, 34251): 22 boards 661-795 s, no unload. | packet orientation: `SPECIAL` order 5 = garrisoning *unit* → hull; `UNGARRISON` object = hull (target = leaving unit or a point). Actor-side joins across the two families are invalid. | **PARTIAL**: unload with follow-up activity observed; per-mission manifest/voyage/land-combat reconstruction not performed | one mission reconstruction using hull-keyed joins (hull ids above) with manifest and landing evidence |
| `merchant.row.real-choke` | ROW sampler ran for all 8 players (1,232-1,307 samples per id); 618 = selected hull, 619 hold reason (−1 none 831, 621/610/614 rejections), 621-622 merchant counts, 623-624 zone/eligible counts; 318 "merchant land proof ally"/"trade land candidate ally" chats, **all from p1** (780-3992 s) | priority hull and hold reason recorded | **PARTIAL**: sampler coverage confirmed; no yield → hull-progress → merchant-resumption chain reconstructed | one hull-keyed chain from the 618/619 records plus trade-cog progress |
| Reactive skirmishers (`production.reactive-skirmisher.t56`) | no diagnostic id in 508 references queues/skirmishers/threats; the generator emits no diagnostics | — | **ANALYSIS PENDING**: needs unit-id-resolved production packets, not diagnostics | count train/queue packets per player for the skirmisher line |
| `help.exact-episode.t53` | ids 300-317 = 0 observations; 202 resource-request chats and 9 tributes | — | **NOT EXERCISED** (threat-help episode absent; the resource-request path ran) | a match containing the ally-help request/silence episode |
| Allied-base landing fallback, `villager.keystates.t53`, `expedition.commitment` | no ally-base/allied-mode records; no Ctrl experiment; no expedition commitment evidence | — | **NOT EXERCISED / ANALYSIS PENDING** | trigger and record separately |

## 3. Precise remaining gaps (cannot be answered from this recording)

1. **DUC selection for group-scoped commands.** 1,628 rows across 34 sites are
   `recipients-unknown` because the file trace snapshots search lists, and the
   group-scoped `up-target-objects 0 …` / `up-target-point position-self-x …`
   sites (1303, 1706, 1738-1741, 1192-1205) consume the current selection
   instead. Missing field: the selected/group object list at PRE time.
2. **Transport-route timer status at migration admission.** The admission
   fingerprint records five of the six OR-block inputs; `up-timer-status
   t-transport-route` is not among them.
3. **Dropsite object identity and status transitions.** The ready branch is
   visible, but the dropsite object id and `status-pending → status-ready` are
   not recorded per actor, so physical completion cannot be separated from the
   controller's recognition.
4. **Movement/completion claims stay unproven**: packet presence is not task
   success, and no collision between two independent fires had to be resolved.
   Command packets cannot establish gathering, deposits, landings or combat.
