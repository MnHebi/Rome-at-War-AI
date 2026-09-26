# T66 — attribution of the three sustained ORDER storms (509 recording)

Offline only: the corrected T62 correlator (`tools/command_contracts.py` +
`tools/command_boundary_log.py`) run over the frozen 509 identity, registry and
records (`.analysis/deployment-t63-509-…/`, `.analysis/t64-509-file-trace.records.jsonl`).
No runtime change, no deployment, no new logger. The installed payload remains
509 and `300dac4`'s taunt fix is untouched.

## 1. The storms (exact intervals and target fields)

| Storm | ORDER packets | Interval | Target | Target coordinates in the packets | Target observed elsewhere |
|---|---|---|---|---|---|
| Red p2 actor 7806 | 12,323 | 3655-3959 s | 53139 | constant 31,104 | **only** ever an ORDER target (26,188×, all p2); never appears as an object in any packet |
| Red p2 actor 34426 | 12,312 | 3655-3959 s | 53139 | constant 31,104 | as above (same episode) |
| Yellow p4 actor 34824 | 16,544* | 3358-3700 s | 7754 | constant 189,204 | ORDER target 16,549× (all p4) **and** object of 130 p4 AI_ORDER packets at x/y = -1 |

*The earlier 12,744 figure came from the flood-run detector's grouping; the raw
count for this actor/target over the interval is 16,544. Red's two actors are one
episode: identical start, end, packet count and target.

## 2. Corrected correlation against those actors/intervals

**Directly compatible traced producers: none for any of the three storms.** No
traced invocation, in the storm window or the +/-120 s margin, has a candidate
packet from the storm. The storm ORDER packets therefore have **no compatible
traced candidate** under the checked contracts/window. That is not evidence that
they were engine-generated; it means the file trace does not identify their
issuer.

The traced invocations that *do* address these actors near the storms are all
scripted **boarding** commands and two later default-action sites, each with
exactly one candidate packet of its own (never a storm packet):

| Player | Site | Source | Command | Recipients (recorded) | Targets (recorded) | PRE window | Candidates | Status |
|---|---|---|---|---|---|---|---|---|
| p2 7806/34426 | 1380, 1398 | `rawai-military.per` (boarding) | `(up-target-objects 0 action-garrison -1 stance-no-attack)` | both actors | hull **63029** | 3650-3655 s | 1 each (SPECIAL order 5) | candidate-not-causation |
| p2 7806/34426 | 1588, 1602 | `rawai-military.per:5175`, `:5361` | `(up-target-objects 0 action-default -1 stance-no-attack)` | both actors | 72542 / 429 | 3964 s, 3989 s | 1 each | candidate-not-causation |
| p4 34824 | 1380, 1398, 1513 (×3) | `rawai-military.per` (boarding) | `(up-target-objects 0 action-garrison …)` | actor | hull **35255** | 3343-3362 s | 1 each (SPECIAL order 5) | candidate-not-causation |
| p4 34824 | 1419 | `rawai-military.per` (boarding) | as above | actor | — (empty remote list) | 3351 s | 0 | empty-input-recorded |

Timing: the boarding invocations are **1-5 s before each storm starts**, and the
storm begins as the actor's traced state reads `action 609 / order 709`. Those
ids are **gather/gather** (section 3), so the storms are gather-order streams,
not the garrisoned-passenger reading of the first draft.

## 3. Actor state during each storm (type-21 records)

The recorded tuple is `(action, order, target)`. It decodes against
`rawai-constants.per` and cross-checks against the shipped `Promisory/const.per`:
**609 = `actionid-gather` and 709 = `orderid-gather`**; 617/717 are
`actionid-enter`/`orderid-enter`.

| Actor | Dominant recorded state inside the storm | Other states |
|---|---|---|
| p2 7806 | `(609, 709, target -1)` ×233 samples — **gather/gather** | 70 unknown, 1 sample `(617, 717, 63029)` — enter hull |
| p2 34426 | identical (233/70/1) | — |
| p4 34824 | `(609, 709, -1)` ×70 samples — **gather/gather** | 10 unknown, 2 samples `(617, 717, 35202)` — enter hull |

