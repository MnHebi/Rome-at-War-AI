# Matched boarding contacts and command-boundary observations

2026-09-08. Continuation of `PROMISORY-RAW-ONSET-VERIFICATION.md`, not a new Promisory audit.

**INSTRUMENTATION READY — PENDING RUNTIME EVIDENCE**

**VILLAGER ORDER706 — INVESTIGATING**

No gameplay repair, deployment, cleanup reconciliation or native-gathering replacement is enabled by this task.

## 1. Identity and scope

Canonical: `G:\Projects\Codex\Rome at War AI\.trade-work\T30-trade-cap-civ-fix`, branch `fix/trade-cog-cap-dacian`, base `f6f1b5bcc53f63d6cec7386eebf658c58b402206`. The user subsequently authorized committing/pushing all pending work to PR11. This report now includes the reserved-sampling revision in `BOARDING-SAMPLING-COVERAGE.md`; the earlier uncommitted-review comment is historical. Boarding/marker work is preserved, with the separate pending ranged-counter correction included for review. No branch/worktree/overlay or deployment.

Keep these identities separate:

| Identity | Evidence |
|---|---|
| A: historical T56 payload | Marker504; recorded103-file aggregate `FB515FA0A52859BCC677353D7B06B38792DC6DAF4C03604AA793EBF30D707730`. |
| B: intentional installed experiment | Verified unchanged once this task: `60E05CFF142D948134C0693674CD37F8B851EE297CD40351D9DAB27B8576895C`. |
| C: canonical instrumentation candidate |108 runtime files; manifest aggregate `0d14e9ff7eb639abc415134753ebea9d11358e6ecf891b93197ed2876f5d0bc2`. NOT deployed; marker504 unchanged and insufficient to identify C. |

C's per-file SHA-256 manifest is external project evidence:
`G:\Projects\Codex\Rome at War AI\.analysis\command-boundary-candidate-20260908.json`.
Its explicitly defined aggregate is SHA256 of LF-joined, lexically sorted `filename:lowercase-file-SHA256` lines, without a final LF. Use the file map rather than assuming different manifest aggregate formats are interchangeable.

B deliberately adds de-game/wk-game definitions, removes the missing-target cleanup STOP while retaining counter1, and DE-guards counter2. These edits were neither reverted nor copied into C. **Counter1 in B means evaluation, not STOP issuance.** The already completed in-memory reconstruction of A was not repeated. Future deployment requires an explicit decision about B and a fresh payload identity.

## 2. Matched comparison method

Reused root `.analysis/t55b-exact.json` and `t56-exact.json`, their existing onset audits, and the corrected length-verified actor decoder. No replay re-decoding. Replay hashes:

- T55B @2026.09.07 121439: `632D89F42B339B06E6B83EF9A58F1FE7855EED9DB22DD3A200B2DDDA4A005858`.
- T56 @2026.09.07 144755: `708AF267E74E6E77F5984F8FAE2AB9E8C94D15BA82683768185BE51F01491B5A`.

New reproducible tool: `tools/compare_boarding_contacts.py`. Outputs:
root `.analysis/t55b-matched-boarding.json` and `t56-matched-boarding.json`.

A contact is a decoded SPECIAL subtype5, keyed by player+actor and exact target hull. Duplicate actor IDs within one packet count once. First means **first observed eligible contact**, not the worker's lifetime first command. Same-hull and different-hull classification uses the preceding eligible contact; long gaps remain explicit.

Follow-up is30,000ms. A sustained burst retains the established definition: at least100 AI_ORDER706 packets, splitting at interpacket gaps above1,000ms. Ordinary ORDER, WORK, SPECIAL and explicit STOP are separate. Isolated706 is not silently made a sustained burst.

A quiet window must have complete replay follow-up AND a later command observation of the same player/actor at or beyond its end, with no earlier explicit DELETE. Otherwise it is censored, not a negative control. This conservative check cannot reconstruct every intervening engine ownership/lifetime change; no absent command is treated as a witnessed boarding success. Positive onset evidence remains positive even if later follow-up is incomplete.

