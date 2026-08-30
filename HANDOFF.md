# Rome at War AI handoff

## CURRENT — T11 source-first ownership implementation, 2026-08-30

This section supersedes the diagnostic-stage priorities below. User directive:
`18529df3-3d8e-4635-84a9-871e505b439d/pasted-text.txt` (source-first ownership).

- Canonical ordinary development repository remains
  `G:\Projects\Codex\Rome at War AI\.pr-work\Rome-at-War-AI`.
- Authorized **experimental recovery checkout**, and location to edit for this
  objective: `G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-transport-only`.
  It does NOT replace the canonical repository. Branch:
  `recovery/p3b44-transport-only`. Starting HEAD:
  `a5de7d85bad71f36f4c8903747908d71ac164a7e`, clean before implementation.
  Resolve current implementation/documentation HEAD with `git rev-parse HEAD`;
  deployed source identity is independently fixed by the hash below. No new
  clone/worktree, branch switch, push or PR update was performed.
- Immutable attack control remains clean at
  `8ec870075d08fcac98bad55b4ff045bf7abbc42e` in
  `.recovery-work\P3B44-attack-baseline`. Do not edit it.
- Build **RAWAI-P3B44T11:456**, **73 plain-source runtime files**, SHA-256
  `2CA656510A99D71A9C5A2CB5014FC3138904D120E806269127DEB5FF5824DABF`.
  **Installed and independently rechecked:** all 73 files match, with no missing,
  different or unexpected runtime files, at
  `C:\Users\LostSoul\Games\Age of Empires 2 DE\76561198053747760\mods\local\Rome at War AI\resources\_common\ai`.
  R4:455 was installed at session start. T11 does **not** use `--writer-trace`
  or a lifetime quota. A fresh match is required; an existing game is not T11.
- Status: **OWNERSHIP IMPLEMENTED FOR SOURCE-PROVEN PATHS — NATIVE BOUNDARY
  REQUIRES ONE DISCRIMINATING TEST**. Gameplay is not CLOSED.

### Implementation / evidence

TASK-OWNERSHIP.md contains the full owner/fault/compatibility matrix and review
dispositions. OWNERSHIP-SOURCE-INVENTORY.md enumerates **662 relevant current
rule sites**, including actual selectors, commands/delegations, reservation
mutations and permission filters. `tools/audit_ownership_source.py --patch`
and `tools/generate_ownership_policy.py` emit reviewable patches for these
generated artifacts. The one-use transformation helper was removed.

- Removed global reset/retreat/ALL-unit STOP from routine land/naval defense,
  siege escalation, loss regroup, periodic-loss recovery and taunt retreat.
  R1/R2/T8 already establish reserved-passenger intersections.
- Separate migration 10/11, recovery 12/13, relic 14/15, naval Scout 16 and
  relief 17 from assault 3/4, raid 8, screen 7 and escorts 9. Capital siege's
  Juggernaut/Octeres slot 2 remains an intentional single-controller alias.
- Direct writers recheck self/ownership. Worker selectors exclude all
  reservations and the active boar lurer. Pass-start group hygiene removes
  foreign/other-owner references before legacy release mutations. Partial
  migration releases failed shore passengers, retaining only actual cargo.
- Native exploration is zeroed AND reset before Scout-capable claims. Native
  build/percentage/hunter admissions pause during worker boarding; assistance/
  repair settings are saved/restored. No claim that a flag is an engine lock.
- Native attack type exclusions are rebuilt from reserved groups before normal
  and taunt dispatch. FREE same-type units temporarily wait too; ordinary
  attacks are not globally disabled while unrelated missions run.
- Routine defense uses <=8 FREE idle responders. Severe defense requires >=8
  live military from one enemy within home 24 and the same land zone. It may
  cancel a wholly local ashore assault/raid/relief owner, release, then acquire
  <=16 responders. Loaded/split/remote missions stay protected.
- Persistent first-reliable TC coordinates for all eight players survive TC
  destruction. Allied help checks actual live enemies around that anchor,
  claims <=12 compatible responders, checks actual count/target, then promises
  help. No arbitrary-villager or allied-under-attack substitution.
- Existing RAW44B/C/R mission evidence remains, rearmed for later missions.
  Old writer tests/maps are archival against immutable source `a5de7d85`, not
  current source with obsolete writer-site IDs. Blue's historical STOP producer
  is still unidentified; that did not block these source-supported fixes.

### Validation and limits

- **PASS:** 190 regression tests, including 27 ownership-contract tests. These
  execute actual filters, reservation/release operations, partial manifests
  and native-exclusion relative jumps, plus source invariants for enemy/zone,
  anchor persistence, actual responder count and generator synchronization.
- **PASS:** PER structure/operands/DE group domain 0..19; attack/strategy
  synchronization (1,156 matchups); naval doctrine; workbook round-trip;
  32 replay benchmarks; all 662 ownership sites audited with zero unguarded
  direct writers/global resets remaining; `git diff --check`.
- **PASS:** adversarial read-only review with accepted findings corrected:
  split/loaded severe release, exact hostile selection, converted group
  references, partial shore-passenger release, loop RuleDelta and ambiguous
  generated patch context. Tests now protect these corrections.
- Formatting-only restoration preserved original unchanged-line PER endings.
  String budget: 1,421 literals, zero writer literals, conservative eight-player
  projection 11,368 under the project's existing budget. This is not measured
  engine string-table capacity or an engine compilation claim.
- **PENDING:** fresh engine compilation and gameplay acceptance of T11.
  Existing R1/R2 and static tests cannot validate this new runtime.

### Unresolved defect ledger / next actions

| Defect | Status | Direct evidence / implementation | Acceptance / next action |
|---|---|---|---|
| Routine/convenience recall steals passengers | FIXED-PENDING-RUNTIME | Source callers + R1/R2/T8; compatible local/severe response implemented | No ordinary recall of active missions; genuine severe defense works |
| Exploration steals boarding Scouts | FIXED-PENDING-RUNTIME | R1 explore 705; budgets zero + reset before claim, positive writers gated | Reserved Scouts board; early exploration can resume after release |
| Direct worker/group conflicts | FIXED-PENDING-RUNTIME | Unsafe selectors/aliases + T7 symptoms; common guards, distinct groups, admission hold | Workers retain task; partial cargo stays owned; released units can work |
| Native worker/attack queued reassignment | INVESTIGATING | Documented suppressions/type exclusions implemented; no per-villager lock or proof of queued-order cancellation | ONE controlled T11 preserved-lobby replay, occupancy-aware early/terminal samples |
| Allied help after original TC destruction | FIXED-PENDING-RUNTIME | Persistent anchors + actual enemy/responders | Help at living/destroyed original TC; no false promise without hostile/responders |
| Historical Blue Scout STOP writer | INVESTIGATING | R2 stream established repeated STOP; old quota exhausted before event | Check recurrence in T11; not a prerequisite to implementing proven source fixes |
| Congestion, landing geometry, unload spam, Port placement, boar resumption, drop-site race, Market/Wonder salvage, crash, landing memory | KNOWN ISSUE — POST-RELEASE | Preserved observations below; deliberately no unrelated behavioral changes | Outside this ownership release unless build is fundamentally unusable |
| Existing Palintonon pack call through up-target-objects action-pack | KNOWN ISSUE — POST-RELEASE | Source/API inspection: that action is unsupported on this command | Separate supported packing correction after ownership acceptance |

1. Start a **fresh** recorded T11 match with the preserved authoritative lobby;
   identify players by selected/visible colors, never slots. Confirm T11:456.
2. Audit every reasonably reconstructable transport/migration/scout/relic/help
   episode across all players. Preserve P3B44 combined attacks and T1–T7 full/
   partial lifts. No own-TC flood, shoreline-fishing flood or routine recall.
3. Test the precise native boundary in TASK-OWNERSHIP.md: distinguish a harmful
   command to an ashore reserved unit from STOP after garrison. Existing native
   gathering/building/queued attacks may still bypass new admission controls.
4. Keep noncritical discoveries in KNOWN ISSUE — POST-RELEASE. Do not start
   another unrelated development cycle before ownership acceptance.

## Historical R4/R2 checkpoint (superseded by T11 above)

## Release-blocking recovery completed — ownership work resumes

**R4 release checkpoint, 2026-08-30:** requested invariant recovery, separate
commits, full static validation and verified deployment completed BEFORE R2
analysis. A: `3b8d534d1d1be48c1bb5a179229c353e53c37d4d`. B guard tests:
`34a53f6055ecd324d7b95368613c37871fb31fde`. The existing R3 work was preserved
in `ea8a382cb2919bed9b02fdc263f7cd3687afb886`; no new worktree or PR update.
Starting branch `recovery/p3b44-transport-only`, HEAD
`544bd843065245235227018635947e48a077f715`, installed R3:454 hash
`DD38785FB1D67813D6F9E8BF88E7D88D8B86B9C441460806C38AE10CC279CBB2`.

- Runtime diff: only hunt 28 -> 16, two operands. Food 12 and all eight self
  fallback exclusions were already present; B required tests, not duplicate
  code. Both cited historical fixes are ancestors of the pre-task checkout.
- Read-only adversarial/protected-diff review: PASS. Attack behavior changed
  beyond self-exclusion: **NO** (no attack runtime delta at all). Transport:
  **NO**. Ownership: **NO**. Migration: **NO**. Farm staffing/gather percentages:
  unchanged. All other PER files match `ea8a382` byte-for-byte. Existing T9/R3
  diagnostics are preserved, not newly implemented by this release.
- PASS: 163 regression tests (8 recovery); PER structure/operands/domains;
  attack/strategy (1,156 matchups); naval doctrine; workbook round-trip;
  31 replay benchmarks; `git diff --check`. Post-marker compiled validation
  and all 17 writer-trace tests PASS. The first sandboxed baseline run had a
  temporary-directory permission error; authorized rerun passed all 155.
- Installed **RAWAI-P3B44T10R4:455**, all **68** files independently verified,
  no missing/different/unexpected files. Source/install aggregate SHA-256:
  `C7554880AC95FE2DBB80325ABEA9130CF91C9BE9A845FC5E291A7AEDEBD57B15`.
  Plain-input SHA: `FA9E0C54BD5395B5B3EB79E19F31FE3CEE44DF008C47CCEF6124CB3C024917D1`.
  Writer-map fingerprint: `806FAFCA8EABC51B70FECA1B0F63937806BCA82A4BF1521F00B3538A9242DC90`.
  Only generated entry identity, init marker and economy file were copied.
- **FIXED-PENDING-RUNTIME**, not gameplay CLOSED. R2 predates this release and
  cannot validate hunt 16. All-player fresh-runtime acceptance remains the
  historical fish/farm and self-target/TSA flood checks specified below.
- Next: analyze supplied R2 (`20260830-182330`) with its archived R2 map, then
  continue TASK-OWNERSHIP.md. No new congestion/salvage/Port micro-fix first.

### R2 evidence audit after release — latest session

Runtime release HEAD: `4bff811431ac12de63fa1fdf7c90eccf4dcb383e` (R4:455).
This following evidence-only update does not change that runtime. Resolve
current documentation HEAD with `git rev-parse HEAD`. No push/PR update.

- Replay `SP Replay v101.103.48987.0 @2026.08.30 182330.aoe2record`,
  25,570,711 bytes, SHA-256
  `06C62FDBD658D27DDDE682FB49A8F9A90F112E7CC0D7FDD33411A935762E904E`.
  Duration 62:04. No parsed resignation; do not infer crash/end cause.
  Selected-color metadata validates the preserved Roman Red/Green/Yellow/
  Purple team versus Orange Picts/Cyan Britons/Blue Germani/Gray Gauls.
  Extreme, population 400, Fast 2.0, shared exploration; RMS id 50.
- All-player command sweep: 282,006 retained exact events, no decoder failures.
  Hull census was expanded beyond old load/unload phases using direct hull
  telemetry and passenger samples, retaining load-only failures too.

| Color | Identified hulls | Load packets | Raw loading windows |
|---|---:|---:|---:|
| Red | 4 | 24 | 7 |
| Green | 2 | 19 | 4 |
| Yellow | 2 | 16 | 2 |
| Purple | 2 | 17 | 11 |
| Orange | 1 | 14 | 7 |
| Cyan | 1 | 5 | 2 |
| Blue | 4 | 36 | 9 |
| Gray | 4 | 29 | 16 |
| Total | 20 | 160 | 58 |

- These are raw reconstructed windows, NOT 58 fully identified missions:
  19 assault-ready, 7 migration-full, 3 assault-partial, 1 migration-partial,
  3 assault-abort, 4 migration-empty-abort, 17 unload-bounded and 4 lacking a
  recorded terminal. Some missing boundary messages merge missions. Purple's
  additional partial-departure count 9 at 48:02.832 belongs inside an
  unload-bounded window because its normal hull-specific terminal is missing.
  Full/ready does not prove exact selected membership or productive landing.
- **Direct recall evidence:** all 76 retreat packets match existing RAW44O
  labels: source 1 land-defense 56, source 2 naval-defense 6, source 3 siege escalation
  12, source 4 loss-regroup 2. Orange priest 33235 starts boarding at 27:26.906 and
  is recalled at 27:37; priest 34388 starts at 37:08.684 and is recalled at
  37:18. Both attempts end in roughly three-minute recovery unloads, without
  outbound relic announcements. Routine recall must respect relic/recovery
  ownership as well as the assault/migration controller goals.
- **Corrected interpretation:** Purple at 48:32.856 is SCREEN-FIND (19),
  after reported nine-passenger partial departure at 48:02.832. Recall includes
  the original ten-unit loading roster but does NOT prove boarding interruption
  or units disembarking. Green at 55:24 includes passenger 41942 during
  WAYPOINT-WAIT (29), also route-stage evidence. The earlier user-facing
  wording calling Purple's units queued was explicitly corrected.
- **STOP stream:** Blue scout 4608 receives 283 AI_ORDER 706 packets between
  55:03.414 loading and the 55:12.050 idle-ashore sample; 276 between 57:16.740
  and 57:30.078. Both samples retain group flag 4 and distance 1 to hull 40501.
  This establishes repeated STOP plus failure of that passenger to board at
  the sample, not the exact script/native/delegated producer. Hull-ready
  messages coexist with this missing originally selected passenger. Blue's
  59:52 twenty-unit migration has STOP packets for 16 selected members and
  a partial terminal at 60:21.982 with 3 remaining; occupancy is unavailable
  for each stopped member, so normal post-garrison cleanup remains a possible
  explanation for some of those packets. Do not blanket-label them preemption.
- **Coverage:** before 09:00 each player has only one invocation each of
  setup sites 10/11/12; R1's early recurring cleanup spam is absent. Gray
  exhausts the total quota at 37:00.648, Blue at 48:29.402, Purple at 56:06.164;
  temporary rate gaps also occur. No RAWAI marker or RAW44W map survives.
  Zero players pass fingerprint verification; the new exact writer-source
  attribution remains withheld. Preserve user-reported R2 + archived map/
  deployment evidence, but do not bypass the analyzer's identity requirement.
- **Other outcomes retained:** 7 scout-candidate missions reject all five
  paths; a Green candidate mission records 3 clear points with unload commands.
  One public assault landing-completed window is present. Six relic outbound
  and four return announcements remain positive evidence. They do not close
  every landing/drop-site/route defect, and do not authorize a navigation fix
  in the ownership release.
- **Artifacts outside repository:** `.analysis\replay-20260830-182330-t10r2-full.json`
  and `.analysis\p3b44t10r2-{command-stream,exact,transport-audit,task-ownership,summary}.json`,
  plus `p3b44t10r2-transport-audit.txt`; matching archived
  `p3b44t10r2-writer-trace-sites.json`. Existing `audit_writer_replay.py` now
  includes sample/public hulls and no longer writes hard-coded R1 conclusions.
  Its raw automated classifications must be read with the boundary limitations
  above: a missing terminal does not imply ownership until match end, and a
  later sample from a different hull is not proof about an earlier mission.
- **Status/next:** ownership remains OPEN; actual recall conflicts are already
  established, harmful STOP producer/protection semantics remain unresolved.
  R4 has the delayed identity delivery introduced in R3 but not exercised by
  R2. Verify fresh R4 identity and recovered invariants, then use occupancy-
  aware evidence for the common ownership/preemption implementation. Do not
  re-open historical fallback absence as an explanation: all 8 guards were
  present. New benchmark is evidence-only; 32 benchmark validations PASS.

**Latest user instruction, 2026-08-30:** "Once you receive the R2 replay,
this directive takes all precedence before analyzing the R2 replay data."
R2 (`20260830-182330`) supplied the trigger. Recovery above is complete; the
following retained requirements document the release, not a request to repeat it.
This section overrides conflicting priority/next-action text elsewhere below.

**Pre-edit source/deployment audit:** installed R3 matches all 68 generated
files, SHA-256 `DD38785FB1D67813D6F9E8BF88E7D88D8B86B9C441460806C38AE10CC279CBB2`.
The directive's lost-fix premise is only partially applicable: food already
clamps to 12 and all eight fallback self-exclusions are present, inherited
directly from the two cited commits (both are ancestors of current HEAD).
Commit `078da6527906eec1101a9848cc1fcc4f66555b77` subsequently raised hunt 16
to 28. Restore hunt 16 as now directed, retain food 12 and existing self
guards, and add the requested focused/mutation tests in separate A/B commits.
Do not claim missing self guards caused the current runtime symptom. This
source evidence does not disprove the observed own-TC/passenger behavior.
R1-R3 intentional telemetry/evidence is checkpointed separately BEFORE causal
patches, not silently included in either restoration commit. No new T9 work.

