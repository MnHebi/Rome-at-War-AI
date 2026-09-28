"""Focused tests for the offline operand-repair acceptance checker."""
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import verify_operand_runtime as verifier

REPAIRED_LOG = """[AI RAW]: (up-can-build): Invalid goal used (0)
[AI RAW]: (up-can-build-line): Invalid goal used (0)
[AI RAW]: (up-get-point-distance): Invalid goal used (0)
"""
CLEAN_LOG = """[AI RAW]: (up-can-build): Invalid goal used (396)
[AI RAW]: (up-get-object-target-data): Object was invalid, returning -2
[AI RAW]: (up-remove-objects): Object was invalid, returning -2
[AI RAW]: (up-find-remote): Focus player is invalid (-1)
"""


class LogScanTests(unittest.TestCase):
    def scan(self, text):
        with TemporaryDirectory() as directory:
            path = Path(directory) / 'MainLog.txt'
            path.write_text(text, encoding='utf-8')
            return verifier.scan_engine_log(path)

    def test_former_error_families_are_counted_with_operands(self):
        counts, operands = self.scan(REPAIRED_LOG)
        self.assertEqual(counts['up-can-build'], 1)
        self.assertEqual(counts['up-can-build-line'], 1)
        self.assertEqual(counts['up-get-point-distance'], 1)
        self.assertEqual(dict(operands['up-can-build']), {0: 1})

    def test_control_families_remain_visible(self):
        counts, operands = self.scan(CLEAN_LOG)
        self.assertEqual(counts['up-can-build'], 1)
        self.assertEqual(dict(operands['up-can-build']), {396: 1})
        self.assertEqual(counts['up-get-object-target-data'], 1)
        self.assertEqual(counts['up-remove-objects'], 1)
        self.assertEqual(counts['up-find-remote'], 1)
        self.assertEqual(counts['up-set-offense-priority'], 0)


class AcceptanceTests(unittest.TestCase):
    def test_repaired_families_must_be_zero_and_controls_present(self):
        counts, operands = LogScanTests().scan(CLEAN_LOG)
        repaired_zero = all(counts.get(name, 0) == 0 for name in verifier.REPAIRED[:2])
        self.assertFalse(repaired_zero)          # up-can-build still reports 396
        self.assertEqual(counts.get('up-get-point-distance', 0), 0)
        controls_present = {name: counts.get(name, 0) > 0 for name in verifier.CONTROLS}
        self.assertTrue(controls_present['up-get-object-target-data'])
        self.assertTrue(controls_present['up-remove-objects'])
        self.assertTrue(controls_present['up-find-remote'])
        self.assertFalse(controls_present['up-set-offense-priority'])

    def test_repaired_site_inventory_and_migration_states_from_records(self):
        registry = {'sites': [
            {'id': 7, 'file': 'a.per', 'original': '(defrule (true) => (up-build place-normal gl-no-escrow-state c: house))'},
            {'id': 9, 'file': 'b.per', 'original': '(defrule (true) => (next-to))'},
        ]}
        with TemporaryDirectory() as directory:
            registry_path = Path(directory) / 'registry.json'
            registry_path.write_text(json.dumps(registry), encoding='utf-8')
            sites = verifier.repaired_sites(registry_path)
            self.assertEqual(sites, {7: 'a.per'})
            records_path = Path(directory) / 'records.jsonl'
            records_path.write_text('\n'.join([
                json.dumps(dict(complete=True, type=1, site=7, player=2, values=[3, 0, 0, -2, 0, 0])),
                json.dumps(dict(complete=True, type=32, site=7, player=2, values=[21, 50556])),
                json.dumps(dict(complete=False, player=2, error='truncated-tail')),
            ]) + '\n', encoding='utf-8')
            states = verifier.migration_states()
            reached, migration, failures = verifier.scan_records(records_path, sites, states)
            self.assertEqual(dict(reached), {7: 1})
            self.assertEqual(dict(migration), {'MIGRATION-DROPSITE-FAILED': 1})
            self.assertEqual(dict(failures), {'truncated-tail': 1})

    def test_migration_state_names_come_from_the_runtime_constants(self):
        states = verifier.migration_states()
        self.assertEqual(states.get(21), 'MIGRATION-DROPSITE-FAILED')
        self.assertEqual(states.get(37), 'MIGRATION-CHECK-DROPSITE')


if __name__ == '__main__':
    unittest.main()
