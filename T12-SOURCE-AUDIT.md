# T12 source-first audit — before backlog integration

## Audit boundary and identity

Audited T11 `6350c8416c43e397b3058b88cf2d9cacb879fd56` against T12
`37a310872dccabc52db02962509f76f813ba4f3a` on
`recovery/p3b44-transport-only`, in
`G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-transport-only`.
The checkout was clean. This remains the authorized experimental checkout;
the canonical ordinary repository remains `.pr-work\Rome-at-War-AI`.
Neither directory nor branch was switched. The immutable P3B44 control was not edited.

This audit changes documentation/evidence metadata only. No runtime edits,
new runtime telemetry, deployment, commits, push, or PR mutation. T12:457 is
an unvalidated mixed runtime, **not a set of eight proven gameplay fixes**.
The previous heading "Recent causal commits" was incorrect.

T11 replay SHA-256:
`088EC5FBFCCB6DDABEAC85BB7181B38B883F05DFDCB1A06FC0EAD46ECD0B904F`.
The all-player evidence sweep and raw-artifact paths remain in
[T11-REPLAY-REVIEW.md](T11-REPLAY-REVIEW.md). Selected colors, not slot order,
identify the Roman team. Nothing in this audit revises the user's observations.

## Classification of every T12 change

Each logical change below has exactly one classification. Some commits contain
several logical changes: a commit is not the unit of causal proof.

- **C:** `CAUSAL FIX — source/runtime evidence identifies the defect`
- **U:** `USER-REQUESTED BEHAVIOR CHANGE — intentionally changes policy`
- **D:** `DIAGNOSTIC ONLY — underlying defect remains unresolved`
- **S:** `SPECULATIVE — insufficient evidence`

"Gameplay" means orders, selection, timing, or policy, not chat/CPU overhead.
"Independent revert" includes its associated definitions and test expectations;
it does not mean blindly reverting a mixed commit.

