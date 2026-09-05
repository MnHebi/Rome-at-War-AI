# T48 Shipyard candidate recovery

## Status

**ROOT-CAUSE-PROVEN / FIXED-PENDING-RUNTIME / DEPLOYED**, 2026-09-05.
Source and installed marker `RAWAI-P3B44T48:496`. The source/install runtime
SHA-256 is
`84608D9C772671F6B34977A744B603544EE1CAAB29429CE12E58C88BA003E07C`.

## Runtime evidence

The completed T47 replay is
`SP Replay v101.103.48987.0 @2026.09.05 153105.aoe2record`, SHA-256
`8FE36339F72B3E2AD0A2073C6F27ED1B56FEE206D677858FAC25E352BBBC800C`.
It runs 49:32 with zero parser errors. Only two Shipyard (`1251`) build orders
appear: Player 8 at 24:16 and Player 6 at 46:31.

Diagnostic 410 reports 43 exact-candidate-unbuildable (`64`) transitions, 30
no-anchor (`61`) transitions and six map-bound (`62`) transitions. It reports
no failed-site-memory (`63`), own-clearance (`65`), allied-clearance (`66`) or
water-exit (`67`) transitions. The dominant runtime boundary is therefore the
candidate generator, before the retained clearance and open-water checks.

## Source cause

T40 replaced T36's runtime-working random +/-14 candidate domain with only 24
fixed cardinal/diagonal offsets at radii 12, 24 and 40. A Shipyard requires a
very particular land/water footprint, so those sparse exact points usually
failed `up-can-build-line`; T47 identifies that failure directly as reason 64.
The T36 control on the same Iberia setup emitted 33 Shipyard build orders.

The anchor iterator also treated end-of-list as absence. After rejecting a
candidate around a single Port, the next scan removed that Port because its ID
was not newer than the stored cursor. The no-target branch emitted reason 61,
stored a false failed-site entry, advanced the candidate counter and only then
reset the cursor. T47's repeated 64 -> 61 sequences confirm this path at
runtime. Half the fixed candidates were consequently skipped for one-anchor
players.

## Bounded correction

- Rebuild and wrap the ready Port/Shipyard anchor list once when its ordered
  cursor is exhausted. Only a genuinely empty rebuilt list emits reason 61.
- Do not consume a candidate step or failed-site-memory entry during a normal
  cursor wrap.
- Restore one bounded integer sample from T36's full 29x29 domain around the
  chosen anchor (`-14..+14` on each axis).
- Retain exact `up-can-build-line`, own/allied ten-tile clearance, four-point
  same-water open-exit validation, worker reachability/ownership, admission,
  affordability, failed-site memory and concrete-foundation verification.
- No trade, transport, economy, wall, Port or naval-combat policy changes.

Behavioral commit: `8e69ef2`.

## Validation

- Shipyard lifecycle/geometry fixture: **PASS**, 16 tests, including a first
  unbuildable point followed by a successful same-anchor wrap/sample.
- Trade topology: **PASS**, 10 tests.
- Validators: **PASS**, 128 tests.
- Generated Shipyard source synchronization: **PASS**.
- PER structural/operand validation: **PASS**, empty report.
- Naval doctrine: **PASS**.
- Strategy execution: **PASS**, all 1,156 matchups.
- Ownership audit: **PASS**, 970 relevant sites, zero permission failures.
- Full Python 3.12 discovery: **PASS**, 514 tests. The sandboxed run reached the
  known Windows Temp permission error only; the authorized rerun passed.
- `git diff --check`: **PASS**.

## Runtime acceptance

Deployment was explicitly authorized from canonical HEAD `407a31f`. Preflight
found only `rawai-init-goals.per` and `rawai-specialplacement.per` different;
both were copied. The post-apply read-only check reports all 99 runtime files
identical with no missing, different or unexpected files.

In a fresh T48 replay:

1. first Shipyard build orders must occur across the players that possess a
   completed Port and can afford/build the yard;
2. reason 64 and false alternating reason 61 must fall materially;
3. concrete foundations must appear and complete;
4. later minimum-capacity yards must continue to progress;
5. reasons 65/66/67 must continue rejecting crowded or closed-water sites;
6. no narrow-crevice congestion regression may appear.

Until those engine outcomes are demonstrated, this remains
**FIXED-PENDING-RUNTIME**.
