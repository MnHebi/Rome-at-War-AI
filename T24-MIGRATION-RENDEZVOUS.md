# T24 migration rendezvous correction

Status: **FIXED-PENDING-RUNTIME**. Candidate marker `RAWAI-P3B44T24: 472`.

## T22 evidence

Replay `SP Replay v101.103.48987.0 @2026.09.01 112916.aoe2record`, SHA-256
`02E96FAE79D42D3F9BA276AFEA503374F2DE21738F026D0854AF7F1B0EFB7F59`, runs
T22:470 for players 2-8, lasts 85:19 and parses with zero action-stream errors.
The replay remains outside this repository.

The user's direct observation is that hundreds of villagers waited on beaches
and nobody migrated. Preserve that visible symptom. Decoded evidence also
contains full worker-migration departures for Gray at 71:48 and 84:05 and Red at
81:42; Red's twenty settlers are detected landed at 83:19. Until the user
clarifies whether "nobody" meant no visible departures during the beach pile-up
or no sustained productive colony, both accounts remain recorded.

The all-player command/telemetry audit reconstructs 26 migration boarding
windows. Early Scout missions give the cleanest causal comparison:

- Yellow closes 81 to 43 and 65 to 39 tiles before two empty aborts;
- Purple closes 55 to 27 tiles before an empty abort;
- Orange closes 45 to 35 and 63 to 25 tiles before two empty aborts;
- Blue closes 159 to 125 and 97 to 73 tiles before two empty aborts.

All carry the correct exact-hull garrison order and no competing command before
the terminal event. They are aborted because the fixed 30-second load timer
starts before passengers travel to the hull. Worker missions reproduce the same
boundary: Purple times out at distances 56 to 33 and 17 to 12, Blue aborts a
late eighteen-passenger attempt, while Red's twenty and Gray's twenty/fourteen
beat the same deadline and depart. Success therefore depends on rendezvous
distance rather than the accepted manifest alone.

There is a separate admission issue. T22's Red gate snapshot at 29:53 reports
idle bucket 0, two Transports, no defense, no resource depletion and no home
resource pressure. Source requires two engine-idle villagers unless depletion
or pressure is active. Visually waiting villagers with stale orders therefore
do not admit ordinary worker migration. Red's home-resource pressure becomes 5
at 50:52 and its first worker migration begins at 52:58. No admission-policy
change is included in T24: equivalent outer-gate state was not exposed for every
player, and broad worker stripping without a proven stalled-worker discriminator
would be speculative.

## Source defect

Migration selected a Transport first, selected its eligible passenger manifest,
issued garrison, and immediately armed the 30-second load timer. There was no
rendezvous state, passenger-distance admission or independent preparation
lease. Remote travel was therefore classified as failed local boarding.

## T24 behavior

1. Preserve the existing migration target, hull, worker/Scout eligibility,
   capacity and passenger ordering.
2. Save the closest reserved passenger as a rendezvous anchor after exact group
   ownership is claimed.
3. Give the exact hull and passenger group a separate 120-second rendezvous
   lease. The hull approaches that anchor while passengers track the exact hull.
4. Renew both commands no faster than every eight seconds.
5. Start the unchanged 30-second local boarding contract only when the nearest
   remaining passenger is within twelve tiles, the accepted manifest is aboard,
   or no reserved shore passenger remains and exact cargo needs classification.
6. On rendezvous timeout, pass the exact hull/cargo once into the established
   full/partial/abort and return policy. Terminal phase 3 marks rendezvous start;
   phase 4 marks its timeout without adding strings to the engine table.
7. Extend exact-hull preparation ownership only across the new states. Assault
   T23, landing validation, migration drop-site handling and voyage policy are
   unchanged.

## Non-regression acceptance

- Previously successful Red/Gray full worker loads and useful partial migration
  remain eligible and enter the same route controller.
- Remote travel never consumes the local 30-second boarding timer.
- Local boarding remains bounded at 30 seconds; rendezvous remains bounded at
  120 seconds.
- Exact-hull loss enters the existing owner-loss recovery and cannot substitute
  another Transport.
- Scout migration, same-zone landing validation and drop-site states are not
  bypassed.
- Fresh replay must audit every player and distinguish mission admission,
  rendezvous phase 3, local full/partial loading, phase-4 timeout, voyage and
  productive landing. T24 cannot be closed from structural tests alone.