### Recovery B — protection retained; FIXED-PENDING-RUNTIME acceptance

- Historical source: `8998cdedc1b5942ec6b93b60b1f33a0188238c94`; every explicit
  military fallback 1..8 already retains its top-level `gl-self-player-number
  c:!= N` guard. No `rawai-military.per` change is needed or manufactured.
- Historical symptom/cause: self is not ally in `stance-toward`, admitting
  self in an unguarded fallback and producing own-TC TSA orders. Current
  contradictory evidence: these guards were NOT lost; the observed ongoing
  own-TC behavior remains an ownership/runtime investigation, not proof of
  this already-guarded fallback failing.
- Tests: four additional source-executed/invariant tests cover all 64
  candidate/self combinations; valid enemy selectable, self rejected even
  when in-game/non-allied/building-owning; valid current targets retained.
  Removing each guard reproduces self selection and fails the invariant.
  Self identity is initialized once from `my-player-number` before military
  rules; automatic explicit writers are scanned across all runtime files.
  Eight focused A+B tests PASS. No attack dispatch/ranking/ownership changes.
- Audit boundary: other target writers are normal `up-find-player enemy`,
  preferred-target save/restore, and explicit user taunts 61..68. Taunts are
  not automatic fallbacks and remain unchanged. Do not generalize fallback
  exclusion into an unproved claim that no other writer can ever select self.
- Acceptance/next action: validate/deploy the recovered cap plus retained
  target invariant, then fresh all-player self-target/TSA flood acceptance.
  Existing R2 can diagnose pre-fix ownership, not validate the new cap.

### Recovery A — FIXED-PENDING-RUNTIME

- Historical source: `56959e6c45fd688710abc3f167aade7262dd4d2f`.
- Preserved pre-task checkpoint: `ea8a382cb2919bed9b02fdc263f7cd3687afb886`.
- Symptom/cause: historical shoreline-fish/farm command contention from an
  uncapped food distance. Contradictory current evidence: food already had 12;
  only the later hunt-28 deviation needed restoration to the requested 16.
- Implementation: exactly two numeric operands in `rawai-economy.per`,
  hunt 28 -> 16; existing food 12 retained. No other runtime source changes.
- Tests: four source-executed/mutation tests in `tools/test_release_regressions.py`.
  FAIL on pre-patch hunt 28; PASS after restoration. Both caps precede native
  SN publication, preserve within-limit values and mutate only their own goal.
  Protected diff preserves farm staffing, gather percentages, transport,
  migration, passengers, attack/defense and ownership.
- Acceptance/next action: full release validation/deployment after B's guard
  tests; then all-player fresh-runtime checks for historical food/hunt command
  floods. This source change does not establish that R2 contains that cause.

Authority: user attachment
`C:\Users\LostSoul\.codex\attachments\ce70220e-7f9c-4f58-a936-c6dde9510419\pasted-text.txt`,
SHA-256 `81BBF627F3AC41D9A3BD831A28EB2D537754D38EB248911E65E5736FBE0CD1EE`.
The actionable requirements are retained here for cold-agent handoff:

- **A, known historical cause / ROOT-CAUSE-PROVEN:** uncapped food/drop
  distance let native economy assign shoreline fish while the farm controller
  repeatedly retasked the same Villagers, causing command flooding. Recover
  `56959e6c45fd688710abc3f167aade7262dd4d2f`, "Cap food and hunt drop distances
  at town perimeter", in current `rawai-economy.per`: clamp
  `max-food-distance <= 12` and `max-hunt-distance <= 16`. Use rules equivalent
  to `(up-compare-goal NAME c:> CAP)` -> `(up-modify-goal NAME c:= CAP)`.
  First check current equivalent protection; retain it if complete, restore
  missing/partial semantics only. No farming, hunting, fishermen, migration,
  worker-ownership, gather-percentage or farm-staffing redesign.
- **B, known historical cause / ROOT-CAUSE-PROVEN:** explicit fallback
  candidates 1..8 tested only not-allied, which also admits self, allowing
  `sn-target-player-number = self` and native TSA orders to the AI's own TC.
  Recover `8998cdedc1b5942ec6b93b60b1f33a0188238c94`, "Exclude self from
  target-selection fallback", in current `rawai-military.per`. Audit EVERY
  current explicit fallback, not old line numbers: each candidate N = 1..8
  must require `(up-compare-goal gl-self-player-number c:!= N)` before setting
  the target. Preserve normal enemy iteration, attack cadence/strength,
  ownership/grouping, transport and ranking beyond rejecting self.
- These are known recovered fixes, NOT new INVESTIGATING items. Do not
  rediscover causes, add telemetry first, or require another replay before
  implementation/deployment. On implementation mark FIXED-PENDING-RUNTIME;
  do not claim runtime closure from static checks or the pre-fix R2 replay.
- Use two independently revertible causal commits: "Restore bounded food and
  hunt gather distances", then "Exclude self from fallback attack targets".
  Limit each to its PER change, focused tests, appropriate changelog/handoff
  and marker material. Do not blindly import historical marker/changelog
  content or neighboring P3B39/P3B40 changes. Manually reproduce invariants
  if old patches no longer apply. No ownership behavior in either commit.
- A tests: values above 12/16 clamp; values within bounds do not expand;
  unrelated gatherer percentages are unchanged. B tests: for EVERY 1..8
  candidate, in-game + non-allied + buildings still rejects self; a valid
  nonself hostile stays selectable. Add a structural invariant preventing
  any future explicit fallback from omitting self-exclusion.
- Protected diff against the pre-task recovery baseline: A changes no
  transport/migration state machine, attack/defense state, passenger selection
  or farm staffing beyond caps. B changes no dispatch, `attack-now`,
  `up-retreat-now`, `up-reset-attack-now`, military percentages, target ranking,
  transport routes, defense thresholds or task ownership. Preserve T1-T8
  recovery improvements, working attacks/lifts and TASK-OWNERSHIP.md evidence.
- Run the FULL current regression suite, PER structure and operand/domain
  validation, attack/strategy validation, replay benchmarks and
  `git diff --check`. Manually audit all occurrences of `max-food-distance`,
  `max-hunt-distance`, `sn-target-player-number`, `gl-self-player-number`.
- After both commits/static PASS, assign the next unique recovery marker,
  deploy immediately from this checkout, verify EVERY installed file and
  aggregate hash. Do not leave fixes committed but undeployed or wait for
  ownership architecture. Leave a clean tree except documented user-owned
  exceptions, while preserving preexisting work (see qualification below).
- Fresh ordinary replay acceptance is all-player: no sustained historical
  shoreline-fish/farm retask flood, no extreme Villager stream from that
  mechanism, no self target, no self-target military/TSA own-TC flood.
  Inspect repeated TC streams without misclassifying legitimate garrison,
  deposit, defense or production-related orders. R2 predates these fixes.
- Immediately resume common task ownership/preemption afterward. No new
  transport micro-fix, Port placement, boar recovery, Market/Wonder salvage,
  migration drop-site or landing-memory work first unless recovery exposes
  a blocking regression. No additional T9 diagnostic implementation in these
  commits; do not use this release recovery to expand diagnostic scope.
- Required implementation report: starting branch/HEAD/marker/install hash;
  A historical commit/current files/exact invariants/tests; B historical
  commit/all fallback audit/self-exclusion/tests; protected-diff YES/NO for
  attack beyond self-exclusion, transport, ownership, migration (all NO);
  regression count/PER/strategy/benchmarks/diff results; new marker,
  source/install aggregate SHA-256, file count and identity result. End exactly
  `P3B39/P3B40 REGRESSIONS RESTORED — FIXED-PENDING-RUNTIME — OWNERSHIP WORK RESUMES NOW`
  or, for a genuine implementation conflict,
  `REGRESSION RECOVERY BLOCKED — exact conflicting evidence`.

**Current-state qualifications, reported to user:** the attachment assumes
installed T8 and undeployed T9 diagnostics. Actual last verified installation
is T10R3:454 (identity below), compiled from input that already includes T9
diagnostics; T9 was not separately installed. Do not silently roll back the
current diagnostic runtime based on that stale premise. Preserve existing
work and isolate the two recovered behavioral deltas; if literal exclusion
requires removing already installed work, resolve that conflict explicitly.
Current HEAD is `544bd843065245235227018635947e48a077f715`; intentional R1-R3
telemetry/evidence edits remain uncommitted, including `rawai-military.per`.
Before recovery commits, establish their exact pre-task baseline and keep them
separate from the causal fixes; never absorb them silently or discard them to
obtain a clean tree. The prior directive-receipt turn changed HANDOFF ONLY;
implementation is now authorized by R2 arrival. R2's archived writer map remains
`.analysis\p3b44t10r2-writer-trace-sites.json`, outside the repository.

## Workspace and Git identity

The single canonical development workspace remains:

`G:\Projects\Codex\Rome at War AI\.pr-work\Rome-at-War-AI`

- Git root: same path.
- Branch: `codex/replay-economy-build-order`.
- Recorded HEAD: `fbaaae134fb74e46ff0872d4747a3654c7b64d1c`.
- Pull request: <https://github.com/MnHebi/Rome-at-War-AI/pull/4>.
- Working-tree exception on 2026-08-29: `AGENTS.md` is the user's modified
  replacement project-rules file and matches the workspace-root copy. Preserve
  it; do not discard or silently normalize it.
- Current canonical status observed before the P3B44T4 transport session:
  `AGENTS.md` and `HANDOFF.md` are modified and
  `tools/clean_smx_magenta.py` / `tools/test_smx_magenta.py` are untracked.
  Those are concurrent DeepSeek/user changes; do not alter or absorb them from
  this experimental worktree.

This handoff belongs to the dedicated transport-development worktree:

`G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-transport-only`

- Git root: same transport path.
- Branch: `recovery/p3b44-transport-only`.
- Starting/base commit: exact P3B44
  `8ec870075d08fcac98bad55b4ff045bf7abbc42e`.
- Initial departure implementation commit: `94fceb4` (`Clear friendly
  transport departure congestion`).
- Landing-clearance implementation commit: `f6ac4fb` (`Clear friendly Scouts
  from transport landings`).
- Verified exact-blocker implementation commit: `3ee2002` (`Verify transport
  blockers before departure retry`). This is the runtime-validated P3B44T3
  implementation.
- Exact-passenger implementation commit: `19c0beb` (`Verify relic ferry
  passenger before departure`). P3B44T4 runtime-closed that defect in the
  21:43 replay.
- Same-zone migration landing implementation: `2a08a2b` (`Screen migration
  landing candidates by zone`). This is the deployed P3B44T5 behavior commit.
- Safe partial assault / passenger diagnostics implementation: `14fd09c`
  (`Depart with safe partial attack lifts`). This is the deployed P3B44T6
  behavior commit and the recorded experimental HEAD before this handoff-only
  documentation successor.
- P3B44T6 evidence handoff: `f25f5bd` (starting HEAD for the T6 replay audit).
- Migrant reservation implementation: `9d0c87b` (`Preserve migrant reservation
  through villager cleanup`). T7 runtime validates the specific flag exclusion.
- T7 audit starting HEAD: `e17a4edf74919cdf85bab360610612aa216de612`.
- Salvage D/offline analyzer: `9b3dded` (`Backport replay retreat analysis
  tooling`). No runtime changes or marker-specific analyzer dependency.
- Current runtime/diagnostic commit: `d10f33e` (`Trace competing recall callers
  during transport boarding`), P3B44T8. Its evidence/handoff successor is
  `16213f8b06da9d791fca527ec18d6fb6b7fcac86`, the starting HEAD for the
  architectural ownership investigation.
- Architectural audit commit: `e86ab8035a9abacb2ff7b632bebf2afe6802db4e`
  (`Audit task ownership across all T7 players`). Audit tooling, tests and
  evidence only; no runtime changes. Its documentation-only successor records
  this handoff. Resolve exact checkout HEAD with `git rev-parse HEAD`.
- The user explicitly authorized committing the intentional investigation-
  breadth amendment in `AGENTS.md` on 2026-08-30. It is included in this branch
  and PR #5; do not continue treating it as an expected uncommitted exception.
  Its content matches the workspace-root rules. The canonical checkout is
  unchanged by this rules-only publication.
- T8 replay-audit starting/current HEAD: `544bd843065245235227018635947e48a077f715`
  (`Commit intentional investigation-breadth project rules`). Worktree was clean before
  the initial evidence-only audit. The subsequent Blue screenshot investigation
  added uncommitted T9 diagnostics. The user's subsequent priority correction
  produced and installed T10 writer telemetry from this SAME worktree. No new
  development directory, commit or PR update was made; AGENTS.md is unchanged.
- Project-rules synchronization commit: `bcd484f` (`Adopt evidence-first
  project rules`).
- Purpose: P3B44-derived transport-only development. P3B44T1 introduced loaded
  departure congestion handling; P3B44T2 fixed final-landing obstruction by
  route-screen and escort Scouts; P3B44T3 corrected T1's replay-proven
  group-and-assume blocker clearance by moving and verifying one exact safe
  blocker at a time; P3B44T4 directly verifies the reserved relic-ferry
  passenger after P3B44T3 proved two load-recognition failures; P3B44T5
  replaces migration's replay-proven water/wrong-island diagonal candidates
  with close, same-zone, exact-hull-path-screened candidates. The 23:25
  P3B44T5 replay runtime-closed that exact landing-candidate defect.
  P3B44T6 addresses the separately proven exact-full assault abort while
  preserving the unknown upstream passenger failure for discriminating
  telemetry: useful five-to-nine-soldier hulls depart through the unchanged
  screened route, and assault/migration boarding publish bounded exact
  candidate command state before the first retry and at a terminal.
- Status: experimental P3B44-derived development worktree. It does not replace
  the canonical workspace.
- Future ordinary development must use the canonical workspace. Continue this
  exact runtime experiment only in this transport worktree.
- T6 audit scope exception: P3B44T7 touches `rawai-general.per` only to exclude
  transport-reserved passengers from the proven generic-cleanup flag mutation.
  This is a demonstrated dependency of transport ownership, not a general
  economy redesign. No military controller or other behavior was changed.
- T7 audit scope exception: T8 adds event-bound diagnostics to military/taunt
  recall callers only. It does not change their conditions, commands, action
  ordering, searches or ownership. No new worktree was created or canonical
  directory switched in this session.
- Architectural scope exception, 2026-08-30: the user's TASK OWNERSHIP /
  PREEMPTION directive supersedes the earlier prohibition on ownership/recall
  changes in this worktree. It authorizes a shared task contract, explicit
  emergency transfer, bounded routine defense and persistent original-TC
  allied-help anchors, while forbidding concurrent transport micro-fixes.
  See `TASK-OWNERSHIP.md` for the complete requirements and evidence state.
  No runtime changes were made under this new directive yet.

Other controls:

- `G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-attack-baseline`,
  branch `recovery/p3b44-attack-baseline`, exact commit `8ec8700`: immutable
  attack-capable control. Never edit, regenerate, or relabel it.
- `G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-friendly-fire-defense`,
  branch `recovery/p3b44-friendly-fire-defense`, HEAD `92b3cf9`: isolated
  P3B44D1 allied-friendly-fire diagnostic. It is preserved but is no longer the
  installed test runtime.
- `G:\Projects\Codex\Rome at War AI\Rome-at-War-AI-main` is an obsolete
  noncanonical extracted snapshot and must not be used.

## Installed runtime identity

**Current: `RAWAI-P3B44T10R4:455`, 68 files**, deployed and independently rechecked
with `tools/sync_test_ai.py --writer-trace`. Full generated/installed SHA-256:
`C7554880AC95FE2DBB80325ABEA9130CF91C9BE9A845FC5E291A7AEDEBD57B15`.
There are zero missing, different or unexpected runtime files in this mode.
The source-site map fingerprint is
`806FAFCA8EABC51B70FECA1B0F63937806BCA82A4BF1521F00B3538A9242DC90`.
R4 preserves R3 telemetry and restores only hunt 16; food 12 and all eight
self-target fallback guards were already present. Runtime acceptance pending.
T10:451 **FAILED engine compilation** with user-reported ERR6003, String table
full, at rawai-init-goals.per:362. T10R1 reuses string constants; subsequent user
screenshots show RAW44W output in a running match, but also inappropriate idle
logging. R1 replay now confirms quota exhaustion before boarding and missing
startup marker/map messages. T10R2 fixes the idle trace gate; T10R3 delays,
staggers and bounds identity announcements. R3 runtime acceptance is PENDING.
Preserved R1 map for the user's running match/replay:
`G:\Projects\Codex\Rome at War AI\.analysis\p3b44t10r1-writer-trace-sites.json`.
R2 map is likewise preserved as `.analysis\p3b44t10r2-writer-trace-sites.json`.
Use the matching historical map, NOT the current R4 map, for prior recordings.

This is an **in-memory diagnostic compilation of the documented checkout**,
not another editable workspace. Edit the existing PER sources and
`tools/writer_trace.py` here, never the generated installed copy. The checkout's
plain PER input retains the T9 marker but now includes the restored hunt cap.
Reproduce deployment with `--writer-trace`; omitting it removes writer telemetry.
Regenerate `writer-trace-sites.json` after any runtime-source change; deployment
rejects a stale map. T9 was never installed as a separate test.

### Historical T8 identity

- Marker: `RAWAI-P3B44T8:449`.
- Runtime files: 68.
- Installed T8 / pre-T9 source SHA-256:
  `0166808361591E65F29FA4B0770DB90A1C68D1F4A200F220C28C76F13A6D2F92`.
