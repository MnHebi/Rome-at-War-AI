# T42 Shipyard probe recovery

## Status

**FIXED-PENDING-RUNTIME / SOURCE ONLY**, 2026-09-05. Runtime marker reserved as
`RAWAI-P3B44T42:490`; the installed test copy remains T41 until the user
explicitly authorizes another deployment.

## Observation and first causal divergence

The user observed that most long-Imperial players still had one Shipyard and
Green had none despite ample wood. T40's admission policy can request the first
yard immediately and the second after a persistent minimum-capacity deficit,
but every admitted candidate then entered a new mobile-water validation gate.

That gate searched only 64 tiles around the candidate for a warship, Transport,
or fishing ship. It rejected the candidate when none was found. Consequently:

- a first Shipyard was circularly dependent on already owning one of the naval
  units it was intended to produce;
- a player with one Shipyard lost all later placement capability when its fleet
  sailed more than 64 tiles away;
- an active Trade Cog, although a real mobile water-path probe, was ignored.

The executable pre-fix fixture reproduced all three cases with zero build
issuances and blocker reason 6.

## Bounded correction

- Search the full supported 255-tile standard-map radius for a mobile probe.
- Include Trade Cogs alongside warships, Transports, and fishing ships.
- When no probe exists, only an already-admitted first or second Shipyard may
  continue. It retains candidate buildability, own/allied naval-building
  separation, worker availability/pathing, affordability, escrow, pending
  placement, foundation verification, completion verification, and failed-site
  memory.
- Expansion after the minimum operational count of two still requires the
  four-point exact mobile-water path proof.
- Diagnostic 410 reason 8 now distinguishes "no mobile water reference after
  minimum capacity" from reason 6 coastline/exit rejection.

This deliberately prioritizes obtaining minimum operational capacity when no
mobile proof object exists; it does not claim the engine has demonstrated the
fallback site's open-water quality. `up-can-build-line` and the retained site,
separation, and worker checks remain the static/source boundary. Fresh runtime
must establish actual foundation placement and usability.

## Validation

- Shipyard fixture: **PASS**, 14 tests.
- Pre-fix reproducer: zero-yard/no-hull, one-yard/no-hull, and distant-Trade-Cog
  cases all produced zero builds with reason 6.
- Post-fix fixtures: first and delayed second yard issue without a probe;
  distant Trade Cog receives exact path queries; third/later yard remains
  blocked without mobile proof and reports reason 8.
- Generated source synchronization: **PASS**.
- PER validation: **PASS**, empty report.
- Full Python 3.12 discovery: **PASS**, 508 tests.
- `git diff --check`: **PASS**.
- Causal commit: `280ae40`.

## Runtime acceptance

After a separately authorized T42 deployment, require a fresh match showing
`T42:490` and verify per player:

1. a player with a Port and desired naval capacity no longer remains at zero
   merely because no qualifying ship already exists;
2. a persistent one-yard deficit reaches two when affordable, including after
   its fleet has departed;
3. foundations appear, complete, and do not repeatedly occupy narrow crevices;
4. later expansion retains exact-path coast validation;
5. diagnostics distinguish reason 8 from actual coast rejection reason 6.

Do not call the runtime behavior closed from these static/fixture results.
