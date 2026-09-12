"""Structural non-regression checks for T52 episode-reserved observers."""
import re
import unittest
from pathlib import Path

from generate_assault_missions import outputs as assault_outputs
from generate_expedition_admission import outputs as expedition_outputs
from generate_naval_right_of_way import outputs as row_outputs
from generate_shipyard_placement import outputs as shipyard_outputs
from test_pre_backlog import source
from validate_naval_doctrine import rule_blocks
from validate_per import validate_file

ROOT = Path(__file__).resolve().parents[1]


class T52DiagnosticTests(unittest.TestCase):
    def test_generated_sources_are_synchronized(self):
        generated = {}
        for producer in (assault_outputs, expedition_outputs, row_outputs, shipyard_outputs):
            generated.update(producer())
        for name, text in generated.items():
            self.assertEqual(source(name), text, name)

    def test_diagnostics_are_armed_by_real_episodes_not_match_lifetime(self):
        joined = '\n'.join(source(name) for name in (
            'rawai-specialplacement.per', 'rawai-naval-right-of-way.per',
            'rawai-expedition-admission.per', 'rawai-expedition-budget.per',
            'rawai-military.per', 'rawai-exploration-policy.per'))
        for obsolete in ('gl-sy-life-left', 'gl-row-diag-left',
                         'gl-exp-life-left', 'gl-mig-diag-writer-left'):
            self.assertNotIn(obsolete, joined)

        shipyard = source('rawai-specialplacement.per')
        self.assertIn('(set-goal gl-sy-diag-admission-left 1)', shipyard)
        self.assertEqual(shipyard.count('(set-goal gl-sy-diag-placement-left 8)'), 4)
        self.assertEqual(shipyard.count('(set-goal gl-sy-diag-foundation-left 2)'), 4)
        self.assertIn('(up-chat-data-to-all str-t12-diag-id c: 545)', shipyard)

        row = source('rawai-naval-right-of-way.per')
        self.assertIn('(up-object-data object-data-id g:!= gl-row-diag-hull)', row)
        for goal, value in (('select', 2), ('stall', 3), ('merchant', 2),
                            ('hold', 4), ('issue', 1)):
            self.assertIn(f'(set-goal gl-row-diag-{goal}-left {value})', row)

        expedition = source('rawai-expedition-admission.per')
        self.assertIn('(up-compare-goal gl-exp-diag-blocker g:!= gl-exp-diag-last-blocker)', expedition)
        self.assertIn('(up-modify-goal gl-exp-diag-last-blocker g:= gl-exp-diag-blocker)', expedition)
        self.assertNotIn('gl-exp-life-', expedition)

        migration = source('rawai-military.per')
        for goal, value in (('stop', 4), ('boarding', 6), ('landing', 4),
                            ('dropsite', 8), ('recovery', 4), ('lifecycle', 16)):
            self.assertIn(f'(set-goal gl-mig-diag-{goal}-left {value})', migration)

    def test_observers_never_gate_command_bearing_rules(self):
        files = ('rawai-assault-missions.per', 'rawai-specialplacement.per',
                 'rawai-naval-right-of-way.per', 'rawai-expedition-admission.per',
                 'rawai-expedition-budget.per', 'rawai-military.per',
                 'rawai-exploration-policy.per')
        commands = ('(up-target-', '(up-build-line ', '(up-modify-group-flag ',
                    '(up-reset-group ', '(up-create-group ')
        budgets = ('diag-left', 'terminal-left', 'life-left', 'writer-left',
                   'diag-admission-left', 'diag-placement-left', 'diag-foundation-left',
                   'diag-select-left', 'diag-stall-left', 'diag-merchant-left',
                   'diag-hold-left', 'diag-issue-left', 'diag-stop-left',
                   'diag-boarding-left', 'diag-landing-left', 'diag-dropsite-left',
                   'diag-recovery-left', 'diag-lifecycle-left')
        for name in files:
            for _start, _end, _block, facts, actions in rule_blocks(source(name)):
                if any(command in actions for command in commands):
                    self.assertFalse(any(budget in facts for budget in budgets),
                                     (name, facts, actions))

    def test_landed_search_diagnostic_is_literal_player_and_bounded(self):
        text = source('rawai-assault-missions.per')
        for slot in range(1, 4):
            for player in range(1, 9):
                self.assertIn(f'(goal gl-am{slot}-enemy {player})', text)
                self.assertIn(f'(up-remove-objects search-remote object-data-player != {player})', text)
            self.assertIn(f'(up-modify-goal gl-am{slot}-combat-diag-left c:- 1)', text)
        self.assertNotIn('(up-get-search-state remote-total)', text)

    def test_migration_command_writer_fingerprints_cover_all_requested_boundaries(self):
        text = source('rawai-military.per') + source('rawai-exploration-policy.per')
        # 5-13 are STOP/default terminal writers; 20-29 cover rendezvous,
        # boarding, unload, builder assignment, retask, release and recall;
        # 30-32 are the three exact remote foundation issuance sites; 33 is
        # the separate preloaded-hull quarantine adoption boundary.
        for code in (*range(5, 14), *range(20, 34)):
            self.assertRegex(text,
                rf'\(up-chat-data-to-(?:all|self) str-t12-diag-id c: 560\)\s*'
                rf'\(up-chat-data-to-(?:all|self) str-t12-diag-value c: {code}\)', code)
        for building in ('mining-camp', 'lumber-camp', 'mill'):
            self.assertIn(f'(up-build-line gl-migration-build-x gl-migration-build-x c: {building})', text)

        expected = {
            **{code: 'stop' for code in range(5, 14)},
            **{code: 'boarding' for code in range(20, 25)},
            25: 'landing', 26: 'dropsite', 27: 'dropsite',
            28: 'recovery', 29: 'recovery',
            30: 'dropsite', 31: 'dropsite', 32: 'dropsite', 33: 'recovery',
        }
        for code, diagnostic_class in expected.items():
            matches = []
            needle = f'(up-chat-data-to-all str-t12-diag-value c: {code})'
            alternate = f'(up-chat-data-to-self str-t12-diag-value c: {code})'
            for _start, _end, _block, facts, actions in (
                    rule_blocks(source('rawai-military.per')) +
                    rule_blocks(source('rawai-exploration-policy.per'))):
                if needle in actions or alternate in actions:
                    matches.append((facts, actions))
            self.assertTrue(matches, code)
            for facts, actions in matches:
                goal = f'gl-mig-diag-{diagnostic_class}-left'
                self.assertIn(goal, facts, code)
                self.assertIn(f'(up-modify-goal {goal} c:- 1)', actions, code)

    def test_migration_admission_snapshot_is_latched_and_reports_every_outer_gate(self):
        text = source('rawai-military.per')
        self.assertEqual(text.count('(set-goal gl-mig-diag-admit-latch 0)'), 2)
        self.assertEqual(text.count('(set-goal gl-mig-diag-admit-latch 1)'), 1)
        for bit in (1, 2, 4, 8, 16, 256):
            self.assertIn(f'(up-modify-goal gl-mig-diag-terminal c:+ {bit})', text)
        for retired in (32, 64, 128):
            self.assertNotIn(f'(up-modify-goal gl-mig-diag-terminal c:+ {retired})', text)
        for code in range(568, 579):
            self.assertIn(f'(up-chat-data-to-all str-t12-diag-id c: {code})', text, code)
        self.assertIn(';T52 class-reserved diagnostic: separate preloaded-hull quarantine adoption path.', text)

    def test_migration_dropsite_lifecycle_keeps_ready_and_failure_evidence(self):
        text = source('rawai-military.per')
        self.assertEqual(text.count('(up-chat-data-to-self str-t12-diag-id c: 579)'), 2)
        self.assertIn('(up-chat-data-to-self str-t12-diag-value c: 2)', text)
        self.assertIn('(up-chat-data-to-self str-t12-diag-value c: 3)', text)
        for goal in ('gl-island-migration-dropsite-id',
                     'gl-island-migration-anchor-id', 'gl-island-migration-zone'):
            self.assertGreaterEqual(text.count(f'(up-chat-data-to-self str-t12-diag-value g: {goal})'), 2)

    def test_right_of_way_diagnostics_cover_rejection_geometry_and_issue_boundary(self):
        text = source('rawai-naval-right-of-way.per')
        # 617-624 identify a sampled rejected priority hull and its exact
        # action/group/destination/reason. 625-630 identify failed holding
        # geometry. 631-637 fingerprint the selected hold immediately before
        # the separate command-bearing rule. Merchant counts expose every
        # operational filter stage (raw, owned/free, safe, same-zone, eligible).
        for code in range(617, 638):
            self.assertIn(f'(up-chat-data-to-all str-t12-diag-id c: {code})', text, code)
        for goal in ('gl-row-diag-merchants', 'gl-row-diag-merchant-owned',
                     'gl-row-diag-merchant-safe', 'gl-row-diag-merchant-zone',
                     'gl-row-diag-merchant-eligible'):
            self.assertIn(f'g: {goal}', text, goal)
        self.assertIn('(set-goal gl-row-diag-hold-reason 1)', text)
        self.assertIn('(set-goal gl-row-diag-hold-reason 5)', text)
        # The pre-issue sample is its own observer rule; exhausting its episode reserve
        # cannot suppress or alter the following merchant move.
        pre_issue = text.index('(up-chat-data-to-all str-t12-diag-id c: 631)')
        command = text.index('(up-target-point gl-row-hold-x action-move -1 stance-no-attack)', pre_issue)
        self.assertLess(pre_issue, command)

    def test_changed_sources_pass_per_validation(self):
        for name in ('rawai-assault-missions.per', 'rawai-assault-admission.per',
                     'rawai-assault-mission-defs.per', 'rawai-specialplacement.per',
                     'rawai-shipyard-defs.per', 'rawai-naval-right-of-way.per',
                     'rawai-naval-row-defs.per', 'rawai-expedition-admission.per',
                     'rawai-expedition-budget.per', 'rawai-expedition-defs.per',
                     'rawai-military.per', 'rawai-exploration-policy.per',
                     'rawai-customconstants.per'):
            self.assertEqual(validate_file(ROOT / name), [], name)


if __name__ == '__main__':
    unittest.main()
