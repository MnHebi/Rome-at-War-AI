# T14 replay audit and overseas target-rotation proposal

## Identity and scope — 2026-08-31

- Replay: `SP Replay v101.103.48987.0 @2026.08.31 115504.aoe2record`.
  SHA256 `E1D8B629F1743E086AE5D9729CAB2E0B7C6D9E440ADD7E115F342E53BFE43977`.
  Ends105:36 with replay player1 resignation; no crash attribution.
- Marker `RAWAI-P3B44T14:459` recorded for players2–8. Recorder self-marker
  asymmetry persists. Read-only deployment verification: all81 source/installed
  runtime files match `DE6010CD8942E7D790A161FDE1A02CFC3F3C1F085E735731B16748F2A782B8A8`.
- Editing directory/Git root remains
  `G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-transport-only`, branch
  `recovery/p3b44-transport-only`, HEAD `387eccab36a3311ca90d9e39bea6d73013584a8b`
  plus the existing intentional pending T14 work. No runtime edits or deployment
  during this audit; no commit, push, new worktree or branch switch.
- Validated selected colors, not row/internal color order: players1–4 are
  Red/Green/Yellow/Purple Romans (user team1); players5–8 are Orange Picts,
  Cyan Britons, Blue Germani, Gray Gauls (team2). Decoded resolved teams2/3.
  Extreme, population400, speed2.0, shared exploration, treaty0.
- Full parser errors0; exact command decoder failures0;1,640,101 retained
  events. All-player boarding/transport sweep, not just the reported players.
  Private chat principally covers Red. Missing private telemetry is not inactivity.
- User requests an explanation/proposal and then specifically target-rotation
  inspection. No gameplay implementation is authorized by this analysis request.
  STOP-spam implementation retains priority after the proposal; the prior
  controlled/reversible-experiment authorization remains in HANDOFF.

## What the transport evidence establishes

121 boarding windows:60 assault,38 migration,23 unresolved/recovery/relic.
The table concerns reconstructable assault boarding windows, not every possible
native/manual-loaded hull or every maritime voyage.

| Color | Assault windows | Accepted loads | Recall | Boarding abort | Landing timeout | Completion log | Unresolved |
|---|---:|---:|---:|---:|---:|---:|---:|
| Red |0|0|0|0|0|0|0|
| Green |0|0|0|0|0|0|0|
| Yellow |0|0|0|0|0|0|0|
| Purple |19|19|19|0|0|0|0|
| Orange |13|13|6|0|1|4|2|
| Cyan |18|18|18|0|0|0|0|
| Blue |6|5|5|1|0|0|0|
| Gray |4|4|4|0|0|0|0|

Accepted means the existing normal/partial boarding acceptance fired, not useful
arrival or combat. Completion is the controller's empty-hull landing terminal;
it is not independent proof of surviving troops on the correct island. Orange's
four such logs occur49:15,67:12,70:20,76:12. Two Orange windows lack a joined
terminal. Zero assault windows for a player does not mean zero migration/relic work.

- **Purple:**15 recalls reason1 (both candidate approaches rejected), three
  reason8 (landing scout under attack), one reason11 (defended landing detected).
  `rawai-military.per` TARGET/THREAT/LEFT/RIGHT/APPLY checks just the original
  anchor and two lateral candidates,28 tiles either side. Reason1 combines
  actual defense with wrong/unknown land-zone rejection. It does NOT prove that
  every coast of the enemy island was unsafe or inaccessible.
- **Cyan:**17 reason3 recalls and one reason1. All17 reason3 cases also print
  `RAW44T screening bypass denied: 4`; none commit unscreened. Hull31854 repeats
  these at56:29,58:32,63:49,65:43,67:54. Hull41140 continues through104:34.
  At56:25 the accepted normal manifest is10; denial follows56:29. The logged
  `assault ready target: 10` is passenger count, NOT an enemy player ID.
- **Across all players:**25 fallback denials, all code4: Cyan17, Orange3
  (beach-timeout reason9), Gray5 (no-scout reason3). No bypass-commit events.
  One Gray denial lies outside the four joined assault boarding windows; retain
  it rather than treating the boarding census as exhaustive of loaded hulls.
