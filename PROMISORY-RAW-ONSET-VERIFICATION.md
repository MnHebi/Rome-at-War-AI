# Promisory–RAW migration: independent onset verification

2026-09-08. **INVESTIGATING; no gameplay correction or deployment in this task.**
Canonical checkout `.trade-work/T30-trade-cap-civ-fix`, branch
`fix/trade-cog-cap-dacian`, HEAD `f6f1b5bcc53f63d6cec7386eebf658c58b402206`.
Existing uncommitted T56 experiment and undeployed ranged-counter repair preserved.

## Result

The comparison identifies real source differences, but does not establish the
order-706 cause. The DE-disabled builder cleanup has **no observed explicit STOP
contact** with the examined flood actors around onset. Boarding renewal **does**
contact affected actors, including one observed entering its intended hull before
later renewals. Whether that renewal is unnecessary, and whether it causes the
flood, remains unproven. Repeated WORK-to-resource packets also touch affected
actors, but the recording does not identify their PER/native producer.

Do not copy a DE guard or suppress renewals as a proven flood fix on this evidence.
Do not replace native gathering, change task percentages, or redesign migration.

## Evidence identity

Read the complete supplied comparison, then inspected the ZIP itself, current
RAW source, existing writer/modifier inventory, exact replay commands and paired
diagnostics. The supplied ZIP is a source snapshot, **not independently verified
as the shipping version of DE AI**, nor a demonstrated flood-free runtime control.

- ZIP: `G:\Projects\Codex\Rome at War AI\Comparison\Promisory.zip`, 36 PER files.
  SHA256 `5fdc527334b78e7a7bc3e7f387020d5050108a358f5c086610b9741cb7db9ff7`.
- ZIP `general.per`: `ad926dd04d6dbad14830203d82f9d9d356f9697dd4eee98e02e207b1757b0afe`.
- ZIP `gatherers.per`: `29179c2b4d9d29b7031b70b5d4f5dff382353df1938304f1115436676b92fb17`.
- ZIP `const.per`: `400160cf46fe9992ddf20817261fd337c925d2729d42083c8865747353803db0`.
- ZIP `init.per`: `d1d4fdbd5bb1936378e8899efdcdcc8bf1a6ab39392d236ed83246bb340d2a01`.
- ZIP `tsa.per`: `27950da53e6357a4e127595fb8b26f1161bd079d22145e07278952a89d043625`.
- T55B: `SP Replay v101.103.48987.0 @2026.09.07 121439.aoe2record`,
  SHA256 `632D89F42B339B06E6B83EF9A58F1FE7855EED9DB22DD3A200B2DDDA4A005858`,
  T55:503 / recorded source `1f87ef0` (see T55B causal investigation).
- T56: `SP Replay v101.103.48987.0 @2026.09.07 144755.aoe2record`,
  SHA256 `708AF267E74E6E77F5984F8FAE2AB9E8C94D15BA82683768185BE51F01491B5A`,
  T56:504 / recorded 103-file aggregate
  `FB515FA0A52859BCC677353D7B06B38792DC6DAF4C03604AA793EBF30D707730`.

### Installed runtime drift discovered during verification

The currently installed payload is **not** the recorded T56 payload despite its
unchanged marker. Its 103-file hash is
`60E05CFF142D948134C0693674CD37F8B851EE297CD40351D9DAB27B8576895C`.
Two files differ from the recorded payload:

1. `rawai-customconstants.per`: adds DE-AVAILABLE / UP-GAME-WK definitions of
   `de-game` and `wk-game`.
2. `rawai-general.per`: removes the missing-target cleanup's STOP (counter 1
   remains) and adds `de-game != 1` to the builder-target cleanup (counter 2).

The latter has filesystem modification time 2026-09-07 18:24:51 local. Timestamp
alone is not provenance. More strongly, substituting the **canonical bytes of
only these two files in memory** reproduces the recorded T56 aggregate exactly.
No installed files were altered. Current military/homebase/boarding-observer
files independently match installed bytes. Undeployed counter-repair differences
in other canonical files were not substituted into this reconstruction.

Therefore the T56 replay is not acceptance evidence for these later installed
cleanup edits. Preserve them; do not silently overwrite on the next deployment.

## Source comparison: verified differences, not causes

