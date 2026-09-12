"""Four-TC policy, including the resource-pressure colony exception."""
import re
import unittest
from test_pre_backlog import ROOT, source
from test_t13_gate_recovery import Gate, CONSTANTS
from validate_naval_doctrine import rule_blocks


class TownCenterCapTests(unittest.TestCase):
    def test_every_civilization_keeps_early_targets_and_caps_late_target(self):
        files = list(ROOT.glob('rawai-civ-*.per'))
        self.assertEqual(len(files), 34)
        for path in files:
            values = re.findall(r'\(up-modify-goal desired-number-towncenters c:= (\d+)\)', source(path.name))
            self.assertEqual([int(v) for v in values], [1, 1, 1, 4, 4], path.name)

    def test_resource_pressure_does_not_bypass_colony_cap(self):
        row = next(r for r in rule_blocks(source('rawai-homebase.per'))
                   if '(goal gl-colony-towncenter-state COLONY-TC-GATE)' in r[3]
                   and '(can-afford-building town-center)' in r[3])
        for count in (3, 4, 8):
            gate = Gate(**{
                'gl-colony-towncenter-state': CONSTANTS['COLONY-TC-GATE'],
                'gl-lumbercamp-placement-state': CONSTANTS['PLACEMENT-IDLE'],
                'gl-miningcamp-placement-state': CONSTANTS['PLACEMENT-IDLE'],
                'current-age': CONSTANTS['imperial-age'],
                'desired-number-towncenters': 1,
                'resources-depleted': 1, 'gl-home-resource-pressure': 1,
            })
            gate.counts['town-center'] = count
            self.assertEqual(gate.accepts(row), count < 4)

    def test_home_expansion_uses_total_including_pending_foundations(self):
        row = next(r for r in rule_blocks(source('rawai-homebase.per'))
                   if '(up-build place-normal 0 c: town-center)' in r[4]
                   and 'desired-number-towncenters' in r[3])
        self.assertIn('(building-type-count-total town-center g:< desired-number-towncenters)', row[3])
        self.assertIn('(up-pending-objects c: town-center <= 0)', row[3])
