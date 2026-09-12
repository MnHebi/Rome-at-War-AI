# T58/506 deployment — 2026-09-12

Status: **DEPLOYED AND HASH VERIFIED; ENGINE STARTUP FAILED ERR6001**.
Subsequent user screenshot proves startup failure in coverage.per2:5979.
See `T58A-RULE-CAPACITY-REPAIR.md`;507 is not yet deployed. Historical hashes and
static results below remain evidence of the failed506 payload, not acceptance.

- Source: canonical `.trade-work/T30-trade-cap-civ-fix`, branch
  `fix/trade-cog-cap-dacian`, HEAD `a635d5598a6d292a9571d14abd178b669189b345`
  plus working changes. No commit or push in this deployment.
- Target: `C:\Users\LostSoul\Games\Age of Empires 2 DE\76561198053747760\mods\local\Rome at War AI\resources\_common\ai`.
- Marker: **RAWAI-P3B44T58:506**; all109 runtime files equal canonical source.
- Aggregate: `0adbc50b89d7fc1d09faacc1ebf3b92e7ca0c34ceb57d8f185a202365dde1569`.
  SHA256 of sorted filename + NUL + lowercase file-SHA256 + LF. This differs
  from the older T57 aggregate algorithm; compare per-file hashes as needed.
- External manifest and frozen registry:
  `G:\Projects\Codex\Rome at War AI\.analysis\deployment-t58-506-20260912T100119Z\manifest.json`
  and adjacent `command-boundary-registry.json`. Use both for decoding this run.
- Complete verified previous-file backup: adjacent `before` directory.
  Prior108 runtime files matched the T57 manifest before copying. Dependencies
  copied first, AI RAW.per last; changelog unchanged; nothing deleted.

## Installed experiments reconciled before deployment

The former installed general/customconstants variants are now in canonical
source, with the new observer regenerated around them. Stripping verified T58
wrappers reproduces both old installed files exactly (normalized line endings).
Counter1 increments without STOP; counter2 retains `de-game != 1`; conditional
de-game/wk-game definitions survive. No other original registered rule changed.
The observer now maps576 rules/814 commands/207 direct lists; its source-map
identity changed accordingly. Use the frozen registry, not an older T58 map.
Villager inventory is74 entries. Counter metadata no longer calls counter1 STOP.

The source includes the user's corrected Syracusan late Spearmen, prior approved
Dacian lineup, four whitespace normalizations and current T58 instrumentation.
The conditional-constant validator now distinguishes opposite preprocessor arms
from overlapping duplicates; focused tests retain rejection of actual duplicates.

## Validation and next acceptance

PASS: Python3.12 discovery655 run/653 passed/2 retired skips,93.116s; PER structure;
observer regeneration; Villager policy; maintenance9 and counter14 focused tests;
diff check; complete backup and installed hashes. Runtime still untested.

Steam options were not changed; no game was launched or terminated. File tracing
requires case-sensitive `LOGSYSTEMS=AIScript VERBOSELOGGING CONSTANTLOGGING`.
Verify startup40 for every AI, complete lists and first real boarding evidence,
and measure overhead at normal speed before requesting a long test. See
`T58-FILE-TRACE.md`. Deployment alone does not resolve the Villager flood.
