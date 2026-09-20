# T68 — 510 runtime results and the crash at 3,633 s

Inputs: `SP Replay v101.103.48987.0 @2026.09.20 120413.aoe2record`
(sha256 `27ebe519ae0ada0e115ba1e43981a90ccf4a32bf8de144976bca392312b84473`) and
`logs\2026.09.20-1200.36\MainLog.txt` (25,405,604 lines, 334,865,530 bytes).
Offline analysis only; nothing installed or launched.

## Identity

The marker `RAWAI-P3B44T58B: 510` appears in the replay (players 6, 7, 8 — the
same three that announce it in the 509 recording). The replay's last event is at
**3,633,275 ms**, identical to the crash report's `WorldTime=3633275`, so the
recording is truncated at the crash instant. There is no resign/defeat/quit
packet: the game did not end, it stopped.

## Did the earlier fixes hold?

| Fix | 509 | 510 | Verdict |
|---|---|---|---|
| Operand repair (named escrow/point goals) | 0 "Invalid goal used" after the repair | **0** in the whole 510 log | holding |
| Taunt-31 acknowledgement (`300dac4`) | site 1829 (`rawai-tauntcommands.per:2`, `(attack-now)`) fired **736** times for p4; the handler re-fired once per AI tick | site 1829 fired **0** times; site 1828 (the acknowledgement itself) fired 44 times match-wide | **fixed** |
| Passenger entering guard (`ba4a77c`) | n/a (not installed) | guarded sites still fire (899 → 908 across the match), and the storms the guard was aimed at persist | **no visible effect** |

The taunt fix is the clear win: the loop that re-fired 184× in 101 s on 509 is
gone. The entering guard changed the selections — boarding calls whose selectees
were already entering dropped from 147 to 77 — but the ORDER storms did not
disappear.

## The storms are still there

99.6 % of the 544,180 ORDER packets fall inside 78 sustained storms (≥150
packets per actor/target). The largest are p7 actors ordered to one object:

| Storm | Packets | Interval |
|---|---|---|
| p7 actor 33602 → 7744 | 34,785 | 2928-3633 s (49/s) |
| p7 actors 33246/33360/34330/34586/33277/33494/33695 → 7744 | 16.6-17.8k each | 2243-3074 s |
| p2 actor 33192 → 34470 (and ~20 more p2 actors) | 13-55k each | — |

Object 7744 is only ever an ORDER target (316,914 packets, all p7) plus 79
`AI_ORDER` packets; 34470 is the same shape for p2. The storming actors' recorded
states are the 509 mix of `enter` (617/717) and gather/hunt (609/709, 613/713),
and each large p7 storm is preceded within a minute by the same boarding writers
(sites 1380/1398) selecting the storm actor.

This match is not a controlled comparison (different lobby, map and players, and
it ran 3,633 s against 509's 4,008 s), so the raw increase from 24 storms to 78
is not a like-for-like regression. What it does show is that the entering guard
did not remove the storm behaviour, which matches the T66 caveat: the
mid-board re-tasking was strongly *associated* with storm onsets, not shown to
cause them.

## What the end of the game shows

- **Every player except p6 was still active at the crash.** p6's last packet is
  at 2,797 s, 836 s before the end — p6 was eliminated early. p1-p5 and p7/p8
  all emit packets within 0-4 s of the crash.
- **The last event is p2's `AI_ORDER` 706 batch** for eight actors at
  3,633,275 ms; p7 is still issuing ORDER packets at 7744 and 49178 in the same
  millisecond. The AI was alive and ordering at the moment of the crash.
- The final 120 s carry 16,047 ORDER, 6,739 AI_ORDER and 11,070 CHAT packets.
  Replay volume peaked earlier (295,607 packets in 2,100-2,400 s) and declined
  to 12,745 in the last partial 300 s bucket, so the crash did not coincide with
  the peak of the traffic.
- **No game-ending event exists in the replay** — no kill-the-king, wonder or
  resignation record.

## Crash forensics

The log ends with:

```
[GetPlayerIsPlatformMuted]/[Banned] pairs ...        (172,520 each over the match)
[AI RAW]: (up-find-remote): Focus player is invalid (-1)          x5
[AI RAW]: (up-remove-objects): Object was invalid, returning -2   x2
[AI RAW]: (up-get-object-target-data): Object was invalid ...     x6
UnhandledExceptionResponse_BugSplat
Writing crash record file.
... WriteCrashAutoSave: Generating autosave...
```

- `Age2CrashReport.txt` contains **no exception type and no stack** — only
  hardware, settings, `WorldTime=3633275`, `LastScreenEntered=widget:dialogscrollanchor`
  and the active mod list. The engine did not record what faulted.
- The engine API complaints are ordinary for a long AI match: 33,942
  `up-get-object-target-data` invalid-object returns, 2,847 invalid focus-player
  returns, 3,103 invalid-object returns from `up-remove-objects` (the first at
  line 13.37 M, i.e. late in the match).
- **One observation worth flagging without attributing**: 25.2 M of the 25.4 M
  log lines (99.2 %) are this mod's own file-trace instrumentation
  (`RAW58P1`..`RAW58P8`), i.e. ~334 MB of log written during one 60-minute
  match. The crash report carries no stack, so nothing here connects that load
  to the fault; it is recorded because it is unusual and because the crash
  handler is the only thing that follows it.
- The newest autosave (`-AUTOSAVE-.aoe2spgame`, 12:39:15) predates the crash by
  about two minutes; the crash-time autosave produced no newer file. A resume
  from that autosave would restart roughly two minutes before the end.

## Not established

- The cause of the crash is **not determined** by the replay or the log: there is
  no exception text, no stack and no failing AI command at the boundary.
- Whether the 510 storms are the same defect as the 509 storms is still
  unresolved — same shape, same writers, different match.
- No gameplay change, no fix and no deployment follows from this analysis.
