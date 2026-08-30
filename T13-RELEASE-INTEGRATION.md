# T13 release backlog integration — 2026-08-31

## Starting state and authority

- Authorized recovery checkout and Git root: `G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-transport-only`.
- Branch: `recovery/p3b44-transport-only`; starting HEAD `37a310872dccabc52db02962509f76f813ba4f3a`.
- Canonical ordinary repository remains `G:\Projects\Codex\Rome at War AI\.pr-work\Rome-at-War-AI`. No checkout/branch switch, clone, or replacement occurred. Continue editing the authorized recovery checkout for this milestone.
- Initial changes were the intentional prior T12 audit documents/benchmark wording, committed first as `77ccb5b`. No unrelated user changes were discarded.
- Installed starting build: **RAWAI-P3B44T12:457**, 78 files, aggregate SHA-256 `A1757B8E758A077BE0F96C18292AF124AD1747EF1F6DBB6D04E8F730B283A345`.
- The user's pre-backlog directive took precedence; its sections 0–4 were committed and focused-tested before the rest of the queue. The later integration directive authorizes one integrated deployment, superseding the earlier audit-only deployment prohibition.
- Immutable P3B44 control `8ec870075d08fcac98bad55b4ff045bf7abbc42e` was untouched. No data-mod payload, replay, savegame, dump, or external binary was added.

## Completed queue

All gameplay outcomes below are **FIXED-PENDING-RUNTIME**, not CLOSED. Policy additions are implemented, awaiting fresh gameplay acceptance. Tests execute selected source rules where practical; they do not emulate pathfinding/native queues.

