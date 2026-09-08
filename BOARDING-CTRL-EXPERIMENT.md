# Mining-passenger Ctrl experiment (T56:504 deployed)

Deployment 2026-09-07: user authorized; 103/103 runtime files independently
verified byte-identical, no overlay/unexpected files. Source is baseline below
plus uncommitted experiment and T56:504 marker. Aggregate SHA-256:
`FB515FA0A52859BCC677353D7B06B38792DC6DAF4C03604AA793EBF30D707730`.
Structural/operand, modifier, generation/policy, string-budget and 15 focused
tests passed after marker update. The following describes the experiment as
prepared; deployment is complete, but fresh-match acceptance remains pending.

Status: **EXPERIMENTAL / PENDING RUNTIME**, not a proven order-706 fix.
Baseline: `f6f1b5bcc53f63d6cec7386eebf658c58b402206` on the canonical
`fix/trade-cog-cap-dacian` checkout. Previous runtime was T55:503/1f87ef0.

## Evidence and hypothesis

T55B Cyan worker 43834 received garrison orders to hull 39461 at 92:23.621
and 92:28.052. Its 8,823 single-actor order-706 packets began at 92:29.578
and ended at 96:10.911, after home-unload attempts. The partial-load STOP
targeted 42268 and 43118, not 43834. See `T55B-CAUSAL-INVESTIGATION.md`.
This establishes a boarding-associated onset, not the native/PER producer of
706. The user authorized isolating the boarding modifier as an experiment.

Cached AIRef `airef-reference-20260830.js` (hash in the T53 audit) documents
0=no keys, 2=Ctrl; the modifier is sampled at DUC issuance and may be reset
immediately. Ctrl's specific effect on garrison/task persistence remains
unproven. Ctrl can affect carried resources: that is an acceptance risk,
**not** authorization to add a zero-carry boarding filter.

## Exact policy

`villager-command-modifier-policy.json` expands the existing T53/ownership
inventory into 75 explicit per-command entries. Mixed migration hull/scout
rules are conservatively included; inclusion does not claim the hull is a
Villager. The all-DUC fingerprint detects changed/new sites outside that subset
and requires renewed review. Validate with `tools/villager_command_policy.py`.

| Writer | Mining-passenger site | Modifier |
|---|---|---|
| 20 | MIGRATION-RENDEZVOUS-START | 2 -> unchanged action-garrison -> 0 |
| 25 | MIGRATION-RENDEZVOUS-PASSENGER, distant renewal | same |
| 21 | MIGRATION-ISSUE-BOARD, accepted mining manifest | same |
| 23 | MIGRATION-LOAD-DIAG-APPLY, first local retry | same |
| 24 | MIGRATION-CHECK-LOAD, subsequent local retries | same |

Writer 25 is a new distinct rendezvous-retry label, not a STOP counter.
Four formerly shared rules have mutually exclusive mining/non-mining copies.
Their original facts/actions remain intact apart from the explicit branch
condition, modifier and diagnostic reads. Scout copies and the scout initial
boarding rule retain modifier 0. No selection, ownership, resource-carry filter,
command/stance, 120-second rendezvous lease, 30-second boarding deadline,
eight-second distant retry, three-second local retry, or terminal policy changes.

Current four economic Ctrl writers remain unchanged. Explicit exceptions:

- Rescue hunters and boar-lurer TC garrison: emergency target/carry semantics
  unassessed; retain 0.
- Wall/gate builder STOP and TC evacuation: defense/garrison semantics
  unassessed; retain 0.
- Failed-colony reboarding, recovery/scout paths: distinct lifecycle semantics
  unassessed; retain 0. Boarding is no longer categorically excluded.
- Migration resource assignment, return-to-TC deposit, foundation build/repair,
  transport repair: family-specific carry/task semantics unassessed; retain 0.
- STOP/release, movement, patrol, unload and retirement/delete: unassessed;
  retain 0. Naval, assault-military and relic commands are unchanged.

## Bounded observations

The five actual issuance sites capture a private four-goal search-count block,
then the first local actor ID, after the command and immediate key reset.
No search-list membership, ordering, target point or gameplay goal changes.
The read-only selected-object pointer is used after issuance; original suffixes
have no object/point reader. The distant retry rebuilds its hull list before
its subsequent movement command. Empty-list captures are invalid (AIRef says
failed target selection retains the previous pointer); `local-count=0` makes
the logged `actor-candidate` explicitly unusable as an actor attribution.

Existing `RAW12 diag id/value` pairs avoid adding new telemetry strings:
700=writer, 701=modifier, 702=hull, 703=local-count, 704=actor-candidate,
705=time; 706–718 are post actor, hull, writer, modifier, observed, time,
mission-state, action, target, order, garrisoned, carry and group, respectively.
Diagnostic ID706 is not native replay order706. ID719 records remote count.
A zero local or remote count is not proof
of a successful command issuance. At most eight issuance records per player per
300 game-seconds; this class rearms, and no other controller consumes its budget.
One nonempty sampled actor is retained independently of later retries.
The delayed read is due after two seconds at the existing farm-IDLE timer
boundary, before farm searches. It includes garrisoned objects and emits saved
actor/hull/writer/modifier, current mission state, action, order, target, carry,
group and garrison flag. `post-observed=0` means unavailable/not self-owned;
`-1` means no safe observation boundary within 60 seconds. Neither means dead
or successfully boarded. Timestamps expose observation delays. The observer
never issues a task, changes ownership, resets a gameplay timer, or holds a mission.

This is **representative actor sampling**, not complete manifest telemetry.
The actor at local index zero need not be the next flooding worker. Join exact
replay command actor arrays to writer time/hull and classify unsampled actors
separately; do not use absent diagnostics to exclude a writer or native producer.
43834 is historical evidence, never a hardcoded runtime actor.

## Validation / acceptance

Static contracts compare every military DUC rule against baseline normalized
facts/actions. Only the five wrappers, observation sequence, moved phase chat
and mutually exclusive mission split are allowed. Generated observers have
private goals, a contiguous four-goal output block and no gameplay commands.
Existing economic, boar rescue, evacuation, assault and migration contracts
remain covered by focused/full suites. Results are recorded in HANDOFF.md.

Final validation: **586/586 Python 3.12 tests PASS** with normal Windows Temp
access; seven new experiment tests PASS, PER structural/operand checks PASS,
ownership 1,036 sites / zero permission failures, strategy 1,156 matchups / zero
errors, naval doctrine, assault generation, boarding generation, policy,
context and diff checks PASS. Payload strings: 1,484/1,500. Initial string-budget
failure was repaired by reusing numeric diagnostic pairs; old one-rule retry
assertions now verify two mutually exclusive branches. Existing six-civ
generated drift and frozen good-units hash are unchanged, not rebaselined.
Changes remain uncommitted. No runtime experiment result exists yet.

Fresh ordinary-match acceptance requires verified deployment identity; all
players' boarding episodes and first 706 onsets must be assessed, including
unsampled actors and failures. Require persistent boarding tasks, actual
occupancy/departure, later unloading/gathering/deposit and no regression in
carried resources, partial manifests, rescue, scout/relic or assault boarding.
A material 706 reduction without those regressions supports the experiment;
unchanged/worse flooding, new passivity, carry loss or failed boarding rejects
it. A replay without the relevant onset is inconclusive. T56 is deployed;
runtime acceptance has not occurred for this change.
