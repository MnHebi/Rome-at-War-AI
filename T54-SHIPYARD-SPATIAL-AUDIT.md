# T54 Shipyard spatial audit and bounded shoreline preference

## Identity and evidence

Replay: `SP Replay v101.103.48987.0 @2026.09.07 100934.aoe2record`,
48:03, marker `RAWAI-P3B44T54:502`, source `5dd9c63`.
Replay SHA-256 and full deployed runtime hash are in
`T54-RUNTIME-REPLAY-ASSESSMENT.md`. Current work does not change that runtime.

The initial 220x220 terrain grid was decoded from the replay header using
the existing mgz fast parser. Its documented row-major X/Y convention was
used, not guessed from minimap orientation. The three successful BUILD packet
coordinates all lie in shallow water adjoining beach, providing coordinate
controls. The map, CSV and per-player plots remain outside Git at:
`G:\Projects\Codex\Rome at War AI\.analysis\t54-shipyard-sites`.

Authoritative external DAT SHA-256:
`A1319BE7E0D4CCF68A13E719BA2D8B4B39383D01B7D3FDD3123452F6A0D36356`.
DOCK2 / Shipyard 1251 has collision radii (1.5,1.5), placement terrain (1,4),
side terrain (2,35), restriction 6. Relevant terrain names are shallow water
(1), beach (2), shallows (4), deep water (22), medium water (23). Restriction
6 disallows the grass/dirt/forest/desert centers found in these samples.

Source semantics were checked in the cached AIRef
`.analysis/airef-reference-20260830.js`: `up-point-terrain` reads terrain at a
goal pair; `up-can-build-line` takes an escrow goal (0 means without escrow).
Thus reason 64 alone is not a geometry-only verdict. Reference:
https://airef.github.io/commands/commands-details.html#up-point-terrain

## Spatial classification across all players

2,571 complete rejected-candidate records were reconstructed by player from
545 + 536/537/538/540. Of these, 2,497 carry reason 64. Coordinates are samples,
not distinct sites, and repeated points remain counted as repeated attempts.

| Player | Reason 64 | Land center | Water, no shore within two tiles | Coastal/mixed unresolved |
|---|---:|---:|---:|---:|
| Blue | 170 | 91 | 47 | 32 |
| Red | 184 | 108 | 41 | 35 |
| Green | 300 | 214 | 49 | 37 |
| Yellow | 407 | 228 | 112 | 67 |
| Cyan | 350 | 153 | 147 | 50 |
| Purple | 227 | 133 | 61 | 33 |
| Gray | 213 | 118 | 76 | 19 |
| Orange | 646 | 398 | 132 | 116 |
| Total | 2,497 | 1,443 | 665 | 389 |

84.4% are land-centered or have an entirely water 5x5 neighborhood. These are
poor shoreline proposals, not evidence that a correct coast point was rejected.
The remaining 389 are NOT classified as valid: footprint, trees/buildings,
exploration, available resources and engine placement rules remain unproven.
The header grid cannot establish dynamic occupancy at the rejection time.

All three issued foundations became ready: Cyan (175.5,94.5), 26:05->26:43;
Purple (153.5,11.5), 34:41->35:13; Blue (43.5,179.5), 44:13->44:53.
Five players issued none; nobody issued a second Shipyard. Runtime acceptance
for adequate multi-player Shipyard output is FAIL. Location quality of the
three completed yards is not declared proven from initial terrain alone.

## Causal boundary and implementation

The generator picks independent random X/Y offsets in a square around a ready
Port/Shipyard. It spends the eight-candidate admission budget on points without
any coastline preference. Spatial evidence confirms the wasted candidate
budget; a new terrain eligibility ban or relaxed build gate is not justified.

Repair commit `fc71f0e` changes only candidate discovery:

- Try at most four cheap draws for each candidate, within the existing domain.
- Prefer beach (2/35), or shallow water/shallows (1/4) with beach at a two-tile
  cardinal sample. Clamp neighbor probes; out-of-map candidates retain reason 62.
- If the first three draws do not qualify, use the fourth UNFILTERED. This
  preserves an avenue for other terrain variants and diagonal coast shapes.
- Only one selected candidate enters the existing expensive checks per pass.
  Eight selected candidates still bound an admission episode (at most 32 draws).
- No new telemetry, timer increases, capacity changes, escrow changes, worker
  commands, placement radius changes or Port redesign.

All buildability, memory, spacing, water-aperture, mobile-path, worker and exact
foundation checks remain. Initial random-number range behavior is intentionally
unchanged (AIRef uses 1..29; subtracting 14 actually yields -13..15).

This is a sampling-efficiency repair, not proof that all Shipyard delays are
fixed. Affordability and the 389 coastal/mixed rejections remain separate
boundaries. Do not widen placement or waive safety based on this result.

## Validation and acceptance

- Shipyard execution tests: 25 PASS (including preserved admission/capacity,
  exact water checks, foundation verification, clearance and bounded retries).
- Spatial-analysis tests: 3 PASS; interleaved player diagnostics cannot mix.
- Episode diagnostics suite: 9 PASS.
- All three T54 successful candidate coordinates remain preferred in a
  deterministic terrain fixture. This does not simulate engine construction.
- Land/open-water samples are skipped before full gates; terrain variants keep
  the unfiltered fallback; all-invalid search remains bounded.
- Generated synchronization and PER structural/operand checks: PASS.
- Full Python 3.12 discovery: 572/572 PASS. The first run failed only the hot
  context size guard; concise handoff maintenance fixed it before the full rerun.

Status: FIXED-PENDING-RUNTIME for wasted blind candidate sampling; overall
Shipyard output remains open. Not deployed. Fresh acceptance must show earlier
concrete foundations across eligible players, progress beyond one yard where
demand/resources permit, and no regression to cramped or unreachable yards.
Compare rejection reasons and build/completion timing, not just chat volume:
the shortlisted distribution necessarily changes the reason-64 sample count.
