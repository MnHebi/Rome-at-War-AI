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
            # T22 intentionally retains landed combat ownership and gives it
            # bounded continuation. Reviewed against the immutable T21 payload;
            # test_landed_assault + voyage fixtures protect the new contract.
            'rawai-assault-missions.per': '2948d22ca2a9c2d51b1a201ed45135e675eeb0190b2c8fdd06b96ded8ebc0614',
            'rawai-assault-cancel-details.per': hashlib.sha256(b'[]').hexdigest(),
        }
        for name, fingerprint in expected.items():
            rows = []
            normalized_trade_cogs = 0
            normalized_landed_anchors = 0
            normalized_landed_commands = 0
            normalized_landed_latches = 0
            normalized_landed_target_classes = 0
            normalized_landed_settle_waits = 0
            normalized_landed_combat_delays = 0
            for r in rule_blocks(source(name)):
                facts = expressions(r[3])
                actions = [e for e in expressions(r[4]) if not e[0].startswith('up-chat') and not
                           (e[0] in ('set-goal', 'up-modify-goal') and e[1].startswith('gl-assault-diag-'))]
                # T19 appends separately tested admission/rotation policy. The
                # original admission predicates/actions must still be identical.
                if name == 'rawai-assault-admission.per' and 'gl-ap-' in r[3]+r[4]: continue
                # T22's independent preparation cooldown does not change the
                # original liveness/cancellation snapshot protected here.
                if name == 'rawai-assault-admission.per' and 'gl-assault-recovery-' in r[3]+r[4]: continue
                # T26's transition-only upstream admission observer adds one
                # initialization rule. Its dedicated tests prove that these
                # goals only drive bounded chat output; omit that whole new
                # rule while retaining the immutable gameplay fingerprint.
                if (name == 'rawai-assault-admission.per' and
                        'gl-assault-admission-diag-' in r[4]):
                    continue
                # T20's independently tested leg transition adds exactly these
                # resets. Keep the historical fingerprint for every OTHER write,
                # predicate and action order rather than replacing the baseline.
                if name == 'rawai-assault-missions.per':
                    # T39 gives newly unloaded passengers one engine sample to
                    # become visible before rebuilding the landed group, then
                    # starts the first combat sample from that handoff. Its
                    # dedicated fixture protects the timing. Strip only those
                    # private deadlines to retain the older gameplay fingerprint.
                    for mission_slot in (1, 2, 3):
                        next_goal = f'gl-am{mission_slot}-next'
                        if ['set-goal', f'gl-am{mission_slot}-state', '14'] in actions:
                            for deadline in (
                                    ['up-modify-goal', next_goal, 'g:=',
                                     'gl-assault-mission-clock'],
                                    ['up-modify-goal', next_goal, 'c:+', '8']):
                                self.assertIn(deadline, actions)
                                actions.remove(deadline)
                            normalized_landed_settle_waits += 1
                        if ['goal', f'gl-am{mission_slot}-state', '14'] in facts:
                            wait = ['up-compare-goal', 'gl-assault-mission-clock',
                                    'g:>=', next_goal]
                            self.assertIn(wait, facts)
                            facts.remove(wait)
                            for deadline in (
                                    ['up-modify-goal', next_goal, 'g:=',
                                     'gl-assault-mission-clock'],
                                    ['up-modify-goal', next_goal, 'c:+', '16']):
                                self.assertIn(deadline, actions)
                                actions.remove(deadline)
                            normalized_landed_combat_delays += 1
                    # T26's independently tested congestion fix adds the idle
                    # Trade Cog class to exactly two blocker searches per slot.
                    # Remove only those six added selectors before comparing
                    # every older mission predicate/action with T16A1.
                    for e in actions[:]:
                        if e == ['up-find-local', 'c:', 'trade-cog-class', 'c:', '20']:
                            actions.remove(e)
                            normalized_trade_cogs += 1
                    # T27 deliberately recovers landed mission members whose
                    # stale movement or under-attack state previously excluded
                    # them from combat. Its dedicated landed-assault fixtures
                    # protect that contract. Normalize only that exact delta
                    # before retaining the immutable T16A1 gameplay fingerprint.
                    slot = None
                    sample = None
                    for e in facts:
                        if (e[0] == 'goal' and
                                re.fullmatch(r'gl-am[123]-sample', e[1])):
                            slot = int(re.search(r'gl-am([123])-sample', e[1]).group(1))
                            sample = e[2]
                            break

                    if slot is not None and sample == '6':
                        reset = ['set-goal', f'gl-am{slot}-combat-target', '-1']
                        if reset in actions:
                            zone = ['up-remove-objects', 'search-local',
                                    'object-data-map-zone-id', 'g:!=',
                                    f'gl-am{slot}-target-zone']
                            self.assertIn(zone, actions)
                            pos = actions.index(zone) + 1
                            actions[pos:pos] = [
                                ['up-remove-objects', 'search-local',
                                 'object-data-idling', '!=', '1'],
                                ['up-remove-objects', 'search-local',
                                 'object-data-under-attack', '>', '0'],
                            ]
                            normalized_landed_anchors += 1

                    if slot is not None and sample == '7':
                        # Remove only the newly supported hostile land-combat
                        # classes from target-search rules. Buildings/villagers
                        # remain and therefore reconstruct the older search.
                        if (['goal', f'gl-am{slot}-combat-target', '-1'] in facts and
                                ['player-in-game', 'focus-player'] in facts and
                                ['stance-toward', 'focus-player', 'enemy'] in facts):
                            added_classes = {
                                'scout-cavalry-class',
                                'cavalry-archer-class',
                                'cavalry-class',
                                'infantry-class',
                                'archery-class',
                                'siege-weapon-class',
                                'tower-class',
                            }
                            for e in actions[:]:
                                if (len(e) >= 3 and e[0] == 'up-find-remote' and
                                        e[2] in added_classes):
                                    actions.remove(e)
                                    normalized_landed_target_classes += 1

                        # T27 replaces "idle and not under attack" with
                        # "not already attacking" when commanding an acquired
                        # hostile. Restore the old pair only for fingerprinting.
                        attack_guard = [
                            'up-remove-objects', 'search-local',
                            'object-data-action', '==', 'actionid-attack'
                        ]
                        if attack_guard in actions:
                            pos = actions.index(attack_guard)
                            actions[pos:pos + 1] = [
                                ['up-remove-objects', 'search-local',
                                 'object-data-idling', '!=', '1'],
                                ['up-remove-objects', 'search-local',
                                 'object-data-under-attack', '>', '0'],
                            ]
                            normalized_landed_commands += 1

                        # T32 closes a landed object-command sample immediately
                        # in PER state. Remove only that post-issue latch while
                        # reconstructing the immutable T16A1 payload.
                        latch = ['set-goal', f'gl-am{slot}-sample', '10']
                        if latch in actions:
                            actions.remove(latch)
                            normalized_landed_latches += 1

                    if slot is not None and sample == '10':
                        # T32 moves the existing third-try failed-target update
                        # behind the post-issue latch. Restore its old sample-7
                        # predicate for historical fingerprinting.
                        failed = ['up-modify-goal', f'gl-am{slot}-combat-failed',
                                  'g:=', f'gl-am{slot}-combat-target']
                        if failed in actions:
                            for e in facts:
                                if (e[0] == 'goal' and
                                        e[1] == f'gl-am{slot}-sample'):
                                    e[2] = '7'
                                    break

                    # T25 deliberately replaces the old four-miss release with
                    # a separately tested twelve-point continuation probe. Strip
                    # only that new state machine here so this historical guard
                    # still fingerprints every unrelated mission predicate and
                    # action against the immutable T16A1 baseline.
                    if any(e[0] == 'goal' and re.fullmatch(r'gl-am[123]-sample', e[1]) and
                           e[2] in ('8', '9') for e in facts):
                        continue
                    for e in actions[:]:
                        if (e[0] == 'set-goal' and re.fullmatch(r'gl-am[123]-sample', e[1]) and
                                e[2] == '8'):
                            actions.remove(e)
                    for index, e in enumerate(facts):
                        if (e[0] == 'up-compare-goal' and
                                re.fullmatch(r'gl-am[123]-combat-misses', e[1]) and
                                e[2:] == ['c:>=', '13']):
                            e[-1] = '4'
                            facts.insert(index, ['goal', e[1].replace('combat-misses', 'sample'), '7'])
                            break
                    for slot in (1, 2, 3):
                        if ['set-goal', f'gl-am{slot}-state', '2'] in actions:
                            for reset in (['set-goal', f'gl-am{slot}-best', '99999'],
                                          ['set-goal', f'gl-am{slot}-stalls', '0']):
                                self.assertEqual(actions.count(reset), 1)
                                actions.remove(reset)
                if actions: rows.append([facts, actions])
            if name == 'rawai-assault-missions.per':
                self.assertEqual(normalized_trade_cogs, 6)
                self.assertEqual(normalized_landed_anchors, 3)
                self.assertEqual(normalized_landed_commands, 3)
                self.assertEqual(normalized_landed_latches, 3)
                self.assertEqual(normalized_landed_target_classes, 189)
                self.assertEqual(normalized_landed_settle_waits, 3)
                self.assertEqual(normalized_landed_combat_delays, 3)
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
