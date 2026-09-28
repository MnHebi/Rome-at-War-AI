"""Focused tests for the AIRef command contracts and the file-trace correlator.

Fixtures are synthetic RAW58 records (type 1 header with declared list counts,
selected object and validity; type 10/11 object rows; type 2 tail), so the rules
under test are the correlator's own: recipient/target source per command, empty
versus incomplete inputs, packet families, the labelled post-invocation second,
ambiguity and unsupported contracts. Real-recording spot checks live in the
T61 report; synthetic fixtures alone are not treated as proof about the match.
"""
import tempfile
import unittest
from pathlib import Path

from command_boundary_log import (BEGIN, END, ESCAPE, POST_INVOCATION_SECONDS,
                                  checksum, correlations, decode_logs)
from command_contracts import compatible, describe, packet_families

POINT_MOVE = '(up-target-point gl-x action-move -1 stance-no-attack)'
POINT_STOP = '(up-target-point position-self-x action-stop -1 stance-no-attack)'
POINT_GARRISON = '(up-target-point gl-hull action-garrison -1 stance-no-attack)'
POINT_UNLOAD = '(up-target-point gl-hull action-unload -1 stance-no-attack)'
OBJECT_GARRISON = '(up-target-objects 0 action-garrison -1 stance-no-attack)'
OBJECT_DEFAULT = '(up-target-objects 0 action-default -1 stance-no-attack)'
OBJECT_SELECTED = '(up-target-objects 1 action-default -1 stance-no-attack)'


def frame(player, kind, site, event, seconds, local=(), remote=(), saved=-2, valid=0, first_record=1):
    """One complete framed observation, matching the emitted record layout."""
    rows = [dict(complete=True, player=player, session=1, event=event, site=site, type=1,
                 record=first_record, game_seconds=seconds,
                 values=[kind, len(local), len(remote), saved, valid, 0])]
    record = first_record + 1
    for source, values in ((10, local), (11, remote)):
        for index, value in enumerate(values):
            rows.append(dict(complete=True, player=player, session=1, event=event, site=site,
                             type=source, record=record, game_seconds=seconds, values=[index, 1, value]))
            record += 1
    rows.append(dict(complete=True, player=player, session=1, event=event, site=site, type=2,
                     record=record, game_seconds=seconds, values=[kind]))
    return rows


def registry(command, site=77, indirect=False):
    return dict(sites=[dict(id=1, file='fixture.per', line=1,
                            file_commands=[dict(index=0, id=site, command=command, indirect=indirect, args=[])])])


def rows_for(command, events, declared_local=None, local=(), remote=(), saved=-2, valid=0, **kwargs):
    records = frame(2, 3, 77, 5, 100, local=local, remote=remote, saved=saved, valid=valid, first_record=1)
    if declared_local is not None:
        records[0]['values'][1] = declared_local
    start = records[-1]['record'] + 1
    records += frame(2, 2, 77, 6, 100, first_record=start)
    return list(correlations(records, events, registry(command, **kwargs)))


def packet(sequence, seconds, action, object_ids=(10,), target_id=-1, order_id=None):
    row = dict(sequence=sequence, milliseconds=seconds * 1000, player_id=2, action=action,
               object_ids=list(object_ids), target_id=target_id)
    if order_id is not None:
        row['order_id'] = order_id
    return row


def encode_frame(player, schema, values, record=1, event=5, typ=21, site=0, seconds=100, session=1):
    """One physical token frame; the only place the wire layout is asserted.

    The framing BEGIN is never escaped (framing flag set); a data value equal to
    BEGIN or ESCAPE is. The tail END is bare and a data value equal to END is
    legal, which is why the decoder uses the declared length.
    """
    payload = [BEGIN, schema, session, record, event, typ, site, seconds, len(values), *values]
    tokens = []
    for index, token in enumerate(payload):
        if index and token in (BEGIN, ESCAPE):
            tokens.append(ESCAPE)
        tokens.append(token)
    # The trailer's third token repeats the event id, as the emitted serial does.
    tokens += [len(payload), checksum(payload), event, END]
    return [f'RAW58P{player} {token}\n' for token in tokens]


def decode_frames(lines):
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / 'engine.log'
        path.write_text(''.join(lines), encoding='utf-8')
        return list(decode_logs([path]))


