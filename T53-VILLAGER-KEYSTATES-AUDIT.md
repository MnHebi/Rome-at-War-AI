# T53 Villager DUC writer audit

## Current policy amendment (2026-09-07)

The Phase A column below records the historical T53 experiment, not a blanket
prohibition on boarding investigation. The current explicit, per-command policy
is `villager-command-modifier-policy.json`, checked by
`tools/villager_command_policy.py`. It expands this family inventory to current
rule sites, including mixed migration hull/passenger exceptions.
Five mining-passenger initial/retry garrison writers now test Ctrl2; shared scout
paths remain unchanged. See `BOARDING-CTRL-EXPERIMENT.md` for scope and acceptance.

This audit was completed before the T53 behavioral experiment. It covers every
current `up-target-objects` / `up-target-point` family whose local list is known
from source to contain, or can retain, a Villager. The complete all-object
inventory remains `OWNERSHIP-SOURCE-INVENTORY.md`; entries below are the
Villager-capable subset and are grouped only when generated/retry rules have the
same ownership and command contract.

## Reference result

The authoritative cached AIRef snapshot
`G:\Projects\Codex\Rome at War AI\.analysis\airef-reference-20260830.js`
(SHA-256
`5AA1EF72D01BAB33C1A60189FEADE0AFE37D4209ED816E7B70EEFD914B8BC0C8`)
documents `sn-keystates` as DE-effective, range 0-3: 0 none, 1 Shift,
2 Ctrl, 3 Ctrl+Shift. It applies to `up-target-objects` and
`up-target-point` at command issuance, may safely be restored immediately, and
describes Ctrl as targeting more directly/being less likely to retarget.

AIRef also records a material carry boundary: Ctrl reassignment can drop a
Villager's carried resource and immediately change `object-data-gather-type`.
The experiment therefore admits only `object-data-carry <= 0` workers. A
carrying worker remains under its current economy task and can be reconsidered
by a later bounded five/fifteen-second farm-staffing pass.

The theory that an ordinary DUC right-click is conflicting with native Villager
assignment remains a hypothesis. These semantics justify a controlled test;
they do not prove that mechanism or the order-706 root cause.

## Villager-capable writers

