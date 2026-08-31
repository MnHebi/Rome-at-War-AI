"""Packet/lifecycle tests; these do not simulate native engine tasking."""
import struct
import unittest

from audit_task_ownership import analyze, decode_packet


class OwnershipPacketTests(unittest.TestCase):
    def test_transport_ids_are_not_magnitude_shifted(self):
        for pad in (b"", b"\0"):
            members = [4638, 80000, 169999]
            special = struct.pack("<Iiff4xh2xh2x", 3, 31091, -1, -1, 0, 5)
            special += pad + struct.pack("<3I", *members)
            result = decode_packet("SPECIAL", special, dict(player_id=5, order_id=5, target_id=31091))
            self.assertEqual(result["object_ids"], members)
            unload = struct.pack("<IffiI", 1, 23, 142, -1, 0) + pad + struct.pack("<I", 80000)
            self.assertEqual(decode_packet("UNGARRISON", unload, {})["object_ids"], [80000])

    def test_retreat_contains_exact_members_and_target(self):
        raw = struct.pack("<IffII3I", 4538, 82, 35, 3, 1, 44331, 80000, 90000)
        result = decode_packet("DE_RETREAT", raw, dict(player_id=1))
        self.assertEqual(result["object_ids"], [44331, 80000, 90000])
        self.assertEqual(result["target_id"], 4538)
        with self.assertRaises(ValueError):
            decode_packet("DE_RETREAT", raw[:-1], {})

    def test_ai_order_all_members_and_real_order_offset(self):
        prefix = struct.pack("<IIIIIffff4B", 2, 4638, 0xFFFFFFFF, 0, 706,
                             -1, -1, -1, 1, 1, 255, 1, 0)
        result = decode_packet("AI_ORDER", prefix + struct.pack("<2I", 4638, 30434), dict(player_id=5))
        self.assertEqual(result["object_ids"], [4638, 30434])
        self.assertEqual(result["order_id"], 706)
        self.assertEqual((result["target_id"], result["x"], result["y"]), (-1, -1, -1))

    def test_worker_order_has_exact_target_and_members(self):
        raw = struct.pack("<IffH6x2I", 66155, 207.5, 16.5, 2, 80000, 90000)
        result = decode_packet("WORK", raw, dict(player_id=8))
        self.assertEqual(result["object_ids"], [80000, 90000])
        self.assertEqual(result["target_id"], 66155)