- Code4 in `rawai-assault-screen-fallback.per` covers TWO source paths: no valid
  enemy returned at scan start, OR final saved objective no longer active/hostile/
  known to own a building. Current logs do not disambiguate these or report the
  saved enemy ID. Do NOT reinterpret code4 as known route danger, incomplete
  cargo, or proof that the enemy actually died. All25 failing the same validation
  deserves direct investigation; the optional-screening gameplay acceptance FAILS
  in this replay. This is separate from missing failure-driven rotation.

The user-visible lack of overseas participation is corroborated. The narrower
explanation "they never try to load" is contradicted by repeated accepted loads;
the failure occurs after loading in these episodes. This does not reject what
the user saw, nor establish the cause of all earlier loading failures.

## Source-first target-rotation audit

**Status: ROOT-CAUSE-PROVEN for absent failure-feedback policy; NOT proven to be
the sole cause of all T14 recalls. Proposal only, not implemented.**

1. `rawai-military.per:11072–11128`: while military superiority is at least
   TOLERABLE, choose `up-find-player enemy find-closest` and write
   `sn-target-player-number`. A valid preferred target can override this.
   Phase initialization sets preferred-target-player to-1. None of these rules
   reads assault failures, failed landing candidates, elapsed nonparticipation,
   or whether this opponent has yielded a viable overseas objective.
2. `rawai-military.per:11131–11283`: viability fallback only replaces an inactive,
   allied or zero-known-building target, using the first matching live hostile
   player. It does not compare surviving enemies' landing feasibility.
3. `rawai-military.per:11285–11356`: classify the currently chosen enemy using a
   known building's zone. Classification answers whether transportation is
   needed; it does not choose a more feasible enemy.
4. FIND/TARGET near5490 seal the mission player and choose an enemy anchor near
   that player's focus position. Landing rejection near6078 unloads/recovers.
   Recovery near7311 releases the groups and retries after90 seconds; it does
   not penalize that opponent or retain the failed candidate as strategic memory.
5. A one-time write of a new target would not suffice: the closest-enemy writer
   can select the old enemy again on the next sweep. Screen checks near6433 and
   6564 also read the mutable global target, not the saved mission player. A
   rotation change must not switch the opponent underneath an active voyage.
6. All runtime PER target/preferred-target writers were searched, including
   explicit player attack taunts. Global attack-loss escalation is not a
   per-opponent overseas viability/rotation mechanism.