| Item; prior status | Evidence/provenance and implementation | Commit | Focused PASS / acceptance still required |
|---|---|---|---|
| T12 S1; SPECULATIVE | `rawai-military.per`, custom constants: restore nearest-enemy capital targeting, remove unproven ordered iteration. Preserve 48→96→192→255 inactivity radius, command-time identity rebuild, converted-target guard. | `2918ec9` | 14 T11 tests + PER. Preserve working capital target selection in fresh play. |
| Heavy-reme alias; ROOT-CAUSE-PROVEN | `rawai-military-units-common*.per`, military, navy diagnostics, custom/unit constants, naval validator. DAT concrete IDs 1870/1750 replace live `-282` turtle-line operands. Combined queue-aware family census/cap; upgraded trainable form preferred, base fallback. All seven same-family searches repaired. Octeres1884 untouched. | `82a6bf9` | 4 concrete-family fixtures, 14 T11 tests, naval/PER. Demonstrate bounded Roman production. |
| Builder ownership; ROOT-CAUSE-PROVEN | `rawai-ownership.per`, homebase: later animal-policy writers cannot undo active worker hold. Hold reasserts assistance disable; release derives current hunters/shepherds, not a saved flag. | `21c810f` | 2 actual load-order fixtures, 27 ownership tests, PER. No claim this identifies the 7,561-STOP producer. |
| Allied identity/location; ROOT-CAUSE-PROVEN source faults, historical incidents unresolved | New `rawai-attack-verification.per`, loader, military/diplomacy/taunt commands/custom constants. Bounded enemy/candidate scan requires hostile attacking an exact victim-owned live asset. Claim and relief use that asset point, not original TC. Invalid first candidate/enemy does not stop the scan. Revalidate target identity at dispatch; preserve FREE/same-zone responders. Ordinary proximity defense remains an incursion, not an attack claim. | `4874ea7` | 8 executable identity/location fixtures, 14 T11 tests, 27 ownership tests, PER. Fresh real/false attack cases required; cooldown alone was not a detection fix. |
| Migration pending/foundation race; ROOT-CAUSE-PROVEN | Military/custom constants: retain requested point; search concrete owned matching type/zone near point AND resource anchor. A global pending count no longer advances assignment; absent local foundation stays in existing 20-second/four-offset lifecycle. Existing build/completion/retask/release chain retained. | `b71c6dd` | 4 foundation fixtures + PER. Preserve T5 Red complete colony lifecycle. Does NOT identify T11 Red's no-foundation cause. |
| Recovery unload loop; OPEN → supported fix | Military/custom constants: unbounded 15-second RECOVERY-CHECK unload writer now has two original-point retries, one retained boarding-origin fallback, then exact-hull terminal quarantine. Occupied quarantine retains ownership without further unloads; never overwrites another hull. Empty/dead cleanup preserved. | `60c33d5` | 4 actual-rule recovery fixtures + PER. Fresh failed recovery must terminate command issuance; ordinary route/landing unchanged. |
| Palintonon pack; ROOT-CAUSE-PROVEN API misuse | Two military sites used `action-pack` with `up-target-objects`, documented as action-none. Use `up-target-point`, preserving FREE selection and conversion wait. | `f10912c` | 1 packing contract (7 prerequisite fixtures total), PER. Verify actual packing and reacquisition. |
| A — tiered aid; approved waiting policy | Manual `81ce73d22438750adb0ce77f6c13bbec90b7ca63` + operand repair from `90287ea6106dace6fe043309ad5b73e3773f3831`. Trade/custom constants: <100 current stock required for every tier; lifetime collected <500/500–999/≥1000 selects 100/500/1000. Independent 120s resource and 10s shared deadlines. Nominal donor reserves retained; numeric self exclusion; all unfulfilled taunts consumed this pass. Speaker identifies sender; formatted player label identifies recipient. | `171a69d` | 4 aid-policy fixtures + PER. Verify automatic tiers, multi-ally replies and no delayed gifts. |
| B — Imperial Market; approved waiting policy | Six independent critical/operating wood/food/stone rules manually extracted from `0e1169f54a3d06fe1cd6c1f76e32714e3e835ec7`; 15s serialization and historical price/resource limits. No `gl-land-target-needs-transport` dependency. The abbreviated hash in the pasted directive was malformed; existing audited Git commit resolved it. | `d7a9660` | 2 Market fixtures (6 with aid), PER. Verify purchases under high gold and critical deficits. |
| C — Wonder; approved waiting policy with known historical faults | New isolated `rawai-wonder.per`, loader/custom constants, two saving purchases in trade. Adapt same historical commit: Standard + Imperial + ≥60:00; explicit baseline; three 300s quiet windows; both-team cumulative loss counters; staggered candidates; allied Wonder suppression; 60 villagers; 1400w/1500g/1400s; worker-hold/home-defense admission; three 180s placement attempts then 900s cooldown. No protected attack/transport/defense writers. | `f62f77c` | 7 executable Wonder fixtures + PER; aid/identity reruns PASS. Verify actual Wonder foundation/completion and serialized saving purchases. |
| Port settings; approved waiting policy | SN/homebase: proximity +10000, minimum body area600; rear-biased first Port, front-biased second on water maps, standard mode after two complete Ports. Existing same-water preference retained. | `8010cf6` | 1 Port contract (7 policy tests then), PER. Verify shoreline outcomes on fresh maps. |
| Integrated literal budget; caught before deployment | Aid reply literals allocated 120 times, exceeding project payload budget at1538. Twelve shared `str-aid-*` constants preserve identical replies and reduce total to1430/1500. Current-payload budget regression added (historical writer-trace tests alone did not cover this build). | Final integration validation commit | Current payload budget PASS; no raised limit, no new tracing build. |
| D — offline analysis; already integrated | `9b3dded` remains present. Reused exact-packet/ownership evidence and existing all-player boarding windows; did not add a competing replay parser. | Existing commit | Historical packet tests PASS. |
| Hunting; OPEN / optional source audit | `rawai-hunt.per`: zero hunters cannot enter ordinary retry, and retry rejects a lurer whose target changed even if saved boar still exists. However Yellow22–24's exact post-garrison state, target/carcass survival and selected path remain unestablished. | No behavioral patch | Keep OPEN; correlate saved target/lurer and garrison transition before safe FREE-worker reacquisition. |

## Important policy limits and open defects