| Boundary | Supplied Promisory | Current RAW / causal limitation |
|---|---|---|
| Builder cleanup | `gatherers.per:4448` requires `de-game != 1`; `const.per:4952` defines DE as 1. Checks build order, nonmissing target, target not pending before STOP. | `rawai-general.per:82` lacks that guard in canonical/recorded T56 source. No actor STOP at studied onsets. |
| Missing-target cleanup | Adjacent attack/build/repair/enter cleanup is not DE guarded. Gather/hunt cleanup separately is guarded. Whole scope also has early-game/difficulty gating. | Do not conflate all cleanup with the single DE-disabled builder rule. RAW reserves only free workers while preparation route is IDLE, excluding existing group flags and boar/tree targets. |
| Main migration | `general.per:2219–2297` counts already-entering home-zone workers before selecting a new boarding batch; timed recovery can STOP workers. | RAW initial/accepted/retry/rendezvous writers 20/21/23/24/25 reselect nongarrisoned reserved passengers without a same-hull active-entry/progress exclusion. |
| Nile Delta startup | `general.per:5307–5333` has initial boarding and bounded three-second retry; retry removes `actionid-enter`, `orderid-enter`, and workers targeting transport class. | Not evidence that all stock boarding is one-shot or never needs renewal. |
| Other worker tasking | `gatherers.per:2910`, `:2998` and `tsa.per:5447` explicitly remove entering workers. | RAW instead relies substantially on group ownership. Neither selection rule is proof of actual runtime exclusion at every boundary. |
| Gathering controls | No named `sn-keystates` or explicit named resource-drop-distance `-2` assignment in the 36 files; special startup/nomad/infinite-resource branches modify gathering. | No migration-wide native gathering shutdown to transplant. Text search does not resolve numeric aliases or native engine behavior. |

The active RAW cleanup selects group-flag < 0, creates a temporary
`attack-transport-group`, rechecks self/group before STOP, then releases it.
Migration passengers are reserved in group 11. Sampled Yellow34730 and Green34564
still have group11 near their onsets. That supports the ownership boundary but
is not continuous-state proof for every actor.

## All-player exact replay sweep

Used `audit_task_ownership.read_stream` with length-verified actor arrays; both
streams report zero decoding failures. The broad parser's shifted AI_ORDER
actor fields are not used. New `tools/audit_boarding_flood_onsets.py` groups
order706 by **player + actor**, splitting at gaps over 1,000 ms and retaining
bursts of at least 100 packets. This operational definition is not an engine
mission boundary. Counts are actor-packet references; shared packets must not be
summed as unique commands. Shorter isolated packets are not claimed absent.

- T55B: 25 sustained bursts, 17 distinct player/actor pairs.
- T56: 9 sustained bursts, 9 distinct player/actor pairs.
- **Every one of the 34 bursts has zero explicit actor STOPs in the preceding
  30 seconds and during the burst.** No claim that all possible interruption
  commands are STOPs, or that a much earlier state change is excluded.

