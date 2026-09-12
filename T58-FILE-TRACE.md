# T58 file-observer candidate

**T58/506 ENGINE STARTUP FAILED;507 REPAIR DEPLOYED, STARTUP PENDING.**
See `T58A-RULE-CAPACITY-REPAIR.md`: shared emitter fixes excessive compiled rules;
the record/roster contract below remains unchanged. Historical physical counts
and costs below describe506, not507.
**VILLAGER COMMAND FLOOD — INVESTIGATING.** T58/506 deployed2026-09-12;
see `T58-DEPLOYMENT.md` for installed identity and frozen source map. Former
installed experiments are reconciled in source. No Steam-option change, game
launch or termination was performed by the agent. User startup failed ERR6001;
no usable engine delivery was demonstrated.

## Findings and scope

T57 failed at two distinct boundaries: zero720/721 headers and609 orphan762
ends; available boarding snapshots72 calls/65 nonempty/zero detailed selections.
Neither a larger allowance nor the observed50-message timestamp group explains
these failures. The latter is not an established engine limit.

Source requires a valid previously selected object before the old capture can
proceed. List-based commands do not require that pointer. This is an unnecessary
prerequisite for **invocation logging**, but the historical evidence does not
identify which gate rejected each T57 call. T58 emits ENTRY before that test and
does not use legacy phase/credit selection. Invalid saved pointers produce an
explicit gap without changing selection, and the original command still runs.
The old phase/credit fields are retained as retired-policy inputs, not portrayed
as a still-running shadow scheduler or proof of T57's failed gate.

The old detailed720-family chat observer is replaced, not run alongside the file
observer. Existing separate boarding-Ctrl experiments/counters remain unchanged.
Only one compact RAW12 diagnostic790 warning is added on first observer failure.

The deployed registry contains576 rules and814 observed command/setting/lifecycle
sites, including207 direct final-list DUC commands. This deliberately includes
non-Villager/mixed sites rather than silently excluding possible worker writers.
The initial75-entry inventory preserved the source command digest. Deployment
reconciliation removes the STOP already absent from installed T57, yielding74
entries; the remaining modifiers are unchanged. The registry retains original rules,
command expressions, hashes, file locations, command indices and old boarding
writer20/21/23/24/25 mappings. Native/indirect sites have UNKNOWN recipients.

All final local and remote entries are enumerated, including repeated IDs and
empty invocations. The supported selector indices0..240 cover241 entries, not32
or two. A larger reported list yields TRACE_INCOMPLETE, never claimed complete.
Remote lists and targeting mode are inputs, not a claim that every actor targets
remote index0. Point commands copy current coordinates, not just a point goal ID.

## API and physical safeguards

