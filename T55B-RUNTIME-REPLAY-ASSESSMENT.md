# T55 second replay — 2026-09-07 12:14:39

Follow-up: `T55B-CAUSAL-INVESTIGATION.md` supersedes causal uncertainties below
where stated. It inspects actual candidate footprints and exact hull/worker
commands. Blue49162 completion is independently corroborated by the52:50
completed-count snapshot; the exact ready event is still missing. Corrected
actor-array decoding is required for AI_ORDER/UNGARRISON joins.

## Identity and limits

Replay `SP Replay v101.103.48987.0 @2026.09.07 121439.aoe2record`:
SHA-256 `632D89F42B339B06E6B83EF9A58F1FE7855EED9DB22DD3A200B2DDDA4A005858`.
Duration **114:19**, no parse errors. Marker **T55:503**; current installed
99-file runtime equals source `1f87ef0`, aggregate SHA-256
`6EE2AC23972B252500C62F9961D51E6C0C42956F4DA52125C5B487F87229D86C`.
Same nominal settings: Extreme, population 400, speed 1.69, shared exploration,
map ID 49, 220x220 terrain. Not an identical-seed control for the earlier game.

Analysis checkout: `.trade-work/T30-trade-cap-civ-fix`, branch
`fix/trade-cog-cap-dacian`, HEAD `6f1d31a`. Earlier T55 report/context edits
were already uncommitted and were preserved. No runtime/source behavior changed.

External artifacts under workspace `.analysis`:

- `replay-20260907-121439-t55-full.json`: complete decoded actions/chats.
- `t55b-shipyard-sites/`: rejection CSV, summary and per-player map overlays.
- `t55b-episodes.json`: Shipyard snapshots, foundations, plan records,
  mission events and exact-stream Ctrl/706 correlation.
- `summarize_t55b.py`: reproduction script, using repository parsers.

Evidence distinguishes issued commands, scripted state reports and actual engine
outcomes. A landed event does not prove traversable land or productive combat.
Self-only diagnostics do not provide equal coverage for all players.

## 1. Shipyards — expansion works, delay remains

**24 build orders, 24 concrete foundations, 23 recorded ready events.**
Seven players build yards; Purple does not.

| Player | Orders | Recorded ready | First order | First recorded ready | Later ready times |
|---|---:|---:|---|---|---|
| Blue | 2 | 1 | 51:22 | 55:06 | — |
| Red | 4 | 4 | 55:16 | 55:58 | 57:56, 59:35, 83:36 |
| Green | 2 | 2 | 48:02 | 48:49 | 50:19 |
| Yellow | 6 | 6 | 27:47 | 28:19 | 54:01, 57:03, 57:46, 60:57, 80:00 |
| Cyan | 2 | 2 | 23:01 | 23:36 | 81:32 |
| Purple | 0 | 0 | — | — | — |
| Gray | 6 | 6 | 41:05 | 41:39 | 43:36, 47:39, 50:20, 59:22, 69:51 |
| Orange | 2 | 2 | 14:03 | 14:30 | 28:35 |

These are cumulative events, not end-of-match surviving counts. Blue foundation
49162 appears at 51:22 without a recorded ready event; do not label it completed
or destroyed. Blue's second, 52881, completes at 55:06. Other ready events join
the exact foundation identities. Four yards are ready by the preceding replay's
34:11 cutoff, versus three there; that is descriptive, not controlled causality.

### Placement quality and remaining rejection work

There are 16,376 complete rejection records, of which 15,082 are reason 64:

| Initial-terrain class | Count | Share |
|---|---:|---:|
| Land center | 5,226 | 34.7% |
| Water without nearby shore in 5x5 | 3,317 | 22.0% |
| Coastal/mixed, unresolved | 6,539 | 43.4% |

Thus **56.6%** still miss plausible coast, versus 57.9% in the first T55 run and
84.4% in T54. The shoreline preference improves the rejected-sample distribution
but does not eliminate waste. These samples are not every cheap random draw.

Every issued point is classified coastal/mixed on initial terrain. Inspection of
Red, Cyan and Orange overlays shows the issued yards along outer coasts rather
than deep inside the central inlets. This does not validate dynamic building
clearance, actual ship exit paths or congestion. Red and Cyan repeatedly sample
limited coastal sectors; good-looking terrain does not explain their rejected
buildability checks by itself.

### Affordability is not the whole explanation

| Player | Deficit snapshots | Affordable | Unaffordable |
|---|---:|---:|---:|
| Blue | 44 | 6 | 38 |
| Red | 88 | 56 | 32 |
| Green | 39 | 1 | 38 |
| Yellow | 62 | 25 | 37 |
| Cyan | 90 | 39 | 51 |
| Purple | 51 | 0 | 51 |
| Gray | 62 | 13 | 49 |
| Orange | 18 | 0 | 18 |

Across 554 snapshots, 414 are unaffordable and 140 affordable. As in the previous
assessment, this means resources outside escrow, not a prerequisite test.
Periodic samples miss intervening opportunities (Orange builds twice despite
all its sampled deficit checks being false). Purple's sampled gate remains
resource-related; Red/Cyan plainly also encounter placement/other admission
boundaries when affordable. Do not carry forward the short replay's resource-only
emphasis as an explanation of all delay.

**Acceptance: PARTIAL, not CLOSED.** Preserve successful multi-yard expansion
and the full placement gates. Next reconstruct affordable deficit intervals
against anchor/candidate/issue state, particularly Red and Cyan; keep Blue's
unconfirmed first foundation explicit. No broad resource-policy change justified.