- Wonder uses cumulative **all-unit** deaths as a conservative proxy: five civilian OR military deaths reset the sequence; three building losses do likewise. Replacement production cannot cancel those losses. It is not a civilian-only statistic. Continuing military attrition can postpone a Wonder even without territorial progress. Small losses accumulate across windows. Counter/team-membership decreases also reset safely.
- Port surface area is not channel width. Front/back means toward/away from map center, not opposite sides of an island. This supported preference cannot certify cliff access, open crevices, or two opposite shores.
- Exact historical STOP producer remains **INVESTIGATING**: 152,771 STOP706 records, including7,561 to one Red17-settler group. The earlier home-TC4503-directed transition remains the lead; existing command counters/ownership evidence must be reused. No blanket STOP/native-economy disabling and no further tracing build was added.
- Octeres rejection remains **INVESTIGATING**. Availability/prerequisite/role/cap/resources/producer/rotation/concrete train gates have source paths; no exact failed runtime gate is established. The bad Quadrireme alias does not explain Octeres.
- T11 Red18 settlers/no concrete Mining Camp remains **INVESTIGATING**. The separate Purple asynchronous-foundation race is fixed in source, not evidence that Red shares that cause.
- Friendly-fire/false and missed attack symptoms remain runtime-unverified. The new exact victim/hostile path fixes identified source faults; it does not retroactively prove every Green warning's cause. Cross-water allied relief is still unsupported.
- A second loaded recovery hull may remain owned and command-free while the one detached quarantine slot is occupied. No claim that this rescues every blocked hull.
- Crash investigation remains separate/deferred by the user's transport priority; no crash fix or attribution was made here.

## T12 disposition

The complete one-category-per-change audit remains [T12-SOURCE-AUDIT.md](T12-SOURCE-AUDIT.md).
Retain C1 live boarding clock, C2 command-list rebuild, C3 cooldown spacing, C4 converted-target guard, U1 two-tile deletion area and U2 adaptive naval radius. Retain bounded D1 STOP/reset/native-exclusion counters, D2 heavy-navy gate diagnostics, D3 foundation-boundary diagnostics and D4 attack-claim provenance as diagnostics only. S1 ordered capital priority/iteration was selectively reverted. No other speculative policy was smuggled into this integration.

## All-player T11 assault funnel

Evidence: replay `20260830-211106`, build **T11:456**, SHA-256 `088EC5FBFCCB6DDABEAC85BB7181B38B883F05DFDCB1A06FC0EAD46ECD0B904F`. This is not runtime validation of T13.

[T13-ASSAULT-FUNNEL.json](T13-ASSAULT-FUNNEL.json) contains all39 identified assault boarding episodes, their hulls, boundaries, outcomes and reasons. Derivation reuses `.analysis/p3b44t11-exact.json` and `.analysis/p3b44t11-task-ownership.json`: join by player/exact hull, stop each episode at the next recorded boarding start for that hull regardless of owner, correlate load terminals and later hold/landing events. Duplicate legacy/RAW44C ready messages are not counted as two missions.

The broader83 boarding windows comprise39 confirmed assault,29 migration and15 unresolved/recovery/relic. An observation of zero identified assaults is not proof the player never attempted activation.

| Visible color | Assault boarding episodes | Useful loads | Boarding aborts | Pre-departure screen recalls | Landing timeouts | Completed landings | Replay-ended unresolved |
|---|---:|---:|---:|---:|---:|---:|---:|
| Red |7|5|2|5|0|0|0|
| Green |0|0|0|0|0|0|0|
| Yellow |0|0|0|0|0|0|0|
| Purple |10|8|2|5|0|2|1|
| Orange |11|11|0|9|2|0|0|
| Cyan |2|2|0|2|0|0|0|
| Blue |9|7|2|7|0|0|0|
| Gray |0|0|0|0|0|0|0|
| Total |39|33|6|28|2|2|1|

Actual controller order places screening **before hull departure**, not after it:

