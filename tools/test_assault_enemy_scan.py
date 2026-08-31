"""Finite hostile-player enumeration must work when the native iterator fails."""
import unittest

from test_assault_screen_fallback import ScreenFallback


class LiteralScan(ScreenFallback):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scanned, self.iterator_calls = [], 0

    def action(self, e, pc=0):
        if e[0] in ('up-find-player', 'up-find-next-player'):
            self.iterator_calls += 1
            self.g[e[-1]] = -1  # reproduce T16 lookup failure if it is called
            return 0
        if e[:3] == ['up-modify-sn', 'sn-focus-player-number', 'g:='] and e[3] == 'gl-assault-fallback-player':
            self.scanned.append(self.g['gl-assault-fallback-player'])
        return super().action(e, pc)


class AssaultEnemyScanTests(unittest.TestCase):
    def test_broken_native_iterator_cannot_reject_live_accepted_manifest(self):
        for cargo in (5, 7, 9, 10):
            for reason in (3, 5, 9):
                m = LiteralScan(cargo=cargo)
                if reason != 3: m.scout(reason)
                self.assertEqual(m.finish(), m.val('TRANSPORT-ROUTE-DEPARTURE-START'))
                self.assertEqual(m.iterator_calls, 0)
                self.assertEqual(m.scanned, [6, 7])
                self.assertEqual(m.g['gl-assault-fallback-player'], 9)

    def test_all_eight_literal_ids_are_checked_once_without_wraparound(self):
        m = LiteralScan(enemies=tuple(range(1, 9)))
        self.assertEqual(m.finish(), m.val('TRANSPORT-ROUTE-DEPARTURE-START'))
        self.assertEqual(m.scanned, list(range(1, 9)))
        self.assertEqual(m.g['gl-assault-fallback-seen'], 8)
        self.assertEqual(m.iterator_calls, 0)

    def test_every_hostile_player_can_veto_at_either_retained_point(self):
        for player in range(1, 9):
            for point in ((50, 50), (90, 90)):
                m = LiteralScan(enemies=tuple(range(1, 9)))
                m.defense(player=player, point=point)
                self.assertEqual(m.finish(), m.val('TRANSPORT-ROUTE-SCREEN-RECALL'))
                self.assertEqual(m.g['gl-assault-fallback-denial'], 2)
                self.assertEqual(m.scanned, list(range(1, player+1)))

    def test_inactive_and_nonhostile_players_are_skipped_not_scanned(self):
        m = LiteralScan(enemies=tuple(range(1, 9)))
        for p in (1, 2, 3): m.players[p]['enemy'] = False
        for p in (4, 5, 8): m.players[p]['active'] = False
        for p in (1, 2, 3, 4, 5, 8):
            m.defense(player=p)
            m.objects[100+p] = m.objects.pop(100)
        self.assertEqual(m.finish(), m.val('TRANSPORT-ROUTE-DEPARTURE-START'))
        self.assertEqual(m.scanned, [6, 7])

    def test_departing_saved_enemy_during_scan_is_still_terminal(self):
        m = LiteralScan(); m.scan_first_enemy()
        m.players[6]['active'] = False
        self.assertEqual(m.finish(), m.val('TRANSPORT-ROUTE-SCREEN-RECALL'))
        self.assertEqual(m.g['gl-assault-diag-subcode'], 413)
        self.assertEqual(m.g['gl-assault-manifest-player'], 6)


if __name__ == '__main__': unittest.main()
