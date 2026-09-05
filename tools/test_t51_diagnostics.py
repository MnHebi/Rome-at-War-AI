"""Structural non-regression checks for the finite T51 runtime observers."""
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


class T51DiagnosticTests(unittest.TestCase):
    def test_generated_sources_are_synchronized(self):
        generated = {}
        for producer in (assault_outputs, expedition_outputs, row_outputs, shipyard_outputs):
            generated.update(producer())
        for name, text in generated.items():
            self.assertEqual(source(name), text, name)

    def test_diagnostic_budgets_are_initialized_once_and_never_replenished(self):
        checks = {
            'rawai-assault-admission.per': [
                *(f'gl-am{i}-combat-diag-left 24' for i in range(1, 4)),
                *(f'gl-am{i}-combat-diag-terminal-left 4' for i in range(1, 4)),
            ],
            'rawai-specialplacement.per': ['gl-sy-life-left 24'],
            'rawai-naval-right-of-way.per': ['gl-row-diag-left 32'],
            'rawai-expedition-admission.per': ['gl-exp-life-left 24'],
            'rawai-military.per': ['gl-mig-diag-left 40', 'gl-mig-diag-writer-left 24'],
        }
        for name, needles in checks.items():
            text = source(name)
            for needle in needles:
                self.assertEqual(text.count(f'(set-goal {needle})'), 1, (name, needle))
            self.assertNotRegex(text, r'up-modify-goal gl-[\w-]*(?:diag-left|life-left|writer-left) c:\+')

    def test_observers_never_gate_command_bearing_rules(self):
        files = ('rawai-assault-missions.per', 'rawai-specialplacement.per',
                 'rawai-naval-right-of-way.per', 'rawai-expedition-admission.per',
                 'rawai-expedition-budget.per', 'rawai-military.per',
                 'rawai-exploration-policy.per')
        commands = ('(up-target-', '(up-build-line ', '(up-modify-group-flag ',
                    '(up-reset-group ', '(up-create-group ')
        budgets = ('diag-left', 'terminal-left', 'life-left', 'writer-left')
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
        # 30-32 are the three exact remote foundation issuance sites.
        for code in (*range(5, 14), *range(20, 33)):
            self.assertRegex(text,
                rf'\(up-chat-data-to-(?:all|self) str-t12-diag-id c: 560\)\s*'
                rf'\(up-chat-data-to-(?:all|self) str-t12-diag-value c: {code}\)', code)
        for building in ('mining-camp', 'lumber-camp', 'mill'):
            self.assertIn(f'(up-build-line gl-migration-build-x gl-migration-build-x c: {building})', text)

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
        # The pre-issue sample is its own observer rule; exhausting the budget
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
