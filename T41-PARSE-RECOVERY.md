# T41 parse recovery

## Status

**FIXED-PENDING-RUNTIME**, deployed 2026-09-05 as
`RAWAI-P3B44T41:489`.

The first T40 test launch reported `ERR2005: Invalid Identifier` in
`rawai-military.per` line 1620. T39 had introduced four direct expressions of
the form `(villager-count >= 60)` / `(villager-count < 60)`. `villager-count`
is project goal 494, populated with `up-get-fact`; it is storage, not an engine
fact identifier. The first expression stopped parsing and the other three
would have failed subsequently.

## Causal correction

All four comparisons now use `up-compare-goal` with the appropriate `c:`
comparison operator. This preserves T39's exact-villager-count policy; it does
not broaden the measurement to `civilian-population`, which also includes
non-villager civilian classes.

`tools/validate_per.py` now rejects any identifier demonstrably used as writable
goal storage when it is called with bare fact syntax. The regression fixture
proves the invalid form is rejected and the corresponding `up-compare-goal`
form is accepted.

## Validation and deployment

- PER validation: **PASS**, empty report.
- Focused validator suite: **PASS**, 128 tests.
- Migration suite: **PASS**, 23 tests.
- Transport-lane suite: **PASS**, 3 tests.
- Ownership suite: **PASS**, 27 tests.
- Full Python 3.12 discovery: **PASS**, 505 tests.
- `git diff --check`: **PASS**.
- Causal/runtime commit: `31d86f5`.
- Installed runtime: 99 files, aggregate SHA-256
  `AB2271FA659CC47F6471CA950006FF73F986918D71057C12DD90BED099A858F2`.
- Synchronization postcheck: zero missing, different, unexpected, or remaining
  mismatched runtime files.
- Installed marker-file SHA-256:
  `926867FBC56C1312473934F906AAD251BAD2258E66F944AF97D3AB4359D9A5E8`.

Runtime acceptance still requires a fresh match to display `T41:489` and load
the AI without `ERR2005`. Static validation and byte identity do not close that
engine-level acceptance step.
