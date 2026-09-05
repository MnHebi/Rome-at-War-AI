# T40 naval / overseas hardening — source only

Canonical checkout: `G:\Projects\Codex\Rome at War AI\.trade-work\T30-trade-cap-civ-fix`,
branch `fix/trade-cog-cap-dacian`, baseline `4d9c519` (T39). No deployment.
The latest explicit user instruction supersedes the obsolete `.pr-work` path
in the general project rules. No branch or worktree was created.

## Shipyards — FIXED-PENDING-RUNTIME

**Evidence / boundary.** User reports late/missing yards and congested inlets.
The original 155-line `rawai-specialplacement.per` bypassed tech saving only
for the first yard. Its final build gate also required `total < desired`, so
the apparent first-yard priority could not actually issue when the current
civilization phase still requested zero yards. Later yards had no persistent
minimum-capacity escape from `wait-techup-requirements`. Placement randomly
offset the newest naval building by roughly 14 tiles, checked buildability and
7-tile building clearance, then reset to IDLE on `up-build-line` issuance.
There was no water-exit test or concrete-foundation/completion check.

**Change.** Preserve early-age/Port/250-wood first-yard admission, including its
intended one-yard exception to a zero phase target. A 90-game-second deficit
below `min(desired, 2)` can bypass only tech saving, never affordability or
escrow. Later expansion retains ordinary saving policy. Lake 4 / Rivers 6 caps
and all civilization phase targets remain unchanged. No escrow is released.
Twenty-four deterministic coastal offsets extend to 40 tiles, with rotating
naval anchors and four exit orientations. Each accepted orientation requires
four open exact-path water points in the real nearby ship's water zone, ten
tiles from existing naval buildings, plus a free nearby worker with a bounded
vicinity path. Queries use mobile ships/workers, never buildings. Four failed
sectors expire after 180 seconds. A build remains pending for 24 seconds until
the actual own Shipyard object appears within two tiles, then is watched for
completion for at most 180 seconds. Failure is not counted as completion.
One rate-limited reason transition (diagnostic ID 410) distinguishes cost,
pending placement, foundation loss, worker hold, tech hold and coastline failure.

**Authority.** Cached AIRef `airef-reference-20260830.js`: `up-path-distance`
option 1 requires an open exact tile; option 0 allows vicinity. Point pairs are
bounded without substituting a clipped point. `up-build-line` is an issuance,
not a guarantee that a foundation exists. Native `up-assign-builders shipyard 4`
is preserved; the eligible worker path is admission evidence, not a promise
that the native engine assigns that particular worker. No worker is stolen
from a protected DUC group and no global task/reset/percentage is changed.

**Validation.** PASS: 9 executable-PER fixtures, 126 general validator tests,
PER structural validation, ownership audit (849 sites, zero permission failures).
Tests cover high-priority first yard, persistent second yard, later saving/caps,
no false foundation success, four-probe crevices, building separation, missing
or owned/unreachable worker, and finite distributed candidate enumeration.

**Runtime acceptance / uncertainty.** Still required: first yard completion,
minimum operational count despite prolonged tech saving, actual open exits and
adequate sector coverage on Iberia and islands, ordinary expansion restraint,
native worker assignment/completion, pending-queue behavior and no regression in
transport/fishing/Port traffic. Four sampled open points are a bounded quality
heuristic, not a proof of a wide corridor everywhere. Rejected candidates/no
nearby probing ship may still delay placement; the reason remains observable.

## Merchant right-of-way and expedition throughput

INVESTIGATING in this turn. Neither implementation nor runtime acceptance has
yet been claimed for these items.
