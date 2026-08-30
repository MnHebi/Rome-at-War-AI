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


class NavalSearchTests(unittest.TestCase):
    def test_expansion_has_bounded_clock_and_real_progress_not_command_progress(self):
        rows = list(rule_blocks(source('rawai-naval-siege-watch.per')))
        expand = next(r for r in rows if 'RAW12 siege search radius:' in r[4])
        self.assertIn('gl-naval-search-clock g:>= gl-naval-search-progress', expand[3])
        self.assertIn('gl-naval-search-radius c:< 255', expand[3])
        self.assertIn('gl-naval-search-progress c:+ 120', expand[4])
        factor = int(re.search(r'gl-naval-search-radius c:\* (\d+)', expand[4])[1])
        cap = int(re.search(r'gl-naval-search-radius c:min (\d+)', expand[4])[1])
        radius = 48
        actual = []
        for _ in range(4):
            radius = min(radius * factor, cap)
            actual.append(radius)
        self.assertEqual(actual, [96, 192, 255, 255])
        progress = next(r for r in rows if 'object-data-hitpoints g:<' in r[3])
        self.assertIn('(goal gl-naval-watch-attacking YES)', progress[3])
        self.assertIn('object-data-id g:== gl-naval-watch-target', progress[3])
        commands = [r for r in rule_blocks(source('rawai-military.per'))
                    if '(goal gl-naval-siege-state SIEGE-TARGET-COMMAND)' in r[3]
                    and 'up-target-objects' in r[4]]
        self.assertEqual(len(commands), 2)
        self.assertTrue(all('gl-naval-search-progress' not in r[4] for r in commands))

    def test_enemy_iteration_rebuilds_before_consuming_search(self):
        text = source('rawai-military.per')
        rows = list(rule_blocks(text))
        scan = next(r for r in rows if '(goal gl-naval-siege-state SIEGE-TARGET-SEARCH)' in r[3])
        self.assertIn('gl-naval-search-sea-radius', scan[4])
        self.assertIn('up-full-reset-search', scan[4])
        consumers = [r for r in rows if '(goal gl-naval-siege-state SIEGE-TARGET-FIND-STRUCTURE)' in r[3]]
        self.assertTrue(all(scan[0] < r[0] for r in consumers))
        self.assertIn('up-find-next-player enemy find-ordered gl-naval-siege-player', text)
        self.assertIn('gl-naval-siege-player g:== gl-naval-search-first-player', text)

    def test_cross_sweep_command_revalidates_target_and_owned_family(self):
        text = source('rawai-military.per')
        rows = list(rule_blocks(text))
        rebuild = next(r for r in rows if '(goal gl-naval-siege-state SIEGE-TARGET-COMMAND)' in r[3]
                       and 'up-add-object-by-id search-remote g: gl-naval-siege-target-id' in r[4])
        self.assertIn('object-data-player g:!= gl-naval-siege-player', rebuild[4])
        self.assertIn('object-data-group-flag != juggernaut-bombardment-group', rebuild[4])
        self.assertIn('object-data-map-zone-id g:!= gl-naval-siege-zone', rebuild[4])
        for r in rows:
            if '(goal gl-naval-siege-state SIEGE-TARGET-COMMAND)' in r[3] and 'up-target-objects' in r[4]:
                self.assertLess(rebuild[0], r[0])
                self.assertIn('object-data-id g:== gl-naval-siege-target-id', r[3])


class CommandCounterTests(unittest.TestCase):
    def test_every_explicit_stop_or_scout_reset_has_one_counter(self):
        codes = []
        for path in ROOT.glob('*.per'):
            for row in rule_blocks(path.read_text(encoding='utf-8-sig')):
                if 'action-stop' in row[4] or '(up-reset-scouts)' in row[4]:
                    found = re.findall(r'up-modify-goal gl-command-counter-(\d+) c:\+ 1', row[4])
                    self.assertEqual(len(found), 1, path.name)
                    codes.extend(int(c) for c in found)
        self.assertEqual(sorted(codes), list(range(1, 25)))
        self.assertIn('up-modify-goal gl-command-counter-23 c:+ 1', source('rawai-severe-defense.per'))

    def test_counter_reports_are_nonzero_and_minute_bounded(self):
        text = source('rawai-command-counters.per')
        reports = [r for r in rule_blocks(text) if 'up-chat-data-to-all' in r[4]]
        self.assertEqual(len(reports), 26)
        for row in reports:
            self.assertIn('gl-command-counter-clock g:>= gl-command-counter-next', row[3])
            self.assertIn('c:> 0', row[3])
            self.assertRegex(row[4], r'\(set-goal gl-command-counter-\d+ 0\)')
        self.assertIn('(up-modify-goal gl-command-counter-next c:+ 60)', text)
        self.assertNotRegex(text, r'up-(?:target|find|reset|set-group)')

    def test_counter_generation_is_synchronized(self):
        from instrument_command_counters import render
        for name, expected in render().items():
            self.assertEqual(source(name), expected, name)
        text = source('rawai-native-attack-ownership.per')
        self.assertEqual(text.count('up-modify-goal gl-command-counter-90 c:+ 1'), 1)
        self.assertEqual(text.count('up-modify-goal gl-command-counter-91 c:+ 1'), 17)


class HelpCooldownTests(unittest.TestCase):
    def test_each_help_request_starts_a_full_cooldown(self):
        requests = [r for r in rule_blocks(source('rawai-diplomacy.per'))
                    if '(chat-to-allies "48 ' in r[4]]
        self.assertEqual(len(requests), 2)
        for row in requests:
            self.assertIn('(goal dont-spam-taunts NO)', row[3])
            self.assertIn('(set-goal dont-spam-taunts YES)', row[4])
            self.assertIn('(enable-timer t-taunt-spam 120)', row[4])


class FlareDeletionTests(unittest.TestCase):
    def test_small_radius_nearest_one_and_no_candidate_fallback(self):
        text = source('rawai-tauntcommands.per')
        row = next(r for r in rule_blocks(text) if 'up-find-player-flare any-ally gl-flared-delete-x' in r[4])
        limit = int(re.search(r'\(up-filter-distance c: -1 c: (\d+)\)', row[4])[1])
        self.assertEqual(limit, 2)
        self.assertIn('(up-clean-search search-local object-data-distance search-order-asc)', row[4])
        self.assertIn('(up-remove-objects search-local object-data-index >= 1)', row[4])
        for distances, expected in (([1, 3, 5], [1]), ([3, 4, 6], []), ([2, 2], [2])):
            self.assertEqual(sorted(d for d in distances if d <= limit)[:1], expected)
        failure = next(r for r in rule_blocks(text) if 'taunt 69 no structure candidates:' in r[4])
        self.assertNotIn('action-delete', failure[4])


if __name__ == '__main__':
    unittest.main()