- Historical T8 deployment check: all 68 runtime files were byte-identical, with no missing,
  different, or unexpected runtime files. Relative to T7, exactly
  `rawai-military.per`, `rawai-tauntcommands.per` and `rawai-init-goals.per`
  were copied from this worktree by `tools/sync_test_ai.py --apply`.
- Installed directory:
  `C:\Users\LostSoul\Games\Age of Empires 2 DE\76561198053747760\mods\local\Rome at War AI\resources\_common\ai`.
- Before editing, the full T7 source/deployment hash was verified as
  `69C30C50661D3E1E8A1F8DC081C63E80D0C899D8E695B16D3E02F95B910B7738`.
  T8 is diagnostic only; it has no fresh-match behavioral acceptance yet.

Historical T9 plain input, **not separately deployed**, now preserved in the
R3 checkpoint `ea8a382`: `RAWAI-P3B44T9:450`, 68 files,
SHA-256 `3BB032283550D1C549431E8F3921BCCEA685747F84C8CEF9FB67D678BE4AABE1`.
The T9 preparation check identified three differences from the then-installed
T8: `rawai-customconstants.per`, `rawai-init-goals.per`, `rawai-military.per`;
no missing/unexpected files. T9 only observes terminal transport failures and
publishes previously private assault hold reasons. It is not a congestion or
ownership fix; engine compilation, log delivery and gameplay validation remain
pending. Do not attribute the T8 replay to this untested source.

## Current objective and preserved behavior

P3B44T6 runtime-closes the exact-full assault abort: five useful partial loads
completed enemy-shore landings with exact passenger membership, while below-five
loads retained abort behavior. P3B44T5 landing-candidate screening also remains
CLOSED. The broader queued-passenger defect remains INVESTIGATING, with several
distinct observed failure classes rather than one universal explanation.

P3B44T7 runtime-validates the specific mining-passenger reservation exclusion:
generic villager cleanup was overwriting group 4 with temporary group 0 and
clearing it. All twelve T6 mining-passenger snapshots showed unassigned flag
-2; all 39 identified T7 mining snapshots retain flag 4. This closes only the
specific flag mutation, not exclusive command ownership or successful migration.

The immediate objective is now the user's architectural task ownership /
threat-preemption recovery directive, recorded repository-locally in
`TASK-OWNERSHIP.md`. Completion state is **ROOT CAUSE NOT FULLY PROVEN —
OWNERSHIP TELEMETRY REQUIRED**. The audit covers all 378 recorded loads and
202 retreats, with 132 boarding windows and exact command-stream ordering.
It identifies 83 pre-boarding conflicts with task-owner evidence, including
67 WORK packets, but does not establish every producing script/native writer,
continuous ownership at the instant of overwrite, or a verified per-unit
native economy lock. See the report for successes and unresolved outcomes;
83 is not a count of failed missions.

T8 labels the six existing global-recall callers. It does not trace all worker
writers, acquire/release/preemption boundaries, or native task delegation.
No shared selection contract, emergency-transfer patch, routine-recall
replacement or persistent allied-home anchor has been implemented. The
section-H gameplay contract tests and fresh architectural runtime acceptance
are also pending. Do not mistake the new audit-tool tests for those tests.

**Priority correction:** passenger command ownership is the immediate work,
not further congestion case studies. T10 now traces competing rule calls,
group/reservation operations and native policy/delegation while assault or
migration boarding is active (plus explicit reservation boundaries and
single-use policy setup). Analyze the next T10 replay with its exact writer
map. Do not re-request the already established T8 siege-recall attribution.

T8 replay is now audited: all 100 retreat packets map to 56 tagged invocations.
Red's 54:03 siege-escalation call is established as an actual boarding-order
overwrite, not merely a capable source rule. Worker/native attribution is
still unresolved. Red's newly reported late obstruction is a migration-stage
coverage gap; manual clearance coincides with the loading deadline, so the
unassisted departure outcome is not recorded. See the T8 evidence below.
The user's Blue screenshots at 49:11 and 66:50 exposed missed physical
obstructions: a command-episode census was incorrectly treated as sufficient
obstruction coverage. Blue's first window has no issued departure; its second
contains failed migration route/recovery attempts. Both remain INVESTIGATING.

Purple's proven drop-site race remains open for its own patch. Salvage A-C and
Port placement remain authorized but are held outside this diagnostic runtime
to avoid mixing changes into caller attribution. They are not canceled or
user-deferred. Salvage D was useful to the audit and is already implemented.

P3B44 Gray/Blue combined attacks and the successful T1-T5 transport outcomes
are the known-good behavior at regression risk. Preserve ordinary attack
dispatch and effective genuine defense while replacing only ownership-
violating acquisition/preemption. The new directive explicitly allows changing
routine global recalls; preserving those exact calls is not an acceptance
requirement. Do not backport P3B46-P3B50 attack redesigns into this branch.

## Authorized post-T7 work (2026-08-30)

The user authorized proceeding with SAFE POST-P3B44 SALVAGE INTEGRATION once
the P3B44T7 replay is supplied, and also authorized the previously requested
dock strategic-number work. This expands the permitted work in this recovery
worktree after T7; it does not replace the canonical workspace. The T7 replay
has now been audited across all players. Starting/pre-salvage HEAD is
`e17a4edf74919cdf85bab360610612aa216de612`. D is implemented in `9b3dded`;
A-C and Port behavior are pending, with no claim of runtime validation. The
user was informed that these runtime changes are held outside T8's isolated
caller-attribution experiment, prioritizing the repeated boarding defect.

1. Audit T7 across all reasonably reconstructable transport events and players,
   verify runtime identity, and evaluate reservation survival plus complete
   mission outcomes. If a regression appears, follow the regression-first
   rules before adding features. Record the accepted pre-salvage HEAD.
2. Manually backport the corrected aid tiers from
   `81ce73d22438750adb0ce77f6c13bbec90b7ca63` plus the relevant compiler fix in
   `90287ea6106dace6fe043309ad5b73e3773f3831`. Stockpile below 100 gates requests;
   lifetime collected totals select 100 / 500 / 1000 at bank thresholds 500
   and 1000. Preserve independent 120-second resource deadlines, the ten-second
   global minimum gap, donor reserves, recipient identification, and immediate
   acknowledgment of unaffordable requests. Use `gl-self-player-number`
   comparisons for every donor self-exclusion and port the validator rejecting
   direct `(player-number != N)` predicates.
3. Extract only the six independent Imperial Market purchases and standalone
   Wonder controller from `0e1169f54a3d06fe1cd6c1f76e32714e3e835ec7`, adding the
   two Wonder purchases/sale guards only with that controller. Retain source
   price/resource bounds and one shared 15-second portfolio deadline. Exclude
   the transport-wood rule and any added `gl-land-target-needs-transport`
   dependency. Existing recovery relocation-Market rules remain unchanged.
   Wonder must be late-Imperial/Standard-victory gated, require three five-minute
   no-progress windows accounting for both teams, reset for meaningful losses,
   stagger allied candidates, yield to an allied Wonder, retain the 60-villager
   threshold and resource reserves, and bound retries with cooldown. It may
   read home-defense state but must not write protected controller state.
   Source inspection found a missing Standard-victory gate, negative baseline
   sentinel reuse with one/two enemy buildings, and net-count sampling that can
   mask losses. Resolve these isolated Wonder gaps and strengthen lifecycle
   tests; do not copy the source blindly or import later military dependencies.
4. Port only offline DE_RETREAT retention, `retreat_actions`, generic compact
   chat categories, and independent analyzer tests from
   `91ea476f779f41c2cde858f7cca1cd3c06fbcd59`. No RAW49 runtime instrumentation.
5. Then investigate and implement the Port-placement work in its own causal
   patch, using the three requested controls and acceptance criteria below.
   Do not fold it into the salvage commits or alter protected transport logic.

Never cherry-pick the source commits wholesale. Preserve ordinary attacking,
timers, superiority, target selection, ownership/recall, home defense,
escalation, siege, and every recovery transport selection/loading/routing/
ownership/screening/recovery/readiness/landing/clearance rule, including T7's
general-cleanup exclusion. Stop a conflicting backport rather than importing
P3B46-P3B50 military/transport behavior. Keep the baseline immutable.

Historical salvage goal IDs collide with current transport goals. The original
selected features need 27 new goals; 1163 onward was free at scoping HEAD
`e17a4edf74919cdf85bab360610612aa216de612`. Recheck and allocate fresh IDs;
Wonder corrections may need additional state. Prefer three separable salvage
commits: corrected aid; independent Market/Wonder; offline analyzer. Port work
is separate. Expected salvage runtime files are customconstants, init-goals,
trade, and homebase only. Run focused tests, structural/domain validators,
relevant synchronization checks, the full recovery regression suite, adversarial
review and a complete protected-symbol/semantic diff audit against the recorded
pre-salvage HEAD. Use a unique recovery marker and verified runtime hash, update
this handoff, and require fresh replay acceptance; static success is not runtime
closure. Do not import historical markers or later handoffs wholesale.

## Defect ledger

### Friendly Transport departure congestion

- **Status:** CLOSED.
- **User-visible symptom:** Purple had a loaded mission Transport that could not
  get underway because Purple's own idle Transports physically blocked it. The
  loaded hull remained stuck.
- **Direct evidence:** user visual observation in the 11:01 P3B44 replay, plus
  two systematic Green failures in the 13:10 P3B44T2 replay.
- **Initial proven failure mechanism:** P3B44's
  `TRANSPORT-ROUTE-WAYPOINT-WAIT/CHECK` treated `distance > 8` as sufficient to
  reissue the identical waypoint every eight seconds. It had no previous/best
  distance, progress threshold, stall count, clearance attempts, or terminal
  bound. Both independent transport-clear entry rules require
  `TRANSPORT-ROUTE-IDLE`; they cannot run during an active route and are
  designed for stale partial loads or empty idle Port/Shipyard obstruction.
- **P3B44T2 runtime result:** Green hulls 58807 and 30210 each stalled 49/52
  tiles from their waypoint with garrisoned passengers and three blockers. At
  94:39, 100:14, and 100:49 the runtime selected the same blocker IDs 30476,
  53715, and 57617 and moved all three as one group to one staging point. Both
  loaded hulls made no progress and emitted `departure congestion unresolved`.
  The identical blocker set surviving into the later mission proves command
  issuance was incorrectly treated as clearance.
- **P3B44T1 implementation:** initializes best/current waypoint distance from
  the exact reserved hull, requires two tiles of improvement, resets the stall
  count on progress, and checks the saved embarkation point after three
  non-progress samples. Only a loaded hull still within twenty tiles of origin
  can enter congestion handling.
- **P3B44T3 implementation:** select only the nearest exact eligible blocker,
  save its object ID, move it, reconstruct that same ID after eight seconds,
  and require its distance from the saved mission-hull point to exceed twelve
  tiles before logging `blocker cleared`. One retry is allowed only while the
  hull remains empty, unattacked, ungrouped, and unquarantined. A hull that
  remains blocked or becomes unsafe is excluded while another exact blocker is
  tried. Three selections are the hard bound before the existing terminal
  recovery path.
- **Safety:** initial scans continue to exclude the mission hull, quarantine,
  loaded, attacked, non-idle, grouped, and different-water-zone ships. The
  adversarial review added the same mutable safety protection to the delayed
  exact-ID retry so a newly claimed hull cannot be retasked.
- **Acceptance criterion:** a loaded hull obstructed by friendly idle
  Transports logs an exact blocker order followed by `blocker cleared` only
  after measured separation; the loaded hull then logs `departure resumed`,
  leaves origin, and continues the existing mission. Unsafe hulls are skipped,
  failures remain bounded, and ordinary P3B44 attacks remain effective.
- **Latest runtime result:** in the 15:12 P3B44T3 replay, Blue loaded hull
  31205 reported departure congestion at 44:26. Exact blocker 37204 received
  one move and one bounded retry, then emitted `blocker cleared` at 44:42; the
  source can emit that event only after the exact blocker exceeds twelve tiles
  from the mission hull. Hull 31205 resumed at 44:51, issued its remote unload
  at 45:08, completed the landing at 45:47, and withdrew home. This directly
  satisfies the scoped runtime criterion.
- **Non-regression result:** the same mission's route-screen Scout moved aside,
  no guard targeted the hull during its 45:08-45:47 unload window, and the
  landing completed. P3B44T2 remained intact.
- **Closure basis:** exact runtime blocker separation, loaded-hull resumption,
  and completed landing are all replay-visible. P3B44T4 does not alter any T3
  departure rule.

### Red and Blue Port crowding outside assault-clearance coverage

- **Status:** INVESTIGATING. The physical symptom is accepted; missing migration
  coverage is source-established, but the unassisted departure outcome is absent.
- **User-visible symptom:** near the end of T8, Red's loaded Transport was blocked
  by other friendly Transports; the user manually moved the blockers away.
  Blue also has user-observed blockages at 49:11 and 66:50, preserved with the
  two screenshots and exact command windows in the T8 evidence below.
- **Direct evidence:** at 66:24 replay playback shows four villagers aboard the
  migration hull and two adjacent empty Transports at Red's Port. Recorded moves
  of 48064/31880 occur at 66:30-32. Hull 31691 starts its route at 66:31.236 and
  reports distance 52 at 66:46, 30 at 67:01, 15 at 67:17, and zero at 67:32.
- **Cause/limit:** T3's exact-blocker clearance belongs to assault departure,
  not migration loading/departure. However, the first migration departure order
  coincides with its normal 30-second partial-load deadline and manual clearance.
  This does not prove an issued departure remained stuck before intervention.
  Do not dismiss the visible obstruction or silently label normal boarding wait
  as a measured departure-path stall. Keep both accounts together.
- **Instrumentation/tests:** existing RAW44B snapshots record 18 remaining at
  66:04 and 16 at 66:31; sampled passengers retain group 4 and enter orders.
  Exact hull positions/progress and eligible blocker states during this loading
  phase are not logged. The subsequent migration reaches a landing candidate
  just before the 67:33 replay cutoff, not a proven economic settlement.
- **Implementation:** prepared T9 terminal-only diagnostics, not deployed.
  No navigation, blocker selection, ownership or recovery behavior changed.
- **Acceptance criterion:** an unassisted obstructed migration records phase,
  actual no-progress condition, safe exact blocker clearance and restored
  boarding/departure; occupied, task-owned, threatened and wrong-water blockers
  remain protected, and ordinary loading deadlines/successes are preserved.
- **Latest result:** crowding/coverage-gap evidence PASS; autonomous recovery
  FAIL in the user-observed Blue cases, causal gate/blocker eligibility still
  unresolved. Orange's independent assault clearance succeeds in T8.
- **Next action:** keep separate from the architectural ownership patch. Use a
  bounded phase-aware migration observation or controlled unassisted reproduction
  to distinguish blocked passenger access, blocked departure and normal loading
  wait before extending clearance. Do not ask the user again for blocker type/time.
  The generic idle-berth utility requires all transport controllers idle; simply
  removing that gate risks retasking active owners and is not an accepted fix.

### Relic-ferry passenger load recognition

- **Status:** CLOSED.
- **User-visible symptom:** Red loaded a Priest into a Transport, the hull did
  nothing, the controller later unloaded the Priest at home, and the Priest
  retrieved a relic from Red's own island instead of completing the intended
  ferry mission.
- **Direct evidence:** exact Priest 31572 was ordered aboard hull 31206 at
  19:23 in the P3B44T3 replay. No outbound hull order followed; exactly 180
  seconds later the relic watchdog issued a home unload at 22:23. After another
  home unload at 24:25, the same Priest received an ordinary order to own-island
  relic 31456 at 25:11. The defect repeated with hull 33537: boarding at 31:11,
  no outbound order, and exact watchdog home unload at 34:11.
- **Root cause boundary:** the earliest repeated divergence is the load check,
  before sailing, pathing, landing, or relic tasking. P3B44T3 checked readiness
  indirectly through the reserved hull's `object-data-garrison-count` and had
  no CHECK-LOAD branch when the exact hull search target was absent. The replay
  proves that this recognition path failed twice; it cannot distinguish an
  absent hull result from an unobserved/stale count.
- **Engine constraint:** DE direct-unit searches exclude garrisoned units by
  default. P3B44T4 uses `fe-filter-garrisoned c: 1` before rebuilding the exact
  stored passenger ID so the lookup remains valid across boarding. Provenance:
  official AoE II DE Update 111772 scripting notes,
  <https://www.ageofempires.com/news/age-of-empires-ii-definitive-edition-update-111772/>.
- **Implementation:** commit `19c0beb` changes only the relic-ferry LOADING and
  CHECK-LOAD transition. It verifies the exact reserved Priest/Brahmin's
  `object-data-garrisoned == 1`, then rebuilds the unchanged reserved hull and
  issues the existing target/home unload. The existing 180-second watchdog and
  hull group reservation remain. One pending-or-missing event per boarding
  attempt and exact outbound/return unit/hull records provide bounded evidence.
- **Regression risk:** T3 attack-Transport departure and T2 landing-screen /
  escort behavior. No corresponding rules were changed; the existing focused
  tests remain and must be reconfirmed in the fresh replay.
- **Acceptance criterion:** exact boarding is followed by `RAW44R relic ferry
  outbound unit/hull/target` and the same hull's remote unload before the
  180-second watchdog. The carrier acquires the off-home relic, emits exact
  return unit/hull records, unloads at home, and receives the unchanged home
  Monastery task. Pending/missing logging remains one-shot.
