# Reserved boarding observations: historical coverage demonstration

2026-09-08. PR11 instrumentation candidate, **not deployed**. The ORDER706 defect remains **INVESTIGATING**. This changes diagnostic selection/output, not boarding eligibility, commands, modifier2, ownership, retry cadence or deadlines.

## Why the original allowance was insufficient

Four reports at the first eligible invocations in each180-second family interval could be exhausted during travel/early loading. Counting only decoded boarding packets is optimistic: T56 Yellow's writer23 at2212.704s and Green's writer23 at3624.674s have invocation headers but no matching new SPECIAL5 packet. Those calls would still consume an unreserved allowance.

The replacement retains four boarding reports per player/family/180s:

- One early report, after a quiet observation has established a possible pair.
- One reserved report at each loading age **12,20,28 seconds**, anchored by the existing local-loading start writer21. Travel writers20/25 cannot spend these three credits. Ages are eligibility thresholds, not new timers that issue commands.
- Quiet observations at actual calls, at least3 fresh game-seconds apart, retain the latest two actor/hull samples between reports. They emit no detail messages. After a report, rotate to another pair; follow that pair across subsequent quiet calls, searching at most32 final members for each identity.
- A new hull/start clears tracking/phase, **not the family allowance**. Only the existing180s refill replenishes credits. Default/resource writers retain their separate four-report allowance.

The original command executes regardless of capture, missing identity, quota or output. Sampling never gates gameplay. No new telemetry strings/fields: maximum boarding detail remains4×142=568 chat lines per anchored interval. With defaults/coverage, the original856/player anchored-period bound remains; conservative sliding180s bound1712. The reduction is repeated early output, not a raised cap. Quiet work is bounded to two object tracks and32-member identity searches, at most once/3s per active player; engine overhead still needs ordinary-match validation.

## Historical timelines, explicitly conditional

Run `py -3.12 tools/boarding_sampling.py`. The compact fixture `tools/fixtures/boarding-sampling-windows.json` retains replay hashes, packet/header sequences, packet membership, source-writer evidence and onset times. Reproduce it from the **existing corrected caches**, without decoding another replay:

`py -3.12 tools/boarding_sampling.py --extract "G:\Projects\Codex\Rome at War AI\.analysis"`

This is a **counterfactual schedule**, assuming a fresh family allowance, valid selected-object pointer and the listed calls reaching the mining observer. Headered sites are witnessed; unheadered packets use labelled site20/24 proxies, not invented source attribution. Fresh time is modelled as floor(replay milliseconds/1000), not the old shared-clock field. The exact pre-header/pre-packet acquisition time is unavailable, so near-integer-boundary timing remains uncertain. No historical PER list order, paired coordinates, complete unlogged-call history or allowance carry-in is reconstructed.

| Window / first706 | Old four-report schedule (seconds) | Reserved schedule (seconds) | What this demonstrates |
|---|---|---|---|
| T56 Yellow7706:2223.713;34730:2238.899 |2205.076,2208.887,2212.704,2215.980|2208.887 early;2222.525 age12;2229.065 age20;2238.884 age28|Later eligibility survives the invocation-only renewal. Age12 precedes7706 onset by1.188s; age28 proxy precedes34730 onset by15ms. The15ms is **not** a newly measured observer timestamp.|
| T56 Red34636:3718.157;34616:3718.480 |3676.775,3680.598,3688.834,3697.090|3680.598 early;3710.858 age12;3717.502 age20|Travel no longer consumes the late credits. Last proxy is655/978ms before onsets. No age28 call is observed before them.|
| T56 Green34564:3627.901 |3617.531,3620.817,3624.674,3627.970|3620.817 early|**Coverage tradeoff:** reservation does not print the nearer3624.674 invocation. Next observed writer24 is after onset; it cannot establish first causation. No exact immediate pre-onset detailed pair is guaranteed.|
| T55B Cyan43834:5549.578 |5543.621,5548.052|5548.052 early|Potential pair/report1.526s before onset, but both source sites, actual lists, current phase and allowance history are unknown. Historical stage86 is about395s old and cannot supply them.|

The scheduling model is checked against execution of the actual generated PER subset, not merely a test for the presence of threshold expressions. Synthetic lists in that test establish scheduling equivalence only.

### Temporal eligibility is not actor coverage

- Yellow7706 is in the2222.540 outgoing packet;34730 is in2238.884. Red34636/34616 are in3717.502. That establishes decoded recipients, **not final PER index order or which two actors would have been tracked**.
- Unknown final lists can make every affected actor unsampled. No claim of guaranteed paired coverage is made from packet order or historical representative-candidate goals.
- Header-only renewals retain `packet_members: null`; absence of a packet is not absence of a writer or proof of native origin.
- Missing intermediate calls may alter the actual report time/tracked pair. Within a valid phase they cannot consume a later tier before its threshold. A missed phase restart/other hull can alter that premise; it is not reconstructed here.
- Fully exhausted carry-in before these short windows yields **zero** detailed reports under both policies. The test explicitly exercises that lower bound. New hulls cannot manufacture credits, and the policy does not promise every episode a report.
- Quiet captures help only if the tracked actor remains identifiable. The offline decoder still rejects missing/changed identities, ownership, targets or stale positions. It never turns quiet sampling into a boarding-success claim.

## Validation and unresolved evidence

Six new tests cover historical/model-to-generated-PER scheduling, fixed cap, invocation-only headers, the Green gap, unknown lists, exhausted carry-in, fresh quiet pairs, travel exclusion, hull reset without refill and intermediate renewals. Existing15 observer tests protect final selections, pointer restoration, unchanged ordered commands, modifier and private-state boundaries. Full validation is recorded in `MATCHED-BOARDING-COMMAND-OBSERVATIONS.md` and `HANDOFF.md`.

Adversarial review: accepted early-budget exhaustion, packet-only undercount and the need for quiet recent pairs. Rejected guaranteed actor coverage, inferred historical movement, automatic source attribution for unheadered packets and raising the cap as a substitute. Deferred actual engine cost, affected-actor paired coverage and task outcomes to a future explicitly authorized ordinary match.

Installed cleanup/Ctrl experiments remain untouched. The existing separate ranged-counter correction is included in PR11 for review, not represented as part of this diagnostic-only change. Neither this policy nor the matched comparison closes the flood defect.
