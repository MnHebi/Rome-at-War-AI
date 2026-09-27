"""T157 parity system: ratio bands, two-poll hysteresis, two-way army signal.

Configuration contract only. The review that produced these rules is recorded in
the PR body: the old ladder compared populations against *half* the enemy team,
broke the rung on exact equality, and was consumed only to throttle attacks.
"""
import re
import unittest

from test_pre_backlog import source
from validate_naval_doctrine import rule_blocks

MILITARY = 'rawai-military.per'


def parity_rules():
    return [r for r in rule_blocks(source(MILITARY))
            if 'gl-parity' in r[4] or 'milcheck-concluded' in r[3]]


class ParityTests(unittest.TestCase):
    def test_bands_are_ratios_of_the_full_enemy_army(self):
        text = source(MILITARY)
        # No halved enemy totals and no exact-equality rung remain.
        self.assertNotIn('g:== gl-enemy-team-military-population', text)
        self.assertNotIn('g:== gl-enemy-team-navy', text)
        for line in ('(up-modify-goal gl-parity-ratio g:= gl-own-military-population)',
                     '(up-modify-goal gl-parity-ratio c:* 100)',
                     '(up-modify-goal gl-parity-ratio g:z/ gl-enemy-team-military-population)',
                     '(up-modify-goal gl-parity-ratio-navy g:= gl-own-navy)',
                     '(up-modify-goal gl-parity-ratio-navy g:z/ gl-enemy-team-navy)'):
            self.assertIn(line, text)
        # Team games measure the whole team, still against the whole enemy team.
        self.assertIn('(up-modify-goal gl-parity-ratio g:= gl-team-combined-mil-pop)', text)
        self.assertIn('(up-modify-goal gl-parity-ratio-navy g:= gl-team-combined-navy)', text)

    def test_band_cutoffs_are_60_100_and_120(self):
        rows = [r for r in rule_blocks(source(MILITARY))
                if '(set-goal gl-parity-candidate ' in r[4] or '(set-goal gl-parity-candidate-navy ' in r[4]]
        self.assertEqual(len(rows), 8)
        for goal in ('gl-parity-ratio', 'gl-parity-ratio-navy'):
            facts = [r[3] for r in rows if goal in r[3]]
            joined = ' '.join(' '.join(f.split()) for f in facts)
            for cut in ('c:< 60', 'c:>= 60', 'c:< 100', 'c:>= 100', 'c:< 120', 'c:>= 120'):
                self.assertIn(cut, joined, f'{goal} missing {cut}')
        # No enemy army is SUPERIOR, not a zero ratio.
        self.assertIn('(up-modify-goal gl-parity-ratio c:= 200)', source(MILITARY))
        self.assertIn('(up-modify-goal gl-parity-ratio-navy c:= 200)', source(MILITARY))

    def test_attack_share_follows_the_ratio_instead_of_a_ladder(self):
        text = source(MILITARY)
        for goal in ('land-attack-percentage', 'naval-attack-percentage'):
            self.assertNotRegex(text, rf'\(set-goal {goal} (10|30|50|80)\)')
        self.assertIn('(up-modify-goal land-attack-percentage g:= gl-parity-ratio)', text)
        self.assertIn('(up-modify-goal naval-attack-percentage g:= gl-parity-ratio-navy)', text)
        for op in ('c:z/ 2', 'c:min 80', 'c:max 10'):
            self.assertGreaterEqual(text.count(f'(up-modify-goal land-attack-percentage {op})'), 1)
            self.assertGreaterEqual(text.count(f'(up-modify-goal naval-attack-percentage {op})'), 1)

    def test_rung_changes_need_two_consecutive_censuses(self):
        text = source(MILITARY)
        self.assertIn('(up-modify-goal gl-parity-prev g:= gl-parity-candidate)', text)
        self.assertIn('(up-modify-goal gl-parity-prev-navy g:= gl-parity-candidate-navy)', text)
        rows = [r for r in rule_blocks(source(MILITARY))
                if 'g:== gl-parity-prev' in r[3]]
        self.assertEqual(len(rows), 2)
        for _a, _b, _body, facts, actions in rows:
            self.assertIn('(goal milcheck-concluded COMPARISONS)', facts)
            self.assertRegex(actions, r'\(up-modify-goal (military|naval)-superiority g:= gl-parity-candidate')
        # Nothing else writes a rung.
        self.assertNotRegex(text, r'\(set-goal (military|naval)-superiority (INFERIOR|TOLERABLE|EQUAL|SUPERIOR)\)')

    def test_census_requires_an_enemy_still_in_game(self):
        rows = [r for r in rule_blocks(source(MILITARY))
                if 'gl-enemy-team-military-population' in r[4]]
        self.assertTrue(any('(player-in-game any-enemy)' in r[3] for r in rows))
        self.assertTrue(any('(not (player-in-game any-enemy))' in r[3] for r in rows))

    def test_poll_and_major_loss_re_census(self):
        text = source(MILITARY)
        self.assertIn('(enable-timer t-mil-pop-check 30)', text)
        self.assertNotIn('(enable-timer t-mil-pop-check 60)', text)
        rows = [r for r in rule_blocks(source(MILITARY))
                if 't-mil-pop-check c: 1' in r[4]]
        self.assertEqual(len(rows), 1)
        self.assertIn('gl-current-soldier-losses', rows[0][3])

    def test_parity_is_a_two_way_signal(self):
        text = source(MILITARY)
        rows = [r for r in rule_blocks(source(MILITARY))
                if '(set-goal gl-parity-army-priority ' in r[4]]
        self.assertEqual(len(rows), 3)
        for row in rows:
            self.assertIn('(game-time > 300)', row[3])
        # Consumer 1: unit-type spend follows the signal.
        train = [r for r in rule_blocks(source(MILITARY))
                 if '(goal train-type MAIN)' in r[3] and '(gold-amount < 500)' in r[3]]
        self.assertEqual(len(train), 1)
        self.assertIn('(goal gl-parity-army-priority 2)', train[0][3])
        # Consumer 2: while hopelessly behind the army floor is raised, and only
        # that value is released again.
        floor = [r for r in rule_blocks(source(MILITARY))
                 if 'gl-parity-army-priority' in r[3] and 'land-attack-requirement' in r[4]]
        raised = [r for r in floor if 'g:= gl-five-percent' in r[4]]
        released = [r for r in floor if 'g:= gl-one-percent' in r[4]]
        self.assertEqual(len(raised), 1)
        self.assertEqual(len(released), 1)
        self.assertIn('(goal gl-parity-army-priority 2)', raised[0][3])
        self.assertIn('g:== gl-five-percent', released[0][3])


if __name__ == '__main__':
    unittest.main()
