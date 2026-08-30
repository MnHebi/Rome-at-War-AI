# Task ownership / threat preemption recovery

Status: **ROOT CAUSE NOT FULLY PROVEN — OWNERSHIP TELEMETRY REQUIRED**.

This is the user's 2026-08-30 architectural recovery objective. It supersedes
the earlier narrow restriction against changing ownership/recall in this
experimental worktree. It does not authorize navigation, landing-coordinate,
route-scoring, recovery-unload, Mining Camp resource-wait, escort-geometry,
unrelated command-flood, salvage, or Port-placement changes in the same patch.
No runtime behavior was changed in this investigation.

## Required invariant

A deliberately reserved unit remains owned by its task until that owner
completes, aborts, loses the unit, explicitly releases it, or accepts a verified
higher-priority emergency. Issuing a newer command is not an ownership transfer.

- Ordinary acquisition must exclude incompatible task-owned units, including
  assault/migration boarding, active expeditions, relief, scouts and siege.
- Apply the same rule to worker selection, builder/repair assignment, drop-site
  and idle-worker retasking, hunting support, retirement and resource pressure.
- Revalidate permission at command time, not only at initial selection; other
  controllers can run between selection and dispatch.
- An emergency must establish hostile identity, live presence, relevant
  distance and severity, then cancel/release the old owner before acquiring
  units. Damage flags alone cannot authorize strategic recall.
- Routine/local threats acquire a bounded free pool. They do not cancel active
  attacks or passenger tasks. Global recall is only a verified severe strategic
  emergency with explicit owner cancellation, not a regrouping convenience.
- Allied relief uses a persistent first-Town-Center coordinate per player.
  Capture the first reliable TC anchor, retain it after destruction, search
  live enemy military near that coordinate, and dispatch available responders
  toward the verified enemy position. No allied under-attack predicate and no
  arbitrary surviving-villager substitute. A current TC may be an additional
  anchor, not a replacement for the persistent original.

These are acceptance requirements, not claims about current behavior. A DUC
group flag is not a verified lock on native economy/attack/exploration tasking.

## Replay-wide audit

Source: T7 `SP Replay v101.103.48987.0 @2026.08.30 131412.aoe2record`, SHA-256
`04AB5E6664F9DBE0284E320A99AB16070DBC00DE67FE876AC8C5512176E7DDB5`.
The prior verified T7 runtime identity and original selected colors/teams are
retained in HANDOFF.md and its benchmark. T8 has not been supplied as a replay.

`tools/audit_task_ownership.py` reparses the raw stream. It checks exact packet
lengths for Transport lists, all retreat members, multi-unit AI_ORDER and WORK.
It never shifts an object ID based on its magnitude. The stock SPECIAL and
UNGARRISON decoder misses a one-byte field in this replay; WORK was absent and
AI_ORDER misread the order field and omitted additional selected units.

All 378 load commands on the established 25-hull union are covered, with
132 evidence-delimited boarding windows and every one of the 202 retreat events. The
windows have 33 assault, 41 migration and 58 unresolved/recovery/relic owners.
Full-load corroboration is not an individual boarding acknowledgment. Every
passenger record retains its initial garrison, first subsequent other command,
time/target, source hypothesis, reservation samples, result and uncertainty.
Every retreat retains exact members and their preceding commands/task links.

| Player | Windows | Successful, corroborated | Pre-boarding conflict with owner evidence | Unresolved | Retreats |
|---|---:|---:|---:|---:|---:|
| Red | 31 | 35 | 9 | 185 | 36 |
| Green | 9 | 2 | 9 | 52 | 35 |
| Yellow | 1 | 1 | 0 | 0 | 31 |
| Purple | 23 | 21 | 4 | 148 | 22 |
| Orange | 26 | 2 | 3 | 215 | 1 |
| Cyan | 4 | 1 | 2 | 19 | 23 |
| Blue | 13 | 2 | 12 | 100 | 53 |
| Gray | 25 | 1 | 44 | 186 | 1 |
| Total | 132 | 65 | 83 | 905 | 202 |

Passenger columns count passenger-window instances, not distinct people or
failed voyages. Of 1,053 instances, 56 have full-load corroboration and nine
have exact partial-landing membership without an observed conflicting command;
83 have a pre-boarding conflicting command and owner evidence, and 905 remain
unresolved (323 include a conflict whose
pre-boarding timing/continuous ownership is not established). No individual
death or genuine loss of availability is proven by this command stream; do not
turn that into a claim that nobody died. Exact flags at overwrite are generally
not recorded, and uninterrupted ownership between sparse snapshots is not
directly observable. Later retries/samples establish that the unit was still
ashore; they do not identify the writer or exclude an unlogged legitimate
preemption. The tool preserves these qualifications per record.

First conflicting commands in the 83 corroborated pre-boarding cases:
67 WORK, five ORDER, seven garrison commands targeting a different object,
two AI_ORDER STOP, one AI_ORDER explore, and one STOP. These are command
categories, not a universal cause. Some units ultimately board successfully.

The Red 55:02.350 event begins with STOP before its retreat packet, so the first
divergence is earlier than the retreat itself. Orange's 61:36-62:06 repeated
STOPs remain a separate producing path: its only retreat is at 67:46.218.
Worker WORK overwrites occur across Red, Green, Purple, Orange, Blue and Gray;
Cyan also has a resource-target ORDER. The issue is therefore not limited to
military retreat, but native versus script-triggered worker attribution is open.

