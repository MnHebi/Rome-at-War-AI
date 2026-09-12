import re
import unittest

from operand_smoke_probe import render
from validate_naval_doctrine import rule_blocks


class OperandSmokeTests(unittest.TestCase):
    def test_bounded_single_pass(self):
        text = render()
        rules = rule_blocks(text, diagnostic_view=False)
        self.assertEqual(len(rules), 57)
        self.assertIn('(up-jump-rule 56)', text)
        self.assertIn('(set-goal 100 1)', text)
        begins = re.findall(r'RAW-OPERAND BEGIN-(\S+) %d', text)
        ends = re.findall(r'RAW-OPERAND END-(\S+) %d', text)
        self.assertEqual(begins, ends)
        self.assertEqual(len(begins), 17)
        for forbidden in ('(load ', '(train ', '(build ', '(research ', '(up-target-', '(set-strategic-number '):
            self.assertNotIn(forbidden, text)

    def test_age_representation_pairs(self):
        text = render()
        for i, age in enumerate(('dark-age', 'feudal-age', 'castle-age')):
            self.assertIn(f'(defconst probe-age-{i} {age})', text)
            for value in (str(i), age, f'probe-age-{i}'):
                self.assertIn(f'(current-age == {value})', text)


if __name__ == '__main__':
    unittest.main()
