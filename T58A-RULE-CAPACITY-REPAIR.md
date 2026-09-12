# T58A/507 — startup rule-capacity repair

Status: **FIXED-PENDING-RUNTIME; DEPLOYED507**. Previous T58/506 **FAILED
engine startup**.507 startup remains unverified.

## Evidence and cause

User screenshot: Player1, `rawai-command-boundary-coverage.per2`, line5979,
`ERR6001: List full`, during match loading. Installed109 hashes still match the
506 deployment manifest, excluding accidental deployment drift.

`Program.token` in `tools/command_boundary_file.py` inlined the same eight-player
escape/log/checksum rules for every scalar. This produced6,542 library rules plus
7,229 coverage rules, exceeding the documented **10,000 total loaded rules per
AI** even without gameplay rules. Source: [AIRef data limits](https://airef.github.io/resources/articles/data-limits.html).
The cached AIRef `up-get-rule-id` semantics confirm a zero-based global rule ID,
usable with `up-jump-direct`; no new engine primitive is introduced.

The old tests validated individual rules and fixture execution but omitted the
aggregate compiled load limit. T58-DEPLOYMENT's static PASS was therefore not
startup acceptance. The screenshot directly falsifies engine readiness.

## Narrow correction and preservation

- Each token calls one shared emitter per module, with two appended private
  goals for the token return address/framing flag. Existing goal addresses stay
  fixed; outer observer returns are untouched. Normal fallthrough skips emitter.
- Same tokens, escaping, checksum, players, frame schema and record order.
  No quota reduction, sampling loss, actor cap reduction or shortened retention.
- Library491 + coverage528 = **1,019 rules**, down12,752.
- No gameplay rule/command-map changes in this repair. Registry metadata adds
  only the two private trace names. Installed cleanup experiments,
  boarding modifiers, ownership, mission code and user civilization edits remain.
- Marker becomes `RAWAI-P3B44T58A:507`. RAW58 log schema/prefix stays compatible.
  Source-map identity stays unchanged because command scopes did not change;
  full payload hash and marker distinguish this emitter implementation.

## Validation

`tools/validate_rule_capacity.py` recursively counts physical loaded rules, not
the semantic observer-stripped view. It resolves34 civilizations x6 difficulties
with DE enabled, counting both arms of all other conditions conservatively.
Repeated loads count repeatedly; missing/recursive loads fail closed.

Failed506: conservative maximum22,004, first overflow in coverage. Candidate507:
maximum**9,252**, leaving748 rules. This bound intentionally overcounts mutually
exclusive map/other branches; it is not an exact engine preprocessor emulation
or a claim to reconstruct the reported per2 line precisely.

The gate is enforced by both `validate_per.py` and source-manifest preparation.
New5-test regression suite passes: failed506 rejected; all204 candidate profiles
accepted with reserve; exact log-stream comparison for all8 players including
signed sentinels, initial/repeated invocations and late roster release; combined
startup/coverage/library calls at nonzero global offsets; comments, strings,
conditional arms, repeated loads and emitter fallthrough. Existing17 file-trace
tests pass, including unchanged actual scripted command issuance in fixtures.
Full discovery:660 run,656 passed,2 context-metadata failures,2 retired skips
(96.895s). Both metadata inconsistencies corrected; context9 and maintenance9
tests then passed. Context-size guard remains30,000 bytes; handoff was shortened,
not its limit raised. No outstanding test failure remains; full discovery was
not repeated for those documentation-only corrections.

Final deployment comparison proves only the two emitter modules, private
definitions/init and marker file differ from installed506. Every existing
private goal address and all registered command scopes remain identical. Installed506
files remain unchanged; candidate109 hashes match the new manifest.

External artifacts: `.analysis/t58-{failed,compact}-rule-capacity.json` and
`.analysis/t58a-507-source-manifest.json`. Candidate109-file aggregate:
`9e3823727574792e3677321a1ca07a92f2e5f80144269844f0f967b0d7ac5969`
(sorted filename + NUL + lowercase file-SHA256 + LF, then SHA256).

## Remaining acceptance / authority

Repair initially source-only. User authorized redeployment2026-09-12:
109/109 canonical files installed and hash verified; full506 backup verified;
changelog unchanged. Manifest/frozen registry/backup:
`.analysis/deployment-t58a-507-20260912T102708Z/`.
Fresh PER validation and five capacity tests PASS. Initial unittest module-style
invocation failed import resolution; correct discovery invocation passed all5.
No launch-option edits, game launch, commit or push.
Fresh engine startup must succeed for all players, then prove complete log
delivery, ordinary commands and real boarding. Runtime execution cost is still
unmeasured: smaller compiled code does not itself prove faster simulation.
The Villager706 flood remains INVESTIGATING, not fixed by this compiler repair.