- **Latest runtime result:** the 21:43 P3B44T4 replay contains two independent
  complete round trips. Orange carrier 33139 used exact hull 31942 to visit
  relic 4656 and returned to Monastery 33023; Cyan carrier 34011 used exact
  hull 33693 to visit relic 4662 and returned to Monastery 33653. Red carrier
  33314 and Green carrier 33487 independently advanced from boarding to exact
  outbound hull/target commands before the watchdog, although neither return
  completed before later mission outcomes.
- **Non-regression result:** five assault unload windows in the same replay had
  zero GUARD commands on the active landing hull. Two completed and three reached
  the unchanged bounded timeout.
- **Closure basis:** exact garrison recognition, outbound identity, remote
  unload, relic acquisition, same-hull return, home unload, and exact Monastery
  task are replay-visible for two independent players.

### Friendly Scout obstruction at attack-Transport landing

- **Status:** CLOSED.
- **User-visible symptom:** near the end of the P3B44T1 replay, Purple's loaded
  Transport aborted instead of having a friendly Scout Ship move out of the
  way.
- **Direct evidence:** user visual observation plus decoded actions from
  `SP Replay v101.103.48987.0 @2026.08.29 122745.aoe2record`.
- **Root cause:** Purple Scout 32389 guarded the future route hull, then the
  route-screen owner ordered it to waypoint 28,182 at 49:24/49:54 and landing
  72,185 at 50:10. The success branch released its group and erased its exact
  ID without issuing another order, leaving it stationary on the landing.
  Purple Transport 32174 reached waypoint 28,182, issued its unload at that
  exact landing at 51:29, remained loaded, and was recalled home at 52:15 by
  the fixed forty-five-second landing timeout. A second Scout, 32970, also
  received guard orders on Transport 32174 every twenty seconds during the
  approach/window. No P3B44T1 departure-stall event fired because departure
  progress was normal.
- **Implementation:** P3B44T2 moves the exact route-screen Scout eighteen tiles
  to one side of the screened approach before releasing `transport-screen-group`.
  Immediately before unload, it moves the already-owned transport escort group
  eighteen tiles to the opposite side while retaining that ownership. The
  periodic escort selector cannot reissue guard during
  `TRANSPORT-ROUTE-RETURN-WAIT` and resumes immediately after the landing owner
  exits that state.
- **Instrumentation:** public bounded events identify the exact cleared screen
  Scout, staged landing route, completed landing, or terminal timeout.
- **Acceptance criterion:** `RAW44T2 route-screen landing cleared` is followed
  by visible screen-Scout clearance; `RAW44T2 transport landing escort staged`
  occurs once; no guard is reissued to that loaded hull during the unload
  window; passengers disembark; `RAW44T2 transport landing completed` occurs
  before forty-five seconds; and no timeout occurs for that mission. Ordinary
  P3B44 attack behavior remains unchanged.
- **Latest runtime result:** the systematic P3B44T2 audit found eighteen
  landing-screen events across all players and an exact same-timestamp Scout
  move for every event. Fifteen missions reached unload windows and none had a
  guard action targeting the active hull during that window. Both Purple
  missions completed at 62:59 and 88:41. This directly satisfies the scoped
  screen/escort acceptance criterion.
- **Closure basis:** runtime replay evidence demonstrates exact screen-Scout
  clearance, guard suppression, and completed landings. The nine other
  timeouts are a distinct repeated-landing-selection defect with zero
  unload-window guard actions.

### Queued passenger blocks Transport route start

- **Status:** CLOSED for the exact-full assault route gate (T6 runtime PASS);
  INVESTIGATING for the upstream reason an individual queued passenger does
  not board.
- **User-visible symptom:** several queued units remained outside their
  Transport. Manually loading the assumed passengers caused the hull to enter
  its route.
- **Direct replay evidence:** the systematic P3B44T5 boarding audit found 48
  detailed Red scripted episodes: 31 full/ready, 13 aborts, 3 partial, and 1
  unresolved. At 51:14, 55:04, 57:38, and 59:46 ten-passenger assault
  manifests shrank to a one-passenger retry list and still reached the
  exact-full abort. Passenger 39672 was the sole serialized retry candidate in
  the latter three episodes. At 281:51, a separate migration load record
  uniquely included exact hull 31558 in its selected objects, identifying a
  human load action; `migration depart full: 11` followed at 282:05 and the
  hull immediately received route movement. This independently corroborates
  the user's direct observation.
- **Proven downstream root cause:** the assault loader required the exact
  selected count at the thirty-second terminal. Any one nonboarding passenger
  therefore discarded the useful loaded remainder. Simply lowering the count
  was unsafe because the original `attack-boarding-group` still contained
  shore stragglers that would later receive the remote landing order.
- **Unknown upstream cause:** passenger 39672 has repeated replay-visible
  SPECIAL garrison commands to hull 31558 and no serialized ORDER, AI_ORDER,
  WORK, GUARD, or PATROL command that visibly transferred it to another owner
  in the bounded 55-to-60-minute audit. The replay does not expose whether
  shoreline geometry, internal/unserialized command replacement, object state,
  or an engine loading failure stopped it. Preserve this uncertainty.
- **Instrumentation:** P3B44T6 publishes one bounded candidate before the first
  assault or migration retry and another at a partial/abort terminal. Each
  sample includes exact object ID, action, target ID, order, command ID,
  distance from the stored embarkation origin (not a moving hull's current
  position), land zone, controller group flag,
  move coordinates, and idling state. A land-to-water path query was
  deliberately rejected because it cannot distinguish shoreline boarding
  reachability.
- **Implementation:** commit `14fd09c` retains the ten-passenger maximum and
  thirty-second assault window. With five through nine exact garrisoned
  soldiers, it stops every shore straggler, reconstructs
  `attack-boarding-group` from garrisoned members only, updates the target to
  actual occupancy, and continues through unchanged target revalidation,
  route screening, and landing. Fewer than five retains the existing bounded
  unload/recovery abort. Migration receives diagnostics only; its full,
  partial, and abort thresholds are unchanged.
- **Regression risk / control:** full assault lifts, low-strength abort,
  home-defense interrupt, target invalidation, P3B44T2 final-landing Scout
  clearance, P3B44T3 exact departure-blocker verification, P3B44T4 relic
  ferries, P3B44T5 same-zone migration landings, and Gray/Blue ordinary attack
  behavior.
- **Acceptance criterion:** the fresh replay contains marker
  `RAWAI-P3B44T6:447` and exact installed hash. Every still-underfilled first
  retry emits a candidate snapshot. A hull with five through nine actual
  garrisoned soldiers emits `RAW44B attack partial departure`, enters the
  existing screened route, and gives the remote order only to passengers that
  were aboard; a hull below five retains bounded recovery. Candidate action
  and target evidence establishes the first upstream divergence before any
  further passenger-behavior fix.
- **Latest result:** T6 runtime PASS for safe partial assault. Orange's six
  partial terminals at 43:11, 51:37, 56:44, 59:48, 63:22, and 67:12 retained
  9/8/8/8/8/6 soldiers. The first five completed landings at 46:40, 54:15,
  58:42, 61:41, and 65:26. Each completed remote-order set exactly equals the
  original manifest minus the stopped shore stragglers. The sixth received a
  home-recovery unload at 68:50; its later route rejection is not publicly
  diagnosed. Four below-five terminals aborted with 0/4/0/0 passengers.
- **New upstream evidence / next action:** 56 snapshots show distinct cases:
  all twelve mining samples lost group ownership (causal fix below); three
  scout samples resumed exploration; most other samples retained enter orders
  toward the correct hull, sometimes still approaching from far away. Orange
  soldier 40673 was idle with no target at 51:22 and 51:37, but later belonged
  to the successful 58:42 landing, so it is not inherently untransportable.
  Exact geometry/internal command causes for the close military stalls remain
  unknown. The nominal four-second assault retry and thirty-second terminal
  use `gl-game-time`, refreshed only every fifteen seconds; observed early
  snapshots can occur up to fifteen seconds after loading. Keep that timing
  defect separate from the T7 reservation patch.

### Generic cleanup strips mining-passenger reservation

- **Status:** CLOSED for the specific cleanup flag mutation, T7 runtime PASS.
- **User-visible symptom:** queued migrant villagers lose their transport
  reservation flag while boarding; this is one established sub-defect of the wider
  passenger failure report, not a universal explanation for military stalls.
- **Direct evidence:** twelve RAW44B mining snapshots across Purple, Cyan and
  Gray show flag -2, including Purple 31871 at 66:38 and 31787 at 67:05. All
  27 military and 17 scout snapshots retain flag 4.
- **Root cause:** `rawai-general.per` selects non-exploring villagers with a
  non-tree target, puts them into group 0, sets their flag to 0, then clears
  it. Migrants targeting their hull match that selector. The original group-4
  search membership can still retrieve them, but their ownership flag is gone.
  AIRef documents that the flag is per-object and -2 means unassigned:
  <https://airef.github.io/commands/commands-details.html#up-modify-group-flag>.
- **Contradictory/limiting evidence:** retaining enter orders in these samples
  does not prove every worker was stopped or that flag loss explains every
  loading failure. Soldiers are not selected by this villager cleanup.
- **Implementation:** `9d0c87b` excludes `migration-boarding-group` before
  temporary group creation. Existing unreserved-villager cleanup remains.
  `rawai-military.per` is byte-identical to T6; no thresholds, routes, attack
  owners, hunt rules, or Port settings changed.
- **Instrumentation/tests:** existing transition-bounded RAW44B group/command
  snapshots are retained. A focused selector/flag model reproduces old flag
  4 -> 0 -> -2 behavior and proves reserved exclusion under the patched
  selector; a mutation removing the filter reproduces the failure.
- **Acceptance criterion:** early and terminal mining samples retain flag 4
  while reserved, with the general-cleanup exclusion retained. Broader command
  exclusivity, boarding/landing/work progress and other STOP writers are
  separate acceptance criteria, not consequences of preserving a flag.
- **Latest result:** T7 all-player audit finds 39/39 identified mining-worker
  snapshots retaining flag 4, versus 12/12 flag -2 in T6. Deterministic selector
  and non-regression tests PASS. T7 military and identified migration samples
  also retain flag 4. Command interference nevertheless occurs: see next entry.
- **Next action:** preserve this exclusion and its test; do not reapply it as
  the fix for subsequent STOP/recall events or close overall transportation.

### Reserved passengers receive competing recall, STOP and work orders

- **Status:** INVESTIGATING overall. T8 proves the siege-escalation boarding
  overwrite and identifies every recorded global-recall caller; worker/native
  producing paths and the complete safe ownership mechanism remain unresolved.
  Directive completion state: ROOT CAUSE NOT FULLY PROVEN — OWNERSHIP
  TELEMETRY REQUIRED. The shared architectural requirement is in
  `TASK-OWNERSHIP.md`; this is not a collection of isolated micro-fix tickets.
- **User-visible symptom:** queued soldiers are pulled away from Transports;
  armies accumulate at Town Centers. Manual loading can release pending routes.
- **Direct evidence:** T7 all-player audit, 103 boarding snapshots and 202 raw
  DE_RETREAT packets. Red reserved scout 44331 has a flag-4 enter-order snapshot
  at 54:57, then appears in recalls to TC 4538 at (82,35) at 55:02.350 and
  55:08.354, before any unload. Gray at 61:08.762, Blue at 68:42.820 and Purple
  at 80:42.502 also have selected passengers recalled before recorded unload.
  Nineteen load-record/retreat overlaps include repeated loads and some later
  post-unload recalls; do not present all nineteen as stolen boarding groups.
- **Distinct STOP evidence:** Orange's 61:36-62:06 boarding window contains
  749 identical AI_ORDER packets selecting scout 4638 and soldier 30434 with
  order 706 (STOP). Both are selected passengers with flag-4/no-active-target
  snapshots. Nine passengers depart; the scout stays ashore. Orange's only
  DE_RETREAT is 67:46.218, so this is not an overlapping recorded retreat.
  Cyan scout 4639 receives explore order 705 between boarding retries, and
  Green worker 47605 receives repeated TC-target orders starting at 83:01.
- **Architectural replay-wide evidence:** 132 windows / 1,053 passenger-window
  instances: 65 corroborated successful without observed conflict (56 full,
  nine exact partial landing), 83 pre-boarding conflicts with owner evidence,
  905 unresolved. Per-color conflict counts: Red 9, Green 9, Yellow 0,
  Purple 4, Orange 3, Cyan 2, Blue 12, Gray 44. Among the 83 first conflicts,
  67 are WORK; therefore recall-only changes cannot cover the demonstrated
  failure surface. Continuous ownership and exact native/script attribution
  remain open rather than inferred from sparse flags. All 202 retreats retain
  exact members, previous commands and applicable boarding-window links.
- **Current causal hypotheses:** scripted global recall/all-unit reset,
  native attack/scout ownership, or another local command writer can overwrite
  boarding without changing the reservation flag. Five military rules and
  taunt 45 call global recall; two also reset all units. Local defense/leash
  selection does not exclude every reservation. Source existence alone does
  not identify which path produced the replay commands.
- **Contradictory/limiting evidence:** group 4 persists in all 101 identified
  snapshots, so flag loss is not the general cause. Some stalled units retain
  correct enter orders. Red eventually boards despite the two recalls. Orange
  has a separate STOP mechanism. Snapshot timing can miss between-retry orders;
  the new full-stream audit corrects packed-ID/second-resolution limitations,
  but cannot supply missing simulation acknowledgments or owner-change logs.
- **Instrumentation/tests:** T8 `RAW44O` logs immediately before each scripted
  global recall: source, assault state/hull, migration state/hull. Sources:
  1 land defense; 2 naval defense; 3 siege escalation; 4 loss regroup;
  5 periodic losses/all-unit reset; 6 allied taunt 45/all-unit reset. Five logs
  per invocation; no new sampling loop, search mutation or goal allocation.
  Tests verify all six callers and hash the entire military/taunt executable
  program back to T7 after removing only the added logs.
  T10 additionally traces 351 command/group/native-policy sites, selected-object
  identity/flag and pre/post boarding state/hulls, bound to a replay-visible
  exact source map. See the T10 section for limits and queued-packet handling.
- **Implementation:** diagnostic commit `d10f33e`, deployed T8. No behavioral
  ownership fix implemented. Salvage D retains offline retreat events and
  generic compact chat categories. New `tools/audit_task_ownership.py` and its
  packet/lifecycle tests retain replay-wide command evidence; raw artifacts
  remain external. T10R3:454 writer diagnostics are now installed; gameplay
  ownership decisions remain unchanged and the new tooling is uncommitted.
- **Acceptance criterion:** shared ownership lasts until explicit complete,
  abort, loss, release or verified emergency preemption; ordinary military and
  economic selectors respect it; routine defense acquires bounded free units;
  severe hostile defense cancels old owners cleanly; allied relief uses live
  hostile presence near persistent first-TC coordinates, even after TC loss.
  Pass the nine section-H contracts plus all-player fresh runtime validation,
  preserving ordinary attacks, partial/full lifts, relics and screened landings.
- **Latest result:** T8 caller attribution PASS: 100 packets / 56 tagged calls.
  Red's 54:03.506 source-3 recall interrupts passengers 40149, 43815 and 47309
  during boarding; later retries corroborate that they remain ashore. All 56
  candidate snapshots retain group 4. Broad ownership acceptance remains FAIL /
  unresolved, not fixed by the diagnostics. See TASK-OWNERSHIP.md for exact
  sequences and qualifications. Worker/native attribution is still pending.
  R1 adds scout-specific evidence: source-1 land defense recalls Green/Orange
  reserved scouts; exploration order 705 overwrites Purple/Orange boarding
  while reservation flag 4 remains visible. Do not relabel these as workers.
- **Next action:** check R3's corrected off-mission gate and delayed identity, then analyze
  writer traces using the map for that replay's actual build. R1's map is
  preserved externally; its early idle logging may exhaust coverage before
  useful boarding. Distinguish
  script-selected, script-delegated and autonomous native orders in a controlled
  engine test. Use T8 for the six recall writers but do not claim it alone can
  settle worker attribution. Use the source-map-verified T10 events and retain
  ambiguous queued issuers instead of choosing the closest log. Establish the minimum protection mechanism, then
  implement the shared contract, threat preemption and allied-anchor requirements.
  Do not reapply the closed generic flag fix or guess that flags lock native work.

### Repeated attack-Transport landing timeouts

- **Status:** INVESTIGATING.
- **User-visible symptom:** assault Transports often load, fail to land, and
  later unload at home or remain loaded.
- **Direct evidence:** of seventeen P3B44T2 semantic assault missions, fifteen
  reached unload windows; six completed and nine timed out. Orange timed out
  six and Cyan three. Orange repeatedly reused candidates near 182,119 and Cyan
  near 116,1. No window contained a guard action targeting its hull.
- **Current hypothesis:** failed or inaccessible candidate coordinates are not
  remembered/rejected, allowing later missions to repeat the same terminal
  landing choice.
- **Contradictory/unknown evidence:** command records prove unload issuance and
  terminal outcome but not terrain collision, passability, hostile obstruction,
  or actual passenger state. A coordinate timeout is not by itself proof that
  the tile is permanently invalid.
- **Instrumentation/tests:** existing public screen, landing-staged, completed,
  and timed-out events reconstruct mission lifecycles but do not publish the
  selected/rejected coordinates or exact remaining garrison at terminal.
- **Implementation:** none in P3B44T3 or P3B44T4; deliberately excluded from
  both narrow causal patches.
- **Acceptance criterion:** after a terminal unload failure, the exact failed
  landing and local offsets are rejected for a bounded period; a later mission
  selects a distinct viable candidate and passengers disembark.
