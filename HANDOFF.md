# Rome at War AI handoff

## Canonical workspace and Git state

- Canonical working directory: `G:\Projects\Codex\Rome at War AI\.pr-work\Rome-at-War-AI`
- Git repository root: `G:\Projects\Codex\Rome at War AI\.pr-work\Rome-at-War-AI`
- Active branch: `codex/replay-economy-build-order`
- P3B50 code commit: `558a39e` (`Fix attack escalation and routine defense recalls`)
- P3B49 instrumentation commit: `91ea476` (`Instrument military and transport failures`)
- Pull request: <https://github.com/MnHebi/Rome-at-War-AI/pull/4>
- Installed runtime marker: `RAWAI-P3B50:50`
- Installed 68-file runtime SHA-256: `9673193834809E7ED8E8FB355BBA1E2E566D7BCEF0622CF6EB311AD93B4B42C9`
- Expected worktree state after this handoff: clean.

The legacy directory
`G:\Projects\Codex\Rome at War AI\Rome-at-War-AI-main` is a noncanonical
extracted source snapshot and has no `.git` metadata. Do not edit it or treat
DeepSeek changes made there as current project state. Future agents must use the
canonical Git worktree above. The canonical directory has not been moved or
replaced in this session.

## Current milestone

Obtain a fresh P3B50 Britannia 4v4 replay using the preserved original lobby and
validate the closed attack-escalation invariants: routine land/naval probes use
only bounded idle response groups, severe threats can still recall globally,
mixed siege families satisfy the literal two-engine package, and one fortified
player objective cannot repeatedly retreat on 3/2 scan noise. Then resume the
explicitly deferred migration, transport, port, relic-ferry, and command-flood
work using the existing RAW49 telemetry.

## Unresolved defects and runtime validation

- The 19:06 P3B49 replay accounted for all 45 distinct retreat decisions: 14
  fortification, 25 land-defense, and 6 naval-defense retreats. No direct
  Town-Center defense-leash telemetry fired. P3B50 deterministically restores
  all three land attack-group strategic numbers on every SIEGE/REGROUP exit,
  latches SIEGE by fortified player, and removes the global reset/retreat from
  routine defense. A fresh replay still must confirm the engine-visible behavior
  while severe siege/large-probe recalls remain operational.
- The same replay confirmed the worker-migration idle gate still repeatedly sees
  zero engine-idle Villagers despite available villagers and Transports. No
  worker migration completed; eleven boarding attempts ended with zero cargo,
  five routes became unreachable, and six returns exhausted unload retries.
  This task deliberately did not modify migration or transport behavior.
- P3B49 publishes Transport escort, worker migration, repair, Port clearing,
  assault, recovery, relic-ferry, and quarantine state snapshots plus public
  lifecycle/terminal messages for every AI. Boarding timeouts now report actual
  and requested cargo, and every route-screen failure has a classified RAW49
  message. Transport failure remains unresolved pending the fresh replay.
- The 19:06 replay contained 491,938 AI_ORDER actions. Green generated 345,645,
  with four parser-unidentified object IDs accounting for 343,632. Cyan object
  4560 and Blue object 4561 were also high-volume owners. Object type/controller
  ownership remains unproven, so P3B50 deliberately makes no command-flood
  behavioral change.
- Taunt 69 has repeatedly acknowledged the command without visibly deleting the
  intended flared structure. Flare ownership and bounded cleanup were changed in
  P3B30/P3B31, but visible deletion remains unconfirmed and therefore unresolved.
- Green repeatedly attempted to place a Shipyard on an unreachable beach behind
  cliffs. No reliable builder-path primitive has yet been established, so the
  placement defect remains unresolved.
- P3B46 screens an assault route with an empty hull reservation and Scout Ship,
  then loads only after the scout reaches the corridor and landing water. This
  proves water connectivity, not that a cliff has an adjacent disembark tile.
  Loaded distance/garrison progress and bounded recovery need fresh validation.
- The 16:02 replay showed Purple's civilian migration owning the shared
  Transport path while military lifts remained uncompleted. P3B48 gives a
  current, sufficiently strong cross-water assault the first ready ownership
  window and lets migration use the assault cooldown. Fresh play must prove the
  controllers alternate and that Red/Purple armies no longer accumulate at
  home solely because migration repeatedly wins the owner.
- Purple's two late migration manifests overlapped 27 of the 29 objects in an
  81,789-order own-Town-Center loop. P3B48 excludes every resource-carrying
  Villager from all mining-migration manifests. Fresh replay evidence must show
  that garrisoned passengers no longer generate consecutive-tick deposit spam
  and that total command volume remains bounded.
