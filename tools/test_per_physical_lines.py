"""T17 startup regression: formatting safeguards, not an engine parser emulator."""
import hashlib
import re
import unittest
from unittest.mock import Mock

from generate_assault_missions import preparation_ownership
from validate_naval_doctrine import rule_blocks
from validate_per import MAX_CODE_LINE_BYTES, validate_file


class PhysicalLineTests(unittest.TestCase):
    def validate(self, text):
        return validate_file(Mock(read_text=Mock(return_value=text)))

    def test_old_single_line_condition_is_rejected(self):
        # Recreate the exact 727-byte condition at the reported T17 line 8.
        facts = rule_blocks(preparation_ownership())[0][3].removeprefix('(defrule')
        old_line = '\t' + ' '.join(facts.split())
        self.assertEqual(len(old_line.encode('utf-8')), 727)
        issues = self.validate('(defrule\n' + old_line + '\n=>\n(disable-self)\n)')
        self.assertEqual(issues, [dict(kind='physical_code_line_too_long', line=2,
                                      bytes=727, maximum=MAX_CODE_LINE_BYTES)])

    def test_wrapped_module_passes_structural_and_physical_checks(self):
        self.assertEqual(self.validate(preparation_ownership()), [])

    def test_hotfix_preserves_every_t17_token(self):
        # Whitespace-normalized original from immutable T17 startup-failure
        # payload E060FC4B...11C3D. Conditions/actions/order are unchanged.
        normalized = ' '.join(re.findall(r'\S+', preparation_ownership()))
        self.assertEqual(hashlib.sha256(normalized.encode()).hexdigest(),
                         '17f2e0c44a172bcd4a4b0888ac727be9a248bbaab7a2759bc6eb34ea757341d7')

    def test_project_limit_boundary(self):
        for size in (MAX_CODE_LINE_BYTES, MAX_CODE_LINE_BYTES + 1):
            with self.subTest(size=size):
                line = '(defconst sample 1)'.ljust(size)
                issues = self.validate(line)
                self.assertEqual(len(issues), int(size > MAX_CODE_LINE_BYTES))

    def test_comments_alone_do_not_trigger_executable_line_limit(self):
        self.assertEqual(self.validate('; ' + 'x' * 1000), [])

    def test_strings_are_counted_in_physical_utf8_bytes(self):
        line = '(chat-to-all "' + '\u00e9' * 120 + '")'
        issues = self.validate('(defrule\n(true)\n=>\n' + line + '\n)')
        self.assertEqual(issues[0]['kind'], 'physical_code_line_too_long')
        self.assertEqual(issues[0]['bytes'], len(line.encode('utf-8')))


if __name__ == '__main__':
    unittest.main()