**Correction to the first draft.** That draft read this tuple as a "garrisoned
passenger". The constants contradict it: the standing state is gather/gather, so
these are **gather-order storms**. The single enter-hull sample per actor is the
boarding command (the boardings tabulated in section 2); it is the exception, not
the state the unit holds while the stream runs.

The packet cadence agrees. The three storms run at a ~16 ms median gap
(~40-48 packets/s), roughly 15x the AI's own order rate (`AI_ORDER` median
235 ms, ~4/s) and far above `300dac4`'s taunt loop (~1.8/s). So this is the
engine re-applying a standing order, not an AI rule re-firing on its tick.

The storming villagers therefore stay *gatherers* whose recorded state is
gather/gather throughout, while a fixed-point gather ORDER to one object is
re-issued ~40x/s for 3.5-5 minutes. Red's two actors share one path exactly (one
hull, 63029, one episode). Yellow differs in actor, hull (35255) and destination,
and its destination additionally receives AI orders while Red's does not — **the
same packet symptom, not yet proven to be one defect**.

## 4. Classification and the smallest discriminating gap

Per the attribution rules: **no directly compatible traced producer**; the only
traced events correlated with the storms are the scripted boardings, 1-5 s before
the onset. That establishes timing, not causation, and "no direct match" is not
"engine generated".

Smallest discriminating gap: the file trace records which scripted site
addressed an actor, but the storm's ORDER packets are attributable to no traced
invocation. The missing observation is the **issuer/mode of a gather order
re-issued to a unit that is boarding or aboard a transport** — whether a script
selection keeps re-issuing it, or the engine re-applies the unit's own standing
order. One bounded discriminator settles it: in a controlled recording, board one
villager with no pending gather order and give only the hull a destination, then
see whether the villager's gather stream appears; or record, for one voyage, the
site that issues the villager's gather order together with its packet stream.

## 5. Stock-AI guard this checkout does not carry (source comparison)

The shipped AI's source is available locally
(`G:\SteamLibrary\steamapps\common\AoE2DE\resources\_common\ai\Promisory\`, 36
`.per` files — the same snapshot as the 2026-09-07
`comparison\Promisory_vs_RAW_Migration_Comparison.md`). Its worker-task
selections strip out units tied up with a transport, in **both** the action and
the order field:

```per
(up-remove-objects search-local object-data-action == actionid-enter)
(up-remove-objects search-local object-data-order  == orderid-enter)
```

Occurrences: `gatherers.per` 2 (lines 2923-2924, 3010-3011), `general.per` 11,
`tsa.per` 7; separate `object-data-garrisoned` filters appear in `general.per`
(4), `tsa.per` (4), `orb.per` (3) and `boarhunting.per` (1).

This checkout defines the same ids (`rawai-constants.per`: `actionid-enter 617`,
`orderid-enter 717`, matching `Promisory/const.per`) but applies them unevenly:

| Guard | Promisory | this checkout |
|---|---|---|
| `object-data-action == actionid-enter` | 20+ sites, 3 files | **never used** — the defconst is its only occurrence |
| `object-data-order == orderid-enter` | used in task selections | only `rawai-expedition-budget.per`, `rawai-general.per:196`, `rawai-military.per` |
| `object-data-garrisoned` | `general`, `tsa`, `orb`, `boarhunting` | only the assault/attack files |

The economy-side tasking paths carry no transport guard at all: the camp
placement selections at `rawai-homebase.per:6077` and `:6107` filter on
`actionid-gather`, gather type and `target-id` with no enter/transport predicate.
A villager tied up with a transport therefore stays eligible for gather-side
tasking — the class the stock AI guards against, and the strongest remaining
candidate for these storms. It is a candidate, not an attribution: no traced site
has yet been shown to select actor 7806, 34426 or 34824.

**No fix implemented.** The decode correction changes what the storms are (a
gather-order stream, not a garrisoned-passenger stream), but it does not yet name
the writer that produces them, and the instruction was to stop at the smallest
discriminating gap rather than add blanket retry suppression, waits or order
throttling.
