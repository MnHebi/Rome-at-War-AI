import unittest
from analyze_shipyard_sites import rejection_records, classify_point


class ShipyardSiteAnalysisTests(unittest.TestCase):
    def test_interleaved_players_do_not_share_coordinates(self):
        chats=[]
        for key, values in [(545,(64,65)),(536,(10,20)),(537,(11,21)),(538,(100,200)),(540,(0,1))]:
            for p in (1,2): chats.append(dict(player=p,time='12:00',message=f'RAW12 diag id: {key}'))
            for p in (1,2): chats.append(dict(player=p,time='12:00',message=f'RAW12 diag value: {values[p-1]}'))
        a,b=rejection_records(chats)
        self.assertEqual((a['x'],a['y'],a['anchor']),(10,11,100))
        self.assertEqual((b['x'],b['y'],b['anchor']),(20,21,200))

    def test_incomplete_record_is_not_a_site(self):
        chats=[dict(player=1,time='00:00',message=m) for m in
               ['RAW12 diag id: 545','RAW12 diag value: 64','RAW12 diag id: 540','RAW12 diag value: 1']]
        self.assertEqual(rejection_records(chats),[])

    def test_grid_axes_and_no_buildability_claim(self):
        tiles=[(23,1)]*49
        tiles[3*7+2]=(0,1)
        self.assertEqual(classify_point(2,3,7,tiles)['spatial_class'],'land-center')
        self.assertEqual(classify_point(6,3,7,tiles)['spatial_class'],'water-without-nearby-shore')
        self.assertEqual(classify_point(3,3,7,tiles)['spatial_class'],'coastal-or-mixed-unresolved')
        self.assertEqual(classify_point(-1,3,7,tiles)['spatial_class'],'outside-map')
