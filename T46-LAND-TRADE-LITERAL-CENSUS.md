# T46 land-trade literal allied-Market census

**CLOSED — RUNTIME PASS.** Deployed with T47:495 and accepted from the complete
T47 replay.

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

The complete T47:495 replay
`SP Replay v101.103.48987.0 @2026.09.05 153105.aoe2record` runs 49:32 with zero
parser errors. The user directly observed the restored Trade Carts. Replay
analysis confirms 124 autonomous Trade Cart (`128`) train orders across all
eight players. Seven players exceed the three-Cart candidate ceiling; current
source permits that growth only after observing live `actionid-trade`. Player 8
remains at exactly three, demonstrating the unproven-route ceiling.

Player 1's visible self-channel telemetry identifies Players 2, 3 and 4 as
actual allied Market candidates, then records 134 live land-trade proofs for
Player 4. It produces 26 Carts from two Markets. The other players' private
self-channel proof messages are not replay-visible, but their growth beyond
three is direct behavioral proof that the identical proof gate passed. The
water fallback remains independent: Player 2 also issues two Trade Cog train
orders.

All acceptance criteria are satisfied. The previously absent land-trade
behavior is **CLOSED**. The installed test copy remains the byte-verified
T47:495 aggregate at SHA-256
`9800DEF42ED21A3A46729713DEA02B46849E898DE8C47D7FEA444D57C0F4061B`.
