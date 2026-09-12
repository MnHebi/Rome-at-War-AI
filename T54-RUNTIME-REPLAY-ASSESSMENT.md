# T54 assault landing regression

Replay: `SP Replay v101.103.48987.0 @2026.09.07 100934.aoe2record`.
SHA-256: `F54A298A2D2AD9A4BE22BFA126E4BDC31BA573CD6DC2CD4AD01976B03EA276C5`.
Duration 48:03; parser errors: none. Replay marker T54:502 agrees with deployed
source `5dd9c63`; all 99 installed files match aggregate hash
`572BAEC05AEEE6C71E1E434EF2CB3ACA953E1157D227A8EB9CC424651EE5365A`.

## Acceptance result: FAIL

The user rescued two assault squads around 44 minutes because their actual
unload tiles had no route to the objective. This directly fails the T54
land-egress acceptance criterion. A scripted landed/combat event is not proof
of productive landing or traversable terrain.

Matching Blue lifecycle leads:

| Hull / slot | Commit | Landed event | Subsequent event |
|---|---|---|---|
| 36399 / 1 | 42:21 | 43:25 | Combat target 43:41; repeated later |
| 34955 / 2 | 43:07 | 44:03 | Combat release 44:19 |

These are temporal matches, not a proof that each is one of the user-rescued
groups. Blue unload requests include (80,159) at 43:09, (71,162) at 43:47,
(65,179) at 43:52, and (42,209) at 44:07/44:22. Orders alone do not identify
manual versus scripted provenance or prove actual passenger landing positions.
The parser's UNGARRISON object IDs also appear shifted relative to diagnostic
hull IDs; do not join those fields as literal identity without decoder validation.

Across the whole replay's recorded slot telemetry, Blue has five commits and
five landed events, 28 combat-target events and four combat releases. Yellow
commits once at 47:53, ten seconds before the replay ends. No other player's
slot commit appears. Only two plan failures appear, both reason 30 (lost
admitted objective), one each for Blue and Yellow. There are no reason-41
land-egress rejections. Recorded telemetry is not a census of unobserved native
operations.

## Source defect and narrow correction

T54 queried each enemy land witness with option 0. AIRef documents that this
permits a few tiles of separation to find a reachable open tile; option 1
requires the destination tile itself to be open/reachable:
https://airef.github.io/commands/commands-details.html#up-path-distance
(definition verified from https://airef.github.io/js/commands.js on 2026-09-07).

Consequently, a finite option-0 result cannot establish a path to the proposed
landing tile. The correction changes only the three land-witness checks to
option 1. Transport unload-vicinity checks remain option 0. The deterministic
regression case supplies an option-0 success and option-1 failure at the first
candidate and verifies reason-41 memory plus selection of another shore with
the loaded manifest intact.

This is a source-proven insufficient test, but T54 did not record which
acceptance branch the two reported missions took. It is not proof that this
single correction resolves both observed landings.

## Unresolved boundaries and diagnostic coverage

- No visible witness still bypasses land proof, preserving the existing
  structure-only cleanup fallback. Absence of a visible unit is not evidence
  that the objective region is accessible.
- A mobile enemy within 80 tiles is only a proxy for the objective region;
  it does not establish every friendly passenger's path to the exact objective.
- Actual unload tiles may differ from the requested coordinate, especially
  with obstruction and cliff geometry.

Three accepted-candidate records per new preparation mission now capture hull,
objective, requested landing x/y, witness count and selected witness ID.
Witness -1 explicitly means the no-witness fallback. The budget is not rearmed
by candidate retries. Existing reason 41 records rejected candidates.
This adds no unit commands. The diagnostic is needed to distinguish the
remaining paths rather than guessing which caused the two rescues.

The broader landing defect remains INVESTIGATING. The option-1 correction is
FIXED-PENDING-RUNTIME and is not deployed. Next acceptance must include actual
unload positions and autonomous movement from those positions toward the
objective; manual rescue does not count as a pass.

No help episode IDs 312-317 appear in this replay. This does not validate the
help repair; its previous runtime-pending status remains.

## Validation

- Assault planner: 31 tests PASS, including tolerant-neighbor rejection and
  bounded missing-witness diagnostics.
- Shoreline resolver: 12 tests PASS.
- PER structural/operand checks and generated-source comparison: PASS.
- Full discovery result is recorded in HANDOFF.md.
- Runtime acceptance for land egress: FAIL; further fresh runtime required.
