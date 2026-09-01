"""Structural tests for the bounded T26 assault-admission diagnostics."""

import re
import unittest

from test_pre_backlog import source
from validate_naval_doctrine import rule_blocks


class AssaultAdmissionDiagnosticTests(unittest.TestCase):
    def setUp(self):
        self.military = source('rawai-military.per')
        self.rules = list(rule_blocks(self.military))

    def test_diagnostic_goals_are_unique_and_generated(self):
        defs = source('rawai-assault-mission-defs.per')
        expected = {
            'gl-assault-admission-diag-next': 14923,
            'gl-assault-admission-diag-state': 14924,
            'gl-assault-admission-diag-mask': 14925,
            'gl-assault-admission-last-stage': 14926,
            'gl-assault-admission-last-time': 14927,
            'gl-assault-admission-reported-mask': 14928,
            'gl-assault-admission-reported-stage': 14929,
        }
        found = {name: int(value) for name, value in re.findall(
            r'\(defconst (gl-assault-admission-[\w-]+) (-?\d+)\)', defs)}
        for name, value in expected.items():
            self.assertEqual(found[name], value)
        self.assertEqual(len(expected.values()), len(set(expected.values())))

    def test_outer_mask_has_each_distinct_blocker_and_one_minute_cadence(self):
        start = next(row for row in self.rules
                     if 'gl-assault-admission-diag-next' in row[3]
                     and 'set-goal gl-assault-admission-diag-mask 0' in row[4])
        self.assertIn('current-age >= early-antiquity-age', start[3])
        self.assertIn('up-modify-goal gl-assault-admission-diag-next c:+ 60', start[4])
        expected = {
            1: 'gl-transport-route-state TRANSPORT-ROUTE-IDLE',
            2: 'gl-assault-admission-open YES',
            4: 'gl-island-migration-state MIGRATION-IDLE',
            8: 'gl-relic-ferry-state RELIC-FERRY-IDLE',
            16: 'gl-transport-recovery-state TRANSPORT-RECOVERY-IDLE',
            32: 'gl-transport-repair-state TRANSPORT-REPAIR-IDLE',
            64: 'gl-transport-clear-state TRANSPORT-CLEAR-IDLE',
            128: 'gl-home-defense-state NO',
            256: 'unit-type-count transport-ship < 1',
            512: 'gl-ap-seed-enemy c:< 1',
            1024: 't-transport-route != timer-triggered',
        }
        for bit, fact in expected.items():
            rows = [row for row in self.rules
                    if 'goal gl-assault-admission-diag-state 1' in row[3]
                    and re.search(rf'gl-assault-admission-diag-mask c:\+ {bit}\)', row[4])]
            self.assertEqual(len(rows), 1)
            self.assertIn(fact, rows[0][3])

    def test_output_is_transition_only_and_reuses_existing_strings(self):
        report = next(row for row in self.rules
                      if 'str-t12-diag-id c: 400' in row[4])
        self.assertIn('gl-assault-admission-diag-mask g:!= gl-assault-admission-reported-mask', report[3])
        self.assertIn('gl-assault-admission-last-stage g:!= gl-assault-admission-reported-stage', report[3])
        self.assertNotRegex(report[4], r'up-target-|up-create-group|up-modify-group-flag|up-reset-group')
        self.assertIn('set-goal gl-assault-admission-diag-state 2', report[4])
        continuation = [row for row in self.rules
                        if 'goal gl-assault-admission-diag-state 2' in row[3]
                        or 'goal gl-assault-admission-diag-state 3' in row[3]]
        self.assertEqual(len(continuation), 2)
        self.assertNotIn('RAW46', source('rawai-assault-mission-defs.per'))
        terminal = [row for row in self.rules
                    if row[3].count('(goal gl-assault-admission-diag-state 1)') == 1
                    and row[3].count('\n\t') == 1
                    and 'set-goal gl-assault-admission-diag-state 0' in row[4]]
        self.assertEqual(len(terminal), 1)

    def test_lifecycle_stages_cover_every_preparation_exit(self):
        expected = {
            1: 'TRANSPORT-ROUTE-IDLE',
            2: 'TRANSPORT-ROUTE-ADMISSION-CHECK',
            3: 'TRANSPORT-ROUTE-ADMISSION-CHECK',
            4: 'attack lift passengers unavailable',
            5: 'attack lift unavailable',
            6: 'assault claim rejected hull',
            7: 'TRANSPORT-ROUTE-RENDEZVOUS-START',
            8: 'TRANSPORT-ROUTE-LOAD-ISSUE',
            9: 'RAW44C assault ready hull',
        }
        for stage, marker in expected.items():
            rows = [row for row in self.rules
                    if f'set-goal gl-assault-admission-last-stage {stage}' in row[4]]
            self.assertGreaterEqual(len(rows), 1, stage)
            self.assertTrue(any(marker in row[3] or marker in row[4] for row in rows), stage)
            self.assertTrue(all('gl-assault-admission-last-time g:= gl-assault-mission-clock' in row[4]
                                for row in rows), stage)


if __name__ == '__main__':
    unittest.main()