| Change / class | Files and rules changed | Exact defect or objective; evidence | Gameplay changed? | Independently revertible? |
|---|---|---|---|---|
| C1 — C | `rawai-military.per` assault LOAD-ISSUE/CHECK/REISSUE/PARTIAL clock; `rawai-customconstants.per` goal 1248. Commit `5c3a7ff`. | Intended 30-second boarding allowance was started from `gl-game-time`, refreshed about every 15 seconds. Red's 60:00 request aborted at 60:19. Fresh `game-time` is now used for deadline and four-second retries. This repairs the clock, not every failure to board. | Yes: deadline/renewal timing. Minimum five cargo, partial-manifest policy and routes unchanged. | Yes; isolated causal commit plus corresponding tests. |
| U1 — U | `rawai-tauntcommands.per` flare deletion selector, radius 6 -> 2; commit `e2c43b3`. | User requested a smaller response area after collateral selection. Two tiles is the chosen policy, not an engine-proven uniquely correct radius. Nearest one self-owned structure/no-candidate no-op remain. | Yes: which structures qualify. | Yes; revert selector/comment and radius assertion together. |
| U2 — U | `rawai-naval-siege-watch.per`; military load, radius operands and progress sampling; custom goals 1249–1256/1258. Part of `d7400bb`. | User explicitly requested increasing search distance after inactivity. Implements 48 -> 96 -> 192 -> 255, 120 seconds without sampled progress; sea-tower range starts at least 120. This is not proof distance caused every idle ship. One representative source plus its target's HP is sampled, not each Juggernaut or each projectile. | Yes: discovery radius and progress policy. | Yes by coordinated hunks; not by reverting all of `d7400bb`. Remove dependent watcher guard C4 only if removing the watcher. Goal 1256 is unused and can be removed as cleanup. |
| C2 — C | `rawai-military.per`, SIEGE-TARGET-COMMAND reconstruction, exact remote ID/owner and local owner/family/zone checks. Part of `d7400bb`. | Fallback producer lies below the command consumer, so COMMAND can execute next pass after other controllers replace shared searches. Persistent IDs existed, but T11 did not rebuild both command lists there. This is a source-demonstrable lifetime error; it does not prove that every idle Red ship took this path. | Yes: only re-resolved intended sources/target receive commands. | Yes by hunks, preserving reconstruction independently of radius and enemy iteration. |
| S1 — S | `rawai-military.per` initial `find-closest` -> `find-ordered`, all-enemy NEXT/ADVANCE loop and SEARCH state; custom first-player goal 1257 / SEARCH enum. Part of `d7400bb`. | A one-enemy scan has a blind spot, but the audit has not established a T11 episode where this was the first blocker and another enemy had a usable target. Starting with ordered players also changes target priority. The user's explicit request was distance growth, not this priority change. Insufficient evidence to label this a T11 causal fix. | Yes: opponent priority, coverage and search work. | Yes by hunks; restore nearest-enemy selection and original family completion while retaining C2 and U2. Whole-commit revert would wrongly remove those too. |
| C3 — C | `rawai-diplomacy.per` both actual help-request emissions; commit `8820cb0`. | Timer was armed when the window opened, not when the request was sent. Green 20:01/20:03 corroborates an almost-expired window. Rearm 120 seconds at emission. **No repair of false or missed attack detection.** | Yes: request spacing only. | Yes; two timer insertions and timing test. |
| C4 — C | `rawai-naval-siege-watch.per` saved enemy focus/owner filter; military saves watcher player; goal 1259. Part of `18648ce`. | In the newly added watcher, target ID alone could keep accepting HP changes after conversion. Reacquire/filter by saved enemy owner. This repairs a source hole inside U2, not an independently observed T11 conversion incident. | Yes: what renews the progress clock. | Conditional: remove independently only if also removing U2; otherwise retain this safeguard. |
| D1 — D | New `rawai-command-counter-defs.per`, `rawai-command-counters.per`; loads in `AI RAW.per`; increments in `rawai-general.per`, `rawai-military.per`, `rawai-ownership.per`, `rawai-severe-defense.per`, `rawai-tauntcommands.per`, `rawai-native-attack-ownership.per`; `tools/instrument_command_counters.py`, `tools/generate_ownership_policy.py`. Commit `12189f6`. | Counts 24 explicit STOP/scout-reset sites and two native-exclusion operations. Underlying 152,771 STOP flood remains unattributed. Nonzero totals once/minute/player; no new order or owner policy. A positive invocation can have an empty selection and is not a packet attribution. | No intended order/policy change; adds bookkeeping/chat and runtime cost. | Yes as one instrumentation bundle, including generators/definitions/load sites. Do not revert T11 ownership restrictions with it. |
| D2 — D | New `rawai-naval-production-diag.per`, load in `rawai-military-units-common-hard.per`, diagnostic goals/init/strings. `18648ce`, interval correction `47cf53f`. | Samples availability, line/concrete trainability, caps, rotation, tech and resources. Fixes no train gate. Once/300 seconds after phase >=4 and a completed Shipyard; cannot identify every rejected opportunity or individual producer queue. The wrong line is source-visible without this probe. | No intended gameplay change; fact reads/chat. | Yes with load/owned diagnostic state and tests; shared strings/init must remain while other probes use them. |
| D3 — D | New `rawai-dropsite-diag.per`; military stores request point/stage at mining/lumber/mill requests and loads probe before WAIT-DROPSITE; goals/init. Part of `18648ce`. | Request/timeout masks and one settler snapshot do not create a foundation or repair native builder selection. Important limit: this probe **does** replace shared DUC searches, target point and scratch counts, though it sends no task order or flag mutation. It is not a zero-side-effect observer. | No intended gameplay policy change; shared-search observation risk remains. | Yes with request hooks/load/state/tests; other diagnostics independent. Preserve evidence fields, but do not claim search neutrality. |
| D4 — D | Military local-response kind/asset/hostile capture; diplomacy request fields; taunt response identity/result fields; diagnostic goals/init. Part of `18648ce`. | Distinguishes formal-town, attacked-asset and proximity calls, requesters/responders. Successful-scan-only capture avoids relabeling an old latch with a failed scan. Does not require the hostile to be attacking that asset, update response location, or cover all busy/no-anchor terminals. | No intended detection/dispatch change. | Yes with hooks/state/tests; cooldown C3 is separate. |
| D5 — D | `rawai-init-goals.per` T12:457 marker; shared diagnostic initialization/strings; `tools/test_t11_replay_fixes.py`, modified `tools/test_validators.py`; `OWNERSHIP-SOURCE-INVENTORY.md`, `T11-REPLAY-REVIEW.md`, `replay-benchmarks.json`, `HANDOFF.md`. | Build identity, assertions, inventory and evidence packaging. Tests encode the policies above and do not establish engine causality. Documentation's blanket causal label overstated the result. | No (except marker/chat); tests do not run in-game. | Yes as support artifacts, but retain provenance and keep expectations consistent with whichever behaviors remain. Do not reuse an old marker for a different payload. |