The API describes find-closest as nearest-player selection, not a route planner:
[UserPatch AI reference](https://userpatch.aiscripters.net/reference.html)
and the cached AIRef `airef-reference-20260830.js` command definitions. Its
documented player iteration wraps; a guessed non-wrapping scan is not established
as the fallback denial cause. No unsupported API semantic was used as a fix.

The user's historical hypothesis is plausible: removing/crippling the preferred
closest target enough to invalidate it can expose a different feasible opponent.
However, this replay's public logs do not expose every assault's enemy ID, so we
cannot claim Purple/Cyan targeted one specific opponent for all19/18 attempts or
that target rotation alone would have made those missions succeed.

## Proposed bounded policy, independently implementable

The thresholds below are initial policy proposals, not measured optimal values.

- Keep a small per-enemy record: distinct completed planning failures, last
  meaningful progress, failure class, rejected landing/zone and retry-after time.
  Count terminal attempts once, not every rule sweep, STOP or movement retry.
- With a ready idle assault force, re-evaluate other live enemies after e.g.
  **three distinct objective/landing failures OR180 game-seconds without a viable
  plan**. Do not count intentional home defense, an active progressing voyage,
  absent transports/Shipyards, or a broken generic validator as enemy-specific
  infeasibility. Repair those local/systemic blockers separately.
- Evaluate a bounded set of same-island landing candidates for each alternative
  known living hostile objective. Prefer an admissible approach before shorter
  distance. Temporarily deprioritize the repeatedly failed opponent, e.g.300s;
  retry sooner if defenses/ownership materially change. Avoid permanent blacklists.
- Keep overseas target choice persistent against the ordinary closest-enemy
  refresh. Plan before boarding where possible. Do not steal reserved passengers
  or retarget a progressing voyage; bind each mission's player, objective, landing
  zone and safety checks to one consistent plan. Reuse an accepted load only after
  explicit replanning/revalidation, never by changing its target SN underneath it.
- If all enemies fail, try another valid coast/objective or bounded siege/support
  preparation and retry on a bounded schedule. Do not declare a living enemy
  "viable" solely because buildings remain, or interpret failed scouting as
  permission to ignore actual defensive fire/known defended approaches.
- Preserve approved5–9 partial loads, same-target-island checks, actual-danger
  vetoes, one-way unscreened commitment and progress/travel deadlines. Diagnose
  and resolve fallback code4 before treating optional screening as operational.

Acceptance: with enemyA alive but repeatedly infeasible and enemyB feasible,
the planner evaluates/chooses B within the budget while A remains alive; the
closest-enemy rule cannot immediately undo it. A progressing A mission remains
stable; failures increment once; all-infeasible search terminates and later
retries; full and accepted partial loads can commit when checks genuinely pass;
known danger and disconnected islands remain rejected. Fresh engine/replay proof
is required, including useful landings, not just new target logs.

## Additional defects and next implementation priority

- **Allied help — OPEN/INVESTIGATING.** User sees real enemies in towns without
  defenders or help calls; this replay contains zero settlement-reinforcement
  call messages. The verifier runs before military/diplomacy, so an asserted
  reversed load order is not the explanation. It requires an exact enemy attack
  action/target-owner match, then a live exact victim asset within48 tiles. Its
  self result is a same-pass pulse. The request additionally needs cooldown ready
  and low military superiority OR cached local responders<=0. Candidate discovery,
  exact target resolution and stale response counts remain distinct possible
  blockers. No exact failed gate established for the observed incidents. Do not
  call cooldown changes a fix; retain friendly-fire identity protection.
- **Cyan Shipyard — OPEN/INVESTIGATING.** Zero BUILD1251 requests in the entire
  replay, versus at least two for every other player. Cyan does request four
  Ports and nine Transports (counts are requests, not surviving structures/ships).
  `rawai-specialplacement.per` gates resources/prerequisites, then samples within
  about14 tiles of the newest Port/Shipyard and requires a7-tile naval-building
  clearance. No progressively wider coastal/alternate-anchor search is present.
  BUILD also waits for worker hold to clear. This source policy is vulnerable to
  constrained coastlines; source/replay do not distinguish candidate geometry,
  affordability, worker hold and other admission failures for Cyan. No foundation
  request exists to blame on a later builder ignoring it. Missing Shipyards can
  reduce screen supply, but cannot explain away the fallback's code4 failure.
- **STOP flood — INVESTIGATING, next implementation priority.**432,975 actual
  STOP706 packets: Red24,647; Green629; Yellow355; Purple2,179; Orange36,371;
  Cyan8,881; Blue7,993; Gray351,920. Gray IDs31795/31892/32192 individually receive
  108,046/104,142/101,106 identical STOPs; unit types/writers not established by
  these counts. Cyan group[4649,31914,31984] gets8,395 between69:28–73:57.
  Preserve this baseline and exact T14 runtime for controlled causal experiments.
  Raw match totals are not exposure-matched rate comparisons or proof of lag cause.
- **Other T14 fixes:** user reports new Trihemiolia production (positive observed
  evidence). No Roman PACK packet is recorded; Blue2/Gray25 PACK packets still
  need exact role validation. Do not blanket-close packing, migration drop-sites,
  economy, actual naval composition, or previous defects from this proposal audit.

## Artifacts and validation

Outside Git: `G:\Projects\Codex\Rome at War AI\.analysis\` contains
`replay-20260831-115504-t14-full.json`, `p3b44t14-command-stream.json`,
`p3b44t14-exact.json`, `p3b44t14-transport-audit.json/.txt`,
`p3b44t14-task-ownership.json`, `p3b44t14-summary.json`,
`p3b44t14-findings.json` and `p3b44t14-gates.json`.
Reproducible reducers: `summarize_t13.py p3b44t14` and
`summarize_t14_gates.py`; raw replay remains outside the AI repository.

Parser/identity checks PASS. T14 optional-screening acceptance FAIL (zero commits,
25 objective-validation denials); broad useful assault participation FAIL for
Purple/Cyan. Cause below denial4 still INVESTIGATING. No runtime patch proposed
here has been implemented or gameplay-tested. Only evidence docs/metadata and
offline reduction changed; no full code test suite or adversarial code-change
review was needed for this read-only gameplay audit.
