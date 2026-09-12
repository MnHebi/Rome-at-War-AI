#!/usr/bin/env python3
"""Assemble bounded agent context from repository metadata.

The pack contains concise state, dependency summaries and references. It never
concatenates source, reports, archives or generated evidence.
"""

from __future__ import annotations

import argparse
import json
import sys
import tomllib
from collections import deque
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
CONTEXT = ROOT / "context"
STATE_FILE = CONTEXT / "project-state.json"
NODES_FILE = CONTEXT / "nodes.json"
ROLES_FILE = CONTEXT / "roles.json"
ROUTING_FILE = CONTEXT / "agent-routing.json"
CAPSULE_TEMPLATE_FILE = CONTEXT / "task-capsule-template.json"
VALID_FINDING_STATUSES = {
    "OPEN",
    "INVESTIGATING",
    "ROOT-CAUSE-PROVEN",
    "FIXED-PENDING-RUNTIME",
    "CLOSED",
    "DEFERRED",
}


class ContextError(RuntimeError):
    """Raised when context metadata cannot produce a trustworthy packet."""


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ContextError(f"cannot read {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(value, dict):
        raise ContextError(f"{path.relative_to(ROOT)} must contain a JSON object")
    return value


def load_metadata() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    return load_json(STATE_FILE), load_json(NODES_FILE), load_json(ROLES_FILE)


def load_routing() -> dict[str, Any]:
    return load_json(ROUTING_FILE)


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _text_list(value: Any) -> bool:
    return isinstance(value, list) and all(_text(item) for item in value)


def _check_paths(owner: str, field: str, values: Any, errors: list[str]) -> None:
    if not _text_list(values):
        errors.append(f"{owner}: {field} must be a list of non-empty paths")
        return
    for value in values:
        path = Path(value)
        if path.is_absolute() or ".." in path.parts:
            errors.append(f"{owner}: {field} path must be repository-relative: {value}")
        elif not (ROOT / path).exists():
            errors.append(f"{owner}: missing {field} path: {value}")


def _validate_agent_routing(
    routing: dict[str, Any], role_ids: set[str], errors: list[str]
) -> None:
    if routing.get("schema_version") != 1:
        errors.append("agent-routing.json: schema_version must be 1")
    if not _text(routing.get("optimization_target")):
        errors.append("agent-routing.json: optimization_target is required")

    modes = routing.get("modes")
    if not isinstance(modes, list) or not modes:
        errors.append("agent-routing.json: modes must be a non-empty list")
        modes = []
    mode_ids = {
        mode.get("id") for mode in modes
        if isinstance(mode, dict) and _text(mode.get("id")) and _text(mode.get("policy"))
    }
    if routing.get("default_mode") not in mode_ids:
        errors.append("agent-routing.json: default_mode must name a valid mode")
    if mode_ids != {"economy", "normal", "high-assurance"}:
        errors.append("agent-routing.json: expected economy, normal and high-assurance modes")

    tiers = routing.get("tiers")
    if not isinstance(tiers, list) or {
        tier.get("id") for tier in tiers if isinstance(tier, dict)
    } != set(range(5)):
        errors.append("agent-routing.json: tiers must be exactly 0 through 4")

    worker = routing.get("general_worker")
    if not isinstance(worker, dict) or worker.get("default") is not True:
        errors.append("agent-routing.json: general_worker must be the default")

    capabilities = routing.get("capabilities")
    if not isinstance(capabilities, list) or not capabilities:
        errors.append("agent-routing.json: capabilities must be a non-empty list")
        capabilities = []
    capability_ids: set[str] = set()
    for index, capability in enumerate(capabilities):
        if not isinstance(capability, dict) or not _text(capability.get("id")):
            errors.append(f"agent-routing capabilities[{index}] requires an id")
            continue
        capability_id = capability["id"]
        if capability_id in capability_ids:
            errors.append(f"duplicate agent capability: {capability_id}")
        capability_ids.add(capability_id)
        if capability.get("context_role") not in role_ids:
            errors.append(f"{capability_id}: unknown context_role")
        for field in ("invoke_when", "do_not_invoke_when"):
            if not _text_list(capability.get(field)) or not capability[field]:
                errors.append(f"{capability_id}: {field} must be a non-empty text list")
        config = capability.get("config")
        if not _text(config):
            errors.append(f"{capability_id}: config is required")
        _check_paths(capability_id, "config", [config] if _text(config) else [], errors)
        if not _text(config) or not (ROOT / config).exists():
            continue
        try:
            agent = tomllib.loads((ROOT / config).read_text(encoding="utf-8"))
        except (OSError, tomllib.TOMLDecodeError) as exc:
            errors.append(f"{config}: invalid TOML: {exc}")
            continue
        for field in ("name", "description", "developer_instructions"):
            if not _text(agent.get(field)):
                errors.append(f"{config}: {field} is required")
        if agent.get("name") != capability_id:
            errors.append(f"{config}: name must match capability id {capability_id}")
        if agent.get("sandbox_mode") != "read-only":
            errors.append(f"{config}: optional capabilities must be read-only")
        instructions = agent.get("developer_instructions", "")
        for marker in ("RESULT:", "EVIDENCE:", "ACTION:", "UNCERTAINTY:"):
            if marker not in instructions:
                errors.append(f"{config}: output contract omits {marker}")
        if "spawn another agent" not in instructions:
            errors.append(f"{config}: nested delegation is not explicitly forbidden")
        if (ROOT / config).stat().st_size >= 2_000:
            errors.append(f"{config}: recurring agent prompt exceeds 2 KB")

    expected_capabilities = {
        "economy_scout", "economy_analyst", "economy_planner", "economy_verifier"
    }
    if capability_ids != expected_capabilities:
        errors.append("agent-routing.json: expected exactly four optional capabilities")

    task_classes = routing.get("task_classes")
    if not isinstance(task_classes, list) or not task_classes:
        errors.append("agent-routing.json: task_classes must be a non-empty list")
        task_classes = []
    expected_classes = {
        "trivial-edit", "localized-bug-fix", "unfamiliar-code-investigation",
        "feature-implementation", "test-failure-diagnosis", "refactor",
        "documentation", "research-analysis", "architectural-change",
        "high-assurance-review", "project-planning", "repository-maintenance",
    }
    class_ids: set[str] = set()
    allowed_topology = capability_ids | {"worker", "tools"}
    for task_class in task_classes:
        if not isinstance(task_class, dict) or not _text(task_class.get("id")):
            errors.append("agent-routing.json: every task class requires an id")
            continue
        class_id = task_class["id"]
        class_ids.add(class_id)
        if task_class.get("default_tier") not in range(5):
            errors.append(f"{class_id}: default_tier must be 0 through 4")
        if not _text_list(task_class.get("topology")) or not task_class["topology"]:
            errors.append(f"{class_id}: topology must be non-empty")
        elif not set(task_class["topology"]).issubset(allowed_topology):
            errors.append(f"{class_id}: topology names an unknown capability")
        if not _text_list(task_class.get("conditional")):
            errors.append(f"{class_id}: conditional must be a text list")
    if class_ids != expected_classes:
        errors.append("agent-routing.json: representative task classes are incomplete")
    by_class = {
        task_class["id"]: task_class for task_class in task_classes
        if isinstance(task_class, dict) and _text(task_class.get("id"))
    }
    for class_id in ("trivial-edit", "localized-bug-fix", "documentation"):
        task_class = by_class.get(class_id, {})
        if task_class.get("topology") != ["worker"] or task_class.get("conditional") != []:
            errors.append(f"{class_id}: must remain worker-only")

    if routing.get("output_contract") != ["RESULT", "EVIDENCE", "ACTION", "UNCERTAINTY"]:
        errors.append("agent-routing.json: compact output contract changed")
    expected_capsule = [
        "objective", "scope", "relevant_context", "known_facts", "constraints",
        "files", "expected_output", "validation", "stop_when",
    ]
    if routing.get("task_capsule_fields") != expected_capsule:
        errors.append("agent-routing.json: task capsule fields changed")
    nesting = routing.get("nested_delegation")
    if not isinstance(nesting, dict) or nesting.get("default") != "forbidden" or nesting.get("maximum_depth") != 1:
        errors.append("agent-routing.json: nested delegation must default to depth one")

    try:
        template = load_json(CAPSULE_TEMPLATE_FILE)
    except ContextError as exc:
        errors.append(str(exc))
        return
    if list(template) != expected_capsule:
        errors.append("task-capsule-template.json: fields/order must match routing metadata")
    for field, value in template.items():
        if not (_text(value) or (_text_list(value) and value)):
            errors.append(f"task-capsule-template.json: {field} must be non-empty")


def validate_metadata() -> list[str]:
    errors: list[str] = []
    try:
        state, graph, roles_doc = load_metadata()
    except ContextError as exc:
        return [str(exc)]

    for name, payload in (
        ("project-state.json", state),
        ("nodes.json", graph),
        ("roles.json", roles_doc),
    ):
        if payload.get("schema_version") != 1:
            errors.append(f"{name}: schema_version must be 1")

    nodes = graph.get("nodes")
    if not isinstance(nodes, list) or not nodes:
        return errors + ["nodes.json: nodes must be a non-empty list"]

    node_by_id: dict[str, dict[str, Any]] = {}
    for index, node in enumerate(nodes):
        if not isinstance(node, dict):
            errors.append(f"nodes[{index}] must be an object")
            continue
        node_id = node.get("id")
        if not _text(node_id):
            errors.append(f"nodes[{index}] requires a non-empty id")
            continue
        if node_id in node_by_id:
            errors.append(f"duplicate node id: {node_id}")
            continue
        node_by_id[node_id] = node
        for field in ("kind", "status", "summary"):
            if not _text(node.get(field)):
                errors.append(f"{node_id}: {field} must be non-empty text")
        for field in ("depends_on", "related_to"):
            if not _text_list(node.get(field)):
                errors.append(f"{node_id}: {field} must be a text list")
        _check_paths(node_id, "authoritative_files", node.get("authoritative_files"), errors)
        _check_paths(node_id, "evidence", node.get("evidence"), errors)
        capsule = node.get("capsule")
        if capsule is not None:
            _check_paths(node_id, "capsule", [capsule], errors)

    for node_id, node in node_by_id.items():
        for field in ("depends_on", "related_to"):
            for target in node.get(field, []):
                if target not in node_by_id:
                    errors.append(f"{node_id}: unknown {field} node: {target}")
                if target == node_id:
                    errors.append(f"{node_id}: self-reference in {field}")

    current_task = state.get("current_task")
    if current_task not in node_by_id:
        errors.append(f"project-state.json: unknown current_task: {current_task}")
    repository = state.get("repository")
    if not isinstance(repository, dict):
        errors.append("project-state.json: repository must be an object")
    else:
        for field in ("canonical_workspace", "branch", "runtime_source_commit",
                      "runtime_marker", "runtime_sha256"):
            if not _text(repository.get(field)):
                errors.append(f"project-state.json: repository.{field} is required")

    findings = state.get("findings")
    finding_ids: set[str] = set()
    if not isinstance(findings, list):
        errors.append("project-state.json: findings must be a list")
        findings = []
    for index, finding in enumerate(findings):
        if not isinstance(finding, dict):
            errors.append(f"findings[{index}] must be an object")
            continue
        finding_id = finding.get("id")
        if not _text(finding_id):
            errors.append(f"findings[{index}] requires a non-empty id")
            continue
        if finding_id in finding_ids:
            errors.append(f"duplicate finding id: {finding_id}")
        finding_ids.add(finding_id)
        if finding.get("status") not in VALID_FINDING_STATUSES:
            errors.append(f"{finding_id}: invalid finding status {finding.get('status')!r}")
        for field in ("claim", "acceptance", "next_action", "reopen_when"):
            if not _text(finding.get(field)):
                errors.append(f"{finding_id}: {field} must be non-empty text")
        if not _text_list(finding.get("related_to")):
            errors.append(f"{finding_id}: related_to must be a non-empty text list")
        else:
            for target in finding["related_to"]:
                if target not in node_by_id:
                    errors.append(f"{finding_id}: unknown related_to node: {target}")
        if not _text_list(finding.get("depends_on")):
            errors.append(f"{finding_id}: depends_on must be a text list")
        _check_paths(finding_id, "evidence", finding.get("evidence"), errors)
        if not _text_list(finding.get("implementation")):
            errors.append(f"{finding_id}: implementation must be a text list")

    for finding in findings:
        if not isinstance(finding, dict):
            continue
        for dependency in finding.get("depends_on", []):
            if dependency not in finding_ids:
                errors.append(f"{finding.get('id')}: unknown finding dependency: {dependency}")

    baseline_failures = state.get("known_baseline_failures")
    if not isinstance(baseline_failures, list):
        errors.append("project-state.json: known_baseline_failures must be a list")
    else:
        for failure in baseline_failures:
            if not isinstance(failure, dict) or not _text(failure.get("id")):
                errors.append("every known baseline failure requires an id")
                continue
            _check_paths(failure["id"], "evidence", failure.get("evidence"), errors)

    roles = roles_doc.get("roles")
    role_ids: set[str] = set()
    if not isinstance(roles, list) or not roles:
        errors.append("roles.json: roles must be a non-empty list")
        roles = []
    for index, role in enumerate(roles):
        if not isinstance(role, dict) or not _text(role.get("id")):
            errors.append(f"roles[{index}] requires a non-empty id")
            continue
        role_id = role["id"]
        if role_id in role_ids:
            errors.append(f"duplicate role id: {role_id}")
        role_ids.add(role_id)
        for field in ("summary", "stopping_condition"):
            if not _text(role.get(field)):
                errors.append(f"role {role_id}: {field} must be non-empty text")
        for field in ("include", "exclude"):
            if not _text_list(role.get(field)):
                errors.append(f"role {role_id}: {field} must be a text list")

    try:
        routing = load_routing()
    except ContextError as exc:
        errors.append(str(exc))
    else:
        _validate_agent_routing(routing, role_ids, errors)

    for node_id, node in node_by_id.items():
        capsule_path = node.get("capsule")
        if not capsule_path or not (ROOT / capsule_path).exists():
            continue
        try:
            capsule = load_json(ROOT / capsule_path)
        except ContextError as exc:
            errors.append(str(exc))
            continue
        if capsule.get("schema_version") != 1:
            errors.append(f"{capsule_path}: schema_version must be 1")
        if capsule.get("id") != node_id:
            errors.append(f"{capsule_path}: id must match node {node_id}")
        for field in ("objective", "runtime_acceptance"):
            if not _text(capsule.get(field)):
                errors.append(f"{capsule_path}: {field} must be non-empty text")
        for field in ("scope", "ordered_steps", "authoritative_files", "constraints",
                      "preserve", "focused_validation", "stopping_conditions",
                      "cold_evidence"):
            if not _text_list(capsule.get(field)):
                errors.append(f"{capsule_path}: {field} must be a text list")
        for field in ("authoritative_files", "cold_evidence"):
            _check_paths(capsule_path, field, capsule.get(field), errors)

    return errors


def node_closure(node_id: str, nodes: dict[str, dict[str, Any]], depth: int) -> list[str]:
    """Return the selected node plus bounded dependency closure in BFS order."""
    result: list[str] = []
    seen: set[str] = set()
    queue: deque[tuple[str, int]] = deque([(node_id, 0)])
    while queue:
        current, current_depth = queue.popleft()
        if current in seen:
            continue
        seen.add(current)
        result.append(current)
        if current_depth >= depth:
            continue
        for dependency in nodes[current].get("depends_on", []):
            queue.append((dependency, current_depth + 1))
    return result


def _bullet_list(lines: list[str], heading: str, values: Iterable[str]) -> None:
    values = list(values)
    if not values:
        return
    lines.extend([f"### {heading}", ""])
    lines.extend(f"- {value}" for value in values)
    lines.append("")


def render_context(node_id: str, role_id: str | None = None, depth: int = 1) -> str:
    state, graph, roles_doc = load_metadata()
    nodes = {node["id"]: node for node in graph["nodes"]}
    roles = {role["id"]: role for role in roles_doc["roles"]}
    if node_id not in nodes:
        raise ContextError(f"unknown context node: {node_id}")
    if role_id is not None and role_id not in roles:
        raise ContextError(f"unknown role: {role_id}")
    if not 0 <= depth <= 3:
        raise ContextError("dependency depth must be between 0 and 3")

    selected_ids = node_closure(node_id, nodes, depth)
    selected = nodes[node_id]
    repository = state["repository"]
    lines = [
        f"# Context packet: {node_id}",
        "",
        "Generated from compact metadata. Referenced files are not concatenated.",
        "",
        "## Current repository state",
        "",
        f"- Canonical workspace: `{repository['canonical_workspace']}`",
        f"- Branch: `{repository['branch']}`",
        f"- Runtime source: `{repository['runtime_source_commit']}`",
        f"- Runtime identity: `{repository['runtime_marker']}` / `{repository['runtime_sha256']}`",
        f"- Current task: `{state['current_task']}`",
        "",
        "## Selected node",
        "",
        f"- Kind/status: `{selected['kind']}` / `{selected['status']}`",
        f"- {selected['summary']}",
        "",
    ]

    capsule_path = selected.get("capsule")
    if capsule_path:
        capsule = load_json(ROOT / capsule_path)
        lines.extend(["## Task capsule", "", f"- Objective: {capsule['objective']}", ""])
        _bullet_list(lines, "Ordered steps", capsule.get("ordered_steps", []))
        _bullet_list(lines, "Constraints", capsule.get("constraints", []))
        _bullet_list(lines, "Preserve", capsule.get("preserve", []))
        _bullet_list(lines, "Focused validation", [f"`{item}`" for item in capsule.get("focused_validation", [])])
        lines.extend(["### Runtime acceptance", "", capsule["runtime_acceptance"], ""])
        _bullet_list(lines, "Stopping conditions", capsule.get("stopping_conditions", []))

    dependencies = [nodes[value] for value in selected_ids[1:]]
    if dependencies:
        lines.extend(["## Dependency summaries", ""])
        for dependency in dependencies:
            lines.append(
                f"- `{dependency['id']}` [{dependency['status']}]: {dependency['summary']}"
            )
        lines.append("")

    relevant_ids = set(selected_ids)
    findings = [
        finding for finding in state.get("findings", [])
        if relevant_ids.intersection(finding.get("related_to", []))
    ]
    if findings:
        lines.extend(["## Relevant accepted state", ""])
        for finding in findings:
            lines.extend([
                f"### `{finding['id']}` — {finding['status']}",
                "",
                finding["claim"],
                "",
                f"- Acceptance: {finding['acceptance']}",
                f"- Next action: {finding['next_action']}",
                f"- Evidence: {', '.join(f'`{path}`' for path in finding['evidence'])}",
                "",
            ])

    authoritative: list[str] = []
    evidence: list[str] = []
    for current_id in selected_ids:
        for value, destination in (
            (nodes[current_id].get("authoritative_files", []), authoritative),
            (nodes[current_id].get("evidence", []), evidence),
        ):
            for path in value:
                if path not in destination:
                    destination.append(path)
    _bullet_list(lines, "Authoritative files to open as needed", [f"`{path}`" for path in authoritative])
    _bullet_list(lines, "Deeper evidence (cold unless directly needed)", [f"`{path}`" for path in evidence])

    if role_id is not None:
        role = roles[role_id]
        lines.extend([
            f"## Role: {role_id}",
            "",
            role["summary"],
            "",
        ])
        _bullet_list(lines, "Role receives", role["include"])
        _bullet_list(lines, "Role normally excludes", role["exclude"])
        lines.extend(["### Role stopping condition", "", role["stopping_condition"], ""])

    lines.extend([
        "## Retrieval rule",
        "",
        "Open a referenced source/evidence file only when the current step depends on it, "
        "an accepted claim is challenged, contradictory evidence appears, or provenance is required.",
        "",
    ])
    return "\n".join(lines)


def render_listing() -> str:
    state, graph, roles_doc = load_metadata()
    routing = load_routing()
    lines = [f"Current task: {state['current_task']}", "", "Nodes:"]
    for node in graph["nodes"]:
        lines.append(f"  {node['id']:<34} {node['kind']:<10} {node['status']}")
    lines.extend(["", "Roles:"])
    for role in roles_doc["roles"]:
        lines.append(f"  {role['id']:<18} {role['summary']}")
    lines.extend(["", f"Default agent mode: {routing['default_mode']}", "Task classes:"])
    for task_class in routing["task_classes"]:
        lines.append(
            f"  {task_class['id']:<34} tier {task_class['default_tier']}  "
            f"{' -> '.join(task_class['topology'])}"
        )
    return "\n".join(lines)


def render_route(task_class_id: str, mode_id: str | None = None) -> str:
    routing = load_routing()
    modes = {mode["id"]: mode for mode in routing["modes"]}
    task_classes = {task_class["id"]: task_class for task_class in routing["task_classes"]}
    selected_mode = mode_id or routing["default_mode"]
    if selected_mode not in modes:
        raise ContextError(f"unknown agent mode: {selected_mode}")
    if task_class_id not in task_classes:
        raise ContextError(f"unknown task class: {task_class_id}")
    task_class = task_classes[task_class_id]
    lines = [
        f"# Economy route: {task_class_id}", "",
        f"- Mode: `{selected_mode}` - {modes[selected_mode]['policy']}",
        f"- Default tier: `{task_class['default_tier']}`",
        f"- Default topology: `{' -> '.join(task_class['topology'])}`", "",
        "`worker` means the current primary agent, not a new subagent. Planning, research or review requests alone do not require delegation.", "",
        "## Conditional capabilities", "",
    ]
    if task_class["conditional"]:
        lines.extend(f"- {condition}" for condition in task_class["conditional"])
    else:
        lines.append("- None. Complete with the worker and stop.")
    if selected_mode == "high-assurance" and "economy_verifier" not in task_class["topology"]:
        lines.append("- High-assurance mode may add one verifier after mechanical checks when it can test a material risk.")
    lines.extend([
        "", "## Decision gate", "",
        f"- Default: {routing['delegation_gate']['default']}.",
        "- Use the first operation in the escalation order capable of resolving the next uncertainty.",
        "- A conditional capability is permitted only when expected saved context/reasoning or correctness value exceeds its full spawn-and-integration cost.",
        "- Optional capabilities receive a task delta plus one role-filtered context packet and return RESULT / EVIDENCE / ACTION / UNCERTAINTY.",
        "- Nested delegation is forbidden by default; replan only after a listed material trigger.", "",
    ])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("node", nargs="?", help="task/subsystem/workflow node id")
    parser.add_argument("--role", help="optional role id")
    parser.add_argument("--depth", type=int, default=1, help="dependency depth, 0-3 (default: 1)")
    parser.add_argument("--list", action="store_true", help="list available nodes and roles")
    parser.add_argument("--check", action="store_true", help="validate context metadata and references")
    parser.add_argument("--route", help="show economy route for a representative task class")
    parser.add_argument("--mode", help="economy, normal or high-assurance (with --route)")
    args = parser.parse_args(argv)

    errors = validate_metadata()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    if args.check:
        state, graph, roles_doc = load_metadata()
        routing = load_routing()
        print(
            "context metadata valid: "
            f"{len(graph['nodes'])} nodes, {len(roles_doc['roles'])} roles, "
            f"{len(state['findings'])} findings, "
            f"{len(routing['capabilities'])} optional agents, "
            f"{len(routing['task_classes'])} task classes"
        )
        return 0
    if args.list:
        print(render_listing())
        return 0
    if args.route:
        try:
            print(render_route(args.route, args.mode))
        except ContextError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
        return 0
    if args.mode:
        print("ERROR: --mode requires --route", file=sys.stderr)
        return 2

    state, _, _ = load_metadata()
    node_id = args.node or state["current_task"]
    try:
        print(render_context(node_id, args.role, args.depth))
    except ContextError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
