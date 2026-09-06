"""Focused T53 audit, episode diagnostics and replay-correlation tests."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from audit_task_ownership import economic_retask_correlation  # noqa: E402


def diag_pair(player: int, code: int, value: int, sequence: int, milliseconds: int):
    return [
        {"action": "CHAT", "player": player, "message": f"RAW12 diag id: {code}",
         "sequence": sequence, "milliseconds": milliseconds},
        {"action": "CHAT", "player": player, "message": f"RAW12 diag value: {value}",
         "sequence": sequence + 1, "milliseconds": milliseconds},
    ]


class EconomicRetaskDiagnosticsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.home = (ROOT / "rawai-homebase.per").read_text(encoding="utf-8-sig")
        self.constants = (ROOT / "rawai-customconstants.per").read_text(
            encoding="utf-8-sig"
        )
        self.init = (ROOT / "rawai-init-goals.per").read_text(encoding="utf-8-sig")

    def test_reference_audit_precedes_and_bounds_the_experiment(self) -> None:
        audit = (ROOT / "T53-VILLAGER-KEYSTATES-AUDIT.md").read_text(encoding="utf-8")
        self.assertIn("SHA-256", audit)
        for category in (
            "ECONOMIC RESOURCE ASSIGNMENT", "ECONOMIC BUILD/REPAIR",
            "TRANSPORT/GARRISON", "MOVEMENT", "DEFENSE/COMBAT",
            "STOP/RELEASE", "OTHER",
        ):
            self.assertIn(category, audit)
        self.assertIn("MIGRATION-ASSIGN-RETASK-ANCHOR", audit)
        self.assertIn("audited Phase B candidates", audit)

    def test_diagnostic_class_rearms_instead_of_expiring(self) -> None:
        self.assertIn("(defconst gl-econ-retask-diag-armed 15816)", self.constants)
        self.assertNotIn("gl-econ-retask-diag-left", self.constants)
        self.assertIn("(set-goal gl-econ-retask-diag-armed YES)", self.init)
        self.assertIn("(up-modify-goal gl-econ-retask-diag-next c:+ 300)", self.home)
        self.assertIn("(goal gl-econ-retask-diag-armed NO)", self.home)
        self.assertIn("(set-goal gl-econ-retask-diag-armed YES)", self.home)

    def test_only_actual_farm_retask_states_can_consume_the_latch(self) -> None:
        consume = "(set-goal gl-econ-retask-diag-armed NO)"
        self.assertEqual(self.home.count(consume), 4)
        for name in (
            "rawai-military.per", "rawai-hunt.per", "rawai-general.per",
            "rawai-economy.per", "rawai-exploration-policy.per",
        ):
            self.assertNotIn("gl-econ-retask-diag-armed", (
                ROOT / name
            ).read_text(encoding="utf-8-sig"), name)

    def test_pre_and_delayed_actor_fields_are_replay_visible(self) -> None:
        for code in range(640, 658):
            self.assertIn(f"str-t12-diag-id c: {code}", self.home, code)
        self.assertIn("object-data-carry gl-econ-retask-diag-carry", self.home)
        self.assertIn("object-data-type gl-econ-retask-diag-target-type", self.home)
        self.assertIn("object-data-class gl-econ-retask-diag-target-class", self.home)
        self.assertIn("object-data-language-id gl-econ-retask-diag-language", self.home)
        self.assertIn("object-data-gather-type gl-econ-retask-diag-gather", self.home)


class EconomicRetaskCorrelationTests(unittest.TestCase):
    def test_actor_level_pre_post_and_later_706_rates(self) -> None:
        events = [
            {"action": "AI_ORDER", "player_id": 2, "object_ids": [42],
             "order_id": 706, "sequence": 1, "milliseconds": 50000},
            {"action": "AI_ORDER", "player_id": 2, "object_ids": [42],
             "order_id": 706, "sequence": 2, "milliseconds": 55000},
        ]
        sequence = 10
        values = {
            640: 1, 641: 42, 642: 10, 643: 90, 644: 11, 645: 1,
            646: 0, 647: 700, 648: 50, 649: 10, 650: 60,
        }
        for code, value in values.items():
            events += diag_pair(2, code, value, sequence, 60000)
            sequence += 2
        events += [
            {"action": "AI_ORDER", "player_id": 2, "object_ids": [42],
             "order_id": 706, "sequence": sequence, "milliseconds": 61000},
            {"action": "AI_ORDER", "player_id": 2, "object_ids": [42],
             "order_id": 706, "sequence": sequence + 1, "milliseconds": 65000},
        ]
        sequence += 2
        for code, value in {
            651: 42, 652: 5, 653: 700, 654: 12, 655: 0, 656: 65, 657: 1,
        }.items():
            events += diag_pair(2, code, value, sequence, 65000)
            sequence += 2
        events += [
            {"action": "AI_ORDER", "player_id": 2, "object_ids": [42],
             "order_id": 706, "sequence": sequence, "milliseconds": 100000},
            {"action": "AI_ORDER", "player_id": 3, "object_ids": [99],
             "order_id": 706, "sequence": sequence + 1, "milliseconds": 100000},
        ]

        report = economic_retask_correlation(events, 30000)
        episode = report["episodes"][0]
        self.assertEqual((episode["player"], episode["actor"], episode["writer"]),
                         (2, 42, 1))
        self.assertEqual(episode["order706"]["pre_count"], 2)
        self.assertEqual(episode["order706"]["post_count"], 2)
        self.assertEqual(episode["order706"]["later_recurrence_count"], 1)
        self.assertTrue(episode["role_transition_observed"])
        self.assertTrue(episode["target_transition_observed"])

    def test_major_unsampled_actor_is_reported(self) -> None:
        events = [
            {"action": "AI_ORDER", "player_id": 4, "object_ids": [88],
             "order_id": 706, "sequence": index, "milliseconds": index * 10}
            for index in range(100)
        ]
        report = economic_retask_correlation(events)
        self.assertEqual(report["major_order706_actors_without_sample"][0]["actor"], 88)


if __name__ == "__main__":
    unittest.main()
