# Boarding Ship nonconversion audit — 2026-08-31

## Result and scope

**INVESTIGATING — the reported failed conversions are not yet causally resolved.**
Diagnostic-only user request. No runtime, DAT, deployment, commit or branch change.
Two distinct findings must not be conflated:

1. Normal Boarding Ship1880 has **zero conversion range** in the authoritative
   DAT. This is a concrete configuration difference and a candidate explanation
   for visible contact without conversion, **not engine proof of failure**.
2. The siege-escort acquisition rule can commandeer an ungrouped Boarding Ship
   without checking its current conversion action. This is a source-visible
   ownership gap, **not established attribution for Red's early encounter**.

User evidence: Red visibly attached to an enemy Scout Ship around29min, and to
an enemy Fishing Ship earlier, without converting either. Preserve this symptom.

## Identity and authority

- Recovery checkout: `G:\Projects\Codex\Rome at War AI\.recovery-work\P3B44-transport-only`;
  branch `recovery/p3b44-transport-only`, HEAD `387eccab36a3311ca90d9e39bea6d73013584a8b`.
- T16 replay162617: `F8D75EC49C2FF9DA206B872CAD697E98DF56F9C17FCE559F012F90BE130859E7`.
  Archived T16A2:463 runtime has87 files. Its relevant opportunity command and
  siege-escort selector match current source.
- T17 replay183134 comparison: `608B6681C240FC681E5C883A0CA9A138F3934FAE56DB40445B0AEDA45ECA5499`.
- DAT: workspace `RaW data fix/resources/_common/dat/empires2_x2_p1.dat`,
  SHA256 `A1319BE7E0D4CCF68A13E719BA2D8B4B39383D01B7D3FDD3123452F6A0D36356`.
  This verifies the inspected reference, not an independently recovered replay DAT.

## Mod mechanics checked

-1880 is **class53, Converting Ship**, not a conventional damaging warship.
  Its attack list is empty; its conversion tasks are action104.
- Explicit enabled task definitions cover warships22, merchants2, transports20
  and Fishing Ships21. Scout Ship527 is class22. Neither reported target is
  excluded by type, nor do the base target definitions have hero immunity.
- Naval conversion tasks use work values6/10, no positive task-range override,
  and the unit's maximum range is0. Identical zero-range configuration in the
  five tested civilization definitions (Britons, Gauls, Germani, Picts, Romans).
- Hidden Boarding Ship2359 has range1/task range1; reference Boarding Galleys535
  and536 have range1. These comparisons motivate an experiment; they do not prove
  that zero-range conversion is impossible under this engine's contact rules.
- Base resources67/87 are0 but automatic technologies234/317 enable conversion
  and ship conversion. No matching disable-tech effects were found. Do not call
  a base-resource snapshot a proven missing research gate.
- Military-charge fields are0 on1880 **and original class53 Boarding Galleys**.
  Do not apply ordinary non-Monk/Sun Ce charge-type requirements blindly to53.

