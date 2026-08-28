# Rome at War AI handoff

## Canonical workspace and Git state

- Canonical working directory: `G:\Projects\Codex\Rome at War AI\.pr-work\Rome-at-War-AI`
- Git repository root: `G:\Projects\Codex\Rome at War AI\.pr-work\Rome-at-War-AI`
- Active branch: `codex/replay-economy-build-order`
- P3B45 code commit: `81ce73d` (`Add need-gated allied resource request tiers`)
- Pull request: <https://github.com/MnHebi/Rome-at-War-AI/pull/4>
- Installed runtime marker: `RAWAI-P3B45:45`
- Installed 68-file runtime SHA-256: `51EC00866E32FDD2EB1CD6F33B536E7F1B84CB3465AD40F2ED99B7C7825A373E`

The legacy directory
`G:\Projects\Codex\Rome at War AI\Rome-at-War-AI-main` is a noncanonical
extracted source snapshot and has no `.git` metadata. A full Git clone was
created at the canonical path on 2026-08-23 16:27:54 +03:00. The move to that
clone was not reported to the user at the time. The workspace-root, canonical,
and legacy `AGENTS.md` copies now all identify the canonical path above.

The P3B45 code commit is based on `8ec8700` and the installed test AI is
byte-for-byte synchronized to the 68 runtime files at the SHA-256 above. This
handoff update is the only planned commit after the P3B45 code commit.

## Current milestone

Obtain a fresh P3B45 Britannia 4v4 replay and validate the need-gated
100/500/1000 allied-resource request tiers, including exact donor/recipient
messages and the absence of delayed stale tribute. Continue resolving the
established pathing, transport, trade-growth, taunt-command, tactical-idleness,
and command-flood defects using replay and source evidence.

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
- Allied resource aid still needs fresh-match validation. P3B45 restores the
  stock taunts 3..6 to 100, adds project taunts 241..244 for 500 and 245..248
  for 1000, selects larger tiers only after the matching engine cumulative
  collected-resource bank reaches 500/1000 while live stock is below 100,
  preserves donor reserves, names the exact recipient, and consumes
  unaffordable taunts immediately so they cannot cause stale delayed tribute.
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
- Command flood (28/8 replay, 410,021 ACTION ops / 61 min): the largest source
  (165,882 villager WORK retasks) was addressed in P3B35 and shoreline food/hunt
  contention in P3B39. P3B36/P3B37 narrowed and instrumented the DUC ship owner;
  P3B40 fixed a self-target fallback that sent military to its own Town Center.
  A fresh P3B45 replay is still required to measure the remaining order rates.
- Port collision recovery, Palintonon packed-state recovery, Transport path
  safety, and naval opportunity engagement remain unverified in a fresh match.
- Cross-water allied relief is not implemented, and some tactically idle ships
  may remain owned by another controller.
- The game crash has no proven AI root cause. Existing dumps identify heap
  corruption detection without the earlier corrupting writer.

## Important recent changes

- `81ce73d` (`RAWAI-P3B45`) replaces the test-specific 600 request with
  100/500/1000 per-donor tiers backed by four cumulative collected-resource
  banks. All tiers require current stock below 100; per-resource deadlines stop
  one shortage starving the others; explicit handlers exclude self and identify
  the recipient; unaffordable requests are acknowledged without tribute.
- `8ec8700` (`RAWAI-P3B44`) makes one siege weapon a home-defense threat while
  requiring five regular units, or two after attack commitment expires.
- `a66a9d9` (`RAWAI-P3B43`) fixes allied relief by anchoring the enemy scan on
  the requester's Town Center instead of filtering allied objects through the
  engine's self-only `object-data-under-attack` field.
- P3B36..P3B41 prevent inland Town Centers from becoming naval-siege targets,
  release stale transport escorts, serialize taunt attacks through the normal
  dispatch owner, cap remote food/hunt work, exclude self from target fallback,
  and stop repeated defense re-retreat/loaded-Transport recall during attack
  commitment.
- `f8a83ae` (`RAWAI-P3B35`) makes post-depletion gatherer allocation one-shot,
  addressing the leading 165,882-WORK command-flood source.
- P3B32 probes all four concrete Legionary forms under one family bound; recent
  replay evidence confirmed Legionary production, but sustained composition
  remains a runtime calibration item.
- Replay metadata joins commands through validated player numbers and uses the
  DE header's selected visible colors; replay files remain external evidence.

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

- Full P3B45 regression suite: 111 tests passed.
- Replay-benchmark validator: 20 benchmarks passed.
- PER, strategy execution, civilization strategy synchronization, good-unit
  JSON, ODS workbook, naval doctrine, and generated naval-score checks passed.
- Installed test runtime matches all 68 repository runtime files at the SHA-256
  recorded above.
- P3B45 adversarial read-only review verified mutually exclusive request tiers,
  all 120 reserve-safe explicit donor handlers, self exclusion, taunt mappings,
  and that all 12 acknowledgment-only fallbacks follow every donation handler.
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
2. In the next fresh match, verify `RAWAI-P3B45`, exercise all affordable allied
   resource tiers, confirm 500/1000 do not fire before their banks qualify, and
   verify that an initially unaffordable request does not produce delayed aid.
3. Confirm the P3B33 stance behavior: the army no longer alternates
   attack/home-defense on lone raiders, a real multi-unit raid still latches
   defense, and assault Transports board, depart, and land without being
   recalled by single raiders.
4. Measure the per-minute WORK, DUC, and attack-order rates and confirm the
   P3B35..P3B40 flood fixes before attributing any remaining endgame lag.
5. Implement a random per-AI taunt-response delay so allies stop answering the
   same taunt in the same instant.
6. Add a safe offset-from-Port fallback staging point so idle Transports no
   longer block fishing/merchant dropoffs when no other ship is 24-plus tiles
   away.
7. Continue taunt-69 visible deletion, behind-cliff Shipyard placement,
   attack-lift load/unload churn, migration drop-site work, idle priests,
   under-strength Town Center attacks, and the late Town Center order loop.
8. Analyze the next replay with `tools/analyze_replay.py`, update
   `replay-benchmarks.json`, rerun the complete validation set, synchronize the
   installed test AI, and update this handoff before ending the session.
