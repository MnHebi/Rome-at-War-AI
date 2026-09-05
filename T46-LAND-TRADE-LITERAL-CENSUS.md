# T46 land-trade literal allied-Market census

**ROOT-CAUSE-PROVEN / FIXED-PENDING-RUNTIME.** Deployed with T47:495.

## Runtime evidence

The current live T45:493 match directly shows Blue producing Merchant Ships but
no visible Trade Carts. This is a runtime failure of T43's land-trade acceptance,
not proof that the independent water branch is unhealthy. Merchant Ships may be
created by the bounded fallback after three topology failures, so their presence
does not prove that the allied-player candidate iterator succeeded.

The earlier complete T41 replay already supplies the matching lifecycle:
completed own and allied Markets, no `trade land candidate ally` event, no Trade
Cart for any player, and repeated `trade topology no candidate` events.

## First remaining causal divergence

T43 repaired the local Market source boundary, allowing
`TRADE-ROUTE-LAND-SOURCE` to execute. Its next action was still:

```text
up-find-player ally find-ordered gl-trade-route-player
```

The cached DE AI reference's known-issues entry records that `find-ordered`
returns `-1`. That invalid player becomes the focus owner for the remote Market
scan, before any land-candidate mask bit can be set.

There was a second invalid boundary in the same candidate census: LAND-START
built `search-remote`, restored focus, and LAND-CHECK consumed that shared list
on a later rule sweep. The project already established with T43 that DUC lists
cannot safely carry controller state across such a boundary. The T43 focused
test covered only its repaired local list and accidentally required the remote
dependency to remain.

## Bounded correction

- Walk literal player slots 1 through 8 instead of using the broken ordered
  iterator.
- Admit only a non-self, in-game ally for a remote Market census.
- In one rule, set the literal focus, find the ally's Markets, read
  `remote-total`, persist it in `gl-trade-valid-producer-total`, restore the
  prior focus, and enter LAND-CHECK.
- Consume only that persistent count in LAND-CHECK. Empty, non-allied, self,
  and inactive slots take a zero-count fallthrough.
- Advance exactly eight slots, then continue into the independent water scan.

The change does not alter Cart resource gates, `wait-techup-requirements`,
`can-train`, the three-Cart candidate probe ceiling, live `actionid-trade`
proof, normal trade growth, retirement, Market epochs, or water trade.

## Validation

PASS:

- trade topology: 10/10;
- T13 gate recovery: 7/7;
- validators: 128/128;
- full Python 3.12 discovery: 512/512;
- PER structure and operand validation;
- naval doctrine and strategy execution;
- generated naval doctrine/capability synchronization;
- ownership audit: 969 relevant sites, zero permission failures;
- `git diff --check`.

Behavioral commit: `6daa09c`.

## Runtime acceptance

A fresh marker-495 replay must show:

1. `trade land candidate ally` for an actual allied Market owner;
2. one to three autonomous Trade Cart probes;
3. live `merchant land proof ally` when the engine finds a usable route;
4. normal bounded Cart growth only after that proof;
5. water discovery/fallback still operating independently.

Until then the gameplay defect remains **FIXED-PENDING-RUNTIME**. The installed
test copy contains the 99-file T47:495 aggregate, byte-identical to source at
SHA-256
`9800DEF42ED21A3A46729713DEA02B46849E898DE8C47D7FEA444D57C0F4061B`.