1. Eligible opportunity: denominator not recorded; cannot infer it from absence of a load.
2. Mission activated / passengers reserved: at least39 identified episodes with concrete load commands.
3. Useful load:33 (29 full,4 useful partial);6 boarding aborts.
4. Screen acquired and route/beach cleared:4;28 recalls;1 still unresolved when replay ended.
5. Hull departure/landing command stage:4; these are controller/command witnesses, not four independently measured physical departures.
6. Landing complete:2 Purple;2 Orange landing timeouts. Empty-hull notice alone is not delivery proof.
7. Useful troops ashore / enemy-land task issuance:2 correlated concrete postlanding orders, five reserved units at59:44 and ten at63:27, both toward(43,112). Source applies aggressive stance before release. Subsequent useful combat is not independently demonstrated by these packets.

Screen recall reasons: no screen ship8; route waypoint timeout5; beach approach timeout6; route defensive fire1; landing defensive fire4; defended beach3; scout lost1. Thus19 are acquisition/progress failures and9 are danger/loss cases; do not label all28 illegitimate or physically viable routes.

**Single RC transport blocker: loaded-assault route-screen acquisition/progress before departure.** It is the largest observed attrition stage (28/33 useful loads, with19 acquisition/progress cases). Next establish the first divergence in that stage using exact screen ownership/command/position evidence. Do not weaken all threat screening or steal busy ships to force the percentage upward. Fresh T13 evidence must distinguish repaired boarding/departure behavior from this retained screening limitation.

## Validation and non-regression

- Final full suite: **242 tests PASS;0 failures;0 errors;0 skips**. Writer-trace temporary-directory checks required sandbox escalation; rerun passed.
- New focused coverage:7 prerequisite/packing,8 attack verification,4 foundation,4 recovery,8 aid/Market/Port/budget,7 Wonder tests. Included in242, not added twice.
- PER structure/operand/32-element checks: PASS. All source/runtime files checked.
- Ownership inventory: **671 sites;0 direct permission failures**; generated inventory refreshed. Ownership policy and command-counter generators remain exact matches.
- Naval doctrine/generation: PASS for34 civilization scores and queue-safe role/family caps.
- Strategy: **1149/1156 historical** and **1152/1156 Extreme** matchups adjusted; zero validation errors.
- Evaluation/workbook: **34×20 ratings**,680 evidence rows,340 naval rows PASS. Only source provenance hashes changed; ratings/focus policy were not revised.
- Civilization generator:0 pending updates after newline-only normalization in Germani/Han/Kushans/Mauryans. No semantic change in those four files.
- Replay benchmarks: **33 PASS**. These do not validate T13 gameplay.
- Current plain payload: **1430/1500 string literals;0 writer-trace literals**. Project safety budget, not an assertion of engine allocation capacity.
- `git diff --check`: PASS. No intermediate runtime was deployed.
- Adversarial read-only self-review: accepted/fixed the saving-state resampling/election-reset edge, sticky Wonder placement retry edge, literal-budget overflow and stale tests/provenance. Rejected blanket STOP disabling, Octeres identifier substitution, unsafe removal of screening, and treating T11 Red as the proven Purple race.

| Regression of previously working behavior? | Source/fixture result | Fresh runtime result |
|---|---|---|
| Ordinary attacks | NO detected | Not run; cannot claim NO in engine |
| Ownership architecture | NO detected | Pending |
| Full/partial assault lifts | NO detected | Pending |
| Migration landing / T5 colony lifecycle | NO detected | Pending |
| Relic ferry | NO detected; policy unchanged | Pending |
| Departure clearance | NO detected; policy unchanged | Pending |
| Genuine defense | NO detected; exact-identity fixtures PASS | Pending real/false attack comparison |

## Integrated deployment identity

Candidate: **RAWAI-P3B44T13:458**, **80 plain runtime files**, aggregate SHA-256 **A260148B2998E72203883BF34578D96B9AD6B72A561857C89ADBB28F23C96FB6**.

Deployment target: `C:\Users\LostSoul\Games\Age of Empires 2 DE\76561198053747760\mods\local\Rome at War AI\resources\_common\ai`.
Final installation result is recorded in the current section of [HANDOFF.md](HANDOFF.md). No writer-trace compilation overlay, extra runtime payload, push or PR mutation is part of this session.

BACKLOG INTEGRATED — RC TRANSPORT BLOCKER IDENTIFIED
