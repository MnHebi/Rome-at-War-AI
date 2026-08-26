#!/usr/bin/env python3
"""Regression tests for semantic PER and strategy validation."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

from validate_per import validate_command_domains, validate_timer_sources
from validate_good_units import EXPECTED_CATEGORIES, validate_document, validate_provenance_sources
from validate_strategy_execution import bounded_direct_train_blocks
from validate_naval_doctrine import matching_rules
from sync_naval_capabilities import competitive_enemy_ceiling, runtime_score


class PerDomainTests(unittest.TestCase):
    def validate_text(self, text: str) -> list[dict[str, object]]:
        return validate_command_domains(text.splitlines())

    def test_multiline_training_technology_is_rejected(self) -> None:
        issues = self.validate_text(
            """(defrule
    (can-train
        ut-example)
=>
    (train
        ri-example)
)
"""
        )
        self.assertEqual(
            [issue["kind"] for issue in issues].count(
                "technology_used_as_training_operand"
            ),
            2,
        )

    def test_multiline_up_training_technology_is_rejected(self) -> None:
        issues = self.validate_text(
            """(defrule
    (up-can-train gl-unitescrow-state c:
        ut-example)
=>
    (up-train gl-unitescrow-state c:
        ri-example)
)
"""
        )
        self.assertEqual(
            [issue["kind"] for issue in issues].count(
                "technology_used_as_training_operand"
            ),
            2,
        )

    def test_two_guards_and_two_actions_are_ambiguous(self) -> None:
        issues = self.validate_text(
            """(defrule
    (can-research ut-one)
    (can-research ut-two)
=>
    (research ut-one)
    (research ut-two)
)
"""
        )
        self.assertIn(
            "ambiguous_multiple_research_guards",
            [issue["kind"] for issue in issues],
        )

    def test_assignment_operator_in_comparison_is_rejected(self) -> None:
        issues = self.validate_text(
            """(defrule
    (up-compare-goal current-action c:= ACTION-ATTACK)
=>
    (set-goal current-action ACTION-WAIT)
)
"""
        )
        self.assertIn(
            "assignment_operator_in_comparison",
            [issue["kind"] for issue in issues],
        )

    def test_comparison_operator_in_goal_fact_is_rejected(self) -> None:
        issues = self.validate_text(
            """(defrule
    (goal placement-attempts < 4)
=>
    (set-goal placement-attempts 0)
)
"""
        )
        self.assertIn(
            "comparison_operator_in_goal_fact",
            [issue["kind"] for issue in issues],
        )

    def test_search_state_requires_four_goal_block_base(self) -> None:
        issues = self.validate_text(
            """(defrule
    (true)
=>
    (up-get-search-state remote-total)
)
"""
        )
        self.assertIn(
            "invalid_search_state_output_base",
            [issue["kind"] for issue in issues],
        )
        self.assertEqual(
            [],
            self.validate_text(
                """(defrule
    (true)
=>
    (up-get-search-state local-total)
)
"""
            ),
        )

    def test_set_goal_cannot_copy_another_goals_identifier(self) -> None:
        issues = self.validate_text(
            """(defrule
    (true)
=>
    (set-goal naval-attack-requirement gl-two-percent)
)
"""
        )
        self.assertIn(
            "goal_identifier_stored_as_value",
            [issue["kind"] for issue in issues],
        )

    def test_position_source_cannot_be_used_as_goal_pair(self) -> None:
        issues = self.validate_text(
            """(defrule
    (true)
=>
    (up-set-target-point position-focus-x)
)
"""
        )
        self.assertIn(
            "invalid_position_point_identifier",
            [issue["kind"] for issue in issues],
        )

    def test_position_source_alias_is_rejected_in_any_command(self) -> None:
        issues = self.validate_text(
            """(defrule
    (true)
=>
    (up-target-point position-object-y action-move -1 stance-no-attack)
)
"""
        )
        self.assertIn(
            "invalid_position_point_identifier",
            [issue["kind"] for issue in issues],
        )

    def test_undefined_target_action_is_rejected(self) -> None:
        issues = self.validate_text(
            """(defrule
    (true)
=>
    (up-target-point point-x action-explore -1 stance-no-attack)
)
"""
        )
        self.assertIn(
            "invalid_target_action_identifier",
            [issue["kind"] for issue in issues],
        )

    def test_near_miss_target_action_is_rejected(self) -> None:
        issues = self.validate_text(
            """(defrule
    (true)
=>
    (up-target-point point-x action_move -1 stance-no-attack)
)
"""
        )
        self.assertIn(
            "invalid_target_action_identifier",
            [issue["kind"] for issue in issues],
        )

    def test_wrong_domain_target_action_is_rejected(self) -> None:
        issues = self.validate_text(
            """(defrule
    (true)
=>
    (up-target-point point-x stance-no-attack -1 stance-no-attack)
)
"""
        )
        self.assertIn(
            "invalid_target_action_identifier",
            [issue["kind"] for issue in issues],
        )

    def test_out_of_range_numeric_target_action_is_rejected(self) -> None:
        issues = self.validate_text(
            """(defrule
    (true)
=>
    (up-target-point point-x 99 -1 stance-no-attack)
)
"""
        )
        self.assertIn(
            "invalid_target_action_identifier",
            [issue["kind"] for issue in issues],
        )

    def test_position_source_must_be_copied_before_targeting(self) -> None:
        issues = self.validate_text(
            """(defrule
    (true)
=>
    (up-target-point position-enemy action-move -1 stance-no-attack)
)
"""
        )
        self.assertIn(
            "position_source_used_as_target_point",
            [issue["kind"] for issue in issues],
        )

    def test_timer_ids_must_be_unique_and_within_engine_range(self) -> None:
        report = validate_timer_sources(
            {
                "first.per": (
                    "(defconst t-valid 18)\n"
                    "(defconst t-too-high 51)\n"
                ),
                "second.per": "(defconst t-collision 18)\n",
            }
        )
        kinds = [
            issue["kind"]
            for issues in report.values()
            for issue in issues
        ]
        self.assertIn("timer_id_out_of_range", kinds)
        self.assertIn("duplicate_timer_id", kinds)

    def test_duc_group_ids_must_be_between_zero_and_nine(self) -> None:
        issues = self.validate_text(
            """(defconst invalid-naval-group 10)
(defrule
    (up-group-size c: invalid-naval-group > 0)
=>
    (up-reset-group c: invalid-naval-group)
)
"""
        )
        self.assertEqual(
            2,
            [issue["kind"] for issue in issues].count(
                "duc_group_id_out_of_range"
            ),
        )

    def test_valid_symbolic_duc_group_is_accepted(self) -> None:
        self.assertEqual(
            [],
            self.validate_text(
                """(defconst valid-naval-group 9)
