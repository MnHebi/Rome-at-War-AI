# Rome at War AI handoff

## Workspace and Git identity

The single canonical development workspace remains:

`G:\Projects\Codex\Rome at War AI\.pr-work\Rome-at-War-AI`

- Git root: same path.
- Active branch: `codex/replay-economy-build-order`.
- Recorded HEAD: `fbaaae134fb74e46ff0872d4747a3654c7b64d1c`.
- Pull request: <https://github.com/MnHebi/Rome-at-War-AI/pull/4>.
- Working-tree exception on 2026-08-29: `AGENTS.md` is modified because it is
  the user's replacement project-rules file. Its content matches the workspace
  root copy. Preserve it; do not discard or silently normalize it.

This document is in a separate diagnostic worktree created on 2026-08-29:

`G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-friendly-fire-defense`

- Git root: same diagnostic path.
- Branch: `recovery/p3b44-friendly-fire-defense`.
- Base: exact P3B44 commit `8ec870075d08fcac98bad55b4ff045bf7abbc42e`.
- Rules commit: `1a0b642` (`Adopt evidence-first project rules`).
- Diagnostic implementation commit: `59a8b96963fabdeaa0d65a29c4d01c4c2dd8f8c2`.
- Installed diagnostic marker: `RAWAI-P3B44D1:441`.
- Installed 68-file runtime SHA-256:
  `E418812BBEACCB7E1345344C8E9D550BEE304903FA0A30DABA0D5391496F7DC5`.
- Purpose: telemetry-only investigation of the allied-friendly-fire defense
  response observed in the 2026-08-29 11:01 replay.
- Status: experimental diagnostic; it does not replace the canonical workspace.
- Future agents must edit the canonical workspace for ordinary development and
  use this worktree only to continue this isolated P3B44 experiment.

Other recovery controls:

- `G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-attack-baseline`,
  branch `recovery/p3b44-attack-baseline`, exact commit `8ec8700`: immutable
  attack-behavior control. Never edit or relabel its runtime marker.
- `G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-transport-only`,
  branch `recovery/p3b44-transport-only`, exact commit `8ec8700`: transport-only
  experiment. Do not mix defense work into it.

The obsolete extracted snapshot
`G:\Projects\Codex\Rome at War AI\Rome-at-War-AI-main` is noncanonical and
must not be treated as current source.

## Current objective and preserved behavior

Establish the exact controller, attacker identity, selected player, final target
owner/type, and order path that caused Green military to converge after an
allied Mangonel fired on allied naval vessels. Do not implement a hostility fix
until a targeted P3B44D1 replay identifies the first causal divergence.

P3B44 Gray/Blue combined attacks are the known-good behavior at regression
risk. The diagnostic acceptance criterion is that all original P3B44 military
rules and command counts remain unchanged and that Gray/Blue still conduct
coordinated attacks in the fresh match.

## Defect ledger

### Friendly-fire defense trigger

- **Status:** INVESTIGATING.
- **User-visible symptom:** after a useless pond Shipyard was deleted, an allied
  Mangonel fired on allied AI naval vessels; nearby Green military then
  converged on that allied Mangonel despite locked teams.
- **Direct evidence:** user visual observation in
  `SP Replay v101.103.48987.0 @2026.08.29 110101.aoe2record`.
  The replay shows Green deleting objects 39457 at 48:53 and 40783 at 49:04.
  At 49:10 four Green objects received an ORDER targeting object 38529 in the
  same sequence as a Green DE_RETREAT.
- **Current causal hypothesis:** P3B44 selects an owned object with
  `object-data-under-attack`, then calls `up-find-player enemy find-attacker`.
  Allied splash may leave an allied attacker/player or target in that path, or
  a different controller may own the observed order.
- **Contradictory/unknown evidence:** the compact replay cannot identify dynamic
  object 38529's type or owner and therefore cannot prove it was the Mangonel.
  Source inspection does not prove how the engine applies the `enemy` selector
  to `find-attacker` after allied damage.
- **Instrumentation:** P3B44D1 publishes the attacked asset ID/type, raw
  attacker ID, selected focus player, final target ID/type/player, and command
  code. Reports are capped independently at 16 land and 16 naval command events
  per AI. Command codes: 1 severe land; 2 global naval; 3 coastal naval; 4
  fallback water target; 5 fallback land target.
- **Implementation:** diagnostic only. No selection, retreat, attack, transport,
  or defense command was changed.
- **Acceptance criterion:** reproduce the event while the report cap remains;
  identify the exact first allied identity transition and command path. If all
  recorded identities remain hostile, investigate the identified alternate
  controller instead of adding a speculative hostility gate. Gray/Blue combined
  attacks must remain comparable to P3B44.
- **Latest result:** deterministic/static validation PASS. Runtime attribution
  is not yet available, so the defect is not fixed or closed.
- **Next action:** run the preserved lobby with the verified P3B44D1 deployment,
  reproduce the condition early, and analyze the public `RAW44D DEF L/N`
  sequence.

