#!/usr/bin/env python3
"""Regression tests for the economy-first optional Codex agent toolbox."""

from __future__ import annotations

import json
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENT_DIR = ROOT / ".codex" / "agents"


class AgentRoutingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.routing = json.loads(
            (ROOT / "context" / "agent-routing.json").read_text(encoding="utf-8")
        )
        cls.agents = {
            path.stem: tomllib.loads(path.read_text(encoding="utf-8"))
            for path in AGENT_DIR.glob("*.toml")
        }

    def test_suite_has_four_optional_capabilities_and_no_duplicate_worker(self) -> None:
        self.assertEqual(
            set(self.agents),
            {"economy_scout", "economy_analyst", "economy_planner", "economy_verifier"},
        )
        self.assertTrue(self.routing["general_worker"]["default"])
        self.assertEqual(
            {item["id"] for item in self.routing["capabilities"]}, set(self.agents)
        )
        self.assertEqual(self.routing["nested_delegation"]["maximum_depth"], 1)
        self.assertEqual(self.routing["nested_delegation"]["default"], "forbidden")

    def test_optional_agents_are_small_read_only_non_recursive_capabilities(self) -> None:
        for stem, agent in self.agents.items():
            self.assertEqual(agent["name"], stem)
            self.assertEqual(agent["sandbox_mode"], "read-only")
            self.assertIn("spawn another agent", agent["developer_instructions"])
            for marker in ("RESULT:", "EVIDENCE:", "ACTION:", "UNCERTAINTY:"):
                self.assertIn(marker, agent["developer_instructions"])
            self.assertLess((AGENT_DIR / f"{stem}.toml").stat().st_size, 2_000)

    def test_trivial_bug_and_docs_routes_are_worker_only(self) -> None:
        by_class = {item["id"]: item for item in self.routing["task_classes"]}
        for class_id in ("trivial-edit", "localized-bug-fix", "documentation"):
            self.assertEqual(by_class[class_id]["topology"], ["worker"])
            self.assertEqual(by_class[class_id]["conditional"], [])

    def test_capabilities_are_conditional_including_high_assurance(self) -> None:
        optional = {item["id"] for item in self.routing["capabilities"]}
        for task_class in self.routing["task_classes"]:
            self.assertTrue(optional.isdisjoint(task_class["topology"]))
        topology = {item["id"]: item["topology"] for item in self.routing["task_classes"]}
        self.assertEqual(topology["high-assurance-review"][:1], ["worker"])

    def test_planning_requests_do_not_automatically_delegate(self) -> None:
        by_class = {item["id"]: item for item in self.routing["task_classes"]}
        self.assertEqual(by_class["project-planning"]["topology"], ["worker"])
        planner = next(x for x in self.routing["capabilities"] if x["id"] == "economy_planner")
        self.assertNotIn("user explicitly asks for planning or design", planner['invoke_when'])
        self.assertTrue(any(
            "plan is requested" in item for item in planner["do_not_invoke_when"]))

    def test_task_capsule_and_result_contract_are_compact_and_stable(self) -> None:
        template = json.loads(
            (ROOT / "context" / "task-capsule-template.json").read_text(encoding="utf-8")
        )
        self.assertEqual(list(template), self.routing["task_capsule_fields"])
        self.assertEqual(
            self.routing["output_contract"],
            ["RESULT", "EVIDENCE", "ACTION", "UNCERTAINTY"],
        )
        self.assertLess(
            (ROOT / "context" / "task-capsule-template.json").stat().st_size,
            1_500,
        )

    def test_project_config_limits_default_fanout_without_disabling_user_control(self) -> None:
        config = tomllib.loads((ROOT / ".codex" / "config.toml").read_text(encoding="utf-8"))
        self.assertEqual(config["agents"]["max_concurrent_threads_per_session"], 2)
        self.assertNotIn('service_tier', config)
        self.assertNotIn('default_subagent_model', config['agents'])


if __name__ == "__main__":
    unittest.main()
