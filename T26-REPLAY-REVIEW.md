# T26 replay review and causal fixes

Replay: `SP Replay v101.103.48987.0 @2026.09.01 155609.aoe2record`

SHA-256: `70003C7FD3CFCA8079CB1FE388AF8B89E385DE461E0CE12FF6FEF6304C5B400E`

Runtime: `RAWAI-P3B44T25:473`. Duration 112:09, zero action-stream
parse errors. The user ended the game because neither side could establish an
advantage. The replay and all parsed payloads remain outside this repository.

## Broad transport audit

The all-player command audit reconstructs 47 command-linked Transport hulls,
220 load/unload samples, 38 assault partial/abort terminals and 191 boarding
windows. Per-player hull/boarding-window/load-command totals are:

| Player | Hulls | Boarding windows | Load commands |
|---|---:|---:|---:|
| Red | 6 | 55 | 215 |
| Green | 3 | 11 | 89 |
| Yellow | 7 | 17 | 151 |
| Purple | 1 | 1 | 18 |
| Orange | 6 | 33 | 215 |
| Cyan | 7 | 15 | 110 |
| Blue | 7 | 15 | 126 |
| Gray | 10 | 44 | 320 |

These are reconstructed command lifecycles, not claims that every engine action
completed. Assault telemetry distinguishes the players sharply. Gray owns 31
voyages and confirms 23 landings/combat handoffs. Orange owns 15 voyages and
confirms six landings. Red owns nine voyages but confirms no landing: six end in
hostile damage and three in the ninety-second no-progress path. Green and Purple
never reach an assault-stage record. Yellow accepts four full and one useful
partial assault load, but owns no voyage.

## Source/runtime-proven defects

### Yellow never reaches Blue in overseas target rotation

At 54:18, 61:04, 97:36, 103:45 and 110:55 Yellow has an accepted assault load.
The planner evaluates three opponents and terminates reason 27 each time. The
103:45 hull is the apparently inexplicable Yellow Transport later seen beside a
small resource island. Its plan examines enemy 8 and then enemies 5 and 6; it
never evaluates living enemy 7 (Blue). Source imposed a fixed three-opponent
search cap even though a four-versus-four match can have four living enemies.

Commit `6ce427f` expands only this bounded opponent scan to all seven possible
other player numbers. Existing candidate validation, cooldowns and failure
memory remain unchanged.

Status: **FIXED-PENDING-RUNTIME**. A future accepted Yellow load must either
select a viable fourth opponent and dispatch, or publish a specific rejection
for every living opponent before recall.

### Useful manifests are cut off while correct passengers are still local

The fixed local thirty-second load terminal repeatedly fires with a valid group-4
passenger still garrisoning the exact hull at one to four tiles: Red examples
include 9/10 at distance 3, 5/10 at distance 3, 7/10 at distance 1, and 7/10 at
distance 4. The existing useful-partial threshold correctly preserves the
already boarded army, but the last nearby accepted members are needlessly left
ashore.

Commit `04ff4ca` grants exactly one twelve-second grace only when the remaining
candidate still has the correct group, exact hull target, garrison action/order
and distance at most twelve. A wrong-hull, retasked or distant candidate keeps
the original terminal behavior.

Status: **FIXED-PENDING-RUNTIME**. Near valid passengers must receive at most one
grace interval; all pre-existing partial/abort bounds must remain terminal.

### Near-waypoint migration is recalled without testing its landing

The user's two-villager Red Transport did not alternate between two landing
sites. Hull 38985 improved to ten tiles from one stored route waypoint, then
oscillated between ten and eleven tiles. After four stalls the strict eight-tile
waypoint gate recalled it without invoking the already existing same-zone and
path landing validator.

Commit `84add70` permits only the bounded terminal case at distance twelve or
less to enter that validator. It does not issue an unload, weaken wrong-island
checks or accept an unreachable path; distance thirteen and above still recalls.