- **Latest result / next action:** add bounded public landing-coordinate,
  remaining-garrison, and rejection telemetry before selecting a behavioral
  fix.

### Migration blind landing offsets

- **Status:** CLOSED.
- **User-visible symptom:** Purple performed odd scout-Transport actions around
  14 and 24 minutes in P3B44T2. Green later performed the same conspicuous
  twenty-passenger migration around 1:22 in P3B44T4 and returned home without
  landing anyone.
- **Direct replay evidence:** Green hull 32009 tried resource anchor 134,196 at
  80:42, followed by the exact source-generated eight-tile diagonals 142,204,
  126,204, 142,188, and 126,188 at twenty-second intervals. No passenger
  landed; five home unloads followed from 82:23 through 83:24. Purple T2 had
  already reproduced the same five-point sequence twice.
- **Authoritative terrain evidence:** the P3B44T4 replay header identifies
  134,196 as terrain 0, the first two diagonals as terrain 1, and the southern
  diagonals as terrain 0 on landmasses separated from the target island by
  continuous water. The Rome at War DAT names terrain 0 `Grass` and terrain 1
  `Water, Shallow`. Thus two retries were water and two were different islands.
- **Root cause:** `up-bound-point` only shifts coordinates into map bounds. The
  migration state treated that as sufficient validation, issued unloads to
  four fixed eight-tile diagonals without reading their zone or testing the
  exact hull's path, and exhausted the sequence into home recall.
- **Implementation:** P3B44T5 replaces the diagonals with four close two-tile
  cardinal candidates around the exact resource anchor. Before the initial or
  any alternate unload, it reads the candidate point zone, requires equality
  with the stored resource-anchor zone, rebuilds the exact reserved hull, and
  requires `up-path-distance ... 0 != 65535`. Wrong-zone and unreachable
  candidates emit bounded public reason/identity telemetry and advance after
  one second without an unload command.
- **Non-regression risk:** previously successful migration landings, the
  P3B44T4 relic ferry, T3 departure clearance, and T2 assault landing screen.
  The patch changes only the shared migration landing-candidate transition.
- **Acceptance criterion:** each migration unload is preceded by a same-zone
  exact-hull path-clear event; no unload follows a wrong-zone or path-rejected
  candidate; a small-island mission either lands in its selected resource zone
  or terminates with bounded explicit reasons without targeting water/another
  island. At least one previously successful migration remains successful.
- **Latest runtime result:** P3B44T5 supplied 48 public migration candidate
  missions across seven players. All 95 `landing path clear` events had an
  exact same-second unload by the reported hull; all 4 wrong-zone and 36
  path-rejected events had no same-second unload. Four all-invalid missions
  skipped all five invalid candidates and recalled home. Red independently
  landed ten settlers in zone 3, completed a Mining Camp, and retasked them.
  Previously working assault and relic transport behavior remained present.
- **Closure basis:** every behavioral acceptance criterion was demonstrated by
  the byte-identified runtime replay. No further landing-candidate patch is
  authorized without new contrary runtime evidence.

### Migration escort ownership overlap

- **Status:** INVESTIGATING.
- **User-visible symptom:** a loaded migration hull can have friendly warships
  crowding it during approach, landing retries, or recall.
- **Direct evidence:** Green warships repeatedly received GUARD orders on exact
  migration hull 32009 throughout both 77:58-83:24 and 84:40-88:00 episodes,
  including every refresh across the first remote unload/retry window.
- **Current causal boundary:** the generic escort selector excludes only the
  assault controller's `TRANSPORT-ROUTE-RETURN-WAIT`; it does not exclude a
  Transport reserved by `migration-transport-group` or any migration landing
  state. This proves overlapping ownership policy. Replay commands do not
  serialize collision polygons, so they do not prove which unload physically
  failed because of an escort.
- **Implementation:** none in P3B44T5. Removing protection for the whole
  civilian voyage would risk a transport-survival regression without proving
  the necessary clearance window.
- **Acceptance criterion:** targeted telemetry or direct visual evidence ties
  a specific guard/ship position to a stalled migration approach; the eventual
  patch stages owned escorts clear only for the proven window and preserves
  voyage protection.
- **Latest result / next action:** 30 of 48 P3B44T5 public migration candidate
  windows contained guard commands on the exact hull, totaling 62 guard
  events. Guards also overlapped successful or partial Red landings, so they
  are not universally fatal. Preserve INVESTIGATING status until position or
  targeted clearance evidence ties a specific guard to a specific stall.

### Migration drop-off establishment and premature recall

- **Status:** ROOT-CAUSE-PROVEN for Purple; INVESTIGATING for Orange.
- **User-visible symptom:** Purple and Orange delivered villagers to an island
  but established no resource drop-off.
- **Purple direct evidence:** hull 30184 landed twenty builder-capable
  passengers at 82:57/83:17. Passenger 30667 issued Mining Camp build 584 at
  94,161 at 83:36. At 83:37 nineteen passengers were ordered to reboard and at
  83:39 the hull began home unloads.
- **Purple root cause:** `MIGRATION-WAIT-DROPSITE` advances on the global
  `up-pending-objects mining-camp >= 1` condition. Assignment then searches for
  a concrete pending foundation within eight tiles and the target zone. A
  queued build command can satisfy the global count before such a foundation
  is searchable; the no-target assignment branch immediately sets
  `MIGRATION-DROPSITE-FAILED`, bypassing the intended twenty-second/four-offset
  placement retries. The one-second build-to-reboard cadence follows only that
  source path.
- **Orange direct evidence:** hull 34221 landed twenty builders at
  83:36-84:16. No passenger issued a Mill/Lumber/Mining Camp build within
  twenty-four tiles during the rest of the replay. Fifteen were told to
  reboard at 86:02 and never unloaded again before the replay ended.
- **P3B44T5 evidence:** Red completed one full landing/drop-off lifecycle at
  52:33-54:28: ten settlers landed, exact builders were assigned, the Mining
  Camp completed, and the settlers were retasked. Three later Red zone-14
  landings delivered 2, 6, and 11 settlers but each then emitted an explicit
  `migration mining camp resource wait:14` for 60 seconds before drop-site
  failure and home recall. Those are resource-starvation terminals, not the
  earlier Purple one-second global-pending race.
- **Contradictory/unknown evidence:** only each local AI's self chat is private;
  Orange's exact anchor, affordability, placement-owner, and watchdog state is
  not serialized. Purple has a build command but the replay does not prove a
  placed foundation or engine rejection reason.
- **Instrumentation/tests:** action cadence plus source-state comparison proves
  Purple's transition; Orange needs public first-blocker/terminal telemetry.
- **Implementation:** none in P3B44T3 or P3B44T4.
- **Acceptance criterion:** a landed migration waits for and assigns a concrete
  same-zone drop-site foundation, completes it, and uses it before passengers
  can be recalled; unavailable placement reaches bounded retries and a precise
  terminal reason.
- **Latest result / next action:** fix Purple's premature global-pending
  transition as a separate causal patch. Preserve the successful Red lifecycle
  as the non-regression control. Add or retain bounded public affordability and
  first-blocker evidence for Orange and the late Red resource-wait cases before
  changing their distinct pre-drop-site paths.

### Orange delayed assault activation

- **Status:** INVESTIGATING.
- **User-visible symptom:** Orange performed no observed assault transportation
  until Blue and Gray were effectively defeated.
- **Direct evidence:** Orange's first public assault-screen event was at 42:26
  and first completed assault landing at 53:41. The user's visual timing is
  preserved as authoritative observation.
- **Contradictory/unknown evidence:** the replay contains no serialized
  defeat/resignation notice for Blue or Gray and does not publish Orange's
  private attack-ready, army ownership, passenger, or target gate before 42:26.
- **Instrumentation/tests:** current public telemetry begins only after a route
  screen exists, too late to identify the first blocked activation condition.
- **Implementation:** none.
- **Acceptance criterion:** Orange activates an eligible cross-water assault
  based on its own readiness/target state rather than allied collapse, or
  bounded telemetry proves which legitimate prerequisite is absent.
- **Latest result / next action:** add public transition-only telemetry for the
  first blocked assault-activation gate; do not guess a gate from timing alone.

### Command-volume anomaly and deferred crash

- **Status:** DEFERRED by the user until transport defects are handled.
- **User-visible symptom:** the 15:12 P3B44T3 match crashed before its natural
  end. The user believes this is the already known crash class.
- **Direct evidence:** the decoded replay ends at 59:33 without a resignation
  action and has zero parser errors. Cyan serialized about 586,260 AI_ORDER
  records; Green, Yellow, and Blue also produced unusually high WORK volumes.
  The non-crash 21:43 P3B44T4 replay independently contains 1,256,052 ACTION
  operations: 580,574 ORDER, 372,491 AI_ORDER, and 194,037 WORK. Several
  garrisoned Green migration passengers each received roughly 5,400-10,100
  repeated ORDERs toward object 4561 at the exact home point; large repeated
  streams also occur for other players and objects.
- **P3B44T5 evidence:** the 5:11:04 replay contains 3,260,167 ACTION
  operations: 1,830,452 AI_ORDER, 916,162 ORDER, and 235,131 WORK. The largest
  repeated ORDER stream is Yellow object 52175 to target 57803 at 139,121:
  49,780 orders from 180:10 through 311:03. Replay BUILD evidence identifies a
  Yellow Town Center at that coordinate, but the producing rule remains
  unproven. Separately, Yellow hull 32151 produced 792 and Green hull 59397
  produced 412 repeated home unloads. Source inspection proves
  `TRANSPORT-ROUTE-RECOVERY-CHECK` can reissue a home unload every 15 seconds
  indefinitely while garrison count remains positive; these 1,204 unloads are
  a proven sub-loop, not an explanation for the millions of other commands.
- **Current causal boundary:** the Green streams begin as individual passengers
  disappear from the three-second unboarded retry list and stop around their
  home unload, strongly correlating this instance with garrisoning. Other
  repeated streams prove the subsystem is broader than migration or relic
  ferry. The replay does not identify which script/built-in owner generated
  every engine ORDER or prove that command volume caused the earlier crash.
- **Unknown evidence:** the replay does not contain an exception code, faulting
  module, corrupting writer, stack, or linked dump. High command volume and the
  crash coexist but causality is not established.
- **Implementation:** none. Do not mix an unproven command-spam change into the
  same-zone migration P3B44T5 patch.
- **Acceptance criterion / next action:** after the user resumes crash work,
  correlate an exact ProcDump/Windows exception with this runtime and identify
  the first command-volume producer or corrupting writer before proposing a
  fix.

### Boar gathering abandoned after emergency Town Center garrison

- **Status:** INVESTIGATING; separate hunting/economy defect, not part of the
  transport-only behavioral patch.
- **User-visible symptom / direct evidence:** while P3B44T6 was running on
  2026-08-30, the user observed Yellow abandon gathering a boar at approximately
  22-24 minutes after its villagers garrisoned in the Town Center during an
  enemy attack. Color and approximate time were explicitly confirmed by the
  user. The supplied T6 replay does not expose Yellow's private hunt-state
  chat; remaining food and exact post-exit worker assignments remain unknown.
- **Source evidence / causal hypotheses:** `rawai-hunt.per:467-491` requires
  at least one hunter for the normal support retry. At `:497-571`, retry
  validation removes the original lurer if its current target is no longer
  the saved boar, then disables hunting and releases ownership if either the
  lurer lookup or boar lookup fails. A changed worker assignment is therefore
  conflated with target loss in that branch. Zero hunters can instead leave
  the ordinary retry ineligible. Neither branch is yet tied to this event.
- **Contradictory/alternative evidence:** built-in worker reassignment, a
  continuing threat, resource exhaustion, or a different hunt state remain
  untested; source inspection does not establish the in-engine transition.
- **Instrumentation/tests / latest result:** the all-player chat and relevant
  order sweep does not establish Yellow's hunt transition. WORK payloads lack
  worker/target fields in the current parser; absence of decoded boar orders
  does not contradict the user's observation. Initial-object metadata proves
  repeated target 4475 is Yellow's Town Center. Red's own logs show three
  active-to-released transitions at 07:34,18:57,29:08, which are separate
  evidence and not proof of Yellow's cause.
- **Implementation:** none for hunting; `rawai-hunt.per` is unchanged.
- **Acceptance criterion / next action:** improve the missing WORK decoding if
  reliably possible, or add bounded public owner/lurer/boar/threat transition
  diagnostics in a separately scoped hunting patch. A safe surviving carcass
  should regain gatherers after the threat ends
  without premature ungarrison, a second lure, or disruption of sheep/transport
  ownership. Do not merge a guessed hunting fix into the transport experiment.

### Port placement: opposite island shores and open-water access

- **Status:** OPEN; explicitly authorized on 2026-08-30 for the development
  cycle after the P3B44T7 replay is supplied, separate from salvage integration.
- **User-visible symptom / direct evidence:** the user reports Ports being
  placed in narrow crevices, causing problems for trade ships.
- **Requested behavior:** for an island start, place the two Ports on opposite
  sides of the island and avoid narrow crevices that obstruct ship traffic.
- **Requested controls / causal hypothesis:** investigate and adjust
  `sn-dock-placement-mode`, `sn-minimum-water-body-size-for-dock`, and
  `sn-dock-proximity-factor`. Their exact semantics and sufficiency for these
  requirements are not yet verified; do not treat parameter tuning alone as
  proof of shoreline clearance or opposite-shore placement.
- **Contradictory evidence / instrumentation/tests:** no new placement analysis
  or tests in this note-only session; exact sites and failure mechanisms await
  replay/source investigation.
- **Implementation / latest result:** none; documentation only. No runtime
  changes, deployment, full test suite, commit, or PR update.
- **Acceptance criterion / next action:** in the next development cycle,
  inspect Port placement across all players and verify the controls before
  choosing values. Validate opposite-side placement on island starts with
  suitable buildable shores, accessible builders, and clear ship approaches,
  including sustained trade traffic without crevice congestion. Preserve
  functioning early Port construction and existing transport behavior.

### Deliberately unchanged defects

This one-cause patch does not change or claim to fix:

- cliff-bound or otherwise unreachable landing points unrelated to friendly
  Scout obstruction;
- route-scouting, route-threat scanning, landing selection, or naval pathfinding;
- the still-unproven upstream cause of individual passenger nonboarding,
  migration passenger thresholds, migration escort ownership, or migration
  drop-site establishment outside exact landing-candidate screening;
- hostile-fire survival, enemy landing memory, Port placement, or transport
  production quantity;
- the separate allied-friendly-fire defense trigger;
- taunt 69 deletion, behind-cliff Shipyard construction, command flooding,
  Merchant Vessel growth, allied resource aid, Palintonon recovery, Market
  buying, Wonder construction, or cross-water allied relief;
- the unexplained heap-corruption crash, whose existing dumps show detection
  rather than the earlier corrupting writer.

## Replay evidence and artifacts

- Replay basename:
  `SP Replay v101.103.48987.0 @2026.08.29 110101.aoe2record`.
- SHA-256:
  `C1F85E836D59CBC2D77643D2608930DC3D7940C3ECFDC6081F0C08BBF833917F`.
- Duration: 58:51; the user manually resigned. This replay did not crash.
- Preserved lobby mapping: Red/Green/Yellow/Purple Roman Empire versus Orange
  Picts, Cyan Britons, Blue Germani, and Gray Gauls.
- External compact analysis:
  `G:\Projects\Codex\Rome at War AI\.analysis\replay-20260829-110101-p3b44-compact.json`.
- Repository evidence entry:
  `britain-4v4-20260829-110101-p3b44-transport-congestion` in
  `replay-benchmarks.json`.
- The prior immutable P3B44 deployment had 68 files and SHA-256
  `EE04DE7BFA1448E90D54E8AC592D0EEECF4E9DAD93100272D2941F0209B75846`.

P3B44T1 final-landing replay:

- Basename:
  `SP Replay v101.103.48987.0 @2026.08.29 122745.aoe2record`.
- SHA-256:
  `D891771AA04A4EA626A42B9F5353C495314E033FC00D312DECDB413C397B82D2`.
- Duration: 54:03; Red manually resigned. The replay parsed cleanly and
  contained the P3B44T1 marker from players 2 through 8.
- Preserved lobby mapping: Red/Green/Yellow/Purple Roman Empire versus Orange
  Picts, Cyan Britons, Blue Germani, and Gray Gauls.
- External compact analysis:
  `G:\Projects\Codex\Rome at War AI\.analysis\replay-20260829-122745-p3b44t1-compact.json`.
- Repository evidence entry:
  `britain-4v4-20260829-122745-p3b44t1-landing-escort` in
  `replay-benchmarks.json`.

P3B44T2 all-player transport replay:

- Basename:
  `SP Replay v101.103.48987.0 @2026.08.29 131027.aoe2record`.
- SHA-256:
  `932E900C02D50DD01B0FC24FF3B113F562BACE88F102B180C7316550B1412F88`.
- Duration: 1:43:19; parse errors: zero; marker `RAWAI-P3B44T2:443`
  serialized from players 2 through 8.
- Selected-color metadata independently validates the preserved lobby mapping;
  no team/color was inferred from row or slot.
- External analyses:
  `G:\Projects\Codex\Rome at War AI\.analysis\replay-20260829-131027-p3b44t2-compact.json`
  and
  `G:\Projects\Codex\Rome at War AI\.analysis\replay-20260829-131027-p3b44t2-full.json`.
