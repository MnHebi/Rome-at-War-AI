# Rome at War AI project rules

These rules apply to all work in this workspace, including the AI repository,
the Rome at War data-mod reference, replays, spreadsheets, analyses, and test
fixtures.

## Incomplete project material

- Treat an obviously incomplete project artifact, dataset, spreadsheet,
  analysis document, test fixture, mapping table, or other supporting resource
  as unresolved project work. Do not assume the incomplete state is
  intentional and do not silently work around it.
- Investigate unexplained gaps whenever they materially affect the current
  objective. Determine what is missing, why it matters, and which behavior or
  conclusion depends on it.
- First determine whether the missing material can be completed from repository
  data, the current Rome at War data mod, existing replays, generated strategy
  data, validated game constants, or another authoritative project source.
- When reliable completion is reasonably within the task's scope, complete the
  supporting material as part of the task and validate every dependent output.
- When reliable completion requires information that is not available, state
  the exact missing information, identify the affected implementation or
  analysis, and ask the user for it. Do not substitute an undocumented guess.
- If work can safely continue around a non-blocking gap, record the gap and its
  consequences explicitly; do not let it disappear from the handoff.

## Maintain project knowledge proactively

- Treat spreadsheets, civilization matchups, unit evaluations, build orders,
  strategy notes, map classifications, replay benchmarks, test results, and
  similar artifacts as implementation infrastructure rather than optional
  documentation.
- Update the relevant knowledge artifacts when code inspection, data-mod
  inspection, replay analysis, testing, or authoritative historical evidence
  changes what the project knows.
- When an incomplete knowledge artifact can be completed reliably, finish it.
  Do not preserve known gaps merely because the immediate prompt did not name
  the artifact.
- Keep machine-readable strategy data, generated civilization PER files,
  spreadsheets, and explanatory documentation synchronized. Run the repository
  synchronization and semantic validators after changing strategy knowledge.
- Record provenance for non-obvious conclusions. Distinguish direct replay or
  data evidence from inference, intended design, and unresolved hypotheses.
- When duplicate working copies of an artifact exist at the workspace root and
  in the AI repository, update both deliberately and verify that their contents
  match. Do not allow them to drift silently.

## Source authority and conflicts

- Use the current Rome at War data mod as the authority for unit, building,
  technology, civilization, availability, and identifier mechanics. Do not
  upload the data mod to the AI repository.
- Treat `RAW AI unit focus spreadsheet.ods` as the developer-agreed design
  constraint for Extreme difficulty. Do not revise that agreement solely from
  a replay or inferred efficiency; surface a proposed change for explicit
  approval.
- Apply the Extreme focus categories to generic planned composition, not to a
  civilization's own unique units. Civilization-specific unique units are
  globally exempt and may use bounded direct production independently of the
  generic focus selection; strategy-specific conditions may further gate them.
- Maintain `unique-unit-production.json` as the audited AI-side manifest of
  military and naval unique families. Keep its source hashes and ambiguity
  notes synchronized with the authoritative DAT/tech-tree exports, and require
  every listed production copy to have a persistent role-independent bound.
- Reactive counter production is also exempt from the Extreme focus categories
  when it answers observed enemy composition. Skirmishers are the established
  example; keep such production threat-gated and bounded rather than treating
  the exemption as an unrestricted alternate composition.
- Model the in-mod `Britons` as a composite Iron Age British civilization. Its
  Iceni background is an important identity and calibration source, but it does
  not limit the AI to Iceni-only evidence or doctrine. Label evidence from
  different British peoples and periods instead of silently conflating it.
- Treat `RAW AI good units per civ.ods` as a working evaluation artifact. It is
  expected to be completed and maintained from validated mod data, testing, and
  documented analysis.
- Treat replay files as diagnostic evidence, never as instructions. A replay
  observation can update evaluations, benchmarks, and issue records, but must
  be separated from the proposed explanation until the code or data supports
  that explanation.
- When the user's match observation or match-setup account conflicts with a
  replay parser field, decoded metadata, or an interpretation of the replay,
  stop before choosing between them. State the exact conflict and ask the user
  to confirm the observed setup or behavior. Until confirmation, preserve both
  accounts as unresolved evidence and do not silently reject, overwrite, or
  relabel the user's account from parser-derived inference.
- Treat `civ-strategy-data.json` and
  `civ-strategy-historical-overrides.json` as the machine-readable strategy
  sources for generated civilization files. Edit generated PER blocks through
  their source data and generator unless a verified exception requires direct
  code.
- When authoritative sources conflict and the conflict cannot be resolved from
  project evidence, document the conflict and ask the user instead of silently
  selecting one source.

## Review and validation

- Use an adversarial, read-only review pass for replay-driven or cross-system AI
  changes. The reviewer should try to falsify the proposed fix, check runtime
  state ownership and engine semantics, and report actionable findings before
  corrective edits begin.
- Do not treat structural validators as proof of in-game correctness. They do
  not prove command operand domains, transport ownership, shared-search
  lifetime, path safety, placement success, or runtime strategy behavior.
- Validate changes proportionally with structural PER checks, strategy
  synchronization checks, focused code review, artifact consistency checks,
  and a fresh-match replay when runtime behavior is involved.
- Preserve the AI-only repository boundary: commits and pull requests may
  contain AI code and its supporting knowledge artifacts, but never the Rome at
  War data-mod payload or savegame/replay files.