- The user visually observed a Purple Transport sail through hostile Towers and
  die. P3B48 scans the destination and both lateral corridors against every live
  enemy, widens corridor coverage, checks the exact loaded hull every five
  seconds, and returns/rejects the destination on damage. This reduces but
  cannot eliminate risk from a hidden defense or destruction between samples;
  the escape behavior remains runtime-only validation.
- P3B46 removes the 200/120/48-tile capital-ship eligibility bottlenecks, scans
  every live enemy, advances an exact Juggernaut or Octeres through bounded
  halfway staging, and temporarily rejects stalled targets. Geometric staging
  can still reject a valid route that initially moves away from its waypoint,
  and ships owned by another active group remain unavailable.
- P3B46 resets attack-now when the current target leaves the game or loses a
  valid hostile objective, retasks idle same-zone survivors to the next live
  target, and wakes transport recovery for disconnected survivors. The fresh
  replay must confirm this after an engine defeated notice.
- P3B46 serializes Imperial Market buying to one transaction every fifteen
  seconds, covering critical deficits, Wonder reserves, transport wood, and
  ordinary operating reserves. Actual resource stocks, prices, and sustained
  purchase behavior are replay/runtime-only evidence.
- P3B46 samples material building and civilian losses on both teams. Three
  five-minute no-progress windows after 60:00 enter Wonder saving, stagger the
  allied election, and bound placement retries/cooldowns. Foundation visibility,
  completion, and the Standard-victory countdown need a long fresh match.
- Red previously produced only two Merchant Vessels despite a verified trade
  route. Profitable growth toward 100, or 160 under sustained scarcity, remains
  unverified.
- P3B47 corrects the P3B45 tribute donor compile blocker: FactId
  `player-number` was incorrectly used as a rule predicate in all 120 explicit
  donor handlers, producing `rawai-trade.per` ERR2011 at the first occurrence.
  Every handler now compares the initialized `gl-self-player-number` goal.
  Resource aid still needs fresh runtime confirmation: stock taunts 3..6
  request 100; project taunts 241..244 request 500 and 245..248 request 1000 only after the
  matching cumulative collected-resource bank reaches 500 or 1000. Donor
  reserve enforcement, exact recipient messages, and no stale delayed tribute
  remain runtime checks.
- P3B32 probes all four Roman Legionary concrete forms under one shared family
  cadence. Production occurred in the 00:51 replay, but sustained Roman
  composition remains a calibration item.
- Migration reached a remote island in prior testing, but the 14:38 replay left
  small-island gold/stone untouched with idle villagers. P3B48 prevents workers
  from boarding with carried resources, but sustained passenger work and
  correct drop-site completion remain unresolved.
- Idle empty Transports can still stage at a Port when no safe same-basin offset
  is found, blocking fishing or merchant dropoffs. Port collision recovery,
  Palintonon packed-state recovery, transport path safety, and naval opportunity
  engagement still need fresh evidence.
- Cross-water allied relief is not implemented. Randomized allied taunt-response
  delay, active priest support, safer weak-force target selection, and wall-route
  enemy-perimeter rejection also remain outstanding.
- The game crash has no proven AI root cause. The two existing ProcDump files
  captured one stopped `STATUS_HEAP_CORRUPTION` crash and identify only the
  detection/free stack, not the earlier corrupting writer. Do not propose an AI
  crash fix without first-chance/PageHeap/Application Verifier evidence.

## Important recent changes

- `558a39e` (`RAWAI-P3B50`) restores population-derived attack-group sizes on
  every SIEGE/REGROUP exit; classifies the former `:9968` site as a legitimate
  defeated-target `up-reset-attack-now` rather than a retreat; counts Rams,
  Armored Elephants, Mangonels, and Catapults in one literal two-unit package;
  latches SIEGE by fortified player until objective loss/change or an actual
  siege-supported launch; and separates routine capped idle responder dispatch
  from severe global home-defense recall.
- `91ea476` (`RAWAI-P3B49`) makes all six global-retreat sources and the separate
  Town-Center defense leash replay-visible, periodically reports the first
  passive-army and migration blocker, publishes all transport-controller state
  snapshots and lifecycle failures for every AI, records actual boarding cargo,
  and preserves DE_RETREAT actions in compact replay analysis.
