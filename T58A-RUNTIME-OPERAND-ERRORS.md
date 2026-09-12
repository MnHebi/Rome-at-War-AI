# T58A live engine operand errors — INVESTIGATING

**Superseded snapshot note:** completed-match results are in
`T58A-RUNTIME-REPLAY-ASSESSMENT.md`. The historical RAW58P1 prefix below is NOT
proof of Blue's identity: a FactId/player-domain bootstrap bug mislabeled Green.
That diagnostic initializer is corrected locally, not deployed. Operand errors
remain unresolved; the prepared standalone probe is still not installed.

2026-09-12 user reported repeated invalid ages1/2 and invalid goal0 after507
deployment. Source workspace/branch/HEAD still match HANDOFF; no runtime file
changes or deployment in this investigation. Installed507 identity remains the
verified prior-turn manifest. The game is running, but runtime acceptance fails.

Log supplied by user:
`C:\Users\LostSoul\Games\Age of Empires 2 DE\logs\2026.09.12-1328.46\MainLog.txt`.
It is nested below the standard logs folder. Live process command line confirms
LOGSYSTEMS=AIScript, VERBOSELOGGING and CONSTANTLOGGING; no options were changed.

At a193,869,370-byte snapshot, error counts and first physical lines were:

| Error | Count | First line |
|---|---:|---:|
| Invalid age ID1 |2,154,176|13,573|
| Invalid age ID2 |2,380,052|13,574|
| Invalid age ID0 |48,160|13,581|
| Invalid goal used0 |66,356|13,725|

Earlier decoder pass read192,370,649 bytes and recovered93,711 complete RAW58
records, no incomplete/checksum/framing records. First record ends at14,033;
startup40 at16,784 exactly matches the installed source-map identity. Only player1
appeared in that pass. This is not all-player trace acceptance. Live snapshots
differ as the file grows. Error lines have no player/site/rule identity.

## Boundaries, not a guessed fix

- Age errors precede the first trace frame. They are engine diagnostics, not
  malformed trace tokens. This does NOT exclude logger startup operations.
- Lowercase age aliases in rawai-unitconstants.per are0/1/2, unchanged at HEAD;
  uppercase phase constants are a separate domain and must not be rewritten.
- Cached AIRef documents Age0..3; the current engine rejects some uses of0..2.
  Numeric versus native-symbol handling is a lead, not established causation.
  The bundled AiBuilder uses a native-symbol alias (`phase1-age-cap castle-age`).
- No directly zero-valued goal storage operand was found in a simple exact-case
  literal/constant scan of goal/set-goal/up-modify-goal/up-compare-goal and g:
  operands. This scan does not prove dynamic/indirect operands are valid.
- Cached command signatures identify zero inputs in group creation, escrow
  flags, point-distance/target-point and precise-time. Several explicitly permit
  zero as a sentinel. Do not blanket-replace them or infer which emits the error.
- Additional object-invalid, focus-player(-1), and class-ID unit-type diagnostics
  exist; they were noted, not folded into a speculative behavioral patch.

## Discriminating experiment prepared, not installed

`tools/operand_smoke_probe.py` generates standalone `.analysis/T58 Operand Probe.per`:
57 rules,17 individually BEGIN/END-bracketed cases, all skipped after first pass.
It prints native age values, compares numeric/native/native-alias representations,
then tests documented zero-sentinel APIs independently. Goal-backed escrow/group
controls distinguish literal-zero handling. It loads no production AI and does
not issue unit movement, production, research or resource changes. Its sole group
operation uses an explicitly reset empty local search. Run only as a standalone
one-AI smoke case with the same mod, not appended to the production AI.

Two structural tests cover the bounded skip, paired markers and three age forms.
Static tests cannot determine current engine argument semantics. Exact missing
evidence is the bracket containing the error and its corresponding native/goal
control outcome. If standalone calls are clean, original rule/operand state must
be captured at the first production error instead; no runtime cause is asserted.

No gameplay correction, commit, push or deployment performed. Existing cleanup,
Ctrl boarding and transport behavior remain unchanged. Log delivery is partially
working; age/goal errors and all-player coverage remain unresolved.
