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

Timing: the boarding invocations are **1-5 s before each storm starts** and the
storm begins exactly as the actor's traced state becomes `action 609 / order 709`
— the pair observed for garrisoned passengers.

## 3. Actor state during each storm (type-21 records)

| Actor | Dominant recorded state inside the storm | Other states |
|---|---|---|
| p2 7806 | `(609, 709, target -1)` ×233 samples — garrisoned | 70 unknown, 1 move sample `(617, 717, 63029)` |
| p2 34426 | identical (233/70/1) | — |
| p4 34824 | `(609, 709, -1)` ×70 samples — garrisoned | 10 unknown, 2 move samples `(617, 717, 35202)` |

So in all three storms the ordered actor is **inside a hull** (it was boarded
1-5 s earlier) while the ORDER stream to a fixed destination continues for
3.5-5 minutes. The two Red actors share this path exactly (one hull, 63029, one
episode); Yellow shows the same symptom class but a different actor, hull (35255)
and destination, and its destination also receives AI orders while Red's does not
— so the two are **the same packet symptom, not yet proven to be one defect**.

## 4. Classification and the smallest discriminating gap

Per the attribution rules: **no directly compatible traced producer**; the only
traced events correlated with the storms are the scripted boardings that put the
actors into the hull. "Earlier scripted tasking causing delayed native
repetition" remains a **hypothesis** — the boarding is 1-5 s before the onset,
which establishes timing, not causation.

Smallest discriminating gap (no new logger needed): the file trace records which
scripted site addressed an actor, but a garrisoned unit's ORDER packets in the
storm window are not attributable to any traced invocation — the missing
observation is the **issuer/mode of orders issued for a unit inside a transport**
(whether the script re-issues the destination order for a loaded hull, or the
engine expands the hull's own destination order per passenger). One bounded
discriminator would settle it: in a controlled recording, board one transport,
give the hull a single destination order and no further scripted orders, and see
whether the same ORDER stream appears for the passenger; or record, for one
voyage, the command site that issues the hull's destination order together with
the passenger order stream.

**No fix implemented.** Attribution is ambiguous, the implicated state cannot be
named, and the instruction was to stop at the smallest discriminating gap rather
than add blanket retry suppression, waits or order throttling.