## Script command boundaries

The audit report also inventories 247 command/build-delegation rules and 248
selection rules across runtime PER files, preserving source file, line, facts
and actions. This is a source-boundary inventory, not a completed certification
of every controller's ownership safety or native strategic-number behavior.
An omission of a filter
in a dispatch rule alone is not proof: some selectors are in preceding states.
Conversely, an earlier filter does not prove permission survives until dispatch.

| Boundary | Current source evidence / implementation obligation |
|---|---|
| Generic worker cleanup | Excludes migration group 4, not a common all-task invariant; temporary group 0 mutations must respect every owner. |
| Farm/fisherman/colony/lumber staffing | Some paths filter group 4, others do not; stored-ID retasks require command-time ownership verification. |
| Hunting support | Some selectors exclude group 4; exact lurer rescue and other task reservations need explicit compatibility. |
| Retirement | Bounded trade retirement excludes grouped workers; legacy global idle deletion has no per-unit permission gate. |
| Native economy/build/repair | Percentage settings and persistent builder assignments delegate selection to the engine. Script filters alone do not prove protection here. |
| Local/naval defense and defend leash | Unfiltered local military selection and global recall can touch incompatible tasks. Acquisition and recall must share the invariant. |
| Raid/attack preparation/recovery | Audit free acquisition against active native attacks as well as flagged groups; currently no complete shared contract. |
| Active transport/scout/siege/escort | Preserve successful T1-T5 paths; inspect acquisition, explicit terminal release and shared group-slot lifetimes, not navigation. |
| Relic ferry | Hull is flagged, but the exact priest is tracked by ID without equivalent passenger reservation; include it in the ownership design. |
| Allied relief | Already avoids allied under-attack in this branch, but searches current TCs plus villagers; no persistent original anchor or retained relief ownership. |

All six global retreat sources lack a complete explicit task-cancellation gate:

1. Land defense: one siege unit, five threats, or two threats after commitment.
2. Naval defense: two threats after commitment or four regardless.
3. Siege escalation: three known fortifications, not severe home invasion.
4. Loss regroup: repeated attack losses, not severe home invasion.
5. Periodic losses: broad all-unit STOP, attack-group reset and global retreat.
6. Allied taunt 45: broad all-unit STOP and global retreat, without threat proof.

This proves incompatible source capability and specific runtime intersections;
it does not assign every recorded retreat or WORK packet to an exact rule.
The later policy must distinguish an explicit human strategic request from
ordinary automatic preemption while still canceling old owners cleanly.

## Remaining discriminating evidence and tests

T8 already labels the six recall sources with assault/migration states/hulls.
Use it for exact recall attribution, but do not pretend those six tags cover
every worker writer or native engine task. Full ownership tracing also needs
owner acquisition/release/preemption reasons and exact commanded members at
ordinary command boundaries. Any quota/sampling exhaustion must be explicit:
an untagged packet is not native-cause proof if trace coverage was incomplete.
Do not introduce a search-reset observer that corrupts shared DUC searches.

The required gameplay/deterministic contract tests are **not implemented or
passed** in this audit-only revision: assault reservation versus ordinary
military controllers; migration reservation versus economy controllers;
complete/abort release; bounded routine defense; verified severe preemption;
friendly-fire rejection; allied help with live TC, destroyed TC and no hostile.
All-player runtime acceptance must additionally preserve ordinary P3B44 attacks,
successful T1-T5 missions, safe partial lifts and economic settlement progress.
Packet/lifecycle-tool tests are separate and cannot substitute for these tests.

No selector/global-retreat/anchor patch, navigation change, new runtime marker,
or deployment was made here. The installed runtime remains T8:449. The work is
open; this document and the audit are intermediate evidence, not resolution.

## Reproduction and audit validation

From the documented transport worktree, use the Python 3 path in HANDOFF.md:

```text
python tools/audit_task_ownership.py "C:/Users/LostSoul/Games/Age of Empires 2 DE/76561198053747760/savegame/SP Replay v101.103.48987.0 @2026.08.30 131412.aoe2record" --parser-root "../../.analysis/replay_parser_kjir" --transport-audit "../../.analysis/p3b44t7-transport-audit.json" --output "../../.analysis/p3b44t7-task-ownership.json"
```

The prior transport audit supplies the independently established hull/color
union and partial-landing evidence; it must belong to the same replay. That
older artifact has no embedded replay hash, so the new report records both
input hashes and the dependency explicitly rather than claiming an automatic
cross-file identity check. Preserve the raw report outside the AI repository.

Read-only adversarial audit findings:

- ACCEPTED: decode object arrays by exact packet length, never ID magnitude;
  retain all members and the actual AI_ORDER field.
- ACCEPTED: do not invent a 45-second task timeout; end windows only at recorded
  terminals/unloads/new starts, with replay-end cases explicitly unresolved.
- ACCEPTED: distinguish full-load corroboration, exact partial landing, conflict
  with later ashore evidence, and unresolved outcomes. A DELETE request does
  not prove execution or death.
- REJECTED: treat group 4 as an engine-task lock, attribute every STOP to global
  recall, or call a later successful lift a prevented completion.
- DEFERRED: exact writer/native-task attribution and uninterrupted reservation
  at overwrite require the missing boundary telemetry, not stronger wording.

Packet and lifecycle regression tests verify these audit properties only.
They do not implement or pass the gameplay tests required by section H.
