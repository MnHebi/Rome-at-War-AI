#!/usr/bin/env python3
"""Regression tests for semantic PER and strategy validation."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

from validate_per import validate_command_domains
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
        cls.economy = (root / "rawai-economy.per").read_text(encoding="utf-8-sig")
        cls.general = (root / "rawai-general.per").read_text(encoding="utf-8-sig")
        cls.homebase = (root / "rawai-homebase.per").read_text(encoding="utf-8-sig")
        cls.init_goals = (root / "rawai-init-goals.per").read_text(encoding="utf-8-sig")
        cls.military = (root / "rawai-military.per").read_text(encoding="utf-8-sig")
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
        self.assertIn("RAWAI-P3B16", self.init_goals)
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

    def test_resource_camps_bootstrap_from_resources_then_follow_workers(self) -> None:
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
        ):
            self.assertIn(evidence, self.homebase)
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

        opening_mill = matching_rules(
            self.homebase,
            facts=(
                "(up-object-type-count-total c: mill == 0)",
                "(can-afford-building mill)",
                "(up-can-build 0 c: mill)",
            ),
            actions=(
                "(up-build place-normal 0 c: mill)",
                "(set-goal gl-opening-mill-requested YES)",
            ),
        )
        self.assertEqual(len(opening_mill), 1)
        self.assertNotIn("(set-goal gl-escrow", opening_mill[0][4])

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
        self.assertEqual(len(civilian_gate), 1)
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

    def test_migration_reissues_and_recounts_boarding(self) -> None:
        loading = matching_rules(
            self.military,
            facts=("(goal gl-island-migration-state MIGRATION-LOADING)",),
            actions=(
                "(up-set-group search-local c: migration-boarding-group)",
                "object-data-garrisoned == 1",
                "gl-island-migration-outstanding-count",
            ),
        )
        self.assertEqual(len(loading), 1)
        self.assertNotIn("t-island-migration-board-retry", loading[0][3])
        retry = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-CHECK-LOAD-RESULT)",
                "(up-timer-status t-island-migration-board-retry == timer-triggered)",
            ),
            actions=(
                "(up-target-objects 0 action-garrison -1 stance-no-attack)",
                "(up-set-timer c: t-island-migration-board-retry c: 3)",
            ),
        )
        self.assertEqual(len(retry), 1)
        recount = matching_rules(
            self.military,
            facts=("(goal gl-island-migration-state MIGRATION-CHECK-LOAD)",),
            actions=(
                "object-data-garrison-count gl-island-migration-loaded-count",
                "gl-island-migration-outstanding-count",
                "MIGRATION-CHECK-LOAD-RESULT",
            ),
        )
        self.assertEqual(len(recount), 1)
        self.assertIn("(generate-random-number 1)", self.military)
        self.assertNotIn("(generate-random-number 2)", self.military)

        scout_departure = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-CHECK-LOAD-RESULT)",
                "(goal gl-island-migration-mission MIGRATION-MISSION-SCOUT)",
                "gl-island-migration-loaded-count c:>= 1",
            ),
            actions=("MIGRATION-ROUTE-PREPARE",),
        )
        self.assertEqual(len(scout_departure), 1)

        exact_hull_refresh = matching_rules(
            self.military,
            facts=("(goal gl-island-migration-state MIGRATION-LOADING)",),
            actions=(
                "(up-find-local c: transport-ship c: 40)",
                "object-data-id g:!= gl-island-migration-transport-id",
                "(set-goal gl-island-migration-loaded-count -1)",
                "MIGRATION-CHECK-LOAD",
            ),
        )
        self.assertEqual(len(exact_hull_refresh), 1)
        lost = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-CHECK-LOAD-RESULT)",
                "gl-island-migration-loaded-count c:< 0",
            ),
            actions=("migration transport lost: %d",),
        )
        self.assertEqual(len(lost), 1)
        below_minimum = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-CHECK-LOAD-RESULT)",
                "gl-island-migration-loaded-count c:>= 0",
                "gl-island-migration-load-target c:< 1",
                "gl-island-migration-load-target c:< 2",
            ),
            actions=(
                "migration below minimum: %d",
                "(up-set-group search-local c: migration-boarding-group)",
                "position-self-x action-stop",
                "gl-island-migration-origin-x action-unload",
                "MIGRATION-RETURNING",
            ),
        )
        self.assertEqual(len(below_minimum), 1)

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
                "(up-set-timer c: t-island-colony-threat c: 120)",
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
        self.assertEqual(len(civilian_gate), 1)

    def test_naval_exploration_is_scout_ship_only(self) -> None:
        self.assertIn(
            "(set-strategic-number sn-number-boat-explore-groups 0)",
            self.general,
        )
        scout_producer = matching_rules(
            self.military,
            facts=(
                "(up-timer-status t-naval-scout == timer-triggered)",
                "(goal gl-naval-scout-state NAVAL-SCOUT-IDLE)",
            ),
            actions=(
                "(up-find-local c: scout-galley-line c: 10)",
                "gl-naval-scout-count",
                "NAVAL-SCOUT-CHECK",
            ),
        )
        self.assertEqual(len(scout_producer), 1)
        scout_rules = matching_rules(
            self.military,
            facts=(
                "(goal gl-naval-scout-state NAVAL-SCOUT-CHECK)",
                "gl-naval-scout-count c:> 0",
            ),
            actions=(
                "(up-find-local c: scout-galley-line c: 10)",
                "(up-create-group 0 0 c: naval-scout-group)",
                "(up-get-point position-enemy point4-x)",
                "(up-target-point point4-x action-move -1 stance-no-attack)",
            ),
        )
        self.assertEqual(len(scout_rules), 1)
        _, _, _, _, actions = scout_rules[0]
        self.assertNotIn("juggernaut", actions.lower())
        self.assertNotIn("octeres", actions.lower())
        self.assertNotIn("warship-class", actions.lower())
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
                "(up-set-timer c: t-island-migration-rejection c: 180)",
                "(set-goal gl-island-migration-rejection-armed YES)",
            ),
        )
        self.assertEqual(len(armed), 1)
        release = matching_rules(
            self.military,
            facts=(
                "(up-timer-status t-island-migration-rejection == timer-triggered)",
                "(goal gl-island-migration-rejection-armed YES)",
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
                "object-data-on-mainland != on-mainland",
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
        land_dispatches = matching_rules(
            self.military,
            facts=(
                "(goal gl-attack-dispatch-owner ATTACK-DISPATCH-LAND)",
                "(goal gl-land-transport-ready YES)",
            ),
            actions=("(attack-now)",),
        )
        self.assertEqual(len(land_dispatches), 4)

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
        self.assertNotIn(
            "(goal gl-island-migration-state MIGRATION-RETURN-FAILED)",
            self.military,
        )

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
