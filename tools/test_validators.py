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
        cls.homebase = (root / "rawai-homebase.per").read_text(encoding="utf-8-sig")
        cls.init_goals = (root / "rawai-init-goals.per").read_text(encoding="utf-8-sig")
        cls.timers = (root / "rawai-timers.per").read_text(encoding="utf-8-sig")

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
        self.assertIn("RAWAI-P3B8", self.init_goals)
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


if __name__ == "__main__":
    unittest.main()