Identity cohorts:

- T55B: within previously affected actors with independently recorded migration hull IDs552/563. This is outcome-selected, not a population incidence estimate.
- T56 adds peers selected independently of706: complete mining-only writer700–705 headers20/21/23/24/25, modifier2, uniquely matched within100ms to exact SPECIAL5 hull/player/array length. There are72 such packet links. Candidate goals alone do not establish outgoing actors.
- Unresolved/out-of-cohort garrison actor incidences excluded:17,910 /15,386. These include other command families; they are not a count of failed migrations.
- Existing telemetry cannot establish every historical command's exact stage or physical position.

## 3. Denominators and result

Counts below are **actor-command incidences**, not unique commands, independent trials, or completed transports.

| Replay / contact | Sustained onset within30s | No706 with full follow-up | Isolated706 | Censored |
|---|---:|---:|---:|---:|
| T55B first observed hull |7|10|0|0|
| T55B same hull |53|82|0|0|
| T55B different hull |1|1|0|0|
| T56 first observed hull |3|95|0|0|
| T56 same hull |51|658|1|14|
| T56 different hull |0|8|0|0|

T55B:154 incidences /66 unique packets /17 actors. T56:830 /108 /98. No already-active-burst contacts occur in these eligible cohorts; the classifier explicitly supports that category. This does not exclude such commands in unresolved/out-of-cohort data.

The narrower T56 **exact mining-writer-linked packet subset** has628 incidences: first2 onset/56 quiet; same38 onset/516 quiet/10 censored; different6 quiet. Thus the quiet-renewal result does not depend solely on working backward from known floods.

Typical same-hull spacing is practically indistinguishable:

| Replay | Onset-associated median spacing / prior renewals | Quiet median spacing / prior renewals |
|---|---|---|
| T55B |3.320s /4|3.3115s /5|
| T56 |3.307s /4|3.313s /4|

Nearby WORK within ±5s occurs in4/53 onset-associated vs14/82 quiet T55B renewals, and13/51 vs158/658 T56 renewals. These overlapping windows are descriptive, not effect estimates.

**Finding:** same-hull renewal is common without a nearby sustained flood. Neither renewal presence nor its normal cadence isolates a causal defect. Blanket renewal suppression is unsupported.

## 4. Representative matched timelines

Times are replay elapsed seconds; all listed quiet examples have complete30s actor follow-up.

| Case | Observable sequence / boundary |
|---|---|
| T55B Cyan43834 →39461 |5543.621 first;5548.052 renewal (+4.431s); first7065549.578. The last stage550 is86 but approximately395s old: not current-stage proof. No paired positions or contemporaneous actor state. |
| T55B Gray35104 →35263 |2325.113 first;2328.915 renewal (+3.802s), no706 through2358.915. No WORK/ORDER/STOP ±5s for this actor. Latest stage76 emitted3.287s earlier, not a fresh physical state sample. |
| T56 Yellow34730 →35010 |Renewals2219.255,2222.540,2225.795,2229.078,2232.338,2235.628,2238.884. Ninth renewal at2238.884; first7062238.899; WORK→343482238.925. |
| T56 Blue34834 →38342 |2583.411 first;2586.667 renewal (+3.256s), no706 through2616.667. Post-state record emitted2586.646: action617/order717, intent38342, not garrisoned, carry0, group11. Its shared clock stamp is2583, not fresh precise time. Enter intent is not movement. |
| T56 Green34564 →40020 |3617.563 first;3620.844 renewal; onset3627.901 precedes the next writer24 report3627.970. That later report cannot explain first onset. |
| Same Green actor, different hull45544 |4323.213 assignment;4327.069 renewal (+3.856s);4334.151 renewal. All are quiet30s contacts. A post-record emitted4333.026 still names actual intent40020 despite reservation45544; stale shared time4327. This is a mismatch lead, not proof of a writer causing the old flood. |

Yellow's most recent available post-state at final renewal is21.282s old by emission time: action617/order717, actual target35010, not garrisoned, carry15, group11. It cannot establish progress immediately before2238.884.

