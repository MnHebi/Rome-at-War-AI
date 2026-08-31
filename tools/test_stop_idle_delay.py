"""T16S1 configuration checks only; native STOP generation needs an engine test."""
import re
import unittest

from test_pre_backlog import source
from validate_naval_doctrine import rule_blocks


class IdleDelayExperimentTests(unittest.TestCase):
    def test_nonzero_delay_in_each_advanced_difficulty(self):
        text = source('rawai-sn-defines.per')
        for difficulty in ('MODERATE', 'HARD', 'HARDEST', 'EXTREME'):
            block = text.split('#load-if-defined DIFFICULTY-' + difficulty + '\n', 1)[1]
            block = block.split('#end-if', 1)[0]
            self.assertEqual(re.findall(r'\(set-strategic-number sn-consecutive-idle-unit-limit (\d+)\)', block), ['5'])

    def test_every_idle_delay_writer_is_one_shot_and_no_zero_writer_remains(self):
        # This verifies script configuration, not the engine's interpretation.
        from pathlib import Path
        root = Path(__file__).resolve().parents[1]
        found = []
        for path in root.glob('*.per'):
            for row in rule_blocks(path.read_text(encoding='utf-8-sig')):
                if '(set-strategic-number sn-consecutive-idle-unit-limit ' in row[4]:
                    self.assertIn('(disable-self)', row[4])
                    self.assertNotIn('action-stop', row[4])
                    found.extend(re.findall(r'sn-consecutive-idle-unit-limit (\d+)\)', row[4]))
        self.assertCountEqual(found, ['10', '5', '5', '5', '5'])


if __name__ == '__main__':
    unittest.main()
