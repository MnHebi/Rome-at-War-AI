# T11 replay review and T12 acceptance

**Subsequent source-first audit:** [T12-SOURCE-AUDIT.md](T12-SOURCE-AUDIT.md)
supersedes any implication that all T12 changes are causal fixes. It identifies
the wrong Quadrireme-line production ID and the competing builder-assistance
writer, separates allied victim/location defects from cooldown, and records the
complete STOP-writer audit. Ordered-all-enemy naval priority is classified as
speculative; radius growth and the smaller flare area are requested policies.
The evidence below remains the historical T11/T12 test record, not runtime
validation or proof that the diagnostic-only defects have been repaired.

## Identity and scope

Replay: `SP Replay v101.103.48987.0 @2026.08.30 211106.aoe2record`;
82:39, SHA-256
`088EC5FBFCCB6DDABEAC85BB7181B38B883F05DFDCB1A06FC0EAD46ECD0B904F`.
All eight players were audited, not only the reported Red incidents.
Selected colors agree with the established Roman team: Red, Green, Yellow,
Purple. Opponents: Orange/Picts, Cyan/Britons, Blue/Germani, Gray/Gauls.
The recorded speed is Fast 2.0, not the original lobby note's Normal speed.
The map is the preserved Britannia setup; population 400, Extreme, shared exploration.

Before editing, the installed 73-file T11:456 runtime matched source:
`2CA656510A99D71A9C5A2CB5014FC3138904D120E806269127DEB5FF5824DABF`.
Players 2-8 serialize the build marker. Owner-player self-chat/marker coverage
is asymmetric; absence of another player's private telemetry is not inactivity.
Basic and exact-packet parsing both reported zero errors.
No crash diagnosis is inferred from this replay.

## All-player transport coverage

| Color | Hulls | Loads | Point unloads | Alternating phases | Terminal load-only |
|---|---:|---:|---:|---:|---:|
| Red | 5 | 53 | 57 | 14 | 0 |
| Green | 1 | 11 | 14 | 4 | 0 |
| Yellow | 1 | 28 | 12 | 5 | 1 |
| Purple | 5 | 35 | 48 | 12 | 2 |
| Orange | 2 | 22 | 37 | 16 | 0 |
| Cyan | 4 | 37 | 8 | 5 | 2 |
| Blue | 4 | 28 | 114 | 15 | 0 |
| Gray | 4 | 31 | 2 | 1 | 3 |
| Total | 26 | 245 | 292 | 72 | 8 |

The separate ownership reconstruction has 83 boarding windows. These command
phases are **not** 72 successful voyages. Successful examples include Purple's
57:00 partial load: five shore stragglers excluded, five boarded members issued
the 59:44 landing order, and another landing at 63:27. Exact manifest membership,
terminal cargo, geometry, and interference are not reconstructable in every case.
Automated conflicting-command classifications are leads, not blanket causal proof:
a STOP after garrisoning or at landing is not necessarily a stolen boarding task.

## Defects, evidence, and disposition

### 1. Red stone colony without a drop-site — INVESTIGATING

- User observation: settlers stood without a drop-site; user eventually built it.
- Replay: hull 32077 landed 18 settlers in zone 14 at 55:17. Live resource 739 was
  found; mining-camp requests at 57:25 and 57:49, rejected intermediate offsets,
  terminal failure at 58:09. No corresponding mining-camp BUILD packet appears.
- Proven boundary: request accepted by the PER gate does not mean foundation
  created. Native builder admission, reserved-worker interference, and physical
  placement rejection remain plausible; none is selected as the proven cause.
- T12 diagnostic: requested point, queue/foundation/affordability/hold mask and
  one exact reserved same-zone settler's action/order/target at request and timeout.
- Acceptance: foundation, assigned builders, completed drop-site and actual
  gathering/drop-off without manual intervention. Still open, not a telemetry fix.

### 2. Idle Juggernauts / limited discovery — FIXED-PENDING-RUNTIME

- User had to direct Red's ships. Source searched one enemy and fortifications
  within 48 tiles; fallback results could cross a shared-search sweep.
- T12: search all enemies; grow discovery 48 -> 96 -> 192 -> 255 after each
  120 seconds without sampled useful bombardment progress. Preserve the initial
  120-tile sea-tower search, escort restrictions and same-water source groups.
- Progress requires the sampled source attacking the exact target and lower target
  HP. Reissuing an order is not progress. Revalidate target owner/source family at
  command time, including fallback. Converted targets cannot renew the progress clock.