- Systematic union: 28 active hulls, 393 load commands, 284 unload commands,
  108 load-to-unload phases, 10 load-only phases, and 4 unload-only phases.
  Per-player load/unload-phase counts were Red 54/17, Green 48/9, Yellow
  63/9, Purple 71/24, Orange 61/21, Cyan 65/25, Blue 13/2, Gray 18/1.
- Repository evidence entry:
  `britain-4v4-20260829-131027-p3b44t2-all-transport` in
  `replay-benchmarks.json`.

P3B44T3 all-player transport replay:

- Basename:
  `SP Replay v101.103.48987.0 @2026.08.29 151250.aoe2record`.
- SHA-256:
  `0C1C909D4BB36D3680FEDDACB7E2E74647665CA67B00F1C0F0406D093F2D95DD`.
- Duration: 59:33; parser errors: zero; no decoded resignation action; marker
  `RAWAI-P3B44T3:444` serialized from players 2 through 8.
- Selected-color metadata independently validates the preserved lobby mapping;
  no team/color was inferred from row or slot.
- External analyses:
  `G:\Projects\Codex\Rome at War AI\.analysis\replay-20260829-151250-p3b44t3-compact.json`
  and
  `G:\Projects\Codex\Rome at War AI\.analysis\replay-20260829-151250-p3b44t3-full.json`.
- External semantic audit helper:
  `G:\Projects\Codex\Rome at War AI\.analysis\audit_transport_20260829_151250.py`.
- Systematic union: 16 explicit Transport hulls, 157 load commands, 129
  point-coordinate sea unload commands, 45 alternating load-to-unload phases,
  and 4 terminal load-only phases. Generic building/siege ungarrison records
  were excluded. Per-player hull/load/unload totals: Red 4/29/23, Green
  2/18/22, Yellow 1/5/13, Purple 2/27/18, Orange 2/23/13, Cyan 1/24/2, Blue
  2/16/24, Gray 2/15/14.
- Repository evidence entry:
  `britain-4v4-20260829-151250-p3b44t3-all-transport` in
  `replay-benchmarks.json`.

P3B44T4 all-player transport replay:

- Basename:
  `SP Replay v101.103.48987.0 @2026.08.29 214328.aoe2record`.
- SHA-256:
  `36561ABA8EDCDA3B5623E491ED0222B2852C1435B4F461C713059261CF58B41B`.
- Duration: 1:49:40; parser errors: zero; no decoded resignation action;
  marker `RAWAI-P3B44T4:445` serialized from players 2 through 8.
- Selected-color metadata independently validates the preserved lobby mapping;
  no team/color was inferred from row or slot.
- External analyses:
  `G:\Projects\Codex\Rome at War AI\.analysis\replay-20260829-214328-p3b44t4-compact.json`
  and
  `G:\Projects\Codex\Rome at War AI\.analysis\replay-20260829-214328-p3b44t4-full.json`.
- External semantic helpers and terrain diagnostic:
  `G:\Projects\Codex\Rome at War AI\.analysis\summarize_p3b44t4.py`,
  `G:\Projects\Codex\Rome at War AI\.analysis\render_p3b44t4_map.py`, and
  `G:\Projects\Codex\Rome at War AI\.analysis\p3b44t4-green-migration-terrain.png`.
- Systematic union: 35 explicit/likely Transport hull IDs, 509 loads, 249
  point unloads, 120 alternating phases, 7 terminal load-only phases, and 2
  unload-only phases. Per-player hull/load/unload/phase totals: Red 10/67/70/26,
  Green 2/58/26/7, Yellow 4/61/27/20, Purple 5/47/6/4, Orange 2/50/45/21,
  Cyan 5/99/56/31, Blue 5/109/15/8, and Gray 2/18/4/3.
- Repository evidence entry:
  `britain-4v4-20260829-214328-p3b44t4-all-transport` in
  `replay-benchmarks.json`.

P3B44T5 all-player transport replay:

- Basename:
  `SP Replay v101.103.48987.0 @2026.08.29 232526.aoe2record`.
- SHA-256:
  `B12989601E59BDE4D4BE3ACA4D6C9B0F2F322E31FA7D9E97198AA3CDE61924CE`.
- Duration: 5:11:04; action-stream parser errors: zero; no decoded
  resignation action; marker `RAWAI-P3B44T5:446` serialized from players 2
  through 8.
- Selected-color metadata independently validates the preserved lobby mapping;
  no team/color was inferred from row or slot.
- External full analysis:
  `G:\Projects\Codex\Rome at War AI\.analysis\replay-20260829-232526-p3b44t5-full.json`.
- External semantic helper:
  `G:\Projects\Codex\Rome at War AI\.analysis\summarize_p3b44t5.py`.
- Systematic union: 42 explicit/likely Transport hull IDs, 1,678 loads, 2,054
  point unloads, 352 alternating phases, 5 terminal load-only phases, 5
  initial unload-only phases, and 11,437 raw transport actions. Per-player
  hull/load/unload/phase totals: Red 8/189/328/93, Green 3/167/459/40, Yellow
  3/81/837/24, Purple 1/484/64/64, Orange 9/238/92/36, Cyan 9/210/173/51,
  Blue 6/84/78/39, and Gray 3/225/23/5.
- Forty-eight public migration candidate missions yielded 95 path-clear, 4
  wrong-zone, and 36 path-rejected events. All 95 clear events had an exact
  same-second hull unload; no invalid event did. Red completed one full
  landing/drop-off/retask lifecycle and three later resource-wait landings.
- Repository evidence entry:
  `britain-4v4-20260829-232526-p3b44t5-all-transport` in
  `replay-benchmarks.json`.
- External cross-replay boarding audit helper:
  `G:\Projects\Codex\Rome at War AI\.analysis\audit_boarding_departure_20260829.py`.
  It is diagnostic material outside the repository and must not be committed.
- P3B44T6 boarding evidence entry:
  `britain-4v4-20260829-232526-p3b44t6-boarding-evidence` in
  `replay-benchmarks.json`. It reuses the same source replay for the distinct
  boarding-lifecycle acceptance target and is `fresh-replay-required`.

P3B44T6 all-player transport replay (2026-08-30 audit):

- Basename: `SP Replay v101.103.48987.0 @2026.08.30 114855.aoe2record`.
- SHA-256: `A26B08497C5168F942A6CA67903FAC61AD32CD2C8BFF2D07BDA69B2DE9512CE8`.
- Duration 75:25; zero action-stream parse errors; no decoded resignation.
  Ending cause is unknown, not assumed to be a crash or manual termination.
- Markers `RAWAI-P3B44T6:447` from players 2-8; before editing, all 68 installed
  files matched T6 hash
  `D5A2314E461603F68D5327E71BD7FB3737F0518C8969F2D5A4C45809B11598EB`.
- Use parser root `G:\Projects\Codex\Rome at War AI\.analysis\replay_parser_kjir`
  with repository `tools/analyze_replay.py`. The older `replay_parser` fails
  this header; do not fall back to inferred colors. The supported parser
  validates the original selected colors and resolved teams independently.
  WORK target fields and some AI_ORDER coordinates remain incomplete.
- External full report:
  `G:\Projects\Codex\Rome at War AI\.analysis\replay-20260830-114855-p3b44t6-full.json`.
- External all-player semantic audit helper and outputs:
  `G:\Projects\Codex\Rome at War AI\.analysis\audit_p3b44t6.py`,
  `G:\Projects\Codex\Rome at War AI\.analysis\p3b44t6-transport-audit.txt`, and
  `G:\Projects\Codex\Rome at War AI\.analysis\p3b44t6-transport-audit.json`.
  The helper reuses `summarize_p3b44t5.py` for existing acceptance checks.
  Its CORRECTED_PLAYER_TOTAL section adds Yellow's telemetry-identified hull
  omitted by the older movement/unload-only identity heuristic.
- Systematic union: 22 hulls, 183 loads, 142 point unloads, 55 alternating
  load/unload phases and 7 final load-only phases. Empty aborted missions can
  be load-only: these counts are not interchangeable with successful voyages.
- Per-player hull/load/unload/phase totals: Red 1/4/4/4, Green 1/8/0/0,
  Yellow 1/8/0/0, Purple 2/25/28/7, Orange 4/29/30/16, Cyan 4/27/23/7,
  Blue 3/31/15/6, Gray 6/51/42/15. All 4,176 raw SPECIAL/UNGARRISON records
  were screened; non-transport Town Center garrisons remain outside that union.
- Nine public migration boarding terminals are full, six partial and seven
  empty aborts. Ten candidate missions yield 21 clear/same-second unloads,
  1 wrong-zone rejection and 26 path rejections with zero invalid unloads.
- Six assault landing windows complete with zero active-hull guard refreshes.
  Five are Orange's safe partial lifts; Purple completes a full lift. Seven
  exact relic outbound and three return-readiness events preserve the T4 check.
- Migration escort overlap recurs (7 guards across 2 Purple candidate missions).
  Gray's 19 settlers reboard at 57:16 and 71:29 after remote landings; successful
  economic settlement is not established. The existing drop-site defect stays
  separate from reservation loss.
- 727,415 ACTION records include 355,625 ORDER and 135,582 AI_ORDER records.
  Yellow worker 31642 targets its initial TC 4475 in 27,669 repeated ORDERs
  from 17:52 to 47:50. This identifies the destination, not its producing
  controller or a crash cause; broad command-volume work remains deferred.
- Repository benchmark: `britain-4v4-20260830-114855-p3b44t6-all-transport`.
  T6 partial acceptance is runtime-confirmed; this entry's next T7 ownership
  acceptance is fresh-replay-required.

P3B44T7 all-player transport replay (2026-08-30 audit):

- Basename: `SP Replay v101.103.48987.0 @2026.08.30 131412.aoe2record`.
- SHA-256: `04AB5E6664F9DBE0284E320A99AB16070DBC00DE67FE876AC8C5512176E7DDB5`.
- Duration 98:29; zero parse errors; Red resigns at 98:28. Markers from players
  2-8 identify T7:448; full source/deployment hash was checked before editing.
  Decoded selected colors/resolved teams agree with preserved fixture
  `britain-4v4-lobby-20260827-6969d5e2`: Red/Green/Yellow/Purple Romans versus
  Orange Picts/Cyan Britons/Blue Germani/Gray Gauls. No slot-color inference.
- Screened all 5,390 SPECIAL/UNGARRISON records: 25 hulls, 378 loads, 205 point
  unloads, 119 alternating load/unload phases and five final load-only phases.
  Command phases are not completed missions. Per-player hull/load/unload/phase:
  Red 4/96/50/28; Green 1/42/21/8; Yellow 1/1/3/1; Purple 4/45/24/22;
  Orange 3/58/43/24; Cyan 1/28/1/1; Blue 7/39/35/11; Gray 4/69/28/24.
- 103 candidate snapshots: 43 military flag 4, 58 identified migration flag 4,
  two missing migration candidates. All 39 identified mining snapshots retain
  flag 4. Ten safe partial assault departures; three Purple completed landing
  windows and zero active-hull guard refreshes. Twelve migration-candidate
  missions produce 20 clear events (18 same-second unloads, Red's other two
  next-second), two wrong-zone and sixteen path rejections, with zero rejected
  same-second unloads. Two relic outbound/return readiness pairs survive.
- Purple's 90:44 partial lift completes at 93:47. Exactly nine boarded IDs
  receive the land order, excluding stopped straggler 40008. The older audit
  falsely required the army order's destination to equal the ship unload point;
  RETURN-CHECK actually orders toward the enemy target. The corrected offline
  comparison passes exact manifest-minus-stopped membership. No gameplay
  regression or behavioral patch was needed for this audit false negative.
- DE_RETREAT counts: Red 36, Green 35, Yellow 31, Purple 22, Orange 1, Cyan 23,
  Blue 53, Gray 1. All 202 raw payloads satisfy the observed `<IffII` prefix
  (target, x, y, count, mode), followed by count object IDs at offset 20.
  This validates extraction for these packets, not every replay version.
- Exact overlaps and separate STOP evidence are in the competing-orders
  defect ledger above and benchmark
  `britain-4v4-20260830-131412-p3b44t7-ownership`.
- External artifacts under `G:\Projects\Codex\Rome at War AI\.analysis`:
  `replay-20260830-131412-p3b44t7-full.json`,
  `p3b44t7-transport-audit.txt`, `p3b44t7-transport-audit.json`,
  `p3b44t7-ownership-audit.json`, `p3b44t7-packet-evidence.json`.
  Helpers: `audit_p3b44t6.py` (all-player audit, corrected partial comparison),
  `audit_p3b44t7_ownership.py`, and `inspect_t7_packets.py` (all retreats plus
  targeted AI_ORDER IDs 4638/4639/53368/40008). The latter output has 48,912
  targeted packets; adapt watch IDs for another replay rather than assuming
  these IDs recur. The ownership helper takes the full report as argv[1].
- Reproduction tools: use Python 3 at
  `C:\Users\LostSoul\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`;
  PATH Python is version 2. `tools/analyze_replay.py` arguments are parser root,
  replay path, `--output` full report. Audit helper arguments are full report
  and output `.txt`; packet helper takes replay path. Reuse `replay_parser_kjir`.
- Decoder limits: stock parsing omits retreat members and misaligns several
  AI_ORDER fields. Targeted raw parsing keeps bytes and length/count checks;
  AI_ORDER order is at offset 16 in the inspected packets, not the decoded
  floating-point x field. Packed-ID heuristics and coarse episode windows
  require care; a post-unload order is not automatically boarding interference.

### Architectural ownership audit of the same T7 replay

- Requirement/aggregate record: `TASK-OWNERSHIP.md`. This preserves the new
  user directive without requiring access to the conversation or attachment.
- New external artifact:
  `G:\Projects\Codex\Rome at War AI\.analysis\p3b44t7-task-ownership.json`.
  Generated by repository-local `tools/audit_task_ownership.py`; its complete
  reproduction command is in `TASK-OWNERSHIP.md`. Use the same Python 3 and
  `replay_parser_kjir` paths recorded above.
- Prior hull/color/partial-landing evidence input:
  `p3b44t7-transport-audit.json`, SHA-256
  `C0D7CD60350628E7AEDEBA16D5304E74C4D97C45EC84AB9C3085813F216DEB08`.
  This older artifact has no embedded replay hash; its T7 association is
  recorded here, not automatically proven by the new tool. The new report
  fingerprints both inputs and explicitly records the dependency.
- Full-stream decoding uses exact packet lengths for SPECIAL/UNGARRISON,
  WORK, AI_ORDER and every DE_RETREAT. It retains raw bytes, file offset,
  millisecond time, stream sequence, all selected IDs and actual target/order.
  No object-ID magnitude shifts or arbitrary task timeout. Zero decoding
  failures for this replay; no claim of universal version compatibility.
- All 378 load commands are represented in 132 evidence-delimited windows
  (33 assault, 41 migration, 58 unresolved/recovery/relic), alongside all 202
  retreats. The 1,053 passenger-window instances split 65 corroborated
  successful without observed conflict / 83 pre-boarding conflicts with owner
  evidence / 905 unresolved. The unresolved group includes 323 conflicts with
  uncertain timing or ownership. No individual deaths or unavailability are
  proven, not a claim that none occurred.
- Source inventory retains 247 command/build-delegation rules and 248 selection
  rules with facts/actions/line numbers. It is not a complete certification of
  native strategic-number behavior or all permission/release paths. Source
  gaps and every global-recall source are classified in `TASK-OWNERSHIP.md`.
- T8 remains installed unchanged. No shared ownership, threat-preemption or
  allied-anchor implementation is present. Required section-H gameplay tests
  and architecture runtime acceptance remain pending.

Replay/savegame files, compact parser output, crash dumps, and Rome at War data
mod files remain external and must never be committed to the AI repository.

### P3B44T8 replay audit (2026-08-30)

- Source: `SP Replay v101.103.48987.0 @2026.08.30 154021.aoe2record`, SHA-256
  `C7BDFAF53DE72F03012C5AD88F4B930E9B7670A07CDC96490489F7428F2CE29F`.
  Duration 67:33; zero decoder failures. No recorded resignation; ending cause
  is not inferred. Players 2-8 publish T8:449, and the complete installed/source
  runtime matches the hash above. Selected-color metadata agrees with the
  preserved Red/Green/Yellow/Purple Roman team and Orange/Cyan/Blue/Gray team.
- All 3,476 SPECIAL/UNGARRISON records were screened. Transport hull union 19,
  190 loads, 130 point unloads, 47 alternating load/unload phases and seven
  terminal load-only phases. Never-loaded empty blockers are not in that hull
  union. Boarding audit: 58 windows, 354 passenger-window instances. Command
  phases and orders are not voyage-success acknowledgments.

| Color | Boarding windows | Full-load corroborated, no conflict | Conflict + later ashore evidence | Unresolved | Retreat packets |
|---|---:|---:|---:|---:|---:|
| Red | 11 | 23 | 6 | 37 | 5 |
| Green | 4 | 0 | 0 | 31 | 16 |
| Yellow | 3 | 0 | 1 | 2 | 12 |
| Purple | 3 | 0 | 3 | 9 | 26 |
| Orange | 14 | 2 | 0 | 82 | 14 |
| Cyan | 1 | 0 | 0 | 1 | 13 |
| Blue | 18 | 3 | 22 | 128 | 1 |
| Gray | 4 | 0 | 2 | 2 | 13 |
| Total | 58 | 28 | 34 | 292 | 100 |

- Unresolved includes 108 conflicts whose pre-boarding timing/owner continuity
  is unproven. No individual death/unavailability is proven by command absence.
  The 56 candidate snapshots (26 military, 30 migration) all retain flag 4.
