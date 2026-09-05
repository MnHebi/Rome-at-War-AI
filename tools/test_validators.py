#!/usr/bin/env python3
"""Regression tests for semantic PER and strategy validation."""

from __future__ import annotations

import hashlib
import json
import re
import unittest
from historical_test_source import historical_source
from pathlib import Path

from validate_per import code_without_comments_or_strings, validate_command_domains, validate_timer_sources
from validate_good_units import EXPECTED_CATEGORIES, validate_document, validate_provenance_sources
from validate_strategy_execution import bounded_direct_train_blocks
from validate_naval_doctrine import matching_rules
from sync_naval_capabilities import competitive_enemy_ceiling, runtime_score
from analyze_replay import json_default, unavailable_players, validated_players


class ReplayMetadataTests(unittest.TestCase):
    def test_replay_analyzer_retains_retreats_without_runtime_marker_dependency(self) -> None:
        source = (Path(__file__).parent / "analyze_replay.py").read_text(encoding="utf-8-sig")
        self.assertIn("if action == Action.DE_RETREAT:", source)
        self.assertIn("retreat_actions.append(action_record)", source)
        self.assertIn('"retreat_actions": retreat_actions', source)
        for term in ("migration", "transport", "retreat", "route-screen"):
            self.assertIn(f'"{term}"', source)
        self.assertNotIn('"raw49"', source)

    def setUp(self) -> None:
        self.fast = [
            {
                "number": 1,
                "color_id": 0,
                "team_id": 2,
                "civilization_id": 23,
                "ai_name": b"AI RAW",
            },
            {
                "number": 2,
                "color_id": 7,
                "team_id": 3,
                "civilization_id": 21,
                "ai_name": b"AI RAW",
            },
            {"number": -1, "color_id": -1, "team_id": 0, "civilization_id": 0},
        ]
        self.full = [
            {
                "player_number": 1,
                "color_id": 0,
                "selected_color": 1,
                "selected_team_id": 2,
                "resolved_team_id": 2,
                "civ_id": 23,
                "ai_name": {"value": b"AI RAW"},
            },
            {
                "player_number": 2,
                "color_id": 7,
                "selected_color": 7,
                "selected_team_id": 3,
                "resolved_team_id": 3,
                "civ_id": 21,
                "ai_name": {"value": b"AI RAW"},
            },
            {"player_number": -1},
        ]

    def test_selected_colors_join_by_player_number_not_array_position(self) -> None:
        players = validated_players(self.fast, list(reversed(self.full)))
        self.assertEqual([player["number"] for player in players], [1, 2])
        self.assertEqual([player["color_id"] for player in players], [1, 7])
        self.assertEqual([player["internal_color_id"] for player in players], [0, 7])
        self.assertEqual([player["resolved_team_id"] for player in players], [2, 3])

    def test_duplicate_or_missing_active_player_is_rejected(self) -> None:
        duplicate = [self.full[0], dict(self.full[0])]
        with self.assertRaisesRegex(ValueError, "duplicate active player"):
            validated_players(self.fast, duplicate)
        with self.assertRaisesRegex(ValueError, "active player mismatch"):
            validated_players(self.fast, self.full[:1])

    def test_fast_and_full_identity_mismatches_are_rejected(self) -> None:
        for field, value, message in (
            ("color_id", 4, "internal color mismatch"),
            ("resolved_team_id", 4, "resolved team mismatch"),
            ("civ_id", 9, "civilization mismatch"),
        ):
            changed = [dict(player) for player in self.full]
            changed[0][field] = value
            with self.subTest(field=field):
                with self.assertRaisesRegex(ValueError, message):
                    validated_players(self.fast, changed)

    def test_invalid_selected_color_is_never_substituted(self) -> None:
        changed = [dict(player) for player in self.full]
        changed[0]["selected_color"] = 255
        with self.assertRaisesRegex(ValueError, "invalid selected color"):
            validated_players(self.fast, changed)

    def test_unavailable_metadata_keeps_internal_color_nonvisual(self) -> None:
        players = unavailable_players(self.fast)
        self.assertEqual([player["number"] for player in players], [1, 2])
        self.assertEqual([player["color_id"] for player in players], [None, None])
        self.assertEqual(
            [player["internal_color_id"] for player in players], [0, 7]
        )
        self.assertNotIn("team_id", players[0])

    def test_binary_replay_payload_is_serialized_without_guessing_text(self) -> None:
        for payload in (b"\x00\xff", bytearray(b"\x00\xff"), memoryview(b"\x00\xff")):
            with self.subTest(type=type(payload).__name__):
                self.assertEqual(
                    json_default(payload), {"encoding": "hex", "value": "00ff"}
                )
        rendered = json.dumps(
            {"nested": [b"\x02"]}, default=json_default, allow_nan=False
        )
        self.assertEqual(
            json.loads(rendered),
            {"nested": [{"encoding": "hex", "value": "02"}]},
        )

    def test_parser_mapping_is_preserved_but_arbitrary_iterable_is_rejected(self) -> None:
        class ParserContainer(dict):
            pass

        self.assertEqual(json_default(ParserContainer(value=3)), {"value": 3})
        with self.assertRaisesRegex(TypeError, "cannot serialize replay value"):
            json_default({("value", 3)})
        with self.assertRaisesRegex(TypeError, "cannot serialize replay value"):
            json_default(object())

    def test_nonfinite_number_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            json.dumps(
                {"value": float("nan")}, default=json_default, allow_nan=False
            )


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

    def test_writable_goal_identifier_cannot_be_called_as_fact(self) -> None:
        issues = self.validate_text(
            """(defconst fixture-villagers 999)
(defrule
    (fixture-villagers >= 60)
=>
    (set-goal fixture-villagers 0)
)
"""
        )
        issue = next(
            issue
            for issue in issues
            if issue["kind"] == "goal_identifier_used_as_fact"
        )
        self.assertEqual(issue["identifier"], "fixture-villagers")
        self.assertEqual(issue["expected"], "up-compare-goal")

    def test_writable_goal_identifier_is_valid_through_up_compare_goal(self) -> None:
        issues = self.validate_text(
            """(defconst fixture-villagers 999)
(defrule
    (up-compare-goal fixture-villagers c:>= 60)
=>
    (set-goal fixture-villagers 0)
)
"""
        )
        self.assertNotIn(
            "goal_identifier_used_as_fact",
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

    def test_duc_group_ids_must_be_between_zero_and_nineteen(self) -> None:
        issues = self.validate_text(
            """(defconst invalid-naval-group 20)
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
                """(defconst valid-naval-group 19)
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
        cls.diplomacy = (root / "rawai-diplomacy.per").read_text(encoding="utf-8-sig")
        cls.general = (root / "rawai-general.per").read_text(encoding="utf-8-sig")
        cls.homebase = (root / "rawai-homebase.per").read_text(encoding="utf-8-sig")
        cls.hunt = (root / "rawai-hunt.per").read_text(encoding="utf-8-sig")
        cls.init_goals = (root / "rawai-init-goals.per").read_text(encoding="utf-8-sig")
        cls.military = (root / "rawai-military.per").read_text(encoding="utf-8-sig")
        cls.migration_shoreline = (root / "rawai-migration-shoreline.per").read_text(
            encoding="utf-8-sig"
        )
        cls.pop = (root / "rawai-pop.per").read_text(encoding="utf-8-sig")
        cls.military_common = (root / "rawai-military-units-common.per").read_text(
            encoding="utf-8-sig"
        )
        cls.military_common_hard = (
            root / "rawai-military-units-common-hard.per"
        ).read_text(encoding="utf-8-sig")
        cls.research = (root / "rawai-research.per").read_text(encoding="utf-8-sig")
        cls.sn_defines = (root / "rawai-sn-defines.per").read_text(
            encoding="utf-8-sig"
        )
        cls.romeemp = (root / "rawai-civ-romeemp.per").read_text(encoding="utf-8-sig")
        cls.romerep = (root / "rawai-civ-romerep.per").read_text(encoding="utf-8-sig")
        cls.dacians = (root / "rawai-civ-dacians.per").read_text(encoding="utf-8-sig")
        cls.pontus = (root / "rawai-civ-pontus.per").read_text(encoding="utf-8-sig")
        cls.seleucids = (root / "rawai-civ-seleucids.per").read_text(encoding="utf-8-sig")
        cls.unique_manifest = json.loads(
            (root / "unique-unit-production.json").read_text(encoding="utf-8")
        )
        cls.scythians = (root / "rawai-civ-scythians.per").read_text(
            encoding="utf-8-sig"
        )
        cls.specialplacement = (root / "rawai-specialplacement.per").read_text(
            encoding="utf-8-sig"
        )
        cls.rush = (root / "rawai-rush.per").read_text(encoding="utf-8-sig")
        cls.main = (root / "AI RAW.per").read_text(encoding="utf-8-sig")
        cls.timers = (root / "rawai-timers.per").read_text(encoding="utf-8-sig")
        cls.trade = (root / "rawai-trade.per").read_text(encoding="utf-8-sig")
        cls.map = (root / "rawai-map.per").read_text(encoding="utf-8-sig")
        cls.taunts = (root / "rawai-tauntcommands.per").read_text(encoding="utf-8-sig")
        cls.germani = (root / "rawai-civ-germani.per").read_text(
            encoding="utf-8-sig"
        )

    def test_ethiopian_civ_preprocessor_symbol_is_singular_everywhere(self) -> None:
        root = Path(__file__).resolve().parents[1]
        audited = [
            *root.glob("*.per"),
            root / "tools" / "evaluate_good_units.py",
            root / "tools" / "sync_civ_strategies.py",
            root / "good-unit-evaluations.json",
            root / "naval-capability-scores.json",
        ]
        for path in audited:
            self.assertNotIn(
                "ETHIOPIANS-CIV",
                path.read_text(encoding="utf-8-sig"),
                str(path.relative_to(root)),
            )
        self.assertIn("#load-if-defined ETHIOPIAN-CIV", self.main)
        for common in (self.military_common, self.military_common_hard):
            self.assertIn("#load-if-not-defined ETHIOPIAN-CIV", common)
            self.assertIn("#load-if-defined ETHIOPIAN-CIV", common)

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
        self.assertIn("RAWAI-P3B44", self.init_goals)
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

    def test_boar_commit_preserves_shepherds_and_bounds_support(self) -> None:
        startup = matching_rules(
            self.customconstants,
            actions=("(set-strategic-number sn-enable-boar-hunting 0)",),
        )
        self.assertEqual(len(startup), 1)
        self.assertIn("(true)", startup[0][3])
        self.assertIn(
            "(set-goal gl-boar-commit-state BOAR-COMMIT-IDLE)",
            self.init_goals,
        )
        self.assertIn("(set-goal gl-boar-target-zone -1)", self.init_goals)

        candidates = matching_rules(
            self.hunt,
            facts=("(goal gl-boar-commit-state BOAR-COMMIT-IDLE)",),
            actions=(
                "gl-boar-commit-focus s:= sn-focus-player-number",
                "BOAR-COMMIT-CHECK-",
            ),
        )
        self.assertEqual(len(candidates), 2)
        for candidate in candidates:
            facts = candidate[3]
            self.assertIn("(unit-type-count livestock-class <= 0)", facts)
            self.assertIn("(unit-type-count villager-shepherd <= 0)", facts)
            self.assertIn("(unit-type-count villager-hunter <= 0)", facts)
            self.assertIn("(dropsite-min-distance live-boar >= 0)", facts)
            self.assertIn("(up-compare-goal gl-home-zone c:>= 0)", facts)
        self.assertNotIn("(dropsite-min-distance livestock-class", self.hunt)

        sheep_scan = matching_rules(
            self.hunt,
            facts=(
                "BOAR-COMMIT-CHECK-OPENING-SHEEP",
                "BOAR-COMMIT-CHECK-LATER-SHEEP",
                "BOAR-COMMIT-CHECK-ACTIVE-SHEEP",
            ),
            actions=(
                "(up-set-target-point gl-home-anchor-x)",
                "(up-find-remote c: livestock-class c: 40)",
                "object-data-map-zone-id g:!= gl-home-zone",
                "object-data-index >= 1",
            ),
        )
        self.assertEqual(len(sheep_scan), 1)
        sheep_block = matching_rules(
            self.hunt,
            facts=(
                "BOAR-COMMIT-CHECK-OPENING-SHEEP",
                "BOAR-COMMIT-CHECK-LATER-SHEEP",
                "(up-set-target-object search-remote c: 0)",
            ),
            actions=(
                "(set-goal gl-boar-commit-state BOAR-COMMIT-IDLE)",
                "boar commit waiting for sheep food: %d",
                "sn-focus-player-number g:= gl-boar-commit-focus",
            ),
        )
        self.assertEqual(len(sheep_block), 1)

        authorizations = matching_rules(
            self.hunt,
            facts=("(not (up-set-target-object search-remote c: 0))",),
            actions=(
                "(set-goal gl-boar-commit-state BOAR-COMMIT-ARMED)",
                "gl-boar-commit-deadline g:= gl-game-time",
                "boar commit armed: %d",
            ),
        )
        self.assertEqual(len(authorizations), 2)
        for authorization in authorizations:
            self.assertIn(
                "(set-strategic-number sn-minimum-boar-hunt-group-size 1)",
                authorization[4],
            )
            self.assertIn(
                "sn-focus-player-number g:= gl-boar-commit-focus",
                authorization[4],
            )

        verifier = matching_rules(
            self.hunt,
            facts=(
                "(goal gl-boar-commit-state BOAR-COMMIT-ARMED)",
            ),
            actions=(
                "object-data-target != boar-class",
                "(set-goal gl-boar-commit-state BOAR-COMMIT-VERIFY)",
            ),
        )
        self.assertEqual(len(verifier), 1)
        self.assertIn("(up-find-local c: villager-class c: 240)", verifier[0][4])

        accepted = matching_rules(
            self.hunt,
            facts=(
                "(goal gl-boar-commit-state BOAR-COMMIT-VERIFY)",
                "(up-set-target-object search-local c: 0)",
                "(unit-type-count livestock-class <= 0)",
                "(unit-type-count villager-shepherd <= 0)",
            ),
            actions=(
                "(set-goal gl-boar-commit-state BOAR-COMMIT-ACTIVE)",
                "gl-boar-commit-deadline c:+ 600",
                "object-data-id gl-boar-lurer-id",
                "object-data-target-id gl-boar-target-id",
                "(up-request-hunters",
                "(enable-timer t-boar-support 3)",
                "sn-focus-player-number g:= gl-boar-commit-focus",
            ),
        )
        self.assertEqual(len(accepted), 2)
        for acceptance in accepted:
            self.assertIn(
                "(set-strategic-number sn-minimum-boar-lure-group-size 300)",
                acceptance[4],
            )
        sheep_cancel = matching_rules(
            self.hunt,
            facts=(
                "(goal gl-boar-commit-state BOAR-COMMIT-VERIFY)",
                "(not (up-set-target-object search-local c: 0))",
                "(unit-type-count villager-shepherd >= 1)",
            ),
            actions=(
                "(set-strategic-number sn-enable-boar-hunting 0)",
                "boar commit cancelled for sheep: %d",
            ),
        )
        self.assertEqual(len(sheep_cancel), 1)

        late_sheep = matching_rules(
            self.hunt,
            facts=(
                "(goal gl-boar-commit-state BOAR-COMMIT-VERIFY)",
                "(up-set-target-object search-local c: 0)",
                "(unit-type-count villager-shepherd >= 1)",
            ),
            actions=(
                "object-data-id gl-boar-lurer-id",
                "object-data-target-id gl-boar-target-id",
                "(set-goal gl-boar-commit-state BOAR-COMMIT-RESCUE-FIND)",
            ),
        )
        self.assertEqual(len(late_sheep), 1)
        rescue_find = matching_rules(
            self.hunt,
            facts=(
                "(goal gl-boar-commit-state BOAR-COMMIT-RESCUE-FIND)",
            ),
            actions=(
                "search-remote g: gl-boar-target-id",
                "BOAR-COMMIT-RESCUE-ANCHOR",
            ),
        )
        self.assertEqual(len(rescue_find), 1)
        rescue_anchor = matching_rules(
            self.hunt,
            facts=(
                "(goal gl-boar-commit-state BOAR-COMMIT-RESCUE-ANCHOR)",
                "(up-set-target-object search-remote c: 0)",
            ),
            actions=(
                "(up-get-point position-object gl-boar-target-x)",
                "object-data-map-zone-id gl-boar-target-zone",
                "(up-set-target-point gl-boar-target-x)",
                "(up-find-local c: villager-class c: 240)",
                "object-data-map-zone-id g:!= gl-boar-target-zone",
                "object-data-action == actionid-hunt",
            ),
        )
        self.assertEqual(len(rescue_anchor), 1)
        rescue_target_gone = matching_rules(
            self.hunt,
            facts=(
                "(goal gl-boar-commit-state BOAR-COMMIT-RESCUE-ANCHOR)",
                "(not (up-set-target-object search-remote c: 0))",
            ),
            actions=(
                "(set-goal gl-boar-commit-state BOAR-COMMIT-IDLE)",
                "sn-focus-player-number g:= gl-boar-commit-focus",
            ),
        )
        self.assertEqual(len(rescue_target_gone), 1)
        rescue_filter = matching_rules(
            self.hunt,
            facts=(
                "(goal gl-boar-commit-state BOAR-COMMIT-RESCUE-FILTER)",
            ),
            actions=(
                "object-data-target == prey-animal-class",
                "object-data-target == livestock-class",
                "object-data-language-id == lid-villager-shepherd",
                "object-data-language-id == lid-villager-hunter",
            ),
        )
        self.assertEqual(len(rescue_filter), 2)
        rescue_send = []
        for state, minimum in (
            ("BOAR-COMMIT-RESCUE-SEND-SIX", 5),
            ("BOAR-COMMIT-RESCUE-SEND-SEVEN", 6),
        ):
            rules = matching_rules(
                self.hunt,
                facts=(
                    f"(goal gl-boar-commit-state {state})",
                    f"(up-compare-goal local-total c:>= {minimum})",
                ),
                actions=(
                    "search-remote g: gl-boar-target-id",
                    "(up-target-objects 0 action-default -1 stance-no-attack)",
                    "boar rescue non-shepherds: %d",
                    "sn-focus-player-number g:= gl-boar-commit-focus",
                ),
            )
            self.assertEqual(len(rules), 1)
            self.assertNotIn("(up-reset-search", rules[0][4])
            rescue_send.extend(rules)
        self.assertEqual(len(rescue_send), 2)
        rescue_shortfall = matching_rules(
            self.hunt,
            facts=(
                "BOAR-COMMIT-RESCUE-SEND-",
                "(up-compare-goal local-total c:<",
            ),
            actions=(
                "(set-goal gl-boar-commit-state BOAR-COMMIT-RESCUE-GARRISON)",
            ),
        )
        self.assertEqual(len(rescue_shortfall), 2)
        rescue_fallback_find = matching_rules(
            self.hunt,
            facts=(
                "(goal gl-boar-commit-state BOAR-COMMIT-RESCUE-GARRISON)",
            ),
            actions=(
                "search-local g: gl-boar-lurer-id",
                "(set-strategic-number sn-focus-player-number my-player-number)",
                "object-data-map-zone-id g:!= gl-boar-target-zone",
                "object-data-index >= 1",
                "BOAR-COMMIT-RESCUE-GARRISON-SEND",
            ),
        )
        self.assertEqual(len(rescue_fallback_find), 1)
        rescue_fallback_send = matching_rules(
            self.hunt,
            facts=(
                "(goal gl-boar-commit-state BOAR-COMMIT-RESCUE-GARRISON-SEND)",
                "(up-set-target-object search-local c: 0)",
                "(up-set-target-object search-remote c: 0)",
            ),
            actions=(
                "(up-target-objects 0 action-garrison -1 stance-no-attack)",
                "(set-strategic-number sn-enable-boar-hunting 0)",
                "sn-focus-player-number g:= gl-boar-commit-focus",
            ),
        )
        self.assertEqual(len(rescue_fallback_send), 1)
        rescue_fallback_wait = matching_rules(
            self.hunt,
            facts=(
                "(goal gl-boar-commit-state BOAR-COMMIT-RESCUE-GARRISON-SEND)",
                "(up-set-target-object search-local c: 0)",
                "(not (up-set-target-object search-remote c: 0))",
            ),
            actions=(
                "gl-boar-commit-deadline g:= gl-game-time",
                "gl-boar-commit-deadline c:+ 5",
                "(set-goal gl-boar-commit-state BOAR-COMMIT-RESCUE-GARRISON)",
                "sn-focus-player-number g:= gl-boar-commit-focus",
            ),
        )
        self.assertEqual(len(rescue_fallback_wait), 1)

        support = matching_rules(
            self.hunt,
            actions=("(up-request-hunters",),
        )
        self.assertEqual(len(support), 4)
        for support_rule in support:
            facts = support_rule[3]
            self.assertIn("(unit-type-count livestock-class <= 0)", facts)
            self.assertIn("(unit-type-count villager-shepherd <= 0)", facts)
            self.assertIn(
                "(set-strategic-number sn-minimum-boar-lure-group-size 300)",
                support_rule[4],
            )
        self.assertNotIn("(up-reset-search 0 1 0 0)", self.hunt)
        self.assertEqual(
            {"(up-request-hunters c: 6)", "(up-request-hunters c: 7)"},
            {
                next(
                    action.strip()
                    for action in rule[4].splitlines()
                    if "up-request-hunters" in action
                )
                for rule in support
            },
        )

        active_retry_gate = matching_rules(
            self.hunt,
            facts=(
                "(goal gl-boar-commit-state BOAR-COMMIT-ACTIVE)",
                "(up-timer-status t-boar-support != timer-running)",
                "(unit-type-count livestock-class <= 0)",
                "(unit-type-count villager-shepherd <= 0)",
                "(unit-type-count villager-hunter <",
            ),
            actions=(
                "gl-boar-commit-focus s:= sn-focus-player-number",
                "BOAR-COMMIT-CHECK-ACTIVE-SHEEP",
            ),
        )
        self.assertEqual(len(active_retry_gate), 2)
        retry_verify = matching_rules(
            self.hunt,
            facts=(
                "(goal gl-boar-commit-state BOAR-COMMIT-RETRY-VERIFY)",
            ),
            actions=(
                "search-local g: gl-boar-lurer-id",
                "object-data-target-id g:!= gl-boar-target-id",
                "search-remote g: gl-boar-target-id",
                "BOAR-COMMIT-RETRY-COMMIT",
            ),
        )
        self.assertEqual(len(retry_verify), 1)
        retry_requests = matching_rules(
            self.hunt,
            facts=(
                "(goal gl-boar-commit-state BOAR-COMMIT-RETRY-COMMIT)",
                "(up-set-target-object search-local c: 0)",
                "(up-set-target-object search-remote c: 0)",
            ),
            actions=(
                "(up-request-hunters",
                "sn-focus-player-number g:= gl-boar-commit-focus",
            ),
        )
        self.assertEqual(len(retry_requests), 2)
        retry_target_gone = matching_rules(
            self.hunt,
            facts=(
                "(goal gl-boar-commit-state BOAR-COMMIT-RETRY-COMMIT)",
                "(not (up-set-target-object search-local c: 0))",
                "(not (up-set-target-object search-remote c: 0))",
            ),
            actions=(
                "(set-goal gl-boar-commit-state BOAR-COMMIT-IDLE)",
                "boar retry exact target gone: %d",
                "sn-focus-player-number g:= gl-boar-commit-focus",
            ),
        )
        self.assertEqual(len(retry_target_gone), 1)

        active_carcass_rescue = matching_rules(
            self.hunt,
            facts=(
                "(goal gl-boar-commit-state BOAR-COMMIT-CHECK-ACTIVE-SHEEP)",
                "(up-set-target-object search-remote c: 0)",
            ),
            actions=(
                "(set-goal gl-boar-commit-state BOAR-COMMIT-RESCUE-FIND)",
                "boar retry preserving sheep food: %d",
            ),
        )
        self.assertEqual(len(active_carcass_rescue), 1)

        active_late_sheep = matching_rules(
            self.hunt,
            facts=(
                "(goal gl-boar-commit-state BOAR-COMMIT-ACTIVE)",
                "(up-timer-status t-boar-support != timer-running)",
                "(unit-type-count villager-hunter <",
                "(unit-type-count villager-shepherd >= 1)",
            ),
            actions=(
                "gl-boar-commit-focus s:= sn-focus-player-number",
                "(set-goal gl-boar-commit-state BOAR-COMMIT-RESCUE-FIND)",
            ),
        )
        self.assertEqual(len(active_late_sheep), 2)

        carcass_owners = matching_rules(
            self.hunt,
            facts=(
                "(goal gl-boar-commit-state BOAR-COMMIT-ACTIVE)",
                "(dropsite-min-distance boar-hunting >= 0)",
                "(dropsite-min-distance boar-hunting <= 9)",
                "(unit-type-count villager-shepherd <= 0)",
            ),
            actions=(
                "(set-strategic-number sn-minimum-boar-lure-group-size 300)",
            ),
        )
        self.assertEqual(len(carcass_owners), 2)
        sheep_hold = matching_rules(
            self.hunt,
            facts=(
                "(goal gl-boar-commit-state BOAR-COMMIT-ACTIVE)",
                "(dropsite-min-distance boar-hunting >= 0)",
                "(unit-type-count villager-shepherd >= 1)",
            ),
            actions=(
                "(set-strategic-number sn-minimum-boar-lure-group-size 300)",
                "(set-strategic-number sn-minimum-boar-hunt-group-size 1)",
                "(set-strategic-number sn-minimum-number-hunters 1)",
            ),
        )
        self.assertEqual(len(sheep_hold), 1)
        release = matching_rules(
            self.hunt,
            facts=(
                "(goal gl-boar-commit-state BOAR-COMMIT-ACTIVE)",
                "(up-remaining-boar-amount == 65535)",
                "gl-game-time g:>= gl-boar-commit-deadline",
            ),
            actions=(
                "(set-strategic-number sn-enable-boar-hunting 0)",
                "(set-goal gl-boar-commit-state BOAR-COMMIT-IDLE)",
                "boar commit released: %d",
            ),
        )
        self.assertEqual(len(release), 1)
        self.assertNotIn("villager-hunter", release[0][3])

        # The old host-Cumans/Scythian block bypassed the generic owner after
        # load order. No civilization file may directly reactivate boar hunting.
        self.assertNotIn("sn-enable-boar-hunting", self.scythians)

    def test_pocket_preprocessor_role_is_not_inverted(self) -> None:
        flank_block = self.map.split(
            "#load-if-not-defined UP-POCKET-POSITION", 1
        )[1].split("#end-if", 1)[0]
        pocket_block = self.map.split(
            "#load-if-defined UP-POCKET-POSITION", 1
        )[1].split("#end-if", 1)[0]
        self.assertIn("(set-goal flank-position 1)", flank_block)
        self.assertIn('"Flank position"', flank_block)
        self.assertIn("(set-goal flank-position 0)", pocket_block)
        self.assertIn('"Pocket position"', pocket_block)

    def test_trade_units_require_independent_per_ally_topology_and_live_proof(self) -> None:
        phase_three = matching_rules(
            self.pop,
            facts=("(goal current-phase 3)",),
            actions=(
                "(set-goal desired-number-carts 3)",
                "(set-goal desired-number-cogs 3)",
            ),
        )
        self.assertEqual(len(phase_three), 1)

        cart = matching_rules(
            self.economy,
            facts=(
                "(goal gl-land-trade-route YES)",
                "(goal gl-trade-land-verified YES)",
                "(goal gl-trade-action-verified YES)",
                "trade-cart g:< desired-number-carts",
                "trade-cart g:< gl-trade-land-growth-limit",
            ),
            actions=("(train trade-cart)",),
        )
        cog = matching_rules(
            self.economy,
            facts=(
                "(goal gl-water-trade-route YES)",
                "(goal gl-trade-water-verified YES)",
                "(goal gl-trade-action-verified YES)",
                "trade-cog g:< desired-number-cogs",
                "trade-cog g:< gl-trade-water-growth-limit",
            ),
            actions=("(train trade-cog)",),
        )
        self.assertEqual(len(cart), 1)
        self.assertEqual(len(cog), 1)
        self.assertNotIn("(goal gl-land-trade-route NO)", cog[0][3])
        self.assertIn(
            "building-type-count market g:== gl-trade-land-producer-total",
            cart[0][3],
        )
        self.assertIn(
            "building-type-count dock g:== gl-trade-water-producer-total",
            cog[0][3],
        )

        # A land map-zone match is not a Cart path test. Bounded Cart probes
        # admit cross-zone Markets, while both modalities still require
        # actionid-trade before normal growth or retirement can occur.
        self.assertNotIn("(up-path-distance gl-trade-land-source-x", self.economy)
        self.assertNotIn(
            "object-data-map-zone-id g:!= gl-trade-land-zone", self.economy
        )
        self.assertIn(
            "object-data-map-zone-id g:!= gl-trade-water-zone", self.economy
        )
        self.assertIn("object-data-action != actionid-trade", self.economy)
        self.assertIn("(up-find-local c: trade-cog-class c: 240)", self.economy)
        self.assertIn("(up-find-local c: trade-cart c: 240)", self.economy)

        # Land completion must enter water scanning instead of terminating the
        # controller. Candidate identities are accumulated in bounded masks.
        land_to_water = matching_rules(
            self.economy,
            facts=(
                "TRADE-ROUTE-LAND-ADVANCE",
                "gl-trade-scan-count c:>= 8",
            ),
            actions=("TRADE-ROUTE-WATER-SOURCE",),
        )
        self.assertGreaterEqual(len(land_to_water), 1)
        self.assertTrue(all("TRADE-ROUTE-IDLE" not in r[4] for r in land_to_water))
        for mask in ("gl-trade-land-mask", "gl-trade-water-mask"):
            for bit in (1, 2, 4, 8, 16, 32, 64, 128):
                self.assertIn(f"(up-modify-goal {mask} c:+ {bit})", self.economy)

        land_probe = matching_rules(
            self.economy,
            facts=(
                "(goal gl-land-trade-route YES)",
                "(goal gl-trade-land-verified NO)",
                "trade-cart < 3",
            ),
            actions=("(train trade-cart)",),
        )
        water_probe = matching_rules(
            self.economy,
            facts=(
                "(goal gl-water-trade-route YES)",
                "(goal gl-trade-water-verified NO)",
                "trade-cog < 3",
            ),
            actions=("(train trade-cog)",),
        )
        self.assertEqual(len(land_probe), 1)
        self.assertEqual(len(water_probe), 1)
        self.assertNotIn("(goal gl-land-trade-route NO)", water_probe[0][3])
        self.assertNotIn("gl-trade-action-verified YES", land_probe[0][3])
        self.assertNotIn("gl-trade-action-verified YES", water_probe[0][3])

        fallback = matching_rules(
            self.economy,
            facts=(
                "gl-trade-route-failures c:>= 3",
                "(goal gl-land-trade-route NO)",
                "(goal gl-water-trade-route NO)",
                "trade-cog < 3",
                "gl-trade-probe-trained c:< 3",
            ),
            actions=(
                "(train trade-cog)",
                "gl-trade-probe-trained c:+ 1",
                "bounded trade cog probe: %d",
            ),
        )
        self.assertEqual(len(fallback), 1)

        transition = matching_rules(
            self.economy,
            facts=(
                "population-cap >= 300",
                "gl-trade-action-verified YES",
                "TRADE-TRANSITION-NONE",
            ),
            actions=("TRADE-TRANSITION-ROUTE",),
        )
        retirement = matching_rules(
            self.economy,
            facts=(
                "gl-trade-action-verified YES",
                "population-headroom < 2",
                "villager-class g:> desired-number-villagers",
                "gl-trade-active-count c:>= 3",
            ),
            actions=("gl-trade-retirement-state TRADE-RETIRE-SELECT",),
        )
        self.assertEqual(len(transition), 1)
        self.assertEqual(len(retirement), 1)
        for row in transition + retirement:
            self.assertNotIn("gl-trade-land-mask", row[3])
            self.assertNotIn("gl-trade-water-mask", row[3])

    def test_taunt_69_proves_a_nearby_owned_structure_before_delete(self) -> None:
        trigger = matching_rules(
            self.taunts,
            facts=("(taunt-detected any-ally 69)",),
            actions=(
                "(set-goal deletion-flare YES)",
                "(set-goal target-action YES)",
            ),
        )
        self.assertEqual(len(trigger), 1)
        self.assertNotIn("up-jump-rule", trigger[0][4])
        selector = matching_rules(
            self.taunts,
            facts=(
                "(goal deletion-flare YES)",
                "(cc-players-unit-type-count any-ally flare >= 1)",
            ),
            actions=(
                "(up-find-player-flare any-ally gl-flared-delete-x)",
                "(up-filter-distance c: -1 c: 2)",
                "(up-modify-goal gl-delete-flare-candidates g:= local-total)",
                "(set-goal deletion-flare MAYBE)",
            ),
        )
        self.assertEqual(len(selector), 1)
        self.assertNotIn("up-jump-rule", selector[0][4])
        self.assertIn("(set-goal gl-delete-flare-id -1)", trigger[0][4])
        delete = matching_rules(
            self.taunts,
            facts=(
                "(goal deletion-flare MAYBE)",
                "gl-delete-flare-candidates c:> 0",
                "(up-set-target-object search-local c: 0)",
            ),
            actions=(
                "(up-get-object-data object-data-id gl-delete-flare-id)",
                "(up-target-point 0 action-delete -1 -1)",
                "taunt 69 deleted structure id: %d",
            ),
        )
        self.assertEqual(len(delete), 1)
        vanished = matching_rules(
            self.taunts,
            facts=(
                "(goal deletion-flare MAYBE)",
                "gl-delete-flare-candidates c:> 0",
                "(not (up-set-target-object search-local c: 0))",
            ),
            actions=(
                "taunt 69 structure candidate vanished: %d",
                "(set-goal deletion-flare NO)",
                "(set-goal target-action NO)",
            ),
        )
        self.assertEqual(len(vanished), 1)
        self.assertNotIn("all-units-class", self.taunts)
        self.assertIn("taunt 69 no structure candidates: %d", self.taunts)
        self.assertNotIn("(unit-type-count flare", self.taunts)

        no_flare = matching_rules(
            self.taunts,
            facts=(
                "(goal deletion-flare YES)",
                "(cc-players-unit-type-count any-ally flare <= 0)",
            ),
            actions=(
                "(set-goal deletion-flare NO)",
                "(set-goal target-action NO)",
            ),
        )
        self.assertEqual(len(no_flare), 1)

        watchdog = matching_rules(
            self.taunts,
            facts=(
                "(goal target-action YES)",
                "gl-game-time g:>= gl-flare-command-deadline",
            ),
            actions=(
                "Structure deletion flare command expired",
                "(set-goal gl-delete-flare-id -1)",
                "(set-goal gl-delete-flare-candidates 0)",
                "(set-goal target-action NO)",
            ),
        )
        self.assertEqual(len(watchdog), 1)

    def test_taunt_52_uses_an_allied_flare_with_a_deadline(self) -> None:
        selector = matching_rules(
            self.taunts,
            facts=(
                "(goal market-flare YES)",
                "(cc-players-unit-type-count any-ally flare >= 1)",
                "(can-build market)",
            ),
            actions=(
                "(up-find-player-flare any-ally gl-flared-market-x)",
                "(up-build place-point 0 c: market)",
            ),
        )
        self.assertEqual(len(selector), 1)

        no_flare = matching_rules(
            self.taunts,
            facts=(
                "(goal market-flare YES)",
                "(cc-players-unit-type-count any-ally flare <= 0)",
            ),
            actions=(
                "(set-goal market-flare NO)",
                "(set-goal target-action NO)",
            ),
        )
        self.assertEqual(len(no_flare), 1)
        self.assertIn("gl-flare-command-deadline c:+ 8", self.taunts)
        self.assertIn("Market flare command expired", self.taunts)

    def test_crowded_placement_recovery_is_persistent_and_bounded(self) -> None:
        self.assertIn("c:+ 24", self.homebase)
        self.assertIn("g:min gl-placement-pressure-cap", self.homebase)
        self.assertIn("crowded town placement saturated size", self.homebase)
        self.assertIn("PLACEMENT-KIND-ECONOMY", self.homebase)
        self.assertIn("PLACEMENT-KIND-MILITARY", self.homebase)
        self.assertIn("PLACEMENT-KIND-DEFENSE", self.homebase)
        for building in (
            "house",
            "barracks",
            "archery-range",
            "stable",
            "siege-workshop",
            "blacksmith",
            "university",
            "monastery",
            "castle",
            "watch-tower",
            "outpost",
            "wonder",
        ):
            self.assertIn(f"(up-reset-placement c: {building})", self.homebase)
        economy_reset = matching_rules(
            self.homebase,
            facts=(
                "PLACEMENT-PRESSURE-CHECK-ECONOMY",
                "up-pending-placement c: house",
            ),
            actions=("up-reset-placement c: house",),
        )
        self.assertEqual(len(economy_reset), 1)
        for managed in ("town-center", "farm", "market"):
            self.assertNotIn(f"up-reset-placement c: {managed}", economy_reset[0][4])
        self.assertIn("(not (up-can-build 0 c: market))", self.homebase)
        self.assertIn("(not (up-can-build 0 c: farm))", self.homebase)
        self.assertIn("(not (up-can-build 0 c: castle))", self.homebase)
        self.assertNotRegex(
            self.homebase,
            r"\(up-modify-sn\s+sn-maximum-town-size\s+[cg]:[<>]=?",
        )

    def test_wall_owner_uses_correct_role_and_backs_off(self) -> None:
        self.assertIn("(goal flank-position 1)", self.homebase)
        self.assertIn("object-data-map-zone-id g:!= gl-wall-land-zone", self.homebase)
        self.assertIn("(up-assign-builders c: wall-class c: 0)", self.homebase)
        self.assertIn("(up-assign-builders c: gate-class c: 0)", self.homebase)
        self.assertIn("Wall placement no-progress backoff", self.homebase)
        self.assertIn("gl-wall-retries c:>= 3", self.homebase)
        self.assertIn("gl-wall-next c:+ 180", self.homebase)
        wall_builders = matching_rules(
            self.homebase,
            facts=("wall-completed-percentage 2 < 100",),
            actions=("(build-wall 2",),
        )
        self.assertTrue(wall_builders)
        for _, _, _, facts, actions in wall_builders:
            self.assertIn("gl-wall-next", facts)
            self.assertIn("gl-wall-retries", facts)
            self.assertIn("gl-wall-danger-until", facts)
            self.assertIn("building-type-count town-center >= 1", facts)
            self.assertIn("villager-class >= 20", facts)
            self.assertIn("gl-home-defense-state NO", facts)
            self.assertIn("gl-wall-next", actions)

        self.assertIn("gl-wall-material WALL-MATERIAL-UNSET", self.homebase)
        self.assertIn("Wall owner latched stone perimeter", self.homebase)
        self.assertIn("Wall owner latched palisade perimeter", self.homebase)
        self.assertNotIn("sn-gate-type-for-wall", self.taunts)
        gate_builders = matching_rules(
            self.homebase,
            facts=("can-build-gate-with-escrow 2",),
            actions=("(build-gate 2)",),
        )
        self.assertEqual(len(gate_builders), 6)
        first_gate_builders = [
            rule for rule in gate_builders if "gl-wall-gates-issued 0" in rule[3]
        ]
        self.assertEqual(len(first_gate_builders), 2)
        self.assertTrue(all(
            "wall-completed-percentage 2 >= 25" not in rule[3]
            for rule in first_gate_builders
        ))
        second_gate_builders = [
            rule for rule in gate_builders if "gl-wall-gates-issued 1" in rule[3]
        ]
        self.assertEqual(len(second_gate_builders), 2)
        self.assertTrue(all(
            "wall-completed-percentage 2 >= 40" in rule[3]
            for rule in second_gate_builders
        ))
        self.assertTrue(all(
            "wall-completed-percentage 2 >= 75" not in rule[3]
            for rule in second_gate_builders
        ))
        third_gate_builders = [
            rule for rule in gate_builders if "gl-wall-gates-issued 2" in rule[3]
        ]
        self.assertEqual(len(third_gate_builders), 2)
        self.assertTrue(all(
            "wall-completed-percentage 2 >= 75" in rule[3]
            for rule in third_gate_builders
        ))
        self.assertTrue(all("gl-wall-gates-issued 3" in rule[4] for rule in third_gate_builders))
        for _, _, _, facts, actions in gate_builders:
            self.assertIn("gl-wall-gate-next", facts)
            self.assertIn("gl-wall-danger-until", facts)
            self.assertIn("building-type-count town-center >= 1", facts)
            self.assertIn("villager-class >= 20", facts)
            self.assertIn("gl-home-defense-state NO", facts)
            self.assertNotIn("gl-wall-next", facts)
            self.assertIn("gl-wall-gates-issued", actions)
            self.assertIn("gl-wall-gate-next", actions)
            self.assertNotIn("building-type-count-total gate", facts)
            self.assertFalse("release-escrow wood" in actions and "release-escrow stone" in actions)
            if "WALL-MATERIAL-STONE" in facts:
                self.assertIn("release-escrow stone", actions)
                self.assertNotIn("release-escrow wood", actions)
            if "WALL-MATERIAL-PALISADE" in facts:
                self.assertIn("release-escrow wood", actions)
                self.assertNotIn("release-escrow stone", actions)
        self.assertNotIn(
            "wall-completed-percentage 2 >= 100)\n\t(building-type-count-total gate",
            self.homebase,
        )
        self.assertIn("Wall gate availability backoff", self.homebase)
        first_gate_wait = matching_rules(
            self.homebase,
            facts=(
                "gl-wall-gates-issued 0",
                "not (can-build-gate-with-escrow 2)",
            ),
            actions=("gl-wall-gate-attempts c:+ 1",),
        )
        self.assertEqual(len(first_gate_wait), 1)
        self.assertNotIn("wall-completed-percentage 2 >= 25", first_gate_wait[0][3])
        second_gate_wait = matching_rules(
            self.homebase,
            facts=(
                "gl-wall-gates-issued 1",
                "wall-completed-percentage 2 >= 40",
                "not (can-build-gate-with-escrow 2)",
            ),
            actions=("gl-wall-gate-attempts c:+ 1",),
        )
        self.assertEqual(len(second_gate_wait), 1)
        third_gate_wait = matching_rules(
            self.homebase,
            facts=(
                "gl-wall-gates-issued 2",
                "wall-completed-percentage 2 >= 75",
                "not (can-build-gate-with-escrow 2)",
            ),
            actions=("gl-wall-gate-attempts c:+ 1",),
        )
        self.assertEqual(len(third_gate_wait), 1)
        self.assertIn("gl-wall-gates-issued c:< 3", self.homebase)

    def test_dejbjerg_moves_persistent_form_without_unpacking(self) -> None:
        self.assertIn("c: dejbjerg-wagon-stationary c: 10", self.germani)
        self.assertIn("object-data-action != actionid-gather", self.germani)
        self.assertIn("local-total c:>= 3", self.germani)
        self.assertIn("DEJBJERG-SEARCH-WORKERS", self.germani)
        self.assertIn("gl-dejbjerg-rejected-id1", self.germani)
        self.assertIn("DEJBJERG-CHECK-CURRENT", self.germani)
        self.assertIn("gl-dejbjerg-home-distance c:>= 14", self.germani)
        self.assertIn(
            "(up-target-point gl-dejbjerg-target-x action-move -1 stance-no-attack)",
            self.germani,
        )
        self.assertFalse(
            matching_rules(self.germani, actions=("action-unpack",))
        )
        self.assertIn("dejbjerg-wagon-mobile < 1", self.germani)
        self.assertIn("dejbjerg-wagon-stationary < 1", self.germani)

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
        self.assertTrue(all(0 <= value <= 19 for value in groups.values()))
        self.assertNotEqual(groups["naval-scout-group"], groups["opportunistic-raid-group"])
        self.assertNotEqual(groups["relic-ferry-transport-group"], groups["transport-screen-group"])
        self.assertNotEqual(groups["attack-boarding-group"], 0)
        self.assertNotEqual(groups["attack-boarding-group"], groups["migration-boarding-group"])
        self.assertNotEqual(groups["attack-transport-group"], groups["migration-transport-group"])
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
        self.assertEqual(len(raid_release), 0) # no routine global home recall
        severe = (Path(__file__).resolve().parents[1] / "rawai-severe-defense.per").read_text()
        self.assertEqual(len(matching_rules(severe,
            facts=("(goal gl-owner-severe-armed YES)", "local-total g:== gl-owner-severe-members"),
            actions=("(set-goal gl-raid-state RAID-IDLE)",))), 1)

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
                "object-data-idling != 1",
                "object-data-action == actionid-explore",
                "object-data-action == actionid-follow",
                "object-data-map-zone-id g:== gl-naval-opportunity-rejected-zone",
                "object-data-map-zone-id g:== gl-naval-opportunity-rejected-zone2",
                "NAVAL-OPPORTUNITY-FIND-SOURCE",
            ),
        )
        self.assertEqual(len(trigger), 1)
        self.assertIn("object-data-group-flag >= 0", trigger[0][4])
        continuation = matching_rules(self.military,
            facts=("NAVAL-OPPORTUNITY-FIND-SOURCE",),
            actions=("object-data-map-zone-id g:== gl-naval-opportunity-rejected-zone3",))
        self.assertEqual(len(continuation), 1)
        self.assertGreater(continuation[0][0], trigger[0][0])
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
            actions=("naval opportunity wake: %d",),
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

    def test_relic_ferry_verifies_exact_passenger_before_departure(self) -> None:
        loading = matching_rules(
            self.military,
            facts=("(goal gl-relic-ferry-state RELIC-FERRY-LOADING)",),
            actions=(
                "(fe-filter-garrisoned c: 1)",
                "(up-add-object-by-id search-local g: gl-relic-ferry-unit-id)",
                "(set-goal gl-relic-ferry-state RELIC-FERRY-CHECK-LOAD)",
            ),
        )
        self.assertEqual(len(loading), 1)
        self.assertFalse(
            matching_rules(
                self.military,
                facts=(
                    "(goal gl-relic-ferry-state RELIC-FERRY-CHECK-LOAD)",
                    "object-data-garrison-count",
                ),
            )
        )

        outbound = matching_rules(
            self.military,
            facts=(
                "(goal gl-relic-ferry-state RELIC-FERRY-CHECK-LOAD)",
                "(goal gl-relic-ferry-direction RELIC-FERRY-OUTBOUND)",
                "object-data-garrisoned == 1",
            ),
            actions=(
                "(up-add-object-by-id search-local g: gl-relic-ferry-transport-id)",
                "gl-relic-ferry-target-x action-unload",
                "RAW44R relic ferry outbound unit",
                "RAW44R relic ferry outbound hull",
                "RAW44R relic ferry target",
                "(set-goal gl-relic-ferry-state RELIC-FERRY-SAILING)",
            ),
        )
        self.assertEqual(len(outbound), 1)

        returning = matching_rules(
            self.military,
            facts=(
                "(goal gl-relic-ferry-state RELIC-FERRY-CHECK-LOAD)",
                "(goal gl-relic-ferry-direction RELIC-FERRY-RETURN)",
                "object-data-garrisoned == 1",
            ),
            actions=(
                "(up-add-object-by-id search-local g: gl-relic-ferry-transport-id)",
                "gl-home-anchor-x action-unload",
                "RAW44R relic ferry return unit",
                "RAW44R relic ferry return hull",
                "(set-goal gl-relic-ferry-state RELIC-FERRY-SAILING)",
            ),
        )
        self.assertEqual(len(returning), 1)

        pending = matching_rules(
            self.military,
            facts=(
                "(goal gl-relic-ferry-state RELIC-FERRY-CHECK-LOAD)",
                "object-data-garrisoned != 1",
                "(goal gl-relic-ferry-load-wait-reported NO)",
            ),
            actions=(
                "RAW44R relic ferry passenger pending",
                "(set-goal gl-relic-ferry-load-wait-reported YES)",
                "(set-goal gl-relic-ferry-state RELIC-FERRY-LOADING)",
            ),
        )
        missing = matching_rules(
            self.military,
            facts=(
                "(goal gl-relic-ferry-state RELIC-FERRY-CHECK-LOAD)",
                "(not (up-set-target-object search-local c: 0))",
                "(goal gl-relic-ferry-load-wait-reported NO)",
            ),
            actions=(
                "RAW44R relic ferry passenger missing",
                "(set-goal gl-relic-ferry-load-wait-reported YES)",
                "(set-goal gl-relic-ferry-state RELIC-FERRY-LOADING)",
            ),
        )
        self.assertEqual(len(pending), 1)
        self.assertEqual(len(missing), 1)
        self.assertIn(
            "(set-goal gl-relic-ferry-load-wait-reported NO)",
            self.init_goals,
        )

    def test_roman_legionary_and_scorpion_producers_use_concrete_units(self) -> None:
        legionaries = (
            "elite-legionary",
            "elite-legionary-melee",
            "legionary",
            "legionary-melee",
        )
        cadence_fact = "gl-game-time g:>= gl-legionary-request-next"
        cadence_actions = (
            "gl-legionary-request-next g:= gl-game-time",
            "gl-legionary-request-next c:+ 10",
        )
        empire_order = (
            "elite-legionary",
            "elite-legionary-melee",
            "legionary",
            "legionary-melee",
        )
        republic_order = (
            "elite-legionary-melee",
            "elite-legionary",
            "legionary-melee",
            "legionary",
        )
        self.assertIn("(set-goal gl-legionary-request-next 0)", self.init_goals)
        for common in (self.military_common, self.military_common_hard):
            empire_rules = []
            for unit in empire_order:
                rules = matching_rules(
                    common,
                    facts=(
                        "gl-legionary-family-count g:< gl-ten-percent",
                        cadence_fact,
                    ),
                    actions=(
                        f"(up-train gl-unitescrow-state c: {unit})",
                        "Roman Legionary request: %d",
                        *cadence_actions,
                    ),
                )
                self.assertEqual(len(rules), 1)
                empire_rules.extend(rules)
            self.assertEqual(
                tuple(
                    re.search(r"\(up-train\s+\S+\s+c:\s+([^\s)]+)", rule[4]).group(1)
                    for rule in sorted(empire_rules)
                ),
                empire_order,
            )

            for bound in (
                "gl-ten-percent",
                "gl-five-percent",
                "gl-two-percent",
                "gl-one-percent",
            ):
                republic_rules = []
                for unit in republic_order:
                    rules = matching_rules(
                        common,
                        facts=(
                            f"gl-legionary-family-count g:< {bound}",
                            cadence_fact,
                        ),
                        actions=(
                            f"(up-train gl-unitescrow-state c: {unit})",
                            "Roman Republic Legionary request: %d",
                            *cadence_actions,
                        ),
                    )
                    self.assertEqual(len(rules), 1)
                    republic_rules.extend(rules)
                self.assertEqual(
                    tuple(
                        re.search(
                            r"\(up-train\s+\S+\s+c:\s+([^\s)]+)", rule[4]
                        ).group(1)
                        for rule in sorted(republic_rules)
                    ),
                    republic_order,
                )
            for invalid_train_operand in (
                "c: legionary-ranged-line",
                "c: legionary-melee-line",
            ):
                self.assertNotIn(invalid_train_operand, common)

        # The release removed the duplicate civ-local baseline producers. The
        # common role machinery above remains the sole Legionary producer;
        # these civ files retain only the engine availability/trainability
        # diagnostics (including their transport-branch chat actions).
        for civ in (self.romeemp, self.romerep):
            for unit in legionaries:
                self.assertEqual(
                    matching_rules(
                        civ,
                        actions=(f"(up-train gl-unitescrow-state c: {unit})",),
                    ),
                    [],
                )

        for civ_name in ("romeemp", "romerep"):
            legionary_family = next(
                family
                for family in self.unique_manifest["civs"][civ_name]["families"]
                if family["name"] == "Legionary"
            )
            self.assertEqual(set(legionary_family["train_units"]), set(legionaries))

        for unit in ("heavy-scorpion", "scorpion"):
            rules = matching_rules(
                self.military_common,
                facts=("(unit-type-count-total scorpion-line g:< gl-three-percent)",),
                actions=(f"(up-train gl-unitescrow-state c: {unit})",),
            )
            self.assertEqual(len(rules), 1)
        for invalid_train_operand in (
            "c: scorpion-line",
        ):
            self.assertNotIn(invalid_train_operand, self.military_common)

        # Dacian and Imitation Legionary families are also supplied by the
        # shared/common bounded production rules after duplicate cleanup.
        for common in (self.military_common, self.military_common_hard):
            for unit in ("falx-warrior", "elite-falx-warrior", "imitation-legionary-line"):
                self.assertTrue(
                    matching_rules(
                        common,
                        actions=(f"(up-train gl-unitescrow-state c: {unit})",),
                    ),
                    f"common production is missing {unit}",
                )

        # Guard the removed role-independent duplicate paths against silent
        # reintroduction.
        self.assertEqual(
            matching_rules(self.dacians, actions=("(train falx-warrior-line)",)),
            [],
        )
        for civ in (self.seleucids, self.pontus):
            self.assertEqual(
                matching_rules(civ, actions=("(train imitation-legionary-line)",)),
                [],
            )

        for civ, label in (
            (self.romeemp, "Roman Legionary"),
            (self.romerep, "Roman Republic Legionary"),
        ):
            unavailable = matching_rules(
                civ,
                facts=tuple(
                    f"(not (unit-available {unit}))" for unit in legionaries
                ),
                actions=(
                    f"{label} engine reports all forms unavailable: %d",
                    "(disable-self)",
                ),
            )
            blocked = matching_rules(
                civ,
                facts=tuple(
                    f"(not (up-can-train gl-unitescrow-state c: {unit}))"
                    for unit in legionaries
                ),
                actions=(
                    f"{label} all-form trainability blocked: %d",
                    "(disable-self)",
                ),
            )
            self.assertEqual(len(unavailable), 1)
            self.assertEqual(len(blocked), 1)
            for unit in legionaries:
                self.assertIn(f"(unit-available {unit})", blocked[0][3])

    def test_allied_resource_aid_is_scaled_identified_and_reserve_safe(self) -> None:
        for amount in (100, 500, 1000):
            for taunt, resource in ((3, 'food'), (4, 'wood'), (5, 'gold'), (6, 'stone')):
                token = str(taunt) if amount == 100 else f'TAUNT-REQUEST-{resource.upper()}-{amount}'
                requests = matching_rules(self.trade, facts=(f'({resource}-amount < 100)',),
                                          actions=(f'please send {amount} {resource}',))
                self.assertEqual(len(requests), 1)
                for player in range(1, 9):
                    replies = matching_rules(self.trade,
                        facts=(f'(taunt-detected {player} {token})',
                               f'(up-compare-goal gl-self-player-number c:!= {player})',
                               f'(stance-toward {player} ally)'),
                        actions=(f'(tribute-to-player {player} {resource} {amount})',
                                 f'(up-chat-data-to-all str-aid-{resource}-{amount} c: {player})'))
                    self.assertEqual(len(replies), 2 if resource == 'gold' else 1)
        self.assertNotIn('(player-number !=', self.trade)
        self.assertNotIn('please send 600', self.trade)

    def test_pict_team_cows_have_a_persistent_request_budget(self) -> None:
        cow = matching_rules(
            self.economy,
            facts=(
                "gl-pict-cow-requests c:< 4",
                "unit-type-count-total mill-cow g:< gl-one-percent",
                "(can-train mill-cow)",
            ),
            actions=(
                "(train mill-cow)",
                "(up-modify-goal gl-pict-cow-requests c:+ 1)",
            ),
        )
        self.assertEqual(len(cow), 1)

    def test_castle_requests_are_placement_safe_and_cadenced(self) -> None:
        castle = matching_rules(
            self.homebase,
            facts=(
                "(goal gl-migration-placement-lock NO)",
                "(goal gl-placement-pressure-state PLACEMENT-PRESSURE-IDLE)",
                "gl-game-time g:>= gl-castle-request-next",
                "(up-pending-objects c: castle <= 0)",
                "(not (up-pending-placement c: castle))",
            ),
            actions=(
                "(up-build place-normal 0 c: castle)",
                "gl-castle-request-next g:= gl-game-time",
                "gl-castle-request-next c:+ 30",
            ),
        )
        self.assertEqual(len(castle), 1)

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
                "object-data-gather-type != wood",
                "lumber camp live candidates: %d",
                "PLACEMENT-ASSESS",
            ),
        )
        self.assertEqual(len(later_lumber), 1)
        self.assertNotIn("object-data-action != actionid-gather", later_lumber[0][4])
        self.assertNotIn("object-data-target-id", later_lumber[0][4])

        lumber_worker_anchor = matching_rules(
            self.homebase,
            facts=(
                "(goal gl-lumbercamp-placement-state PLACEMENT-ASSESS)",
                "(up-set-target-object search-local c: 0)",
            ),
            actions=(
                "object-data-map-zone-id gl-lumbercamp-resource-zone",
                "position-object gl-lumbercamp-target-x",
                "(up-filter-distance c: -1 c: 12)",
                "(up-find-remote c: tree-class c: 20)",
                "PLACEMENT-FIND-RESOURCE",
            ),
        )
        self.assertEqual(len(lumber_worker_anchor), 1)
        for rejected_id in (
            "gl-lumbercamp-rejected-resource-id",
            "gl-lumbercamp-rejected-resource-id2",
            "gl-lumbercamp-rejected-resource-id3",
        ):
            self.assertIn(f"object-data-id g:== {rejected_id}", lumber_worker_anchor[0][4])

        lumber_assignment = matching_rules(
            self.homebase,
            facts=(
                "(goal gl-lumbercamp-placement-state PLACEMENT-VALIDATE-FOUNDATION-RESOURCE)",
                "object-data-map-zone-id g:== gl-lumbercamp-resource-zone",
            ),
            actions=(
                "(up-add-object-by-id search-remote g: gl-lumbercamp-foundation-id)",
                "(up-filter-distance c: -1 c: 12)",
                "object-data-gather-type != wood",
                "object-data-index g:>= 2",
                "(up-target-objects 0 action-default -1 stance-no-attack)",
            ),
        )
        self.assertEqual(len(lumber_assignment), 1)
        self.assertNotIn("villager-shepherd", lumber_assignment[0][4])
        self.assertNotIn("villager-hunter", lumber_assignment[0][4])

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
            "position-object gl-lumbercamp-target-x",
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
                "(set-goal gl-island-migration-state MIGRATION-PLAN-SCOUT)",
            ),
        )
        self.assertEqual(len(scout_rules), 1)
        self.assertNotIn("gl-island-scout-attempts c:+", scout_rules[0][4])
        reserved_attempt = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-HULL-VERIFY)",
                "(goal gl-island-migration-mission MIGRATION-MISSION-SCOUT)",
                "(up-object-data object-data-group-flag == migration-transport-group)",
                "(up-object-data object-data-id g:== gl-island-migration-transport-id)",
            ),
            actions=(
                "(up-modify-goal gl-island-scout-attempts c:+ 1)",
            ),
        )
        self.assertEqual(len(reserved_attempt), 1)

    def test_home_resource_pressure_evacuates_assigned_fishermen(self) -> None:
        self.assertIn("home resource pressure: %d", self.military)
        self.assertIn("home trees low: %d", self.military)
        low_gold = matching_rules(
            self.military,
            facts=(
                "t-home-resource-pressure == timer-triggered",
                "gold-amount < 200",
                "unit-type-count villager-gold < 1",
                "gl-home-low-gold-samples c:< 4",
            ),
            actions=("gl-home-low-gold-samples c:+ 1",),
        )
        reset_gold = matching_rules(
            self.military,
            facts=("t-home-resource-pressure == timer-triggered",),
            actions=("set-goal gl-home-low-gold-samples 0",),
        )
        self.assertEqual(len(low_gold), 1)
        self.assertEqual(len(reset_gold), 1)
        pressure = matching_rules(
            self.military,
            facts=("gl-home-resource-pressure NO", "gl-home-low-gold-samples c:>= 3"),
            actions=("set-goal gl-home-resource-pressure YES",),
        )
        self.assertEqual(len(pressure), 1)
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
                "(set-goal gl-island-migration-state MIGRATION-OWNERSHIP-CLAIM)",
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
                "(set-goal gl-island-migration-state MIGRATION-PLAN-SCOUT)",
            ),
        )
        self.assertEqual(len(stone_refresh), 1)
        self.assertEqual(len(stone_gate), 1)
        self.assertEqual(len(scout_gate), 1)
        allied_budget = matching_rules(
            self.military,
            facts=(
                "MIGRATION-SCOUT-ALLY-CHECK",
                "gl-island-scout-zone-rejections c:>= 3",
            ),
            actions=(
                "migration scout allied-zone budget exhausted: %d",
                "MIGRATION-IDLE",
            ),
        )
        self.assertEqual(len(allied_budget), 1)
        self.assertIn(
            "(up-modify-goal gl-island-scout-zone-rejections c:+ 1)",
            self.military,
        )

    def test_remote_asset_defense_does_not_truncate_villagers_before_filter(self) -> None:
        verification = (Path(__file__).resolve().parents[1] / 'rawai-attack-verification.per').read_text()
        self.assertIn('(up-find-remote c: all-units-class c: 240)', verification)
        self.assertIn('(up-object-target-data object-data-player g:== gl-verify-victim)', verification)
        self.assertIn('(up-add-object-by-id search-remote g: gl-verify-asset)', verification)
        naval = matching_rules(
            self.military,
            facts=("(goal gl-naval-response-state NAVAL-RESPONSE-IDLE)",),
            actions=(
                "(up-find-local c: villager-class c: 240)",
                "(up-remove-objects search-local object-data-under-attack <= 0)",
                "NAVAL-RESPONSE-HOME-FIND",
            ),
        )
        self.assertEqual(len(naval), 1)
        for rule in naval:
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

        timed_check = matching_rules(
            self.military,
            facts=(
                "(goal gl-relic-ferry-state RELIC-FERRY-WATCHDOG-RETURN)",
                "(up-timer-status t-relic-ferry == timer-triggered)",
            ),
            actions=("RELIC-FERRY-WATCHDOG-CHECK",),
        )
        retry = matching_rules(
            self.military,
            facts=(
                "(goal gl-relic-ferry-state RELIC-FERRY-WATCHDOG-CHECK)",
                "object-data-garrison-count > 0",
                "gl-relic-ferry-return-attempts c:< 3",
            ),
            actions=(
                "gl-home-anchor-x action-unload",
                "gl-relic-ferry-return-attempts c:+ 1",
                "(up-set-timer c: t-relic-ferry c: 30)",
                "RELIC-FERRY-WATCHDOG-RETURN",
            ),
        )
        self.assertEqual(len(timed_check), 1)
        self.assertEqual(len(retry), 1)
        terminal = matching_rules(
            self.military,
            facts=(
                "(up-timer-status t-relic-ferry == timer-triggered)",
                "gl-relic-ferry-return-attempts c:>= 3",
            ),
            actions=("relic ferry watchdog abort: %d", "RELIC-FERRY-IDLE"),
        )
        self.assertEqual(len(terminal), 1)

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
        pack_wait = matching_rules(
            self.military,
            facts=("(goal gl-siege-target-state SIEGE-TARGET-FIND-STRUCTURE)",),
            actions=(
                "(up-find-local c: palintonon c: 20)",
                "object-data-map-zone-id g:!= gl-siege-target-zone",
                "action-pack",
                "SIEGE-TARGET-PACK-WAIT",
            ),
        )
        grouping = matching_rules(
            self.military,
            facts=(
                "(goal gl-siege-target-state SIEGE-TARGET-PACK-WAIT)",
                "t-siege-target == timer-triggered",
            ),
            actions=(
                "up-add-object-by-id search-remote g: gl-siege-target-id",
                "(up-create-group 0 0 c: siege-objective-group)",
                "SIEGE-TARGET-PACK-CHECK",
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
        self.assertEqual(len(pack_wait), 1)
        self.assertEqual(len(grouping), 1)
        self.assertEqual(len(command), 1)
        self.assertIn("up-find-player enemy find-ordered gl-siege-target-player", self.military)
        self.assertIn("up-find-next-player enemy find-ordered gl-siege-target-player", self.military)
        self.assertIn("SIEGE-TARGET-ADVANCE-PLAYER", self.military)
        self.assertIn("SIEGE-TARGET-NEXT-PLAYER", self.military)
        idle_pack = matching_rules(
            self.military,
            facts=(
                "gl-siege-target-state SIEGE-TARGET-FALLBACK",
                "up-set-target-object search-local c: 0",
            ),
            actions=(
                "up-target-point position-self-x action-pack",
                "idle Palintonons packed: %d",
                "SIEGE-TARGET-IDLE",
            ),
        )
        self.assertEqual(len(idle_pack), 1)
        idle_pack_selection = matching_rules(
            self.military,
            facts=(
                "t-siege-target == timer-triggered",
                "unit-type-count-total palintonon >= 1",
                "players-building-count any-enemy < 1",
            ),
            actions=(
                "up-reset-group c: siege-objective-group",
                "(set-goal gl-siege-target-zone -1)",
                "SIEGE-TARGET-FALLBACK",
            ),
        )
        self.assertEqual(len(idle_pack_selection), 1)
        fallback_rebuild = matching_rules(
            self.military,
            facts=("(goal gl-siege-target-state SIEGE-TARGET-FALLBACK)",),
            actions=(
                "(up-full-reset-search)",
                "(up-find-local c: palintonon c: 20)",
                "object-data-type != palintonon",
                "object-data-idling != 1",
            ),
        )
        self.assertEqual(len(fallback_rebuild), 1)

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
            actions=(
                "RAW44B migration full hull: %d",
                "RAW44B migration load target: %d",
                "MIGRATION-SHORE-INIT",
            ),
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
                "RAW44B migration partial hull: %d",
                "RAW44B migration load target: %d",
                "TRANSPORT-LOAD-TERMINAL-PARTIAL",
                "MIGRATION-LOAD-DIAG-FIND",
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
                "RAW44B migration abort loaded hull: %d",
                "RAW44B migration load target: %d",
                "TRANSPORT-LOAD-TERMINAL-ABORT",
                "MIGRATION-LOAD-DIAG-FIND",
            ),
        )
        self.assertEqual(len(loaded_abort), 1)
        empty_abort = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-CHECK-LOAD)",
                "(up-timer-status t-island-migration == timer-triggered)",
                "object-data-garrison-count <= 0",
            ),
            actions=(
                "RAW44B migration abort empty hull: %d",
                "RAW44B migration load target: %d",
            ),
        )
        self.assertEqual(len(empty_abort), 2)
        early_sample = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-CHECK-LOAD)",
                "(up-timer-status t-island-migration-board-retry == timer-triggered)",
                "(goal gl-island-migration-load-reported NO)",
            ),
            actions=(
                "object-data-garrison-count gl-island-migration-load-observed",
                "MIGRATION-LOAD-DIAG-FIND",
            ),
        )
        diagnose = matching_rules(
            self.military,
            facts=("MIGRATION-LOAD-DIAG-PASSENGER",),
            actions=(
                "object-data-id gl-island-migration-load-candidate-id",
                "object-data-action gl-island-migration-load-candidate-action",
                "object-data-target-id gl-island-migration-load-candidate-target-id",
                "object-data-order gl-island-migration-load-candidate-order",
                "object-data-cmdid gl-island-migration-load-candidate-cmdid",
                "object-data-distance gl-island-migration-load-candidate-distance",
                "object-data-map-zone-id gl-island-migration-load-candidate-zone",
                "object-data-group-flag gl-island-migration-load-candidate-group-flag",
                "object-data-move-x gl-island-migration-load-candidate-move-x",
                "object-data-move-y gl-island-migration-load-candidate-move-y",
                "object-data-idling gl-island-migration-load-candidate-idling",
            ),
        )
        diagnostic_retry = matching_rules(
            self.military,
            facts=(
                "MIGRATION-LOAD-DIAG-APPLY",
                "TRANSPORT-LOAD-TERMINAL-NONE",
            ),
            actions=(
                "(up-target-objects 0 action-garrison -1 stance-no-attack)",
                "(set-goal gl-island-migration-load-reported YES)",
                "MIGRATION-LOADING",
            ),
        )
        partial_apply = matching_rules(
            self.military,
            facts=(
                "MIGRATION-LOAD-DIAG-APPLY",
                "TRANSPORT-LOAD-TERMINAL-PARTIAL",
            ),
            actions=("position-self-x action-stop", "MIGRATION-SHORE-INIT"),
        )
        loaded_abort_apply = matching_rules(
            self.military,
            facts=(
                "MIGRATION-LOAD-DIAG-APPLY",
                "TRANSPORT-LOAD-TERMINAL-ABORT",
                "gl-island-migration-load-observed c:== 1",
            ),
            actions=("gl-home-anchor-x action-unload", "MIGRATION-RETURNING"),
        )
        empty_abort_apply = matching_rules(
            self.military,
            facts=(
                "MIGRATION-LOAD-DIAG-APPLY",
                "TRANSPORT-LOAD-TERMINAL-ABORT",
                "gl-island-migration-load-observed c:<= 0",
            ),
            actions=(
                "(up-reset-group c: migration-boarding-group)",
                "MIGRATION-IDLE",
            ),
        )
        self.assertEqual(len(early_sample), 1)
        self.assertEqual(len(diagnose), 1)
        self.assertEqual(len(diagnostic_retry), 1)
        self.assertEqual(len(partial_apply), 1)
        self.assertEqual(len(loaded_abort_apply), 1)
        self.assertEqual(len(empty_abort_apply), 1)
        self.assertNotIn(
            "up-path-distance gl-island-migration-origin-x",
            self.military,
        )
        self.assertNotIn("MIGRATION-CHECK-LOAD-RESULT", self.military)

        watchdog = matching_rules(
            self.military,
            facts=(
                "(up-timer-status t-island-migration == timer-triggered)",
                "(not (goal gl-island-migration-state MIGRATION-IDLE))",
            ),
            actions=(
                "gl-home-anchor-x action-unload",
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

    def test_generic_villager_cleanup_preserves_transport_reservation(self) -> None:
        cleanup = matching_rules(
            self.general,
            actions=(
                "(up-find-local c: villager-class g: villager-count)",
                "(up-create-group 0 0 c: attack-transport-group)",
                "(up-modify-group-flag 1 c: attack-transport-group)",
            ),
        )
        self.assertEqual(len(cleanup), 1)
        actions = cleanup[0][4]
        reservation_filter = (
            "(up-remove-objects search-local object-data-group-flag "
            ">= 0)"
        )
        self.assertIn(reservation_filter, actions)
        self.assertLess(actions.index(reservation_filter), actions.index("(up-create-group"))
        self.assertLess(actions.index(reservation_filter), actions.index("(up-modify-group-flag"))

        # Model this exact selector's flag mutations: before the fix the
        # reserved Purple candidate is selected, assigned 0, then cleared -2.
        # Ordinary unreserved villagers must still receive the old cleanup.
        reservation = int(re.search(
            r"\(defconst migration-boarding-group (\d+)\)", self.customconstants
        ).group(1))
        roster = {31871: reservation, 60000: -2}
        def after_cleanup(source_actions: str) -> dict[int, int]:
            selected = list(roster)
            if reservation_filter in source_actions:
                selected = [unit for unit in selected if roster[unit] < 0]
            result = dict(roster)
            for unit in selected:
                result[unit] = 0
            for unit in selected:
                result[unit] = -2
            return result

        self.assertEqual(after_cleanup(actions), {31871: reservation, 60000: -2})
        self.assertEqual(after_cleanup(actions.replace(reservation_filter, ""))[31871], -2)
        self.assertIn("(up-modify-group-flag 0 c: attack-transport-group)", self.general)
        self.assertIn("(up-reset-group c: attack-transport-group)", self.general)
        self.assertIn("(up-object-data object-data-order == orderid-enter)", self.general)

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
        self.assertEqual(len(target_rules), 4)
        self.assertEqual(
            {0, 1, 2, 3},
            {
                int(re.search(r"gl-naval-scout-leg\s+(\d+)", rule[3]).group(1))
                for rule in target_rules
            },
        )
        scout_block = self.military[: self.military.find(";Ordinary light ships intercept")]
        self.assertNotIn("(up-find-remote c: gold-mine", scout_block)
        self.assertNotIn("object-data-map-zone-id g:== gl-home-zone", scout_block)
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

    def test_engine_explorer_numbers_are_edge_triggered(self) -> None:
        guarded_writes = (
            (
                "(up-compare-sn sn-number-explore-groups g:!= desired-military-explorers)",
                "(up-modify-sn sn-number-explore-groups g:= desired-military-explorers)",
            ),
            (
                "(up-compare-sn sn-cap-civilian-explorers g:!= desired-civilian-explorers)",
                "(up-modify-sn sn-cap-civilian-explorers g:= desired-civilian-explorers)",
            ),
            (
                "(up-compare-sn sn-minimum-civilian-explorers g:!= desired-civilian-explorers)",
                "(up-modify-sn sn-minimum-civilian-explorers g:= desired-civilian-explorers)",
            ),
            (
                "(up-compare-sn sn-number-boat-explore-groups c:!= 0)",
                "(set-strategic-number sn-number-boat-explore-groups 0)",
            ),
            (
                "(up-compare-sn sn-total-number-explorers c:!= 2)",
                "(set-strategic-number sn-total-number-explorers 2)",
            ),
            (
                "(up-compare-sn sn-total-number-explorers c:!= 0)",
                "(set-strategic-number sn-total-number-explorers 0)",
            ),
        )
        for fact, action in guarded_writes:
            self.assertEqual(
                len(matching_rules(self.general, facts=(fact,), actions=(action,))),
                1,
            )

        unconditional_writers = matching_rules(
            self.general,
            facts=("(true)",),
            actions=("sn-number-explore-groups",),
        )
        self.assertEqual(unconditional_writers, [])

    def test_late_phases_release_engine_explorer_ownership(self) -> None:
        expected = {1: (1, 1), 2: (2, 0), 3: (2, 0), 4: (0, 0), 5: (0, 0)}
        for phase, (military, civilian) in expected.items():
            rules = matching_rules(
                self.pop,
                facts=(f"(goal current-phase {phase})",),
                actions=(
                    "desired-military-explorers",
                    "desired-civilian-explorers",
                ),
            )
            self.assertEqual(len(rules), 1)
            actions = rules[0][4]
            military_assignment = re.search(
                r"\((?:set-goal|up-modify-goal) desired-military-explorers "
                r"(?:c:= )?(\d+)\)",
                actions,
            )
            civilian_assignment = re.search(
                r"\((?:set-goal|up-modify-goal) desired-civilian-explorers "
                r"(?:c:= )?(\d+)\)",
                actions,
            )
            self.assertIsNotNone(military_assignment)
            self.assertIsNotNone(civilian_assignment)
            self.assertEqual(int(military_assignment.group(1)), military)
            self.assertEqual(int(civilian_assignment.group(1)), civilian)
            self.assertEqual(military + civilian, 2 if phase < 4 else 0)

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
                "gl-quarantine-transport-id c:< 0",
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

    def test_home_emergency_does_not_recall_loaded_or_remote_passengers(self) -> None:
        severe = (Path(__file__).resolve().parents[1] / "rawai-severe-defense.per").read_text()
        self.assertIn("object-data-garrisoned == 1", severe)
        self.assertIn("local-total g:== gl-owner-severe-members", severe)
        self.assertIn("object-data-map-zone-id g:!= gl-home-zone", severe)
        self.assertNotIn("action-unload", severe)

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
            ),
            actions=(
                "(up-filter-status c: status-pending c: list-active)",
                "c: 8",
                "object-data-map-zone-id g:!= gl-island-migration-zone",
                "(set-goal gl-island-migration-state MIGRATION-FIND-DROPSITE)",
            ),
        )
        self.assertEqual(len(pending_searches), 3)
        for row in pending_searches:
            self.assertNotIn('up-pending-objects', row[3])
            self.assertIn('gl-migration-build-x', row[4])
        publish = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-CHECK-DROPSITE)",
                "(up-object-data object-data-status == status-ready)",
            ),
            actions=(
                "(set-goal gl-island-colony-established YES)",
                "MIGRATION-RETASK-DROPSITE",
            ),
        )
        self.assertEqual(len(publish), 1)
        self.assertEqual(
            self.military.count("(set-goal gl-island-colony-established YES)"),
            1,
        )

        retask = matching_rules(
            self.military,
            facts=("MIGRATION-ASSIGN-RETASK-ANCHOR",),
            actions=(
                "(up-set-group search-local c: migration-boarding-group)",
                "search-remote g: gl-island-migration-anchor-id",
                "(up-target-objects 0 action-default -1 stance-no-attack)",
                "migration settlers retasked: %d",
                "MIGRATION-RELEASE-COLONY",
            ),
        )
        self.assertEqual(len(retask), 1)
        self.assertIn(
            "(up-find-remote g: gl-island-migration-anchor-class c: 20)",
            self.military,
        )
        self.assertIn("migration post-build resource exhausted: %d", self.military)

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
                "gl-home-anchor-x action-unload",
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
                "(goal map-type ISLANDS)",
                "gl-available-transport-count g:>= gl-transport-required",
                "(goal gl-island-migration-state MIGRATION-QUARANTINED)",
            ),
            actions=("(set-goal gl-land-transport-ready YES)",),
        )
        self.assertEqual(len(quarantine_ready), 1)
        busy_controller = matching_rules(
            self.economy,
            facts=(
                "(goal map-type ISLANDS)",
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
        for dispatch in land_dispatches:
            self.assertIn(
                "gl-land-target-scan-player g:== gl-land-target-current-player",
                dispatch[3],
            )
        persisted_land_dispatches = matching_rules(
            self.military,
            facts=("(goal gl-attack-dispatch-owner ATTACK-DISPATCH-LAND)",),
            actions=("up-chat-data-to-self \"land dispatch",),
        )
        self.assertEqual(len(persisted_land_dispatches), 4)

    def test_hybrid_land_dispatch_depends_on_target_land_zone(self) -> None:
        scanner = matching_rules(
            self.military,
            facts=(
                "gl-game-time g:>= gl-land-target-scan-next",
                "LAND-TARGET-SCAN-IDLE",
                "(players-building-count target-player >= 1)",
            ),
            actions=(
                "gl-land-target-scan-player s:= sn-target-player-number",
                "sn-focus-player-number s:= sn-target-player-number",
                "(up-find-remote c: building-class c: 40)",
                "LAND-TARGET-SCAN-CHECK",
            ),
        )
        self.assertEqual(len(scanner), 1)
        self.assertIn(
            "object-data-map-zone-id gl-land-target-zone", self.military
        )
        self.assertIn(
            "gl-land-target-current-player s:= sn-target-player-number",
            self.military,
        )
        stale_target = matching_rules(
            self.military,
            facts=(
                "gl-land-target-scan-player g:!= gl-land-target-current-player",
                "(goal gl-land-target-needs-transport NO)",
            ),
            actions=(
                "(set-goal gl-land-target-needs-transport YES)",
                "land target scan stale player: %d",
            ),
        )
        self.assertEqual(len(stale_target), 1)
        guarded_land_dispatches = matching_rules(
            self.military,
            facts=("(goal gl-land-transport-ready YES)",),
            actions=("(attack-now)",),
        )
        self.assertEqual(len(guarded_land_dispatches), 6)
        for dispatch in guarded_land_dispatches:
            self.assertIn(
                "gl-land-target-scan-player g:== gl-land-target-current-player",
                dispatch[3],
            )
        hybrid_wait = matching_rules(
            self.economy,
            facts=(
                "(goal map-type RIVERS)",
                "(goal gl-land-target-needs-transport YES)",
                "gl-available-transport-count g:< gl-transport-required",
            ),
            actions=("(set-goal gl-land-transport-ready NO)",),
        )
        self.assertEqual(len(hybrid_wait), 1)
        same_zone = matching_rules(
            self.economy,
            facts=(
                "(goal map-type RIVERS)",
                "(goal gl-land-target-needs-transport NO)",
            ),
            actions=("(set-goal gl-land-transport-ready YES)",),
        )
        self.assertEqual(len(same_zone), 1)
        target_shadow = matching_rules(
            self.military,
            facts=(
                "(players-building-count target-player >= 1)",
                "(player-in-game target-player)",
                "(not (stance-toward target-player ally))",
            ),
            actions=(
                "sn-focus-player-number s:= sn-target-player-number",
                "gl-land-target-current-player s:= sn-target-player-number",
            ),
        )
        self.assertEqual(len(target_shadow), 1)
        self.assertNotIn("military-superiority", target_shadow[0][3])

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
                "gl-land-target-current-player s:= sn-target-player-number",
            ),
        )
        self.assertEqual(len(focus_sync), 1)
        self.assertNotIn("military-superiority", focus_sync[0][3])
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
        rush_facts = re.sub(r"\s+", " ", rush_attack[0][3])
        self.assertIn("(goal map-type LAND)", rush_facts)
        self.assertIn("(goal gl-land-transport-ready YES)", rush_facts)
        self.assertIn(
            "(up-compare-goal gl-land-target-current-player c:>= 1)",
            rush_facts,
        )
        self.assertIn(
            "(up-compare-goal gl-land-target-current-player c:<= 8)",
            rush_facts,
        )
        self.assertIn(
            "(up-compare-goal gl-land-target-scan-player "
            "g:== gl-land-target-current-player)",
            rush_facts,
        )
        self.assertIn("(player-in-game target-player)", rush_facts)
        self.assertIn("(not (stance-toward target-player ally))", rush_facts)
        self.assertIn("(players-building-count target-player >= 1)", rush_facts)
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
                "gl-home-anchor-x action-unload",
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
                "(up-add-object-by-id search-local g: gl-island-migration-transport-id)",
                "MIGRATION-QUARANTINE-CHECK",
            ),
        )
        self.assertEqual(len(quarantine_check), 1)
        quarantine_terminal = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-QUARANTINE-CHECK)",
                "object-data-garrison-count <= 0",
            ),
            actions=(
                "(up-modify-group-flag 0 c: migration-transport-group)",
                "(set-goal gl-island-migration-transport-id -1)",
                "(set-goal gl-island-migration-state MIGRATION-IDLE)",
            ),
        )
        self.assertEqual(len(quarantine_terminal), 1)
        detached_quarantine = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-QUARANTINE-CHECK)",
                "object-data-garrison-count > 0",
                "gl-quarantine-transport-id c:< 0",
            ),
            actions=(
                "gl-quarantine-transport-id g:= gl-island-migration-transport-id",
                "(up-modify-group-flag 0 c: migration-boarding-group)",
                "(up-modify-group-flag 0 c: migration-transport-group)",
                "migration quarantined hull detached: %d",
                "(set-goal gl-island-migration-transport-id -1)",
                "(set-goal gl-island-migration-state MIGRATION-IDLE)",
            ),
        )
        self.assertEqual(len(detached_quarantine), 1)
        slot_busy = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-QUARANTINE-CHECK)",
                "object-data-garrison-count > 0",
                "gl-quarantine-transport-id c:>= 0",
            ),
            actions=(
                "position-object point-x",
                "point-x action-unload",
                "migration quarantine slot busy: %d",
                "(up-modify-group-flag 0 c: migration-transport-group)",
                "(set-goal gl-island-migration-transport-id -1)",
                "(set-goal gl-island-migration-state MIGRATION-IDLE)",
            ),
        )
        self.assertEqual(len(slot_busy), 1)
        self.assertNotIn(
            "gl-quarantine-transport-id g:= gl-island-migration-transport-id",
            slot_busy[0][4],
        )
        detached_scan = matching_rules(
            self.military,
            facts=(
                "gl-quarantine-transport-id c:>= 0",
                "TRANSPORT-QUARANTINE-IDLE",
                "gl-game-time g:>= gl-quarantine-transport-next",
            ),
            actions=(
                "up-add-object-by-id search-local g: gl-quarantine-transport-id",
                "TRANSPORT-QUARANTINE-CHECK",
            ),
        )
        self.assertEqual(len(detached_scan), 1)
        detached_retry = matching_rules(
            self.military,
            facts=(
                "TRANSPORT-QUARANTINE-CHECK",
                "object-data-garrison-count > 0",
            ),
            actions=(
                "position-object point-x",
                "point-x action-unload",
                "detached quarantine retry: %d",
                "TRANSPORT-QUARANTINE-IDLE",
            ),
        )
        self.assertEqual(len(detached_retry), 1)
        terminal_quarantine = matching_rules(
            self.military,
            facts=(
                "TRANSPORT-QUARANTINE-CHECK",
                "object-data-garrison-count > 0",
                "(goal gl-quarantine-transport-attempts 3)",
            ),
            actions=(
                "detached quarantine terminal: %d",
                "TRANSPORT-QUARANTINE-TERMINAL",
            ),
        )
        self.assertEqual(len(terminal_quarantine), 1)
        detached_recovered = matching_rules(
            self.military,
            facts=(
                "TRANSPORT-QUARANTINE-CHECK",
                "object-data-garrison-count <= 0",
            ),
            actions=(
                "detached quarantine recovered: %d",
                "(set-goal gl-quarantine-transport-id -1)",
            ),
        )
        self.assertEqual(len(detached_recovered), 1)
        detached_lost = matching_rules(
            self.military,
            facts=(
                "TRANSPORT-QUARANTINE-CHECK",
                "(not (up-set-target-object search-local c: 0))",
            ),
            actions=(
                "detached quarantine hull lost: %d",
                "(set-goal gl-quarantine-transport-id -1)",
            ),
        )
        self.assertEqual(len(detached_lost), 1)
        quarantine_exclusion = (
            "(up-remove-objects search-local object-data-id "
            "g:== gl-quarantine-transport-id)"
        )
        remote_quarantine_exclusion = (
            "(up-remove-objects search-remote object-data-id "
            "g:== gl-quarantine-transport-id)"
        )
        self.assertEqual(self.economy.count(quarantine_exclusion), 1)
        local_quarantine_owners = matching_rules(
            self.military,
            actions=(quarantine_exclusion,),
        )
        repair_exclusions = [
            rule for rule in local_quarantine_owners
            if "t-transport-repair == timer-triggered" in rule[3]
        ]
        berth_exclusions = [
            rule for rule in local_quarantine_owners
            if "TRANSPORT-CLEAR-ANCHOR" in rule[3]
        ]
        self.assertEqual(len(repair_exclusions), 1)
        self.assertEqual(len(berth_exclusions), 1)
        self.assertEqual(self.military.count(remote_quarantine_exclusion), 10)
        escort_selector = matching_rules(
            self.military,
            facts=(
                "t-transport-escort == timer-triggered",
                "ESCORT-IDLE",
            ),
            actions=(
                "(up-find-remote c: transport-ship c: 40)",
                remote_quarantine_exclusion,
                "object-data-garrison-count <= 0",
            ),
        )
        self.assertEqual(len(escort_selector), 1)
        migration_gate = matching_rules(
            self.military,
            facts=(
                "t-island-migration == timer-triggered",
                "(goal gl-island-migration-state MIGRATION-IDLE)",
                "(goal gl-colony-towncenter-state COLONY-TC-IDLE)",
            ),
            actions=(
                "(set-goal gl-island-migration-state MIGRATION-GATE-OWNER)",
            ),
        )
        self.assertEqual(len(migration_gate), 1)
        self.assertNotIn("gl-quarantine-transport-id c:< 0", migration_gate[0][3])
        replacement = matching_rules(
            self.economy,
            facts=(
                "gl-quarantine-transport-id c:>= 0",
                "transport-ship g:<= gl-transport-required",
                "(can-train transport-ship)",
            ),
            actions=("(train transport-ship)",),
        )
        self.assertEqual(len(replacement), 1)
        ordinary_producers = matching_rules(
            self.economy,
            facts=("gl-quarantine-transport-id c:< 0",),
            actions=("(train transport-ship)",),
        )
        self.assertEqual(len(ordinary_producers), 2)
        self.assertIn("(set-goal gl-quarantine-transport-id -1)", self.init_goals)
        self.assertIn(
            "(set-goal gl-quarantine-transport-state TRANSPORT-QUARANTINE-IDLE)",
            self.init_goals,
        )
        watchdog = matching_rules(
            self.military,
            facts=(
                "(up-timer-status t-island-migration == timer-triggered)",
                "(not (goal gl-island-migration-state MIGRATION-IDLE))",
            ),
        )
        self.assertEqual(len(watchdog), 1)
        self.assertNotIn("gl-island-migration-route-waits 0", watchdog[0][4])

    def test_migration_uses_bounded_destination_landings_and_scout_release(self) -> None:
        first_candidate = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-ROUTE-WAYPOINT-CHECK)",
                "object-data-distance <= 8",
            ),
            actions=(
                "gl-island-migration-route-waypoint-x gl-msr-selected-land-x",
                "(set-goal gl-island-migration-landing-attempts 0)",
                "MIGRATION-CHECK-LANDING-PATH",
            ),
        )
        crowded_gate = matching_rules(
            self.military,
            facts=(
                "(up-compare-goal villager-count c:>= 60)",
                "(unit-type-count transport-ship >= 1)",
            ),
            actions=(
                "(set-goal gl-island-migration-mission MIGRATION-MISSION-MINING)",
            ),
        )
        self.assertEqual(len(crowded_gate), 2)
        crowded_manifest = matching_rules(
            self.military,
            facts=(
                "(up-compare-goal villager-count c:>= 60)",
                "(goal resources-depleted NO)",
                "(goal gl-home-resource-pressure NO)",
            ),
            actions=(
                "(up-find-local c: villager-class c: 40)",
                "(set-goal gl-island-migration-state MIGRATION-OWNERSHIP-CLAIM)",
            ),
        )
        self.assertEqual(len(crowded_manifest), 1)
        crowded_actions = crowded_manifest[0][4]
        self.assertNotIn("object-data-idling", crowded_actions)
        for protected in (
            "object-data-action == actionid-build",
            "object-data-action == actionid-repair",
            "lid-villager-farmer",
            "lid-villager-fisherman",
            "lid-villager-shepherd",
            "lid-villager-forager",
            "lid-villager-hunter",
            "object-data-target == prey-animal-class",
            "object-data-target == livestock-class",
        ):
            self.assertIn(protected, crowded_actions)
        self.assertEqual(len(first_candidate), 1)
        self.assertNotIn("action-unload", first_candidate[0][4])
        shoreline_candidates = matching_rules(
            self.migration_shoreline,
            facts=(
                "(goal gl-island-migration-state MIGRATION-SHORE-CANDIDATE)",
                "(goal gl-msr-candidate",
            ),
            actions=(
                "gl-island-migration-route-waypoint-x gl-msr-land-x",
                "gl-msr-candidate-water-x gl-msr-water-x",
                "MIGRATION-SHORE-CACHE",
            ),
        )
        self.assertEqual(len(shoreline_candidates), 5)
        for candidate in shoreline_candidates:
            self.assertNotIn("action-unload", candidate[4])
        self.assertNotIn(
            "gl-island-migration-route-waypoint-x c:+ 2",
            self.military,
        )
        self.assertNotIn(
            "gl-island-migration-route-waypoint-x c:- 2",
            self.military,
        )
        path_setup = matching_rules(
            self.military,
            facts=("(goal gl-island-migration-state MIGRATION-CHECK-LANDING-PATH)",),
            actions=(
                "(up-set-target-point gl-island-migration-route-waypoint-x)",
                "gl-island-migration-route-waypoint-x gl-island-migration-landing-zone",
                "(up-add-object-by-id search-local g: gl-island-migration-transport-id)",
            ),
        )
        self.assertEqual(len(path_setup), 1)
        reachable = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-CHECK-LANDING-PATH)",
                "gl-island-migration-landing-zone g:== gl-island-migration-zone",
                "(up-set-target-object search-local c: 0)",
                "(up-path-distance gl-island-migration-route-waypoint-x 0 != 65535)",
            ),
            actions=(
                "gl-island-migration-route-waypoint-x action-unload",
                "RAW44M landing path clear hull: %d",
                "(up-set-timer c: t-island-migration c: 20)",
                "MIGRATION-SAILING",
            ),
        )
        rejected = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-CHECK-LANDING-PATH)",
                "gl-island-migration-landing-zone g:== gl-island-migration-zone",
                "(up-set-target-object search-local c: 0)",
                "(up-path-distance gl-island-migration-route-waypoint-x 0 == 65535)",
            ),
            actions=(
                "RAW44M landing path rejected hull: %d",
                "RAW44M rejected x: %d",
                "RAW44M rejected y: %d",
                "(up-set-timer c: t-island-migration c: 120)",
                "MIGRATION-SHORE-REMEMBER",
            ),
        )
        wrong_zone = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-CHECK-LANDING-PATH)",
                "gl-island-migration-landing-zone g:!= gl-island-migration-zone",
                "(up-set-target-object search-local c: 0)",
            ),
            actions=(
                "RAW44M landing wrong zone hull: %d",
                "RAW44M wrong-zone actual: %d",
                "RAW44M wrong-zone expected: %d",
                "(up-set-timer c: t-island-migration c: 120)",
                "MIGRATION-SHORE-REMEMBER",
            ),
        )
        self.assertEqual(len(reachable), 1)
        self.assertEqual(len(rejected), 1)
        self.assertEqual(len(wrong_zone), 1)
        self.assertNotIn("action-unload", rejected[0][4])
        self.assertNotIn("action-unload", wrong_zone[0][4])
        self.assertIn("MIGRATION-SHORE-EXHAUSTED", self.migration_shoreline)
        scout_release = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-CHECK-LANDING)",
                "(goal gl-island-migration-mission MIGRATION-MISSION-SCOUT)",
                "object-data-garrison-count <= 0",
            ),
            actions=(
                "(up-set-group search-local c: migration-boarding-group)",
                "MIGRATION-VERIFY-SCOUT-LANDING",
            ),
        )
        self.assertEqual(len(scout_release), 1)
        self.assertNotIn("gl-island-migration-origin-x action-move", scout_release[0][4])
        scout_landed = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-VERIFY-SCOUT-LANDING)",
                "(up-set-target-object search-local c: 0)",
            ),
            actions=(
                "position-self-x action-stop",
                "MIGRATION-TASK-SCOUT",
            ),
        )
        self.assertEqual(len(scout_landed), 1)
        scout_not_landed = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-VERIFY-SCOUT-LANDING)",
                "(not (up-set-target-object search-local c: 0))",
            ),
            actions=(
                "migration scout not landed: %d",
                "gl-island-migration-origin-x action-move",
                "MIGRATION-IDLE",
            ),
        )
        self.assertEqual(len(scout_not_landed), 1)
        self.assertIn("migration scout fallback patrol: %d", self.military)
        self.assertIn("(up-copy-point point2-x gl-island-migration-target-x)", self.military)
        self.assertIn("(up-bound-point point3-x point2-x)", self.military)
        self.assertIn("(up-target-point point3-x action-patrol -1 stance-no-attack)", self.military)
        self.assertNotIn("position-opposite point2-x", self.military)
        fallback_confirm = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-CONFIRM-SCOUT-FALLBACK)",
                "(up-set-target-object search-local c: 0)",
            ),
            actions=(
                "point3-x action-patrol",
                "migration scout fallback patrol: %d",
            ),
        )
        self.assertEqual(len(fallback_confirm), 1)
        scout_confirm = matching_rules(
            self.military,
            facts=("(goal gl-island-migration-state MIGRATION-FIND-SCOUT-PATROL)",),
            actions=("(set-goal gl-island-migration-state MIGRATION-CONFIRM-SCOUT)",),
        )
        self.assertEqual(len(scout_confirm), 1)
        self.assertNotIn("object-data-distance > 20", scout_confirm[0][4])

    def test_scout_ferry_rejects_allied_and_recently_visited_zones(self) -> None:
        self.assertIn("MIGRATION-SCOUT-ALLY-START", self.military)
        self.assertIn("MIGRATION-SCOUT-ALLY-CHECK", self.military)
        self.assertIn("migration scout rejected allied zone: %d", self.military)
        scout_gate = matching_rules(
            self.military,
            facts=(
                "(goal gl-island-migration-state MIGRATION-GATE-OWNER)",
                "gl-island-scout-attempts c:< 3",
            ),
            actions=("MIGRATION-PLAN-SCOUT",),
        )
        self.assertEqual(len(scout_gate), 1)
        scout_plan = matching_rules(
            self.military,
            facts=("(goal gl-island-migration-state MIGRATION-PLAN-SCOUT)",),
            actions=(
                "object-data-map-zone-id g:== gl-island-scout-visited-zone",
                "object-data-map-zone-id g:== gl-island-scout-visited-zone2",
                "object-data-map-zone-id g:== gl-island-scout-visited-zone3",
                "MIGRATION-FIND-SCOUT-LANDING",
            ),
        )
        self.assertEqual(len(scout_plan), 1)
        patrol_watchdog = matching_rules(
            self.military,
            facts=(
                "MIGRATION-SCOUT-PATROL-CHECK",
                "object-data-distance > 12",
            ),
            actions=(
                "migration scout patrol retry: %d",
                "point4-x action-move",
                "MIGRATION-IDLE",
            ),
        )
        self.assertEqual(len(patrol_watchdog), 1)

    def test_zero_responder_threat_rebuilds_and_requests_help(self) -> None:
        latch = matching_rules(
            self.military,
            facts=(
                "LOCAL-RESPONSE-COMMAND",
                "gl-local-response-threats c:>= 1",
            ),
            actions=(
                "(set-goal gl-local-threat-active YES)",
                "gl-wall-danger-until c:+ 90",
            ),
        )
        self.assertEqual(len(latch), 1)
        evacuations = matching_rules(
            self.military,
            facts=("LOCAL-RESPONSE-COMMAND",),
            actions=(
                "object-data-action != actionid-build",
                "position-self-x action-stop",
                "up-filter-distance c: 12 c: 48",
                "up-find-remote c: town-center",
                "up-target-objects 0 action-garrison",
            ),
        )
        self.assertEqual(len(evacuations), 2)
        self.assertTrue(any("object-data-target != wall-class" in rule[4] for rule in evacuations))
        self.assertTrue(any("object-data-target != gate-class" in rule[4] for rule in evacuations))
        self.assertTrue(all("up-full-reset-search" in rule[4] for rule in evacuations))
        rebuild = matching_rules(
            self.military,
            facts=("LOCAL-RESPONSE-COMMAND",),
            actions=(
                "up-find-remote c: siege-weapon-class",
                "LOCAL-RESPONSE-REBUILD",
            ),
        )
        self.assertEqual(len(rebuild), 1)
        emergency_barracks = matching_rules(
            self.homebase,
            facts=(
                "(goal gl-local-threat-active YES)",
                "building-type-count-total barracks < 1",
            ),
            actions=("(up-build place-normal 0 c: barracks)",),
        )
        self.assertEqual(len(emergency_barracks), 1)
        self.assertNotIn("wait-techup-requirements", emergency_barracks[0][3])
        help_request = matching_rules(
            self.diplomacy,
            facts=(
                "(goal gl-self-attack-verified YES)",
                "gl-local-response-responders c:<= 0",
            ),
            actions=("My settlement is under attack",),
        )
        self.assertEqual(len(help_request), 1)

    def test_stranded_recovery_reserves_idle_units_and_terminates(self) -> None:
        selector = matching_rules(
            self.military,
            facts=("TRANSPORT-RECOVERY-FIND-TARGET",),
            actions=(
                "object-data-idling != 1",
                "object-data-group-flag >= 0",
                "TRANSPORT-RECOVERY-FIND-UNIT",
            ),
        )
        self.assertEqual(len(selector), 2)
        boarding = matching_rules(
            self.military,
            facts=("TRANSPORT-RECOVERY-OWNERSHIP-CLAIM",),
            actions=(
                                "recovery-boarding-group",
                "g:!= gl-transport-recovery-zone",
                "(up-target-objects 0 action-garrison",
            ),
        )
        self.assertEqual(len(boarding), 1)
        partial = matching_rules(
            self.military,
            facts=(
                "TRANSPORT-RECOVERY-CHECK-LOAD",
                "object-data-garrison-count > 0",
                "timer-triggered",
            ),
            actions=(
                "transport recovery partial departure: %d",
                "TRANSPORT-RECOVERY-SAILING",
            ),
        )
        self.assertEqual(len(partial), 1)
        landing_success = matching_rules(
            self.military,
            facts=(
                "TRANSPORT-RECOVERY-VERIFY-LANDING",
                "up-set-target-object search-local c: 0",
            ),
            actions=(
                "gl-transport-recovery-target-x action-move",
                "TRANSPORT-RECOVERY-IDLE",
            ),
        )
        self.assertEqual(len(landing_success), 1)
        wrong_zone = matching_rules(
            self.military,
            facts=(
                "TRANSPORT-RECOVERY-FIND-WRONG-ZONE",
                "up-set-target-object search-local c: 0",
                "gl-transport-recovery-attempts c:< 3",
            ),
            actions=(
                "object-data-map-zone-id gl-transport-recovery-landing-zone",
                "g:!= gl-transport-recovery-landing-zone",
                "action-garrison",
                "transport recovery wrong-zone reboard: %d",
            ),
        )
        self.assertEqual(len(wrong_zone), 1)
        no_survivors = matching_rules(
            self.military,
            facts=(
                "TRANSPORT-RECOVERY-FIND-WRONG-ZONE",
                "not (up-set-target-object search-local c: 0)",
            ),
            actions=(
                "transport recovery no survivors: %d",
                "TRANSPORT-RECOVERY-IDLE",
            ),
        )
        self.assertEqual(len(no_survivors), 1)
        self.assertIn("transport recovery recalled: %d", self.military)
        self.assertIn("transport recovery quarantined: %d", self.military)

    def test_stale_partial_transport_is_bounded_and_quarantined(self) -> None:
        stale = matching_rules(
            self.military,
            facts=(
                "TRANSPORT-CLEAR-IDLE",
                "t-transport-clear == timer-triggered",
            ),
            actions=(
                "object-data-garrison-count g:>= gl-transport-min-load",
                "TRANSPORT-CLEAR-STALE-FIND",
            ),
        )
        self.assertEqual(len(stale), 1)
        self.assertIn("stale transport quarantined: %d", self.military)
        empty_return = matching_rules(
            self.military,
            facts=(
                "TRANSPORT-CLEAR-STALE-FIND",
                "not (up-set-target-object search-remote c: 0)",
            ),
            actions=(
                "up-filter-distance c: 24 c: -1",
                "object-data-garrison-count > 0",
                "object-data-idling != 1",
                "TRANSPORT-CLEAR-EMPTY-FIND",
            ),
        )
        self.assertEqual(len(empty_return), 1)
        self.assertNotIn("up-set-timer", empty_return[0][4])
        berth_chain = matching_rules(
            self.military,
            facts=(
                "TRANSPORT-CLEAR-EMPTY-FIND",
                "not (up-set-target-object search-remote c: 0)",
                "building-type-count-total port >= 1",
            ),
            actions=(
                "up-find-local c: port",
                "TRANSPORT-CLEAR-ANCHOR",
            ),
        )
        self.assertEqual(len(berth_chain), 1)
        self.assertNotIn("up-set-timer", berth_chain[0][4])
        quarantine_berth = matching_rules(
            self.military,
            facts=(
                "TRANSPORT-CLEAR-IDLE",
                "t-transport-clear == timer-triggered",
                "gl-quarantine-transport-id c:>= 0",
            ),
            actions=(
                "up-find-local c: port",
                "TRANSPORT-CLEAR-ANCHOR",
            ),
        )
        self.assertEqual(len(quarantine_berth), 1)
        berth = matching_rules(
            self.military,
            facts=("TRANSPORT-CLEAR-EMPTY-FIND",),
            actions=(
                "object-data-map-zone-id gl-transport-clear-water-zone",
                "g:!= gl-transport-clear-water-zone",
                "TRANSPORT-CLEAR-EMPTY-PORT",
            ),
        )
        self.assertEqual(len(berth), 1)
        stage = matching_rules(
            self.military,
            facts=("TRANSPORT-CLEAR-EMPTY-PORT",),
            actions=(
                "object-data-distance < 24",
                "object-data-map-zone-id g:!= gl-transport-clear-water-zone",
                "TRANSPORT-CLEAR-EMPTY-STAGE",
            ),
        )
        self.assertEqual(len(stage), 1)
        self.assertIn("position-object gl-transport-clear-target-x", self.military)
        self.assertNotIn("gl-transport-clear-target-x c:* 4", self.military)
        stale_quarantine = matching_rules(
            self.military,
            facts=(
                "TRANSPORT-CLEAR-STALE-CHECK",
                "gl-transport-clear-attempts c:>= 2",
            ),
            actions=("stale transport quarantined: %d",),
        )
        self.assertEqual(len(stale_quarantine), 1)
        self.assertNotIn("gl-home-anchor-x action-unload", stale_quarantine[0][4])
        detached_retry = matching_rules(
            self.military,
            facts=(
                "TRANSPORT-QUARANTINE-CHECK",
                "object-data-garrison-count > 0",
            ),
            actions=("detached quarantine retry: %d",),
        )
        self.assertEqual(len(detached_retry), 1)
        self.assertIn("position-object point-x", detached_retry[0][4])
        self.assertIn("point-x action-unload", detached_retry[0][4])
        self.assertNotIn("gl-home-anchor-x action-unload", detached_retry[0][4])
        self.assertIn("port hull staged clear: %d", self.military)
        self.assertIn("port hull staging failed: %d", self.military)
        self.assertNotIn("empty transport returned to berth: %d", self.military)
        utility_blocker = matching_rules(
            self.military,
            facts=("TRANSPORT-CLEAR-ANCHOR",),
            actions=(
                "up-find-local c: trade-cog-class",
                "up-find-local c: transport-ship",
                "object-data-idling != 1",
                "object-data-under-attack > 0",
                "object-data-map-zone-id g:!= gl-transport-clear-water-zone",
                "TRANSPORT-CLEAR-UTILITY-CHECK",
            ),
        )
        self.assertEqual(len(utility_blocker), 1)
        self.assertNotIn("object-data-group-flag >= 0", utility_blocker[0][4])
        fallback_blocker = matching_rules(
            self.military,
            facts=(
                "TRANSPORT-CLEAR-UTILITY-CHECK",
                "not (up-set-target-object search-local c: 0)",
            ),
            actions=(
                "up-find-local c: fishing-ship-class",
                "up-find-local c: warship-class",
                "up-find-local c: boarding-ship",
                "object-data-group-flag >= 0",
                "TRANSPORT-CLEAR-DESTINATION",
            ),
        )
        self.assertEqual(len(fallback_blocker), 1)
        verified_move = matching_rules(
            self.military,
            facts=(
                "TRANSPORT-CLEAR-MOVE-CHECK",
                "up-set-target-object search-local c: 0",
            ),
            actions=(
                "port hull staged clear: %d",
                "TRANSPORT-CLEAR-IDLE",
            ),
        )
        self.assertEqual(len(verified_move), 1)

    def test_ally_help_announces_only_after_reachable_dispatch(self) -> None:
        self.assertNotIn("I will send whatever troops I can spare", self.taunts)
        self.assertNotIn("up-find-player enemy find-closest", self.taunts)
        verification = (Path(__file__).resolve().parents[1] / "rawai-attack-verification.per").read_text()
        self.assertIn("up-find-player enemy find-ordered", verification)
        self.assertIn("up-find-next-player enemy find-ordered", verification)
        self.assertIn("up-find-remote c: town-center c: 20", (Path(__file__).resolve().parents[1] / "rawai-home-anchors.per").read_text())
        self.assertNotIn(
            "up-remove-objects search-remote object-data-under-attack <= 0",
            self.taunts,
        )
        self_defense = matching_rules(
            self.taunts,
            facts=(
                "(goal gl-home-defense-state YES)",
                "(taunt-detected any-ally 48)",
            ),
            actions=(
                "(acknowledge-taunt this-any-ally 48)",
                "cannot spare troops while my own town is under attack",
            ),
        )
        self.assertEqual(len(self_defense), 1)
        for player in range(1, 9):
            captures = matching_rules(
                self.taunts,
                facts=(
                    "(goal gl-ally-help-state ALLY-HELP-IDLE)",
                    f"(taunt-detected {player} 48)",
                    f"(stance-toward {player} ally)",
                ),
                actions=(
                    f"(acknowledge-taunt {player} 48)",
                    f"(set-goal gl-ally-help-player {player})",
                    "ALLY-HELP-FIND-ASSET",
                ),
            )
            self.assertEqual(len(captures), 1)

        dispatch = matching_rules(
            self.taunts,
            facts=(
                "(goal gl-ally-help-state ALLY-HELP-OWNERSHIP-COMMAND)",
                "gl-ally-help-responders c:> 0",
                "(up-set-target-object search-remote c: 0)",
            ),
            actions=(
                "(up-target-objects 0 action-default -1 stance-aggressive)",
                "ally relief responders: %d",
                "Reinforcements have been dispatched",
            ),
        )
        self.assertEqual(len(dispatch), 1)
        unavailable = matching_rules(
            self.taunts,
            facts=("(goal gl-ally-help-state ALLY-HELP-DISPATCH)",),
            actions=("no reachable spare troops", "ALLY-HELP-IDLE"),
        )
        self.assertEqual(len(unavailable), 1)

    def test_cross_water_attack_builds_a_safe_scripted_lift(self) -> None:
        blocked_empty_capacity = matching_rules(
            self.economy,
            facts=("(goal gl-land-target-needs-transport YES)",),
            actions=("(set-goal gl-land-transport-ready NO)",),
        )
        reachable_override = matching_rules(
            self.economy,
            facts=("(goal gl-land-target-needs-transport NO)",),
            actions=("(set-goal gl-land-transport-ready YES)",),
        )
        self.assertGreaterEqual(len(blocked_empty_capacity), 1)
        self.assertGreaterEqual(len(reachable_override), 1)

        start = matching_rules(
            self.military,
            facts=(
                "(goal gl-transport-route-state TRANSPORT-ROUTE-ADMISSION-CHECK)",
                "(up-set-target-object search-remote c: 0)",
                "(player-in-game focus-player)",
                "(stance-toward focus-player enemy)",
            ),
            actions=(
                "gl-transport-route-load-player g:= gl-assault-manifest-player",
                "TRANSPORT-ROUTE-MANIFEST-FIND",
            ),
        )
        self.assertEqual(len(start), 1)
        board = matching_rules(
            self.military,
            facts=(
                "TRANSPORT-ROUTE-LOAD-ISSUE",
                "gl-transport-route-load-target c:>= 5",
            ),
            actions=(
                "(up-target-objects 0 action-garrison -1 stance-no-attack)",
                "(set-goal gl-transport-route-script-load YES)",
                "gl-transport-route-load-deadline c:+ 30",
                "attack lift boarding target: %d",
            ),
        )
        manifest = matching_rules(
            self.military,
            facts=("TRANSPORT-ROUTE-MANIFEST-FIND",),
            actions=(
                "gl-transport-route-load-target g:= gl-transport-capacity",
                "gl-transport-route-load-target c:min 10",
                "object-data-index g:>= gl-transport-route-load-target",
                "(up-create-group 0 0 c: attack-boarding-group)",
            ),
        )
        self.assertEqual(len(manifest), 1)
        hull = matching_rules(
            self.military,
            facts=("TRANSPORT-ROUTE-HULL-FIND",),
            actions=(
                "(up-set-target-point gl-assault-rendezvous-x)",
                "(up-find-remote c: transport-ship c: 40)",
                "TRANSPORT-ROUTE-LOAD-FIND",
            ),
        )
        self.assertEqual(len(hull), 1)
        rendezvous = matching_rules(
            self.military,
            facts=("TRANSPORT-ROUTE-RENDEZVOUS-START",),
            actions=(
                "gl-assault-rendezvous-until c:+ 120",
                "gl-assault-rendezvous-x action-move",
                "(up-target-objects 0 action-garrison -1 stance-no-attack)",
                "TRANSPORT-ROUTE-RENDEZVOUS-WAIT",
            ),
        )
        self.assertEqual(len(rendezvous), 1)
        rendezvous_local = matching_rules(
            self.military,
            facts=(
                "TRANSPORT-ROUTE-RENDEZVOUS-PASSENGER",
                "object-data-distance <= 12",
            ),
            actions=("str-assault-event c: 24", "TRANSPORT-ROUTE-LOAD-ISSUE"),
        )
        self.assertEqual(len(rendezvous_local), 1)
        rendezvous_timeout = matching_rules(
            self.military,
            facts=(
                "TRANSPORT-ROUTE-RENDEZVOUS-PASSENGER",
                "object-data-distance > 12",
                "gl-transport-load-clock g:>= gl-assault-rendezvous-until",
            ),
            actions=("str-assault-event c: 25", "TRANSPORT-ROUTE-RECOVERY-WAIT"),
        )
        self.assertEqual(len(rendezvous_timeout), 1)
        for row in matching_rules(self.military, facts=("TRANSPORT-ROUTE-RENDEZVOUS",)):
            self.assertNotIn("gl-transport-route-load-deadline", row[4])
        ready = matching_rules(
            self.military,
            facts=(
                "TRANSPORT-ROUTE-LOAD-CHECK",
                "object-data-garrison-count g:>= gl-transport-route-load-target",
            ),
            actions=("attack lift ready: %d", "TRANSPORT-ROUTE-LOAD-READY"),
        )
        ready_rebuild = matching_rules(
            self.military,
            facts=(
                "TRANSPORT-ROUTE-LOAD-READY",
                "(goal gl-assault-preflight-live YES)",
            ),
            actions=(
                "(set-strategic-number sn-focus-player-number my-player-number)",
                "up-add-object-by-id search-remote g: gl-transport-route-id",
                "TRANSPORT-ROUTE-FIND",
            ),
        )
        partial_terminal = matching_rules(
            self.military,
            facts=(
                "TRANSPORT-ROUTE-LOAD-CHECK",
                "object-data-garrison-count >= 5",
                "object-data-garrison-count g:< gl-transport-route-load-target",
                "gl-transport-load-clock g:>= gl-transport-route-load-deadline",
            ),
            actions=(
                "object-data-garrison-count gl-transport-route-load-observed",
                "TRANSPORT-LOAD-TERMINAL-PARTIAL",
                "RAW44B attack load partial hull: %d",
                "TRANSPORT-ROUTE-LOAD-DIAG-FIND",
            ),
        )
        low_terminal = matching_rules(
            self.military,
            facts=(
                "TRANSPORT-ROUTE-LOAD-CHECK",
                "object-data-garrison-count < 5",
                "gl-transport-load-clock g:>= gl-transport-route-load-deadline",
            ),
            actions=(
                "TRANSPORT-LOAD-TERMINAL-ABORT",
                "RAW44B attack load abort hull: %d",
                "TRANSPORT-ROUTE-LOAD-DIAG-FIND",
            ),
        )
        diagnose = matching_rules(
            self.military,
            facts=("TRANSPORT-ROUTE-LOAD-DIAG-PASSENGER",),
            actions=(
                "object-data-id gl-transport-route-load-candidate-id",
                "object-data-action gl-transport-route-load-candidate-action",
                "object-data-target-id gl-transport-route-load-candidate-target-id",
                "object-data-order gl-transport-route-load-candidate-order",
                "object-data-cmdid gl-transport-route-load-candidate-cmdid",
                "object-data-distance gl-transport-route-load-candidate-distance",
                "object-data-map-zone-id gl-transport-route-load-candidate-zone",
                "object-data-group-flag gl-transport-route-load-candidate-group-flag",
                "object-data-move-x gl-transport-route-load-candidate-move-x",
                "object-data-move-y gl-transport-route-load-candidate-move-y",
                "object-data-idling gl-transport-route-load-candidate-idling",
                "RAW44B attack candidate id: %d",
            ),
        )
        early_sample = matching_rules(
            self.military,
            facts=(
                "TRANSPORT-ROUTE-LOAD-CHECK",
                "gl-transport-route-load-reported NO",
                "gl-transport-load-clock g:>= gl-transport-route-load-next",
            ),
            actions=(
                "object-data-garrison-count gl-transport-route-load-observed",
                "TRANSPORT-LOAD-TERMINAL-NONE",
                "TRANSPORT-ROUTE-LOAD-DIAG-FIND",
            ),
        )
        diagnostic_retry = matching_rules(
            self.military,
            facts=(
                "TRANSPORT-ROUTE-LOAD-DIAG-APPLY",
                "TRANSPORT-LOAD-TERMINAL-NONE",
            ),
            actions=(
                "(up-target-objects 0 action-garrison -1 stance-no-attack)",
                "(set-goal gl-transport-route-load-reported YES)",
                "TRANSPORT-ROUTE-LOAD-WAIT",
            ),
        )
        partial_snapshot = matching_rules(
            self.military,
            facts=(
                "TRANSPORT-ROUTE-LOAD-DIAG-APPLY",
                "TRANSPORT-LOAD-TERMINAL-PARTIAL",
            ),
            actions=(
                "(fe-filter-garrisoned c: 1)",
                "(up-set-group search-local c: attack-boarding-group)",
                "object-data-garrisoned == 1",
                "position-self-x action-stop",
                "object-data-garrisoned != 1",
                "TRANSPORT-ROUTE-LOAD-PARTIAL-MANIFEST",
            ),
        )
        partial_departure = matching_rules(
            self.military,
            facts=("TRANSPORT-ROUTE-LOAD-PARTIAL-MANIFEST",),
            actions=(
                "(up-reset-group c: attack-boarding-group)",
                "(up-create-group 0 0 c: attack-boarding-group)",
                "gl-transport-route-load-target g:= gl-transport-route-load-observed",
                "RAW44B attack partial departure: %d",
                "TRANSPORT-ROUTE-LOAD-READY",
            ),
        )
        abort = matching_rules(
            self.military,
            facts=(
                "TRANSPORT-ROUTE-LOAD-DIAG-APPLY",
                "TRANSPORT-LOAD-TERMINAL-ABORT",
            ),
            actions=("attack lift boarding aborted: %d", "TRANSPORT-ROUTE-RECOVERY-WAIT"),
        )
        mission_text = (Path(__file__).resolve().parents[1] / 'rawai-assault-missions.per').read_text(encoding='utf-8')
        landed = matching_rules(mission_text, facts=('(goal gl-am1-state 2)', 'gl-am1-cargo c:<= 0'),
                               actions=('(set-goal gl-am1-state 14)',))
        landed_handoff = matching_rules(mission_text, facts=('(goal gl-am1-state 14)',),
                                        actions=('gl-am1-target-x action-default',
                                                 '(set-goal gl-am1-state 6)'))
        self.assertEqual(len(landed_handoff), 1)
        self.assertEqual(len(board), 1)
        self.assertEqual(len(ready), 1)
        self.assertEqual(len(ready_rebuild), 1)
        self.assertEqual(len(partial_terminal), 1)
        self.assertEqual(len(low_terminal), 1)
        self.assertEqual(len(diagnose), 1)
        self.assertEqual(len(early_sample), 1)
        self.assertEqual(len(diagnostic_retry), 1)
        self.assertNotIn("TRANSPORT-ROUTE-LOAD-DIAG-PATH", self.military)
        self.assertNotIn(
            "up-path-distance gl-transport-route-origin-x",
            self.military,
        )
        self.assertEqual(len(partial_snapshot), 1)
        self.assertEqual(len(partial_departure), 1)
        self.assertEqual(len(abort), 1)
        self.assertEqual(len(landed), 1)
        invalidated = matching_rules(
            self.military,
            facts=(
                "TRANSPORT-ROUTE-LOAD-READY",
                "(goal gl-assault-preflight-live NO)",
            ),
            actions=(
                "TRANSPORT-ROUTE-RECOVERY-WAIT",
            ),
        )
        self.assertEqual(len(invalidated), 1)
        defense_interrupt = matching_rules(
            self.military,
            facts=(
                "(goal gl-home-defense-state YES)",
                "TRANSPORT-ROUTE-LOAD-DIAG-FIND",
                "TRANSPORT-ROUTE-LOAD-PARTIAL-MANIFEST",
            ),
            actions=(
                "gl-transport-route-origin-x action-unload",
                "TRANSPORT-ROUTE-RECOVERY-WAIT",
            ),
        )
        self.assertEqual(len(defense_interrupt), 0) # central severe policy only
        self.assertFalse(
            matching_rules(
                self.military,
                facts=(
                    "(goal gl-transport-route-state TRANSPORT-ROUTE-IDLE)",
                    "(goal gl-transport-route-script-load YES)",
                ),
            )
        )
        lost_terminals = matching_rules(
            self.military,
            facts=("not (up-set-target-object search-local c: 0)",),
            actions=(
                "(up-reset-group c: attack-boarding-group)",
                "(up-reset-group c: attack-transport-group)",
                "(set-goal gl-transport-route-script-load NO)",
                "(set-goal gl-transport-route-state TRANSPORT-ROUTE-IDLE)",
            ),
        )
        self.assertGreaterEqual(len(lost_terminals), 1)
        for i in range(1, 4):
            self.assertIn(f"(set-goal gl-am{i}-reason 6)", mission_text)

    def test_recall_caller_trace_covers_every_existing_global_recall(self) -> None:
        military_rules = matching_rules(historical_source('rawai-military.per'), actions=("(up-retreat-now)",))
        taunt_rules = matching_rules(historical_source('rawai-tauntcommands.per'), actions=("(up-retreat-now)",))
        self.assertEqual(len(military_rules), 5)
        self.assertEqual(len(taunt_rules), 1)
        for source, rule in enumerate(military_rules + taunt_rules, 1):
            actions = rule[4]
            tag = f'(up-chat-data-to-all "RAW44O recall source: %d" c: {source})'
            self.assertEqual(actions.count(tag), 1)
            self.assertLess(actions.index(tag), actions.index("(up-reset-attack-now)"))
            self.assertLess(actions.index(tag), actions.index("(up-retreat-now)"))
            if "(up-reset-unit" in actions:
                self.assertLess(actions.index(tag), actions.index("(up-reset-unit"))
            for goal in ("gl-transport-route-state", "gl-transport-route-id",
                         "gl-island-migration-state", "gl-island-migration-transport-id"):
                self.assertRegex(actions, rf'up-chat-data-to-all "RAW44O[^\n]+g: {goal}\)')
        self.assertEqual(historical_source('rawai-military.per').count('"RAW44O '), 25)
        self.assertEqual(historical_source('rawai-tauntcommands.per').count('"RAW44O '), 5)

    def test_recall_diagnostic_preserves_every_t7_executable_rule(self) -> None:
        # T7 e17a4ed fingerprints, excluding comments and string contents.
        # T9 adds terminal-only observers, separately checked below to forbid
        # searches, commands, or controller writes. Strip those and additive
        # logs only: the complete original program must still match T7.
        for source, expected in (
            (historical_source('rawai-military.per'), "5983e05d67f97430a5b567ad37b2c498b5091eaa638e79492bf78897de000546"),
            (historical_source('rawai-tauntcommands.per'), "8f3b3e3e92a87b94a706c4d380d8056b4f8f0d0bd868811e821d5d8f1d45c447"),
        ):
            source = re.sub(r'; P3B44T9 OBSERVER BEGIN.*?; P3B44T9 OBSERVER END',
                            '', source, flags=re.S)
            retained = [line for line in source.splitlines() if not re.match(
                r'\s*\(up-chat-data-to-all "(?:RAW44O recall |RAW44C )', line)]
            normalized = " ".join(" ".join(code_without_comments_or_strings(line)
                                          for line in retained).split())
            self.assertEqual(hashlib.sha256(normalized.encode()).hexdigest(), expected)

    def test_congestion_observers_are_terminal_only_and_do_not_mutate_search(self) -> None:
        blocks = re.findall(r'; P3B44T9 OBSERVER BEGIN(.*?); P3B44T9 OBSERVER END',
                            self.military, flags=re.S)
        self.assertEqual(len(blocks), 2)
        for phase, block in enumerate(blocks, 1):
            rules = matching_rules(block)
            self.assertEqual(len(rules), 1)
            facts, actions = rules[0][3:5]
            self.assertIn('(up-set-target-object search-local c: 0)', facts)
            self.assertIn('gl-island-migration-route-waits c:>= 4', facts)
            terminal = matching_rules(self.military, facts=(facts.strip(),),
                                     actions=('(set-goal gl-island-migration-state ',))
            self.assertEqual(len(terminal), 1)
            # This diagnostic leaves the identical terminal enabled, so there
            # is one sample per failed leg, not a new sweep/timer loop.
            for command, operands in re.findall(r'\(([\w-]+) ([^()]*)\)', actions):
                if command == 'up-chat-data-to-all':
                    self.assertTrue(operands.startswith('"RAW44C '))
                elif command == 'up-get-point':
                    self.assertEqual(operands, 'position-object gl-transport-observed-x')
                elif command == 'up-get-object-data':
                    field, destination = operands.split()
                    self.assertIn(field, {'object-data-distance', 'object-data-garrison-count',
                                          'object-data-idling', 'object-data-group-flag'})
                    self.assertEqual(destination, 'gl-transport-observed-value')
                else:
                    self.fail(f'Non-observational command: {command} {operands}')
            self.assertIn(f'"RAW44C migration terminal phase: %d" c: {phase}', actions)
            if phase == 1:
                self.assertIn('object-data-distance g:>= gl-island-migration-route-distance', facts)
                self.assertIn('RAW44C migration current distance:', actions)
            else:
                self.assertNotIn('object-data-distance', block)
                self.assertNotIn('RAW44C migration best distance:', actions)

    def test_assault_hold_reasons_and_ready_identity_are_public_and_bounded(self) -> None:
        fallback = (Path(__file__).resolve().parents[1] / 'rawai-assault-screen-fallback.per').read_text(encoding='utf-8-sig')
        reasons = matching_rules(self.military + '\n' + fallback,
                                 actions=('"RAW44C assault hold reason:',))
        direct = {int(m[1]) for r in reasons
                  if (m := re.search(r'hold reason: %d" c: (\d+)', r[4]))}
        soft = {int(m[1]) for r in matching_rules(self.military)
                if (m := re.search(r'set-goal gl-assault-fallback-reason (\d+)', r[4]))}
        self.assertEqual(direct | soft, {3,5,9,13,14})
        # T19 hard screening failures retain the load and veto the candidate;
        # the removed two-candidate reason1 is replaced by bounded plan search.
        hard={int(m[1]) for r in matching_rules(self.military)
              if (m:=re.search(r'set-goal gl-ap-failure (\d+)',r[4]))}
        self.assertEqual(hard,{2,4,6,7,8,10,11})
        self.assertEqual(soft, {3, 5, 9})
        deferred = [r for r in reasons if 'hold reason: %d" g: gl-assault-fallback-reason' in r[4]]
        self.assertEqual(len(deferred), 1)
        self.assertIn('TRANSPORT-ROUTE-UNSCREENED-DENY', deferred[0][3])
        for rule in reasons:
            self.assertIn('"RAW44C assault hold hull: %d" g: gl-transport-route-id', rule[4])
            self.assertIn('(set-goal gl-transport-route-state ', rule[4])
        ready = matching_rules(self.military, actions=('"RAW44C assault ready hull:',))
        self.assertEqual(len(ready), 1)
        self.assertIn('object-data-garrison-count g:>= gl-transport-route-load-target', ready[0][3])
        self.assertIn('TRANSPORT-ROUTE-LOAD-READY', ready[0][4])

    def test_congestion_scratch_has_private_consecutive_point_goals(self) -> None:
        root = Path(__file__).resolve().parents[1]
        constants = (root / 'rawai-customconstants.per').read_text(encoding='utf-8-sig')
        for name, number in (('x', 1163), ('y', 1164), ('value', 1165)):
            self.assertIn(f'(defconst gl-transport-observed-{name} {number})', constants)
            self.assertIn(f'(set-goal gl-transport-observed-{name} 0)', self.init_goals)
        # Scratch may be written only by the observational primitives above;
        # it must not become a mission condition or command destination.
        for rule in matching_rules(self.military):
            self.assertNotIn('gl-transport-observed-', rule[3])
            for line in rule[4].splitlines():
                if 'gl-transport-observed-' in line:
                    self.assertRegex(line, r'^\s*\(up-(chat-data-to-all|get-point|get-object-data) ')

    def test_transport_departure_moving_normally_resets_stall_without_clearance(self) -> None:
        from test_assault_missions import AssaultMissionTests
        AssaultMissionTests().test_moving_hulls_do_not_receive_repeated_orders()
        self.assertIn('(up-chat-data-to-all "RAWAI-P3B44T50: %d" c: 498)', self.init_goals)

    def test_transport_departure_stalled_near_origin_activates_clearance(self) -> None:
        from test_assault_missions import AssaultMissionTests
        AssaultMissionTests().test_only_free_idle_blocker_yields_to_stalled_mission()

    def test_transport_departure_blocker_selection_preserves_owned_or_unsafe_hulls(self) -> None:
        text = (Path(__file__).resolve().parents[1] / 'rawai-assault-missions.per').read_text(encoding='utf-8')
        for i in range(1, 4):
            rows = matching_rules(text, facts=(f'(goal gl-am{i}-sample 2)',), actions=('up-find-local c: transport-ship c: 20',))
            self.assertEqual(len(rows), 1)
            for guard in ('object-data-group-flag >= 0', 'object-data-garrison-count > 0', 'object-data-idling != 1',
                          'object-data-under-attack > 0', 'orderid-transport', 'orderid-unload', 'object-data-map-zone-id g:!=', 'object-data-index > 0'):
                self.assertIn(guard, rows[0][4])

    def test_transport_departure_clearance_success_resumes_original_waypoint(self) -> None:
        from test_assault_missions import AssaultMissionTests
        AssaultMissionTests().test_only_free_idle_blocker_yields_to_stalled_mission()

    def test_transport_departure_clearance_verifies_one_exact_blocker(self) -> None:
        from test_assault_missions import AssaultMissionTests
        AssaultMissionTests().test_only_free_idle_blocker_yields_to_stalled_mission()

    def test_transport_departure_clearance_failure_is_terminal_and_bounded(self) -> None:
        from test_assault_missions import AssaultMissionTests
        AssaultMissionTests().test_no_progress_recovers_then_quarantines_without_command_loop()

    def test_transport_landing_stages_screen_and_escort_and_blocks_guard_refresh(self) -> None:
        from test_assault_missions import AssaultMissionTests
        AssaultMissionTests().test_landing_stages_only_its_screen_and_paired_escorts()
        for i in range(1, 4): self.assertIn(f'(not (goal gl-am{i}-state 2))', self.military)

    def test_port_clearance_includes_trade_cogs(self) -> None:
        berth_scans = matching_rules(
            self.military,
            facts=("TRANSPORT-CLEAR-ANCHOR",),
            actions=("(up-find-local c: trade-cog-class c: 10)",),
        )
        destination_scans = matching_rules(
            self.military,
            facts=("TRANSPORT-CLEAR-DESTINATION",),
            actions=("(up-find-local c: trade-cog-class c: 10)",),
        )
        self.assertEqual(len(berth_scans), 1)
        self.assertEqual(len(destination_scans), 1)

    def test_simultaneous_naval_dispatch_preserves_land_retry(self) -> None:
        collision = matching_rules(
            self.military,
            facts=(
                "(up-timer-status t-land-attack == timer-triggered)",
                "(up-timer-status t-naval-attack == timer-triggered)",
            ),
            actions=(
                "(up-set-timer c: t-land-attack c: 20)",
                "ATTACK-DISPATCH-NAVAL",
            ),
        )
        self.assertEqual(len(collision), 1)

    def test_unreachable_or_routine_threat_cannot_latch_severe_defense(self) -> None:
        self.assertNotIn("(set-goal gl-home-defense-state YES)", self.military)
        severe = (Path(__file__).resolve().parents[1] / "rawai-severe-defense.per").read_text()
        latches = matching_rules(severe, actions=("(set-goal gl-home-defense-state YES)",))
        self.assertEqual(len(latches), 8)
        for row in latches:
            self.assertIn("gl-owner-severe-count c:>= 8", row[3])
            self.assertIn("enemy)", row[3])
        self.assertIn("object-data-map-zone-id g:!= gl-home-zone", severe)
        self.assertIn("(up-filter-distance c: -1 c: 24)", severe)

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