Verified against [AIRef up-log-data](https://airef.github.io/commands/commands-details.html#up-log-data)
and its backing commands.js. `up-log-data 0` formats one `%d` value; mode1 is plain
output. DE uses engine logging, not the legacy aoelog.txt destination. No file
handles, flush/rotation API or outgoing-native-packet hook is invented.

`up-get-search-state` writes four contiguous private goals. Invalid target
selectors leave the previous selection unchanged: every object field is first
set to-2 and read only after a successful selection. Deep inspection requires a
restorable saved object ID. No search/list/filter, shared point, gameplay goal,
strategic number, timer, ownership or command policy is changed by observation.
If that saved object disappears during inspection, failure3 is explicit; engine
preflight must test this lifetime boundary. A fixture cannot prove engine timing.

Original predicates execute once. Original gameplay actions stay in order;
`disable-self` belongs to the original predicate rule and still affects the next
pass. Original relative jumps are relocated to the same original destination;
unsupported dynamic/conditional-crossing cases fail generation. Physical rules,
not just stripped semantic rules, receive structural validation. Other generators
apply the same verified registry decoration and refuse changed originals.

Startup is special: customconstants and init-goals execute before the shared
logger. Thirteen one-shot setting/initialization sites use private per-site
pre/post/time journals, flushed after logger initialization. They never jump into
an uninitialized subroutine. Private definitions and initialization load first;
the original gameplay initialization order is preserved. These are native-setting
journals, not fabricated DUC recipient lists.

Private scalar goals start10000; startup journal starts10200;400 roster entries
use three goals each at10500..11699. Existing named goal allocations and contiguous
outputs are checked for overlap. The eight reused player strings bring this
**source candidate** to1496/1500 literals. The installed-exception payload must be
counted again before any future deployment; its historical1489 count is not this
source baseline. Player identity is read with `up-get-fact my-player-number`, not
guessed from engine-log prefixes or the numeric value of a symbolic player token.

## Migration and state coverage

All observed self-owned migration-group members enter a400-slot private roster.
Group mutation boundaries capture additions/removals; stage/hull writes emit
site-tagged records, and periodic records retain actual group, action/order,
intent target, carry, garrison state and cargo count. Acquisition/rendezvous,
loading/departure/unload, dropsite/recovery/cancellation/release remain the existing
state machine; the observer does not drive transitions.

Every tracked member and associated hull is sampled at most once per game second,
even without another command. Freshness uses `game-time` seconds, not the unrelated
system timestamp. Released members remain observable until more than60 seconds
since their last observed reservation (one-second sampling granularity). Hulls
and actors have separate positions; enter intent/separation is not path progress.
Reused roster holes cannot duplicate an existing tracked actor. Converted actors
do not refresh self-owned reservation lifetimes. Missing/hidden actors remain-2,
not stale data. Capacity400 emits explicit failure4 and does not evict silently.

Limitations: an invalid saved selection prevents safe deep/periodic capture for
that invocation; hidden garrisoned objects may fail selection; exact membership
between observations is not reconstructed. These gaps must remain visible in
the runtime evidence. Observed hull cargo is a count, not an invented passenger
identity list. Initial effective native settings plus every identified setting
writer are logged; periodic checks detect untagged changes. No settings change.

## Format and parser

Every physical value has a reusable `RAW58P1` through `RAW58P8` prefix. Logical
record, before escaping:

```text
BEGIN schema system-session record-sequence invocation type site game-seconds payload-count
payload...
logical-token-count rolling-checksum invocation END
```

BEGIN=-2147483001; END=-2147483002; ESCAPE=-2147483003. BEGIN/ESCAPE occurring as
data are escaped losslessly. Signed32 values remain intact. Checksum is a rolling
mod65521 delivery check, not cryptographic authentication. Per-player record and
invocation sequences are monotonic; system-session is only a disambiguator, not
simulation milliseconds. Separate captures must not be concatenated as one match.
Startup40 embeds eight signed words of the source-map SHA256. This is not a full
runtime hash: preserve a matching per-file installed manifest as well.

| Type | Meaning / payload |
|---|---|
|1|ENTRY: kind, local/remote counts, savedID/valid, mode, reservedHull, migrationState, ten legacy gate fields, four command operands, pointY, modifier|
|2|Observer complete; kind. Kind2 means INVOKED, never packet acknowledgment|
|10/11|Local/remote index, valid, object fields|
|12|Local/remote selector, index, actual intent-target ID/type/class/player/X/Y|
|20|Roster slot, actor, reserved hull|
|21|Periodic slot, actor, hull, valid, actor fields|
|22|Slot(-1 at command boundary), hull, valid, hull fields|
|23|Post-release expiry: slot, actor, hull, last reservation observation|
|30/31|Changed setting index/value / settings after a scripted writer|
|32|Migration stage and reserved hull after a lifecycle writer|
|40/41|Source-map identity / deferred startup site,time,pre,post journal|
|90|TRACE_INCOMPLETE:1 invalid saved pointer;2 list limit;3 failed restore;4 roster limit|

Object fields in order: ID,type,class,player,preciseX,preciseY,action,order,targetID,
garrisoned,carry,groupFlag,garrisonCount. ENTRY kinds:0 startup;1 direct PRE;
2 INVOKED;3 indirect PRE;4 periodic POST;5 mutation POST;6 settings POST;
7 lifecycle POST. The last three also confirm control passed through their
original operation. Retired gate order is enabled,capture,b-turn,phase-valid,
phase-time,observation-due,early,middle,late,final credits.

`command_boundary_log.py` streams logs with one bounded buffer per player.
It rejects malformed shapes, missing tails, duplicates, sequence mismatches and
missing subrecords. It verifies complete list indices/counts before writer joins.
PRE plus corresponding INVOKED is required. Packet arrays may be native-expanded
subsets; multiple matches are ambiguous, no match is not native-origin proof.
Whole game-second buckets are not fabricated millisecond timestamps. Missing or
mismatched startup identity blocks joins. Records/correlations stream to JSONL.

## Offline result, not fresh runtime acceptance

Corrected T57 cache reduction: ORDER113143 packets/114827 incidences;
WORK306881/313373;70623516/51256; explicit STOP250/631 across the full cache.
These total STOPs are not STOPs attributed to the affected workers.
Dense ORDER retains >=100 packets with <=100ms gaps and the same target;
sustained706 retains >=100 with <=1000ms gaps; additional WORK definition is
>=100 same-target packets with <=1000ms gaps. Families remain separate.

The earliest relevant Orange timelines remain34329 ORDER33:26.344 following
writer24 retry33:26.311;33901 ORDER33:29.604 following retry33:29.589. The output
contains exact last assignments, boarding packets, first ORDER/WORK/706 and later
packet-state changes. A last packet is not inferred recovery/death. Repeated
same-signature packets retain first/last sequence and count.

Targets34365/35071 have11691/20297 cached references but no explicit usable
type/owner link; initial controls are absent. Construction intents without an
instance-ID association do not classify them. Both remain UNKNOWN.

Matched same-hull results remain778 no706-observed,5 onsets,2 already active and
126 censored. The negative label is now
`no706-observed-ORDER-WORK-not-excluded`; it does not mean no command flood or
successful boarding. Follow-up/DELETE/actor-observation censoring and cohort
limitations are retained. No historical final list is reconstructed from T58.

External artifacts under workspace-root `.analysis`: `t58-offline-t57.json`,
`t58-source-manifest.json`, `t58-static-cost.json`, `t58-full-validation.txt`.
Original replay/cache/logs are not committed.

## Engine preflight procedure — not executed

1. Deployment authorized and completed: T58/506 with both experiments reconciled.
   Use the manifest and frozen registry in `T58-DEPLOYMENT.md`, not historical
   b4f0e2c identity. Confirm hashes and startup40. Steam launch-option changes
   still require authorization; deployment did not change those options.
2. Preserve all existing Steam options. Add exactly the case-sensitive options
   `LOGSYSTEMS=AIScript VERBOSELOGGING CONSTANTLOGGING` when authorized. Use normal
   game speed and the authoritative lobby setup. Do not delete any old logs.
3. Locate actual new engine-produced files by timestamp/growth (usual parent is
   the game's `logs` directory; do not assume a filename). At startup, inspect
   startup40 and journals41 immediately. Do not wait30 minutes for migration.
4. Parse chronological segments from this capture, with the installed manifest:

```powershell
py -3.12 tools/command_boundary_preflight.py manifest "G:\Projects\Codex\Rome at War AI\.analysis\t58-source-manifest.json"
py -3.12 tools/command_boundary_log.py --logs "<actual-log-file>" --manifest "<verified-installed-manifest.json>" --output "<capture-report.json>" --expected-players 1 2 3 4 5 6 7 8 --wall-seconds <measured-wall-duration>
# Later, add --cache "<matching-corrected-replay-cache.json>" for correlation.
py -3.12 tools/command_boundary_preflight.py assess-cache "G:\Projects\Codex\Rome at War AI\.analysis\t57-exact.json" "G:\Projects\Codex\Rome at War AI\.analysis\t58-offline-t57.json" --supplement "G:\Projects\Codex\Rome at War AI\.analysis\t57-supplement.json"
```

5. Delivery PASS requires every participating AI's correct startup identity,
   complete multi-actor/multi-target records and repeated/interleaved records
   without invented reconstruction. Check complete indices, not merely a nonzero
   ENTRY count. Verify an ordinary command actually executes with tracing on.
6. At the first real boarding episode require usable PRE/INVOKED/state records OR
   explicit failed-gate evidence. Zero unexplained samples is FAIL. Record actor
   and hull movement/cargo separately; do not call a garrison intent boarding.
7. Basic delivery failure: stop requesting long investigation matches, preserve
   files and diagnose. Do not automatically terminate the game. Boarding/gathering
   health and unchanged explicit Ctrl paths remain ordinary-match acceptance.

Read-only growth monitoring (run two snapshots, no background automation):

```powershell
py -3.12 tools/command_boundary_preflight.py snapshot "<before.json>" --logs "<actual-log-file>"
py -3.12 tools/command_boundary_preflight.py snapshot "<after.json>" --logs "<actual-log-file>" --previous "<before.json>"
```

Archive matching untouched logs, replay and manifest together, retaining original
timestamps. No cleanup/rotation is performed by these tools.

## Cost and acceptance boundary

Static three-actor fixture:324 physical log lines/14 records/5851 evaluated rules
for a boundary; periodic sample228 lines/8 records/4107 evaluated rules. Synthetic
prefix sizes11616/8117 bytes are **not measured DE bytes**. The file library and
coverage contain6542/7229 physical rules; most startup/unchanged-setting blocks
are jumped over. Empty roster scanning stops at its high-water mark.

This is a substantial diagnostic workload. There is no match-lifetime allowance.
The parser reports per-game-second record rates; measured wall duration supplies
bytes/minute and a three-wall-hour storage projection. Snapshot tooling measures
actual growth/free space. Actual DE prefix cost, disk delivery, throughput and
slowdown are PENDING. Compare elapsed wall time versus simulation time at the
same speed/setup; never infer overhead from fixtures. If runtime cost is too high,
explicitly fail preflight and redesign delivery—not silently omit late episodes.

Runtime acceptance remains PENDING. Productive boarding/gathering plus actor-level
causal evidence is the goal; synthetic complete frames do not close the flood.

## Validation and reviewable payload

Historical snapshot below is immutable evidence for b4f0e2c, not the current
working payload. Current marker/whitespace maintenance and the user's Syracusan
edit are documented in `MAINTENANCE-CONSISTENCY.md`; regenerate the manifest.

Source commit: `b4f0e2ca245d3cfc1e51f6cb47ca592fbaf5c844`.
`T58-VALIDATION.json` records all109 committed runtime-file hashes, the source-map
fingerprint, working-copy differences, static costs and validation results.
Its aggregate algorithm is sorted filename + NUL + file SHA-256 + LF; do not
equate this with earlier deployment aggregate algorithms.

- Committed source: `009d7e6836620b147a5fd14edfea80c683633fa795d8bfdd423368a5537f5bcf`.
- Working source: `059c08055e3e9f4d24b10bb24398646541dcf59b14a00df896006defb32365e8`.
- Only runtime-file difference: pre-existing `rawai-init-goals.per` chat marker.
- Final Python3.12 discovery:646 run,644 PASS,2 retired chat-only skips,91.173s.
- Focused file-trace tests:17 PASS; physical PER,1052 ownership sites, modifier
  policy, generation, strategy/naval,42 replay benchmarks and context PASS.
- Six pre-existing generated-civ differences and frozen good-units provenance
  mismatch remain unchanged; they are not claimed as passing checks.

Final discovery log is external `.analysis/t58-final-validation.txt`.
Discovery ran in the canonical working copy with its preserved pre-existing
local changes; this is not a claim of a pristine committed-tree discovery run.
No engine files, installed files, launch options or gameplay policy were changed.
