# T76 deployment — native hunter floor `RAWAI-P3B44T58B:513`

Installed 2026-09-20T14:04:36Z on user authorization, from the canonical
checkout, through the established process (`deploy-t76-513.py`, modelled on
`deploy-t72-512.py`). No game launch, no option change, no installed file
outside the AI payload touched.

## Identity

| Item | Value |
|---|---|
| Marker | **`RAWAI-P3B44T58B:513`** |
| Payload aggregate | `7b0fe74e5493ada25d7e1489862f248ee0ef0b9be9cfaadce2580d97d71ddb67` |
| Files | 109 runtime `.ai`/`.per`; **4 changed vs 512** |
| Changed | `rawai-hunt.per` (floor values), `rawai-sn-defines.per` (bootstrap floor), `rawai-init-goals.per` (marker), `rawai-command-boundary-coverage.per` (identity) |
| Manifest | `.analysis\deployment-t76-513-20260920T140436Z\manifest.json` (+ `before/` backup of the installed 512 payload) |
| Installed / source / backup | identical / identical / identical |
| Engine options changed / game launched | `false` / `false` |

## The change

`sn-minimum-number-hunters` is the engine's "keep at least N villagers on
hunting" control. Ours was a permanent floor of **1**, raised to **6/7** inside
the boar-commit chains and never reset — 24 live writes, none of them 0. The
shipped AI does the opposite: **0 at init** (`Promisory/init.per:390`) and **2**
only while a boar hunt is active (`Promisory/boarhunting.per:292`), with every
other setter in its source commented out.

513 matches that:

- every `1` write in `rawai-hunt.per` becomes `0` (idle / verify / rescue states
  — i.e. no standing hunter demand);
- every `6`/`7` write becomes `2` (the active boar commit, Promisory's value);
- the bootstrap initialises the floor at `0` explicitly.

Nothing else moved: `sn-minimum-boar-lure-group-size`,
`sn-minimum-boar-hunt-group-size`, `sn-enable-boar-hunting`, the gather
percentages and the 511 retasking bundle are all untouched.

## Why this hypothesis

The 512 storms are p7 villagers in the **hunt** state (`action 613 / order 713`),
re-issued to a **stationary object at one fixed tile** at frame rate for 33
minutes, never completing — the owner's WORK collapsed to 298 packets in the
final 15 minutes. A permanently unsatisfied "keep N hunters" floor is exactly
that behaviour: with no reachable huntable left, the engine keeps trying. It
also needs no scripted producer, which is why every correlator pass came up
empty. (The related engine control `sn-disable-villager-garrison` was itself a
mitigation for an earlier storm of the same family, which is what prompted this
comparison.)

## Acceptance (512 → 513)

| Measurement | What to look for |
|---|---|
| Hunt-state storms | the `(613, 713)` actors and their fixed-tile target should stop dominating; per-actor rates and ≥150-packet storm counts |
| Storm targets | whether transport/stationary-target storms persist at the same scale |
| Economy | food from hunting early, then gather distribution; WORK total must not regress |
| Loading/boarding | unchanged from 512 (this build touches no boarding path) |

Honest caveat: the setting is not journaled in the file trace, so this cannot be
confirmed from the trace the way the 512 latch was. The test is whether the
hunt-shaped storms collapse in the next match.
