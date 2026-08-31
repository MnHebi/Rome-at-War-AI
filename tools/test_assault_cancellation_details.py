"""Diagnostic-only code-4 split: execute actual PER and preserve T16A1 policy."""
import hashlib
import json
import re
import unittest
from pathlib import Path

from generate_assault_missions import DENIAL_DETAILS
from test_assault_screen_fallback import ScreenFallback
from test_assault_missions import Missions
from test_pre_backlog import source, expressions
from validate_naval_doctrine import rule_blocks


class CancellationDetailsTests(unittest.TestCase):
    def value(self, m, label):
        entries = [value for text, value in m.logs if label in text]
        self.assertEqual(len(entries), 1, (label, entries))
        return entries[0]

    def check_denial(self, m, subcode, enemy=6, global_target=8):
        m.sn['sn-target-player-number'] = global_target
        self.assertEqual(m.finish(), m.val('TRANSPORT-ROUTE-SCREEN-RECALL'))
        self.assertEqual(m.g['gl-assault-fallback-denial'], 4)
        self.assertEqual(self.value(m, 'cancellation subcode:'), subcode)
        self.assertEqual(self.value(m, 'RAW assault saved enemy:'), enemy)
        self.assertEqual(self.value(m, 'cancellation global target:'), global_target)
        self.assertEqual(self.value(m, 'cancellation hull:'), 10)
        self.assertEqual(self.value(m, 'cancellation stage'), 2)
        message, _ = DENIAL_DETAILS[subcode]
        self.value(m, f'deny {subcode}: {message}:')  # reason is readable, not just a number
        logs, commands = list(m.logs), list(m.commands)
        for _ in range(20): m.sweep()
        self.assertEqual(m.logs, logs)
        self.assertEqual(m.commands, commands)

    def test_corrupt_initial_scan_cursor_has_own_code_and_raw_sentinel(self):
        m = ScreenFallback(); m.sweep()
        m.g['gl-assault-fallback-player'] = -1
        self.check_denial(m, 401)
        self.assertEqual(self.value(m, 'iterator player:'), -1)
        self.assertEqual(self.value(m, 'iterator first:'), 1)
        self.assertEqual(self.value(m, 'iterator previous:'), -1)
        self.assertEqual(self.value(m, 'enemies scanned:'), 0)

    def test_corrupt_next_scan_cursor_is_not_an_invalid_saved_enemy(self):
        m = ScreenFallback(); m.scan_first_enemy()
        m.g['gl-assault-fallback-player'] = -1
        self.check_denial(m, 402)
        self.assertEqual(self.value(m, 'iterator player:'), -1)
        self.assertEqual(self.value(m, 'iterator first:'), 1)
        self.assertEqual(self.value(m, 'iterator previous:'), 6)
        self.assertEqual(self.value(m, 'enemies scanned:'), 1)
        self.assertEqual(self.value(m, 'cancellation live gate:'), 1)

    def test_invalid_saved_ids_include_the_actual_value(self):
        for enemy, code in ((-1, 411), (0, 411), (9, 412), (255, 412)):
            m = ScreenFallback(); m.g['gl-assault-manifest-player'] = enemy
            self.check_denial(m, code, enemy=enemy)
            self.assertEqual(self.value(m, 'cancellation checked enemy:'), enemy)

    def test_departed_and_nonhostile_saved_enemies_are_distinct(self):
        for override, code in (({'active': False}, 413), ({'enemy': False}, 414),
                               ({'active': False, 'enemy': False}, 413)):
            m = ScreenFallback(); m.sweep()
            m.players[6].update(override)
            self.check_denial(m, code)
            self.assertEqual(self.value(m, 'cancellation checked enemy:'), 6)
            self.assertEqual(self.value(m, 'cancellation checked enemy failure:'), code)

    def test_all_eight_literal_players_use_the_same_snapshot_contract(self):
        for player in range(1, 9):
            for active, enemy, detail in ((False, False, 413), (False, True, 413),
                                          (True, False, 414), (True, True, 0)):
                m = ScreenFallback()
                m.g['gl-assault-manifest-player'] = player
                m.players[player] = dict(active=active, enemy=enemy, buildings=0)
                m.admission_snapshot()
                self.assertEqual(m.g['gl-assault-diag-checked-enemy'], player)
                self.assertEqual(m.g['gl-assault-diag-enemy-failure'], detail)
                self.assertEqual(m.g['gl-assault-preflight-live'], int(active and enemy))
                self.assertEqual(m.logs, [])  # status checks themselves never chat

    def test_snapshot_mismatch_and_inconsistent_live_gate_are_explicit(self):
        for mismatch, code in ((True, 415), (False, 419)):
            m = ScreenFallback()
            if mismatch: m.players[6]['active'] = False
            m.admission_snapshot()
            m.g['gl-assault-preflight-live'] = 0
            if mismatch: m.g['gl-assault-manifest-player'] = 7
            m.g['gl-transport-route-state'] = m.val('TRANSPORT-ROUTE-UNSCREENED-DECIDE')
            for row in m.rules: m.rule(row)
            self.assertEqual(m.g['gl-transport-route-state'], m.val('TRANSPORT-ROUTE-SCREEN-RECALL'))
            self.assertEqual(self.value(m, 'cancellation subcode:'), code)
            self.assertEqual(self.value(m, 'cancellation checked enemy:'), 6)
            self.assertEqual(self.value(m, 'RAW assault saved enemy:'), 7 if mismatch else 6)
            self.assertEqual(self.value(m, 'cancellation checked enemy failure:'), 413 if mismatch else 0)

    def test_other_denials_do_not_inherit_a_previous_code4_detail(self):
        for override in ({'hp': 0}, {'under_attack': 1}, {'cargo': 1}):
            m = ScreenFallback(); m.g['gl-assault-diag-subcode'] = 413
            m.objects[10].update(override)
            self.assertEqual(m.finish(), m.val('TRANSPORT-ROUTE-SCREEN-RECALL'))
            self.assertEqual(m.g['gl-assault-fallback-denial'], 1)
            self.assertFalse(any('cancellation' in text for text, _ in m.logs))

    def test_load_ready_cancellation_uses_the_same_precise_enemy_reason(self):
        m = Missions(); m.prepare(10)
        m.g['gl-transport-route-state'] = m.val('TRANSPORT-ROUTE-LOAD-READY')
        m.players[6]['active'] = False
        m.admission_snapshot()
        self.assertEqual(self.value(m, 'cancellation subcode:'), 413)
        self.assertEqual(self.value(m, 'cancellation stage'), 1)
        self.assertEqual(self.value(m, 'RAW assault saved enemy:'), 6)
        cancel = next(r for r in rule_blocks(source('rawai-military.per'))
                      if '(goal gl-transport-route-state TRANSPORT-ROUTE-LOAD-READY)' in r[3]
                      and '(goal gl-assault-preflight-live NO)' in r[3])
        self.assertTrue(m.rule(cancel))
        self.assertEqual(m.g['gl-transport-route-state'], m.val('TRANSPORT-ROUTE-RECOVERY-WAIT'))
        logs = list(m.logs)
        for _ in range(20): m.admission_snapshot()
        self.assertEqual(m.logs, logs)

    def test_voyage_exit_log_retains_slot_enemy_not_new_global_enemy(self):
        m = Missions(); m.prepare(10, enemy=6); m.sweep()
        m.logs.clear(); m.sn['sn-target-player-number'] = 8
        m.g['gl-assault-manifest-player'] = 7  # later preparation cannot relabel slot1
        m.players[6]['active'] = False; m.sweep(8)
        self.assertEqual(self.value(m, 'RAW3 slot:'), 1)
        self.assertEqual(self.value(m, 'RAW3 hull:'), 10)
        self.assertEqual(self.value(m, 'RAW assault saved enemy:'), 6)
        self.assertEqual(self.value(m, 'RAW3 event:'), 1)

    def test_unrelated_t16a1_gameplay_predicates_and_actions_are_unchanged(self):
        # Captured before this diagnostic patch. Drop ONLY chats and new diagnostic
        # goal writes; retain all original predicates, action order and state writes.
        expected = {
            'rawai-assault-admission.per': '44e4587711eddcdb865f5706fcb3581c59557231a753eff606ccce7904cede72',
            # T17 deliberately replaces fallback enumeration; dedicated actual-PER
            # scan/safety tests replace only that old diagnostic-only fingerprint.
            # T20 moves the existing distance sample and unchanged cargo-empty
            # handoff before cancellation. Dedicated actual-PER tests prove the
            # old failure/new success; retain all other predicates/actions here.
            'rawai-assault-missions.per': '68eb64739bad9d1c3b8fa89fb362867fb116638aad693d0eaa8ebc5d390cfe1f',
            'rawai-assault-cancel-details.per': hashlib.sha256(b'[]').hexdigest(),
        }
        for name, fingerprint in expected.items():
            rows = []
            for r in rule_blocks(source(name)):
                actions = [e for e in expressions(r[4]) if not e[0].startswith('up-chat') and not
                           (e[0] in ('set-goal', 'up-modify-goal') and e[1].startswith('gl-assault-diag-'))]
                # T19 appends separately tested admission/rotation policy. The
                # original admission predicates/actions must still be identical.
                if name == 'rawai-assault-admission.per' and 'gl-ap-' in r[3]+r[4]: continue
                # T22's independent preparation cooldown does not change the
                # original liveness/cancellation snapshot protected here.
                if name == 'rawai-assault-admission.per' and 'gl-assault-recovery-' in r[3]+r[4]: continue
                # T20's independently tested leg transition adds exactly these
                # resets. Keep the historical fingerprint for every OTHER write,
                # predicate and action order rather than replacing the baseline.
                if name == 'rawai-assault-missions.per':
                    for slot in (1, 2, 3):
                        if ['set-goal', f'gl-am{slot}-state', '2'] in actions:
                            for reset in (['set-goal', f'gl-am{slot}-best', '99999'],
                                          ['set-goal', f'gl-am{slot}-stalls', '0']):
                                self.assertEqual(actions.count(reset), 1)
                                actions.remove(reset)
                if actions: rows.append([expressions(r[3]), actions])
            self.assertEqual(hashlib.sha256(json.dumps(rows, sort_keys=True).encode()).hexdigest(), fingerprint, name)

    def test_diagnostic_goals_have_no_aliases_and_never_control_gameplay(self):
        root = Path(__file__).resolve().parents[1]
        declarations = [(name, int(value)) for path in root.glob('*.per')
                        for name, value in re.findall(r'\(defconst ([\w-]+) (-?\d+)\)', source(path.name))]
        for name, value in declarations:
            if name.startswith('gl-assault-diag-'):
                self.assertEqual([key for key, number in declarations if key.startswith('gl-') and number == value], [name])
                self.assertLessEqual(value, 15999)
        for path in root.glob('*.per'):
            for row in rule_blocks(source(path.name)):
                facts, actions = expressions(row[3]), expressions(row[4])
                if 'gl-assault-diag-' in str(facts):
                    self.assertTrue(all(e[0].startswith('up-chat') or
                        (e[0] in ('set-goal', 'up-modify-goal') and e[1].startswith('gl-assault-diag-'))
                        for e in actions), (path.name, row[0]))


if __name__ == '__main__': unittest.main()
