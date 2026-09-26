# T67 deployment — passenger-entering-guard candidate `RAWAI-P3B44T58B:510`

Deployed on user authorization ("deploy"), 2026-09-19T19:23:16Z, from the
canonical checkout `.trade-work\T30-trade-cap-civ-fix`, through the established
process used for the 505-509 payloads (`deploy-t67-510.py`, modelled on
`deploy-t63-509.py`). No game launch, no option change, no marker in any other
file, and no installed file outside the AI payload touched.

## Identity

| Item | Value |
|---|---|
| Marker | **`RAWAI-P3B44T58B:510`** (number bumped from 509; label unchanged) |
| Payload aggregate | `ba6b82099dd15900e61bf011c9a080ffc09afd308ce079d4b35d61d294bd6c04` (SHA256 sorted filename + NUL + file hash + LF) |
| Source identity words | `[772654496, 1369038263, -1303685221, -1515768717, -314195307, -700335015, 499018650, 1409466293]` |
| Files | 109 runtime `.ai`/`.per`, 104 identical to the installed 509 payload |
| Source | HEAD at deploy time `74e27f7` plus the disclosed marker bump 509 → 510; the passenger entering guard (`ba4a77c`) and the taunt fix (`300dac4`) are already committed |
| Manifest | `.analysis\deployment-t67-510-20260919T192316Z\manifest.json` (+ `before-manifest.json`, `command-boundary-registry.json`, `before/` backup of all installed files) |
| Prior payload | `.analysis\deployment-t63-509-20260919T172057Z\manifest.json` |
| Engine options changed / game launched | `false` / `false` |

## Files installed (5)

- `rawai-init-goals.per` — marker `(up-chat-data-to-all "RAWAI-P3B44T58B: %d" c: 510)`.
- `rawai-military.per` — the passenger entering guard at 16 command-boundary
  sites (rendezvous start, issue-board, load-diag-apply, check-load renewal and
  the passenger STOP/move/unload/default chains).
- `rawai-exploration-policy.per` — the same guard at the migration retire-scout
  passenger selection (1 site).
- `rawai-tauntcommands.per` — the taunt-31 acknowledgement fix from `300dac4`,
  now installed for the first time (509 predates it).
- `rawai-command-boundary-coverage.per` — regenerated source-map identity words
  after the registry line renumbering.

The guard added at the 17 sites is, immediately after the existing
`garrisoned == 1` removal:

```per
(up-remove-objects search-local object-data-action == actionid-enter)
(up-remove-objects search-local object-data-order  == orderid-enter)
```

Selections that only count passengers (chains issuing no command) were left
untouched, so manifest/admission arithmetic is unchanged. Everything else,
including `changelog.txt`, is byte-identical to the previous install.

## Verification performed

| Check | Result |
|---|---|
| Candidate gates before install | `validate_per` no findings; generator `PASS 579 rules 817 commands`; capacity 9,312/10,000 PASS; strings 1,498/1,500 |
| Focused suites before install | `test_boarding_ctrl`, `test_command_boundary_file`, `test_file_trace_capacity`, `test_command_boundary` — 39 tests OK |
| Installed bytes vs manifest | identical (109/109) |
| Source bytes vs manifest | identical (guards against a source change during deployment) |
| Backup vs pre-deployment hashes | identical (rollback available from the recorded `before/` directory) |
| Installed marker line | `(up-chat-data-to-all "RAWAI-P3B44T58B: %d" c: 510)` |
| Changed vs 509 | 5 of 109 files |
| Extras preserved | `changelog.txt` (hash unchanged) |

## Not yet established

The payload is installed and hash-verified but has **not** been exercised: no
match has been recorded against 510, so the entering guard and the taunt fix are
source-verified only. The next acceptance step is a replay on 510 reporting the
marker, the taunt-31 count and any ORDER-storm change at the same actors.
509 remains the last analysed recording.