Artifacts outside Git: `G:\Projects\Codex\Rome at War AI\.analysis\`:
`t55b-exact.json`, `t56-exact.json`, `t55b-onset-audit.json`,
`t56-onset-audit.json`. They retain packet sequence/offset and exact actor arrays.

### T56 onsets (game seconds, not wall-clock seconds)

| Player / actor(s) | First sustained706 | Relevant contact |
|---|---|---|
| Yellow7706 | 2223.713 | Garrison to35010 at2222.540; first repeated WORK to34348 at2223.739 (+26ms). |
| Yellow34730 | 2238.899 | Garrison to35010 at2238.884, 15ms before onset; WORK34348 at2238.925 (+26ms). |
| Green34564 | 3627.901 | Garrison40020 at3617.563 and3620.844; no WORK in onset's inspected nearby command window. |
| Green39457 | 3628.608 | Three garrison40020 packets in preceding30s. |
| Red41448 | 3717.703 | Repeated garrison40285, latest3717.502; WORK34395 at3719.679. |
| Red38174 | 3717.774 | Same hull renewal; WORK34395 at3717.799. |
| Red34656 | 3717.879 | Same hull renewal; WORK34395 at3717.920. |
| Red34636 | 3718.157 | Same hull renewal; WORK34395 at3718.182. |
| Red34616 | 3718.480 | Same hull renewal; WORK34395 at3718.430, 50ms **before** this actor's first706. |

The native706 packets here target -1, not the fish resource. WORK targets34348
and34395 are initial Gaia objects type69 (`FISHS`, DAT class33), verified against
the initial-object table and current authoritative mod export. Header object
kind/class fields are not interchangeable with DAT unit class.

### Actual boarding-writer attribution

Yellow's numeric diagnostics identify writer24, modifier2, hull35010; exact
SPECIAL subtype5 arrays contain7706/34730. For example, writer24 is reported
at2219.242 and2222.525, followed by garrison packets at2219.255 and2222.540.
This is more than a rule-capability inference: the affected actors are in the
actual packet arrays. Later renewals continue for34730 through2238.884.

At2217.602, delayed post-observation for Yellow34730 records action617,
order717, target35010, nongarrisoned, carry15, group11. Subsequent renewals occur
while the last observed intent was already entering the correct hull. However,
there is no contemporaneous position/distance/progress pair proving that it was
still approaching successfully, rather than blocked or retasked before renewal.

Green34564 is also observed entering40020 (carry17, group11) at3621.361, yet its
onset3627.901 precedes the next writer24 report3627.970. This contradicts a
universal claim that the immediately following writer24 evaluation starts every
burst. A writer23 evaluation at3624.674 reports719=0; an evaluation is not an
actual command packet. Do not equate a telemetry counter with successful issuance.

T55B Cyan43834 receives garrison39461 at5543.621 and5548.052; sustained706 begins
5549.578 and continues to5770.911 (8,823 actor packets). No STOP targets it in
the defined window. Cyan37566 starts a burst4655.750 after one recent command to
the **new** hull42426 at4654.296; it had earlier orders to another hull42875.
Yellow35095/61007/61020 have later T55B bursts with WORK/ORDER activity and no
garrison in their preceding30s windows. Thus the comparison does not explain
every flood as immediate same-hull boarding renewal.

### Competing worker writers

The WORK packets prove competing **orders**, not a specific competing PER site.
In two Yellow cases706 precedes fish WORK; in Red34616 WORK precedes706; Green's
nearby stream lacks the same WORK pattern. Temporal correlation alone cannot pick
one universal initiating command.

Rechecked the existing Villager DUC inventory against source: homebase TC and
lumber-camp assignment target foundations; farm staffing targets farms; fisherman
redirect searches gold/stone/tree (not fish), and rechecks free ownership and
zero carry at issuance (`rawai-homebase.per:2657`). Migration return/deposit,
drop-site work, retask-anchor and hull-repair are distinct state-bound targets.
None is an identified source for these fish WORK tuples. Native task assignment
remains possible; shared-search/state interference remains unexcluded without
an exact issuance record. Do not infer "native producer proven" from lack of
a matching visible intended PER target.

## Decision and exact missing evidence

**No narrowly causal gameplay patch is supported yet.** A DE guard would change
cleanup behavior without evidence that its STOP touched these actors. Dropping
all renewal would change recovery for possibly stuck passengers. Both exceed
what the onset evidence establishes.

The discriminating evidence still needed is:

1. At the actual boarding issuance boundary, for an affected actor: exact actor,
   hull, writer, modifier, action/order/target, carry, reservation, position and
   actor-to-hull distance, plus a second sample sufficient to measure progress.
   Current representative after-samples do not supply pre-command progress.
2. At the first resource retask: exact selected actor **and target/type**, writer
   and current modifier. Per-minute totals and another representative actor do
   not distinguish RAW issuance from native WORK generation. Any new sampling
   must reserve a bounded episode around the affected class, not log per sweep.
3. A controlled same-setup comparison only after that discrimination: omit a
   renewal **only for demonstrated same-hull progressing entry**, keeping stalled
   recovery, selection, deadlines and native gathering unchanged. Do not mix that
   experiment with the two installed cleanup edits or call it an accepted fix.

Acceptance must measure first706 onset/frequency and successful boarding while
ordinary gathering/deposit, useful partial loads, rescue and recovery survive.
No new runtime telemetry or behavioral experiment was installed in this task.

## Adversarial read-only review and validation

- ACCEPTED: absence of STOP is not absence of all cancellation; narrowed claim
  to explicit STOP and stated30s window.
- ACCEPTED: entering intent is not progress; no redundant-renewal fix asserted.
- ACCEPTED: WORK can be downstream of706; preserved both temporal orders.
- ACCEPTED: current installed marker hides two-file drift; reconstructed recorded
  payload hash in memory and kept historical/current identities separate.
- REJECTED: copy stock cleanup guard as causal706 repair; no actor STOP evidence.
- DEFERRED: native-versus-PER resource assignment attribution; missing boundary
  identity above. Gameplay status remains INVESTIGATING.

Changes here are offline analyzer/tests and project knowledge only. Focused
onset, exact packet/ownership and existing boarding-contract tests: **PASS**
(7 + 13 + 7 tests). One initial module-style invocation of the existing ownership
tests failed its import path; rerunning with repository test discovery passes all13.
PER structural/operand, context metadata and `git diff --check`: **PASS**.
Exact replay reanalysis after analyzer hardening retains25/9 episode results.
Full repository suite was not rerun for this offline-only change (prior591-test
baseline retained, not claimed as a fresh result). Fresh gameplay acceptance:
**NOT RUN**, no behavior changed in this task.
