# Rome at War AI handoff

## Canonical workspace and Git state

- Canonical working directory: `G:\Projects\Codex\Rome at War AI\.pr-work\Rome-at-War-AI`
- Git repository root: `G:\Projects\Codex\Rome at War AI\.pr-work\Rome-at-War-AI`
- Active branch: `codex/replay-economy-build-order`
- P3B47 code commit: `90287ea` (`Fix tribute donor compiler error`)
- Pull request: <https://github.com/MnHebi/Rome-at-War-AI/pull/4>
- Installed runtime marker: `RAWAI-P3B47:47`
- Installed 68-file runtime SHA-256: `FD61DF40B9434412DD6C3305179653EC46E25230077F972F7DF547CF6D49D066`

The legacy directory
`G:\Projects\Codex\Rome at War AI\Rome-at-War-AI-main` is a noncanonical
extracted source snapshot and has no `.git` metadata. Do not edit it or treat
DeepSeek changes made there as current project state. Future agents must use the
canonical Git worktree above. The canonical directory has not been moved or
replaced in this session.

## Current milestone

Obtain a fresh P3B47 Britannia 4v4 replay using the preserved original lobby and
validate the long-range capital-ship controller, empty-route-first assault
transport lifecycle, defeated-target expedition recycling, serialized Market
portfolio, and team-elected stalemate Wonder. Continue validating the P3B45
100/500/1000 need-gated allied-resource request tiers and the older unresolved
runtime defects listed below.

## Unresolved defects and runtime validation

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
  small-island gold/stone untouched with idle villagers. Sustained passenger
  work and correct drop-site completion remain unresolved.
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
- `replay-benchmarks.json` now contains 21 validated entries, including
  `britain-4v4-20260828-141213`. The Cyan evidence is preserved exactly: the
  user saw a defeated notice while buildings remained; no Player 6 RESIGN action
  was decoded, so this is recorded as an engine defeat transition.
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
  `G:\Projects\Codex\Rome at War AI\.analysis\replay-20260828-141213-compact.json`
- Previous compact replay report:
  `G:\Projects\Codex\Rome at War AI\.analysis\replay-20260828-005137-compact.json`
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

- Full P3B47 regression suite: 115 tests passed.
- Replay-benchmark validator: 21 benchmarks passed.
- PER structural/operand validation passed.
- Strategy execution validation passed: 1,156 total matchups, with 1,149
  historical and 1,152 Extreme matchups containing adjustments.
- Civilization strategy synchronization check reported zero updates.
- Good-unit JSON validation passed for 34 civilizations x 20 categories.
- ODS round-trip validation passed for 680 unit-evidence and 340 naval-class
  rows.
- Naval doctrine and generated naval-score synchronization checks passed.
- `git diff --check` passed; only expected Git CRLF conversion notices appeared.
- P3B47 adversarial read-only review confirmed `rawai-init-goals.per` loads
  before `rawai-trade.per`, the cached self-player goal is initialized once,
  all 120 donor guards use the valid comparison form, and no stock DE AI script
  uses `player-number` as a direct predicate. The wider P3B46 review checked controller ownership, exact object
  reconstruction after waits, bounded progress termination, target invalidation,
  Market serialization, and team-wide Wonder progress. The one actionable
  Wonder finding was corrected before the final full suite.
- Installed test runtime matches all 68 repository runtime files at the SHA-256
  recorded above.
- Latest analyzed replay:
  `SP Replay v101.103.48987.0 @2026.08.28 141213.aoe2record`, SHA-256
  `11EB682BA3C661489EAA12BC99326AFD087465006BB68EDFEB6BE983E2BBE016`.
- The replay lasted 79:34 with 359,005 ACTION operations, 1,006 Market sells,
  24 buys, and one manual Player 1 resignation. It did not crash. The selected
  visible colors match the preserved lobby: Red/Green/Yellow/Purple Romans
  against Orange Picts, Cyan Britons, Blue Germani, and Gray Gauls.

## Next recommended actions

1. Before editing, compare the Git root, branch, HEAD, and working-tree state
   with the canonical workspace above.
2. Run the next Britannia 4v4 with the installed `RAWAI-P3B47:47` runtime and
   preserve Standard victory, recorded game, and the original visible-color
   setup unless deliberately testing a variant.
3. Watch for `naval bombardment staging target`, bounded stall/rejection, and
   actual Juggernaut/Octeres bombardment by distant Roman players.
4. Confirm an attack lift does not announce boarding until `attack route
   preflight complete`, then reaches the screened landing or emits one bounded
   waypoint/landing stall and recovery without repeated load/home-unload churn.
5. If an opponent receives the defeated notice, verify allied survivor units
   receive a new hostile objective or become available to transport recovery.
6. Observe Market purchases by gold-rich players and, if the match remains
   materially static beyond 75 minutes, verify only one allied Wonder attempt.
7. Exercise taunt 69 and the P3B45 100/500/1000 resource-request tiers; visible
   behavior remains required and should not be inferred from acknowledgments.
8. Analyze the replay with `tools/analyze_replay.py` using
   `G:\Projects\Codex\Rome at War AI\.analysis\replay_parser_kjir`, update the
   replay benchmark, rerun the full suite, synchronize the installed test AI,
   and update this handoff before ending the session.
