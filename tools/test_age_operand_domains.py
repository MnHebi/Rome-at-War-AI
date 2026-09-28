"""Keep engine Age operands separate from RAW phase, goal and TechId domains."""
from pathlib import Path
import unittest

from validate_per import validate_age_operands, validate_command_domains


class AgeOperandDomainTests(unittest.TestCase):
    def test_native_age_names_in_all_three_facts(self):
        for age in ("dark-age", "feudal-age", "castle-age", "imperial-age"):
            for fact in ("current-age", "starting-age", "players-current-age target-player"):
                with self.subTest(age=age, fact=fact):
                    self.assertEqual([], validate_age_operands([f"({fact} >= {age})"]))

    def test_custom_numeric_and_phase_operands_are_rejected(self):
        for age in ("iron-age", "early-antiquity-age", "middle-antiquity-age",
                    "IRON-AGE", "AGING-EARLY-ANTIQUITY", "0", "1", "2", "3", "unknown-age"):
            for fact in ("current-age", "starting-age", "players-current-age target-player"):
                with self.subTest(age=age, fact=fact):
                    self.assertEqual(1, len(validate_age_operands([f"({fact} != {age})"])))

    def test_post_imperial_only_for_starting_age(self):
        self.assertEqual([], validate_age_operands(["(starting-age == post-imperial-age)"]))
        for fact in ("current-age", "players-current-age target-player"):
            self.assertEqual(1, len(validate_age_operands([f"({fact} == post-imperial-age)"])))

    def test_non_age_domains_and_comments_are_untouched(self):
        source = '''(defconst iron-age 0)
(set-goal desired-age iron-age)
(goal current-phase IRON-AGE)
(research ri-early-antiquity-age)
(current-age-time >= 120)
; (current-age == iron-age)
(chat-to-self "(current-age == middle-antiquity-age)")'''
        self.assertEqual([], validate_age_operands(source.splitlines()))

    def test_nested_multiline_fact_and_validator_integration(self):
        lines = ["(defrule", " (not (players-current-age", " target-player >=", " early-antiquity-age))", "=>", " (disable-self))"]
        issues = validate_command_domains(lines)
        self.assertEqual(1, len(issues))
        self.assertEqual("non_native_engine_age_operand", issues[0]["kind"])
        self.assertEqual(2, issues[0]["line"])

    def test_all_current_runtime_sources_including_gitignored_files(self):
        sources = list(Path(__file__).resolve().parents[1].glob("*.per"))
        self.assertGreater(len(sources), 100)
        for source in sources:
            with self.subTest(source=source.name):
                self.assertEqual([], validate_age_operands(source.read_text(encoding="utf-8-sig").splitlines()))

    def test_shipyard_generator_emits_native_age_names(self):
        from generate_shipyard_placement import generate
        self.assertEqual([], validate_age_operands(generate().splitlines()))


if __name__ == "__main__":
    unittest.main()