Status: **FIXED-PENDING-RUNTIME**.

### A valid first colony foundation request vanishes

Red lands eighteen settlers on zone 14. The controller selects exact point
`(131,199)` and issues its Mining Camp request. At the wait terminal there is no
pending placement, pending object, worker emergency or affordability blocker;
the lead settler is gathering and all eighteen remain reserved. A later Red
migration selects the identical point, immediately creates foundation 67503,
assigns builders and completes it. The first asynchronous request was therefore
lost even though its point and prerequisites were valid.

Commit `a7a6584` revalidates and reissues that same exact point once when and
only when no placement/object exists and no worker emergency is active. A live
pending request is never reset and the original four alternate offsets remain.

Status: **FIXED-PENDING-RUNTIME**. A vanished request receives one retry; no
request may loop or duplicate a live foundation.

### Idle Trade Cogs are invisible to departure congestion

The user's boxed-in Red Transport is corroborated by dense merchant traffic.
Source departure clearance searches Transport Ships and warships, but not the
Trade Cog class. It therefore cannot even classify an idle merchant occupying
the departure corridor. Commit `d326f6a` adds Trade Cogs to the same bounded
search while retaining every safety filter: only self-owned, idle, empty,
ungrouped, safe ships in the same water zone may yield. Active trading, loaded,
grouped or attacked ships are not commandeered.

Status: **FIXED-PENDING-RUNTIME**. This does not claim to solve congestion from
active merchant traffic, allied ships, buildings or non-assault migrations.

### Failed migrations win the shared lane before due assaults

Green records nine full migration loads from 76:06 onward. Most reach a bounded
route or return terminal and then form another migration roughly one recovery
interval later. The existing rejected-zone ring is active; the defect is not a
missing blacklist. Source orders the migration intake before assault intake and
tests only whether the assault state is idle, not whether its timer is already
due. When both timers become ready, migration repeatedly claims the one shared
lane first.

Commit `a24d379` makes migration yield exactly one intake pass when every outer
assault prerequisite is live: the assault timer is due, a slot is open, home
defense is inactive, a Transport exists and a living seed enemy exists. If any
of those conditions is false, migration proceeds normally. If assault planning
rejects the attempt, its own bounded timer resets and the still-due migration
can start on the next sweep.

Status: **FIXED-PENDING-RUNTIME**. Green must receive assault admission
opportunities between failed migrations without suppressing legitimate economy
missions when no assault is viable.

## Diagnostic-only work and unresolved evidence

Green and Purple publish no assault-stage record at all, so the replay cannot
identify their first upstream blocker. Commit `e1c9dde` adds transition-only,
one-minute admission diagnostics using existing generic strings. It reports an
outer blocker mask and the last lifecycle stage/time; it issues no unit order or
gameplay mutation. This is **DIAGNOSTIC ONLY**.

After 90:00 Yellow issues no decoded AI attack order. Green issues 1,303 and
Purple 756, so their visible idle formations do not prove global command silence.
The ownership/target of those formations remains **INVESTIGATING** pending the
new admission record and a fresh replay.

Red's nine owned assaults all fail, but positive hostile damage and pure voyage
non-progress are distinct terminal classes. This review does not relax danger
vetoes or guess that all failures are congestion. Gray's 23 successful landings
on the same map are a non-regression control.

## T26 acceptance

- Verify `RAWAI-P3B44T26:474` and full installed/source byte identity.
- Audit every player and every Transport lifecycle on the next map.
- Require fourth-opponent evaluation, one-shot local boarding grace, bounded
  near-waypoint landing validation, one-shot foundation retry, idle-Trade-Cog
  clearance and assault opportunities between failed migrations.
- Preserve Gray's high successful-landing rate, useful partial manifests,
  wrong-zone/path vetoes, active Trade routes, three independent assault slots
  and known-danger retreat.
- Use admission IDs 400-402 to establish why any player which remains silent
  never reaches mission formation; telemetry is not closure of that defect.

