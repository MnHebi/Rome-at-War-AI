# T23 assault manifest/rendezvous correction

Status: **FIXED-PENDING-RUNTIME**. Installed marker `RAWAI-P3B44T23: 471`.

## Defect and source evidence

The empty-lift assault path selected an idle Transport nearest the home anchor,
then selected up to ten eligible soldiers nearest that hull, and immediately
started the 30-second boarding deadline. There was no maximum passenger distance
and no separate rendezvous state. Travel from an arbitrarily distant army was
therefore misclassified as failed local boarding.

This is source-proven and does not depend on replay interpretation. It does not,
by itself, explain already-loaded hulls failing later voyage dispatch or an AI
that never reaches assault admission.

## T23 behavior

1. After opponent/objective admission, reserve 5–10 idle, unowned, home-zone
   combat units first, preserving the existing eligibility and Palintonon
   exclusions.
2. Save the first member of that home-anchor-sorted manifest as the rendezvous
   point.
3. Select and claim the closest eligible empty Transport relative to that saved
   manifest point, not relative to the Town Center/home anchor.
4. Give the hull and passengers a separate 120-second rendezvous lease. The hull
   approaches the saved army point while the reserved passengers track the exact
   hull with the garrison order. Commands are renewed no faster than every eight
   seconds.
5. Enter the existing 30-second boarding contract only when the nearest remaining
   passenger is within 12 tiles, the accepted manifest is already aboard, or no
   reserved passenger remains ashore and exact cargo must be terminally classified.
6. A rendezvous timeout is event 25 and enters the existing bounded recovery.
   Event 23 identifies rendezvous start; event 24 identifies local boarding start.
7. The exact hull remains covered by the preparation ownership lease. Severe
   verified home defense remains the authorized preemption path.

No migration boarding, screened/unscreened voyage, landing, useful-partial load,
three-slot dispatch, target rotation, or combat-continuation policy changed.
The immutable T17 preparation generator remains byte/token-equivalent to its
known control; T23 adds a separate, narrowly scoped ownership guard for the new
rendezvous phases.

## Validation

- PASS: five actual-PER rendezvous fixtures covering manifest-first selection,
  army-relative hull selection, timer separation, local timer admission, bounded
  timeout, missing hull/small manifest release, and exact-hull ownership loss.
- PASS: 409/409 full regression tests.
- PASS: generated assault files and command-counter source map synchronized.
- PASS: 39 replay-benchmark metadata validations.
- PASS: 813 ownership sites, zero direct-permission failures.
- PASS: 91-file installed payload independently matches source SHA-256
  `72A073D5FCC4DD15B33399942AF1CC4B7F4EA64F1AB55FC09E3B9D858BA6BE26`;
  no missing, unexpected, or mismatched runtime files.

## Fresh-replay acceptance

Audit every player. A mission should reserve its army before a hull, acquire a
hull near that army, spend distant travel in rendezvous rather than the 30-second
boarding window, and either begin local boarding (event 24) or terminate once as
event 25 after the bounded lease. Existing useful partial/full loads must still
reach the three independent voyage slots. Separately classify any mission that
never forms and any already-loaded hull that fails after preparation; those are
not declared fixed by this patch.
