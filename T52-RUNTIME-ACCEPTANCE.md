# T52 runtime acceptance plan

## Scope and identity

T52 is the next runtime after the T51 Iberia replay regression assessment. It
contains two independently revertible changes:

- `ec3ee78` — **causal Shipyard repair**: restores T50's full independent
  X/Y `[-14,+14]` near-anchor candidate domain after T51's four sparse
  cardinal sectors reduced seven builders / fifteen orders to one order from
  one player. It preserves the existing eight-attempt lane, buildability,
  separation, same-water-zone and W1-W6 aperture gates, worker path test,
  failed-sector memory, exact foundation verification and all capacity tiers.
- `e7031f9` — **diagnostic-only re-arming**: replaces startup/lifetime sample
  pools with bounded pools reserved for real Shipyard, migration, naval
  right-of-way and expeditionary episodes. No command-bearing rule is gated by
  a diagnostic pool and no controller policy changes.

The deployed source is `e7031f9` on `fix/trade-cog-cap-dacian`, marker
`RAWAI-P3B44T52:500`. Source and installed test runtime contain 99 identical
files with aggregate SHA-256
`387913EFC902E0DF796532F16F31A4B05F7F265962B8AE43C39C7033433C28B5`.
The ordinary payload was deployed without the optional writer-trace overlay.

## Ordered runtime gates

The following gates must be assessed in order. Later observations may be
collected from the same replay, but expeditionary policy must not be changed
until the preceding controller boundaries are resolved.

### 1. Shipyard recovery — primary T52 acceptance gate

Status before replay: **FIXED-PENDING-RUNTIME**.

Evidence required:

1. For each player below desired Shipyard count, reconstruct admission,
   placement, issuance and exact-foundation episodes from codes 524-545.
2. A real admission arms eight placement samples and two foundation samples.
   Code 545 records each sampled rejection reason together with candidate X/Y,
   anchor and attempt (536/537/538/540); these samples must exist late enough
   to explain actual deficits rather than expiring during startup.
3. Issuance is not success. Code 542 value 1 must identify a concrete new
   foundation; code 541 with code 542 value 2 must identify completion.
4. Bootstrap 0->1 and protected 1->minimum capacity must remain available.
   The sustained 180-second, wood-over-600 tier may advance from minimum to
   `min(desired,4)`; later full expansion remains subject to ordinary economy
   and tech-up discipline.

Runtime PASS requires a material recovery from T51's one order / one player,
with multiple eligible players reaching concrete foundations and no return of
the narrow-inlet placement regression. T50's fifteen orders across seven
players is the comparison baseline, not an automatic numeric quota for a
different map. A continuing one-player collapse, repeated unexplained deficit,
or build issuance without a concrete foundation is FAIL.

### 2. First Villager order-706 onset

Status before replay: **INVESTIGATING**; no behavior change in T52.

Start at the first order-706 episode, not the largest late-game aggregate. For
the earliest repeated tuple record timestamp, owner, actor IDs/types, target
ID/type/owner, group, action, order, command subtype and cadence. Correlate it
against:

- migration STOP writer codes 5-13, now protected by the per-migration
  `gl-mig-diag-stop-left` pool;
- boarding/rendezvous writers 20-24, protected by a separate boarding pool;
- the existing once-per-minute nonzero command-boundary counters;
- other source-visible Villager writers already mapped by the ownership audit.

At a real migration start the STOP pool is re-armed independently, so routine
boarding renewals can no longer consume the evidence required for a later STOP
episode. A matching exact actor/time writer is attribution evidence. If no
explicit writer matches while its class-reserved pool and command counters are
known available, the mapped RAW migration STOP writers can be excluded for
that onset; that is not by itself proof of which native manager expanded the
706 orders. Do not change gameplay on an unmatched trace alone.

### 3. Assault preparation aborts

Status before replay: **INVESTIGATING**; no T52 behavior change.

T51 recorded eight Gray abort/useful-partial terminal cycles. In every sampled
cycle the still-reserved candidate was close (2-7 tiles), targeted the exact
Transport, remained in group 4, and showed action 617 / order 717 / command 4;
only one sampled candidate was idle. Those observations exclude remote-hull
selection, lost reservation and absent enter intent for the sampled units.
They instead establish a boundary where the engine does not finish boarding
despite valid close active intent after the existing one-time grace.

For each T52 abort, reconstruct the whole hull episode and determine whether
the remaining passenger is physically blocked, oscillating, repeatedly
reissued, displaced by another mission, or genuinely unable to enter. Preserve
successful three-slot assault dispatch and useful-partial departure. No broader
timer increase is justified without the discriminating evidence.

### 4. Migration drop-site productivity

Status before replay: launch/landing **RUNTIME-SUPPORTED PASS**; productive
drop-site completion **OPEN**.

A complete autonomous success requires this observable chain without manual
orders:

```text
admission -> boarding -> writer 25 unload
-> writer 30/31/32 exact foundation selection/issue
-> writer 26 concrete selected foundation
-> code 579 value 2 (that drop-site reaches status-ready)
-> writer 27 post-foundation gather task
-> settlers visibly gather and deposit the intended remote resource
```

Code 579 value 3 is a terminal drop-site failure and therefore a FAIL for that
episode. Foundation appearance alone is not productive success. Capture the
drop-site ID, anchor ID, resource zone and whether all settlers were released,
recalled or reassigned before work began.

### 5. Merchant right-of-way in a real choke

Status before replay: **INVESTIGATING**; T52 changes diagnostics only.

Acceptance requires a naturally congested late-game episode with an actual
mission Transport or mission warship and nearby self-owned Merchant Ships. The
expected diagnostic/behavior sequence is:

1. selected priority hull and measured no-progress samples (586-590);
2. a plausible active `actionid-trade` merchant survives filters (591-596), or
   a precise 617-624 rejection explains why none can yield;
3. a same-water safe holding candidate is proven (625-630);
4. the exact pre-issuance record appears (631-637) and existing writer 420/421
   moves only one merchant;
5. the priority hull resumes measurable progress before another clearance;
6. native merchant trade later resumes.

No intervention for distant merchants or already-progressing priority hulls,
and no global STOP, is required for PASS. Diagnostics without the actual
clearance/progress/resumption sequence do not close the behavior.

### 6. Expeditionary commitment

Status before replay: **INVESTIGATING / OBSERVATION ONLY**.

T52 emits a census only when the terminal expeditionary blocker changes and a
manifest snapshot once per actual MANIFEST-FIND episode. Use those events to
identify reserve, surplus, naval gate, route/Transport availability and all
three slot states. Do not tune commitment until Shipyard capacity, assault
preparation, migration productivity and ROW have been judged. The acceptance
criterion remains productive saturation and reuse of the existing three slots
while a safe isolated player has real surplus—not simply more manifests or a
smaller home reserve.

## Static validation already complete

- Focused controller suites: 192 tests PASS.
- Full Python 3.12 discovery: 529/529 PASS (the initial sandbox-only Windows
  Temp permission error also passed in isolation and on the permitted rerun).
- PER structure/operands: PASS.
- Strategy execution: 1,156 matchups, zero errors.
- Naval doctrine: PASS.
- Ownership contract: 27 tests PASS.
- Replay benchmark metadata: 42 tests PASS.
- Generated-source synchronization and `git diff --check`: PASS (line-ending
  warnings only).

These results protect structure and source synchronization. They do not close
any runtime-sensitive gate above.