## 2. Assault lifecycle — Cyan watchdog failures dominate

Recorded private-slot commits: **19** (Green 1, Cyan 10, Gray 8).
Recorded landed events: **7** (Green 1, Cyan 1, Gray 5).
Gray also has combat-target activity after its 60:00 commit without a recorded
event 8, so 7/19 must not be presented as an exact physical landing success rate.
Blue, Red and Yellow have preparation activity but no recorded slot commit;
Purple and Orange have none. Preparation events 23/24 are rendezvous and local
boarding admission, not voyage failures or successful departures.

### Cyan's seven no-progress episodes

| Slot | Hull | Commit | Event 4: no progress |
|---|---:|---|---|
| 1 | 35241 | 43:24 | 45:00 |
| 1 | 35302 | 46:12 | 47:48 |
| 1 | 35241 | 48:14 | 49:50 |
| 2 | 35302 | 49:31 | 51:07 |
| 3 | 35461 | 55:27 | 57:03 |
| 1 | 35241 | 80:02 | 81:38 |
| 1 | 35241 | 108:17 | 109:53 |

Each terminates outbound progress **96 seconds after commit**. Source initializes
the progress deadline to 90 seconds and samples every eight seconds. This is
consistent with the watchdog firing without useful recorded progress, not proof
that traffic, a bad waypoint or command interference caused the stall.
Two other Cyan missions report hostile fire; its last commit at 109:15 lands at
110:19 and produces seven combat-target events. Five Cyan quarantine events
follow recovery timeouts. In particular, hull 35241 later returns empty at
79:04 after its earlier quarantine: bounded release of preparation ownership
does not guarantee prompt recovery of the loaded physical ship.

Gray has two hostile-fire recoveries, five recorded landed events, 31 combat
target events and six combat releases. Green lands at 38:35 but releases combat
at 38:51 without a combat-target event: productive land continuation is unproven
for that group. Do not classify its release as success merely from unloading.

### Exact land-witness check is exercised

Four recorded reason-41 rejections:

| Player | Time | Hull | Objective | Rejected landing |
|---|---|---:|---:|---|
| Gray | 84:17 | 46207 | 46729 | 61,164 |
| Blue | 100:23 | 35373 | 7779 | 58,185 |
| Gray | 101:00 | 52377 | 7750 | 58,170 |
| Green | 106:07 | 36323 | 7779 | 37,190 |

Gray hull 46207 subsequently commits at 85:22 and lands at 86:18; hull 52377
commits at 101:07 and lands at 101:39. This supports rejection followed by
continued planning, rather than automatic destruction of the loaded mission.
It does not prove the actual unload tiles have an autonomous route to the target.

Of 121 bounded accepted-candidate records, **68 have a witness and 53 have
witness -1**. The no-visible-witness fallback remains a substantial unproven
path, not an exceptional theoretical concern. These are samples, not unique
missions. Broader shore-egress status remains **INVESTIGATING**.

## 3. Order-706 flood persists

Exact packet decoding finds **38,850 actor incidences** of subtype 706.
Cyan actor **43834** accounts for **8,823**, from **92:29.578 to 96:10.911**
(about 39.9/sec over that interval). It previously received a House build at
50:22 and is later the expedition worker identity (diagnostic 603) at 97:46:
this ties the lead to a worker, not an unidentified warship.

Other high totals: Gray 35144 (2,804), 35104 (2,230), 35670 (2,083), and
Cyan 34893 (2,040). Totals over long intervals are not uniform rates.
The 235,169 ORDER and 1,055 explicit STOP packets are separate packet families.

All **15** instrumented Ctrl-retask samples belong to Blue and have zero 706
packets in both their preceding and following 30-second windows. This does not
test the active Cyan/Gray floods. **Ctrl experiment INCONCLUSIVE; flood OPEN.**
Next attribute the exact first onset for 43834 at 92:29.578 against the reserved
writer records and command history; do not claim that aggregate reduction or
quiet sampled actors validate the experiment.

## 4. Other outstanding issues

- **Help:** no help requests or diagnostics 312–317 appear. Verification remains
  unproven; this is not a pass for silence. The missing exact-episode records
  locate the evidence gap upstream of request cooldown. Establish a concrete
  attack/victim episode before changing the verifier again.
- **Migration:** preparation/partial-load/terminal activity is present (37
  terminal-phase reports). No captured code-579 ready lifecycle proves a
  productive colony. Self-only diagnostic coverage limits negative conclusions
  for players other than Blue. Do not equate missing ready telemetry with every
  player's failed drop-site construction.
- **ROW:** no 631–637 merchant-clearance issuance records. Those are broadcast,
  so the recorded run provides no successful policy-issued yield episode.
  Cyan's repeated stalled voyages make this a relevant unresolved boundary,
  but do not alone prove nearby merchants caused them.
- **Expedition:** source emits blocker/slot state. For Cyan at 97:46 all three
  slots report state 4 (quarantine), with blocker 7. Diagnose physical recovery
  and admission before increasing strategic commitment or slot capacity.

## Disposition

Retain T55's working multi-yard expansion and exercised exact-witness rejection.
No gameplay behavior is CLOSED by this assessment. Highest discriminating leads:
affordable-but-unsuccessful placement (Red/Cyan), Cyan's repeat 96-second voyage
stalls, and worker 43834's precise flood onset. No deployment, policy tuning or
new tracing runtime was performed for this replay analysis.
