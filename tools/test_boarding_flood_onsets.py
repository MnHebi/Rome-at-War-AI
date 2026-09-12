import unittest

from tools.audit_boarding_flood_onsets import summarize


def event(ms, seq, action='AI_ORDER', order=706, actors=(10,), player=1, target=-1):
    return dict(milliseconds=ms, sequence=seq, offset=seq * 32,
                action=action, order_id=order, object_ids=list(actors),
                player_id=player, target_id=target)


class FloodOnsetTests(unittest.TestCase):
    def test_shared_packet_and_duplicate_actor(self):
        rows = summarize([event(0, 1, actors=(10, 10, 11)),
                          event(13, 2, actors=(10, 11))], minimum_packets=2)
        self.assertEqual([(r['actor'], r['packets']) for r in rows], [(10, 2), (11, 2)])
        self.assertEqual(rows[0]['first_offset'], 32)

    def test_player_and_subtype_isolation(self):
        rows = summarize([event(0, 1), event(13, 2, player=2),
                          event(26, 3, order=700),
                          event(39, 4, action='SPECIAL')], minimum_packets=2)
        self.assertEqual(rows, [])

    def test_gap_and_minimum(self):
        events = [event(0, 1), event(1000, 2), event(2001, 3)]
        rows = summarize(events, minimum_packets=2)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['last_ms'], 1000)

    def test_stop_timing_uses_packet_sequence(self):
        events = [event(0, 1, 'STOP', None),
                  event(1000, 2, 'STOP', None), event(1000, 3),
                  event(1000, 4, 'STOP', None), event(1013, 5),
                  event(1013, 6, 'STOP', None)]
        row = summarize(list(reversed(events)), minimum_packets=2, window_ms=10)[0]
        self.assertEqual((row['pre_stop'], row['during_stop']), (1, 1))

    def test_nearby_commands_preserve_actor_array_and_target_switch(self):
        events = [event(0, 1), event(13, 2, 'SPECIAL', 5, (10, 11), target=20),
                  event(26, 3, 'SPECIAL', 5, (10, 11), target=20),
                  event(39, 4, 'WORK', None, target=30), event(52, 5)]
        row = summarize(events, minimum_packets=2)[0]
        commands = row['nearby_commands']
        self.assertEqual([c['count'] for c in commands], [2, 1])
        self.assertEqual(commands[0]['actors'], [10, 11])
        self.assertEqual(commands[1]['key'][2], 30)

    def test_invalid_thresholds(self):
        for kwargs in ({'gap_ms': -1}, {'minimum_packets': 0}, {'window_ms': -1}):
            with self.assertRaises(ValueError):
                summarize([], **kwargs)

    def test_changed_selection_is_not_hidden_by_compaction(self):
        events = [event(0, 1), event(13, 2, 'SPECIAL', 5, (10, 11), target=20),
                  event(26, 3, 'SPECIAL', 5, (10,), target=20), event(39, 4)]
        row = summarize(events, minimum_packets=2)[0]
        self.assertEqual([c['actors'] for c in row['nearby_commands']], [[10, 11], [10]])


if __name__ == '__main__':
    unittest.main()
