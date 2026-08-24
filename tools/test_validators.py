#!/usr/bin/env python3
"""Regression tests for semantic PER and strategy validation."""

from __future__ import annotations

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


if __name__ == "__main__":
    unittest.main()
