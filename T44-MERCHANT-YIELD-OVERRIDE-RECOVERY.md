# T44 merchant-yield override recovery

## Status

**ROOT-CAUSE-PROVEN / FIXED-PENDING-RUNTIME.** No deployment was performed.

## Runtime evidence

The T41 replay `SP Replay v101.103.48987.0 @2026.09.05 121955.aoe2record`
contains marker `RAWAI-P3B44T41:489` and proves that right-of-way detection and
command issuance ran, but did not preserve a usable clearance:

- Player 1 yielded merchants 63142 and 56835 for stalled priority hull 53151.
- Player 6 yielded merchants 49854, 36796, and 66270 for stalled priority hull
  39350.
- At 68:08, Player 1 issued sequence 4088229 as a single-object `ORDER` moving
  merchant 63142 to the recorded hold at `(10, 125)`.
- Later in the same displayed second, native trade issued sequence 4088262 as a
  35-merchant fleet `MOVE` to approximately `(1.48, 142.90)`. Merchant 63142
  was included in that fleet command, so its yield was immediately overwritten.
- Native fleet movement continued in subsequent records while the right-of-way
  controller advanced to merchant 56835.

This is a runtime FAIL for T40's merchant-right-of-way acceptance. The blocker
detector and initial command site were active; the first divergence was the
failure to distinguish the controller's hold MOVE from native trade's MOVE.

## Source cause

The generated hold-renewal rule treated `actionid-move` as sufficient evidence
that a yielded merchant was still obeying its lateral hold. It only renewed a
merchant observed trading, or idle more than three tiles from the hold.

That assumption is invalid because native trade may replace the controller's
single-object order with a fleet MOVE while leaving the merchant in
`actionid-move`. The source retained the intended hold coordinates but never
compared them with the merchant's live `object-data-move-x/y` destination.

The rule order compounded this defect: stage 4 could allocate a new merchant
before the existing hold records were checked. A newly issued clearance set
`gl-row-issued`, suppressing the overwritten merchant's renewal for that sample.
Thus the three-attempt ceiling could be spent on additional merchants while the
first merchant had already returned to the choke.

## Implementation

- A moving merchant counts as reacquired when its live move destination differs
  from the recorded hold point on either axis.
- Existing hold renewal/release rules now run after priority-hull progress and
  intent are remeasured, but before stage-4 allocation of another merchant.
- If a due renewal issued in that sample, stage 4 returns to observation instead
  of consuming a distinct-merchant intervention.
- A merchant moving to the exact hold destination is left alone, preserving the
  one-at-a-time progression to another blocker when the priority hull remains
  stalled.

The existing bounds are unchanged: eight-second samples, no more than three
renewals per held merchant, no more than three distinct interventions, a
32-second hold, 120-second merchant cooldown, and 180-second priority-hull
cooldown. The patch issues no STOP, does not order the priority hull, does not
take group ownership, and does not alter trade, economy, transport, or combat
policy outside this overwrite recovery.

## Validation

- Right-of-way fixtures: **13/13 PASS**. New executable fixtures reproduce the
  native fleet-MOVE override and prove that the same merchant is repaired before
  another merchant is allocated; an exact hold destination does not spam
  renewal.
- Trade topology: **10/10 PASS**.
- Validator suite: **128/128 PASS**.
- Full Python 3.12 discovery: **512/512 PASS** in the permitted temporary-file
  environment.
- Generated right-of-way synchronization: **PASS**.
- PER structure/operands: **PASS**.
- Naval doctrine: **PASS**.
- Strategy execution: **PASS**.
- Ownership audit: **960 relevant sites, zero direct permission failures**.
- `git diff --check`: **PASS** (line-ending warnings only).

## Runtime acceptance

A fresh replay carrying marker `RAWAI-P3B44T44:492` must show:

1. a verified stalled Transport or mission warship still activates bounded
   right-of-way clearing;
2. if native trade overwrites a yielded merchant's destination, the controller
   repairs that same hold before selecting another merchant;
3. the merchant sustains a lateral hold long enough for the priority hull to
   progress by more than two tiles;
4. hull progress stops further clearing, and native trade later resumes toward
   the original live allied Dock;
5. renewal/intervention ceilings remain respected, with no STOP commands,
   distant-merchant intervention, or ownership leakage.

Until a fresh replay demonstrates those conditions, this defect is not CLOSED.

## Identity

Behavioral commit: `d05c130`. Source marker: `RAWAI-P3B44T44:492`. The installed
test copy remains exact T41:489 with aggregate SHA-256
`AB2271FA659CC47F6471CA950006FF73F986918D71057C12DD90BED099A858F2`.
