# T72 deployment — migration load-wait latch `RAWAI-P3B44T58B:512`

Installed 2026-09-20T12:14:49Z on user authorization, from the canonical
checkout, through the established process (`deploy-t72-512.py`, modelled on
`deploy-t71-511.py`). No game launch, no option change, no installed file
outside the AI payload touched.

## Identity

| Item | Value |
|---|---|
| Marker | **`RAWAI-P3B44T58B:512`** |
| Payload aggregate | `8c8d1f09661834af5f11f162aec109671d9d40b3d99774acb3d6c59e528ac8b8` |
| Files | 109 runtime `.ai`/`.per`; **3 changed vs 511** |
| Changed | `rawai-military.per` (the latch), `rawai-init-goals.per` (marker), `rawai-command-boundary-coverage.per` (identity) |
| Source | HEAD `b7e1c1c` plus the disclosed marker bump 511 → 512 and the T72 latch; the corrected tree is committed immediately after |
| Manifest | `.analysis\deployment-t72-512-20260920T121449Z\manifest.json` (+ `before/` backup of the installed 511 payload) |
| Installed / source / backup bytes | identical / identical / identical |
| Engine options changed / game launched | `false` / `false` |

## The change

One build note: the first install (12:11:52Z) was made from a tree whose
`rawai-military.per` had been rewritten with LF line endings by the removal
script. That was caught in review, the file was restored and the block removed
byte-preservingly, and the payload was reinstalled from the corrected tree —
against the 511 baseline restored from the backup. The installed payload now
differs from 511 by the 49-line block plus the marker and the coverage identity,
with no line-ending churn.

The 511 trace showed `MIGRATION-LOADING ↔ MIGRATION-CHECK-LOAD` alternating at
roughly 2 Hz for ~31 s stretches — 56 transitions each way — on hull 36524 (p1),
35288 (p2) and 35262 (p4), with 183–232 repetitions per player across the match.

The driver was one bridge site (1516): while the board-retry timer was still
**running** and the hull remained underfilled, it set the state back to
`MIGRATION-LOADING`, and `LOADING` immediately returned to `CHECK-LOAD`. Its only
job is to wait, so the branch is **removed** rather than latched:

- the retry timer still fires the bounded retry through the existing paths, so a
  genuinely dropped boarding order still recovers;
- the hull list built by the last `LOADING` entry persists across passes, and the
  selected object is re-resolved live from it, so the occupancy read stays
  current;
- seven legitimate `LOADING` entries remain (issue-board, renewal, recovery).

Nothing else changed: percentages untouched, the retasking bundle from 511
untouched, and the sea-leg `SAILING ↔ CHECK-LANDING` cycle deliberately left
alone so 512 stays a single-variable test.

## Acceptance (511 → 512)

| Measurement | What to look for |
|---|---|
| `LOADING` entries per voyage | the 183/209/232-style repetition collapses toward one initial entry plus justified retries |
| Same-hull reissues | garrison orders to passengers already entering the reserved hull approach zero |
| Storms | total ORDER packets, ≥150-packet storms, per-actor rate, and especially storms whose target is a **transport hull** |
| Loading reliability | boarding completion time, partial loads, successful departures, stranded passengers/hulls must not regress |

A drop in transport-target storms would strengthen the causal chain
(state oscillation → repeated boarding intent → native frame-rate order
persistence); it is not required to judge the state-machine correction itself.

For each permitted `LOADING` re-entry, record the reason from the existing state
and count information — timeout/no progress, changed hull, newly eligible
passenger — so the latch's remaining retries are auditable without a new logger.

## Also observed on 511 (context, not part of 512)

- No crash: the match ended cleanly (`Exiting with code 0`) after 53.8 min.
- Economy healthy: 234,778 WORK packets (72.7/s, the highest of the three
  recordings) — no worker freeze from the 511 retasking bundle.
- The storm actors are hunt/gather villagers whose only correlated traced events
  are the boarding writers, and no WORK packets land on the storm targets.
- The sea leg shows the same oscillation shape (222 × `SAILING → CHECK-LANDING`,
  216 back for p1) and is the next candidate if 512 leaves it intact.