- `7d46090` (`RAWAI-P3B48`) excludes resource carriers from migration,
  alternates the shared Transport window in favor of a ready military lift,
  scans migration landings and both corridors against all live enemies, aborts
  the exact loaded hull on damage with five-second samples, and rejects target
  player zero before defeated-expedition recycling.
- `90287ea` (`RAWAI-P3B47`) replaces all 120 invalid direct `player-number`
  predicates with `up-compare-goal gl-self-player-number`, adds a validator for
  this compiler-error class, and updates the tiered-aid regression expectations.
- `0e1169f` (`RAWAI-P3B46`) implements the five fixes authorized from the 14:12
  replay: long-range naval-siege staging, empty-route-first assault transports,
  defeated-target survivor recycling, a serialized Imperial Market portfolio,
  and a protected team-elected stalemate Wonder.
- The adversarial review found that the first Wonder implementation measured
  only enemy losses and could misclassify a steadily losing defense as a
  stalemate. The final implementation samples self plus allies as well as every
  enemy and resets on material losses by either team.
- `replay-benchmarks.json` now contains 23 validated entries, including
  `britain-4v4-20260828-170956`. It records the exact preserved visible-color
  setup, zero-idle-worker migration gate, failed/partial Red migration and
  assault lifts, late Red retreat actions, and the limits of pre-P3B49 replay
  inference for visually passive military units.
- `81ce73d` (`RAWAI-P3B45`) replaced the test-specific 600-resource request with
  100/500/1000 per-donor tiers backed by cumulative collected-resource banks,
  explicit recipient handlers, donor reserves, and immediate consumption of
  unaffordable requests.
- P3B35..P3B40 bounded the major villager, explorer, DUC-ship, and self-target
  command-flood owners. The latest replay was far below the earlier 410,021
  ACTION operations in 61 minutes but still needs per-controller fresh analysis.
- Replay metadata joins players by validated player number and uses the DE
  header's selected visible color. Internal color IDs remain nonvisual
  diagnostics only.

## Generated diagnostic artifacts

- Latest compact replay report:
  `G:\Projects\Codex\Rome at War AI\.analysis\replay-20260828-170956-compact.json`
- Previous compact replay report:
  `G:\Projects\Codex\Rome at War AI\.analysis\replay-20260828-160237-compact.json`
- Prior 27 August full and compact reports remain under
  `G:\Projects\Codex\Rome at War AI\.analysis`.
- Replay benchmark knowledge: `replay-benchmarks.json`
- Unique production audit: `unique-unit-production.json`
- Generated unit evaluation: `good-unit-evaluations.json`
- Generated naval scores: `naval-capability-scores.json`
- Generated naval doctrine: `rawai-naval-doctrine.per`
- External crash dumps:
  `C:\AoE2CrashDumps\AoE2DE_s.exe_260827_131920.dmp` and
  `C:\AoE2CrashDumps\AoE2DE_s.exe_260827_132003.dmp`

## Tests and replays already performed

- Full P3B50 regression suite: 126 tests passed.
- Replay-benchmark validator: 23 benchmarks passed.
- PER structural/operand validation passed.
- Strategy execution validation passed: 1,156 total matchups, with 1,149
  historical and 1,152 Extreme matchups containing adjustments.
- Civilization strategy synchronization check reported zero updates.
- Good-unit JSON validation passed for 34 civilizations x 20 categories.
- ODS round-trip validation passed for 680 unit-evidence and 340 naval-class
  rows.
- Naval doctrine and generated naval-score synchronization checks passed.
- `git diff --check` passed; only expected Git CRLF conversion notices appeared.
- P3B50 adversarial read-only review checked every attack-group-size write and
  escalation-state transition, verified all five non-initial NORMAL exits
  restore the three strategic numbers, proved `gl-one-percent` no longer owns
  siege readiness, and confirmed 3/2 scan oscillation cannot rearm the same
  fortified-player latch. It found and corrected a routine-response ownership
  gap by requiring candidates to be idle, ungrouped, and neither attacking nor
  retreating before the fixed eight-land/six-naval cap. Severe land siege/five
  regular and four-ship naval rules retain the only home-defense global recalls.
