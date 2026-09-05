# T43 land-trade shared-search recovery

## Status

**ROOT-CAUSE-PROVEN / FIXED-PENDING-RUNTIME.** No deployment was performed.

## Runtime evidence

The T41 replay `SP Replay v101.103.48987.0 @2026.09.05 121955.aoe2record`
contains the replay marker `RAWAI-P3B44T41:489` and runs to 85:45. Player 1
built Markets at 10:29 and 27:33. Every allied player also issued at least one
Market build order between 10:50 and 16:51. Nevertheless:

- no player emitted `trade land candidate ally`;
- no player produced a Trade Cart (unit 128);
- Player 1 emitted all eight `trade topology no candidate` samples;
- water discovery remained live and repeatedly emitted `merchant water proof
  ally`.

This is a runtime FAIL for T38's land-trade acceptance. Removing the Market
zone veto was necessary but did not reach the earliest remaining divergence.

## First causal divergence

Each topology-start rule built a local Market DUC search, saved the producer
counts, and advanced to `TRADE-ROUTE-LAND-SOURCE`. On the following rule sweep,
the land-source rule required:

```text
(up-set-target-object search-local c: 0)
```

That depends on the preceding rule's shared `search-local` list surviving a
state boundary. It is not controller-owned storage and can be overwritten by
any intervening DUC search. The repository already treats this as unsafe in the
military controller and T12 source audit. The water branch succeeds because it
rebuilds its searches in the rule which consumes them.

The failed shared-list lookup prevented the per-ally land scan from starting,
which is earlier than Cart admission, resources, `can-train`, the three-Cart
probe cap, and live `actionid-trade` proof.

## Implementation

- Persist the known home or colony land anchor alongside the completed Market
  producer census at topology start.
- Advance from `TRADE-ROUTE-LAND-SOURCE` using the persisted producer counts and
  anchor, without consuming a shared DUC list from the previous rule sweep.
- Keep the exact producer-epoch check, per-ally scan, `wait-techup-requirements`,
  resources, `can-train`, three-Cart probe ceiling, and live `actionid-trade`
  proof unchanged.
- Keep the independent water candidate/proof path unchanged.

The persisted anchor is used only to order candidate Markets. Actual route
viability is still established by the bounded Trade Cart probes, not inferred
from the anchor.

## Validation

- Focused executable/mechanical topology tests: **10/10 PASS**. The executable
  fixture deliberately clobbers the shared DUC list and verifies that a valid
  persisted producer census still begins the land scan.
- T13 gate recovery: **7/7 PASS**.
- Validator tests: **128/128 PASS**.
- Full Python 3.12 discovery: **510/510 PASS** in the permitted temporary-file
  environment.
- PER structure/operands: **PASS**.
- Naval doctrine: **PASS**.
- Strategy execution: **PASS**.
- Ownership audit: **960 relevant sites, zero direct permission failures**.
- Naval-capability synchronization: **PASS**.
- `git diff --check`: **PASS** (line-ending warnings only).

`sync_civ_strategies.py` reports six pre-existing generated civilization files
which it would update. They were not written because they are unrelated to this
causal patch.

## Runtime acceptance

A fresh replay carrying marker `RAWAI-P3B44T43:491` must show:

1. an AI with a completed own Market and a living ally's Market emits `trade
   land candidate ally`;
2. it produces no more than three Cart probes until a Cart is observed in
   `actionid-trade`;
3. a viable route emits `merchant land proof ally` and permits bounded normal
   Cart growth;
4. an unreachable candidate remains capped at three and does not trigger
   retirement or full growth;
5. water discovery and proof continue independently.

Until those conditions are observed, land trade is not CLOSED.

## Deployment identity

Source marker: `RAWAI-P3B44T43:491`. The installed test copy remains exact
T41:489 with aggregate SHA-256
`AB2271FA659CC47F6471CA950006FF73F986918D71057C12DD90BED099A858F2`.

