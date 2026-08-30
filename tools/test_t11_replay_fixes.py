"""Focused T11 source-contract regressions; not an engine simulation."""
from pathlib import Path
import re
import unittest

from validate_naval_doctrine import rule_blocks

ROOT = Path(__file__).resolve().parents[1]


def source(name):
    return (ROOT / name).read_text(encoding='utf-8-sig')


class BoardingClockTests(unittest.TestCase):
    def test_boarding_clock_precedes_issue_and_is_unconditional(self):
        text = source('rawai-military.per')
        rows = list(rule_blocks(text))
        clock = next(r for r in rows if 'up-get-fact game-time 0 gl-transport-load-clock' in r[4])
        issue = next(r for r in rows if '(goal gl-transport-route-state TRANSPORT-ROUTE-LOAD-ISSUE)' in r[3])
        self.assertIn('(true)', clock[3])
        self.assertLess(clock[0], issue[0])
        self.assertNotIn('disable-self', clock[4])

    def test_all_load_deadlines_and_retries_use_live_clock(self):
        text = source('rawai-military.per')
        expressions = re.findall(r'\((?:up-compare-goal|up-modify-goal)[^\n()]*gl-transport-route-load-(?:deadline|next)[^\n()]*\)', text)
        self.assertGreaterEqual(len(expressions), 11)
        self.assertTrue(all('gl-game-time' not in e for e in expressions))
        deadline = re.search(r'\(up-modify-goal gl-transport-route-load-deadline c:\+ (\d+)\)', text)
        self.assertIsNotNone(deadline)
        duration = int(deadline[1])
        for stale_age in range(15):
            live = 3600
            stale = live - stale_age
            self.assertEqual((live + duration) - live, 30)
            self.assertLessEqual((stale + duration) - live, 30)

    def test_full_and_partial_loading_contract_preserved(self):
        text = source('rawai-military.per')
        self.assertIn('(up-object-data object-data-garrison-count g:>= gl-transport-route-load-target)', text)
        self.assertIn('(up-object-data object-data-garrison-count >= 5)', text)
        self.assertIn('(up-remove-objects search-local object-data-group-flag != attack-boarding-group)', text)


if __name__ == '__main__':
    unittest.main()
