# T58B: allied-base landing as last choice

Status: **FIXED-PENDING-RUNTIME**. Local candidate508 only; not deployed.
Canonical branch: `fix/trade-cog-cap-dacian`, HEAD `a635d5598a6d292a9571d14abd178b669189b345` plus preserved working changes.

## Source boundary and requested change

The existing planner exhausts candidate beaches, alternative enemy objectives,
and enemy-plan failure/deadline limits before `AP-ENEMY-FAILED` cools/rotates the
opponent. It never searches an allied base as a landing anchor. This establishes
the missing policy, not proof that a usable allied shore existed in any old
replay. T58A Yellow50457's eight accepted loads without a slot commit remain
historical evidence of repeated rejection, not runtime acceptance of this patch.

The user requested a final allied-base fallback. The implementation inserts it
at exhausted enemy-plan handling, before cooling/rotating that opponent:

1. Retain the accepted full/useful-partial manifest, exact owned hull, hostile
   opponent and original enemy objective.
2. Once per opponent per loaded mission, examine living allies (not self).
   Select the nearest ready, surviving Town Center on the enemy objective's
   map-zone, at most one base per ally. No allies means the old immediate
   rotation/recovery behavior.
3. Resolve a shoreline from the allied TC anchor using the existing bounded
   coarse/refinement/lateral search. Do not replace the enemy objective with
   the allied TC, command allied units, or path-test the immobile building.
4. Retain hull-water/unload path tests, failed-coast exclusions, all-enemy
   defensive-fire checks, screening and bounded unscreened policy.
5. Require an exact land-path witness: an existing visible enemy mobile unit
   near the original objective must path to the candidate landing. The ordinary
   structure-only/no-witness exception is **not** allowed for allied fallback.
6. Revalidate the literal allied base's type/readiness, owner, diplomacy,
   survival and land-zone before screening and final departure approval.
   The unscreened acceptance path also passes through this final check, once.
7. If a coast fails, try the next bounded candidate/ally. Exhaustion resumes
   existing enemy rotation/recovery. The fallback gets at most120 game-seconds
   including screening, never extending the original360-second mission limit.
   Actual hull danger, invalid cargo and lost ownership still take precedence.

The120-second local allowance accommodates the existing two screening waits;
the original per-enemy180-second timeout does not immediately cancel the final
option it just triggered. No existing voyage, boarding or total-mission timer
was increased. The three dispatched slots and landed combat controller are
unchanged: they receive the original enemy target and the new landing point.

## Diagnostics and generated source

Existing `RAW plan` events gain reasons42 trial,43 invalid ally/base,44 exhausted
allies,45 no land witness,46 accepted allied landing,47 local budget exhausted.
Trial/acceptance include hull, ally and base identities; acceptance includes the
enemy objective, landing coordinates and witness. Lost bases emit reason43.
Existing failed-approach events retain coordinates/reasons.
These are bounded transition events, not per-sweep output.

Implementation: `tools/generate_assault_plans.py`, generated
`rawai-assault-plan-defs.per`/`rawai-assault-plans.per`, and the narrow final
check in `rawai-assault-screen-fallback.per`.
Command-boundary registry/wrappers and Villager-policy line references were
regenerated deliberately.579 registered rules/817 commands; new command sites
only reuse existing screen-release behavior. Frozen507 registry remains the
authority for old logs. Existing Ctrl, diagnostic, migration and cap4 changes
were preserved; no civilization doctrine regeneration was performed.

## Validation and protected behavior

Focused:14 new executable-PER fixture tests PASS;31 existing planner tests PASS.
New coverage includes normal-plan non-interference, actual direct-coast
exhaustion,5/9/10 accepted cargo, original enemy/slot preservation, next ally,
wrong-zone/self/neutral/dead/packed/unfinished bases, exact cliff rejection,
no-witness rejection, hostile coast, successful screening, final unscreened
base loss, original total deadline and hull-emergency precedence.

All131 assault tests PASS, including the committed-voyage graph invariant.
An initial final-check integration produced a departure-to-planning edge;
it was replaced with a pre-departure acceptance state, not a weaker assertion.
PER structure/operands and generator synchronization PASS. Physical load
matrix:9312/10000 rules,688 headroom. Project literal budget:1498/1500; this
budget is not a claim about undocumented engine allocation. No more strings
should be added without reclaiming budget. Final full Python3.12 discovery:
683 run,681 PASS,2 retired skips in98.462s (outside sandbox for temporary-file
fixtures). Initial sandbox fixture denials and a74-byte hot-context overflow
were resolved/revalidated; no assertions were weakened. Context metadata and
`git diff --check` PASS. All109 installed507 hashes remain unchanged.

## Runtime acceptance and unresolved limits

Fresh verified508 runtime must show direct approaches failing, reason42 on the
same accepted hull, reason46 followed by an actual slot commit, autonomous
unload near the ally and land advance toward the original enemy. It must also
retain ordinary direct assaults, partial manifests, three-slot independence,
danger refusals and bounded recovery. Static path fixtures are not engine proof.

This deliberately uses one ready TC per ally, not arbitrary allied buildings
or every TC. An inland TC beyond the resolver's bounded reach may fail even
when another allied coastal site exists. No visible objective-region mobile
witness means rejection, not permission. The existing witness is proximity-
bounded around the objective (80 tiles); it is not a simulation of every
passenger's path or guaranteed exact engine unload tile. Prior cliff/unload,
preparation, migration and flood defects remain open. No broad redesign or
claim that this guarantees a viable allied route in every match.