class OwnershipAuditTests(unittest.TestCase):
    def event(self, sequence, milliseconds, action, **fields):
        return dict(sequence=sequence, milliseconds=milliseconds, action=action, **fields)

    def run_window(self, middle, terminal="RAW44B migration full hull: 30"):
        event = self.event
        events = [event(1, 1000, "SPECIAL", player_id=1, target_id=30, order_id=5, object_ids=[40]),
                  event(2, 1000, "CHAT", player=1, message="migration board target: 1")]
        events.extend(middle)
        events.append(event(20, 12000, "CHAT", player=1, message=terminal))
        return analyze(events, {(1, 30)}, {1: "Red"})

    def test_first_overwrite_requires_later_ashore_evidence(self):
        work = self.event(3, 1100, "WORK", player_id=1, target_id=100, object_ids=[40])
        retry = self.event(4, 4000, "SPECIAL", player_id=1, target_id=30, order_id=5, object_ids=[40])
        row = self.run_window([work, retry])["boarding_windows"][0]["passengers"][0]
        self.assertEqual(row["classification"], "overwritten_reserved")
        self.assertEqual(row["first_conflicting_command"]["target_id"], 100)
        self.assertEqual(row["overwrite_prevented_completion"], "not established; full load later")
        uncertain = self.run_window([work])["boarding_windows"][0]["passengers"][0]
        self.assertEqual(uncertain["classification"], "unresolved_conflict_before_terminal")

    def test_success_is_distinct_from_absence_of_evidence(self):
        row = self.run_window([])["boarding_windows"][0]["passengers"][0]
        self.assertEqual(row["classification"], "successful_reserved_corroborated_full_load")
        row = self.run_window([], terminal="RAW44B migration abort empty hull: 30")["boarding_windows"][0]["passengers"][0]
        self.assertEqual(row["classification"], "unresolved")

    def test_deletion_request_does_not_prove_death_or_unavailability(self):
        deletion = self.event(3, 1100, "DELETE", player_id=1, object_ids=[40])
        report = self.run_window([deletion], terminal="RAW44B migration abort empty hull: 30")
        row = report["boarding_windows"][0]["passengers"][0]
        self.assertEqual(row["classification"], "unresolved_requested_deletion")
        self.assertEqual(row["deletion_request"]["action"], "DELETE")
        self.assertEqual(report["aggregate"]["Red"]["died_proven"], 0)
        self.assertEqual(report["aggregate"]["Red"]["genuinely_unavailable_proven"], 0)

    def test_terminal_stop_is_not_an_overwrite(self):
        events = [self.event(21, 12000, "STOP", player_id=1, object_ids=[40])]
        report = self.run_window(events, terminal="RAW44B migration abort empty hull: 30")
        self.assertIsNone(report["boarding_windows"][0]["passengers"][0]["first_conflicting_command"])

    def test_other_player_does_not_overwrite_same_number(self):
        event = self.event(3, 1100, "WORK", player_id=2, target_id=100, object_ids=[40])
        row = self.run_window([event])["boarding_windows"][0]["passengers"][0]
        self.assertIsNone(row["first_conflicting_command"])

    def test_long_pending_task_is_not_split_at_an_invented_timeout(self):
        events = [self.event(1, 1000, "SPECIAL", player_id=1, target_id=30, order_id=5, object_ids=[40]),
                  self.event(2, 1000, "CHAT", player=1, message="migration board target: 1"),
                  self.event(3, 60000, "WORK", player_id=1, target_id=100, object_ids=[40]),
                  self.event(4, 65000, "SPECIAL", player_id=1, target_id=30, order_id=5, object_ids=[40]),
                  self.event(5, 70000, "CHAT", player=1, message="RAW44B migration full hull: 30")]
        report = analyze(events, {(1, 30)}, {1: "Red"})
        self.assertEqual(len(report["boarding_windows"]), 1)
        self.assertEqual(report["boarding_windows"][0]["passengers"][0]["classification"], "overwritten_reserved")

    def test_new_explicit_start_ends_old_ownership_window(self):
        events = [self.event(1, 1000, "SPECIAL", player_id=1, target_id=30, order_id=5, object_ids=[40]),
                  self.event(2, 1000, "CHAT", player=1, message="migration board target: 1"),
                  self.event(3, 20000, "SPECIAL", player_id=1, target_id=30, order_id=5, object_ids=[50]),
                  self.event(4, 20000, "CHAT", player=1, message="migration board target: 1"),
                  self.event(5, 21000, "WORK", player_id=1, target_id=100, object_ids=[40]),
                  self.event(6, 25000, "CHAT", player=1, message="RAW44B migration full hull: 30")]
        report = analyze(events, {(1, 30)}, {1: "Red"})
        self.assertEqual(len(report["boarding_windows"]), 2)
        self.assertIsNone(report["boarding_windows"][0]["passengers"][0]["first_conflicting_command"])

    def test_exact_partial_landing_is_success_evidence(self):
        events = [self.event(1, 1000, "SPECIAL", player_id=1, target_id=30, order_id=5, object_ids=[40]),
                  self.event(2, 1000, "CHAT", player=1, message="attack lift boarding target: 1"),
                  self.event(3, 12000, "CHAT", player=1, message="RAW44B attack load partial hull: 30")]
        evidence = dict(player=1, hull=30, time="00:12",
                        membership_acceptance=dict(exact_boarded_only=True, dispatched=[40]))
        row = analyze(events, {(1, 30)}, {1: "Red"}, (evidence,))["boarding_windows"][0]["passengers"][0]
        self.assertEqual(row["classification"], "successful_reserved_corroborated_partial_landing")

    def test_public_ready_is_hull_specific_without_private_player_chat(self):
        events = [self.event(1, 1000, "SPECIAL", player_id=7, target_id=30, order_id=5, object_ids=[40]),
                  self.event(2, 1100, "CHAT", player=7, message="RAW44C assault ready hull: 31"),
                  self.event(3, 1200, "CHAT", player=7, message="RAW44C assault ready hull: 30")]
        report = analyze(events, {(7, 30), (7, 31)}, {7: 'Blue'})
        window = report['boarding_windows'][0]
        self.assertEqual(window['owner'], 'assault')
        self.assertEqual(window['terminal']['sequence'], 3)
        self.assertEqual(window['passengers'][0]['classification'],
                         'successful_reserved_corroborated_full_load')
        self.assertTrue(any('not a census' in note for note in report['limitations']))


if __name__ == "__main__":
    unittest.main()
