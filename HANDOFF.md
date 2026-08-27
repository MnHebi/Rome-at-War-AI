# Rome at War AI handoff

## Canonical workspace and Git state

- Canonical working directory: `G:\Projects\Codex\Rome at War AI\.pr-work\Rome-at-War-AI`
- Git repository root: `G:\Projects\Codex\Rome at War AI\.pr-work\Rome-at-War-AI`
- Active branch: `codex/replay-economy-build-order`
- Recorded HEAD: `2674e7a09ecd116a40cb053249873171386e39bd`
- Pull request: <https://github.com/MnHebi/Rome-at-War-AI/pull/4>
- Installed runtime marker: `RAWAI-P3B34:34`
- Installed 68-file runtime SHA-256: `0E69742F798AE2A2E9B0F02A44C5E26A8CCEE6306641C1E0474EAD4C5F5217AE`

The legacy directory
`G:\Projects\Codex\Rome at War AI\Rome-at-War-AI-main` is a noncanonical
extracted source snapshot and has no `.git` metadata. A full Git clone was
created at the canonical path on 2026-08-23 16:27:54 +03:00. The move to that
clone was not reported to the user at the time. The workspace-root, canonical,
and legacy `AGENTS.md` copies now all identify the canonical path above.

At the time this handoff was initialized, the recorded HEAD was synchronized
with `origin/codex/replay-economy-build-order` and the working tree was clean.
Commit `93f78b5` (`RAWAI-P3B33`) then landed the military-stance change set
described below and is pushed to the PR branch; the installed test AI is
re-synchronized to the same runtime SHA-256.

## Current milestone

Obtain a fresh P3B32 Britannia 4v4 replay and complete runtime validation of
the four-form Roman Legionary producers and scaled, identified allied resource
aid. Continue resolving the established pathing, transport, trade-growth,
taunt-command, tactical-idleness, and command-flood defects using replay and
source evidence.

## Unresolved defects

- DeepSeek edited the noncanonical `Rome-at-War-AI-main` snapshot before the
  canonical-workspace discrepancy was discovered. Do not infer that those
  edits belong in the Git repository; audit and reconcile them deliberately if
  the user requests recovery of any of that work.
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
  loaded hulls that fail to depart or land. P3B33 raised the home-recall
  threshold and dampened the flip-flop; P3B34 fixed the relief chatter. The
  28/8 replay still shows one loaded lift repeatedly loading/unloading (possible
  trading-vessel pathing obstruction) and a migration that unloaded settlers but
  produced no resource drop site.
- Red's late army became largely frozen around its Town Center; P3B33 addresses
  the flip-flop half, but the late order loop toward object 34518 remains
  unresolved.
- Taunt chatter is fixed for the help path (42 to 39, two-unit threshold,
  self-response), but a random per-AI response delay is still wanted so three
  allies do not answer the same taunt in the same instant.
- Idle empty Transports still stage at their Port when no other same-basin ship
  is at least 24 tiles away ("port hull staging failed" / "empty transport no
  staging point"), blocking fishing/merchant dropoffs; a safe offset-from-port
  fallback staging point is still needed.
- Wall planning does not reject a route that enters an enemy town perimeter,
  risking the wall-building villagers.
- Priests attached to attack groups stand idle instead of healing or converting.
- Units attack enemy Town Centers without a sufficient force, instead of
  raiding less-defended outlying resources.
- Migration has reached a remote island, but passenger retasking and sustained
  resource work after drop-site completion require fresh confirmation.
- Port collision recovery, Palintonon packed-state recovery, Transport path
  safety, and naval opportunity engagement remain unverified in a fresh match.
- Cross-water allied relief is not implemented, and some tactically idle ships
  may remain owned by another controller.
- The game crash has no proven AI root cause. Existing dumps identify heap
  corruption detection without the earlier corrupting writer.

## Important recent changes

- `2674e7a` (`RAWAI-P3B34`): help-decline replies use taunt 39 instead of the
  unrelated 42, a relief request needs two same-zone threats, and an AI ignores
  its own taunt 48 instead of answering its own call for help.
- `93f78b5` (`RAWAI-P3B33`): a forty-five-second attack-commitment window plus
  a two-unit defense-latch trigger (five land / four naval severe override) stop
  the attack/defend flip-flop; the two naval-timer executors use a distinct
  wake owner so they do not arm the dwell; and the loaded-Transport home-recall
  threshold is raised from one to two threats.
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

- Latest compact replay report (28/8 crash test):
  `G:\Projects\Codex\Rome at War AI\.analysis\replay-20260828-005137-compact.json`
- Prior full replay report:
  `G:\Projects\Codex\Rome at War AI\.analysis\replay-20260827-164510-full.json`
- Prior compact replay report:
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
  `SP Replay v101.103.48987.0 @2026.08.28 005137.aoe2record`
- Latest replay duration: 3672 seconds (61:12); the game crashed before a normal
  end, so no postgame record was decoded. Observations: taunt-42 help replies,
  an AI answering its own help call, simultaneous ally replies, false help
  calls, Transports staging at Ports, an attack lift repeatedly loading and
  unloading, a migration unload with no drop site, idle priests, under-strength
  Town Center attacks, plus confirmed Legionary production, Battering Ram
  coordination, and much-improved Transport usage.

## Next recommended actions

1. Before editing, compare the current Git root, branch, HEAD, and working-tree
   state with the canonical workspace recorded above.
2. In the next fresh match, verify `RAWAI-P3B34` and that help declines use
   taunt 39, relief requests fire only on two-plus threats, and no AI answers
   its own help call.
3. Confirm the P3B33 stance behavior: the army no longer alternates
   attack/home-defense on lone raiders, a real multi-unit raid still latches
   defense, and assault Transports board, depart, and land without being
   recalled by single raiders.
4. Implement a random per-AI taunt-response delay so allies stop answering the
   same taunt in the same instant.
5. Add a safe offset-from-Port fallback staging point so idle Transports no
   longer block fishing/merchant dropoffs when no other ship is 24-plus tiles
   away.
6. Continue taunt-69 visible deletion, behind-cliff Shipyard placement,
   attack-lift load/unload churn, migration drop-site work, idle priests,
   under-strength Town Center attacks, and the late Town Center order loop.
7. Analyze the next replay with `tools/analyze_replay.py`, update
   `replay-benchmarks.json`, rerun the complete validation set, synchronize the
   installed test AI, and update this handoff before ending the session.
