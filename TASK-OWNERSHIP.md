# Task ownership / threat preemption recovery

Status: **ROOT CAUSE NOT FULLY PROVEN — OWNERSHIP TELEMETRY REQUIRED**.

R2-arrival release priority completed first: R4:455 is installed and all 68
files verified. Only hunt distance changed 28 -> 16; food 12 and all eight
self-target fallback guards were already present. Eight new regression tests
protect both invariants; all 163 tests pass. No ownership or military runtime
change. The directive's premise that these guards were lost is contradicted
by current source/history; do not use it to explain away the observed own-TC
or passenger behavior. See HANDOFF.md for hashes, separate commits and pending
fresh-runtime acceptance. R2 ownership analysis resumes with the archived R2
map, not the current R4 map.

This is the user's 2026-08-30 architectural recovery objective. It supersedes
the earlier narrow restriction against changing ownership/recall in this
experimental worktree. It does not authorize navigation, landing-coordinate,
route-scoring, recovery-unload, Mining Camp resource-wait, escort-geometry,
unrelated command-flood, salvage, or Port-placement changes in the same patch.
No runtime behavior was changed in this investigation. T8 now identifies the
recorded global-recall callers, including a proven siege-escalation overwrite
of Red's boarding orders; worker/native attribution and the shared protection
mechanism remain unresolved. See the T8 update below, not the older T7 limits,
for current caller evidence.
T10:451 passenger-writer telemetry FAILED engine compilation (ERR6003 at
rawai-init-goals.per:362). T10R1:452 reused 12 string constants and produced
visible RAW44W output in the user's running match, but misclassified generic
villager cleanup as a reservation change and logged it while no mission existed.
T10R4:455 is now installed: retains R2's actual-mutation classification and
adds delayed, staggered, bounded identity announcements after R1's startup
marker/map loss was established. All 351 source sites are retained;
R3 engine/replay acceptance remains pending. The R1 replay map is preserved at
`G:\Projects\Codex\Rome at War AI\.analysis\p3b44t10r1-writer-trace-sites.json`.
The user explicitly restored this as the priority over congestion investigation.

R1 18:10 replay now establishes SCOUT-ferry interference (not worker migration):
source-1 land-defense recall interrupts Green twice and Orange twice; Purple
and Orange receive exploration order 705 during boarding while group flag 4
remains visible. R1's writer quota is exhausted for all players at 05:40-05:41,
before first boarding at 10:05. No startup map/marker survives, so zero players
pass fingerprint validation. Missing trace data cannot identify other writers.
All 15 scout episodes across eight players are recorded in HANDOFF.md and the
new R1 benchmark: five full-load confirmations, ten empty aborts (five with
recorded preemption, five still approaching at timeout), no assault episodes.
Root-cause evidence is sufficient to name the scout preemptors; the controlled
native exploration release/protection mechanism and wider worker ownership
remain unresolved. Do not substitute another congestion investigation for them.

## Required invariant

### R2 all-player evidence update

After the release-blocking recovery was deployed, R2 was audited: 282,006 exact
events, 20 identified hulls, 160 load packets and 58 raw loading windows.
Missing boundaries mean those windows are not 58 fully proven lifecycles.
All 76 retreat packets have existing source labels. Orange's priests 33235
and 34388 receive land-defense recall during relic boarding at 27:37 and
37:18. Their assault/migration goals are both idle: those goals alone cannot
represent every passenger owner. Preserve this as a common-contract requirement.

Purple's 48:32 siege recall is route-stage SCREEN-FIND, after partial departure;
Green's 55:24 recall is WAYPOINT-WAIT. They include prior passenger rosters but
are not proof of boarding interruption or forced disembarkation. Blue scout
4608 has repeated STOP 706 (283 and 276 packets in two short boarding intervals),
with later idle/ashore/distance-1/group-4 samples. Producer remains unresolved:
Blue's trace budget was already exhausted. STOP for an already-garrisoned unit
must not be confused with harmful ashore cancellation. The late 20-unit worker
load has insufficient occupancy evidence to label every STOP a lost passenger.

R2 contains no complete marker/map identity; new writer-site attribution remains
withheld. R4 preserves R3's delayed identity fix, which this earlier replay
cannot validate. Keep the known recall cause distinct from the unidentified
STOP/native boundary. Full evidence, limits, positive outcomes and exact
artifacts are in HANDOFF.md and the R2 benchmark. No further runtime change was
made during this audit; common ownership implementation remains pending.

### Contract

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
retained in HANDOFF.md and its benchmark. The following table is historical T7
evidence; T8 was subsequently supplied and audited below.

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

## T8 caller attribution and late Red obstruction

T8 `20260830-154021`, SHA-256
`C7BDFAF53DE72F03012C5AD88F4B930E9B7670A07CDC96490489F7428F2CE29F`,
matches marker `RAWAI-P3B44T8:449` and the recorded 68-file deployment hash.
All-player totals: 190 loading commands, 58 boarding windows, 354 passenger-
window instances. There are 28 full-load-corroborated successes without an
observed conflict, 34 conflicts with later ashore/owner evidence, and 292
unresolved instances (108 include a conflict with uncertain pre-boarding
timing/ownership). These remain evidence categories, not failed-mission counts.

