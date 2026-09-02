"""Source-executed checks for the two historical recovery invariants.

These tests exercise the relevant PER predicates/actions, not the game engine.
Fresh all-player runtime evidence is still required for gameplay closure.
"""
from pathlib import Path
import re
import unittest

from validate_naval_doctrine import rule_blocks

ROOT = Path(__file__).resolve().parents[1]
CAPS = {"max-food-distance": 12, "max-hunt-distance": 28}


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


def expressions(text):
    """Parse the comment-free facts returned by the existing PER rule reader."""
    tokens = iter(re.findall(r"\(|\)|[^\s()]+", text))

    def read(first):
        if first != "(":
            return first
        result = []
        for token in tokens:
            if token == ")":
                return result
            result.append(read(token))
        raise AssertionError("unterminated expression")

    return [read(token) for token in tokens]


def fallback_rules(text, require_guard=True):
    result = []
    for rule in rule_blocks(text):
        writes = re.findall(
            r"\((?:set-strategic-number\s+sn-target-player-number\s+|"
            r"up-modify-sn\s+sn-target-player-number\s+c:=\s+)([1-8])\)", rule[4])
        for candidate in writes:
            # Taunt-directed targets are not automatic fallback selection.
            facts = expressions(rule[3] + ")")[0][1:]
            if require_guard:
                assert ["up-compare-goal", "gl-self-player-number", "c:!=", candidate] in facts
                assert ["player-in-game", candidate] in facts
                assert ["not", ["stance-toward", candidate, "ally"]] in facts
                assert ["players-building-count", candidate, ">=", "1"] in facts
            result.append((int(candidate), facts, rule))
    return result


def evaluate(fact, self_player, candidate, target_valid=False):
    command, *args = fact
    if command in ("or", "and", "nor"):
        values = [evaluate(x, self_player, candidate, target_valid) for x in args]
        return {"or": any(values), "and": all(values), "nor": not any(values)}[command]
    if command == "not":
        return not evaluate(args[0], self_player, candidate, target_valid)
    if command == "up-compare-goal":
        if args == ["military-superiority", "c:>=", "TOLERABLE"]:
            return True  # All non-self predicates are deliberately satisfied.
        assert args[:2] == ["gl-self-player-number", "c:!="]
        return self_player != int(args[2])
    player = candidate if args[0] != "target-player" else (9 if target_valid else 0)
    if command == "player-in-game":
        return player != 0
    if command == "stance-toward":
        assert args[1] == "ally"
        return False  # In particular, self is NOT an ally for this predicate.
    if command == "players-building-count":
        count = int(player != 0)
        assert args[1:] in ([">=", "1"], ["<=", "0"])
        return count >= 1 if args[1] == ">=" else count <= 0
    raise AssertionError(f"Unsupported fallback fact: {fact}")


class SelfTargetRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.source = (ROOT / "rawai-military.per").read_text(encoding="utf-8-sig")

    def test_every_explicit_military_fallback_has_mandatory_self_guard(self):
        fallbacks = fallback_rules(self.source)
        self.assertEqual([n for n, _, _ in fallbacks], list(range(1, 9)))
        # Also catch a future automatic fallback added in another runtime file.
        for path in ROOT.glob("*.per"):
            text = path.read_text(encoding="utf-8-sig")
            for n, facts, _ in fallback_rules(text, require_guard=False):
                if not any(
                        str(f[0]).startswith("taunt-") for f in facts):
                    self.assertIn(["up-compare-goal", "gl-self-player-number", "c:!=", str(n)], facts)

    def test_each_self_rejected_and_each_nonself_enemy_selectable(self):
        for candidate, facts, _ in fallback_rules(self.source):
            for self_player in range(1, 9):
                with self.subTest(candidate=candidate, self_player=self_player):
                    enabled = all(evaluate(f, self_player, candidate) for f in facts)
                    self.assertEqual(enabled, candidate != self_player)
                    self.assertFalse(all(evaluate(f, self_player, candidate, target_valid=True)
                                         for f in facts))

    def test_removing_any_guard_reproduces_self_selection_and_fails_invariant(self):
        for candidate, _, _ in fallback_rules(self.source):
            mutant = self.source.replace(
                f"(up-compare-goal gl-self-player-number c:!= {candidate})", "")
            with self.assertRaises(AssertionError):
                fallback_rules(mutant)
            mutated = [facts for n, facts, _ in fallback_rules(mutant, require_guard=False)
                       if n == candidate][0]
            self.assertTrue(all(evaluate(f, candidate, candidate) for f in mutated))

    def test_self_identity_is_initialized_before_fallbacks(self):
        entry = (ROOT / "AI RAW.per").read_text(encoding="utf-8-sig")
        self.assertLess(entry.index('(load "rawai-init-goals")'),
                        entry.index('(load "rawai-military")'))
        initializers = []
        for path in ROOT.glob("*.per"):
            for rule in rule_blocks(path.read_text(encoding="utf-8-sig")):
                if "(up-get-fact my-player-number 0 gl-self-player-number)" in rule[4]:
                    initializers.append(rule)
                self.assertNotRegex(rule[4], r"\((?:set-goal|up-modify-goal) gl-self-player-number\b")
        self.assertEqual(len(initializers), 1)
        self.assertEqual(compact(initializers[0][3]), "(defrule (true)")
        self.assertIn("(disable-self)", initializers[0][4])


if __name__ == "__main__":
    unittest.main()
