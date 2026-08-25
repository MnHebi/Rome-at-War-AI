#!/usr/bin/env python3
"""Generate match-relative naval doctrine from good-unit-evaluations.json."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_SCORE_SCALE = 100


def runtime_score(capability_score: float) -> int:
    """Preserve the evaluator's two-decimal score in integer PER goals."""
    return int(round(capability_score * RUNTIME_SCORE_SCALE))


def competitive_enemy_ceiling(capability_score: float) -> int:
    """Largest scaled enemy score for which own/enemy remains at least 85%."""
    return min(
        100 * RUNTIME_SCORE_SCALE,
        math.floor(runtime_score(capability_score) / 0.85),
    )


def compact_scores(document: dict[str, Any]) -> dict[str, Any]:
    civilizations: dict[str, Any] = {}
    for key in document["display_order"]:
        civ = document["civilizations"][key]
        navy = civ["ratings"]["Navy"]
        score = runtime_score(navy["capability_score"])
        civilizations[key] = {
            "civilization": civ["civilization"],
            "host_civilization_constant": civ["host_civilization_constant"],
            "capability_score": navy["capability_score"],
            "runtime_score": score,
            "rating": navy["rating"],
            "steady_state_capability_score": navy["steady_state_capability_score"],
            "lineup_completeness_score": navy["lineup_completeness_score"],
            "ship_class_quality_score": navy["ship_class_quality_score"],
            "support_upgrade_score": navy["support_upgrade_score"],
            "production_throughput_adjustment": navy["production_throughput_adjustment"],
            "fleet_throughput_multiplier": navy["fleet_throughput_multiplier"],
            "shipyard_work_rate": navy["shipyard_work_rate"],
            "shipyard_throughput_multiplier": navy["shipyard_throughput_multiplier"],
            "primary_navy_doctrine": civ["good_navy"],
            "competitive_enemy_ceiling": competitive_enemy_ceiling(navy["capability_score"]),
            "has_quadrireme_or_quinquereme": navy["has_quadrireme_or_quinquereme"],
            "has_octeres": navy["has_octeres"],
            "specialist_support_detachment": navy["specialist_support_detachment"],
            "ship_classes": {
                name: {
                    field: record[field]
                    for field in (
                        "available",
                        "unit_id",
                        "unit_name",
                        "tier_multiplier",
                        "combat_ratio",
                        "number_multiplier",
                        "number_adjusted_ratio",
                        "lineup_points",
                        "quality_points",
                        "throughput_multiplier",
                        "production_source",
                        "production_work_rate",
                        "production_batch_size",
                        "production_resource_cost_per_ship",
                        "potential_production_source",
                        "potential_throughput_multiplier",
                        "potential_production_work_rate",
                        "potential_production_batch_size",
                        "potential_production_resource_cost_per_ship",
                        "upgrade_tech_ids",
                        "applied_upgrade_tech_ids",
                        "forced_upgrade_from_unit_ids",
                        "statistics",
                        "reference_statistics",
                    )
                    if field in record
                }
                for name, record in navy["ship_classes"].items()
            },
        }
    return {
        "schema_version": 1,
        "score_model": {
            "lineup_completeness_max": 30,
            "ship_class_quality_max": 50,
            "support_upgrade_max": 20,
            "production_throughput_adjustment_range": [-5, 5],
            "competitive_ratio": 0.85,
            "runtime_score_scale": RUNTIME_SCORE_SCALE,
            "rating_thresholds": {"Excellent": 80, "Good": 70, "Mediocre": 60, "Bad": 0},
            "doctrine_separation": "Naval Yes/No is not a capability grade. It is a runtime doctrine override: Naval Yes owns primary team fleets, while Naval No uses support fleets rather than contesting Naval Yes enemies one-for-one.",
            "score_scope": "Fully upgraded steady-state fleet capability plus a signed production adjustment from paths the AI currently operates. Missing Conscription is counted; validated Cothon batch potential remains recorded but is excluded until the AI has a Cothon construction and batch-production implementation. Research cost/time and age-of-unlock readiness require separate calibration.",
            "cothon_identifier_resolution": document["score_model"]["cothon_identifier_resolution"],
        },
        "source_provenance": document["source_provenance"],
        "naval_upgrade_chains": document["naval_upgrade_chains"],
        "display_order": document["display_order"],
        "civilizations": civilizations,
    }