### Other unresolved canonical defects

These remain owned by the canonical P3B50 line and are not changed here:

- Worker migration frequently reports zero engine-idle Villagers; boarding,
  route reachability, return/unload, and remote drop-site work remain unresolved.
- Assault Transport departure/landing, cliff-safe landings, hostile-corridor
  safety, and controller alternation remain pending runtime validation.
- Taunt 69 still acknowledges without visibly deleting the flared structure.
- Behind-cliff Shipyard placement remains unresolved.
- Command flooding remains unresolved: the prior P3B49 replay contained
  491,938 AI_ORDER actions, dominated by parser-unidentified Green objects.
- Profitable Merchant Vessel growth to 100/160 remains unverified.
- Tiered 100/500/1000 resource requests and donor fulfillment remain pending
  runtime confirmation.
- Port collision recovery, Palintonon recovery, naval opportunity engagement,
  Market buying, stalemate Wonder construction, and sustained Legionary
  composition still need runtime evidence.
- Cross-water allied relief is not implemented.
- The crash has no proven AI root cause. Existing ProcDump files establish heap
  corruption detection only, not the earlier corrupting writer.

## Replay evidence and diagnostic artifacts

- Replay basename:
  `SP Replay v101.103.48987.0 @2026.08.29 110101.aoe2record`.
- Replay SHA-256:
  `C1F85E836D59CBC2D77643D2608930DC3D7940C3ECFDC6081F0C08BBF833917F`.
- Duration: 58:51; the user manually resigned because the match was not
  advancing. This was not a crash.
- Visible-color/team mapping matches the authoritative preserved lobby:
  Red/Green/Yellow/Purple Roman Empire versus Orange Picts, Cyan Britons, Blue
  Germani, and Gray Gauls.
- External compact analysis:
  `G:\Projects\Codex\Rome at War AI\.analysis\replay-20260829-110101-p3b44-compact.json`.
- Repository evidence entry:
  `britain-4v4-20260829-110101-p3b44-control` in
  `replay-benchmarks.json`.
- The replay did not serialize P3B44's private startup marker. The pre-match
  deployment was independently verified as the exact immutable 68-file P3B44
  payload with SHA-256
  `EE04DE7BFA1448E90D54E8AC592D0EEECF4E9DAD93100272D2941F0209B75846`.
- P3B44D1 changes the marker to public `RAWAI-P3B44D1:441` so the next replay
  can establish runtime identity.

Replay/savegame files, crash dumps, compact parser output, and Rome at War data
mod files remain external and must never be committed to the AI repository.

## Validation performed

- Focused friendly-fire telemetry test: PASS (1 test).
- Full P3B44-derived regression suite: PASS (111 tests).
- PER structural/operand validator: PASS.
- Naval doctrine validator: PASS.
- Strategy execution validator: PASS (1,156 total matchups; 1,149 historical
  and 1,152 Extreme matchups with adjustments).
- ODS workbook round trip: PASS (34 civilizations, 680 unit-evidence rows, 340
  naval-class rows).
- Replay benchmark validator: PASS (21 entries).
- `git diff --check`: PASS; only expected CRLF conversion notices.
- Adversarial rule comparison against immutable P3B44: PASS. All 763 baseline
  military rules remain present after normalized-whitespace comparison, zero
  are missing, and the diagnostic adds ten observer/report rules. Counts of
  `up-target-objects`, `up-retreat-now`, `up-reset-attack-now`,
  `up-target-point`, `attack-now`, `up-find-player`, and
  `up-full-reset-search` are identical.
- Deployment verification: PASS. All 68 installed runtime files are
  byte-identical to the diagnostic source at SHA-256
  `E418812BBEACCB7E1345344C8E9D550BEE304903FA0A30DABA0D5391496F7DC5`;
  there are no missing, different, or unexpected runtime files, and the public
  P3B44D1 marker plus all five command-code records are present in the target.
- `validate_good_units.py`: pre-existing FAIL on both immutable P3B44 and this
  diagnostic branch because the recorded `unique-unit-production.json` hash is
  stale. This diagnostic patch does not mutate frozen strategy provenance.
- Fresh engine/replay validation: REQUIRED.

## Exact next actions

1. Verify this worktree's branch, HEAD, and clean state against this document.
2. Use the preserved Britannia 4v4 lobby and confirm `RAWAI-P3B44D1` appears.
3. Reproduce the allied Mangonel/naval friendly-fire condition early enough to
   stay below the 16-event report caps.
4. Preserve the complete Green `RAW44D DEF L/N` record and confirm Gray/Blue
   combined attacks still work.
5. Analyze the replay. Implement one causal hostility/ownership fix only after
   the telemetry establishes the earliest divergence. Keep this defect
   INVESTIGATING until then.
6. Do not merge diagnostic telemetry into the canonical P3B50 line merely
   because it compiles; first use it to establish causality and then port only
   the supported fix with a non-regression test.