- Limit: one representative source, not per-projectile attribution or a per-hull
  guarantee. Expanded discovery is not longer weapon range or safe water access.
- Acceptance: autonomous distant bombardment, existing close attacks and escorts
  preserved; no endless movement toward unreachable inland structures.

### 3. Empty assault aborts — clock fault FIXED-PENDING-RUNTIME; boarding still OPEN

- Red's 60:00 request aborted empty at 60:19. Early/terminal Scout 4599 still
  had enter action/order 617/717, exact hull 33888, flag 4, distance 10.
  The 62:22 abort instead had candidate 35153 idle, action/order/target -1.
  These do not support one universal theft or one universal distance explanation.
- Source: deadline was based on gl-game-time, refreshed every 15 seconds.
  T12 uses a live boarding clock for the full 30-second allowance and four-second
  retries. Minimum five cargo, full/partial manifests and route policy unchanged.
- Acceptance: preserve useful full/partial lifts, allow the full window; establish
  remaining nonboarding causes rather than silently extending deadlines again.

### 4. Red return around 66 minutes — INVESTIGATING

- Hull 37810 progressed 77 -> 52 -> 26 -> 12 tiles from the waypoint, then stayed
  at 12 through four retries. At 66:14 the no-progress watchdog returned it:
  hull position (138,91), home (181,19), reported cargo 19, transport group 10.
- At 67:31 return failure still reported two aboard; alternate return and eventual
  quarantine followed. This is **not a maximum voyage-distance cutoff**.
- Mixed passenger classes are not established by the cargo count; preserve the
  user's mixed-cargo observation. Waypoint geometry, collision or another
  obstruction remains unresolved. No speculative route patch.
- Acceptance: reach the intended waypoint/landing or correctly identify and clear
  the actual obstruction; do not call a returned cargo load a successful migration.

### 5. Roman Quinquereme/Octeres production — INVESTIGATING

- Authoritative DAT makes Quadrireme 1870 -> Quinquereme 1750 (upgrade 1003) and
  Octeres 1884 available. Advanced Weaponry prerequisite 47 and Shipyard 1251
  matter. No Roman MAKE for these three hull types was found.
- Modern production checks rotation, phase, total fleet cap, per-type cap, and
  up-can-train; older disabled switcher blocks are not evidence of the cause.
- T12 samples those gates, concrete-versus-line training checks, resources,
  headroom, role and producer count. Do not infer completed research from a
  research request or missing native RESEARCH packet.
- Acceptance: identify exact rejection gate, apply supported fix, then demonstrate
  bounded Roman heavy-ship production without violating doctrine/focus constraints.

### 6. Taunt 69 collateral deletion — FIXED-PENDING-RUNTIME

- User reports unintended targets caught. Source radius was six tiles.
- T12 searches within **two tiles of the flare**, nearest one self-owned structure;
  no-candidate remains a no-op. Flare near the intended structure's center.
- Acceptance: only intended structure removed; adjacent outside-radius structures
  survive, including repeated use around Ports.

### 7. Late command flood / lag — INVESTIGATING

- T11: 152,771 AI_ORDER STOP 706 records. Identical STOP to Red's 17-settler
  group: 7,561 times, 55:17-59:19. Blue peaks at 26,363 commands during minute 61.
  Thousands of repeated worker orders and exploration commands also occur.
- R2 already had 55,148 STOP records over 62:04. Do not attribute all spam to
  T11's new native exclusions, or assume every STOP is an explicit PER writer.
- T12 counts every explicit STOP/reset-scouts invocation plus native attack-exclusion
  reset/type operations. Nonzero totals only, once per minute, with no lifetime
  quota. A positive count may involve an empty selection; it is not exact packet
  attribution. Zero can exclude a producer in the matching interval.
- Acceptance: identify source/native boundary, fix it, then show sharply reduced
  pointless repetition with exploration, transport and normal attacks preserved.
  No CPU profile supports claiming all observed lag has this sole cause.

### 8. False/missed allied attacks — cooldown FIXED-PENDING-RUNTIME; detection OPEN

- User: Green warned shortly after Yellow without enemies in Green's town;
  real allied attacks were missed. Keep this symptom as evidence.
- Green made 26 local-help calls; 20:01 and 20:03 expose the cooldown fault.
  There were 253 cannot-verify-reachable-attack replies across players.
- Source: local fallback searches same-zone enemies within home 48 even without
  an attacked asset; relief checks the requester's persistent original TC anchor,
  not necessarily its attacked colony. These are possible location mismatches,
  not proven attribution of each Green incident.