This covers all 24 paths in `git diff --name-only 6350c84..37a3108`.
Formatting-only hunks in the counter insertion commit add no separate behavior.
Supporting definitions/tests belong to their logical change; D5 covers the
remaining common identity and audit infrastructure, not a second classification
of the behavioral hunks.

## Roman heavy ships: complete source-first production gate

Authoritative DAT inspected directly with the existing vendored `genieutils`:
`RaW data fix/resources/_common/dat/empires2_x2_p1.dat`, SHA-256
`A1319BE7E0D4CCF68A13E719BA2D8B4B39383D01B7D3FDD3123452F6A0D36356`.
Also checked `CivTechTrees/BYZANTINES.json`. No DAT payload is copied into Git.
The AI and data-mod identities are different checks; neither substitutes for
the replay's transient research/queue/resource state.

| Gate, in execution/dependency order | Source finding | Audit result |
|---|---|---|
| Availability / correct family | Constants: Quadrireme 1870, Quinquereme 1750, Octeres 1884, Shipyard 1251. Rome is civ 23; tech-tree effect 256 does not disable 47/1001/1002/1003. DAT effect 917 upgrades 1870 -> 1750. | These are the intended Roman hulls, not generic units forbidden by Extreme focus. |
| Prerequisites | Automatic techs 1001/1002 require **both** Imperial 103 and Advanced Weaponry 47. Quinquereme tech 1003 additionally requires 1001, costs 800 food/600 gold, takes 60 seconds at Shipyard 1251. Advanced Weaponry costs 300 food/200 gold, takes 100 seconds at University 209. Its alternative tech-800 early unlock belongs to Syracusans, not Rome. | No pre-Imperial Roman Quadrireme/Octeres availability. The existing pre-Imperial SUPPORT Quadrireme rule is unreachable under this DAT; it is not the current competitive-role root cause. |
| Prerequisite research policy | `rawai-research.per` early Advanced Weaponry rule uses actual `up-can-research`; the broad age condition cannot override DAT prerequisites. Quinquereme rule around 529 requires phase 7, navy upgrades enabled, allowed role, and >=24/27 villagers according to economy policy, then actual research trainability. | Research path exists. Red request chats at 29:08/31:04 are requests, **not completion proof**. The parser's research array is empty, so it does not establish completion either. |
| Strategic demand / preprocessing | `rawai-naval-doctrine.per` Rome rating 8820, specialist YES; all four equal Roman allies and these opposing naval ratings select COMPETITIVE. Final role rules enable navy upgrades/roster. `AI RAW.per` loads common-hard on Extreme; Q/Oct rules have no excluding local preprocessor guard. | No Rome-specific disable or accidental disabled legacy-switcher dependency in the live production rules. This is the source-computed role for the recorded setup, not a captured runtime role value. |
| Fleet / family caps | Competitive cap = 8% of 400 = 32, family cap = 1% = 4. Census uses warship class plus separate boarding ship count; each train increments the shared total. Support instead uses a bounded specialist reserve. | A full fleet can legitimately block heavy ships; no reserved heavy slots for COMPETITIVE. Whether it was full at each T11 opportunity is not serialized. Do not remove caps to conceal a bad identifier. |
| Resources / escrow / population | Concrete base costs: Quadrireme and Quinquereme 200 wood/100 gold; Octeres 300 wood/225 gold; one population each. Discounts can reduce wood; fully upgraded evaluation costs are not every runtime's cost. `rawai-escrow.per` changes unit escrow mode in Imperial. `up-can-train` uses that mode and actual headroom. Earlier research/land production can spend resources first. | Gold alone does not prove trainability. Ordinary competitive rules have no extra arbitrary stockpile floor; SUPPORT specialist rules do. No proven resource-starvation episode for Octeres yet. |
| Producer availability | Both families train at **Shipyard 1251**, not merely any Port. `sn-dock-training-filter = 0`, training queue = 2. Construction rules exist, competitive desired Shipyards become 3 at phase 5 and 6 at phase 7. They still require an affordable, placeable foundation and admitted builder. Other Roman Shipyard makes establish producers at some times, not free queues during every heavy slot. | No permanent source disable. Individual queue/research occupancy remains a runtime fact; a completed Shipyard count is not proof of a free producer. |
| Rotation | Active modern cycle is SCOUT -> POLY -> FIRE -> DEMO -> HEMI -> BOARDING -> Q -> OCT -> JUG -> SCOUT. Each choice holds 12 seconds (nominal full cycle 108 seconds), timer reset prevents same-pass collapse. SUPPORT has separate direct heavy rules. Old switchers are behind undefined `RAWAI-LEGACY-NAVY-SWITCHER`. | Q and Oct slots are reachable. A slot does not wait for affordability or guarantee admission. No evidence supports blaming the disabled switcher or simply increasing ship caps. |
| Concrete trainability / train action | Common-hard around 2498–2547 and common around 2471 onward: Q count, `up-can-train` and `up-train` all use **`quadrireme-line = -282`**. DE defines -282 as **Turtle Ship line (831/832)**. Those DAT entries remain TURTL/UTURT; no upgrade links connect them to 1870/1750. Octeres checks/trains concrete 1884 correctly. | **SOURCE-PROVEN Q production identifier defect.** No concrete 1870/1750 fallback exists. **Octeres remains INVESTIGATING**, not explained by this defect. |

