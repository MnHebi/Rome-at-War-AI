#!/usr/bin/env python3
"""Regression tests for the economy-first optional Codex agent toolbox."""

from __future__ import annotations

import importlib.util
import json
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENT_DIR = ROOT / ".codex" / "agents"
MODULE_PATH = ROOT / "tools" / "context_pack.py"
SPEC = importlib.util.spec_from_file_location("context_pack", MODULE_PATH)
assert SPEC and SPEC.loader
context_pack = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(context_pack)


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

    def test_metadata_and_agent_files_are_valid(self) -> None:
        self.assertEqual(context_pack.validate_metadata(), [])

    def test_suite_has_four_optional_capabilities_and_no_duplicate_worker(self) -> None:
        self.assertEqual(
            set(self.agents),
            {"economy_scout", "economy_analyst", "economy_planner", "economy_verifier"},
        )
        self.assertTrue(self.routing["general_worker"]["default"])
        self.assertEqual(
            self.routing["general_worker"]["implementation"],
            "current primary Codex agent; worker in topology means this agent, not a spawn",
        )

    def test_optional_agents_are_small_read_only_non_recursive_capabilities(self) -> None:
        for stem, agent in self.agents.items():
            self.assertEqual(agent["name"], stem)
            self.assertEqual(agent["sandbox_mode"], "read-only")
            self.assertIn("Do not", agent["description"])
            self.assertIn("spawn another agent", agent["developer_instructions"])
            for marker in ("RESULT:", "EVIDENCE:", "ACTION:", "UNCERTAINTY:"):
                self.assertIn(marker, agent["developer_instructions"])
            self.assertLess((AGENT_DIR / f"{stem}.toml").stat().st_size, 2_000)

    def test_only_scout_pins_a_lightweight_model(self) -> None:
        scout = self.agents["economy_scout"]
        self.assertEqual(scout["model"], "gpt-5.6-luna")
        self.assertEqual(scout["model_reasoning_effort"], "low")
        for name in ("economy_analyst", "economy_planner", "economy_verifier"):
            self.assertNotIn("model", self.agents[name])
            self.assertEqual(self.agents[name]["model_reasoning_effort"],
                             "medium" if name == "economy_planner" else "high")

    def test_trivial_bug_and_docs_routes_are_worker_only(self) -> None:
        by_class = {item["id"]: item for item in self.routing["task_classes"]}
        for class_id in ("trivial-edit", "localized-bug-fix", "documentation"):
            self.assertEqual(by_class[class_id]["topology"], ["worker"])
            self.assertEqual(by_class[class_id]["conditional"], [])
            route = context_pack.render_route(class_id)
            self.assertIn("Complete with the worker and stop", route)
            self.assertNotIn("worker -> economy_", route)

    def test_capabilities_are_conditional_including_high_assurance(self) -> None:
        optional = {item["id"] for item in self.routing["capabilities"]}
        for task_class in self.routing["task_classes"]:
            self.assertTrue(optional.isdisjoint(task_class["topology"]))
        review=context_pack.render_route("high-assurance-review")
        self.assertIn("independent-agent review is explicitly requested", review)
        self.assertIn("concrete acceptance risk", review)

    def test_planning_requests_do_not_automatically_delegate(self) -> None:
        route=context_pack.render_route("project-planning")
        self.assertIn("Default topology: `worker`", route)
        self.assertIn("not a new subagent", route)
        self.assertIn("separate planner is explicitly requested", route)
        planner=next(x for x in self.routing['capabilities'] if x['id']=='economy_planner')
        self.assertNotIn("user explicitly asks for planning or design", planner['invoke_when'])
        self.assertIn("A request for a plan alone is not a delegation trigger", self.agents['economy_planner']['description'])

    def test_specialists_leave_shared_state_to_primary(self) -> None:
        for agent in self.agents.values():
            self.assertIn("shared",agent['developer_instructions'])
        verifier=self.agents['economy_verifier']['developer_instructions']
        self.assertIn("dependencies",verifier)
        self.assertIn("specific acceptance risk",verifier)

    def test_representative_escalation_is_specific_and_sequential(self) -> None:
        unfamiliar = context_pack.render_route("unfamiliar-code-investigation")
        self.assertIn("Default topology: `worker`", unfamiliar)
        self.assertIn("economy_scout only if targeted search is insufficient", unfamiliar)
        architecture = context_pack.render_route("architectural-change", "high-assurance")
        self.assertIn("economy_planner when planning saves rework", architecture)
        self.assertIn("may add one verifier after mechanical checks", architecture)
        self.assertEqual(self.routing["nested_delegation"]["maximum_depth"], 1)
        self.assertEqual(self.routing["nested_delegation"]["default"], "forbidden")

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
        self.assertEqual(config['model'], 'gpt-6-astra')
        self.assertEqual(config['model_reasoning_effort'], 'medium')
        self.assertNotIn('service_tier', config)
        self.assertNotIn('default_subagent_model', config['agents'])


if __name__ == "__main__":
    unittest.main()
