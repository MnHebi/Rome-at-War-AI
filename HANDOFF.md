# Rome at War AI handoff

## Canonical workspace and Git state

- Canonical working directory: `G:\Projects\Codex\Rome at War AI\.pr-work\Rome-at-War-AI`
- Git repository root: `G:\Projects\Codex\Rome at War AI\.pr-work\Rome-at-War-AI`
- Active branch: `codex/replay-economy-build-order`
- Recorded HEAD: `ef96d9e5ebba21584c0ce039a675b9e5ad39b382`
- Pull request: <https://github.com/MnHebi/Rome-at-War-AI/pull/4>
- Installed runtime marker: `RAWAI-P3B32:32`
- Installed 68-file runtime SHA-256: `BD4FCB3CB8D25C3C247AA3B7CB748B1897AEAF92310C6CEEE30532E61CEC636E`

At the time this handoff was initialized, the recorded HEAD was synchronized
with `origin/codex/replay-economy-build-order` and the working tree was clean.
During this rules-only task, concurrent modifications appeared in
`rawai-customconstants.per`, `rawai-init-goals.per`, `rawai-military.per`, and
`rawai-timers.per`. They were not created, inspected, staged, or altered by this
task. Treat the working tree as dirty and establish their owner and purpose
before beginning unrelated edits.

## Current milestone

Obtain a fresh P3B32 Britannia 4v4 replay and complete runtime validation of
the four-form Roman Legionary producers and scaled, identified allied resource
aid. Continue resolving the established pathing, transport, trade-growth,
taunt-command, tactical-idleness, and command-flood defects using replay and
source evidence.

## Unresolved defects

- Taunt 69 has repeatedly acknowledged the command without visibly deleting
  the intended flared structure. P3B31 changed flare ownership and command-state
  cleanup, but successful visible deletion still needs fresh confirmation.
- Green repeatedly attempted to place a Shipyard on an unreachable beach behind
  cliffs and attempted Transport loading across cliffs.
- Red produced only two Merchant Vessels despite a verified trade route; the
  intended 100/160-unit profitable trade growth remains unverified.
- No Roman Empire player trained a Legionary in the P3B31 replays. P3B32 now
  probes all ranged/melee and base/elite forms, but runtime success remains
  unverified.
- Purple repeatedly requested and bought wood yet remained without it for long
  periods. P3B32 scales team requests to 600 nominal, sends reserve-safe
  200-resource donor tranches, and identifies the recipient player; actual
  delivery and net tribute remain unverified.
- Assault Transport missions still show frequent boarding aborts, unloads, or
  loaded hulls that fail to depart or land.
- Red's late army became largely frozen around its Town Center. The latest
  replay contains a sustained order loop toward object 34518 at point 186,182,
  but the target object type and owning controller remain unresolved.
- Migration has reached a remote island, but passenger retasking and sustained
  resource work after drop-site completion require fresh confirmation.
- Port collision recovery, Palintonon packed-state recovery, Transport path
  safety, and naval opportunity engagement remain unverified in a fresh match.
- Cross-water allied relief is not implemented, and some tactically idle ships
  may remain owned by another controller.
- The game crash has no proven AI root cause. Existing dumps identify heap
  corruption detection without the earlier corrupting writer.

## Important recent changes

- `ef96d9e` (`RAWAI-P3B32`) probes all four concrete Legionary forms for Roman
  Empire and Roman Republic production under one aggregate family bound and a
  shared request deadline.
- P3B32 replaces fixed 100-resource allied aid with a 600-resource team request,
  one 200-resource tranche per eligible donor, protected reserves, and replies
  naming the exact recipient player number.
- Roman diagnostics now distinguish all-four engine availability results from
  all-four concrete trainability blockage for both Roman civilizations.
- `5649977` preserves opaque binary replay-action payloads in analyzer JSON.
- Replay metadata now joins command players through validated player numbers
  and uses the DE header's selected visible colors.
- P3B31 bounded Pict-team Cow requests, retasked migration settlers after a
  completed drop site, reduced attack-lift manifests, revised taunt flare
  ownership and cleanup, released late engine explorer budgets, and bounded
  Castle placement retries.

## Generated diagnostic artifacts

- Latest full replay report:
  `G:\Projects\Codex\Rome at War AI\.analysis\replay-20260827-164510-full.json`
- Latest compact replay report:
  `G:\Projects\Codex\Rome at War AI\.analysis\replay-20260827-164510-compact.json`
- Replay benchmark knowledge: `replay-benchmarks.json`
- Unique production audit: `unique-unit-production.json`
- Generated unit evaluation: `good-unit-evaluations.json`
- Generated naval scores: `naval-capability-scores.json`
- Generated naval doctrine: `rawai-naval-doctrine.per`
- External crash dumps:
  `C:\AoE2CrashDumps\AoE2DE_s.exe_260827_131920.dmp` and
  `C:\AoE2CrashDumps\AoE2DE_s.exe_260827_132003.dmp`

## Tests and replays already performed

- Full P3B32 regression suite: 110 tests passed.
- Replay-benchmark validator: 20 benchmarks passed.
- PER, strategy execution, civilization strategy synchronization, good-unit
  JSON, ODS workbook, naval doctrine, and generated naval-score checks passed.
- Installed test runtime matched all 68 repository runtime files at the SHA-256
  recorded above.
- Latest analyzed replay:
  `SP Replay v101.103.48987.0 @2026.08.27 164510.aoe2record`
- Latest replay SHA-256:
  `F617D137A8450DE33933193726F327F2353DA64341969721C59DCA35B71C9436`
- Latest replay duration: 6413 seconds (106:53).
- Confirmed lobby: Red/Green/Yellow/Purple Roman Empire versus Orange Picts,
  Cyan Britons, Blue Germani, and Gray Gauls on Britannia.

## Next recommended actions

1. Before editing, compare the current Git root, branch, HEAD, and working-tree
   state with the canonical workspace recorded above.
2. Run a fresh match with the installed P3B32 runtime and verify that the replay
   contains `RAWAI-P3B32` near startup.
3. Confirm concrete Legionary MAKE commands or capture the new all-four gate
   diagnostic, and check that no same-sweep production burst occurs.
4. Drive one player below 100 wood, observe the 600-resource team request, count
   the 200-resource donor responses, verify their named recipient, and measure
   actual net tribute received.
5. Re-test taunt 69 against a clearly owned structure at the flare and continue
   through root-cause implementation if visible deletion still fails.
6. Exercise behind-cliff shore placement and Transport loading, verified trade
   growth, attack-lift departure/landing, migration resource work, and the late
   Town Center order-loop scenario.
7. Analyze the replay with `tools/analyze_replay.py`, update
   `replay-benchmarks.json`, rerun the complete validation set, synchronize the
   installed test AI, and update this handoff before ending the session.
