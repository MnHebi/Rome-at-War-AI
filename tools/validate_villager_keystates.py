#!/usr/bin/env python3
"""Validate the narrow T53 Ctrl-retask boundary and immediate key reset."""
from __future__ import annotations

import re
import sys
from pathlib import Path

from validate_naval_doctrine import rule_blocks


ROOT = Path(__file__).resolve().parents[1]
SET_CTRL = "(set-strategic-number sn-keystates 2)"
RESET_KEYS = "(set-strategic-number sn-keystates 0)"
RETASK = "(up-target-objects 0 action-default -1 stance-no-attack)"
CARRY_RECHECK = "(up-remove-objects search-local object-data-carry > 0)"
EXPECTED_STATES = {
    "FARM-STAFFING-CHECK-FISHERMAN",
    "FARM-STAFFING-CHECK-IDLE",
    "FARM-STAFFING-ASSIGN",
    "FARM-STAFFING-FIND-RESOURCE",
}


def semantic_action_lines(actions: str) -> list[str]:
    """Return nonempty single-line PER actions with comments removed."""
    result = []
    for raw in actions.splitlines():
        line = raw.split(";", 1)[0].strip()
        if line and line != ")":
            result.append(line)
    return result


def validate_repository(root: Path = ROOT) -> list[str]:
    issues: list[str] = []
    wrappers: list[tuple[str, str]] = []
    modifier_lines: list[tuple[str, str]] = []
    for path in sorted(root.glob("*.per")):
        text = path.read_text(encoding="utf-8-sig")
        for raw in text.splitlines():
            line = raw.split(";", 1)[0].strip()
            if "sn-keystates" in line:
                if (path.name == 'rawai-command-boundary.per' and line == '(up-modify-goal gl-cb-modifier s:= sn-keystates)' or
                    path.name in {'rawai-command-boundary.per', 'rawai-command-boundary-coverage.per'} and
                    line == '(up-modify-goal gl-cbf-value s:= sn-keystates)'):
                    continue  # exact read-only observation, not a modifier writer
                modifier_lines.append((path.name, line))
                if path.name not in {"rawai-homebase.per", "rawai-military.per"} or line not in {
                    SET_CTRL, RESET_KEYS
                }:
                    issues.append(
                        f"{path.name}: unauthorized sn-keystates use: {line}"
                    )
        for _start, _end, _block, facts, actions in rule_blocks(text):
            semantic = semantic_action_lines(actions)
            state_match = re.search(
                r"\(goal gl-farm-staffing-state ([^)]+)\)", facts
            )
            state = state_match.group(1) if state_match else "<no-farm-state>"
            boarding = path.name == 'rawai-military.per'
            if boarding:
                state_match = re.search(r'\(goal gl-island-migration-state ([^)]+)\)', facts)
                state = state_match.group(1) if state_match else '<no-migration-state>'
            for index, action in enumerate(semantic):
                match = re.fullmatch(
                    r"\(set-strategic-number sn-keystates (-?\d+)\)", action
                )
                if match and match.group(1) not in {"0", "2"}:
                    issues.append(
                        f"{path.name}:{state}: unsupported nonzero sn-keystates "
                        f"value {match.group(1)}"
                    )
                if action != SET_CTRL:
                    continue
                wrappers.append((path.name, state))
                expected = semantic[index:index + 3]
                command = '(up-target-objects 0 action-garrison -1 stance-no-attack)' if boarding else RETASK
                if expected != [SET_CTRL, command, RESET_KEYS]:
                    issues.append(
                        f"{path.name}:{state}: Ctrl must immediately wrap exactly "
                        "one unchanged economic action-default command and reset"
                    )
                if boarding and '(goal gl-island-migration-mission MIGRATION-MISSION-MINING)' not in facts:
                    issues.append(f'{path.name}:{state}: mining-only boundary missing')
                if not boarding and CARRY_RECHECK not in semantic[:index]:
                    issues.append(
                        f"{path.name}:{state}: missing zero-carry command recheck"
                    )

    expected_wrappers = {
        ("rawai-homebase.per", state) for state in EXPECTED_STATES
    }
    expected_wrappers |= {('rawai-military.per', state) for state in (
        'MIGRATION-RENDEZVOUS-START', 'MIGRATION-RENDEZVOUS-PASSENGER',
        'MIGRATION-ISSUE-BOARD', 'MIGRATION-LOAD-DIAG-APPLY', 'MIGRATION-CHECK-LOAD')}
    actual_wrappers = set(wrappers)
    if len(wrappers) != 9:
        issues.append(f"expected exactly 9 Ctrl wrappers, found {len(wrappers)}")
    if actual_wrappers != expected_wrappers:
        missing = sorted(expected_wrappers - actual_wrappers)
        extra = sorted(actual_wrappers - expected_wrappers)
        issues.append(f"Ctrl wrapper boundary mismatch; missing={missing}, extra={extra}")
    if sum(line == RESET_KEYS for _path, line in modifier_lines) != 9:
        issues.append("each of the 9 Ctrl wrappers must have exactly one reset")

    for forbidden in (
        "rawai-hunt.per",
        "rawai-general.per",
        "rawai-economy.per",
        "rawai-exploration-policy.per",
    ):
        source = (root / forbidden).read_text(encoding="utf-8-sig")
        if "sn-keystates" in source:
            issues.append(f"{forbidden}: modifier leaked into protected controller")
    return issues


def main() -> None:
    issues = validate_repository()
    if issues:
        for issue in issues:
            print(issue)
        raise SystemExit(1)
    print("villager keystates validation: PASS (4 economic + 5 mining boarding Ctrl wrappers)")


if __name__ == "__main__":
    main()