- P3B49's prior adversarial review enumerated all six repository-wide
  `up-retreat-now` sources, verified each reason record precedes the command,
  distinguished the separate direct-move home-defense leash, and added the
  initially omitted Transport escort owner and land-attack eligibility report.
  It checked that public transport messages have no matching private remnants,
  controller snapshots are transition-bounded, blocker reports use thirty- or
  sixty-second cadence, and telemetry does not change transport ownership or
  issue military commands. P3B48's prior review correlated Purple's two
  migration manifests with 27 of 29 objects in the Town Center command loop,
  distinguished that economy flood from the user's military-idleness
  observation, and confirmed that the migration owner rule preceded assault
  ownership. It also checked the
  all-enemy ordered-cycle termination, exact-hull reconstruction after waits,
  bounded route/landing recovery, and preservation of Red's legitimate
  home-defense recall. P3B47's prior review confirmed `rawai-init-goals.per` loads
  before `rawai-trade.per`, the cached self-player goal is initialized once,
  all 120 donor guards use the valid comparison form, and no stock DE AI script
  uses `player-number` as a direct predicate. The wider P3B46 review checked controller ownership, exact object
  reconstruction after waits, bounded progress termination, target invalidation,
  Market serialization, and team-wide Wonder progress. The one actionable
  Wonder finding was corrected before the final full suite.
- Installed P3B50 test runtime matches all 68 repository runtime files at the
  SHA-256 recorded above.
- Workspace-root mirrors of `rawai-customconstants.per`, `rawai-init-goals.per`,
  and `rawai-military.per` were mechanically synchronized from the canonical
  repository and verified byte-identical by SHA-256. They do not replace the
  canonical Git workspace.
- Latest analyzed replay:
  `SP Replay v101.103.48987.0 @2026.08.28 190624.aoe2record`, SHA-256
  `3A068DD0D426B7D1A3CFD2A41CCA71FBA8FC4AF20F36F48F7942B22E31980A96`.
- The replay lasted 63:54. All 45 distinct retreats matched a public P3B49
  reason; the direct home leash never fired. It also contained 491,938 AI_ORDER,
  201,285 ORDER, and 132,260 WORK actions. Worker migration did not complete,
  Blue alone completed two ten-unit assault landings, and repeated unchanged
  transport/Port failures remained visible. The selected visible colors exactly
  match the preserved original lobby.

## Next recommended actions

1. Before editing, compare the Git root, branch, HEAD, and working-tree state
   with the canonical workspace above.
2. Run the next Britannia 4v4 with the installed `RAWAI-P3B50:50` runtime and
   preserve Standard victory, recorded game, and the original visible-color
   setup unless deliberately testing a variant.
3. For P3B50 acceptance, preserve routine land/naval defense telemetry and
   verify no matching DE_RETREAT occurs; provoke or observe a home siege/five-unit
   land or four-ship naval emergency and verify severe recall still works. Also
   preserve `siege usable engines`, `siege objective player`, and fortification
   messages to confirm mixed-family readiness and one entry per objective.
4. Preserve the complete `RAW49 TRN`/`RAW49 FAIL` sequence for every failed
   transport. It should reveal controller owner, exact state, selected hull,
   boarding actual/target cargo, route-screen result, progress, and the terminal
   recall, retry, recovery, quarantine, or loss reason.
5. For worker migration, correlate `RAW49 MIG` first blockers with the public
   migration-gate counters. In particular, confirm whether apparently idle
   workers still produce an engine-idle count below two and whether resource
   pressure or depletion ever overrides that gate.
6. Confirm no migration passenger produces repeated own-Town-Center deposit
   orders while garrisoned, and that one ready assault lift claims the shared
   Transport before civilian migration; migration should remain possible during
   the assault route cooldown.
7. Watch a migration route near defenses belonging to any opponent. It should
   reject the landing/corridor before departure or emit `migration route under
   fire` / `migration landing under fire` and turn home on the bounded sample.
8. Watch for `naval bombardment staging target`, bounded stall/rejection, and
   actual Juggernaut/Octeres bombardment by distant Roman players.
9. Confirm an attack lift does not announce boarding until `attack route
   preflight complete`, then reaches the screened landing or emits one bounded
   waypoint/landing stall and recovery without repeated load/home-unload churn.
10. If an opponent receives the defeated notice, verify allied survivor units
   receive a new hostile objective or become available to transport recovery.
11. Observe Market purchases by gold-rich players and, if the match remains
   materially static beyond 75 minutes, verify only one allied Wonder attempt.
12. Exercise taunt 69 and the P3B45 100/500/1000 resource-request tiers; visible
   behavior remains required and should not be inferred from acknowledgments.
13. Analyze the replay with `tools/analyze_replay.py` using
   `G:\Projects\Codex\Rome at War AI\.analysis\replay_parser_kjir`, update the
   replay benchmark, rerun the full suite, synchronize the installed test AI,
   and update this handoff before ending the session.
