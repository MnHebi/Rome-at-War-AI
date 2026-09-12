# Source consistency maintenance — 2026-09-12

Historical maintenance-stage snapshot. Subsequent authorized deployment and
experiment reconciliation supersede installed/candidate identities below;
see `T58-DEPLOYMENT.md`. Original maintenance evidence is retained unchanged.

Scope: four whitespace-only civilization differences, stale runtime references
and the good-units evaluation provenance warning. No deployment or gameplay
policy change. Preserve the user's separate Syracusan edit.

## Whitespace

`rawai-civ-pontus.per`, `rawai-civ-romeemp.per`, `rawai-civ-romerep.per` and
`rawai-civ-seleucids.per` were normalized using the existing strategy generator.
Before writing, generated/current source was compared after whitespace removal;
all four matched. `git diff -w` is empty for those files, and generation is now
idempotent. Only Dacian/Syracusan intentional policy differences remain; do not
regenerate these over the user-approved lineups.

## Runtime identity

- Installed: **T57/505**,108 files, reverified byte hashes without changes against
  external `.analysis/deployment-t57-505/manifest.json`.
- Current working candidate: **T58/506**,109 runtime files, **NOT DEPLOYED**.
- Removed stale marker500/502 prescriptions from current next actions. T57/505
  remains the verified replay baseline; later evidence needs its own identity.
- Removed the obsolete pre-marker hash labelled as the current candidate from
  project state. Generate a fresh manifest from current files before deployment.
- Fresh109-file working snapshot: external
  `.analysis/maintenance-t58-506-source-manifest.json`, aggregate
  `d785bfef88e3552e2f8f4a919deded811829aa34fbb154a94c7fbaf0df8ad462`
  using sorted filename + NUL + file SHA-256 + LF. Includes the user's Syracusan
  edit, not just this maintenance patch. It is not an installed-runtime hash.
- `T58-VALIDATION.json` remains the historical b4f0e2c snapshot, not silently
  rewritten evidence. The current marker, formatting and user's Syracusan edit
  mean its aggregate is not the current candidate aggregate.

## Good-units provenance

Recorded `AI RAW.per` hash `970c965c08c8396b89a41e7c6a1662a3c2f57e0e885e0189915400686d4dbb00`
matches the Git blob at `dc81448571bc4c49d97a3c5574b26c321de209e0`.
The evaluator reads only34 civilization priest/navy affinity pairs from this
file. Every pair is identical in the recorded source and current source.

The shared extraction now lives in `tools/good_units_provenance.py`; evaluator
and validator consume the same implementation. Input schema is
`priest-navy-affinities-v1`; canonical sorted compact JSON SHA-256 is
`b9cecfeecf7b21d75848d586e8721f9f43c05ece7642662a7f6c5c3748d81a28`.
The original full-file hash remains historical provenance, not overwritten.
Legacy documents without input fingerprints still require exact raw hashes.
Missing sources, unsupported input schemas or changed input flags remain errors;
DAT, tech-tree, civilizations and unique-unit manifest hashes remain strict.

No ratings were recomputed or changed. Both canonical and workspace-root
`RAW AI good units per civ.ods` are byte-identical, SHA-256
`6116bb540a4a6acfbec111812cb756f6b1768454a97af558d3418e8541f1bcf9`,
and validate against the unchanged ratings,
680 unit-evidence rows and340 naval-class rows. The JSON provenance fields were
the only evaluation-data edits. No spreadsheet rewrite is necessary.

This closes these maintenance warnings, not the Villager flood or pending T58
engine delivery/performance acceptance. Dacian/Syracusan strategy-source
reconciliation is a distinct remaining item, with user-approved policy known.

## Validation

- Eight focused maintenance tests PASS, including meaningful input changes,
  harmless diagnostic edits, legacy strict hashes, missing sources and markers.
- Good-units document and both ODS copies PASS; raw Git-blob comparison confirms
  every non-provenance evaluation field is unchanged.
- Four formatting round-trips PASS; `git diff -w` empty for those four PERs.
- Physical PER, command-boundary generation, context and diff checks PASS.
- Final Python3.12 discovery:654 run,652 PASS,2 retired chat-only skips,92.206s.
  Canonical working tree includes preserved pre-existing changes. First attempt
  hit sandbox Temp permissions and handoff size; shortened the handoff without
  relaxing the limit, then reran with authorized normal Temp access.
- Installed108-file manifest and current109-file candidate manifest PASS.
  No deployment, workbook cell changes, commits or pushes in this maintenance.
