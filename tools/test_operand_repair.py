"""Contracts for the dedicated no-escrow goal and the repaired operands.

Source-level checks of the emitted payload: allocation, one-shot initialization,
immutability, and the per-command operand roles verified against the cached
AIRef signatures (up-can-build/up-can-build-line/up-build take an EscrowGoalId;
up-build-line takes two Points; up-get-point-distance takes two Points).
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOAL = 'gl-no-escrow-state'


def source(name):
    return (ROOT / name).read_text(encoding='utf-8-sig')


def strip_comments(text):
    return re.sub(r';[^\n]*', '', text)


class NoEscrowGoalTests(unittest.TestCase):
    def test_goal_is_allocated_once_in_the_documented_escrow_range(self):
        allocations = re.findall(r'\(defconst ([\w-]+) (-?\d+)\)',
                                 strip_comments(source('rawai-customconstants.per')))
        matches = [(name, int(value)) for name, value in allocations if name == GOAL]
        self.assertEqual(len(matches), 1, matches)
        value = matches[0][1]
        # Documented valid range for an EscrowGoalId operand: extended goals 41-510.
        self.assertGreaterEqual(value, 41)
        self.assertLessEqual(value, 510)
        for name, other in allocations:
            if name != GOAL:
                self.assertNotEqual(int(other), value, name)

    def test_goal_is_initialized_once_before_any_consumer(self):
        init = source('rawai-init-goals.per')
        writes = re.findall(r'\(set-goal ' + GOAL + r' ([\w-]+)\)', strip_comments(init))
        self.assertEqual(writes, ['without-escrow'])
        self.assertEqual(len(re.findall(r'\(set-goal ' + GOAL + r'\b', strip_comments(init))), 1)
        loads = re.findall(r'\(load "([^"]+)"\)', source('AI RAW.per'))
        # Consumers are the files that pass the no-escrow goal; the one-shot
        # initialization must load before every one of them.
        usage = re.compile(r'\(up-(?:can-)?build\b[^()]*' + GOAL)
        consumers = {name for name in loads if usage.search(strip_comments(source(f'{name}.per')))}
        self.assertTrue(consumers)
        self.assertLess(loads.index('rawai-init-goals'),
                        min(loads.index(name) for name in consumers))

    def test_goal_is_never_written_after_initialization(self):
        for path in sorted(ROOT.glob('*.per')):
            if path.name == 'rawai-init-goals.per':
                continue
            text = strip_comments(path.read_text(encoding='utf-8-sig'))
            self.assertNotRegex(text, r'\((?:set-goal|up-modify-goal)\s+' + GOAL + r'\b', path.name)
            self.assertNotRegex(text, r'up-get-[a-z-]+[^()]*\s' + GOAL + r'\s*\)', path.name)

    def test_every_escrow_operand_is_named_or_dynamic_never_literal_zero(self):
        for path in sorted(ROOT.glob('*.per')):
            text = strip_comments(path.read_text(encoding='utf-8-sig'))
            self.assertNotRegex(text, r'\(up-can-build 0(?= c:)', path.name)
            self.assertNotRegex(text, r'\(up-can-build-line 0(?= \S)', path.name)
            self.assertNotRegex(text, r'\(up-build [a-z-]+ 0(?= c:)', path.name)
            for operand in re.findall(r'\(up-can-build ([^)\s]+)', text):
                self.assertIn(operand, (GOAL, 'gl-buildingescrow-state'), path.name)
            for operands in re.findall(r'\(up-build ([a-z-]+) ([^)\s]+)', text):
                self.assertIn(operands[1], (GOAL, 'gl-buildingescrow-state'), path.name)

    def test_build_line_and_point_distance_keep_their_point_signatures(self):
        for path in sorted(ROOT.glob('*.per')):
            text = strip_comments(path.read_text(encoding='utf-8-sig'))
            # up-build-line takes two Points; no escrow goal may be inserted.
            for operands in re.findall(r'\(up-build-line ([^\n]*?)\)', text):
                self.assertNotIn(GOAL, operands, path.name)
            for operands in re.findall(r'\(up-get-point-distance ([^\n]*?)\)', text):
                self.assertNotIn(' 0 ', operands, (path.name, operands))

    def test_shipyard_memory_checks_compare_the_candidate_point(self):
        text = strip_comments(source('rawai-specialplacement.per'))
        for index in range(4):
            self.assertIn(f'(up-get-point-distance gl-sy-memory{index}-x gl-shipyard-x gl-sy-count)', text)
        self.assertEqual(len(re.findall(r'up-get-point-distance gl-sy-memory\d-x gl-shipyard-x', text)), 4)


if __name__ == '__main__':
    unittest.main()