Identifier reference: [AIRef parameter definitions](https://airef.github.io/parameters/parameters-details.html#UnitId),
[AIRef object table](https://airef.github.io/tables/objects.html).
The local cached reference additionally records `turtle-ship-line` DE ID -282;
its older UserPatch ID differs. Do not substitute the older game's numbering.

Required Q repair: explicit availability/trainability and concrete train actions
for 1870 and 1750, with a **combined family count** including queued units and
the existing fleet/rotation/role/resource limits. Apply to both common difficulty
files; ensure the upgraded member cannot double the family cap. Check every
other use of this same bad alias (naval acquisition/threat census) separately;
do not pretend changing production automatically repairs those searches.
Do not globally redefine the line as one member and silently lose the other.

Acceptance: before/after-upgrade bounded concrete production, unavailable-civ
no-op, no cap bypass, then a fresh Roman replay showing actual MAKE/completion.
Status is ROOT-CAUSE-PROVEN for the identifier, not CLOSED for Roman production.
No additional telemetry was needed or added to establish it.

## False and missed allied attacks: T11 persistent-anchor audit

The persistent anchor correctly binds **player identity**; it does not prove
an attack exists or locate every attack. It is unchanged by T12.

Source-demonstrable defects:

1. `rawai-military.per` LOCAL-RESPONSE-ASSET-FIND's no-attacked-asset branch
   searches one closest enemy's land forces within 48 of home. It tests neither
   enemy action nor the victim. LOCAL-RESPONSE-COMMAND latches that proximity as
   a threat; `rawai-diplomacy.per` calls it "under attack" when >=2 threats and
   no local responders exist. The formal-town request also uses enemy presence,
   not an actual attacked asset. Therefore a nearby fight belonging to Yellow
   can produce Green's own attack claim without anyone attacking Green.
2. The attacked-asset path selects one **farthest** under-attack asset (within
   160), then one `find-attacker` enemy player and nearby same-zone land troops
   within 32. It never establishes that those troops attacked that asset.
   An allied hit plus an unrelated nearby enemy can satisfy it. If the chosen
   player has no candidate, it returns IDLE rather than testing every candidate
   player/attacked asset. Friendly-fire identity and missed-threat bugs remain.
3. `rawai-home-anchors.per` records each player's first ready TC only while
   its stored x is -1. No relocation/death update exists. The ally-help
   FIND-ASSET rules in `rawai-tauntcommands.per` merely copy that original
   anchor; despite the state name they do **not** find an attacked allied asset.
4. Relief SCAN-THREAT checks land military within 48 of that original TC and in
   that original land zone. It iterates enemies but does not establish a victim.
   Own-home relocation in `rawai-homebase.per` updates the owner's home point,
   **not another AI's cached ally point**. A real colony/new-town attack can
   consequently be rejected, while unrelated troops near the old TC validate.
5. Responders must be FREE, idle, same-zone and within 96 of the original anchor.
   This intentionally protects other owners but cannot provide cross-water
   relief. Naval/building attackers and outlying sites do not fit the land-only
   original-anchor query. These coverage limits are not fixed by cooldowns.

The mechanism above is source-proven. **Which particular Green warning used
which branch/hostile is not established by T11's private telemetry.** The user
observed the false warnings; no lack of parser identity disproves that symptom.
Do not assert actual Yellow/Green radius overlap for an individual call without
its coordinates/target. Public timing includes Yellow 14:07 / Green 14:10 and
both 24:04; not every Green call follows Yellow immediately.

Required repair, split from general defense policy: distinguish **incursion**
from **verified attack**; only the latter emits the attack claim. Establish
hostile identity plus victim ownership/current threatened location; do not use
`under-attack` alone as attacker identity. Route the same verified event/location
to relief (or rediscover a genuinely attacked requester-owned asset), rather
than substituting the original TC. Search other valid candidates after a miss.
Preserve bounded FREE/same-zone dispatch and real local defense; cross-water
relief remains a separately recorded missing capability.

Acceptance fixtures: enemies attacking Yellow near Green do not produce a
Green attack claim; allied friendly fire does not validate hostile ownership;
real attack on a relocated/colony asset selects that location; wrong first enemy
does not hide a second valid attacker. Then fresh all-player runtime evidence
must demonstrate correct warnings and actual response. C3 controls frequency
only. D4 provides evidence only.

## STOP flood: exhaustive source-visible writer audit

Reused `tools/audit_ownership_source.py`, its 666-rule inventory, the existing
command-counter map, exact command stream, and ownership reconstruction.
Searched all top-level PER for literal/numeric STOP aliases, dynamic DUC actions,
global unit/reset/retreat calls, scouting resets, group/flag mutation, native
builder/gatherer/repair/explorer/attack admission and settler default orders.
`action-stop = 5`, `orderid-stop = 706`; no alternate numeric/dynamic STOP writer
or active `up-reset-unit`/global reset/retreat was found in addition to this list.
The inventory's zero permission failures is a syntax result, **not** proof that
the engine respects every reservation or that no implicit order can be stopped.

### All explicit STOP sites (T12 counter IDs; T11 order policy is unchanged)

| ID | File / rule start | Selected class/owner and trigger | Relevance to Red's landed settlers |
|---|---|---|---|
| 1, 2 | `rawai-general.per` stale target / non-pending build target | FREE villagers only, excluding boar lurer/tree job; temporary group 0; iterator retains one indexed source, then tests its job. | Inspectable direct candidates if reservation is lost, but intended one-worker selection does not explain the fixed 17-member packet. No evidence permits declaring them impossible at runtime. |
| 3 | `rawai-military.per` idle transport escort release | Escort group 9 warships, then release; escort timer. | Not the settler class under the acquisition contract. |
| 5 | military MIGRATION-LOAD-PARTIAL | Group 11 nongarrisoned shore stragglers; terminal partial manifest. | Can STOP settlers once, then state leaves this branch. |
| 6, 7, 8 | military migration cargo-one abort / empty abort / missing hull CHECK-LOAD | Group 11; release/return/IDLE after terminal STOP. | Legitimate terminal candidates, not an identified continuously executing landing writer. |
| 9 | military MIGRATION-VERIFY-SCOUT-LANDING | Group 11, scout mission path; immediately changes state to TASK-SCOUT. | Mining landing uses VERIFY-LANDING, not this STOP branch. |
| 10 | military scout target-missing fallback | Group 11; clear/reset and return hull home. | Different mission/terminal state. |
| 11 | military CHECK-LANDING missing hull | Group 11; release and IDLE. | Hull-loss terminal, not the observed continuing camp negotiation. |
| 12 | military migration general watchdog | Nongarrisoned group 11; unload/return state and 15-second timer. | Can STOP settlers on timeout. No matching four-minute per-tick terminal cadence established. |
| 14 | military assault partial-manifest | Group 4 nongarrisoned stragglers, then rebuild actual cargo. | Separate passenger owner; no source-only proof that group 11 was reassigned here. |
| 17 | military recovery partial timeout | Group 13 shore stragglers, then bounded sail/unload. | Separate recovery owner. |
| 18, 19 | military LOCAL-RESPONSE-COMMAND wall/gate builder evacuation | FREE, nongarrisoned, currently building wall/gate, not boar lurer; then safe-TC garrison. | Genuine additional settler STOP writers, but not all reserved island settlers merely waiting for a camp. |

Nine scout reset sites (IDs **4, 13, 15, 16, 20, 21, 22, 23, 24**) occur in
migration scout claim, assault initial/partial claim, recovery claim, local
defense, raid, common ownership suspension, severe defense and allied relief.
Each requires `gl-owner-explore-suspended NO`, zeros explorer admissions and
sets it YES. The only normal release requires phase <4 and empty compatible
groups. This is not a source-visible late-game per-pass reset loop. Check
actual counts, not the command's mere existence. IDs **90/91** count native
attack exclusion reset/type calls; those run each pass and can affect native
admission, but they are not explicit STOP instructions. The type-removal loop
is finite. R2's 55,148 STOPs predate this T11 exclusion implementation, so the
new exclusion list cannot explain the entire historical flood by itself.

Other reviewed boundaries: group reset/flag release is bookkeeping, not an
explicit STOP instruction; migration gather/build/reboard/default orders can
be superseded or rejected by native tasks. Native gathering/return-of-cargo,
builder assistance, hunter retasking, repair and explore admissions therefore
remain part of the causal audit rather than being dismissed by flag checks.
The current DE group domain is 0..19; the old 0..9 source comment is stale,
not proof group 11 is invalid (see TASK-OWNERSHIP.md).

### Earliest reconstructed Red divergence, not just totals

- Full T11: **152,771** STOP-706 packets. The exact 17-settler signature occurs
  **7,561** times, 55:17–59:19, rather than just one timeout STOP.
- First fixed-signature packet: sequence **728918**, **3,317,112 ms**.
  The "18 settlers landed" / recovered-zone messages are sequence
  **728945/728946**, **3,317,234 ms** — the flood starts **122 ms earlier**.
- Immediately before that first fixed group packet, individual settlers are
  repeatedly ordered to Red home TC **4503**, point **(204,16)**, interleaved
  with smaller STOP groups. There are **3,592** such TC-targeting ORDER packets
  involving these settlers during 55:00–59:30; **10,209** STOP packets in that
  window intersect the same 17 IDs (including the smaller groups).
- The repeated group cadence continues through camp negotiation and recall.
  It is not explained by the later 57:25 placement request beginning a loop.
  An ORDER to a TC alone does not tell us whether native return-of-resources,
  garrison, another right-click task, or a script generated it.

**Status: INVESTIGATING.** The actual STOP producer is not established by a
source match or tagged packet. There is no justification for calling C1, the
counter bundle, or native-exclusion speculation a STOP fix. No new tracing
build is proposed: retain/use the existing command-boundary, ownership and
nonzero writer counters, correlate exact player/time/manifest, and pursue the
earlier home-TC task transition. Do not disable all STOP or all native economy.

### Separate source-proven native-admission leak

`rawai-ownership.per` disables native builder assistance once when worker hold
becomes active. Later in the load order, `rawai-homebase.per`'s no-shepherd/
no-hunter branch can set `sn-disable-builder-assistance` back to **0**, without
testing worker hold. Since `gl-owner-native-hold-applied` is already YES,
ownership does not reapply the hold on following passes. The reverse restoration
can also temporarily disagree with the current animal-food policy.

This is a concrete competing-writer defect in the promised boarding admission
hold. Repair the common writer contract (including exact restoration/policy
reconciliation) in one causal patch and test both load order and hold release.
**It does not prove builder assistance issued Red's STOPs or explain his camp
failure:** the migration releases worker hold before that colony placement.

## Red's 18-settler landing without a foundation

T11 proves landing (55:17), live stone anchor 739, accepted PER placement
requests (57:25/57:49), two rejected offsets, and 58:09 terminal failure.
It does not contain a matching Mining Camp BUILD/foundation. `up-can-build`
plus `up-build place-point` is not a concrete builder/foundation success event.

Source path: landed owner group 11 -> resource anchor -> placement-owner wait ->
four +/-3 offsets -> native build queue -> 20-second WAIT -> exact pending
foundation search -> assign reserved builders -> completion -> retask/release.
Settlers are not explicitly selected as foundation creators at `up-build`;
they receive direct construction orders **after** a foundation is found.
Thus native admission and placement remain real unproved links, not satisfied
by the existence of eighteen builder-capable units nearby.

There is also the already-recorded **different**, source-proven Purple race:
global `up-pending-objects >=1` advances to ASSIGN, an empty local same-zone
foundation search immediately fails, and the intended wait/retry is bypassed.
Purple's one-second build-to-reboard evidence matches it. Red's twenty-second
placement waits and absent BUILD do **not** establish that same race as his
cause. Fix the race separately; do not close Red by association.

Required race repair: pending queue != concrete foundation. Keep the existing
placement deadline and bounded offsets while waiting for an exact owned,
same-zone, near-anchor foundation; only then assign settlers. An unrelated
pending camp or delayed foundation must not immediately recall them.
Preserve the successful T5 Red landing/camp/completion/drop-off as control.
For T11 Red, retain D3's bounded evidence fields and the existing ownership
record; determine native request rejection/creator admission before changing
placement policy or declaring the STOP flood its cause.

## Validation and adversarial disposition

- PASS this audit: existing 14 focused T11/T12 tests; read-only ownership
  inventory (666 sites, zero direct permission-pattern failures); direct DAT
  prerequisite/producer/family inspection; all-player MAKE/call/STOP queries.
- No full suite rerun: no runtime or test implementation changed. Previous
  204-test result remains historical, not fresh engine validation.
- No new T12 replay or game launch. Runtime acceptance remains PENDING.
- PASS: 33 replay benchmark validations after wording corrections; diff
  whitespace check. Read-only deployment check matched all 78 runtime files,
  no copied/missing/different/unexpected files, full SHA-256
  `A1757B8E758A077BE0F96C18292AF124AD1747EF1F6DBB6D04E8F730B283A345`.
- ACCEPTED: distinguish U/S/D from causal fixes; reject blanket "causal commits".
- ACCEPTED: wrong Q family is source-visible; do not demand telemetry first.
- ACCEPTED: cooldown cannot repair victim/location identification.
- ACCEPTED: builder-assistance hold has a later competing writer.
- REJECTED: same identifier fault explains Octeres; it uses concrete 1884.
- REJECTED: Purple's queue/foundation race proves Red's absent BUILD cause.
- REJECTED: 666 guard-pattern passes prove STOP cannot reach settlers.
- DEFERRED attribution, not canceled work: exact Octeres rejection, native STOP
  producer, Red foundation creation failure, individual Green warning identity.

## Disposition and return to the authorized backlog

### T12 changes worth retaining

C1 fresh boarding clock; C2 exact command-time source/target reconstruction;
C3 request cooldown as a spacing-only fix; U1 smaller taunt area; U2 explicitly
requested bounded radius growth with its limited sampling claim; C4 converted
target guard if the watcher remains. Preserve close naval attacks, ordinary
combined land attacks, successful full/partial lifts and escort ownership.
All gameplay acceptance is still FIXED-PENDING-RUNTIME or policy-pending-runtime.

### T12 diagnostics worth retaining

D1 bounded writer counters, D4 request/response identity, D2 concrete availability/
trainability/resource evidence for the still-unresolved Octeres gate, D3 request/
timeout evidence for concrete foundation creation, and D5 provenance/tests.
No additional probe is needed to identify the Q alias or the allied-location
contract faults. Correct Q probe interpretation with the production repair.
D3 must remain explicitly search-mutating; prefer taking the worker snapshot
from an existing legitimate selection when touching that path, rather than
adding more search consumers. None of these diagnostics counts as resolution.

### Anything that should be reverted

S1's unevidenced ordered-all-enemy priority/iteration change, **selectively**;
do not revert the entire naval commit and lose C2/U2. Remove the unused watcher
goal when making that cleanup. Correct the documentation/benchmark's blanket
causal wording now. No runtime revert or deployment is performed by this audit.

### Source-proven fixes before backlog integration

1. Replace the wrong Q production family with bounded concrete 1870/1750
   admission/counts, both common files; audit dependent bad-alias selectors.
2. Repair the builder-assistance hold's later writer override/restoration.
3. Repair verified-attack versus proximity classification and original-TC-only
   relief location. Preserve genuine local defense/owner boundaries; do not
   smuggle in cross-water relief or a general attack rewrite.
4. Repair the independently proven pending-queue/concrete-foundation race.

One causal patch and focused falsification/acceptance at a time. Continue the
STOP, Octeres and Red foundation investigations using existing evidence while
these source defects are addressed; their unresolved state is not permission
to guess a behavioral patch or repeatedly ship tracing builds.

Then resume the already-authorized backlog in HANDOFF's **Authorized post-T7
work**: corrected bank-gated 100/500/1000 aid tiers; independent Imperial Market
purchases; isolated Wonder controller with the documented source corrections;
Port strategic-number work. Offline salvage D is already integrated. Keep
animal-food recovery, cross-water relief, transport geometry and deferred crash
work explicit. No whole-commit salvage, protected attack/transport redesign,
canonical-directory switch, or implicit deployment is authorized by this audit.
