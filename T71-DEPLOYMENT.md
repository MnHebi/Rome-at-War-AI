# T71 deployment — native-gather retasking experiment `RAWAI-P3B44T58B:511`

Installed 2026-09-20T11:03:54Z on user authorization, from the canonical
checkout, through the established process (`deploy-t71-511.py`, modelled on
`deploy-t67-510.py`). No game launch, no option change, no installed file
outside the AI payload touched.

## Identity

| Item | Value |
|---|---|
| Marker | **`RAWAI-P3B44T58B:511`** (number bumped from 510; label unchanged) |
| Payload aggregate | `3f3430a6b3e541c64c8f726458afdca1a0a2041e9b94690d81f5c7662f450360` |
| Files | 109 runtime `.ai`/`.per`; **8 changed vs 510** |
| Changed | `rawai-sn-defines.per` (retask bundle), `rawai-homebase.per` (retask writes removed), `rawai-init-goals.per` (marker), and the T69/T70 guard files: `rawai-assault-missions.per`, `rawai-assault-plans.per`, `rawai-assault-screen-fallback.per`, `rawai-attack-verification.per`, `rawai-command-boundary-coverage.per` |
| Source | HEAD `7e49d17` plus the disclosed marker bump 510 → 511 and the T71 experiment |
| Manifest | `.analysis\deployment-t71-511-20260920T110354Z\manifest.json` (+ `before-manifest.json`, registry copy, `before/` backup of the installed 510 payload) |
| Installed bytes / source bytes / backup | identical / identical / identical |
| Engine options changed / game launched | `false` / `false` |

## The experiment

One bounded native-gather configuration change, at bootstrap only
(`rawai-sn-defines.per`, the single `(true)` rule):

```per
(set-strategic-number sn-intelligent-gathering 1)
(set-strategic-number sn-retask-gather-amount 0)
(set-strategic-number sn-max-retask-gather-amount 0)
```

The gather percentages and their phase rules are **unchanged**. The only other
places that wrote those two strategic numbers were the shepherd/hunter retention
rules in `rawai-homebase.per` (they toggled the pair between 20/40 and 40/40);
they now own only `sn-disable-builder-assistance`, so 0/0 holds for the whole
match. Nothing else in the payload writes either number (verified against the
installed files).

**Why this and not latching.** Both sides rewrite percentages freely — 0 of
Promisory's 134 percentage rules use `disable-self`, and 11 of our 19 economy
chains do not either. The configuration that *differs* is the retasking budget:
Promisory disables native retasking (`init.per:122-124` sets intelligent
gathering on and both amounts to 0), while this build left the engine a 20–40
villager retasking budget. Native retasking is the engine subsystem that issues
**gather** orders to villagers, which is the shape of the storm.

## The question this build answers

> Does adopting Promisory's native retasking configuration eliminate the
> frame-rate gather-order storms while preserving RAW's existing desired
> resource percentages?

## What to measure on the replay

1. **Storms** — total gather ORDER packets and their per-frame rate; per-actor
   sustained streams (the 509/510 signature was actors at ~16 ms median spacing,
   ~20–50 packets/s for minutes).
2. **Economy health** — idle villagers, the food/wood/gold/stone worker
   distribution against the configured percentages, resource collection over
   time, and whether villagers still acquire new tasks at all (the specific
   "worker freeze" the old comment warned about).

## Reading the result

| Outcome | Reading | Next |
|---|---|---|
| Storms collapse, workers functioning | The native retasking budget was the driver — a strong result | Keep the bundle; re-check the percentage rules only if ratios drift |
| Storms collapse, workers freeze | Promisory's other gather-management settings matter | Add them incrementally (civilian caps, then percentages) |
| Storms essentially unchanged | These SNs correlate with the architecture but are not the direct cause | Latch the percentage writes (the 512 candidate) |

## Deliberately not included

`sn-cap-civilian-gatherers`, builder/explorer caps, percentage-write latching,
and any further change to the shepherd/hunter rules beyond removing the retask
writes. Including them would stop 511 from being a single-variable experiment.

## On the old "worker freeze" comment

The removed comment claimed 40 was needed as "a bounded retention floor instead
of freezing every resource worker". The documented semantics do not predict that
`0` freezes workers — they predict less retention before a villager switches
task. If this build does freeze workers, that is evidence about an interaction
inside RAW, not a reason to treat the documented behaviour as reversed.
