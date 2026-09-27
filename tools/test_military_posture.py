"""T157 military posture: target choice, chase leash, and party admission.

Configuration contract only: the engine verdict for each strategic number is
recorded in the project's AIRef snapshot (`airef-reference-20260830.js`), and the
leash is a script rule, so these tests pin what the payload asks for rather than
claiming what DE does with it.
"""
import re
import unittest

from test_pre_backlog import source
from validate_naval_doctrine import rule_blocks


class MilitaryPostureTests(unittest.TestCase):
    def test_target_choice_uses_the_de_effective_setting(self):
        # sn-target-evaluation-* is inherited/AoE1 (de 0, up 0, effective 0), so the
        # only effective target-choice knob is sn-local-targeting-mode.
        text = source('rawai-customconstants.per')
        self.assertIn('(set-strategic-number sn-local-targeting-mode 1)', text)
        self.assertNotIn('sn-target-evaluation-', text)

    def test_idle_military_is_recalled_instead_of_drifting(self):
        text = source('rawai-customconstants.per')
        self.assertIn('(set-strategic-number sn-gather-idle-soldiers-at-center 1)', text)
        self.assertIn('(set-strategic-number sn-sentry-distance-variation 0)', text)
        self.assertIn('(set-strategic-number sn-percent-enemy-sighted-response 60)', text)
        # The DE-ineffective defence numbers are left alone, not retuned.
        self.assertIn('(set-strategic-number sn-defense-distance 12)', text)

    def test_periodic_party_is_not_gated_on_superiority(self):
        # A tolerable-but-not-equal army still sends its bounded land-attack-percentage
        # probe; the dispatch itself is unchanged.
        rows = [r for r in rule_blocks(source('rawai-military.per'))
                if 'periodic attack' in r[4]]
        self.assertEqual(len(rows), 1)
        facts, actions = rows[0][3], rows[0][4]
        self.assertIn('(up-compare-goal military-superiority c:>= TOLERABLE)', facts)
        self.assertNotIn('(up-compare-goal military-superiority c:>= EQUAL)', facts)
        self.assertIn('(up-modify-sn sn-percent-attack-soldiers g:= land-attack-percentage)', actions)
        self.assertIn('(attack-now)', actions)


if __name__ == '__main__':
    unittest.main()