class SchemaCompatibilityTests(unittest.TestCase):
    """T142: schema 59 appends the actor `gather-type` field.

    The 509-515 captures were schema 58 (17-value actor rows). Appending the new
    field must not invalidate them, and the two layouts must not be confused.
    """

    def test_schema_58_and_59_actor_records_both_decode(self):
        old = decode_frames(encode_frame(2, 58, [0, 10, 20, 1] + [-2] * 13))
        self.assertTrue(all(r['complete'] for r in old), old)
        self.assertEqual(len(old[0]['values']), 17)
        new = decode_frames(encode_frame(2, 59, [0, 10, 20, 1] + [-2] * 14))
        self.assertTrue(all(r['complete'] for r in new), new)
        self.assertEqual(len(new[0]['values']), 18)

    def test_wrong_length_for_the_declared_schema_is_rejected(self):
        mismatched = decode_frames(encode_frame(2, 58, [0, 10, 20, 1] + [-2] * 14))
        self.assertEqual([r['errors'] for r in mismatched], [['record-shape']])
        unknown = decode_frames(encode_frame(2, 57, [0, 10, 20, 1] + [-2] * 14))
        self.assertEqual([r['errors'] for r in unknown], [['schema']])


class ContractTests(unittest.TestCase):
    def test_action_contracts_follow_the_reference(self):
        # (command, expected recipient source, expected target source, action family)
        cases = (
            (POINT_MOVE, 'local-list', 'point', {'move', 'order'}),
            (POINT_GARRISON, 'local-list', 'point', {'move', 'order'}),   # documented as action-move
            (POINT_UNLOAD, 'local-list', 'point', {'unload'}),
            (POINT_STOP, 'local-list', 'point', {'stop'}),
            (OBJECT_GARRISON, 'local-list', 'remote-list', {'garrison'}),
            (OBJECT_DEFAULT, 'local-list', 'remote-list', {'work', 'order', 'garrison', 'guard', 'follow', 'move'}),
            (OBJECT_SELECTED, 'local-list', 'selected-object', {'work', 'order', 'garrison', 'guard', 'follow', 'move'}),
        )
        for command, recipients, target, packets in cases:
            with self.subTest(command=command):
                shape = describe(command)
                self.assertEqual((shape['recipients'], shape['target']), (recipients, target))
                self.assertEqual(shape['packets'], packets)

    def test_unload_on_objects_is_action_none_and_unsupported_commands_stay_unclassified(self):
        self.assertEqual(describe('(up-target-objects 0 action-unload -1 stance-no-attack)')['packets'], set())
        self.assertEqual(describe('(up-target-point gl-x action-pack -1 stance-no-attack)')['kind'], 'unclassified')
        self.assertEqual(describe('(some-new-command 1 2)')['kind'], 'unclassified')
        self.assertEqual(describe('(set-goal gl-x 1)')['kind'], 'state-write')
        self.assertEqual(describe('(up-build place-normal gl-no-escrow-state c: house)')['kind'],
                         'native-effect-command')
        self.assertEqual(describe('(up-reset-unit c: 0)')['recipients'], 'type-based')

    def test_packet_families_are_documented_only(self):
        self.assertEqual(packet_families(packet(1, 100, 'SPECIAL', order_id=5)), {'garrison'})
        self.assertEqual(packet_families(packet(2, 100, 'UNGARRISON')), {'unload'})
        self.assertEqual(packet_families(packet(3, 100, 'AI_ORDER', order_id=706)), {'stop'})
        self.assertEqual(packet_families(packet(4, 100, 'AI_ORDER', order_id=705)), set())
        self.assertEqual(packet_families(packet(5, 100, 'STOP')), {'stop'})
        self.assertFalse(compatible(packet(6, 100, 'SPECIAL', target_id=9, order_id=5), POINT_GARRISON))
        self.assertTrue(compatible(packet(7, 100, 'SPECIAL', target_id=9, order_id=5), OBJECT_GARRISON))
        self.assertFalse(compatible(packet(8, 100, 'AI_ORDER', order_id=706), OBJECT_DEFAULT))


