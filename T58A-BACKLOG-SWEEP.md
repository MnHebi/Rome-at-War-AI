# T58A/507: additional all-player backlog assessment

2026-09-12. Supplements, rather than replaces, `T58A-RUNTIME-REPLAY-ASSESSMENT.md`.
The prior assessment compared all-player transport records but did not complete
a fresh Shipyard/help/ROW/production assessment. Pending labels were not adequate
substitutes for examining available evidence.

Source: completed replay133042, SHA256
`ff2dba2e61952b3cf4ed630901188d73e63b9a4f04ae57be674f7b484e20280e`;
existing exact/broad extracts with zero recorded parser failures. Reproducible
read-only sweep: workspace `.analysis/t58a_backlog.py`. The raw artifacts remain
outside Git. MAKE means production order, not birth; BUILD means issued request,
not completed construction. Diagnostic542=2 is the Shipyard ready confirmation.

## Shipyards: construction works, timeliness remains unresolved

| Player | First recorded ready | Ready confirmations | Build orders |
|---|---|---:|---:|
|1 Blue|40:45|2|2|
|2 Red|44:21|5|6|
|3 Green|42:46|2|2|
|4 Yellow|50:42|6|6|
|5 Cyan|43:20|2|2|
|6 Purple|14:49|2|2|
|7 Gray|50:44|5|6|
|8 Orange|28:48|3|3|

All eight have ready confirmations; these are not simultaneous surviving counts.
Most first completions remain late. Gray and Red's final issued foundations lack
a corresponding ready sample; that alone does not distinguish loss, incomplete
construction, or diagnostic exhaustion. Prior coastal-quality/timeliness defect
remains open. Next: compare first admission/affordability to candidate and build
timestamps, then spatially evaluate rejected coastal sectors. Do not call late
construction a placement-quality PASS merely because it eventually succeeds.

## Merchant right-of-way: no recorded clearing operation

No player emitted actual merchant-move IDs420/421. Rejection623 is predominantly
8 (2,055 samples across players): source rejects an empty, ungrouped Transport.
There are also20 reason4 samples. These are repeated samples, not distinct hull
episodes. No holding-point rejection625 was captured. This establishes lack of
recorded ROW intervention, not proof that every observed candidate was congested.
Next: correlate loaded priority-hull no-progress windows with selected/rejected
hull IDs and nearby self-owned merchants. Do not weaken safety or move ships
merely from this aggregate.

## Help calls: no verified-help episode in recovered chat

No312–317 verification/balance records or help/relief messages were recovered for
any player. Raw CHAT was also checked for312, not only paired diagnostic output.
The broad extract contains14 FLARE packets, but generic flares do not establish
the AI help-request path. This does not validate the help fix. Exact attacked
asset, hostile and responder state are still needed to distinguish verifier
failure from nonqualification. No new help behavior patch is justified yet.

## Production and land trade: positive but bounded evidence

Skirmisher-family MAKE orders by player1–8:63,246,209,35,199,171,209,123.
Purple's171 are138 ranged Mounted Skirmishers and33 stable Mounted Skirmishers;
the other players' counts use unit7. All eight therefore request relevant units.
Births, threat matching, ratios and battlefield use still need verification.

Trade Cart128 MAKE orders by player1–8:94,28,26,101,82,115,102,41.
Blue emits251 `merchant land proof ally` messages. Other players' production is
not itself live-trade proof. Land trading is no longer universally absent, but
these counters do not establish income or route health for every player.

## Floods remain important, not background noise

Fresh full MainLog scan (374,667,099bytes): invalid age2=4,156,519;
age1=3,836,427; age0=84,255; invalid goal0=166,522; invalid object returning-2=
115,969; invalid focus-player-1=6,578; adding invalid object-1=360. These messages
lack writer/player attribution. Do not claim the identity repair fixes them.

AI_ORDER706 packet counts by player1–8:
745,1925,1023,688,919,1023,20142,915. Gray dominates. Its actor34568 appears in
5,004 singleton706 packets and4,158 four-actor packets. This identifies a priority
onset investigation;706 alone is not proof of a particular PER STOP writer.

Separate native ORDER tuples also flood. Gray36145→43279 occurs12,516 times
from56:42.984 to61:18.421; Red35950→7630 occurs5,004 times from64:21.105 to66:22.159.
Green34526→34971 occurs1,994 times from48:33.124 to49:05.740, including693 adjacent
13ms gaps. Do not conflate native ORDER repetition with scripted706 issuance.
Actor type/current ownership and first-onset writer causality remain unproven
for these tuples.507's broken player label means the file log cannot provide
reliable all-player attribution; the local508 identity repair is not deployed.

No579 migration drop-site outcome was recovered for any player; that code uses
self-chat, so absence is especially weak evidence. Mining lifecycle messages in
other players do not prove colony foundation completion or productive deposits.
Yellow's eight full manifests without dispatch and Gray's three preparation/
planner-no-opponent failures remain separate unresolved transport findings.

No runtime backlog defect is CLOSED by this sweep. Immediate evidence priorities:
operand-error experiment and correctly attributed first flood onset; Shipyard
admission-to-foundation timing; help-verifier qualification; ROW selection versus
real congestion; migration productivity and failed landing-candidate geometry.
