# T57 / 505 deployment

2026-09-08, explicitly authorized by the user. **DEPLOYED / PENDING RUNTIME ACCEPTANCE**.

- Source: canonical `.trade-work/T30-trade-cap-civ-fix`, branch `fix/trade-cog-cap-dacian`, HEAD `225403832206684c0c9363b99759665d082d96bc` plus the T57/505 marker. Marker assertions updated locally; no new commit/push in this deployment task.
- Replay marker: `RAWAI-P3B44T57:505`.
- Target: `C:\Users\LostSoul\Games\Age of Empires 2 DE\76561198053747760\mods\local\Rome at War AI\resources\_common\ai`.
- 108/108 runtime files verified:106 canonical files and2 intentionally preserved installed experiment files. Existing `changelog.txt` unchanged; no files deleted.
- Source aggregate: `050ff63f98b8500709c692b00a984aa76a9b0a965f0335f5fe894b8803f980db`.
- Installed aggregate: `8bb2b763162f4eabf726131774164127996f1f01d4634fc185a2b12884c9a949`.
- Full before/source/installed file hashes and backup: `G:\Projects\Codex\Rome at War AI\.analysis\deployment-t57-505\manifest.json`; sibling `before` contains all104 prior installed files.

Aggregate format: SHA256 of LF-joined, ordinally sorted `filename:lowercase-file-SHA256` lines, without final LF. Non-runtime changelog is recorded separately.

## Preserved experiments and identity caveat

`rawai-general.per` retains the removed missing-target STOP while still incrementing counter1, plus the DE guard on counter2. `rawai-customconstants.per` retains conditional `de-game`/`wk-game` definitions. Both remain byte-identical to the pre-deployment installation. These are recorded exceptions, not a claimed canonical cleanup repair. Counter1 still does not establish STOP issuance.

The old reported installed aggregate `60E05C...` did not reproduce under the explicit format above. Deployment initially stopped. Direct verification showed military/homebase/hunt equal the canonical pre-observer source text, both common-production files byte-equal the f6f1 baseline, entry-load differences explained by this candidate, and the two documented experiment differences. The fresh103-file pre-deployment aggregate is `4b0e50d6509e8a68f2eb8fe33dd22e14d6db0e1dcb779759fbeafe2b56ea5700`. The historical aggregate remains an unresolved format/provenance discrepancy, not evidence of a gameplay change; use the new per-file manifest for this match.

## Validation and acceptance

Prior candidate:625 Python3.12 tests PASS. After marker update: PER PASS; sampling6, observer15 and trade-topology10 tests PASS. Load dependency preflight and all installed hashes PASS. Backup hashes verified before copying; entry point copied last. This is deployment verification, not an engine startup or gameplay PASS.

Start a fresh ordinary match and confirm505. Observe IDs720–772 for paired boarding actors/hulls and actual default-writer targets; retain unknown list/credit coverage and the documented Green gap. Judge actual boarding/gather/deposit outcomes and native706 onset separately. Reactive Skirmisher production also needs fresh runtime evidence. No defect is closed by deployment.