class CorrelatorTests(unittest.TestCase):
    def test_point_move_matches_a_move_packet_and_ignores_an_unrelated_remote_list(self):
        rows = rows_for(POINT_MOVE, [packet(7, 100, 'ORDER', target_id=-1)], local=(10,), remote=(54321,))
        self.assertEqual(rows[0]['category'], 'candidate-not-causation')
        self.assertEqual([c['sequence'] for c in rows[0]['candidates']], [7])
        self.assertTrue(rows[0]['candidates'][0]['exact_recipients'])

    def test_point_garrison_is_movement_not_boarding(self):
        rows = rows_for(POINT_GARRISON, [packet(9, 100, 'SPECIAL', target_id=54321, order_id=5)],
                        local=(10,), remote=(54321,))
        self.assertEqual(rows[0]['category'], 'unmatched-not-native-proof')

    def test_point_command_ignores_auxiliary_target_and_unrelated_remote_list(self):
        # An UNGARRISON packet names the released object, not the PER point
        # command's target, and its nonnegative field must not be compared
        # against an unrelated remote search list.
        unload = packet(11, 100, 'UNGARRISON', object_ids=(10,), target_id=99999)
        with_remote = rows_for(POINT_UNLOAD, [unload], local=(10,), remote=(54321,))
        without_remote = rows_for(POINT_UNLOAD, [unload], local=(10,), remote=())
        self.assertEqual([c['sequence'] for c in with_remote[0]['candidates']], [11])
        self.assertEqual([c['sequence'] for c in without_remote[0]['candidates']], [11])
        self.assertEqual(with_remote[0]['category'], without_remote[0]['category'])
        # ... while a genuinely object-directed command keeps the requirement.
        object_mismatch = rows_for(OBJECT_GARRISON,
                                   [packet(12, 100, 'SPECIAL', object_ids=(10,), target_id=99999, order_id=5)],
                                   local=(10,), remote=(54321,))
        self.assertEqual(object_mismatch[0]['category'], 'unmatched-not-native-proof')

    def test_object_garrison_requires_the_traced_target(self):
        wrong = rows_for(OBJECT_GARRISON, [packet(7, 100, 'SPECIAL', target_id=99999, order_id=5)],
                         local=(10,), remote=(54321,))
        self.assertEqual(wrong[0]['category'], 'unmatched-not-native-proof')
        right = rows_for(OBJECT_GARRISON, [packet(7, 100, 'SPECIAL', target_id=54321, order_id=5)],
                         local=(10,), remote=(54321,))
        self.assertEqual([c['sequence'] for c in right[0]['candidates']], [7])

    def test_select_object_option_targets_the_recorded_selected_object(self):
        rows = rows_for(OBJECT_SELECTED, [packet(7, 100, 'WORK', target_id=54321)],
                        local=(10,), remote=(), saved=54321, valid=1)
        self.assertEqual([c['sequence'] for c in rows[0]['candidates']], [7])
        stray = rows_for(OBJECT_SELECTED, [packet(8, 100, 'WORK', target_id=12345)],
                         local=(10,), remote=(), saved=54321, valid=1)
        self.assertEqual(stray[0]['category'], 'unmatched-not-native-proof')

    def test_complete_empty_input_differs_from_missing_rows(self):
        empty = rows_for(OBJECT_GARRISON, [packet(7, 100, 'SPECIAL', target_id=54321, order_id=5)],
                         local=(), remote=(54321,))
        self.assertEqual(empty[0]['category'], 'empty-input-recorded')
        incomplete = rows_for(OBJECT_GARRISON, [packet(7, 100, 'SPECIAL', target_id=54321, order_id=5)],
                              declared_local=3, local=(10,), remote=(54321,))
        self.assertEqual(incomplete[0]['category'], 'incomplete-inputs')

    def test_type_based_and_engine_side_commands_are_classified_not_guessed(self):
        typed = rows_for('(up-reset-unit c: 0)', [packet(7, 100, 'STOP')], local=(10,))
        self.assertEqual(typed[0]['category'], 'type-based-recipients')
        native = rows_for('(up-build place-normal gl-no-escrow-state c: house)', [packet(7, 100, 'BUILD')])
        self.assertEqual(native[0]['category'], 'no-direct-packet-expected')
        unknown = rows_for('(new-command 1)', [packet(7, 100, 'ORDER')])
        self.assertEqual(unknown[0]['category'], 'unsupported-contract')

    def test_post_invocation_second_is_labelled_and_bounded(self):
        same = rows_for(POINT_MOVE, [packet(7, 100, 'ORDER')], local=(10,))
        self.assertEqual(same[0]['candidates'][0]['second_offset'], 0)
        later = rows_for(POINT_MOVE, [packet(8, 100 + POST_INVOCATION_SECONDS, 'ORDER')], local=(10,))
        self.assertEqual(later[0]['candidates'][0]['second_offset'], POST_INVOCATION_SECONDS)
        self.assertEqual(later[0]['window_seconds'], [100, 100 + POST_INVOCATION_SECONDS])
        too_late = rows_for(POINT_MOVE, [packet(9, 101 + POST_INVOCATION_SECONDS, 'ORDER')], local=(10,))
        self.assertEqual(too_late[0]['category'], 'unmatched-not-native-proof')

    def test_ambiguity_and_recipient_subset_are_reported(self):
        rows = rows_for(POINT_MOVE, [packet(7, 100, 'ORDER'), packet(8, 100, 'MOVE')], local=(10,))
        self.assertEqual(rows[0]['category'], 'ambiguous')
        self.assertEqual([c['sequence'] for c in rows[0]['candidates']], [7, 8])
        subset = rows_for(OBJECT_DEFAULT, [packet(7, 100, 'WORK', object_ids=(10,), target_id=54321)],
                          local=(10, 11), remote=(54321,))
        self.assertFalse(subset[0]['candidates'][0]['exact_recipients'])


if __name__ == '__main__':
    unittest.main()