(defrule
    (true)
=>
    (up-create-group 0 0 c: valid-naval-group)
    (up-modify-group-flag 1 c: valid-naval-group)
)
"""
            ),
        )

    def test_target_action_name_cannot_be_invented_as_an_action_id(self) -> None:
        issues = self.validate_text(
            """(defrule
    (true)
=>
    (up-remove-objects search-local object-data-action == actionid-guard)
)
"""
        )
        self.assertIn(
            "undefined_action_id_constant",
            [issue["kind"] for issue in issues],
        )

    def test_undefined_target_point_is_rejected(self) -> None:
        issues = self.validate_text(
            """(defrule
    (true)
=>
    (up-target-point position_enemy action-move -1 stance-no-attack)
)
"""
        )
        self.assertIn(
            "invalid_target_point_identifier",
            [issue["kind"] for issue in issues],
        )


class UniqueProductionTests(unittest.TestCase):
    def test_role_dependent_path_is_not_direct(self) -> None:
        text = """(defrule
    (goal primary-unit CHAMPION)
    (unit-type-count-total unique-line g:< gl-five-percent)
    (can-train unique-line)
=>
    (train unique-line)
)
"""
        self.assertEqual(bounded_direct_train_blocks(text, "unique-line"), [])

    def test_phase_five_only_path_is_not_persistent(self) -> None:
        text = """(defrule
    (goal current-phase 5)
    (unit-type-count-total unique-line g:< gl-five-percent)
    (can-train unique-line)
=>
    (train unique-line)
)
"""
        self.assertEqual(bounded_direct_train_blocks(text, "unique-line"), [])

    def test_early_phase_only_path_is_not_persistent(self) -> None:
        text = """(defrule
    (goal current-phase 4)
    (unit-type-count-total unique-line g:< gl-one-percent)
    (can-train unique-line)
=>
    (train unique-line)
)
"""
        self.assertEqual(bounded_direct_train_blocks(text, "unique-line"), [])

    def test_late_phase_cutoff_is_not_persistent(self) -> None:
        text = """(defrule
    (up-compare-goal current-phase <= 5)
    (unit-type-count-total unique-line g:< gl-one-percent)
    (can-train unique-line)
=>
    (train unique-line)
)
"""
        self.assertEqual(bounded_direct_train_blocks(text, "unique-line"), [])

    def test_every_multi_form_bound_is_required(self) -> None:
        text = """(defrule
    (up-object-type-count-total c: mobile-form < 4)
    (can-train mobile-form)
=>
    (train mobile-form)
)
"""
        self.assertEqual(
            bounded_direct_train_blocks(
                text,
                "mobile-form",
                {"mobile-form", "stationary-form"},
            ),
            [],
        )

    def test_persistent_bounded_path_is_accepted(self) -> None:
        text = """(defrule
    (up-compare-goal current-phase >= 5)
    (unit-type-count-total unique-line g:< gl-two-percent)
    (can-train unique-line)
=>
    (train unique-line)
)
"""
        self.assertEqual(len(bounded_direct_train_blocks(text, "unique-line")), 1)

    def test_manifest_aggregate_goal_bound_is_accepted(self) -> None:
        text = """(defrule
    (up-compare-goal current-phase >= 5)
    (up-compare-goal gl-family-count g:< gl-two-percent)
    (can-train mobile-form)
=>
    (train mobile-form)
)
"""
        self.assertEqual(
            len(
                bounded_direct_train_blocks(
                    text,
                    "mobile-form",
                    {"mobile-form", "stationary-form"},
                    "gl-family-count",
                )
            ),
            1,
        )


class GoodUnitEvaluationTests(unittest.TestCase):
    def test_blank_rating_is_rejected(self) -> None:
        ratings = {
            category: {"rating": "No", "reason": "Unavailable."}
            for category in EXPECTED_CATEGORIES
        }
        ratings["Cavalry"] = {"rating": "", "reason": "Missing."}
        document = {
            "display_order": [f"civ-{index}" for index in range(34)],
            "category_order": list(EXPECTED_CATEGORIES),
            "civilizations": {
                f"civ-{index}": {
                    "civilization": f"Civ {index}",
                    "host_civilization": "Host",
                    "unique_unit_type": "Other",
                    "ratings": ratings,
                }
                for index in range(34)
            },
            "source_provenance": {},
        }
        self.assertIn("civ-0/Cavalry: invalid or blank rating", validate_document(document))

    def test_missing_authoritative_provenance_source_is_rejected(self) -> None:
        issues = validate_provenance_sources(
            {"source_provenance": {"source_sha256": "0" * 64}},
            {"source_sha256": Path("missing-authoritative-source")},
        )
        self.assertEqual(len(issues), 1)
        self.assertIn("authoritative source is missing", issues[0])


class NavalDoctrineTests(unittest.TestCase):
    def test_commented_reservation_is_not_an_action(self) -> None:
        text = """(defrule
    (true)
=>
    ;(up-modify-goal gl-naval-fleet-count-total c:+ 1)
    (chat-local-to-self "semicolon ; inside a string is not a comment")
)
"""
        self.assertEqual(
            matching_rules(
                text,
                actions=("(up-modify-goal gl-naval-fleet-count-total c:+ 1)",),
            ),
            [],
        )

    def test_runtime_score_preserves_exact_matchup_threshold(self) -> None:
        self.assertEqual(runtime_score(62.87), 6287)
        self.assertEqual(competitive_enemy_ceiling(62.87), 7396)
        self.assertLess(62.87 / 74.26, 0.85)
        self.assertGreater(runtime_score(74.26), competitive_enemy_ceiling(62.87))


class FarmPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        root = Path(__file__).resolve().parent.parent
        cls.customconstants = (root / "rawai-customconstants.per").read_text(
            encoding="utf-8-sig"
        )
        cls.economy = (root / "rawai-economy.per").read_text(encoding="utf-8-sig")
        cls.general = (root / "rawai-general.per").read_text(encoding="utf-8-sig")
        cls.homebase = (root / "rawai-homebase.per").read_text(encoding="utf-8-sig")
        cls.init_goals = (root / "rawai-init-goals.per").read_text(encoding="utf-8-sig")
        cls.military = (root / "rawai-military.per").read_text(encoding="utf-8-sig")
        cls.military_common = (root / "rawai-military-units-common.per").read_text(
            encoding="utf-8-sig"
        )
        cls.research = (root / "rawai-research.per").read_text(encoding="utf-8-sig")
        cls.sn_defines = (root / "rawai-sn-defines.per").read_text(
            encoding="utf-8-sig"
        )
        cls.romeemp = (root / "rawai-civ-romeemp.per").read_text(encoding="utf-8-sig")
        cls.specialplacement = (root / "rawai-specialplacement.per").read_text(
            encoding="utf-8-sig"
        )
        cls.rush = (root / "rawai-rush.per").read_text(encoding="utf-8-sig")
        cls.main = (root / "AI RAW.per").read_text(encoding="utf-8-sig")
        cls.timers = (root / "rawai-timers.per").read_text(encoding="utf-8-sig")
        cls.trade = (root / "rawai-trade.per").read_text(encoding="utf-8-sig")

    def test_dependent_farm_demand_bounds_fisherman_substitution(self) -> None:
        rules = matching_rules(
            self.homebase,
            facts=("(goal dependent-farms FARM-DEMAND-DEPENDENT)",),
            actions=(
                "(up-get-fact unit-type-count villager-food 509)",
                "(up-get-fact unit-type-count villager-farmer 509)",
                "(up-get-fact unit-type-count villager-fisherman 509)",
                "(up-modify-goal 509 c:min 2)",
            ),
        )
        self.assertEqual(len(rules), 1)

    def test_farm_builders_are_available_in_both_demand_modes(self) -> None:
        farm_builders = matching_rules(
            self.homebase,
            actions=("c: farm",),
        )
        farm_builders = [
            rule for rule in farm_builders
            if "up-build" in rule[4]
        ]
        self.assertGreaterEqual(len(farm_builders), 3)
        for _, _, _, facts, _ in farm_builders:
            self.assertNotIn("dependent-farms", facts)
            self.assertIn("(goal gl-farm-placement-suspended NO)", facts)

    def test_independent_target_uses_villagers_not_population_cap(self) -> None:
        rules = matching_rules(
            self.homebase,
            facts=(
                "(goal dependent-farms FARM-DEMAND-INDEPENDENT)",
            ),
            actions=(
                "(up-modify-goal gl-farm-build-target g:= villager-count)",
                "(up-modify-goal gl-farm-build-target s:%* sn-food-gatherer-percentage)",
                "(up-get-fact unit-type-count villager-fisherman 509)",
                "(up-modify-goal 509 c:min 2)",
            ),
        )
        self.assertEqual(len(rules), 1)
        self.assertNotIn("resources-depleted", rules[0][3])
        self.assertNotIn("gl-fourty-percent", rules[0][4])

    def test_farm_build_target_is_separate_from_depleted_villager_target(self) -> None:
        self.assertNotIn("desired-number-farms", self.homebase)
        self.assertNotIn("desired-number-farms", self.economy)
        self.assertIn("desired-depleted-villagers", self.economy)

    def test_phase_five_resource_allocation_has_no_farm_feedback_loop(self) -> None:
        rules = matching_rules(
            self.economy,
            facts=(
                "(current-age-time > 120)",
                "(goal current-phase 5)",
                "(building-type-count-total university > 0)",
                "(building-type-count-total monastery > 0)",
            ),
            actions=(
                "(up-modify-sn sn-food-gatherer-percentage c:= 30)",
                "(up-modify-sn sn-wood-gatherer-percentage c:= 25)",
                "(up-modify-sn sn-gold-gatherer-percentage c:= 40)",
                "(up-modify-sn sn-stone-gatherer-percentage c:= 5)",
            ),
        )
        self.assertEqual(len(rules), 1)
        self.assertNotIn("farm", rules[0][3])

    def test_depleted_island_suspends_home_farm_placement(self) -> None:
        suspend = matching_rules(
            self.economy,
            facts=(
                "(goal resources-depleted YES)",
                "(goal gl-island-colony-established NO)",
                "(goal map-type ISLANDS)",
            ),
            actions=("(set-goal gl-farm-placement-suspended YES)",),
        )
        self.assertEqual(len(suspend), 1)
        resume = matching_rules(
            self.economy,
            facts=(
                "(goal resources-depleted NO)",
                "(goal gl-island-colony-established YES)",
            ),
            actions=("(set-goal gl-farm-placement-suspended NO)",),
        )
        self.assertEqual(len(resume), 1)

    def test_no_hunt_sentinel_does_not_count_as_nearby_food(self) -> None:
        near_rules = matching_rules(
            self.economy,
            facts=(
                "(dropsite-min-distance hunting >= 0)",
                "(dropsite-min-distance hunting <= 8)",
            ),
            actions=("(set-goal dependent-farms FARM-DEMAND-DEPENDENT)",),
        )
        self.assertEqual(len(near_rules), 1)
        exhausted_rules = matching_rules(
            self.economy,
            facts=(
                "(dropsite-min-distance hunting < 0)",
                "(dropsite-min-distance hunting > 8)",
            ),
            actions=("(set-goal dependent-farms FARM-DEMAND-INDEPENDENT)",),
        )
        self.assertEqual(len(exhausted_rules), 1)
        normalized = re.sub(r"\s+", " ", exhausted_rules[0][3])
        self.assertIn(
            "(or (dropsite-min-distance hunting < 0) "
            "(dropsite-min-distance hunting > 8) )",
            normalized,
        )
        self.assertIn("(current-age != early-antiquity-age)", normalized)
        self.assertIn("(building-type-count-total market > 0)", normalized)
        self.assertIn("(building-type-count-total blacksmith > 0)", normalized)

    def test_new_nearby_sheep_or_forage_restores_dependent_mode(self) -> None:
        rules = matching_rules(
            self.economy,
            facts=("(sheep-and-forage-too-far)",),
            actions=("(set-goal dependent-farms FARM-DEMAND-DEPENDENT)",),
        )
        self.assertEqual(len(rules), 1)
        self.assertIn("(not", rules[0][3])

    def test_farm_state_is_replay_observable(self) -> None:
        self.assertIn("RAWAI-P3B21", self.init_goals)
        telemetry = matching_rules(
            self.homebase,
            facts=("(timer-triggered t-farm-report)",),
            actions=(
                "unit-type-count villager-fisherman",
                "unit-type-count villager-farmer",
                "building-type-count farm",
                "farm target: %d",
                "farm placement suspended: %d",
                "hunt distance: %d",
            ),
        )
        self.assertEqual(len(telemetry), 1)
        calculators = matching_rules(
            self.homebase,
            actions=("(up-modify-goal gl-farm-build-target g:= villager-count)",),
        )
        self.assertEqual(len(calculators), 2)
        self.assertTrue(all(rule[1] < telemetry[0][0] for rule in calculators))
        self.assertIn("(up-timer-status t-farm-report != timer-running)", self.timers)

    def test_naval_duc_groups_stay_inside_the_engine_domain(self) -> None:
        groups = {
            name: int(value)
            for name, value in re.findall(
                r"\(defconst\s+([a-z0-9-]*group)\s+(-?\d+)\)",
                self.customconstants,
                re.IGNORECASE,
            )
        }
        self.assertTrue(groups)
        self.assertTrue(all(0 <= value <= 9 for value in groups.values()))
        self.assertEqual(groups["naval-scout-group"], groups["opportunistic-raid-group"])
        self.assertEqual(groups["relic-ferry-transport-group"], groups["transport-screen-group"])
        self.assertEqual(
            groups["juggernaut-bombardment-group"],
            groups["octeres-bombardment-group"],
        )
        self.assertIn("up-group-size c: naval-scout-group > 0", self.military)
        self.assertIn("up-group-size c: juggernaut-bombardment-group > 0", self.military)
        raid_release = matching_rules(
            self.military,
            facts=(
                "(goal gl-home-defense-state YES)",
                "(goal map-type LAND)",
                "up-group-size c: opportunistic-raid-group > 0",
            ),
        )
        self.assertEqual(len(raid_release), 1)

    def test_naval_opportunities_are_vessel_first_and_fortification_averse(self) -> None:
        trigger = matching_rules(
            self.military,
            facts=(
                "gl-game-time g:>= gl-naval-opportunity-next",
                "NAVAL-OPPORTUNITY-IDLE",
                "gl-naval-theater YES",
                "gl-naval-role c:<= NAVAL-ROLE-COMPETITIVE",
                "gl-naval-role c:>= NAVAL-ROLE-PRIMARY",
            ),
            actions=(
                "up-find-player enemy find-random",
                "up-get-point position-focus gl-naval-opportunity-source-x",
                "up-find-local c: scout-galley-line",
                "object-data-action == actionid-explore",
                "object-data-action == actionid-follow",
                "object-data-map-zone-id g:== gl-naval-opportunity-rejected-zone",
                "object-data-map-zone-id g:== gl-naval-opportunity-rejected-zone2",
                "object-data-map-zone-id g:== gl-naval-opportunity-rejected-zone3",
                "NAVAL-OPPORTUNITY-FIND-SOURCE",
            ),
        )
        self.assertEqual(len(trigger), 1)
        source = matching_rules(
            self.military,
            facts=(
                "NAVAL-OPPORTUNITY-FIND-SOURCE",
                "up-set-target-object search-local c: 0",
            ),
            actions=(
                "object-data-map-zone-id gl-naval-opportunity-zone",
                "up-find-remote c: transport-ship",
                "object-data-garrison-count <= 0",
                "NAVAL-OPPORTUNITY-SCAN-LOADED",
            ),
        )
        self.assertEqual(len(source), 1)
        self.assertIn("NAVAL-OPPORTUNITY-SCAN-WARSHIP", self.military)
        self.assertIn("NAVAL-OPPORTUNITY-SCAN-TRANSPORT", self.military)
        self.assertIn("NAVAL-OPPORTUNITY-SCAN-FISHING", self.military)
        self.assertIn("up-find-remote c: fishing-ship-class", self.military)
        self.assertIn("up-filter-distance c: -1 c: 18", self.military)
        self.assertIn("up-filter-distance c: -1 c: 32", self.military)
        self.assertIn(
            "up-lerp-percent gl-naval-opportunity-route-x "
            "gl-naval-opportunity-source-x c: 50",
            self.military,
        )
        for hard_target in ("sea-tower", "tower-class", "castle", "town-center"):
            self.assertIn(f"up-find-remote c: {hard_target}", self.military)

        target_start = matching_rules(
            self.military,
            facts=("NAVAL-OPPORTUNITY-START-TARGET-DEFENSE",),
            actions=(
                "gl-naval-opportunity-defense-player",
                "up-filter-distance c: -1 c: 18",
                "NAVAL-OPPORTUNITY-CHECK-TARGET",
            ),
        )
        self.assertEqual(len(target_start), 1)
        target_advance = matching_rules(
            self.military,
            facts=("NAVAL-OPPORTUNITY-ADVANCE-TARGET-DEFENSE",),
            actions=(
                "up-find-next-player enemy find-ordered",
                "NAVAL-OPPORTUNITY-NEXT-TARGET-DEFENSE",
            ),
        )
        route_advance = matching_rules(
            self.military,
            facts=("NAVAL-OPPORTUNITY-ADVANCE-ROUTE-DEFENSE",),
            actions=(
                "up-find-next-player enemy find-ordered",
                "NAVAL-OPPORTUNITY-NEXT-ROUTE-DEFENSE",
            ),
        )
        self.assertEqual(len(target_advance), 1)
        self.assertEqual(len(route_advance), 1)
        next_target = matching_rules(
            self.military,
            facts=(
                "NAVAL-OPPORTUNITY-NEXT-TARGET-DEFENSE",
                "gl-naval-opportunity-defense-player g:!= gl-naval-opportunity-defense-first",
            ),
            actions=(
                "sn-focus-player-number g:= gl-naval-opportunity-focus",
                "NAVAL-OPPORTUNITY-START-TARGET-DEFENSE",
            ),
        )
        next_route = matching_rules(
            self.military,
            facts=(
                "NAVAL-OPPORTUNITY-NEXT-ROUTE-DEFENSE",
                "gl-naval-opportunity-defense-player g:!= gl-naval-opportunity-defense-first",
            ),
            actions=(
                "sn-focus-player-number g:= gl-naval-opportunity-focus",
                "NAVAL-OPPORTUNITY-START-ROUTE-DEFENSE",
            ),
        )
        self.assertEqual(len(next_target), 1)
        self.assertEqual(len(next_route), 1)
        self.assertNotIn("up-find-remote", next_target[0][4])
        self.assertNotIn("up-find-remote", next_route[0][4])
        route_start = matching_rules(
            self.military,
            facts=("NAVAL-OPPORTUNITY-START-ROUTE-DEFENSE",),
            actions=(
                "gl-naval-opportunity-defense-player",
                "up-filter-distance c: -1 c: 32",
                "NAVAL-OPPORTUNITY-CHECK-ROUTE",
            ),
        )
        self.assertEqual(len(route_start), 1)
        all_enemies_clear = matching_rules(
            self.military,
            facts=(
                "NAVAL-OPPORTUNITY-NEXT-ROUTE-DEFENSE",
                "gl-naval-opportunity-defense-player g:== gl-naval-opportunity-defense-first",
            ),
            actions=("NAVAL-OPPORTUNITY-PREPARE",),
        )
        self.assertEqual(len(all_enemies_clear), 1)

        basin_ring = matching_rules(
            self.military,
            facts=("NAVAL-OPPORTUNITY-SCAN-FISHING",),
            actions=(
                "gl-naval-opportunity-rejected-zone3 g:= gl-naval-opportunity-rejected-zone2",
                "gl-naval-opportunity-rejected-zone2 g:= gl-naval-opportunity-rejected-zone",
                "gl-naval-opportunity-rejected-zone g:= gl-naval-opportunity-zone",
                "NAVAL-OPPORTUNITY-IDLE",
            ),
        )
        self.assertGreaterEqual(len(basin_ring), 1)

        retry_loaded = matching_rules(
            self.military,
            facts=(
                "NAVAL-OPPORTUNITY-REJECT",
                "NAVAL-OPPORTUNITY-LOADED",
                "gl-naval-opportunity-reject-count c:< 2",
            ),
            actions=(
                "object-data-garrison-count <= 0",
                "object-data-id g:== gl-naval-opportunity-rejected-id",
                "object-data-id g:== gl-naval-opportunity-rejected-id2",
                "NAVAL-OPPORTUNITY-SCAN-LOADED",
            ),
        )
        self.assertEqual(len(retry_loaded), 1)
        empty_transport_searches = matching_rules(
            self.military,
            actions=(
                "up-find-remote c: transport-ship",
                "object-data-garrison-count > 0",
                "NAVAL-OPPORTUNITY-SCAN-TRANSPORT",
            ),
        )
        self.assertGreaterEqual(len(empty_transport_searches), 2)

        verified_command = matching_rules(
            self.military,
            facts=(
                "NAVAL-OPPORTUNITY-VERIFY",
                "gl-naval-opportunity-ship-count c:> 0",
                "up-set-target-object search-remote c: 0",
            ),
            actions=(
                "up-target-objects 1 action-default",
                "NAVAL-OPPORTUNITY-FINISH",
            ),
        )
        self.assertEqual(len(verified_command), 1)
        failed_verify = matching_rules(
            self.military,
            facts=("NAVAL-OPPORTUNITY-VERIFY",),
            actions=("NAVAL-OPPORTUNITY-IDLE",),
        )
        self.assertEqual(len(failed_verify), 2)

    def test_ordinary_navy_is_not_released_through_autonomous_attack_now(self) -> None:
        naval_dispatches = matching_rules(
            self.military,
            facts=("ATTACK-DISPATCH-NAVAL",),
            actions=("naval opportunity dispatch: %d",),
        )
        self.assertEqual(len(naval_dispatches), 2)
        self.assertTrue(all("(attack-now)" not in rule[4] for rule in naval_dispatches))
        periodic_land = matching_rules(
            self.military,
            facts=("(goal map-type LAND)",),
            actions=(
                "(set-strategic-number sn-percent-attack-boats 0)",
                "(attack-now)",
            ),
        )
        self.assertEqual(len(periodic_land), 1)
        self.assertIn("(set-strategic-number sn-warship-targeting-mode 1)", self.customconstants)
        self.assertIn("(set-strategic-number sn-disable-tower-priority 1)", self.customconstants)
        self.assertNotIn(
            "(set-strategic-number sn-disable-tower-priority 0)",
            self.sn_defines,
        )

    def test_capital_escorts_do_not_consume_an_invalid_second_group(self) -> None:
        self.assertNotIn(
            "up-create-group 0 0 c: juggernaut-bombardment-escort-group",
            self.military,
        )
        self.assertNotIn(
            "up-create-group 0 0 c: octeres-bombardment-escort-group",
            self.military,
        )
        escort = matching_rules(
            self.military,
            facts=(
                "SIEGE-TARGET-ESCORT",
                "up-group-size c: juggernaut-bombardment-group > 0",
            ),
            actions=(
                "up-find-local c: scout-galley-line",
                "up-find-local c: boarding-ship",
                "up-add-object-by-id search-remote g: gl-naval-siege-source-id",
                "up-target-objects 0 action-guard",
            ),
        )
        self.assertEqual(len(escort), 1)
        group_builders = matching_rules(
            self.military,
            facts=("SIEGE-TARGET-GROUP",),
            actions=(
                "up-find-local c: juggernaut-line",
                "up-find-local c: octeres",
                "up-create-group 0 0 c:",
            ),
        )
        self.assertEqual(len(group_builders), 2)
        juggernaut_commands = matching_rules(
            self.military,
            facts=("SIEGE-TARGET-FIND-STRUCTURE", "gl-naval-siege-family 0"),
            actions=(
                "up-set-group search-local c: juggernaut-bombardment-group",
                "object-data-type == octeres",
            ),
        )
        octeres_commands = matching_rules(
            self.military,
            facts=("SIEGE-TARGET-FIND-STRUCTURE", "gl-naval-siege-family 1"),
            actions=(
                "up-set-group search-local c: octeres-bombardment-group",
                "object-data-type != octeres",
            ),
        )
        self.assertEqual(len(juggernaut_commands), 1)
        self.assertEqual(len(octeres_commands), 1)

        transport_escort = matching_rules(
            self.military,
            facts=("ESCORT-SELECT",),
            actions=(
                "object-data-action == actionid-explore",
                "object-data-action == actionid-follow",
            ),
        )
        self.assertEqual(len(transport_escort), 1)

    def test_relic_carrier_reboards_the_reserved_transport(self) -> None:
        wait = matching_rules(
            self.military,
            facts=("(goal gl-relic-ferry-state RELIC-FERRY-WAIT-CARRIER)",),
            actions=(
                "(up-add-object-by-id search-local g: gl-relic-ferry-unit-id)",
                "(up-add-object-by-id search-remote g: gl-relic-ferry-transport-id)",
                "(set-goal gl-relic-ferry-state RELIC-FERRY-CHECK-CARRIER)",
            ),
        )
        self.assertEqual(len(wait), 1)
        reboard = matching_rules(
            self.military,
            facts=(
                "(goal gl-relic-ferry-state RELIC-FERRY-CHECK-CARRIER)",
                "object-data-class == monk-with-relic-class",
            ),
            actions=(
                "(up-target-objects 0 action-garrison -1 stance-no-attack)",
                "(set-goal gl-relic-ferry-direction RELIC-FERRY-RETURN)",
                "(set-goal gl-relic-ferry-state RELIC-FERRY-LOADING)",
            ),
        )
        self.assertEqual(len(reboard), 1)

    def test_roman_legionary_and_scorpion_producers_use_concrete_units(self) -> None:
        for unit in ("elite-legionary", "legionary"):
            rules = matching_rules(
                self.military_common,
                facts=("gl-legionary-family-count g:< gl-ten-percent",),
                actions=(f"(up-train gl-unitescrow-state c: {unit})",),
            )
            self.assertEqual(len(rules), 1)
        for unit in ("heavy-scorpion", "scorpion"):
            rules = matching_rules(
                self.military_common,
                facts=("(unit-type-count-total scorpion-line g:< gl-three-percent)",),
                actions=(f"(up-train gl-unitescrow-state c: {unit})",),
            )
            self.assertEqual(len(rules), 1)
        for invalid_train_operand in (
            "c: legionary-ranged-line",
            "c: legionary-melee-line",
            "c: scorpion-line",
        ):
            self.assertNotIn(invalid_train_operand, self.military_common)

    def test_roman_shipyards_are_requested_before_late_land_structures(self) -> None:
        phase_two = matching_rules(
            self.romeemp,
            facts=("(goal current-phase 2)",),
            actions=("(up-modify-goal desired-number-shipyards c:= 1)",),
        )
        phase_three = matching_rules(
            self.romeemp,
            facts=("(goal current-phase 3)",),
            actions=("(up-modify-goal desired-number-shipyards c:= 3)",),
        )
        first_shipyard = matching_rules(
            self.specialplacement,
            facts=(
                "(current-age >= early-antiquity-age)",
                "(building-type-count port > 0)",
                "(building-type-count-total shipyard == 0)",
            ),
            actions=("(set-goal shipyard-placement-state SHIPYARD-ANCHOR)",),
        )
        self.assertEqual(len(phase_two), 1)
        self.assertEqual(len(phase_three), 1)
        self.assertEqual(len(first_shipyard), 1)

    def test_crossbow_and_scout_cavalry_unlock_their_actual_armor(self) -> None:
        padded = matching_rules(
            self.research,
            facts=("(unit-type-count crossbowman > 0)",),
            actions=("(up-research gl-researchescrow-state c: ri-padded-archer-armor)",),
        )
        marksmanship = matching_rules(
            self.research,
            facts=("(unit-type-count crossbowman > 0)",),
            actions=("(up-research gl-researchescrow-state c: ri-marksmanship)",),
        )
        scale = matching_rules(
            self.research,
            facts=("(unit-type-count scout-cavalry-class > 0)",),
            actions=("(up-research gl-researchescrow-state c: ri-scale-barding-armor)",),
        )
        self.assertEqual(len(padded), 1)
        self.assertEqual(marksmanship, [])
        self.assertEqual(len(scale), 1)

    def test_resource_camps_bootstrap_from_resources_then_follow_workers(self) -> None:
        search_state_block = {
            name: int(value)
            for name, value in re.findall(
                r"\(defconst\s+(local-total|local-last|remote-total|remote-last)\s+(\d+)\)",
                self.customconstants,
            )
        }
        self.assertEqual(
            search_state_block,
            {
                "local-total": 495,
                "local-last": 496,
                "remote-total": 497,
                "remote-last": 498,
            },
        )
        self.assertNotIn("(build lumber-camp)", self.homebase)
        self.assertNotIn("(up-build place-normal 0 c: lumber-camp)", self.homebase)
        self.assertNotIn("(can-build-with-escrow lumber-camp)", self.homebase)

        lumber_bootstrap = matching_rules(
            self.homebase,
            facts=(
                "(building-type-count-total lumber-camp == 0)",
                "desired-number-lumbercamps c:>= 1",
                "gl-home-zone c:>= 0",
            ),
            actions=(
                "(set-strategic-number sn-focus-player-number 0)",
                "(up-set-target-point gl-home-anchor-x)",
                "(up-find-remote c: tree-class c: 40)",
                "object-data-map-zone-id g:!= gl-home-zone",
                "gl-lumbercamp-rejected-resource-id3",
                "PLACEMENT-FIND-RESOURCE",
            ),
        )
        self.assertEqual(len(lumber_bootstrap), 1)
        self.assertNotIn("(goal wood-present YES)", lumber_bootstrap[0][3])

        later_lumber = matching_rules(
            self.homebase,
            facts=(
                "(building-type-count-total lumber-camp >= 1)",
                "lumber-camp g:< desired-number-lumbercamps",
            ),
            actions=(
                "object-data-action != actionid-gather",
                "object-data-target-id == -1",
                "PLACEMENT-ASSESS",
            ),
        )
        self.assertEqual(len(later_lumber), 1)
        for rejected_id in (
            "gl-lumbercamp-rejected-resource-id",
            "gl-lumbercamp-rejected-resource-id2",
            "gl-lumbercamp-rejected-resource-id3",
        ):
            self.assertIn(f"object-data-target-id g:== {rejected_id}", later_lumber[0][4])

        lumber_builds = matching_rules(
            self.homebase,
            facts=("(goal gl-lumbercamp-placement-state PLACEMENT-PLACE)",),
            actions=("(up-build place-point 0 c: lumber-camp)",),
        )
        self.assertEqual(len(lumber_builds), 4)
        self.assertEqual(
            {
                ("c:+", "c:+"),
                ("c:-", "c:+"),
                ("c:+", "c:-"),
                ("c:-", "c:-"),
            },
            {
                tuple(
                    re.findall(
                        r"\(up-modify-goal\s+point2-[xy]\s+(c:[+-])\s+3\)",
                        rule[4],
                    )
                )
                for rule in lumber_builds
            },
        )
        for evidence in (
            "object-data-target-id gl-lumbercamp-resource-id",
            "object-data-action != actionid-gather",
            "(up-object-data object-data-class == tree-class)",
            "object-data-map-zone-id gl-lumbercamp-resource-zone",
            "(up-compare-goal remote-total c:>= 3)",
            "object-data-map-zone-id g:!= gl-lumbercamp-resource-zone",
            "(up-get-search-state local-total)",
        ):
            self.assertIn(evidence, self.homebase)
        self.assertNotIn(
            "(up-get-search-state remote-total)", self.homebase + self.military
        )
        self.assertIn(
            "object-data-index g:!= gl-lumbercamp-candidate-index",
            lumber_bootstrap[0][4],
        )
        lumber_sparse = matching_rules(
            self.homebase,
            facts=(
                "(goal gl-lumbercamp-placement-state PLACEMENT-CHECK-RESOURCE)",
                "(up-compare-goal remote-total c:< 3)",
            ),
            actions=(
                "gl-lumbercamp-candidate-index c:+ 1",
                "lumber camp sparse tree count: %d",
            ),
        )
        self.assertEqual(len(lumber_sparse), 1)
        self.assertIn(
            "gl-lumbercamp-rejected-resource-id g:= gl-lumbercamp-resource-id",
            lumber_sparse[0][4],
        )
        lumber_retry = matching_rules(
            self.homebase,
            facts=(
                "(goal gl-lumbercamp-placement-state PLACEMENT-ASSESS)",
                "(not (up-set-target-object search-local c: 0))",
            ),
            actions=(
                "(set-goal gl-lumbercamp-rejected-resource-id -1)",
                "(set-goal gl-lumbercamp-rejected-resource-id2 -1)",
                "(set-goal gl-lumbercamp-rejected-resource-id3 -1)",
                "(set-goal gl-lumbercamp-candidate-index 0)",
            ),
        )
        self.assertEqual(len(lumber_retry), 1)

        # The freshly rebuilt list has stable distance ranks. Advancing the
        # retained rank must therefore inspect A, B, C, D rather than allowing
        # a three-entry exact-ID ring to rotate back to A on the fourth retry.
        candidates = ["A", "B", "C", "D", "E"]
        cursor = 0
        visited: list[str] = []
        for _ in range(4):
            visited.extend(
                candidate
                for index, candidate in enumerate(candidates)
                if index == cursor
            )
            cursor += 1
        self.assertEqual(visited, ["A", "B", "C", "D"])
        self.assertEqual(len(visited), len(set(visited)))
        lumber_exhausted = matching_rules(
            self.homebase,
            facts=(
                "(goal gl-lumbercamp-placement-state PLACEMENT-WAIT)",
                "gl-lumbercamp-placement-attempts c:>= 4",
            ),
            actions=(
                "gl-lumbercamp-rejected-resource-id3 g:= gl-lumbercamp-rejected-resource-id2",
                "gl-lumbercamp-rejected-resource-id g:= gl-lumbercamp-resource-id",
            ),
        )
        self.assertEqual(len(lumber_exhausted), 1)
        lumber_backoff_release = matching_rules(
            self.homebase,
            facts=(
                "(goal gl-lumbercamp-placement-state PLACEMENT-FIND-RESOURCE)",
                "(not (up-set-target-object search-remote c: 0))",
            ),
            actions=(
                "(set-goal gl-lumbercamp-rejected-resource-id -1)",
                "(set-goal gl-lumbercamp-rejected-resource-id2 -1)",
                "(set-goal gl-lumbercamp-rejected-resource-id3 -1)",
            ),
        )
        self.assertEqual(len(lumber_backoff_release), 1)

        mining_bootstrap = matching_rules(
            self.homebase,
            facts=(
                "(building-type-count-total mining-camp == 0)",
                "desired-number-miningcamps c:>= 1",
                "gl-home-zone c:>= 0",
            ),
            actions=(
                "(up-set-target-point gl-home-anchor-x)",
                "object-data-map-zone-id g:!= gl-home-zone",
                "gl-miningcamp-rejected-resource-id3",
                "PLACEMENT-FIND-RESOURCE",
            ),
        )
        self.assertEqual(len(mining_bootstrap), 2)
        self.assertTrue(
            all("(goal gold-present YES)" not in rule[3] for rule in mining_bootstrap)
        )
        self.assertTrue(
            all("(goal stone-present YES)" not in rule[3] for rule in mining_bootstrap)
        )
        self.assertTrue(
            any("(up-find-remote c: gold-mine-class c: 40)" in rule[4] for rule in mining_bootstrap)
        )
        self.assertTrue(
            any("object-data-type != 66" in rule[4] for rule in mining_bootstrap)
        )
        self.assertTrue(
            any("(up-find-remote c: stone-mine-class c: 40)" in rule[4] for rule in mining_bootstrap)
        )
        self.assertTrue(
            any("object-data-type != 102" in rule[4] for rule in mining_bootstrap)
        )

        later_mining = matching_rules(
            self.homebase,
            facts=("(building-type-count-total mining-camp >= 1)",),
            actions=(
                "object-data-action != actionid-gather",
                "object-data-target-id == -1",
                "PLACEMENT-ASSESS",
            ),
        )
        self.assertEqual(len(later_mining), 2)
        self.assertTrue(
            all("(goal gold-present YES)" not in rule[3] for rule in later_mining)
        )
        self.assertTrue(
            all("(goal stone-present YES)" not in rule[3] for rule in later_mining)
        )

        mining_builds = matching_rules(
            self.homebase,
            facts=("(goal gl-miningcamp-placement-state PLACEMENT-PLACE)",),
            actions=("(up-build place-point 0 c: mining-camp)",),
        )
        self.assertEqual(len(mining_builds), 4)
        self.assertTrue(
            all("(can-afford-building mining-camp)" in rule[3] for rule in mining_builds)
        )
        for evidence in (
            "object-data-target-id gl-miningcamp-resource-id",
            "object-data-map-zone-id gl-miningcamp-resource-zone",
            "object-data-map-zone-id g:!= gl-miningcamp-resource-zone",
            "PLACEMENT-CHECK-FOUNDATION",
            "PLACEMENT-VALIDATE-FOUNDATION-RESOURCE",
        ):
            self.assertIn(evidence, self.homebase)

        pending_radius = matching_rules(
            self.homebase,
            actions=(
                "(up-filter-distance c: -1 c: 8)",
                "(up-find-status-local c: mining-camp c: 8)",
            ),
        )
        self.assertEqual(len(pending_radius), 1)

        retry = matching_rules(
            self.homebase,
            facts=(
                "(goal gl-miningcamp-placement-state PLACEMENT-WAIT)",
                "gl-miningcamp-placement-attempts c:< 4",
            ),
            actions=(
                "search-remote g: gl-miningcamp-resource-id",
                "PLACEMENT-FIND-RESOURCE",
            ),
        )
        retry_consumer = matching_rules(
            self.homebase,
            facts=(
                "(goal gl-miningcamp-placement-state PLACEMENT-FIND-RESOURCE)",
                "(up-set-target-object search-remote c: 0)",
            ),
            actions=("object-data-map-zone-id gl-miningcamp-resource-zone",),
        )
        self.assertEqual(len(retry), 1)
        self.assertEqual(len(retry_consumer), 1)
        self.assertLessEqual(retry[0][1], retry_consumer[0][0])
        mining_backoff_release = matching_rules(
            self.homebase,
            facts=(
                "(goal gl-miningcamp-placement-state PLACEMENT-FIND-RESOURCE)",
                "(not (up-set-target-object search-remote c: 0))",
            ),
            actions=(
                "(set-goal gl-miningcamp-rejected-resource-id -1)",
                "(set-goal gl-miningcamp-rejected-resource-id2 -1)",
                "(set-goal gl-miningcamp-rejected-resource-id3 -1)",
            ),
        )
        self.assertEqual(len(mining_backoff_release), 1)

        home_anchor_capture = matching_rules(
            self.homebase,
            actions=(
                "object-data-map-zone-id gl-home-zone",
                "(up-get-point position-object gl-home-anchor-x)",
            ),
        )
        self.assertEqual(len(home_anchor_capture), 1)
        home_anchor_transfer = matching_rules(
            self.homebase,
            actions=(
                "(set-goal gl-home-retirement-target-id -2)",
                "gl-home-zone g:= gl-island-colony-zone",
                "(up-copy-point gl-home-anchor-x gl-island-colony-x)",
            ),
        )
        self.assertEqual(len(home_anchor_transfer), 2)

        mining_unrelated_reset = matching_rules(
            self.homebase,
            facts=(
                "(goal gl-miningcamp-placement-state PLACEMENT-CHECK-FOUNDATION)",
                "(not (up-set-target-object search-local c: 0))",
            ),
            actions=("(up-reset-placement c: mining-camp)",),
        )
        self.assertEqual(len(mining_unrelated_reset), 1)

        opening_mill_search = matching_rules(
            self.homebase,
            facts=(
                "(game-time >= 60)",
                "(game-time < 300)",
                "(up-timer-status t-opening-mill == timer-triggered)",
                "(goal gl-opening-mill-state OPENING-MILL-IDLE)",
                "(goal gl-migration-placement-lock NO)",
                "(up-object-type-count-total c: mill == 0)",
                "(not (up-pending-placement c: mill))",
                "(can-afford-building mill)",
                "(up-can-build 0 c: mill)",
            ),
            actions=(
                "sn-focus-player-number 0",
                "(up-set-target-point gl-home-anchor-x)",
                "(up-filter-distance c: -1 c: 32)",
                "(up-find-remote c: forage-class c: 20)",
                "object-data-map-zone-id g:!= gl-home-zone",
                "object-data-index g:!= gl-opening-mill-candidate-index",
                "OPENING-MILL-FIND-RESOURCE",
            ),
        )
        self.assertEqual(len(opening_mill_search), 1)
        self.assertNotIn("(set-goal gl-escrow", opening_mill_search[0][4])

        resource_producer = matching_rules(
            self.homebase,
            facts=(
                "(goal gl-opening-mill-state OPENING-MILL-FIND-RESOURCE)",
                "(up-object-data object-data-class == forage-class)",
            ),
            actions=(
                "object-data-id gl-opening-mill-resource-id",
                "object-data-map-zone-id gl-opening-mill-resource-zone",
                "position-object gl-opening-mill-target-x",
                "(up-filter-distance c: -1 c: 8)",
                "(up-find-remote c: forage-class c: 20)",
                "(up-get-search-state local-total)",
                "OPENING-MILL-CHECK-RESOURCE",
            ),
        )
        cluster_consumer = matching_rules(
            self.homebase,
            facts=(
                "(goal gl-opening-mill-state OPENING-MILL-CHECK-RESOURCE)",
                "(up-compare-goal remote-total c:>= 3)",
            ),
            actions=(
                "gl-opening-mill-cluster-count g:= remote-total",
                "OPENING-MILL-PLACE",
            ),
        )
        self.assertEqual(len(resource_producer), 1)
        self.assertEqual(len(cluster_consumer), 1)
        self.assertLess(resource_producer[0][1], cluster_consumer[0][0])

        allied_resource_producer = matching_rules(
            self.homebase,
            facts=(
                "(goal gl-opening-mill-state OPENING-MILL-FIND-RESOURCE)",
                "(up-object-data object-data-class == forage-class)",
                "(player-in-game any-ally)",
            ),
            actions=(
                "position-object gl-opening-mill-target-x",
                "up-find-player ally find-ordered gl-opening-mill-ally-player",
                "gl-opening-mill-ally-first g:= gl-opening-mill-ally-player",
                "OPENING-MILL-START-ALLY-CHECK",
            ),
        )
        ally_search = matching_rules(
            self.homebase,
            facts=(
                "(goal gl-opening-mill-state OPENING-MILL-START-ALLY-CHECK)",
            ),
            actions=(
                "sn-focus-player-number g:= gl-opening-mill-ally-player",
                "(up-set-target-point gl-opening-mill-target-x)",
                "(up-filter-distance c: -1 c: 18)",
                "(up-find-remote c: town-center c: 10)",
                "OPENING-MILL-CHECK-ALLY-TC",
            ),
        )
        ally_rejection = matching_rules(
            self.homebase,
            facts=(
                "(goal gl-opening-mill-state OPENING-MILL-CHECK-ALLY-TC)",
                "(up-set-target-object search-remote c: 0)",
            ),
            actions=(
                "opening Mill rejected allied-base forage",
                "gl-opening-mill-candidate-index c:+ 1",
                "(set-goal gl-migration-placement-lock NO)",
            ),
        )
        ally_iterator = matching_rules(
            self.homebase,
            facts=(
                "(goal gl-opening-mill-state OPENING-MILL-ADVANCE-ALLY)",
            ),
            actions=(
                "up-find-next-player ally find-ordered gl-opening-mill-ally-player",
                "OPENING-MILL-NEXT-ALLY",
            ),
        )
        ally_cluster_producer = matching_rules(
            self.homebase,
            facts=(
                "(goal gl-opening-mill-state OPENING-MILL-NEXT-ALLY)",
                "gl-opening-mill-ally-player g:== gl-opening-mill-ally-first",
            ),
            actions=(
                "sn-focus-player-number 0",
                "(up-find-remote c: forage-class c: 20)",
                "(up-get-search-state local-total)",
                "OPENING-MILL-CHECK-RESOURCE",
            ),
        )
        self.assertEqual(len(allied_resource_producer), 1)
        self.assertEqual(len(ally_search), 1)
        self.assertEqual(len(ally_rejection), 1)
        self.assertEqual(len(ally_iterator), 1)
        self.assertEqual(len(ally_cluster_producer), 1)
        self.assertLess(ally_cluster_producer[0][1], cluster_consumer[0][0])

        mill_point_placements = matching_rules(
            self.homebase,
            facts=("(goal gl-opening-mill-state OPENING-MILL-PLACE)",),
            actions=(
                "(up-build place-point 0 c: mill)",
                "(set-goal gl-opening-mill-requested YES)",
                "OPENING-MILL-WAIT",
            ),
        )
        self.assertEqual(len(mill_point_placements), 4)

        mill_fallback = matching_rules(
            self.homebase,
            facts=("(goal gl-opening-mill-state OPENING-MILL-FALLBACK)",),
            actions=(
                "(up-build place-normal 0 c: mill)",
                "(set-goal gl-opening-mill-requested YES)",
                "OPENING-MILL-FALLBACK-WAIT",
            ),
        )
        self.assertEqual(len(mill_fallback), 1)
        self.assertEqual(self.homebase.count("(up-build place-normal 0 c: mill)"), 2)

        unconditional_fallback = matching_rules(
            self.homebase,
            facts=(
                "(goal gl-opening-mill-state OPENING-MILL-FIND-RESOURCE)",
                "(not (up-set-target-object search-remote c: 0))",
                "(game-time >= 300)",
            ),
            actions=("OPENING-MILL-FALLBACK",),
        )
        emergency_fallback = matching_rules(
            self.homebase,
            facts=(
                "(goal gl-opening-mill-state OPENING-MILL-FIND-RESOURCE)",
                "(not (up-set-target-object search-remote c: 0))",
                "(game-time >= 180)",
                "(goal gl-home-defense-state YES)",
                "(goal resources-depleted YES)",
                "(not (goal rush-rushing NO))",
            ),
            actions=("OPENING-MILL-FALLBACK",),
        )
        self.assertEqual(len(unconditional_fallback), 1)
        self.assertEqual(len(emergency_fallback), 1)

        deadline_fallback = matching_rules(
            self.homebase,
            facts=(
                "(game-time >= 300)",
                "(goal gl-opening-mill-state OPENING-MILL-IDLE)",
                "(goal gl-opening-mill-requested NO)",
                "(not (up-pending-placement c: mill))",
            ),
            actions=(
                "(set-goal gl-migration-placement-lock YES)",
                "OPENING-MILL-FALLBACK",
            ),
        )
        self.assertEqual(len(deadline_fallback), 1)

        destroyed_mill_reset = matching_rules(
            self.homebase,
            facts=(
                "(goal gl-opening-mill-state OPENING-MILL-IDLE)",
                "(goal gl-opening-mill-requested YES)",
                "(building-type-count-total mill == 0)",
                "(up-pending-objects c: mill <= 0)",
                "(not (up-pending-placement c: mill))",
                "(up-timer-status t-opening-mill == timer-triggered)",
            ),
            actions=(
                "(up-reset-placement c: mill)",
                "(set-goal gl-opening-mill-requested NO)",
            ),
        )
        self.assertEqual(len(destroyed_mill_reset), 1)

        pending_verifier = matching_rules(
            self.homebase,
            facts=(
                "(goal gl-opening-mill-state OPENING-MILL-WAIT)",
                "(up-pending-objects c: mill >= 1)",
            ),
            actions=(
                "status-pending",
                "object-data-map-zone-id g:!= gl-opening-mill-resource-zone",
                "OPENING-MILL-CHECK-FOUNDATION",
            ),
        )
        ready_verifier = matching_rules(
            self.homebase,
            facts=(
                "(goal gl-opening-mill-state OPENING-MILL-WAIT)",
                "(up-pending-objects c: mill <= 0)",
                "(building-type-count-total mill >= 1)",
            ),
            actions=(
                "status-ready",
                "object-data-map-zone-id g:!= gl-opening-mill-resource-zone",
                "OPENING-MILL-FIND-COMPLETED",
            ),
        )
        self.assertEqual(len(pending_verifier), 1)
        self.assertEqual(len(ready_verifier), 1)
        self.assertNotIn("action-delete", pending_verifier[0][4] + ready_verifier[0][4])

        candidate_rejections = matching_rules(
            self.homebase,
            actions=("gl-opening-mill-candidate-index c:+ 1",),
        )
        self.assertEqual(len(candidate_rejections), 3)
        self.assertTrue(
            all(
                "(set-goal gl-migration-placement-lock NO)" in rule[4]
                for rule in candidate_rejections
            )
        )
        self.assertNotIn(
            "gl-opening-mill-candidate-index g:+ gl-opening-mill-cluster-count",
            self.homebase,
        )

        migration_validation = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-VALIDATE-DROPSITE-ANCHOR)",
            ),
            actions=(
                "search-remote g: gl-island-migration-anchor-id",
                "MIGRATION-CHECK-DROPSITE-ANCHOR",
            ),
        )
        self.assertEqual(len(migration_validation), 1)
        self.assertIn("(up-compare-goal remote-total c:>= 3)", self.military)
        self.assertIn("migration refreshing stale resource anchor: %d", self.military)
        refresh = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-REFRESH-DROPSITE-ANCHOR)",
            ),
            actions=("MIGRATION-FIND-RECOVERY-ANCHOR",),
        )
        refresh_consumer = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-FIND-RECOVERY-ANCHOR)",
                "(up-set-target-object search-remote c: 0)",
            ),
            actions=("migration refreshed resource anchor: %d",),
        )
        self.assertEqual(len(refresh), 1)
        self.assertEqual(len(refresh_consumer), 1)
        self.assertLessEqual(refresh[0][1], refresh_consumer[0][0])
        migration_pending = matching_rules(
            self.military,
            facts=("(goal gl-island-migration-state MIGRATION-WAIT-DROPSITE)",),
            actions=(
                "(up-filter-distance c: -1 c: 8)",
                "(up-filter-status c: status-pending c: list-active)",
            ),
        )
        self.assertEqual(len(migration_pending), 3)
        for evidence in (
            "gl-island-migration-rejected-tree1-x",
            "gl-island-migration-rejected-tree2-x",
            "gl-island-migration-rejected-tree3-x",
            "MIGRATION-CHECK-DROPSITE-NONTREE",
            "MIGRATION-REFRESH-DROPSITE-TREES",
            "(up-remove-objects search-remote object-data-distance <= 8)",
            "migration alternate tree clusters exhausted: %d",
        ):
            self.assertIn(evidence, self.military)

    def test_island_migration_waits_for_a_real_transport(self) -> None:
        scout_rules = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-GATE-OWNER)",
                "(unit-type-count transport-ship >= 1)",
                "(unit-type-count scout-cavalry-class >= 1)",
            ),
            actions=(
                "(set-goal gl-island-migration-mission MIGRATION-MISSION-SCOUT)",
            ),
        )
        self.assertEqual(len(scout_rules), 1)
        self.assertNotIn("gl-island-scout-attempts c:+", scout_rules[0][4])
        reserved_attempt = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-FIND-TRANSPORT)",
                "(goal gl-island-migration-mission MIGRATION-MISSION-SCOUT)",
            ),
            actions=(
                "(up-modify-goal gl-island-scout-attempts c:+ 1)",
                "migration-transport-group",
            ),
        )
        self.assertEqual(len(reserved_attempt), 1)

    def test_home_resource_pressure_evacuates_assigned_fishermen(self) -> None:
        self.assertIn("home resource pressure: %d", self.military)
        self.assertIn("home trees low: %d", self.military)
        civilian_gate = matching_rules(
            self.military,
            facts=(
                "(goal gl-home-resource-pressure YES)",
                "(unit-type-count transport-ship >= 1)",
            ),
            actions=(
                "(set-goal gl-island-migration-mission MIGRATION-MISSION-MINING)",
            ),
        )
        self.assertEqual(len(civilian_gate), 2)
        self.assertTrue(
            any(
                "gl-home-stone-count c:<= 0" in rule[3]
                for rule in civilian_gate
            )
        )
        evacuation = matching_rules(
            self.military,
            facts=("(goal gl-home-resource-pressure YES)",),
            actions=(
                "(up-find-local c: villager-class c: 40)",
                "(set-goal gl-island-migration-state MIGRATION-ISSUE-BOARD)",
            ),
        )
        self.assertEqual(len(evacuation), 2)
        initial = [rule for rule in evacuation if "gl-island-colony-established NO" in rule[3]]
        reinforcement = [rule for rule in evacuation if "gl-island-colony-established YES" in rule[3]]
        self.assertEqual(len(initial), 1)
        self.assertEqual(len(reinforcement), 1)
        self.assertNotIn("object-data-idling", initial[0][4])
        self.assertIn("lid-villager-farmer", reinforcement[0][4])
        self.assertIn("lid-villager-fisherman", reinforcement[0][4])
        self.assertIn("lid-villager-shepherd", reinforcement[0][4])

    def test_active_home_stone_pressure_preempts_scout_migration(self) -> None:
        stone_refresh = matching_rules(
            self.military,
            facts=(
                "(up-timer-status t-home-resource-pressure == timer-triggered)",
                "(current-age >= middle-antiquity-age)",
            ),
            actions=(
                "(up-find-remote c: stone-mine-class c: 20)",
                "(up-modify-goal gl-home-stone-count g:= remote-total)",
            ),
        )
        stone_gate = matching_rules(
            self.military,
            facts=("gl-home-stone-count c:<= 0",),
            actions=(
                "(up-find-remote c: stone-mine-class c: 20)",
                "(set-goal gl-island-migration-mission MIGRATION-MISSION-MINING)",
            ),
        )
        scout_gate = matching_rules(
            self.military,
            facts=("gl-home-stone-count c:> 0",),
            actions=(
                "(set-goal gl-island-migration-mission MIGRATION-MISSION-SCOUT)",
            ),
        )
        self.assertEqual(len(stone_refresh), 1)
        self.assertEqual(len(stone_gate), 1)
        self.assertEqual(len(scout_gate), 1)

    def test_remote_asset_defense_does_not_truncate_villagers_before_filter(self) -> None:
        local = matching_rules(
            self.military,
            facts=("(goal gl-local-response-state LOCAL-RESPONSE-IDLE)",),
            actions=(
                "(up-find-local c: villager-class c: 240)",
                "(up-remove-objects search-local object-data-under-attack <= 0)",
                "LOCAL-RESPONSE-ASSET-FIND",
            ),
        )
        naval = matching_rules(
            self.military,
            facts=("(goal gl-naval-response-state NAVAL-RESPONSE-IDLE)",),
            actions=(
                "(up-find-local c: villager-class c: 240)",
                "(up-remove-objects search-local object-data-under-attack <= 0)",
                "NAVAL-RESPONSE-HOME-FIND",
            ),
        )
        self.assertEqual(len(local), 1)
        self.assertEqual(len(naval), 1)
        for rule in local + naval:
            self.assertLess(
                rule[4].find("villager-class c: 240"),
                rule[4].find("object-data-under-attack <= 0"),
            )

    def test_relic_watchdog_keeps_hull_until_empty_at_home(self) -> None:
        stranded = matching_rules(
            self.military,
            facts=("(goal gl-relic-ferry-state RELIC-FERRY-FIND-CARRIER)",),
            actions=(
                "object-data-under-attack > 0",
                "object-data-group-flag >= 0",
                "RELIC-FERRY-FIND-TRANSPORT",
            ),
        )
        watchdog = matching_rules(
            self.military,
            facts=(
                "(up-timer-status t-relic-ferry == timer-triggered)",
                "gl-relic-ferry-return-attempts c:< 3",
            ),
            actions=(
                "gl-home-anchor-x action-unload",
                "gl-relic-ferry-return-attempts c:+ 1",
                "RELIC-FERRY-WATCHDOG-RETURN",
            ),
        )
        release = matching_rules(
            self.military,
            facts=(
                "(goal gl-relic-ferry-state RELIC-FERRY-WATCHDOG-CHECK)",
                "object-data-garrison-count <= 0",
                "object-data-distance <= 16",
            ),
            actions=(
                "(up-reset-group c: relic-ferry-transport-group)",
                "RELIC-FERRY-IDLE",
            ),
        )
        self.assertEqual(len(stranded), 1)
        self.assertEqual(len(watchdog), 1)
        self.assertEqual(len(release), 1)

        abort = matching_rules(
            self.military,
            facts=(
                "(up-timer-status t-relic-ferry == timer-triggered)",
                "gl-relic-ferry-return-attempts c:>= 3",
            ),
            actions=(
                "(up-reset-group c: relic-ferry-transport-group)",
                "(set-goal gl-relic-ferry-return-attempts 0)",
                "relic ferry watchdog abort",
                "RELIC-FERRY-IDLE",
            ),
        )
        self.assertEqual(len(abort), 1)

    def test_migration_transport_fallbacks_use_active_home_anchor(self) -> None:
        for state in (
            "MIGRATION-FIND-COLONY-LANDING",
            "MIGRATION-FIND-SCOUT-LANDING",
        ):
            rules = matching_rules(
                self.military,
                facts=(f"(goal gl-island-migration-state {state})",),
                actions=(
                    "(up-set-target-point gl-home-anchor-x)",
                    "(up-find-remote c: transport-ship c: 40)",
                    "MIGRATION-FIND-TRANSPORT",
                ),
            )
            self.assertEqual(len(rules), 1)

    def test_reserved_naval_scouts_are_evasion_candidates(self) -> None:
        inspect = matching_rules(
            self.military,
            facts=(
                "(up-timer-status t-juggernaut-evasion == timer-triggered)",
                "JUGGERNAUT-EVASION-IDLE",
            ),
            actions=(
                "(up-set-group search-local c: naval-scout-group)",
                "JUGGERNAUT-EVASION-SCOUT-CHECK",
            ),
        )
        capture = matching_rules(
            self.military,
            facts=(
                "JUGGERNAUT-EVASION-SCOUT-CHECK",
                "(up-set-target-object search-local c: 0)",
            ),
            actions=(
                "gl-juggernaut-evasion-unit-id",
                "(up-find-remote c: sea-tower c: 10)",
                "JUGGERNAUT-EVASION-CHECK",
            ),
        )
        self.assertEqual(len(inspect), 1)
        self.assertEqual(len(capture), 1)

    def test_palintonons_receive_one_same_zone_objective_group(self) -> None:
        selection = matching_rules(
            self.military,
            facts=("(goal gl-siege-target-state SIEGE-TARGET-IDLE)",),
            actions=(
                "(up-reset-group c: siege-objective-group)",
                "(up-set-target-point gl-home-anchor-x)",
                "(up-find-local c: palintonon-packed c: 20)",
            ),
        )
        grouping = matching_rules(
            self.military,
            facts=("(goal gl-siege-target-state SIEGE-TARGET-FIND-STRUCTURE)",),
            actions=(
                "(up-find-local c: palintonon c: 20)",
                "object-data-map-zone-id g:!= gl-siege-target-zone",
                "(up-create-group 0 0 c: siege-objective-group)",
                "SIEGE-TARGET-COMMAND",
            ),
        )
        command = matching_rules(
            self.military,
            facts=(
                "(goal gl-siege-target-state SIEGE-TARGET-COMMAND)",
                "gl-siege-source-count c:> 0",
            ),
            actions=(
                "(up-target-objects 1 action-default -1 stance-aggressive)",
                "siege objective group: %d",
            ),
        )
        self.assertEqual(len(selection), 1)
        self.assertEqual(len(grouping), 1)
        self.assertEqual(len(command), 1)

    def test_completed_farms_are_restaffed_same_zone(self) -> None:
        start = matching_rules(
            self.homebase,
            facts=(
                "(up-timer-status t-farm-staffing == timer-triggered)",
                "(building-type-count farm >= 1)",
                "(unit-type-count villager-fisherman > 0)",
            ),
            actions=(
                "(up-filter-distance c: -1 g: map-size)",
                "(up-find-remote c: farm c: 240)",
                "object-data-tasks-count > 0",
                "FARM-STAFFING-FIND-FARM",
            ),
        )
        self.assertEqual(len(start), 1)
        self.assertNotIn("object-data-on-mainland != on-mainland", start[0][4])
        assignments = matching_rules(
            self.homebase,
            actions=(
                "search-remote g: gl-farm-staffing-id",
                "(up-target-objects 0 action-default -1 stance-no-attack)",
                "t-farm-staffing",
            ),
        )
        self.assertGreaterEqual(len(assignments), 3)
        orphan_reject = matching_rules(
            self.homebase,
            facts=(
                "(goal gl-farm-staffing-state FARM-STAFFING-ASSIGN)",
                "(not (up-set-target-object search-local c: 0))",
            ),
            actions=(
                "object-data-id g:== gl-farm-staffing-id",
                "(set-goal gl-farm-staffing-state FARM-STAFFING-FIND-FARM)",
            ),
        )
        self.assertEqual(len(orphan_reject), 1)
        self.assertGreaterEqual(self.homebase.count("(up-reset-search 1 1 0 0)"), 3)
        self.assertIn(
            "object-data-map-zone-id g:!= gl-farm-staffing-zone",
            self.homebase,
        )
        self.assertIn("fisherman redirected to resource: %d", self.homebase)

    def test_colony_restores_normal_villager_target(self) -> None:
        rules = matching_rules(
            self.economy,
            facts=(
                "(goal resources-depleted YES)",
                "(goal gl-island-colony-established YES)",
            ),
            actions=(
                "(up-modify-goal desired-depleted-villagers g:= desired-number-villagers)",
            ),
        )
        self.assertEqual(len(rules), 1)

    def test_house_requests_share_a_cooldown(self) -> None:
        house_rules = matching_rules(self.homebase, actions=("up-build", "c: house"))
        self.assertEqual(len(house_rules), 9)
        for _, _, _, facts, actions in house_rules:
            self.assertIn("(up-timer-status t-house-placement != timer-running)", facts)
            self.assertIn("(up-set-timer c: t-house-placement c: 8)", actions)
        self.assertIn("(up-modify-goal point2-x c:+ 6)", self.homebase)
        self.assertNotIn("(up-modify-goal point2-x c:+ 14)", self.homebase)

    def test_migration_reissues_and_checks_exact_hull_occupancy(self) -> None:
        retry = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-CHECK-LOAD)",
                "(up-timer-status t-island-migration-board-retry == timer-triggered)",
                "object-data-garrison-count g:< gl-island-migration-load-target",
            ),
            actions=(
                "(up-target-objects 0 action-garrison -1 stance-no-attack)",
                "(up-set-timer c: t-island-migration-board-retry c: 3)",
            ),
        )
        self.assertEqual(len(retry), 1)
        exact_hull_refresh = matching_rules(
            self.military,
            facts=("(goal gl-island-migration-state MIGRATION-LOADING)",),
            actions=(
                "(up-find-local c: transport-ship c: 40)",
                "object-data-id g:!= gl-island-migration-transport-id",
                "MIGRATION-CHECK-LOAD",
            ),
        )
        self.assertEqual(len(exact_hull_refresh), 1)
        self.assertIn("(generate-random-number 1)", self.military)
        self.assertNotIn("(generate-random-number 2)", self.military)

        scout_departure = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-CHECK-LOAD)",
                "(goal gl-island-migration-mission MIGRATION-MISSION-SCOUT)",
                "object-data-garrison-count >= 1",
            ),
            actions=("MIGRATION-ROUTE-PREPARE",),
        )
        self.assertEqual(len(scout_departure), 1)

        partial_departure = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-CHECK-LOAD)",
                "(goal gl-island-migration-mission MIGRATION-MISSION-MINING)",
                "(up-timer-status t-island-migration == timer-triggered)",
                "object-data-garrison-count >= 2",
                "object-data-garrison-count g:< gl-island-migration-load-target",
            ),
            actions=(
                "migration depart partial target: %d",
                "MIGRATION-ROUTE-PREPARE",
            ),
        )
        self.assertEqual(len(partial_departure), 1)
        lost = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-CHECK-LOAD)",
                "(not (up-set-target-object search-local c: 0))",
            ),
            actions=("migration transport lost: %d",),
        )
        self.assertEqual(len(lost), 1)
        loaded_abort = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-CHECK-LOAD)",
                "(up-timer-status t-island-migration == timer-triggered)",
                "object-data-garrison-count == 1",
            ),
            actions=(
                "migration boarding abort loaded: %d",
                "(up-set-group search-local c: migration-boarding-group)",
                "position-self-x action-stop",
                "gl-island-migration-origin-x action-unload",
                "MIGRATION-RETURNING",
            ),
        )
        self.assertEqual(len(loaded_abort), 1)
        self.assertNotIn("MIGRATION-CHECK-LOAD-RESULT", self.military)

        watchdog = matching_rules(
            self.military,
            facts=(
                "(up-timer-status t-island-migration == timer-triggered)",
                "(not (goal gl-island-migration-state MIGRATION-IDLE))",
            ),
            actions=(
                "gl-island-migration-origin-x action-unload",
                "MIGRATION-RETURNING",
            ),
        )
        self.assertEqual(len(watchdog), 1)
        self.assertNotIn("MIGRATION-IDLE", watchdog[0][4])

    def test_attacked_colony_holds_reinforcement(self) -> None:
        self.assertIn("migration colony threat hold: %d", self.military)
        naval_latch = matching_rules(
            self.military,
            facts=(
                "(goal gl-naval-response-state NAVAL-RESPONSE-HOME-THREAT)",
                "gl-naval-response-asset-zone g:== gl-island-colony-zone",
            ),
            actions=(
                "(set-goal gl-island-colony-threat YES)",
                "gl-island-colony-threat-until g:= gl-game-time",
                "gl-island-colony-threat-until c:+ 120",
            ),
        )
        self.assertEqual(len(naval_latch), 1)
        civilian_gate = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-GATE-OWNER)",
                "(goal gl-island-colony-threat NO)",
            ),
            actions=(
                "(set-goal gl-island-migration-mission MIGRATION-MISSION-MINING)",
            ),
        )
        self.assertEqual(len(civilian_gate), 2)

    def test_naval_exploration_is_scout_ship_only(self) -> None:
        self.assertIn(
            "(set-strategic-number sn-number-boat-explore-groups 0)",
            self.general,
        )
        scout_producer = matching_rules(
            self.military,
            facts=(
                "gl-game-time g:>= gl-naval-scout-next",
                "(goal gl-naval-scout-state NAVAL-SCOUT-IDLE)",
            ),
            actions=(
                "(up-find-local c: scout-galley-line c: 10)",
                "gl-naval-scout-count",
                "NAVAL-SCOUT-CHECK",
            ),
        )
        self.assertEqual(len(scout_producer), 1)
        scout_reservation = matching_rules(
            self.military,
            facts=(
                "(goal gl-naval-scout-state NAVAL-SCOUT-CHECK)",
                "gl-naval-scout-count c:> 0",
            ),
            actions=(
                "(up-find-local c: scout-galley-line c: 10)",
                "(up-create-group 0 0 c: naval-scout-group)",
                "(set-goal gl-naval-scout-state NAVAL-SCOUT-TARGET)",
            ),
        )
        self.assertEqual(len(scout_reservation), 1)
        _, _, _, _, actions = scout_reservation[0]
        self.assertNotIn("juggernaut", actions.lower())
        self.assertNotIn("octeres", actions.lower())
        self.assertNotIn("warship-class", actions.lower())
        target_rules = matching_rules(
            self.military,
            facts=("(goal gl-naval-scout-state NAVAL-SCOUT-TARGET)",),
            actions=(
                "(up-set-group search-local c: naval-scout-group)",
                "action-move",
            ),
        )
        self.assertEqual(len(target_rules), 2)
        self.assertTrue(any("position-enemy" in rule[4] for rule in target_rules))
        for _, _, _, _, target_actions in target_rules:
            self.assertNotIn("juggernaut", target_actions.lower())
            self.assertNotIn("octeres", target_actions.lower())
            self.assertNotIn("warship-class", target_actions.lower())
        unavailable = matching_rules(
            self.military,
            facts=(
                "(goal gl-naval-scout-state NAVAL-SCOUT-CHECK)",
                "gl-naval-scout-count c:<= 0",
            ),
            actions=(
                "naval scout safe hull unavailable: %d",
                "NAVAL-SCOUT-IDLE",
            ),
        )
        self.assertEqual(len(unavailable), 1)

    def test_migration_rejects_failed_zone_for_a_bounded_window(self) -> None:
        self.assertGreaterEqual(
            self.military.count(
                "object-data-map-zone-id g:== gl-island-migration-rejected-zone"
            ),
            3,
        )
        failures = matching_rules(
            self.military,
            actions=(
                "gl-island-migration-rejected-zone3 g:= gl-island-migration-rejected-zone2",
                "gl-island-migration-rejected-zone2 g:= gl-island-migration-rejected-zone",
                "gl-island-migration-rejected-zone g:= gl-island-migration-zone",
                "(set-goal gl-island-migration-rejection-armed NO)",
            ),
        )
        self.assertGreaterEqual(len(failures), 3)
        armed = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-IDLE)",
                "(goal gl-island-migration-rejection-armed NO)",
            ),
            actions=(
                "gl-island-migration-rejection-until g:= gl-game-time",
                "gl-island-migration-rejection-until c:+ 180",
                "(set-goal gl-island-migration-rejection-armed YES)",
            ),
        )
        self.assertEqual(len(armed), 1)
        release = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-rejection-armed YES)",
                "gl-game-time g:>= gl-island-migration-rejection-until",
            ),
            actions=(
                "(set-goal gl-island-migration-rejected-zone -1)",
                "(set-goal gl-island-migration-rejected-zone2 -1)",
                "(set-goal gl-island-migration-rejected-zone3 -1)",
            ),
        )
        self.assertEqual(len(release), 1)

    def test_depleted_home_preserves_a_transport_and_camp_package(self) -> None:
        emergency = matching_rules(
            self.economy,
            facts=(
                "(goal gl-home-resource-pressure YES)",
                "(wood-amount >= 225)",
                "(can-train transport-ship)",
            ),
            actions=("(train transport-ship)",),
        )
        self.assertEqual(len(emergency), 1)
        facts = emergency[0][3]
        self.assertIn("(unit-type-count-total transport-ship < 2)", facts)
        self.assertIn("gl-available-transport-count c:< 1", facts)
        self.assertIn("(unit-type-count-total transport-ship < 3)", facts)
        self.assertIn("Relocation bridge: buy wood", self.trade)

    def test_home_attack_recalls_the_exact_loaded_transport(self) -> None:
        recalls = matching_rules(
            self.military,
            facts=(
                "(not (goal gl-transport-route-state TRANSPORT-ROUTE-IDLE))",
                "gl-local-response-threats c:>= 1",
                "gl-naval-response-threats c:>= 1",
                "gl-local-response-zone g:== gl-home-zone",
                "gl-naval-response-asset-zone g:== gl-home-zone",
            ),
            actions=(
                "(up-find-local c: transport-ship c: 40)",
                "object-data-id g:!= gl-transport-route-id",
                "gl-transport-route-origin-x action-unload",
                "TRANSPORT-ROUTE-RECOVERY-WAIT",
            ),
        )
        self.assertEqual(len(recalls), 1)
        recall_facts = recalls[0][3]
        self.assertNotIn("TRANSPORT-ROUTE-RETURN-WAIT", recall_facts)
        self.assertNotIn("TRANSPORT-ROUTE-RETURN-CHECK", recall_facts)

    def test_home_tc_retirement_requires_a_live_colony_and_spare_tc(self) -> None:
        starts = matching_rules(
            self.homebase,
            facts=(
                "(goal gl-island-colony-established YES)",
                "(goal gl-island-colony-threat NO)",
                "(goal gl-home-resource-pressure YES)",
                "(building-type-count-total town-center >= 2)",
                "(up-pending-objects c: town-center <= 0)",
                "(not (up-pending-placement c: town-center))",
            ),
            actions=("HOME-RETIRE-VERIFY-COLONY",),
        )
        self.assertEqual(len(starts), 1)
        captures = matching_rules(
            self.homebase,
            facts=(
                "gl-home-retirement-target-id c:== -1",
                "(building-type-count-total town-center >= 1)",
            ),
            actions=("HOME-RETIRE-CAPTURE-STARTING",),
        )
        self.assertEqual(len(captures), 1)
        delete = matching_rules(
            self.homebase,
            facts=(
                "(goal gl-home-retirement-state HOME-RETIRE-VALIDATE-OLD)",
                "(up-object-data object-data-status == status-ready)",
                "object-data-map-zone-id g:== gl-home-zone",
                "(up-object-data object-data-under-attack <= 0)",
                "(building-type-count-total town-center >= 2)",
            ),
            actions=(
                "(up-target-point 0 action-delete -1 -1)",
                "home TC retired exact id: %d",
                "(set-goal gl-home-retirement-target-id -2)",
                "gl-home-zone g:= gl-island-colony-zone",
            ),
        )
        self.assertEqual(len(delete), 1)
        self.assertNotIn(
            "(up-modify-goal position-self-x", self.homebase
        )

    def test_migration_uses_bounded_evasive_waypoint(self) -> None:
        self.assertIn("MIGRATION-ROUTE-WAYPOINT-CHECK", self.military)
        self.assertIn("migration route left threats: %d", self.military)
        self.assertIn("migration route right threats: %d", self.military)
        self.assertIn("migration route unreachable: %d", self.military)
        self.assertIn(
            "(up-target-point gl-island-migration-origin-x action-move -1 stance-no-attack)",
            self.military,
        )

    def test_remote_dropsite_keeps_and_assigns_reserved_settlers(self) -> None:
        gather = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-WAIT-DROPSITE-CLEAR)",
            ),
            actions=(
                "(up-set-group search-local c: migration-boarding-group)",
                "(up-target-objects 0 action-default -1 stance-no-attack)",
                "(set-goal gl-island-migration-state MIGRATION-VALIDATE-DROPSITE-ANCHOR)",
            ),
        )
        self.assertEqual(len(gather), 1)
        self.assertNotIn("up-modify-group-flag", gather[0][4])
        self.assertNotIn("up-reset-group", gather[0][4])

        assignment = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-ASSIGN-DROPSITE)",
                "(up-set-target-object search-local c: 0)",
            ),
            actions=(
                "object-data-id gl-island-migration-dropsite-id",
                "(up-set-group search-local c: migration-boarding-group)",
                "object-data-map-zone-id g:!= gl-island-migration-zone",
                "search-remote g: gl-island-migration-dropsite-id",
                "(up-target-objects 0 action-default -1 stance-no-attack)",
            ),
        )
        self.assertEqual(len(assignment), 1)

    def test_remote_colony_requires_completed_correct_zone_dropsite(self) -> None:
        pending_searches = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-WAIT-DROPSITE)",
                "(up-pending-objects",
            ),
            actions=(
                "(up-filter-status c: status-pending c: list-active)",
                "c: 8",
                "object-data-map-zone-id g:!= gl-island-migration-zone",
                "(set-goal gl-island-migration-state MIGRATION-ASSIGN-DROPSITE)",
            ),
        )
        self.assertEqual(len(pending_searches), 3)
        publish = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-CHECK-DROPSITE)",
                "(up-object-data object-data-status == status-ready)",
            ),
            actions=("(set-goal gl-island-colony-established YES)",),
        )
        self.assertEqual(len(publish), 1)
        self.assertEqual(
            self.military.count("(set-goal gl-island-colony-established YES)"),
            1,
        )

    def test_failed_remote_dropsite_recalls_workers_with_cargo(self) -> None:
        recall = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-DROPSITE-FAILED)",
            ),
            actions=(
                "(up-set-group search-local c: migration-boarding-group)",
                "(up-add-object-by-id search-remote g: gl-island-migration-transport-id)",
                "(up-target-objects 0 action-garrison -1 stance-no-attack)",
                "(set-goal gl-island-migration-state MIGRATION-RECALL-LOADING)",
            ),
        )
        self.assertEqual(len(recall), 1)
        unload = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-RECALL-CHECK)",
                "object-data-garrison-count g:>= gl-island-migration-load-target",
            ),
            actions=(
                "gl-island-migration-origin-x action-unload",
                "(set-goal gl-island-migration-state MIGRATION-RETURNING)",
            ),
        )
        self.assertEqual(len(unload), 1)
        deposit = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-RETURN-CHECK)",
                "(goal gl-island-migration-mission MIGRATION-MISSION-MINING)",
                "object-data-garrison-count <= 0",
            ),
            actions=(
                "object-data-carry <= 0",
                "(up-find-remote c: town-center c: 80)",
                "object-data-map-zone-id g:!= gl-home-zone",
                "(set-goal gl-island-migration-state MIGRATION-RETURN-DEPOSIT)",
            ),
        )
        self.assertEqual(len(deposit), 1)
        deposit_target = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-RETURN-DEPOSIT)",
                "(up-set-target-object search-remote c: 0)",
            ),
            actions=(
                "(up-target-objects 0 action-default -1 stance-no-attack)",
                "migration cargo deposit target: %d",
            ),
        )
        self.assertEqual(len(deposit_target), 1)

    def test_starting_anchor_uses_engine_position_without_shared_search(self) -> None:
        customconstants = (
            Path(__file__).resolve().parent.parent / "rawai-customconstants.per"
        ).read_text(encoding="utf-8-sig")
        anchor_rules = matching_rules(
            customconstants,
            facts=("(true)",),
            actions=("(up-get-point position-self position-self-x)",),
        )
        self.assertEqual(len(anchor_rules), 1)
        self.assertNotIn("position-object position-self-x", customconstants)

    def test_island_land_attacks_wait_for_full_transport_lift(self) -> None:
        readiness = matching_rules(
            self.economy,
            facts=(
                "(goal map-type ISLANDS)",
                "(up-compare-goal gl-available-transport-count g:< gl-transport-required)",
            ),
            actions=("(set-goal gl-land-transport-ready NO)",),
        )
        self.assertEqual(len(readiness), 1)
        usable_count = matching_rules(
            self.economy,
            facts=("(up-timer-status t-transport-readiness == timer-triggered)",),
            actions=(
                "(up-find-local c: transport-ship c: 40)",
                "object-data-garrison-count > 0",
                "object-data-idling != 1",
                "object-data-under-attack > 0",
                "object-data-group-flag >= 0",
                "(up-modify-goal gl-available-transport-count g:= local-total)",
            ),
        )
        self.assertEqual(len(usable_count), 1)
        _, _, _, _, usable_actions = usable_count[0]
        self.assertIn(
            "gl-transport-readiness-focus s:= sn-focus-player-number",
            usable_actions,
        )
        self.assertIn(
            "(set-strategic-number sn-focus-player-number my-player-number)",
            usable_actions,
        )
        self.assertIn(
            "gl-transport-readiness-focus", usable_actions
        )
        quarantine_ready = matching_rules(
            self.economy,
            facts=(
                "gl-available-transport-count g:>= gl-transport-required",
                "(goal gl-island-migration-state MIGRATION-QUARANTINED)",
            ),
            actions=("(set-goal gl-land-transport-ready YES)",),
        )
        self.assertEqual(len(quarantine_ready), 1)
        busy_controller = matching_rules(
            self.economy,
            facts=(
                "(goal gl-island-migration-state MIGRATION-IDLE)",
                "(goal gl-island-migration-state MIGRATION-QUARANTINED)",
                "(not (goal gl-transport-route-state TRANSPORT-ROUTE-IDLE))",
            ),
            actions=("(set-goal gl-land-transport-ready NO)",),
        )
        self.assertEqual(len(busy_controller), 1)
        land_dispatches = matching_rules(
            self.military,
            facts=(
                "(goal gl-attack-dispatch-owner ATTACK-DISPATCH-LAND)",
                "(goal gl-land-transport-ready YES)",
            ),
            actions=("(attack-now)",),
        )
        self.assertEqual(len(land_dispatches), 4)
        persisted_land_dispatches = matching_rules(
            self.military,
            facts=("(goal gl-attack-dispatch-owner ATTACK-DISPATCH-LAND)",),
            actions=("up-chat-data-to-self \"land dispatch",),
        )
        self.assertEqual(len(persisted_land_dispatches), 4)

    def test_sustained_age_advantage_adds_safe_hybrid_pressure(self) -> None:
        latches = matching_rules(
            self.military,
            facts=(
                "(goal gl-age-advantage-pressure NO)",
                "(current-age-time >= 120)",
                "(players-current-age target-player <",
            ),
            actions=(
                "(set-goal gl-age-advantage-pressure YES)",
                "age advantage pressure: %d",
            ),
        )
        self.assertEqual(len(latches), 3)
        pressure = matching_rules(
            self.military,
            facts=(
                "gl-game-time g:>= gl-age-advantage-next",
                "(goal gl-age-advantage-pressure YES)",
                "(goal gl-home-defense-state NO)",
                "(goal gl-island-migration-state MIGRATION-IDLE)",
                "(goal gl-transport-route-state TRANSPORT-ROUTE-IDLE)",
                "(goal gl-land-transport-ready YES)",
                "(goal gl-attack-escalation-state ATTACK-ESCALATION-NORMAL)",
            ),
            actions=(
                "sn-percent-attack-soldiers c:= 60",
                "(attack-now)",
                "age advantage land dispatch: %d",
                "(set-strategic-number sn-percent-attack-soldiers 0)",
                "ATTACK-DISPATCH-AGE",
                "gl-age-advantage-next g:= gl-game-time",
            ),
        )
        self.assertEqual(len(pressure), 1)
        _, _, _, pressure_facts, _ = pressure[0]
        self.assertNotIn("(goal map-type LAND)", pressure_facts)
        self.assertIn("(players-building-count target-player >= 1)", pressure_facts)

        age_up_requests = matching_rules(
            self.military,
            facts=(
                "(goal gl-age-advantage-pressure NO)",
                "(goal gl-attack-escalation-state ATTACK-ESCALATION-NORMAL)",
                "(soldier-count g:>= gl-ten-percent)",
            ),
            actions=(
                "(set-goal gl-age-up-attack-pending YES)",
                "(disable-self)",
            ),
        )
        self.assertEqual(len(age_up_requests), 2)
        age_up_dispatch = matching_rules(
            self.military,
            facts=(
                "(goal gl-age-up-attack-pending YES)",
                "(goal gl-attack-dispatch-owner ATTACK-DISPATCH-NONE)",
            ),
            actions=(
                "(set-goal gl-attack-dispatch-owner ATTACK-DISPATCH-AGE)",
                "sn-percent-attack-soldiers c:= 60",
                "(attack-now)",
                "(set-goal gl-age-up-attack-pending NO)",
            ),
        )
        self.assertEqual(len(age_up_dispatch), 1)
        viable_fallbacks = matching_rules(
            self.military,
            facts=(
                "(players-building-count target-player <= 0)",
                "(player-in-game",
                "(players-building-count",
            ),
            actions=("(set-strategic-number sn-target-player-number",),
        )
        self.assertEqual(len(viable_fallbacks), 8)
        focus_sync = matching_rules(
            self.military,
            facts=(
                "(players-building-count target-player >= 1)",
                "(player-in-game target-player)",
                "(not (stance-toward target-player ally))",
            ),
            actions=(
                "sn-focus-player-number s:= sn-target-player-number",
            ),
        )
        self.assertEqual(len(focus_sync), 1)
        invalid_target = matching_rules(
            self.military,
            facts=(
                "(goal gl-age-advantage-pressure YES)",
                "(not (player-in-game target-player))",
            ),
            actions=(
                "(set-goal gl-age-advantage-pressure NO)",
                "(set-goal gl-age-advantage-next 0)",
            ),
        )
        self.assertEqual(len(invalid_target), 1)
        self.assertNotIn(
            "(set-goal gl-age-up-attack-pending NO)",
            invalid_target[0][4],
        )

    def test_attack_now_is_serialized_through_late_rush_rules(self) -> None:
        military_attacks = matching_rules(
            self.military,
            actions=(
                "(attack-now)",
                "(set-goal gl-attack-dispatch-owner ATTACK-DISPATCH-COMPLETE)",
            ),
        )
        self.assertEqual(military_attacks, matching_rules(
            self.military,
            actions=("(attack-now)",),
        ))
        rush_attack = matching_rules(
            self.rush,
            facts=(
                "(goal gl-attack-dispatch-owner ATTACK-DISPATCH-NONE)",
                "(goal current-action ACTION-ATTACK)",
                "(goal current-action ACTION-RETREAT)",
            ),
            actions=(
                "(set-goal current-action ACTION-ATTACK)",
                "(set-goal gl-attack-dispatch-owner ATTACK-DISPATCH-COMPLETE)",
                "(attack-now)",
            ),
        )
        self.assertEqual(len(rush_attack), 1)
        cleanup = matching_rules(
            self.timers,
            facts=(
                "(goal current-action ACTION-ATTACK)",
                "(goal gl-attack-dispatch-owner ATTACK-DISPATCH-COMPLETE)",
            ),
            actions=(
                "(set-goal gl-attack-dispatch-owner ATTACK-DISPATCH-NONE)",
                "(set-goal current-action ACTION-WAIT)",
            ),
        )
        self.assertEqual(len(cleanup), 1)
        self.assertGreater(
            self.main.find('(load "rawai-timers")'),
            self.main.rfind('(load "rawai-rush")'),
        )

    def test_land_superiority_has_reachable_half_strength_band(self) -> None:
        inferior = matching_rules(
            self.military,
            facts=("g:< gl-enemy-team-mil-pop-divided",),
            actions=("(set-goal military-superiority INFERIOR)",),
        )
        self.assertEqual(len(inferior), 2)
        tolerable = matching_rules(
            self.military,
            facts=(
                "g:>= gl-enemy-team-mil-pop-divided",
                "g:< gl-enemy-team-military-population",
            ),
            actions=("(set-goal military-superiority TOLERABLE)",),
        )
        self.assertEqual(len(tolerable), 2)

    def test_migration_return_has_a_bounded_origin_unload(self) -> None:
        wait_for_retry_window = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-RETURNING)",
                "(up-timer-status t-island-migration == timer-triggered)",
            ),
            actions=(
                "(set-goal gl-island-migration-state MIGRATION-RETURN-CHECK)",
            ),
        )
        self.assertEqual(len(wait_for_retry_window), 1)
        retry = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-RETURN-CHECK)",
                "(up-compare-goal gl-island-migration-route-waits c:< 4)",
            ),
            actions=(
                "gl-island-migration-origin-x action-unload",
                "(up-modify-goal gl-island-migration-route-waits c:+ 1)",
            ),
        )
        self.assertEqual(len(retry), 1)
        failed = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-RETURN-CHECK)",
                "(up-compare-goal gl-island-migration-route-waits c:>= 4)",
            ),
            actions=(
                "(set-goal gl-island-migration-state MIGRATION-RETURN-FAILED)",
                "migration-boarding-group",
            ),
        )
        self.assertEqual(len(failed), 1)
        alternate = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-RETURN-FAILED)",
                "(up-timer-status t-island-migration == timer-triggered)",
            ),
            actions=(
                "gl-home-anchor-x action-unload",
                "(set-goal gl-island-migration-state MIGRATION-QUARANTINED)",
            ),
        )
        self.assertEqual(len(alternate), 1)
        quarantine_check = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-QUARANTINED)",
                "(up-timer-status t-island-migration == timer-triggered)",
            ),
            actions=(
                "(up-set-timer c: t-island-migration c: 1)",
                "(set-goal gl-island-migration-state MIGRATION-RETURNING)",
            ),
        )
        self.assertEqual(len(quarantine_check), 1)
        watchdog = matching_rules(
            self.military,
            facts=(
                "(up-timer-status t-island-migration == timer-triggered)",
                "(not (goal gl-island-migration-state MIGRATION-IDLE))",
            ),
        )
        self.assertEqual(len(watchdog), 1)
        self.assertNotIn("gl-island-migration-route-waits 0", watchdog[0][4])

    def test_unreachable_threat_without_responders_cannot_latch_defense(self) -> None:
        latches = matching_rules(
            self.military,
            actions=(
                "(set-goal gl-home-defense-state YES)",
                "(set-goal current-action ACTION-RETREAT)",
            ),
        )
        self.assertGreaterEqual(len(latches), 2)
        for _, _, _, facts, _ in latches:
            self.assertTrue(
                "gl-local-response-responders" in facts
                or "gl-naval-response-responders" in facts
            )

    def test_legacy_naval_permission_writers_are_compile_gated(self) -> None:
        compatibility_flag = "#load-if-defined RAWAI-LEGACY-NAVY-SWITCHER"
        self.assertEqual(self.military.count(compatibility_flag), 2)
        gated_disallow = re.findall(
            rf"{compatibility_flag}"
            rf"(?:(?!#end-if).)*disallow navy training",
            self.military,
            flags=re.DOTALL,
        )
        self.assertEqual(len(gated_disallow), 2)

    def test_unit_type_timer_has_one_direction_per_gold_band(self) -> None:
        low_gold = matching_rules(
            self.military,
            facts=(
                "(up-timer-status t-unit-type == timer-triggered)",
                "(gold-amount < 500)",
                "(goal train-type MAIN)",
            ),
            actions=("(set-goal train-type TRASH)",),
        )
        high_gold = matching_rules(
            self.military,
            facts=(
                "(up-timer-status t-unit-type == timer-triggered)",
                "(gold-amount > 500)",
                "(goal train-type TRASH)",
            ),
            actions=("(set-goal train-type MAIN)",),
        )
        contradictory = matching_rules(
            self.military,
            facts=(
                "(gold-amount > 500)",
                "(goal train-type MAIN)",
            ),
            actions=("(set-goal train-type TRASH)",),
        )
        self.assertEqual(len(low_gold), 1)
        self.assertEqual(len(high_gold), 1)
        self.assertEqual(contradictory, [])
        self.assertIn("(up-set-timer c: t-unit-type c: 15)", self.timers)
        self.assertNotIn("(enable-timer t-unit-type 15)", self.timers)


if __name__ == "__main__":
    unittest.main()
