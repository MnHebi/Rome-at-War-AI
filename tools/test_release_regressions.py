"""Source-executed checks for the two historical recovery invariants.

These tests exercise the relevant PER predicates/actions, not the game engine.
Fresh all-player runtime evidence is still required for gameplay closure.
"""
from pathlib import Path
import re
import unittest

from validate_naval_doctrine import rule_blocks

ROOT = Path(__file__).resolve().parents[1]
CAPS = {"max-food-distance": 12, "max-hunt-distance": 16}


def compact(text):
    return " ".join(text.split())


def cap_rules(text):
    result = {}
    for name, limit in CAPS.items():
        rules = [r for r in rule_blocks(text)
                 if re.search(rf"\(up-modify-goal\s+{name}\b", r[4])]
        assert len(rules) == 1, (name, "missing/duplicate cap")
        rule = rules[0]
        assert compact(rule[3]) == f"(defrule (up-compare-goal {name} c:> {limit})"
        assert compact(rule[4]) == f"(up-modify-goal {name} c:= {limit}) )"
        result[name] = rule
    return result


def run_cap(rule, goals):
    # Execute the actual single predicate/action, failing on unsupported forms.
    condition = re.fullmatch(r"\(defrule \(up-compare-goal ([\w-]+) c:> (\d+)\)",
                             compact(rule[3]))
    action = re.fullmatch(r"\(up-modify-goal ([\w-]+) c:= (\d+)\) \)",
                          compact(rule[4]))
    assert condition and action
    if goals[condition[1]] > int(condition[2]):
        goals[action[1]] = int(action[2])


class GatherDistanceRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.source = (ROOT / "rawai-economy.per").read_text(encoding="utf-8-sig")

    def test_above_cap_is_clamped_without_other_goal_mutations(self):
        for name, rule in cap_rules(self.source).items():
            for value in (CAPS[name] + 1, 28, 31, 100, 32767):
                with self.subTest(goal=name, value=value):
                    goals = {name: value, "food-gatherer-percentage": 41,
                             "wood-gatherer-percentage": 29, "farm-staffing": 7}
                    expected = dict(goals, **{name: CAPS[name]})
                    run_cap(rule, goals)
                    self.assertEqual(goals, expected)

    def test_within_cap_is_never_expanded(self):
        for name, rule in cap_rules(self.source).items():
            for value in range(-1, CAPS[name] + 1):
                goals = {name: value}
                run_cap(rule, goals)
                self.assertEqual(goals, {name: value})

    def test_caps_precede_engine_distance_publication(self):
        rules = rule_blocks(self.source)
        for name, cap in cap_rules(self.source).items():
            resource = "food" if name == "max-food-distance" else "hunt"
            publish = [r for r in rules if
                       f"(up-modify-sn sn-maximum-{resource}-drop-distance g:= {name})"
                       in r[4]]
            self.assertEqual(len(publish), 1)
            self.assertLess(cap[0], publish[0][0])

    def test_missing_or_raised_cap_is_rejected(self):
        for name, cap in cap_rules(self.source).items():
            for mutant in (
                self.source[:cap[0]] + self.source[cap[1]:],
                self.source.replace(f"{name} c:> {CAPS[name]}", f"{name} c:> 99")
                           .replace(f"{name} c:= {CAPS[name]}", f"{name} c:= 99"),
            ):
                with self.assertRaises(AssertionError):
                    cap_rules(mutant)


if __name__ == "__main__":
    unittest.main()
