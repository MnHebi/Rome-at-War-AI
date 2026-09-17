"""Focused tests for the file-trace correlator's command contracts and window.

Fixtures are synthetic RAW58 records, so these tests check the correlator's
rules (deferred delivery, second boundary, command-specific targets, recipient
categories, ambiguity) without decoding a replay or reading an engine log.
"""
import unittest

from command_boundary_log import POST_INVOCATION_SECONDS, contract, correlations


def frame(player, kind, site, event, seconds, local=(), remote=(), first_record=1):
    """One complete framed observation: header, object rows, tail."""
    rows = [dict(complete=True, player=player, session=1, event=event, site=site,
                 type=1, record=first_record, game_seconds=seconds,
                 values=[kind, len(local), len(remote)])]
    record = first_record + 1
    for index, value in enumerate(local):
        rows.append(dict(complete=True, player=player, session=1, event=event, site=site,
                         type=10, record=record, game_seconds=seconds, values=[index, 1, value]))
        record += 1
    for index, value in enumerate(remote):
        rows.append(dict(complete=True, player=player, session=1, event=event, site=site,
                         type=11, record=record, game_seconds=seconds, values=[index, 1, value]))
        record += 1
    rows.append(dict(complete=True, player=player, session=1, event=event, site=site,
                     type=2, record=record, game_seconds=seconds, values=[kind]))
    return rows


def registry(command, site=77, indirect=False):
    return dict(sites=[dict(id=1, file='fixture.per', line=1,
                            file_commands=[dict(index=0, id=site, command=command, indirect=indirect, args=[])])])


def pre_and_invoked(player=2, site=77, seconds=100, local=(10,), remote=(54321,)):
    records = frame(player, 3, site, event=5, seconds=seconds, local=local, remote=remote, first_record=1)
    start = records[-1]['record'] + 1
    return records + frame(player, 2, site, event=6, seconds=seconds, first_record=start)


def packet(sequence, seconds, action, object_ids=(10,), target_id=-1, order_id=None):
    row = dict(sequence=sequence, milliseconds=seconds * 1000, player_id=2, action=action,
               object_ids=list(object_ids), target_id=target_id)
    if order_id is not None:
        row['order_id'] = order_id
    return row


def rows_for(command, events, **kwargs):
    return list(correlations(pre_and_invoked(**kwargs), events, registry(command)))


class ContractTests(unittest.TestCase):
    def test_contracts_follow_the_command_operands(self):
        cases = {'(up-target-point gl-x action-move -1 stance-no-attack)': 'point',
                 '(up-target-point gl-hull action-garrison -1 stance-no-attack)': 'object-target',
                 '(up-target-point gl-hull action-unload -1 stance-no-attack)': 'object-target',
                 '(up-target-point gl-x action-stop -1 stance-no-attack)': 'point',
                 '(up-reset-unit c: 0)': 'object-target',
                 '(set-goal gl-x 1)': 'state-write',
                 '(up-create-group 0 0 c: g)': 'group-write',
                 '(up-build place-normal gl-no-escrow-state c: house)': 'native-admission'}
        for command, expected in cases.items():
            with self.subTest(command=command):
                self.assertEqual(contract(command), expected)


class CorrelatorTests(unittest.TestCase):
    def test_point_command_is_not_rejected_by_an_unrelated_remote_list(self):
        rows = rows_for('(up-target-point gl-x action-move -1 stance-no-attack)',
                        [packet(7, 100, 'ORDER', target_id=-1)])
        self.assertEqual(rows[0]['contract'], 'point')
        self.assertEqual(rows[0]['status'], 'candidate-not-causation')
        self.assertEqual([c['sequence'] for c in rows[0]['candidates']], [7])
        self.assertTrue(rows[0]['candidates'][0]['exact_recipients'])

    def test_object_target_command_requires_the_traced_target(self):
        unrelated = rows_for('(up-target-point gl-hull action-garrison -1 stance-no-attack)',
                             [packet(7, 100, 'SPECIAL', target_id=99999, order_id=5)])
        self.assertEqual(unrelated[0]['status'], 'unmatched-not-native-proof')
        matched = rows_for('(up-target-point gl-hull action-garrison -1 stance-no-attack)',
                           [packet(7, 100, 'SPECIAL', target_id=54321, order_id=5)])
        self.assertEqual([c['sequence'] for c in matched[0]['candidates']], [7])

    def test_post_invocation_second_is_included_and_bounded(self):
        same = rows_for('(up-target-point gl-x action-move -1 stance-no-attack)',
                        [packet(7, 100, 'ORDER')])
        self.assertEqual(same[0]['candidates'][0]['second_offset'], 0)
        later = rows_for('(up-target-point gl-x action-move -1 stance-no-attack)',
                         [packet(8, 100 + POST_INVOCATION_SECONDS, 'ORDER')])
        self.assertEqual(later[0]['candidates'][0]['second_offset'], POST_INVOCATION_SECONDS)
        too_late = rows_for('(up-target-point gl-x action-move -1 stance-no-attack)',
                            [packet(9, 101 + POST_INVOCATION_SECONDS, 'ORDER')])
        self.assertEqual(too_late[0]['status'], 'unmatched-not-native-proof')
        self.assertEqual(too_late[0]['window_seconds'], [100, 101])

    def test_state_group_and_admission_writes_report_no_expected_packet(self):
        for command, expected in (('(set-goal gl-x 1)', 'state-write'),
                                  ('(up-create-group 0 0 c: g)', 'group-write'),
                                  ('(up-build place-normal gl-no-escrow-state c: house)', 'native-admission')):
            with self.subTest(command=command):
                rows = rows_for(command, [packet(7, 100, 'WORK')])
                self.assertEqual(rows[0]['contract'], expected)
                self.assertEqual(rows[0]['status'], 'no-expected-packet')
                self.assertEqual(rows[0]['candidates'], [])

    def test_missing_recipients_and_ambiguity_stay_explicit(self):
        unknown = rows_for('(up-target-point gl-x action-move -1 stance-no-attack)',
                           [packet(7, 100, 'ORDER')], local=(), remote=())
        self.assertEqual(unknown[0]['status'], 'recipients-unknown')
        ambiguous = rows_for('(up-target-point gl-x action-move -1 stance-no-attack)',
                             [packet(7, 100, 'ORDER'), packet(8, 100, 'MOVE')])
        self.assertEqual(ambiguous[0]['status'], 'ambiguous')
        self.assertEqual([c['sequence'] for c in ambiguous[0]['candidates']], [7, 8])

    def test_subset_recipients_are_not_exact(self):
        rows = rows_for('(up-target-objects 1 action-default -1 stance-aggressive)',
                        [packet(7, 100, 'ORDER', object_ids=(10,), target_id=54321)],
                        local=(10, 11), remote=(54321,))
        self.assertFalse(rows[0]['candidates'][0]['exact_recipients'])


if __name__ == '__main__':
    unittest.main()
