# T47 Shipyard rejection diagnostics

## Status

**RUNTIME COMPLETE / DIAGNOSTIC-ONLY / SUPERSEDED BY T48**, 2026-09-05. Source
and installed marker `RAWAI-P3B44T47:495`.

## Runtime regression evidence

The user reported that the current T45 Iberia match had no Shipyards. A
read-only snapshot of the still-live replay
`SP Replay v101.103.48987.0 @2026.09.05 141708.aoe2record` reached 68:15 with
zero Shipyard (`1251`) build packets. Every player entered the Shipyard
controller: bounded diagnostic 410 alternated between reason 1
(unaffordable/unavailable, including insufficient unescrowed resources) and
generic reason 6 (coast/exit rejected). Once admission became possible, no
candidate reached build issuance.

This is a regression against the same authoritative lobby shape and map ID 49
(Real World Iberia). The earlier T36 replay
`SP Replay v101.103.48987.0 @2026.09.04 223434.aoe2record` emitted 33 Shipyard
build packets across all eight players. Its replay settings and civilization
slots match the current replay. The source already maps the engine's
`REAL-WORLD-SPAIN-MAP` symbol to `RIVERS`, so missing Iberia classification is
disproved.

## Remaining evidence boundary

T40 collapsed seven distinct resolver exits into reason 6:

- no completed Port/Shipyard anchor;
- candidate clipped by map bounds;
- recent failed-site memory exclusion;
- `up-can-build-line` rejecting the exact candidate;
- own Port/Shipyard clearance;
- allied Port/Shipyard clearance;
- all four exact mobile-water exit directions failing.

The current replay cannot distinguish these. Those causes require different
behavioral corrections, so changing candidate density, clearance, or path
policy now would be a guessed fix.

## Diagnostic-only change

The existing transition-latched, 60-second diagnostic 410 now reports the
actual resolver exit:

- 61: no anchor;
- 62: candidate outside the map;
- 63: recent-site memory;
- 64: exact candidate is not buildable;
- 65: own naval-building clearance;
- 66: allied naval-building clearance;
- 67: water-exit validation.

Admission, timing, candidate offsets, clearance radii, exact path checks,
economy gates, worker selection, build issuance, foundation verification, and
failed-site memory are unchanged. This patch therefore does not resolve the
runtime defect and must not be described as a gameplay fix.

## Validation

- Shipyard fixture: **PASS**, 15 tests, including executable coverage of every
  new 61–67 terminal.
- Focused placement/trade/transport/ownership set: **PASS**, 213 tests.
- Generated Shipyard source synchronization: **PASS**.
- PER structural validation: **PASS**, empty report.
- Naval doctrine and strategy execution: **PASS**.
- Ownership audit: **PASS**, 969 relevant sites, zero permission failures.
- Full Python 3.12 discovery: **PASS**, 513 tests.
- `git diff --check`: **PASS**.
- Diagnostic commit: `30d36b0`.

## Runtime acceptance and next action

The user explicitly authorized deployment. Preflight found exactly three
differences (`rawai-economy.per`, `rawai-init-goals.per`, and
`rawai-specialplacement.per`), and the post-apply read-only check reports all 99
runtime files byte-identical with no missing/different/unexpected files.
Installed aggregate SHA-256:
`9800DEF42ED21A3A46729713DEA02B46849E898DE8C47D7FEA444D57C0F4061B`.

The completed T47 replay runs 49:32 with zero parser errors. It contains only
two Shipyard build orders. Diagnostic 410 records 43 reason-64 exact-site
rejections, 30 reason-61 anchor rejections and six reason-62 map-bound
rejections; reasons 63/65/66/67 are absent. Source inspection then proves that
the ordered anchor cursor reports a false reason 61 at normal end-of-list and
that T40's sparse exact-offset lattice replaced T36's runtime-working dense
near-anchor domain. T48 repairs those two candidate-discovery divergences while
retaining the safety gates. The gameplay defect remains open under T48 pending
fresh runtime proof.
