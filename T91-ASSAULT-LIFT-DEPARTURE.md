# T91 - loaded attack transports that do not depart (515 candidate)

Evidence: replay `SP Replay v101.103.48987.0 @2026.09.20 190351` (marker 513) with
its 19:48:53 autosave. Analysis scripts and caches live in `.analysis`
(`t88*`). Nothing in this report is deployed; the installed runtime is the 514
payload (`T84-LADEN-BOARDING-ADMISSION.md`).

## Observed

* Attack-lift hulls are Transport Ships (545); their manifests are Levy Spearman
  (93), Scout Cavalry (448) and Battering Ram (1258), resolved from the autosave.
* Healthy lifts seal and sail tightly: `assault ready`/`attack load partial` ->
  move order 68-84 s later; `landing path clear` -> 21.8 s.
* Eight `attack load abort` terminals reported **0, 0, 2, 3, 3, 0, 0, 4**
  soldiers aboard (`attack load garrison`) against a target of 10 and the >=5
  partial floor, while the two successful partials reported 7 and 8.
* During each wait the lift re-issued boarding orders (`SPECIAL`, order 5, target
  = hull) every ~4 s to a **rotating** subset: 10-18 distinct units, single units
  re-ordered up to 47 times, first and last packet unit sets disjoint.
* After the abort, five hulls received only unload orders - repeating UNGARRISON
  at two alternating points (~15 s cadence, the abort origin and the home anchor)
  and **no MOVE** - so they stayed parked with their remaining passengers (final
  positions 54518 (184,186), 44090 (185,89), 36098 (46,171)); two others (62201,
  49121) happened to receive a MOVE and recovered.
* Not implicated: the screen/ROW layers (zero `assault hold` / `screening bypass`
  messages; RAW3 messages only at the second a hull moves) and berth-clearing
  (only 57618 was quarantined, after its abort).

## Change (two independent patches)

1. **Abort terminal returns the hull** (`rawai-military.per`, site 1705). The
   ABORT terminal ordered `action-unload` at the route origin, which the packets
   show never becoming movement; the empty-hull branch already moves home (site
   1716). The terminal now returns the hull to its berth with `action-move`,
   handing it to the berth/clear owner for the bounded local unload.
2. **Entering soldiers barred from the attack boarding list** (sites 1692, 1694,
   1697, 1698, 1699, 1700, 1706). They gain the stock-AI
   `actionid-enter`/`orderid-enter` guard already used by every migration
   passenger selection (`ba4a77c`); the siege round-robin keeps its per-engine
   index selection ahead of the guard so only an already-entering engine is
   skipped.

Protected: partial-load acceptance (>=5 sails), the 300 s unscreened travel
deadline, screen/ROW ownership, quarantine single-slot semantics, the 514 laden
admission rule, 512 latch, 513 hunter floor, taunt fix and operand repair.

## Validation and acceptance

Static: boarding/migration/transport/assault suites 198 OK (including a loader
that executes the abort terminal and asserts a move with no in-place unload, and
a regression asserting the guard on every attack boarding selection);
file-trace/command-boundary 31 OK; `validate_per` `{}`; capacity 9,394/10,000;
strings 1,498/1,500; `git diff --check` clean. A 514 defect was exposed here
too: the ownership harness had no `object-data-carry` fixture field, now added
with a laden-passenger assertion.

Runtime acceptance (needs a 515 deployment): every `attack load abort` is
followed within the bound by a move order or arrival home; no hull is left with
zero packets after an abort; the abort count falls and `assault ready`/partial
rises; lifts whose group boarded reach >=5 at the deadline; no reduction in
successful departures.