Only39 T56 contacts have any preceding actor post-state; none meets the conservative freshness requirement of both emission age and shared-clock age ≤1s with matching hull. Two emissions alone looked ≤1s fresh, but the old shared-clock stamp was stale. Store both ages rather than pretending one is exact acquisition time. T55B has no equivalent actor post-state coverage.

Gaia fish34348/34395 are type69 FISHS, DAT class33, established by the prior authoritative-object audit. AI_ORDER706 targets−1, not those fish. WORK precedes706 for Red34616 but follows it in Yellow examples. The WORK producer remains unassigned. Green's late quiet renewal has nearby ORDER34549 and WORK4036/4107/4121/4154/5510/5511; their IDs are retained, not relabelled as witnessed resource productivity.

The earlier result—no explicit actor STOP before/during34 sustained bursts—is retained. It weakens direct cleanup-STOP attribution, not all competing-task hypotheses. The Promisory ZIP remains a reference snapshot, not an independently version-verified or flood-free runtime control.

## 5. Canonical observation changes

Authoritative registry: `command-boundary-registry.json`; generator: `tools/generate_command_boundary.py`.
Shared RAW12 numeric IDs720–772; private goals15869–15971. No new diagnostic message text.

### Boarding

Five existing mining-only Ctrl sites20/25/21/23/24 are observed immediately before their original `up-target-objects 0 action-garrison -1 stance-no-attack`. The original modifier2 and reset0, selections, carry policy, ownership, deadlines and cadence are preserved.

Each detailed invocation records player (chat sender), command serial, site/family, fresh game-time, actual modifier, local/remote counts, migration stage and reserved hull. Target0 supplies actual ID/type/class/player/group and precise x/y. Each of up to two distinct tracked actors supplies exact final-list index, ID/type/class/player/group, x/y, action/order/actual intent/garrison/carry and distance to hull.

Two previous banks retain actor/hull IDs, fresh time, both positions and ownership. Quiet captures between reports search up to32 final-list members for the **same prior actor**; do not assume list order is stable. Found1, fully searched absent0, first/partially searched−1 are separate outcomes. Rotate base index by two after a report, then follow the next pair quietly. A report includes the most recent private capture, not merely the last printed sample. Duplicates after list changes do not inflate coverage.

Valid offline progress requires:
same actor and exact reserved hull; exactly one target; valid positions; elapsed1–15s; unchanged self ownership; passenger group11 and hull group10; proven presence in the final outgoing list. Invalid/missing/old data is unknown. Actor displacement, hull displacement and separation are reported separately; straight-line improvement is neither required nor claimed to prove path progress.

### Resource/default writers

Thirteen inventory-selected sites are observed, including building/default paths whose actual targets could differ from their intended resource goal:

| Registry IDs | Source / scope |
|---|---|
|101–105|military: deposit, dropsite-clear, assign-dropsite, retask-anchor, transport-repair|
|106–111|homebase: colony TC, Lumber Camp, fisherman-farm, idle-farm, assign-farm, fisherman-resource|
|112–113|hunt: rescue phases6/7 defaults|

One rotating actor plus actual remote target0 is recorded **after all existing filters**. Intended controller goals are not used as actual-target evidence. If remote count exceeds1, remaining targets are explicitly uncovered. The exact decoded packet array is the authority for other recipients.

All other command families remain unchanged: non-mining/scout boarding, assault/relic boarding, movement, defense, explicit garrisons, STOP/release and native gathering. No new Ctrl application, stance change or `sn-number-forward-builders` change.

### Input and control-flow preservation

Several original rules approach DE's32-element limit. A registered rule evaluates its original predicates once, retains its original action order, calls a private synchronous read-only observer, then unconditionally resumes the original command/suffix. Logging allowance does not gate gameplay.

The generated bridge must exactly match its registered original SHA256 and generator output. Existing semantic ownership/strategy validators use this verified contract; raw PER validation and observer tests inspect physical rules. No semantic validator silently accepts modified bridges.

