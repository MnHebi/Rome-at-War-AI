# T53 runtime replay assessment

## Runtime identity

- Replay: `SP Replay v101.103.48987.0 @2026.09.06 173242.aoe2record`
- SHA-256: `685833c635b61e8d880ba1a0c04955fac73d1f314ef011e2dfaa20c40dc617bd`
- Duration: 60:03
- Settings: Extreme, population 400, speed 1.69, shared exploration
- Replay-visible marker: `RAWAI-P3B44T53:501`
- Deployed behavioral source: `ea3e146`
- Parser errors: none

The replay is evidence for the deployed T53 runtime only. The two fixes below
were committed afterward and have not been deployed.

## Allied help silence

### Runtime result

The replay contains no allied help request and no existing help-request
diagnostic IDs 300-311. This corroborates the user's direct observation that an
AI under overwhelming attack remained silent. The deployed runtime did not log
verifier detection or request suppression, so the replay alone cannot identify
which old gate discarded each attack episode.

### First source-visible causal boundaries

The deployed help pipeline combined three incompatible lifetimes/scopes:

1. Exact attack verification produced `gl-self-attack-verified` as a one-pass
   pulse and reset it every verifier pass.
2. The local-response consumer required an unrelated ten-second
   `t-defense-leash` trigger on that same pass. A real verified attack could
   therefore disappear before local assessment ran.
3. The request policy used the team-wide `military-superiority` estimate or the
   old local responder goal, while initializing the exact attack to one threat.
   A strong allied army elsewhere could suppress a locally overwhelmed player,
   and the responder count did not have to describe the newly verified episode.

The exact hostile-action/target/victim identity verifier introduced in T13 is
retained; the repair changes the event lifetime and local balance assessment,
not the definition of an attack.

### Repair

Commit `0e1a83b`:

- persists a continuously refreshed exact verified-attack episode for 24 game
  seconds so the chat cooldown and defense controller can consume it;
- removes the unrelated defense-leash coincidence from exact local-response
  admission;
- counts current hostile and self-owned mobile military within 48 tiles of the
  exact attacked asset and its map zone;
- requests help when the existing team comparison is inferior/tolerable **or**
  local threats outnumber local responders;
- adds one bounded identity sample (312-315) and one bounded balance sample
  (316-317) per continuous verified episode.

Status: **FIXED-PENDING-RUNTIME**.

Runtime acceptance requires an exact verified episode to emit 312-317 and a
help request when threats exceed local responders, while locally adequate
episodes remain silent and the old false ally reports do not return.

## Assault shores without usable land egress

### Runtime result

The replay contains several successful planner lifecycles, so the existing
assault system must be preserved:

- Blue hull 42443 committed at 46:15 and landed at 47:03, then was reused and
  landed again at 54:28.
- Blue hull 52521 committed at 56:21 and landed at 57:49.
- Yellow hull 35807 committed at 58:20 and landed at 59:24.

It also contains a failed accepted route: Blue hull 37150 committed at 48:01,
reported obstruction at 48:49, no progress at 49:37, and returned empty at
49:45. This is consistent with the reported cliff-bound/unusable approach, but
the replay packets cannot by themselves prove the terrain route available to
land units.

### Source-proven missing gate

The planner selected the Transport and performed both candidate checks from
that hull:

```text
Transport -> exact water point
Transport -> unload vicinity
```

`up-path-distance` measures from the selected target object. Consequently,
these checks prove only that the ship can reach water and an unload vicinity.
The planner had no query proving that a landed unit could travel from that
shore toward the selected enemy objective. Same map-zone identity was not a
substitute for an actual path across cliff/wall geometry.

### Repair

Commit `64d7e02` keeps every existing hull, zone, failed-shore memory, danger,
screen, objective and enemy-rotation gate, then adds one admission condition:

- gather visible enemy Villagers or mobile military within 80 tiles of the
  selected objective and on its exact land zone;
- sort them by distance to the proposed landing;
- require at least one of the nearest three to have a finite land path to that
  landing;
- if all available witnesses fail, record reason 41 and feed the candidate into
  the existing failed-shore/alternative-approach search;
- if no mobile witness exists, retain the old bounded structure-only cleanup
  fallback instead of making late-game cleanup impossible.

The patch issues no unit command and does not alter dispatched assault slots.

Status: **FIXED-PENDING-RUNTIME**.

Runtime acceptance requires reason 41 to reject a cliff-pocket/unconnected
candidate, selection of a materially different usable shore/objective, and a
landed group that can advance toward its objective. Existing successful
assaults and structure-only cleanup must continue.

## T53 Villager order-706 experiment

The replay contains 5,921 order-706 actor incidences across 1,323 actors, but
the nine instrumented home-economy retasks all had zero order-706 packets in
both their 30-second pre- and post-command windows. Several had much later
recurrence, and the two largest individual streams were unsampled: player 6
actor 35359 (182) and player 1 actor 7734 (105).

This replay therefore does not accept or reject the Ctrl experiment. It did not
sample a writer while that same actor was flooding. `villager.order706` remains
**INVESTIGATING** and `villager.keystates.t53` remains an independently
revertible experiment pending a discriminating runtime sample.

## Validation and deployment state

- Help focused test: 10/10 PASS.
- Assault planner focused test: 29/29 PASS.
- Shoreline resolver focused test: 12/12 PASS.
- Validator suite: 128/128 PASS.
- Full Python 3.12 discovery: 563/563 PASS.
- PER structure/operand validation: PASS.
- Generated assault source synchronization: PASS.
- Ownership audit: 1,031 relevant sites, zero direct failures.
- Strategy execution: 1,156 matchups, zero errors.
- Naval doctrine, 42 replay-benchmark records, and context metadata: PASS.
- The read-only strategy synchronizer still reports the six documented,
  pre-existing civilization-file drifts; this task did not regenerate them.
- `git diff --check`: PASS.
- New fixes deployed: **NO**.
