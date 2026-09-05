# T45 three-stage perimeter gates

## Status

**ROOT-CAUSE-PROVEN / FIXED-PENDING-RUNTIME.** This is an explicitly requested
wall policy change. No deployment was performed.

## Evidence and source boundary

The user directly observed Yellow heavily choked behind a completed visible
wall with only one gate. Part of that perimeter entered water, so the engine's
wall completion fact never reached the late gate-admission threshold.

Current source confirmed two deterministic blockers:

- the controller's perimeter-owned quota stopped at two gates;
- the second gate required `wall-completed-percentage 2 >= 75`.

Therefore any perimeter stuck below 75 percent could never request its second
opening, regardless of how complete the usable land wall appeared. A third
opening did not exist in policy at all. The source threshold was 75 percent,
not 70 percent.

The existing first-gate behavior remains valuable and must survive: it requests
the first gate as soon as the engine reports a replaceable perimeter-2 span,
without waiting for a completion percentage.

## Implementation

The perimeter-owned sequence is now:

```text
first replaceable wall span -> gate 1
40% wall completion        -> gate 2
75% wall completion        -> gate 3
```

Both stone and palisade paths implement the same sequence. Each successful
request advances `gl-wall-gates-issued` by exactly one, ending at three. The
40-percent and 75-percent stages each retain the existing 60-second
availability polling, three-attempt limit, and 180-second backoff.

Unchanged safeguards include:

- perimeter-specific ownership rather than global gate counts;
- latched stone/palisade material;
- Town Center, Villager, home-safety, danger, escrow, and availability gates;
- the wall command's separate retry/backoff policy;
- no changes to wall geometry or building placement.

The change does not claim that `build-gate` issuance proves an eventual
completed foundation. No failed-gate-foundation evidence was established in
this observation, so foundation lifecycle work was not broadened into T45.

## Validation

- Focused gate assertions: **PASS** for exactly six material-specific build
  rules; two first-gate rules without a percentage; two second-gate rules at
  exactly 40 percent; and two third-gate rules at 75 percent ending at quota
  three.
- Availability polling/backoff assertions: **PASS** for all three stages.
- Validator suite: **128/128 PASS**.
- Full Python 3.12 discovery: **512/512 PASS** in the permitted temporary-file
  environment.
- PER structure/operands: **PASS**.
- Naval doctrine: **PASS**.
- Strategy execution: **PASS**.
- Ownership audit: **962 relevant sites, zero direct permission failures**.
- `git diff --check`: **PASS** (line-ending warnings only).

## Runtime acceptance

A fresh replay carrying marker `RAWAI-P3B44T45:493` must demonstrate:

1. gate 1 remains eligible at the first replaceable span;
2. a perimeter reaching 40 percent requests gate 2 without waiting for 75;
3. a perimeter reaching 75 percent requests gate 3;
4. no perimeter-owned fourth gate is requested;
5. stone/palisade material, danger, affordability, availability, and bounded
   retry behavior remain intact;
6. land traffic is no longer trapped solely because water-intersecting wall
   segments prevent the late completion threshold.

Until fresh runtime evidence satisfies these conditions, T45 is not CLOSED.

## Identity

Behavioral commit: `1978ac2`. Source marker: `RAWAI-P3B44T45:493`. The installed
test copy remains exact T41:489 with aggregate SHA-256
`AB2271FA659CC47F6471CA950006FF73F986918D71057C12DD90BED099A858F2`.