Observer APIs read final search state into a contiguous private block, read objects, select existing list indices and restore the saved selected-object pointer. No search reset/find/add/remove/filter, gameplay goal/strategic-number/group write, timer change or gameplay command occurs in the observer. Invalid saved pointers skip detail without mutation; failed object selection is not replaced with stale pointer data. Distance uses explicit coordinate pairs, not a shared target-point API.

Existing relative jumps are checked not to cross expanded registered rules. The library's normal traversal skips its body; a call returns to the immediate continuation. Fixture evidence demonstrates these contracts, **not engine scheduling or object lifetime during a native sweep**. Ordinary-match non-regression remains required.

Source files changed by this observation patch: `AI RAW.per`, military/homebase/hunt; four generated command-boundary PER files; registry/generator; observer decoder; matched analyzer/tests; exact semantic-bridge support in naval/keystates/PER validators and the economic adjacency test; synchronized modifier inventory; focused report/handoff/context. Legacy mixed line endings outside changes were restored without substituting old gameplay text.

## 6. Bounded output and coverage

Each player has independent boarding and default-writer allowances: four detailed command invocations per180 game-seconds, minimum3s between captures, rearmed only on actual nonempty command activity. Boarding now reserves one early report and one each at12/20/28s after local-loading writer21; travel cannot spend late credits. Quiet captures retain recent paired evidence without repeated output. New hull/start resets tracking, not credits. Defaults retain their original allowance. Empty calls do not spend detail credits. See `BOARDING-SAMPLING-COVERAGE.md` for executable historical timing, assumptions and uncovered cases.

Maximum new output per detailed command:
- Boarding:142 chat lines (16 header fields + two27-field actor pairs + end marker, two shared messages/field).
- Resource/default:62 lines (same header/end, one14-field actor).
- Coverage:20 lines/family, at most once/180s, only after calls have occurred.

Thus each anchored180s period permits at most856 new lines/player:4×142 +4×62 +40. Long-run upper bound about4.76 lines/game-second/player,38.05 across8 simultaneously saturated players. An arbitrary sliding180s interval can straddle two refill boundaries; conservative bound1,712/player. This is not per-frame/per-packet output. Existing diagnostics are additional, not included in this new-observer cap.

Tracking capacity is two boarding actors and one default-writer actor, not whole manifests. Resource writers cannot spend boarding credits. Aggregate counters retain calls, nonempty calls, suppressed calls, detailed calls, uncovered actor incidences, uncovered targets of detailed calls and invalid saved pointers. Suppressed/missed means unreported, including quiet-captured actors. With credits exhausted: no detail chats, original command still executes, bounded private captures continue, suppressed/missed counters increase and later coverage reports remain available.

Small pairs / changed manifests / multi-target arrays / consumed allowances may miss the affected actor at first onset. Report that explicitly; do not infer a native writer. Coverage counts are player/family totals, not a promise that every site/actor was sampled.

Measured string budget:1489/1500. Restoring this patch's original rules and excluding its four load paths gives1485, which includes the pre-existing undeployed ranged-counter work. The earlier1484 figure is historical, not current canonical. New diagnostic strings:0; new quoted load paths:4.

## 7. Offline joining and ordinary-match acceptance

`tools/command_boundary_observations.py CACHE OUTPUT` decodes720–772, retains incomplete frames, validates actor-paired positions and correlates actual player/actor/target packets within100ms. Multiple matches are ambiguous; no match is **unmatched-not-native-proof**. It records first706 within30s but never labels a command packet as task success.

Evidence levels remain separate:
1. site reached / invocation counter;
2. nonempty final selection and tracked actor;
3. matching decoded outgoing packet(s);
4. subsequent actor state and observed task outcome.

After future explicit deployment authorization, use an ordinary match with comparable settings; record a new marker/full file manifest and the exact choice about intentional cleanup tests. No special scenario substitutes for acceptance. For every actual flood onset:
- find whether its actor has a valid pre-renewal pair; separate passenger and hull motion;
- join exact outgoing arrays, writer/modifier and actual resource target, including uncovered writers/actors;
- order invocation, decoded command, retasking and first706 using sequence and milliseconds;
- reconstruct later boarding and ordinary resource gather/deposit, plus failures;
- include quiet matched contacts with adequate actor follow-up.