def water_fact(indent: str = "\t") -> list[str]:
    return [
        f"{indent}(or",
        f"{indent}\t(goal map-type LAKE)",
        f"{indent}\t(or",
        f"{indent}\t\t(goal map-type RIVERS)",
        f"{indent}\t\t(or",
        f"{indent}\t\t\t(goal map-type ISLANDS)",
        f"{indent}\t\t\t(goal map-type TEAM-ISLANDS)",
        f"{indent}\t\t)",
        f"{indent}\t)",
        f"{indent})",
    ]


def rule(facts: list[str], actions: list[str]) -> list[str]:
    return ["(defrule", *facts, "=>", *actions, ")", ""]


def render(document: dict[str, Any]) -> str:
    order = document["display_order"]
    civs = document["civilizations"]
    if len(order) != 34 or set(order) != set(civs):
        raise ValueError("Expected 34 synchronized civilization capability records")

    lines = [
        "; AUTO-GENERATED by tools/sync_naval_capabilities.py. DO NOT EDIT.",
        "; Capability comes from the current external DAT/tech tree; good-navy",
        "; remains the strategic team-owner/enemy-deterrence doctrine override.",
        "",
    ]

    # Compile-time enemy symbols can include multiple opponents.  These rules
    # monotonically retain the maximum opposing score and whether any opposing
    # civilization carries the primary-navy doctrine.
    for key in order:
        civ = civs[key]
        host = civ["host_civilization_constant"]
        enemy_symbol = f"UP-{host}-ENEMY"
        score = runtime_score(civ["ratings"]["Navy"]["capability_score"])
        lines.extend([f"#load-if-defined {enemy_symbol}", ""])
        lines.extend(
            rule(
                [f"\t(up-compare-goal gl-enemy-max-naval-capability c:< {score})"],
                [f"\t(set-goal gl-enemy-max-naval-capability {score})"],
            )
        )
        if civ["good_navy"]:
            lines.extend(
                rule(
                    ["\t(true)"],
                    ["\t(set-goal gl-enemy-primary-navy YES)", "\t(disable-self)"],
                )
            )
        lines.extend(["#end-if", ""])

    # Host-specific score publication and relative comparison threshold.  A
    # Naval No fleet is competitive only when it is at least 85% as capable as
    # the strongest known opposing Naval No fleet.
    for key in order:
        civ = civs[key]
        host = civ["host_civilization_constant"]
        navy = civ["ratings"]["Navy"]
        score = runtime_score(navy["capability_score"])
        enemy_ceiling = competitive_enemy_ceiling(navy["capability_score"])
        specialist = "YES" if navy["specialist_support_detachment"] else "NO"
        lines.extend([f"#load-if-defined {host}", ""])
        lines.extend(
            rule(
                ["\t(true)"],
                [
                    f"\t(set-goal gl-own-naval-capability {score})",
                    f"\t(set-goal gl-naval-specialist-support {specialist})",
                    "\t(set-goal gl-naval-capability-ready YES)",
                    "\t(disable-self)",
                ],
            )
        )
        # One-on-one all-No comparison.
        lines.extend(
            rule(
                [
                    "\t(goal gl-naval-theater YES)",
                    "\t(goal team-game NO)",
                    "\t(goal good-navy NO)",
                    "\t(goal gl-enemy-primary-navy NO)",
                    f"\t(up-compare-goal gl-enemy-max-naval-capability c:<= {enemy_ceiling})",
                ],
                ["\t(set-goal gl-naval-role NAVAL-ROLE-COMPETITIVE)"],
            )
        )
        lines.extend(
            rule(
                [
                    "\t(goal gl-naval-theater YES)",
                    "\t(goal team-game NO)",
                    "\t(goal good-navy NO)",
                    f"\t(up-compare-goal gl-enemy-max-naval-capability c:> {enemy_ceiling})",
                ],
                ["\t(set-goal gl-naval-role NAVAL-ROLE-SUPPORT)"],
            )
        )
        # In an all-No team, begin with the strongest viable AI as the fleet
        # owner; a higher-scoring allied AI overrides this below.
        lines.extend(
            rule(
                [
                    "\t(goal gl-naval-theater YES)",
                    "\t(goal team-game YES)",
                    "\t(goal good-navy NO)",
                    "\t(goal gl-enemy-primary-navy NO)",
                    f"\t(up-compare-goal gl-enemy-max-naval-capability c:<= {enemy_ceiling})",
                ],
                ["\t(set-goal gl-naval-role NAVAL-ROLE-COMPETITIVE)"],
            )
        )
        lines.extend(
            rule(
                [
                    "\t(goal gl-naval-theater YES)",
                    "\t(goal team-game YES)",
                    "\t(goal good-navy NO)",
                    f"\t(up-allied-goal any-ally gl-own-naval-capability > {score})",
                ],
                ["\t(set-goal gl-naval-role NAVAL-ROLE-SUPPORT)"],
            )
        )
        lines.extend(["#end-if", ""])

    # Water-theater latch. Unknown/MegaRandom does not spend naval escrow until
    # the map classifier has produced a concrete water classification.
    lines.extend(rule(water_fact(), ["\t(set-goal gl-naval-theater YES)"]))
    lines.extend(
        rule(
            ["\t(goal map-type LAND)"],
            [
                "\t(set-goal gl-naval-theater NO)",
                "\t(set-goal gl-naval-role NAVAL-ROLE-UNASSIGNED)",
                "\t(set-goal upgrade-navy 0)",
                "\t(set-goal gl-naval-fleet-cap 0)",
                "\t(set-goal gl-naval-specialist-fleet-cap 0)",
            ],
        )
    )

    # Doctrine overrides run after relative-score election. Naval Yes civs own
    # primary team fleets. Naval No civs never attempt one-for-one competition
    # against such an enemy and yield to any allied primary owner.
    lines.extend(
        rule(
            [
                "\t(goal gl-naval-theater YES)",
                "\t(goal good-navy NO)",
                "\t(goal gl-enemy-primary-navy YES)",
            ],
            ["\t(set-goal gl-naval-role NAVAL-ROLE-SUPPORT)"],
        )
    )
    lines.extend(
        rule(
            [
                "\t(goal gl-naval-theater YES)",
                "\t(goal team-game YES)",
                "\t(goal good-navy NO)",
                "\t(up-allied-goal any-ally good-navy == YES)",
            ],
            ["\t(set-goal gl-naval-role NAVAL-ROLE-SUPPORT)"],
        )
    )
    lines.extend(
        rule(
            ["\t(goal gl-naval-theater YES)", "\t(goal good-navy YES)"],
            ["\t(set-goal gl-naval-role NAVAL-ROLE-PRIMARY)"],
        )
    )

    # Role-owned fleet caps and production permissions. These rules occur after
    # the legacy resource toggles in load order, so a resource check cannot
    # silently promote a support navy back into a full fleet.
    lines.extend(
        rule(
            ["\t(goal gl-naval-role NAVAL-ROLE-PRIMARY)"],
            [
                "\t(up-modify-goal gl-naval-fleet-cap g:= gl-ten-percent)",
                "\t(up-modify-goal gl-naval-specialist-fleet-cap g:= gl-ten-percent)",
                "\t(set-goal upgrade-navy 1)",
                "\t(set-goal train-scoutships YES)",
                "\t(set-goal train-remes YES)",
                "\t(set-goal train-fireships YES)",
                "\t(set-goal train-demoships YES)",
                "\t(set-goal train-hemiolia YES)",
                "\t(set-goal train-boardingships YES)",
            ],
        )
    )
    lines.extend(
        rule(
            ["\t(goal gl-naval-role NAVAL-ROLE-COMPETITIVE)"],
            [
                "\t(up-modify-goal gl-naval-fleet-cap g:= gl-eight-percent)",
                "\t(up-modify-goal gl-naval-specialist-fleet-cap g:= gl-eight-percent)",
                "\t(set-goal upgrade-navy 1)",
                "\t(set-goal train-scoutships YES)",
                "\t(set-goal train-remes YES)",
                "\t(set-goal train-fireships YES)",
                "\t(set-goal train-demoships YES)",
                "\t(set-goal train-hemiolia YES)",
                "\t(set-goal train-boardingships YES)",
            ],
        )
    )
    lines.extend(
        rule(
            [
                "\t(goal gl-naval-role NAVAL-ROLE-SUPPORT)",
                "\t(goal gl-naval-specialist-support NO)",
            ],
            [
                "\t(up-modify-goal gl-naval-fleet-cap g:= gl-three-percent)",
                "\t(up-modify-goal gl-naval-specialist-fleet-cap g:= gl-three-percent)",
            ],
        )
    )
    lines.extend(
        rule(
            [
                "\t(goal gl-naval-role NAVAL-ROLE-SUPPORT)",
                "\t(goal gl-naval-specialist-support YES)",
            ],
            [
                "\t(up-modify-goal gl-naval-fleet-cap g:= gl-three-percent)",
                "\t(up-modify-goal gl-naval-specialist-fleet-cap g:= gl-five-percent)",
            ],
        )
    )
    lines.extend(
        rule(
            ["\t(goal gl-naval-role NAVAL-ROLE-SUPPORT)"],
            [
                "\t(set-goal upgrade-navy 1)",
                "\t(set-goal train-scoutships YES)",
                "\t(set-goal train-remes NO)",
                "\t(set-goal train-fireships YES)",
                "\t(set-goal train-demoships NO)",
                "\t(set-goal train-hemiolia NO)",
                "\t(set-goal train-boardingships YES)",
                "\t(set-goal naval-attack-percentage 0)",
            ],
        )
    )

    # `warship-class` covers every scored combat hull except the class-53
    # Boarding Ship in the current DAT. Read both queue-aware counters and
    # publish their sum before common production is evaluated. Production
    # rules increment the sum immediately after queuing, preventing distinct
    # hull families or multiple Shipyards from overshooting in one rule sweep.
    lines.extend(
        rule(
            ["\t(goal gl-naval-capability-ready YES)"],
            [
                "\t(up-get-fact unit-type-count-total warship-class gl-naval-fleet-count-total)",
                "\t(up-get-fact unit-type-count-total boarding-ship gl-naval-boarding-count-total)",
                "\t(up-modify-goal gl-naval-fleet-count-total g:+ gl-naval-boarding-count-total)",
            ],
        )
    )

    # Common infrastructure overlay supersedes identical per-civ phase plans.
    for role, middle, imperial in (
        ("NAVAL-ROLE-PRIMARY", 4, 8),
        ("NAVAL-ROLE-COMPETITIVE", 3, 6),
        ("NAVAL-ROLE-SUPPORT", 2, 2),
    ):
        lines.extend(
            rule(
                [
                    f"\t(goal gl-naval-role {role})",
                    "\t(up-compare-goal current-phase c:>= 5)",
                ],
                [f"\t(up-modify-goal desired-number-shipyards c:= {middle})"],
            )
        )
        lines.extend(
            rule(
                [
                    f"\t(goal gl-naval-role {role})",
                    "\t(up-compare-goal current-phase c:>= 7)",
                ],
                [f"\t(up-modify-goal desired-number-shipyards c:= {imperial})"],
            )
        )

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evaluations", type=Path, default=ROOT / "good-unit-evaluations.json")
    parser.add_argument("--output", type=Path, default=ROOT / "rawai-naval-doctrine.per")
    parser.add_argument("--scores-output", type=Path, default=ROOT / "naval-capability-scores.json")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    document = json.loads(args.evaluations.read_text(encoding="utf-8-sig"))
    expected = render(document)
    expected_scores = json.dumps(compact_scores(document), ensure_ascii=False, indent=2) + "\n"
    if args.check:
        actual = args.output.read_text(encoding="utf-8-sig") if args.output.exists() else ""
        actual_scores = (
            args.scores_output.read_text(encoding="utf-8-sig") if args.scores_output.exists() else ""
        )
        if actual != expected:
            raise SystemExit(f"ERROR: generated naval doctrine is stale: {args.output}")
        if actual_scores != expected_scores:
            raise SystemExit(f"ERROR: compact naval capability scores are stale: {args.scores_output}")
        print(f"Validated generated naval doctrine and compact scores: {args.output}")
        return
    args.output.write_text(expected, encoding="utf-8")
    args.scores_output.write_text(expected_scores, encoding="utf-8")
    print(
        f"Generated naval doctrine and compact scores for {len(document['display_order'])} civilizations: "
        f"{args.output}"
    )


if __name__ == "__main__":
    main()