- T12 restarts the 120-second cooldown at every actual request. Logs distinguish
  formal town / attacked-asset / proximity fallback; exact asset, hostile, anchor,
  scan time and response anchor are recorded. Failed scans cannot relabel prior
  latched threat evidence. No response radius or relief policy change.
- Acceptance: correct location/hostile attribution, no unsupported under-attack
  claim, actual reachable attacks answered with available responders. Cross-water
  relief remains separately unimplemented.

## Diagnostic decoding and bounds

All-player chat pairs `RAW12 diag id`, `RAW12 diag value`:

| IDs | Meaning |
|---|---|
| 100 / 110 | Quadrireme-line / Octeres rejection mask |
| 120-125 | phase, naval role, rotation slot, fleet count, fleet cap, per-type cap |
| 126-130 | wood, gold, headroom, completed Shipyards, unit escrow mode |
| 200-206 | drop stage, mask, requested x/y, landing zone, attempt count, selected settlers |
| 210-216 | sampled settler ID, action, order, target, group flag, zone, idling |
| 300 | help kind: 1 formal town, 2 attacked asset, 3 home-proximity fallback |
| 301-311 | asset ID, hostile ID, anchor x/y, local target x/y, hostile player, zone, scan time, threats, responders |
| 320-324 | requester, result, response target x/y, zone; emitter is responder |
| result 321 | 1 no verified threat, 2 target lost, 3 no spare responders, 5 dispatched |

Naval rejection bits: 1 no concrete/base-or-upgraded availability; 2 train check
for line/unit failed; 4 concrete base train check failed; 8 fleet cap; 16 type cap;
32 different rotation slot; 64 Advanced Weaponry not complete. Up-can-train also
combines resources, queue and population checks; a bit alone is not a root cause.
Navy snapshots begin at phase >=4 with a completed Shipyard, at most once per
five minutes/player. They are samples, not a history of every rejected queue attempt.

Drop mask bits: 1 pending placement; 2 pending object exists globally (not proof
it is in this colony); 4 unaffordable; 8 worker hold active. Stage 1 is immediately
after request, stage 2 at its timeout. No diagnostic order or ownership mutation.

Writer pairs `RAW12 writer id/count`: codes 1-24 map to all explicit STOP/scout
reset sites in rawai-command-counter-defs.per; 90 resets attack exclusions,
91 totals excluded types. Generated map and coverage are tested. Counters are
aggregate invocations, not a replacement for exact replay packet analysis.

## Artifacts, review, validation

Raw evidence remains outside Git under
`G:\Projects\Codex\Rome at War AI\.analysis`:
replay-20260830-211106-t11-full.json; p3b44t11-command-stream.json;
p3b44t11-exact.json; p3b44t11-transport-audit.json/.txt;
p3b44t11-task-ownership.json; p3b44t11-summary.json.
inspect_t11.py provides bounded spam/chats/window/units/terminals queries.
The exact audit used audit_writer_replay.py --plain-runtime: historical writer
site maps were explicitly disabled, not applied to new source.

Read-only adversarial review dispositions:
- ACCEPTED: prevent four-slot up-get-search-state output from overwriting adjacent
  diagnostic goals; use the established local-total scratch block.
- ACCEPTED: publish help kind/asset only with the corresponding successful hostile
  scan; keep failed later scans from relabeling old threat evidence.
- ACCEPTED: validate progress target's owner against conversion; rebuild command
  sources/target after any cross-sweep fallback.
- ACCEPTED: retain 120-tile sea-tower discovery while expanding the old 48-tile
  land-fortification search. Do not shrink radius after one successful hit.
- REJECTED: infer every transport abort is theft or a distance cap; candidate
  samples and exact no-progress telemetry contradict that blanket explanation.
- DEFERRED pending evidence: native STOP producer, failed foundation cause, heavy
  train rejection, and exact false/missed allied attack attribution.

Validation: 204 regression tests (14 focused T11 tests), PER/operand checks,
strategy synchronization (1,156 matchups), naval doctrine, workbook round-trip,
33 replay benchmarks; current ownership inventory 666 sites, zero direct
permission failures. The full suite required permission for archival temporary
trace files. Tests were updated for the intentionally changed radius/clock/marker,
not weakened ownership or manifest assertions.
String budget: 1,431 literals; eight-player projection 11,448 within the project
budget, not a measured engine string-table limit.

**Fresh T12 engine compilation and replay acceptance are still required.**
No gameplay defect is declared CLOSED by static tests or telemetry.