Task/range interpretation reference: [UGC author's conversion-task reference](https://ugc.aoe2.rocks/general/tasks/tasks/#104-convert).
An [official-forum first-person report](https://forums.ageofempires.com/t/major-bug-convert-task-non-monk-conversion-task-broken-sun-ce-custom-units/287396)
describes ordinary non-Monk conversion failures, but proposes Boarding Galleys as
a workaround. It is **not proof that RaW's class53 has the same engine bug**.

## Source command/ownership audit

`rawai-unitconstants.per` maps boarding-ship to1880. No dedicated conversion
controller, conversion-progress watchdog, faith-aware retry or conversion claim
was found. The AI uses default target orders, not a separate explicit conversion
action. The cached AIRef defines default as right-click; lack of explicit704
packets therefore does **not** prove lack of conversion attempts.

Relevant `rawai-military.per` paths:

| Controller | Source behavior |
|---|---|
| Transport escorts,170–350 | Acquire idle/free ships, then refresh GUARD on their owned group. |
| Naval opportunity,570–1195 | Acquire idle/free ships, issue default target order, do not reserve a conversion-specific owner. |
| Port utility clearing,5167–5440 | Utility admission requires idle/free; persistent selected-hull movement follows. |
| Naval response,8248–8600 | Command admission requires idle/free; may issue default enemy targeting. |
| Siege escorts,9181 | Finds1880, excludes attacked/group-owned/wrong-zone ships, **does not exclude busy/converting ships**, issues GUARD. |
| Home response leash/release,9558–9630 | Acts on the home-response group, not all Boarding Ships. |

Thus an ungrouped conversion started by opportunity control can be eligible for
siege GUARD. Fixing that gap alone would not explain an uninterrupted failure.

## Replay sweep and concrete early lead

All-player1880/2359 MAKE request counts (requests are not completed births):

| Visible color / player | T16 | T17 |
|---|---:|---:|
| Red /1 |4|0|
| Green /2 |4|0|
| Yellow /3 |10|3|
| Purple /4 |1|2|
| Orange /5 |1|4|
| Cyan /6 |7|3|
| Blue /7 |16|11|
| Gray /8 |0|0|

Colors use the recorded fixture, not ordinal color inference. T16 totals43
requests; T17 totals23. Both have zero explicit conversion704 packets, an
inconclusive statistic for default-order conversion. Private opportunity logs
are available for Red only:13 T16 episodes and1 T17 episode, all matched to
their exact default-order packet. Other players' absent private logs are not
evidence of inactivity. Mixed-warship episodes cannot all be relabeled boarding.

**Candidate actor32227, not conclusively typed as1880 by the replay:**

-21:27.708 default target31111; Red opportunity log identifies a Fishing Ship.
-22:44.896 same target;23:09.146 MOVE.
-23:15.042 default target31918; opportunity log identifies a warship.
-25:59.132 same target31918. Next recorded actor command is GUARD at58:32.728:
  approximately32m34s without an intervening explicit actor command.
-31918 continues receiving Blue orders, including29:23. This corroborates a
  still-enemy target in the observation window, but not an in-range conversion.

No actor STOP was found in this candidate lifecycle. Do not describe the early
failure as proven STOP spam or continuous escort retasking. Conversely, no new
packet does not exclude autonomous engine behavior, missing contact, or empty
faith. MAKE records have type/producer but no born instance ID; the candidate's
type and actual conversion state must not be asserted from timing alone.

## Deciding experiment / acceptance

Ask whether a manually issued conversion with this normal Boarding Ship has
ever succeeded; this fact is not recoverable from the supplied packet state.
If still unknown, use a small engine test, not another long eight-player match:

1. Newly created1880 against an ordinary enemy Fishing Ship and Scout Ship;
   fixed open-water geometry, no competing AI orders, known diplomacy/faith.
2. Compare direct human right-click with the AI's default target command.
3. If both fail, compare the **same1880 with only conversion range changed**
   from0 to1 in an isolated test, plus original Boarding Galley535 as a control.
   Do not modify the authoritative mod or installed runtime for this audit.
4. Observe exact source type/ID, target ID/owner, active action/order, separation
   and conversion progress/faith via a verified accessor or game UI. The local
   `object-data-faith` constant comment actually describes resistance; do not
   blindly treat it as a current-faith measurement.

Manual succeeds/AI fails isolates command/controller handling; only positive
range succeeds isolates range/contact mechanics; both native commands fail even
at positive range requires further conversion configuration/engine diagnosis.
Acceptance is an observed ownership change on each eligible target, followed by
bounded reuse without unrelated GUARD stealing an active conversion. The failed
runtime behavior remains OPEN until this distinction is demonstrated.

## Reproducible external artifacts

All under `G:\Projects\Codex\Rome at War AI\.analysis`:

- `audit_boarding_ship.py` (DAT extraction and exact replay reductions).
- `boarding-ship-dat-audit.json` (selected units/tasks/effects/resources).
- `p3b44t16-boarding-audit.json`, `p3b44t17-boarding-audit.json`.
- Existing `p3b44t16-exact.json`, `p3b44t17-exact.json`,
  `p3b44t16a2-runtime-control.zip`.

Validation: DAT extraction and both replay reductions **PASS**. Gameplay causal
test **NOT RUN**. No behavioral patch/full regression run is warranted for this
diagnostic-only turn. This audit is not a completed defect fix.