- All 100 retreat packets match 56 RAW44O invocations: land defense 28/47,
  naval defense 16/32, siege escalation 11/19, loss regroup 1/2 (calls/packets).
  Sources 5/6 absent. One call can emit consecutive land/naval packets at the
  same clock; do not misclassify the second packet as untagged/native. Red's
  source-3 boarding overwrite is detailed in TASK-OWNERSHIP.md.
- Orange 40825 is the only logged departure-congestion episode: blocker 40598
  ordered at 53:43, verified clear at 53:52, departure resumed at 54:00. It reaches
  landing at 54:17 but times out at 55:02. Clearance PASS is not voyage completion.
  Red's late migration has no such detection; manual intervention and phase
  timing are preserved in its separate ledger entry above.
- Seven assault landing windows have zero guard refreshes targeting the active
  hull. Orange completes at 41:49, Red at 65:33; five other windows time out.
  Nine migration landing-candidate missions yield 18 clear events with matching
  same-second unloads; one wrong-zone and 20 path rejections emit no such unload.
  All nine have zero active migration-hull guard overlap. Landing-screen and
  escort protections survive these checks; settlement/drop-off success is not
  established by them. Five exact relic outbound and four return readiness
  events occur; unmatched/pending missions remain unresolved.
- Raw artifacts stay in `G:\Projects\Codex\Rome at War AI\.analysis`:
  `p3b44t8-command-stream.json` (825,076 retained commands/chats, exact arrays),
  `replay-20260830-154021-p3b44t8-full.json`,
  `replay-20260830-154021-p3b44t8-exact.json`, `p3b44t8-transport-audit.txt/json`,
  `p3b44t8-task-ownership.json`, and `p3b44t8-recall-sources.json`.
  External `audit_p3b44t8.py` orchestrates the existing repository decoder and
  legacy lifecycle helpers with their ID-magnitude normalization disabled.
  Join recall sources by exact retreat sequence; the generic ownership report's
  historical `likely_source` text is not the authoritative T8 source attribution.
- Reproduce exact stream/ownership with `tools/audit_task_ownership.py`, the T8
  replay, parser root `../../.analysis/replay_parser_kjir`, T8 transport audit,
  and external output. For caller attribution match preceding same-player
  RAW44O labels in stream order (first packet 14-38 ms later here); allow the
  same label on its adjacent same-clock land/naval bundle only. Preserve all
  unmatched labels/packets rather than inferring native origin.
- Computer Use playback verified the Red Port scene and cargo rather than
  inferring physical positions from orders. Replay left paused at 66:50.
  That initial Red audit changed no gameplay code, marker, installed files,
  Git commit or PR; the later prepared T9 diagnostic changes are recorded below.
- Evidence validation: PASS, all 30 replay benchmarks validate and
  `git diff --check` passes. No full regression suite was run for this
  documentation-only audit. Intentional changes are HANDOFF.md,
  TASK-OWNERSHIP.md and replay-benchmarks.json; AGENTS.md remains committed
  and unchanged. No runtime defect is closed by these document checks.

### T8 missed Blue obstructions / prepared T9 diagnostics

- **Coverage correction:** every reconstructed command episode is not every
  physical obstruction. The 19 mission-linked hulls exclude never-loaded empty
  blockers. Missing congestion logs cannot establish a clear path or successful
  movement. Both user observations are accepted; the screenshot does not itself
  identify a hull ID, and enemy selection in the 66:50 image does not expose cargo.
- **49:11:** Blue hull 35026 receives an assault load of ten at 48:33.312,
  then a home unload at 49:42.634, with no intervening hull departure order.
  Similar load-to-home-unload waits recur at 29:47, 32:49, 35:43, 38:47,
  42:00 and 45:28. An unavailable route-screen Scout is a hypothesis, not a
  finding: T8's relevant hold reasons are private and absent for Blue.
- **66:50:** the corresponding migration episode is hull 36912: seven aboard
  by the partial-load terminal at 64:31.600; six orders to (134,99) from
  64:31.634 through 65:48.306; six home unloads to (204,16) from 66:03.632
  through 67:21.640. The screenshot falls within failed return attempts.
  Migration route/return retries have no active blocker-clearance hook.
- **Broader re-screen:** the same hull also issues six orders to (113,0)
  from 59:42.694 through 60:59.338 and a home unload at 61:14.666; this is an
  additional failure-pattern candidate, not independently proven collision.
  Repeated orders alone are insufficient: Red 31341 repeats nine departure
  orders at 63:47-64:54 yet lands remotely at 65:03 and completes at 65:33.
  Yellow/Purple/Cyan/Gray's unresolved boarding is not declared successful
  merely because no repeated movement orders or blockage tags were found.
- **External evidence:** `.analysis/p3b44t8-blue-4911.jpg`, SHA-256
  `4E0DF49D3E008D2F93C2EA027FC24F76B102429AFACFD15FC93536EE17156DF1`;
  `.analysis/p3b44t8-blue-6650.jpg`, SHA-256
  `EFF7EF6100410DADDFA1553979B58C2D4581BA5DFA1C61D80EAA48126C0219F9`.
  Paths are relative to workspace root, outside this AI-only repository.
  `.analysis/inspect_t8_congestion.py` reproduces exact Blue windows and the
  all-player repeated hull-command screen from the preserved command cache.
- **T9 diagnostic contract:** RAW44C migration terminal phase 1 = exhausted
  route progress; phase 2 = occupied return failure. Both record exact hull ID,
  actual position, origin, cargo, idling and group; only phase 1 records a
  distance because return checks have no established distance reference.
  Each observer uses the existing owner's selected hull and three private
  scratch goals (1163-1165); no searches, commands, timers or controller writes.
  Identical terminal conditions leave the state immediately, bounding output
  to one snapshot per failed leg. Assault ready logs identify the exact hull;
  the accompanying target value is the load quota, not an independent cargo read.
- **Public assault hold codes:** 1 no safe approach; 2 defended corridors;
  3 no screening ship; 4 screen under fire; 5 screen waypoint unreachable;
  6 screen lost; 7 defended route revealed; 8 landing scout under fire;
  9 landing unreachable; 10 landing scout lost; 11 defended landing revealed;
  12 landing timeout. Each existing terminal emits hull + reason once.
- **Adversarial read-only review:** ACCEPTED absent public hold reasons,
  misleading inherited return distance, and command-census overclaim; addressed
  as above. Moving every nearby ship is REJECTED: active/reserved/occupied
  blockers are not established safe to retask. Exact neighbor identity, task
  eligibility and unassisted physical clearance remain unresolved, not covered
  by these observers. Preserve successful Orange clearance and Red landing.
- **Validation:** PASS PER structural/operand checks, 138 regression tests,
  unchanged T7 gameplay-program fingerprints after removing observational
  additions, 30 replay benchmarks, and whitespace check. T9 runtime validation
  PENDING; blockage status INVESTIGATING. Installed T8 remains untouched; no
  new long replay is requested merely to substitute more logs for resolution.

## Validation performed

### R1 18:10 replay audit and R3 identity delivery (latest session)

- Replay `SP Replay v101.103.48987.0 @2026.08.30 181054.aoe2record`, 22:54;
  SHA-256 `FE6D9AAFF07A6478A29BAD07D4FC210F5168B11F2A116340DB4C9A2175CFA91A`.
  User identifies it as R1. Selected-color metadata maps replay IDs 1..8 to
  Red/Green/Yellow/Purple/Orange/Cyan/Blue/Gray, matching the established teams.
  Extreme, 400 population, Fast 2.0, shared exploration; resignation at 22:54.
- **Breadth:** 66,324 retained exact command/chat events, zero packet-array
  decoder failures; all 11 command-linked hulls / 15 boarding episodes. Every
  episode has one passenger and corresponds to scout-ferry selection, not
  mining-worker migration. No assault boarding occurs before cutoff.

| Color | Boarding episodes | Full-load confirmations | Empty aborts |
|---|---:|---:|---:|
| Red | 2 | 2 | 0 |
| Green | 2 | 0 | 2 |
| Yellow | 1 | 0 | 1 |
| Purple | 1 | 0 | 1 |
| Orange | 2 | 0 | 2 |
| Cyan | 1 | 0 | 1 |
| Blue | 3 | 3 | 0 |
| Gray | 3 | 0 | 3 |

- **Root-cause evidence, scout preemption:** all 20 DE_RETREAT packets match
  source-1 land-defense labels. Four intersect boarding: Green scout 4643,
  hulls 31508/31734 at 15:21.180 and 18:48.512; Orange scout 4646,
  hulls 30975/31410 at 12:34.644 and 14:38.636. Labels expose migration state 3;
  retries/samples establish still-ashore passengers. The source invokes global
  `up-retreat-now` without transport cancellation/permission. Scout interference
  subcause ROOT-CAUSE-PROVEN; common ownership implementation remains OPEN.
- **Exploration task:** Purple scout 4645 begins boarding hull 31108 at
  13:07.784; exploration orders start 13:08.876 and repeatedly replace retries.
  Orange 4646 also receives exploration during both lifts. Source constants
  identify order 705/action 605 as exploration, not ordinary move. Purple's
  13:11.760/13:38.422 snapshots show exploration with flag 4 retained. This is
  a second competing task, not proof of a worker-economy writer. Exact native
  versus script-delegated boundary/release mechanism still needs an engine
  comparison before a guessed ownership lock is implemented.
- **Separate timeout class (outside ownership patch):** five aborts have no
  competing packet and retain enter order 717 while approaching: Yellow
  distance 60->21, Cyan 58->19, Gray 82->49 / 70->44 / 74->36. The roughly
  30-second load deadline expires before boarding. Eventual reachability and
  safe replacement timing are not demonstrated. No timeout/navigation patch.
- **Result limits:** five full-load confirmations do NOT prove productive
  landing/settlement. Red's remaining self-visible diagnostics include rejected
  scout landings and return failure. Worker/assault acceptance is untested.
  Initial full-object-header parse fails in the current parser; no unit-type
  claims are based on ID magnitude. A progress update incorrectly called the
  passengers villagers; this was corrected explicitly to scout ferries.
- **Spam cause confirmed:** all players emit `RAW44W coverage gap: 0` at
  05:40-05:41; no subsequent begins/resumes, first boarding only 10:05.882.
  The user's observation of stopping around Port completion is preserved;
  source/trace establish the stop condition was quota exhaustion, not Port
  construction. BUILD packets do not establish actual completion timestamps.
- **New diagnostic defect — FIXED-PENDING-RUNTIME:** no RAWAI marker, map0..3
  or schema survived startup (also absent from raw replay bytes). The first
  recorded chat is Gray's unmatched `end:328`. All 4,118 incomplete/unverified
  brackets remain unverified; zero players pass fingerprint checks. Do not
  bypass identity validation. R1 source identity rests on user report and the
  archived deployment, not an embedded fingerprint. Exact engine loss/queue
  mechanism remains unproven.
- **R3 implementation:** retain R2 gating, all 351 sites and gameplay program.
  Send marker plus four map fragments after startup: nominal initial times
  8..29 seconds by player, three attempts, 30 seconds apart, independent of
  writer budget. Fifteen extra identity records per player total; two private
  scratch goals 13010/13011, included in collision checks. This repairs the
  startup-only delivery assumption, not gameplay ownership. Literal count
  1,466 total / 19 writer (project limits 1,500/32).
- **Validation:** PASS 155 tests (17 writer tests), compiled PER checks,
  original gameplay/jump equivalence, literal guard, bounded staggered identity;
  PASS 31 replay benchmarks and whitespace. PASS deployment and independent
  recheck of all 68 files. Read-only adversarial review ACCEPTED no startup
  delivery assumption, quota-independent bounded retries, and preserved R1/R2
  maps; REJECTED treating missing labels as native proof. R3 runtime PENDING.
- **Artifacts:** external `.analysis\p3b44t10r1-{command-stream,exact,
  transport-audit,task-ownership,summary}.json`, transport-audit.txt, and
  `replay-20260830-181054-t10r1-full.json`. Orchestration is the external
  `audit_writer_replay.py`, reusing exact decoder + established all-player audit
  with magnitude normalization disabled. `summary.json` retains every episode,
  exact recall packet/label, exploration overwrite and coverage cutoff.
- **Next:** use the matching R1/R2 historical map for existing recordings; R3
  for the next test. Verify identity and useful boarding traces. Prioritize
  native exploration handoff and reservation-aware routine defense in the
  authorized shared ownership work; do not lose the established scout causes
  while resolving the still-unattributed T7 worker WORK cases. No new workspace,
  gameplay patch, commit, push or PR update in this audit/diagnostic repair.

### T10R2 off-mission trace spam (previous session)

- **Status:** FIXED-PENDING-RUNTIME. **Symptom/direct evidence:** user screenshots
  at 04:51/04:54 show Red `RAW44W end: 41`, assault/migration state 0, hulls -1;
  04:55 shows Orange with the same site/state values. User reports repetition.
  Still images alone cannot count emissions (the first two may show retained
  chat); the compiled unconditional rule independently establishes repetition.
- **Root cause:** site 41 (`rawai-general.per:43`) excludes
  `migration-boarding-group` from generic villager cleanup, then mutates group 0.
  The compiler matched the reserved group's name anywhere in the action block,
  misclassifying an exclusion as an ownership change. The exemption bypassed
  boarding gating, generating 12 chat records each qualifying pass until the
  96/minute or 512-total invocation budgets stopped it. Not literally unbounded,
  but capable of spending coverage before the first mission.
- **Implementation:** classify only actual create/flag/reset command destination
  operands. All 351 sites audited: remove site 41's false exemption and include
  five previously omitted real hull/passenger mutations (131/132/197/233/240).
  There are now 49 genuine reservation-boundary sites. Site 41 remains traced
  during boarding; no gameplay rule, quota, context field or source ID removed.
- **Contradictory/limiting evidence:** unchanged state values do not establish
  absence of a competing command. Do not suppress invocation evidence merely
  because transport state/hull stayed the same; repeated commands can be causal.
  White `refresh check vills/update facts timer` messages come from older
  rawai-timers.per 15-second rearming logs, separate from RAW44W. Left unchanged
  in this bounded classifier repair; blanket timer-log cleanup is outside it.
- **Instrumentation/tests/review:** PASS 154 tests, including an exact site-41
  false-positive fixture, all four reservation aliases/acquire/release forms,
  all-site gating/quotas, string budgets, and original-program/jump equivalence.
  PASS generated PER checks, 30 benchmarks and whitespace. Read-only adversarial
  review ACCEPTED missing real mutation aliases and R1 map preservation;
  REJECTED deleting site 41 or logging only state changes (loses writer evidence).
- **Acceptance/latest result:** PASS all 68 deployment hashes and independent
  read-only recheck. R2 must show no recurring site-41 logs with both missions
  idle, retain that caller during boarding and retain true reservation changes.
  Gameplay decisions and working full/partial lifts/ordinary attacks must survive.
  Runtime result PENDING. The passenger-ownership defect remains INVESTIGATING.
- **R1 compatibility:** preserved map path above, fingerprint
  `316DCF71092AC28688ECFDA73F8323D2D492246B98CF2596AF526C86B921B13C`, runtime
  `D4D63605982616602778246C9ED864332E548B7883223A49ED58D49385EDD718`.
  It was regenerated/verified BEFORE editing the compiler. Do not use the R2
  map to attribute R1 packets; runtime replay fingerprints still govern identity.
- **Next:** keep the user's current R1 replay analyzable; use R2 on the next
  match. No new workspace, gameplay patch, commit, push or PR update this turn.

### T10R1 string-table compile regression (previous session)

- **Status:** FIXED-PENDING-RUNTIME. **Symptom/direct evidence:** user reports
  `rawai-init-goals.per`, line 362, `ERR6003: String table full` on T10:451.
  The referenced statement is the build-marker chat, not malformed syntax.
