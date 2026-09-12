# T58B: remove Town Center coupling from migration admission

Status: **FIXED-PENDING-RUNTIME** for this admission boundary. Overall resource
migration productivity remains **INVESTIGATING**. Local508; installed507 untouched.

## Evidence and correction

Commit22ab687 added three global TC predicates to migration admission to protect
shared placement: idle colony-TC controller, no pending TC objects, no pending TC
placement. The same commit separately guarded the later drop-site construction
stage. Admission reserves transport ownership; it does not issue construction.
T58A replay133042 sampled pending-placement blocker128 for Blue at40:23.893 and
Yellow at39:57.647, with later route/clearance combinations. These samples prove
specific holds, not uninterrupted blockage or the cause of every failed migration.

At user request, remove those three predicates from admission and its diagnostic
fingerprint. Remove obsolete blocker bits32/64/128 without renumbering remaining
bits; field574 remains informational colony-TC state. Keep writer1312's actions,
all command IDs/operands, deadlines, selections and modifier behavior unchanged.
Refresh command-boundary registry/source-map coverage through the existing generator.

Preserve the three TC predicates at `MIGRATION-WAIT-DROPSITE-OWNER`, placement-lock
acquisition/release, home TC production, relic/recovery/repair/route/clearance
ownership, and the one-pass yield to a viable assault. No queue reset, native
gathering change, assault change, deployment, commit or push.

## Validation and remaining evidence

- Focused lane tests execute current source predicates: all8 combinations of TC
  controller activity, pending foundation and placement permit admission and its
  fingerprint. Each transport-owner conflict still blocks admission.
- Construction-stage tests execute the same8 combinations: any TC conflict still
  blocks construction; no conflict permits entry. Existing assault-priority tests
  and bounded diagnostics assertions remain in place.
- Focused lane6/diagnostic9 tests PASS; generator576rules/814commands and PER PASS.
- Capacity PASS:9249/10000 physical rules,751 headroom. No new log strings.
- Full Python3.12 discovery PASS:666run,664passed,2retired skips(97.463s).
  Initial run encountered sandbox temp-directory errors plus obsolete gate and
  inventory-line assertions; corrected those expectations and reran outside the
  sandbox. Villager inventory changed only by source line numbers, not policy.
- Against frozen507 registry: all writer IDs/actions/command operands unchanged;
  only command-bearing semantic rule1312 has different predicates. All109
  installed507 file hashes still match. Context validation and diff-check PASS.

Runtime acceptance: autonomous resource migration can enter while unrelated TC
work is pending; it still waits safely before conflicting drop-site construction,
then builds a usable drop site and gathers/deposits the intended resource. Preserve
TC construction, relic separation, existing assault service and worker ownership.
Historical zero-mask admission windows and later inner gates remain unresolved;
this change alone is not evidence that Blue/Yellow productivity is fixed.

## Subsequent user-requested Town Center cap

Lowered phase7 desired TC counts from8 to4 in all34 `rawai-civ-*.per` files,
and the independent resource-pressure colony gate from `<8` to `<4` in
`rawai-homebase.per`. Earlier desired targets remain1/1/1/4. No demolition,
placement-policy change or deployment. The structure-count blocks are hand-authored
outside `sync_civ_strategies.py`'s generated doctrine regions.

Preserved installed507 Dacian/Syracusan doctrine exceptions; compared all34
current civilization texts against installed507 with only8-to4 substituted:
no other semantic differences. The doctrine synchronizer still proposes the
pre-existing Dacian/Syracusan changes, which are not authorized by a TC cap task.
Tests cover all34 sequences, ordinary expansion's total-count gate, and colony
resource pressure at3/4/8 TCs. Cap status: FIXED-PENDING-RUNTIME.
Final source validation: focused cap3 PASS; full discovery669run,667PASS,
2retired skips(110.210s); PER/generator/context/diff-check PASS. Runtime not tested.