Every one of the 100 DE_RETREAT packets maps to one of 56 tagged invocations:
land defense 28 invocations/47 packets, naval defense 16/32, siege escalation
11/19, loss regroup 1/2. Sources 5 and 6 do not occur. A single invocation can
emit adjacent land and naval packets at the same clock. A one-label-per-packet
join incorrectly leaves 44 packets unattributed; those are not evidence of
native recall. The corrected external join retains both packets and exact
source-label sequence. All labels have matching packets.

At **54:03.506**, Red's source **3 (siege escalation)** emits a 62-member land
recall toward TC 4434 `(31,136)` and a 13-member naval recall toward Port 30910
`(20.5,122.5)`. Assault state is 33, hull 31341. Passengers 40149, 43815 and
47309 received boarding at 53:56.856, then this recall, and appear in the
54:10 boarding retry. Later samples of 47309 and 40149 retain flag 4. This
establishes that the scripted fortification-escalation recall can overwrite
boarding without releasing the reservation. Its trigger is three known
fortifications, not a verified severe home emergency. Sparse flags do not
prove continuous ownership at every instant; later partial loading does not
mean this recall permanently prevented the voyage. Red's 55:04.182 source-2
recall occurs during route screening, not the earlier boarding window.

Separately, the user confirms that Red's late physical blockers were other
Transports manually moved away. Playback at 66:24 shows the migration hull
with four villagers and two adjacent empty Transports. The command stream
records moves of 48064/31880 at 66:30-32; migration hull 31691 receives its first
departure at 66:31.236 after the 30-second partial-load deadline and reports
route distances 52/30/15/0 through 67:32. T3 clearance belongs to the assault
departure state machine, not migration boarding/departure. This is a coverage
gap, but intervention overlaps the normal loading deadline: do not claim the
replay proves a failed post-departure stall detector, or that every preceding
second of waiting was caused by collision. Retain the physical symptom and
the precise timing limit together. Do not mix a congestion micro-fix into the
shared ownership patch.

The raw reports, per-player table, preserved successes, and next diagnostics
are recorded in HANDOFF.md's T8 section. This audit changes no runtime behavior;
neither physical congestion nor the broader ownership defect is resolved.

The subsequent user screenshots also establish missed Blue obstructions at
49:11 and 66:50. Correlated commands show a no-departure assault wait followed
by home unload (35026), and later exhausted migration route/return attempts
(36912). A command-linked hull census is not a census of physical blockages;
absence of a congestion tag is not success. HANDOFF.md records the screenshots,
exact windows and prepared T9 terminal diagnostics. Those diagnostics add no
ownership/navigation behavior and do not establish safe blocker eligibility.

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
every worker writer or native engine task. T10 now brackets 351 command,
reservation/group and native-policy/delegation sites with source-map-verified
IDs and pre/post assault/migration state/hulls plus selected-object identity/flag.
The map retains exact actions, including acquisition/release intent; replay
packets supply commanded members. No new ownership permission lock is implied.
The compiler adds no search/filter resets or gameplay commands, and relocates
existing jumps to the same original targets (including the guarded farm jump).

T8 directly demonstrates that command packets may arrive AFTER after-command
chat. The new analyzer preserves compatible deferred issuers, not just packets
inside brackets, and refuses to choose among multiple candidates by proximity.
Both explicit quota gaps and absent map fingerprints block unsupported caller
inference. An untagged WORK packet remains unresolved, not automatically native.
See HANDOFF.md's T10 section for bounds, hashes, source-map generation and the
`--writer-manifest writer-trace-sites.json` all-player audit invocation.

The required gameplay/deterministic contract tests are **not implemented or
passed** in this diagnostic revision: assault reservation versus ordinary
military controllers; migration reservation versus economy controllers;
complete/abort release; bounded routine defense; verified severe preemption;
friendly-fire rejection; allied help with live TC, destroyed TC and no hostile.
All-player runtime acceptance must additionally preserve ordinary P3B44 attacks,
successful T1-T5 missions, safe partial lifts and economic settlement progress.
Packet/lifecycle-tool tests are separate and cannot substitute for these tests.

No selector/global-retreat/anchor patch or navigation change was made here.
Installed runtime is T10R4:455, generated in memory from this same checkout by
`tools/sync_test_ai.py --writer-trace`; T9 was never a separate installed test.
T10:451 was rejected by the engine's string table. T10R1 reduces payload literal
occurrences from 5,665 to 1,465 and adds an occurrence-based build budget plus
a regression fixture reproducing the rejected expansion. R2 corrects the idle
trace exemption for site 41 and preserves real acquisition/release sites.
R3 sends marker/map identity three times after startup, with players staggered
and 30-second intervals independent of invocation quota. 163 regression tests
and all 68 deployment hashes pass; fresh engine/replay acceptance is pending.
First check R3 identity delivery and off-mission trace suppression. R1's replay
is audited and its exhaustion confirmed; preserve R1/R2 maps for old recordings.
Unchanged fields do not imply no competing command.
The work is open; this document, the audit
and the diagnostic additions are intermediate evidence, not resolution.

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