- **Cause:** the T10 generator repeated 12 quoted trace templates at 351 sites:
  4,219 writer literals / 5,665 total literals across the payload, versus 1,446
  in plain T9 input. Runtime emission quotas did not bound compile-time strings.
  String defconsts reuse table indexes; identical quoted operands can allocate
  repeatedly (see AI reference [defconst](https://airef.github.io/commands/commands-details.html#defconst)
  and [xs-script-call](https://airef.github.io/commands/commands-details.html#xs-script-call)).
  Exact DE capacity/sharing across players is not established; the early marker
  error location does not establish which earlier allocation exhausted it.
- **Contradictory evidence:** 150 structural/tool tests and matching installation
  hashes had passed. They did not exercise the engine compiler or string budget;
  the user's failure overrides the previous compilation-PENDING assessment.
- **Implementation:** generated prelude defines the 12 templates once, before
  their users. All 351 sites, numeric IDs, 12 fields per invocation, quotas,
  source-map checks, original actions and jump destinations are preserved.
  Corrected marker T10R1:452 distinguishes this build from failed T10:451.
- **Instrumentation/tests:** count literal occurrences, ignoring comments but
  respecting semicolons/escaped quotes in text; fail compilation/deployment
  above project budgets of 1,500 payload / 32 writer literals. These are
  conservative project caps including inactive civ files, NOT claimed engine
  limits. Current counts: 1,465 payload / 19 writer; eight-player projection
  11,720 (informational only). Regression recreates and rejects the exact
  failed 5,665/4,219 allocation pattern. String-name collisions fail closed.
- **Preserved behavior/acceptance:** no changes to military, migration or
  navigation decisions. Original-program equivalence/jump tests PASS. Engine
  acceptance requires a fresh eight-player startup without ERR6003 and correct
  marker/map/trace delivery; subsequent all-player replay must preserve attacks
  and successful full/partial transport missions.
- **Latest result:** PASS 152 tests (14 writer tests), source and generated PER
  structure/operand checks, 30 benchmark metadata validations and whitespace.
  PASS installation plus separate read-only verification of all 68 files.
  Manual adversarial review ACCEPTED occurrence-count guard, definition-before-
  use and unchanged string contents/operands; REJECTED lowering runtime quotas
  as a compile-space fix. Engine startup/delivery PENDING, gameplay defect OPEN.
- **Historical failed identity:** T10:451 payload SHA-256
  `02A76B0FCC1EDA35D85047255A1A4CA1DF7EA5913C793FC3C5A14B83B54EFFFD`;
  map `9AC4950C2744171DC0764C9A5AF25A27C2B606A6504C5E38ECCD0F0F2CD46E0B`.
  No successful T10 replay validates that build. Current map is regenerated
  in the existing `writer-trace-sites.json`; no new workspace/artifacts needed.
- **Next action:** restart the game and check a fresh normal lobby startup
  first, then use T10R1 traces for passenger-writer attribution. No congestion,
  economy, salvage, Port or ownership-behavior patch was added in this repair.

### T10 passenger-writer telemetry (initial implementation; compile failed)

- **User objective:** establish which controllers redirect reserved transport
  passengers; this takes priority over additional congestion analysis.
- **Implementation:** `tools/writer_trace.py` instruments this checkout in memory;
  `writer-trace-sites.json` maps 351 stable IDs to source rules, command APIs,
  group operations and native policy/delegation. No sites in the current
  inventory are excluded. Future unreviewed/consuming predicates are explicitly
  excluded, never silently evaluated twice. Original facts/actions/disable-self
  are retained; existing relative jumps retain their original destinations.
  The farm-building jump uses a private guarded return through its logger.
- **Recorded context:** pre/post assault and migration state and hull, current
  selected object ID/flag, and source rule begin/end. Source group operations
  expose reservation acquisition/release intent. The selected object is not
  assumed to be the commanded army; actual command members come from replay
  packets. This observes existing ownership behavior, not a new permission lock.
- **Bounds:** at most 512 recurring invocations per player, at most 96 per
  minute, plus 16 single-use initialization sites. Each invocation emits 12
  short records. Gap/resume messages identify exhausted coverage; no per-sweep
  logging after exhaustion. Ordinary tracing is active during assault/migration
  boarding; reservation boundaries and single-use setup are also traced.
- **Queued-delivery evidence:** T8's after-command `route-screen landing cleared`
  logs precede matching ORDER packets by 14 ms (40:38.024 -> 40:38.038) and
  18 ms (44:08.686 -> 44:08.704). Therefore a chat bracket is not a packet
  delivery fence. `tools/audit_writer_trace.py` retains complete brackets and
  all compatible deferred issuers within 100 ms, with exact passenger-list
  intersections. Multiple candidates remain ambiguous; unbracketed commands
  do not prove native tasking, and 100 ms is not an engine latency guarantee.
- **Build identity:** four short RAW44W map records bind every player's trace
  to the exact generated source map. Missing/wrong fingerprints refuse source
  attribution. Replay-visible build is T10:451, not the plain T9 input marker.
- **Reproduce:** from this worktree using the recorded Python 3 executable,
  run `tools/writer_trace.py --manifest writer-trace-sites.json`, then
  `tools/sync_test_ai.py <installed-directory-above> --writer-trace` to check;
  append `--apply` only to deploy. For the next replay, append
  `--writer-manifest writer-trace-sites.json` to the existing all-player
  `tools/audit_task_ownership.py` command. Use its matching transport hull audit,
  not a prior replay's hull list. The report adds `writer_trace`, including
  identity verification, exact source sites, packet candidates and quota gaps.
- **Read-only adversarial review:** ACCEPTED queued command delivery (do not
  attribute merely between chat tags), exact jump-target preservation, native
  delegation versus immediate orders, full source-map identity, and explicit
  bounds. Tests cover these, original-program equivalence and observer mutation
  restrictions. REJECTED nearest-log attribution, flags-as-native-lock, and
  treating all unmatched WORK packets as a native mechanism.
- **Validation:** PASS all 150 tests, including 12 writer-telemetry tests for
  compiled PER structure/operands, unchanged original rules/jumps, source-map
  identity, deferred delivery and predicate safety; PASS 30 replay benchmarks
  and whitespace check. Deployment and separate
  read-only verification PASS for all 68 generated files and the hash above.
  Subsequently engine compilation FAILED with ERR6003; see the T10R1 repair
  above. Log delivery and gameplay non-regression still need a fresh corrected
  match. Passenger-stealing remains INVESTIGATING, not CLOSED.
- **Next:** use T10 to locate first competing calls in all players' boarding
  windows, retaining the already proven T8 siege-escalation offender. Once the
  remaining mechanism is established, implement the authorized common ownership
  and preemption fix. Do not resume congestion, salvage or Port tuning first.

- Moving normally: PASS.
- Stalled near origin: PASS.
- Ownership safety: PASS.
- Clearance success: PASS.
- Clearance failure: PASS.
- Landing screen/escort clearance and refresh gate: PASS.
- Relic-ferry exact-passenger load recognition: PASS (focused deterministic
  test, including the required DE garrison-inclusive filter and removal of the
  indirect hull-count CHECK-LOAD condition).
- Migration landing candidate screening: PASS (focused deterministic test;
  the initial and all four alternate candidates pass through exact-hull zone
  and path screening, while wrong-zone/path-rejected branches issue no unload).
- P3B44T6 boarding diagnostics: PASS (one bounded pre-retry sample and one
  terminal sample where applicable for both assault and migration; command,
  target, movement, zone, idling, and group fields are all required).
- P3B44T6 safe partial assault: PASS (five-to-nine versus below-five terminal
  split, shore-straggler stop, garrison-inclusive exact manifest rebuild,
  actual-count update, home-defense interrupt, target revalidation, and prior
  abort recovery are covered).
- Full P3B44-derived regression suite: PASS (155 tests, including R3 bounded
  delayed identity, R2 reservation
  classification, T10R1 string
  budget/constant reuse and compiled T10
  equivalence/structure, writer-map identity, deferred delivery and passengers).
- PER structural/operand validation: PASS.
- Naval-doctrine validation: PASS.
- Strategy execution: PASS (1,156 total matchups; 1,149 historical and 1,152
  Extreme matchups with adjustments).
- ODS workbook round trip: PASS (34 civilizations, 680 unit-evidence rows, 340
  naval-class rows).
- Replay benchmarks: PASS (31 entries).
- `git diff --check`: PASS; only expected CRLF notices.
- Adversarial P3B44T2 comparison: PASS. P3B44T3 changed only the active
  transport departure state, goals/constants, marker, bounded telemetry,
  deterministic tests, and replay evidence. It does not alter the T2
  screen/escort landing rules or any ordinary attack owner.
  `up-target-objects`, `up-retreat-now`, `up-reset-attack-now`, `attack-now`,
  and `up-find-player` counts are identical to P3B44T2.
- Every new departure state has a producer and consumer. Exact blocker movement
  is verified after eight seconds; one safe retry and three blocker selections
  are hard bounds. The adversarial review found and fixed delayed-retry
  ownership safety: loaded, attacked, grouped, or quarantined blockers are
  skipped rather than retasked.
- P3B44T3 runtime/replay acceptance: PASS. Exact blocker 37204 cleared the
  twelve-tile radius; loaded hull 31205 resumed, landed, and preserved the T2
  screen/escort behavior. Friendly departure congestion is CLOSED.
- Adversarial P3B44T4 review: PASS. The patch touches only the relic-ferry
  boarding-readiness transition, marker, one isolated goal, tests, changelog,
  and replay evidence. DE's documented default excludes garrisoned DUC search
  results, so `fe-filter-garrisoned c: 1` is set after each full search reset.
  The exact passenger controls readiness; the exact reserved hull still owns
  the unchanged unload action. Pending/missing telemetry is one-shot per
  attempt and the prior watchdog remains the hard terminal bound.
- P3B44T4 runtime/replay acceptance: PASS. Orange and Cyan completed two
  independent exact relic-ferry round trips, Red and Green independently
  advanced through exact departure before the watchdog, and all five T2 assault
  landing windows remained free of guard refreshes. Relic-ferry load recognition
  is CLOSED.
- Adversarial P3B44T5 review: PASS. Every landing candidate is rebuilt against
  the exact reserved hull; zone equality/inequality, reachable/unreachable, and
  missing-hull outcomes are exhaustive. Rejected candidates yield on a bounded
  one-second timer and retain the existing five-attempt/home-return terminal.
  The patch does not change relic-ferry, departure-clearance, assault landing,
  escort ownership, drop-site construction, or ordinary attack rules.
- Adversarial P3B44T6 review: PASS. The replay-visible manual load is preserved
  as corroboration rather than misclassified as an AI group. Early and terminal
  candidate samples are transition-bounded, so they cannot create a per-sweep
  telemetry loop. The initially proposed passenger-to-hull `up-path-distance`
  diagnostic was removed before deployment because a land unit cannot path to
  a Transport's water tile; actual action, target, command, move, distance,
  zone, group, and idling fields are recorded instead. Partial departure stops
  ashore members and rebuilds the direct-control group from garrisoned members
  before entering the unchanged target and route checks. Home defense can
  interrupt every new diagnostic/manifest state.
- `validate_good_units.py` has a pre-existing P3B44 provenance-hash failure;
  frozen unit-strategy material is outside this transport patch.
- Installed P3B44T6 runtime byte verification: PASS (68 files; aggregate
  source/target SHA-256
  `D5A2314E461603F68D5327E71BD7FB3737F0518C8969F2D5A4C45809B11598EB`; no
  missing, different, or unexpected runtime files).
- Fresh P3B44T5 engine/replay acceptance: PASS. All 95 path-clear candidates
  issued an unload, all 40 wrong-zone/path-rejected candidates issued none,
  all-invalid missions remained bounded, and Red completed a same-zone landing,
  Mining Camp, and settler retask. Migration blind landing offsets are CLOSED.
- P3B44T2/T4 runtime non-regression in P3B44T5: PASS. Eleven resolved assault
  landing windows had zero active-hull guard commands, and exact relic
  passengers continued outbound/return lifecycles. No public exact-blocker
  congestion episode independently re-exercised P3B44T3; its earlier runtime
  acceptance remains the control evidence.
- Fresh P3B44T6 engine/replay acceptance: PASS for safe partial departure.
  Five completed partial landings pass exact-manifest-minus-stopped comparison;
  low-strength aborts are preserved. Other boarding failures remain open.
- P3B44T7 focused selector/flag fixture and regression suite: PASS (119 tests).
  PER, naval, strategy, workbook and 28 replay-benchmark validators: PASS.
- P3B44T7 read-only adversarial review: ACCEPTED the demonstrated group-0
  overwrite/clear and its preselection exclusion. The earlier review rejected
  a universal command-theft explanation from the available military snapshots.
  T7 now proves specific command interference despite group 4; retained flags
  do not establish exclusive control. DEFERRED stale-clock boarding timing,
  scout exploration overrides and close military stalls to separate causal
  patches. No military, hunt, homebase or economy PER file changed from T6.
- P3B44T7 deployed byte identity: PASS, 68 source/target files matching
  `69C30C50661D3E1E8A1F8DC081C63E80D0C899D8E695B16D3E02F95B910B7738`.
  Only general cleanup and the marker differ from the tested T6 runtime.
  T7 runtime PASS for the narrow cleanup flag exclusion (39 mining snapshots).
- T7 all-player partial/relic/landing-screen non-regression: PASS for the
  reconstructable outcomes recorded above. No claim that every voyage worked.
- T8 diagnostic tests: PASS; all six caller tags precede recall/reset actions,
  and removing only logs reproduces T7 military/taunt executable fingerprints.
  The fingerprints deliberately freeze this diagnostic experiment; future
  authorized behavior patches must replace that acceptance fixture explicitly.
- T8 full validation: 122 tests, PER structure/operand domains, 34-civilization
  naval doctrine, strategy execution, ODS workbook and 29 benchmarks PASS.
  `validate_good_units.py` still reports the pre-existing
  `source_provenance/unique-unit-production.json_sha256` mismatch. Do not
  repair frozen strategy provenance as an unrelated transport change.
- T8 read-only adversarial review: ACCEPTED exact retreat-member inspection,
  separation of the Orange STOP loop, and correction of the landing audit's
  coordinate assumption. REJECTED treating reservation flags as exclusive
  ownership or a retreat-only explanation as universal. DEFERRED exact caller
  attribution and native/local STOP cause pending discriminating runtime logs.
- T8 deployment PASS: all 68 files match the installed identity above. Runtime
  caller attribution and gameplay fix acceptance remain PENDING/INVESTIGATING.
  No GitHub push or PR update was made in this session; only local commits.
- Architectural audit validation: PASS, 134 unit tests / 29 replay benchmarks /
  PER structure and operand domains / `git diff --check`. The T7 audit rerun
  covers every known load and retreat with zero decoder failures. Read-only
  adversarial findings are triaged in `TASK-OWNERSHIP.md`; accepted fixes were
  made to the audit, not the runtime. Strategy/workbook validators were not
  rerun for this audit-only change; their prior results and provenance failure
  above remain historical, not new session claims.
- Architectural gameplay acceptance: NOT RUN / NOT IMPLEMENTED. The twelve
  audit tests do not exercise the engine or implement section-H contracts.
  Installed T8 identity rechecked PASS: all 68 runtime files byte-identical,
  no files copied and no marker changes. The canonical checkout and immutable
  attack baseline were not edited; user-owned `AGENTS.md` remains untouched.

## Exact next actions

**R2 arrival gate satisfied:** the release recovery at the top is implemented,
separately committed, fully statically validated and deployed as R4:455.
Resume R2/ownership analysis now; do not repeat recovery or use R2 as validation
of changes that postdate it. Older R3 references in historical sections are
not the current installed identity.

1. Verify this worktree, branch, T8 diagnostic commit `d10f33e`, audit successor,
   installed marker/hash, and current working-tree status. The intentional
   `AGENTS.md` amendment is now committed, not expected working-tree residue.
   T8 was installed from this exact experimental worktree, not the canonical
   or obsolete checkout. CURRENT installation is generated T10R4:455; use
   `--writer-trace` to check it against the source/map. Plain sources remain
   T9-marked input plus hunt 16, not a separately deployable equivalent of R4.
   Recovery commits and release are recorded at the top; no push or PR update.
   No new development directory exists.
2. R2 is now audited across all players (latest section above). Verify R4's
   delayed identity and recovered caps in the next test. R2 proves early idle
   spam is absent but has missing identity and late quota exhaustion.
   Preserve both external R1/R2 maps. Do not use R2 as validation of R4.
   Follow the shared architectural directive in `TASK-OWNERSHIP.md`, not the
   obsolete restriction to one recall micro-fix. Analyze T10's command/group/
   native-policy trace before assigning WORK packets to a native mechanism.
   Distinguish direct script
   selection, persistent native builder/economy delegation and autonomous
   native tasking with a controlled engine comparison. Preserve search state;
   record exact commanded members where available and expose any trace quota
   exhaustion. Untagged packets without complete coverage prove no caller.
   T8 has now identified all 100 recorded recall packets and proved Red's
   source-3 boarding overwrite, but cannot by itself settle every worker/native
   boundary. Use that established cause in the shared fix; do not repeat caller
   attribution as if it were still wholly unknown. Do not request a long T8 run
   while implying that it contains the missing coverage.
   Once the mechanism is established, implement the common selection/command
   permission contract, explicit emergency ownership transfer, bounded routine
   defense and persistent first-TC allied-help anchors. Add all nine section-H
   contracts and validate every player's preemption/boarding events in a fresh
   preserved-lobby replay. Keep ownership INVESTIGATING until then.
3. Preserve T6 safe partial assault as CLOSED and T5 candidate screening as
   CLOSED; preserve T7's specific cleanup exclusion as runtime-validated.
   Reject any regression to ordinary P3B44 attacks or successful full/partial/
   relic lift behavior. Broader boarding/STOP/passivity causes stay INVESTIGATING.
4. Resume the authorized selective salvage A-C above after ownership recovery,
   preserving recovery attack/transport behavior and stopping
   conflicting items. D is already committed as `9b3dded`; do not backport it
   twice. T9 uses private diagnostic goals 1163-1165; recheck 1166 onward for A-C. This runtime
   work is pending, not canceled or explicitly deferred by the user.
5. Separately investigate and implement `sn-dock-placement-mode`,
   `sn-minimum-water-body-size-for-dock`, and `sn-dock-proximity-factor` for
   opposite island shores and open ship approaches. Verify their semantics and
   placement outcomes; do not assume parameter values guarantee geometry.
6. Retain the already ROOT-CAUSE-PROVEN premature global-pending drop-site
   transition for its own later patch, outside salvage and Port tuning. Keep
   resource-wait, stale-time boarding, exploration overrides, military stalls,
   escort overlap and recovery-unload repetition distinct.
7. Yellow's T6 22-24-minute interrupted hunt still needs a causal audit. The
   new WORK decoder may now assist, but was verified on T7 packets; confirm T6
   layout and associate hunt targets/state before using it as hunt evidence.
   No guessed hunting fix is included.
8. Keep broader command-volume/crash and transport micro-fixes outside the
   current directive. Friendly-fire rejection is in scope specifically for
   verified-threat preemption; preserve the separate P3B44D1 evidence/control
   without folding in unrelated targeting or navigation changes.