| Source / state family | Classification | Local Villager contract | T53 Phase A |
|---|---|---|---|
| `rawai-homebase.per` `FARM-STAFFING-CHECK-FISHERMAN` -> Farm | ECONOMIC RESOURCE ASSIGNMENT | One unreserved, same-zone, zero-carry `villager-fisherman`; exact completed Farm | **YES**, writer 1 |
| `rawai-homebase.per` `FARM-STAFFING-CHECK-IDLE` -> Farm | ECONOMIC RESOURCE ASSIGNMENT | One unreserved, same-zone, idle, zero-carry Villager; exact completed Farm | **YES**, writer 2 |
| `rawai-homebase.per` `FARM-STAFFING-ASSIGN` -> Farm | ECONOMIC RESOURCE ASSIGNMENT | One unreserved, same-zone, zero-carry economic Villager after builder/repair/hunt/special-role exclusions; exact completed Farm | **YES**, writer 3 |
| `rawai-homebase.per` `FARM-STAFFING-FIND-RESOURCE` -> Gold/Stone/tree | ECONOMIC RESOURCE ASSIGNMENT | Exact excess `villager-fisherman`, revalidated unreserved/zero-carry; exact same-zone observed resource | **YES**, writer 4; target type/class distinguishes Gold, Stone and tree |
| `rawai-homebase.per` `COLONY-TC-ASSIGN` | ECONOMIC BUILD/REPAIR | Nearby same-zone settlers assigned to a concrete pending Town Center | No: builder behavior |
| `rawai-homebase.per` `PLACEMENT-VALIDATE-FOUNDATION-RESOURCE` (Lumber Camp) | ECONOMIC BUILD/REPAIR | Up to two nearby wood workers assigned to the exact validated foundation | No: builder behavior |
| `rawai-hunt.per` `BOAR-COMMIT-RESCUE-SEND-SIX/SEVEN` | ECONOMIC RESOURCE ASSIGNMENT | Bounded emergency hunters ordered to an exact boar | No: protected boar-rescue path, not ordinary role conversion |
| `rawai-hunt.per` `BOAR-COMMIT-RESCUE-GARRISON-SEND` | TRANSPORT/GARRISON | Exact lurer sent to a verified Town Center refuge | No |
| `rawai-general.per` two temporary-worker repair/enter cleanup rules | STOP/RELEASE | Ungrouped Villagers with stale attack/build/repair/enter orders | No |
| `rawai-economy.per` `TRADE-RETIRE-CHECK` | OTHER | One safe idle non-food Villager deleted at a proven population/trade transition | No |
| `rawai-military.per` migration rendezvous, issue/reissue-board and owner-recovery families | TRANSPORT/GARRISON | Reserved `migration-boarding-group` settlers/scout boarding the exact reserved Transport | No |
| `rawai-military.per` migration partial/abort/check/retire/landing cleanup families and `rawai-exploration-policy.per` `MIGRATION-RETIRE-SCOUT` | STOP/RELEASE | Reserved migration passengers stopped/released only at bounded terminals | No |
| `rawai-military.per` migration passenger rendezvous/scout patrol families | MOVEMENT | Reserved migration passenger/scout movement | No |
| `rawai-military.per` `MIGRATION-RETURN-DEPOSIT` | OTHER | Carrying returned settlers right-click a home Town Center to deposit cargo | No: carry semantics are intentionally opposite to Phase A |
| `rawai-military.per` `MIGRATION-WAIT-DROPSITE-CLEAR` and `MIGRATION-ASSIGN-RETASK-ANCHOR` | ECONOMIC RESOURCE ASSIGNMENT | Landed reserved settlers begin/continue harvesting an exact island resource | No: audited Phase B candidates; autonomous migration is protected |
| `rawai-military.per` `MIGRATION-ASSIGN-DROPSITE` | ECONOMIC BUILD/REPAIR | Landed reserved settlers assigned to the exact pending drop-site foundation | No |
| `rawai-military.per` `MIGRATION-DROPSITE-FAILED` | TRANSPORT/GARRISON | Failed-colony settlers reboard the exact migration Transport | No |
| `rawai-military.per` `TRANSPORT-REPAIR-TASK` | ECONOMIC BUILD/REPAIR | Up to two idle free Villagers repair an exact damaged Transport | No |
| `rawai-military.per` two `LOCAL-RESPONSE-COMMAND` wall/gate-builder paths | DEFENSE/COMBAT then TRANSPORT/GARRISON | Exposed perimeter builders are stopped and sent to a verified Town Center refuge | No |

## Explicitly excluded non-Villager families

Assault mission/boarding/recovery groups are populated only from military
classes; landed-assault commands therefore cannot contain Villagers. Relic
ferry commands select a Priest. Fishing policy selects Fishing Ships. Naval
scout, escort, siege, right-of-way and merchant controllers select vessels.
The Dejbjerg controller selects its mobile wagon. Taunt/severe/local military
responses select military classes. Building/foundation delete writers target
buildings. These writers are covered by the complete inventory but are not
Villager-capable and receive no T53 modifier.

## Experiment boundary

In the original T53 Phase A, only writers 1-4 received Ctrl command issuance. Writer 4 covers three
separately observable target families, so the requested five behavior paths are
Fisherman-to-Farm, Fisherman-to-Gold, Fisherman-to-Stone,
Fisherman-to-tree, and free/idle economic Villager-to-Farm. Apart from the
explicit zero-carry eligibility boundary above, target searches, ownership,
action, stance and five/fifteen-second retry policy remain unchanged.
Those original exclusions were experimental scope, not assessed modifier
semantics. The current amendment explicitly admits five mining boarding sites;
all other exceptions remain unchanged until assessed by command family.
