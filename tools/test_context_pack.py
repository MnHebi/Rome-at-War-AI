#!/usr/bin/env python3
"""Regression tests for bounded agent context assembly."""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "context_pack.py"
SPEC = importlib.util.spec_from_file_location("context_pack", MODULE_PATH)
assert SPEC and SPEC.loader
context_pack = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(context_pack)


class ContextMetadataTests(unittest.TestCase):
    def test_metadata_and_references_are_valid(self) -> None:
        self.assertEqual(context_pack.validate_metadata(), [])

    def test_hot_context_has_a_guarded_size(self) -> None:
        hot = [
            ROOT / "AGENTS.md",
            ROOT / "HANDOFF.md",
            ROOT / "context" / "project-state.json",
        ]
        total = sum(path.stat().st_size for path in hot)
        self.assertLess(total, 30_000, f"hot context grew to {total} bytes")

    def test_handoff_identity_matches_structured_current_state(self) -> None:
        state = json.loads(
            (ROOT / "context" / "project-state.json").read_text(encoding="utf-8")
        )
        handoff = (ROOT / "HANDOFF.md").read_text(encoding="utf-8")
        repository = state["repository"]
        for key in (
            "canonical_workspace",
            "branch",
            "runtime_source_commit",
            "runtime_marker",
            "runtime_sha256",
        ):
            self.assertIn(str(repository[key]), handoff, f"handoff omits {key}")
        self.assertIn(state["current_task"], handoff)
        self.assertLessEqual(len(handoff.splitlines()), 120)

    def test_cold_context_is_excluded_from_broad_ripgrep_by_default(self) -> None:
        ignore = (ROOT / ".ignore").read_text(encoding="utf-8").splitlines()
        self.assertIn("context/archive/", ignore)
        self.assertIn("OWNERSHIP-SOURCE-INVENTORY.md", ignore)
        self.assertIn("writer-trace-sites.json", ignore)
        self.assertIn("replay-benchmarks.json", ignore)

    def test_narrow_shipyard_packet_is_bounded_and_selective(self) -> None:
        packet = context_pack.render_context("subsystem.shipyard", "implementer")
        self.assertLess(len(packet.encode("utf-8")), 12_000)
        self.assertIn("shipyard.sampler.t51", packet)
        self.assertIn("tools/generate_shipyard_placement.py", packet)
        self.assertNotIn("migration.productive-dropsite", packet)
        self.assertNotIn("RAWAI-P3B44T10R4:455", packet)

    def test_task_packet_preserves_order_and_runtime_boundary(self) -> None:
        packet = context_pack.render_context("task.t52-runtime", "runtime-analyst")
        positions = [
            packet.index("Shipyard recovery"),
            packet.index("first Villager order-706 onset"),
            packet.index("assault preparation aborts"),
            packet.index("migration drop-site productivity"),
            packet.index("Merchant right-of-way real-choke exercise"),
            packet.index("expeditionary commitment reassessment"),
        ]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("Telemetry presence alone does not close", packet)
        self.assertIn("RAWAI-P3B44T52:500", packet)

    def test_role_packet_excludes_full_history_by_policy(self) -> None:
        packet = context_pack.render_context("subsystem.assault-transport", "reviewer")
        self.assertIn("Role: reviewer", packet)
        self.assertIn("all prior project narrative", packet)
        self.assertNotIn("P3B44T10R4", packet)
        self.assertNotIn("C7554880AC95FE2", packet)

    def test_all_task_capsules_match_their_nodes(self) -> None:
        graph = json.loads((ROOT / "context" / "nodes.json").read_text(encoding="utf-8"))
        capsules = [node for node in graph["nodes"] if "capsule" in node]
        self.assertGreaterEqual(len(capsules), 1)
        for node in capsules:
            capsule = json.loads((ROOT / node["capsule"]).read_text(encoding="utf-8"))
            self.assertEqual(capsule["id"], node["id"])

    def test_unknown_node_fails_closed(self) -> None:
        with self.assertRaises(context_pack.ContextError):
            context_pack.render_context("subsystem.not-real")


if __name__ == "__main__":
    unittest.main()