Presence of telemetry, quiet unrelated actors, entering intent or reduced aggregate706 count is not acceptance. If the actor is unsampled, the answer remains unknown.

Next experiment (specified only): omit a renewal solely when independent **functional** state proves a recently observed, still-reserved passenger entering the exact hull and a defensible bounded progress criterion. Keep normal bounded renewal/recovery for stalled, retasked or uncertain passengers. A useful detour must not be rejected merely for increasing Euclidean separation. Keep native gathering, Ctrl policy, cleanup variant, candidate selection and deadlines fixed between control/treatment. Do not use diagnostic sample membership as functional eligibility.

## 8. Validation and adversarial self-review

One owner performed a falsification-focused read-only review of the candidate:
- ACCEPTED: negative controls require later actor observation, not merely replay survival;14 T56 contacts now censored.
- ACCEPTED: old shared clock can be stale despite recent chat; retain both ages and conservative freshness.
- ACCEPTED: reordered lists can duplicate samples; distinct actor accounting and same-actor search tested.
- ACCEPTED: invalid selectors retain old pointers; guard successful selection and preserve unknowns.
- ACCEPTED: mixed-line-ending normalization obscured scope; formatting restored on unchanged text.
- REJECTED: blanket renewal suppression or cleanup repair as established706 fixes; data does not establish either.
- DEFERRED: native scheduling, ordinary-match boarding/productivity and first-onset coverage; no engine acceptance claimed.

Fresh validation (2026-09-08):

| Check | Result |
|---|---|
| New command-boundary fixtures |15 PASS: generated-library execution, actor/hull pairs, stale identity, exact final targets, rotation, invalid selectors, bounds, pointer/list preservation, ordered source contracts and control-flow jumps. |
| Reserved-sampling fixtures |6 PASS: known windows/model vs generated PER, unchanged cap, quiet fresh pairs, unknown historical lists, invocation-only calls, carry-in exhaustion, Green coverage gap, travel exclusion and reset without refill. |
| Matched-contact fixtures |6 PASS; exact actor/player grouping, first/repeat/different, sustained/isolated/already-active, packet/incidence counts, replay/actor/deletion censoring. |
| Existing boarding / economic / writer-trace suites |7 /9 /17 PASS. |
| Final full Python3.12 discovery |**625/625 PASS**,57.038s, normal Windows Temp access. |
| PER structural/operand validation |PASS, no issues; actual physical generated rules checked. |
| Ownership |PASS,1,052 relevant sites,0 direct permission failures. |
| Modifier policy |PASS:4 economic +5 mining Ctrl wrappers;75 explicit inventory entries. |
| Boarding and command-boundary generators |PASS, synchronized. |
| Strategy execution / naval doctrine |PASS,1,156 matchups;34 naval capability scores. |
| Context / diff |PASS; post-report handoff exceeded hot-context limit by128 bytes, was shortened without dropping the ledger, and all9 context fixtures passed again. |
| String budget |PASS,1,489/1,500. |
| Read-only civilization synchronization |Known baseline: six would-update files, not regenerated. |
| Good-units provenance |Known baseline FAIL: frozen AI RAW.per hash, not rebaselined. |
| Ordinary engine/runtime acceptance |NOT RUN; no deployment authorized. |

The initial sandboxed discovery ran618 tests and exposed two assertions (hot-context size and lexical Ctrl adjacency) plus a Windows Temp permission error. The context was compressed, the adjacency assertion now permits only an exact hash/generator-verified bridge, and normal-access writer tests passed. The final discovery above includes the additional line-ending regression test. Historical591-test and27-onset-test baselines are not substituted for these new results.

The user requested the implementation itself on PR11, not only another review comment. The pending counter correction is separable from the boarding/instrumentation commit. Installed user experiments remain untouched; no gameplay flood resolution or runtime acceptance is claimed.
