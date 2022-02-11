import unittest

from ipfabric_diagrams.input_models.graph_settings import *


class GraphSettingTest(unittest.TestCase):
    def test_style(self):
        s = Style(color='red').style_settings('v4.3')
        self.assertEqual(s, {'color': '#f00', 'pattern': 'solid', 'thicknessThresholds': [2, 4, 8]})

    def test_style_failed(self):
        with self.assertRaises(ValueError) as err:
            Style(color='red', pattern='bad')

    def test_settings(self):
        s = Setting(name='Test', style=Style(color='red'), type='edge').base_settings('v4.3')
        self.assertEqual(s, {'name': 'Test', 'visible': True, 'grouped': True, 'style':
            {'color': '#f00', 'pattern': 'solid', 'thicknessThresholds': [2, 4, 8]}, 'type': 'edge'})

    def test_edge_setting(self):
        e = EdgeSettings(name='Test', style=Style(color='red'), type='edge').settings('v4.3')
        e.pop('id', None)
        self.assertEqual(e, {'name': 'Test', 'visible': True, 'grouped': True, 'style':
            {'color': '#f00', 'pattern': 'solid', 'thicknessThresholds': [2, 4, 8]},
                             'type': 'edge', 'labels': ['protocols']})

    def test_group_setting(self):
        g = GroupSettings(name='Test', style=Style(color='red'), type='group', label='Label',
                          children=[EdgeSettings(name='Test2', style=Style(color='red'), type='edge')]).settings('v4.3')
        g['children'][0].pop('id', None)
        self.assertEqual(g, {'name': 'Test', 'visible': True, 'grouped': True, 'style':
            {'color': '#f00', 'pattern': 'solid', 'thicknessThresholds': [2, 4, 8]}, 'type': 'group', 'label': 'Label',
                                              'children': [{'name': 'Test2', 'visible': True, 'grouped': True,
                                                            'style': {'color': '#f00', 'pattern': 'solid',
                                                                      'thicknessThresholds': [2, 4, 8]},
                                                            'type': 'edge', 'labels': ['protocols']}]})

    def test_pathlookup(self):
        self.assertEqual(vars(PathLookup(ignoredTopics=['ACL'])),
                         {'ignoredTopics': ['ACL'], 'colorDetectedLoops': True})

    def test_pathlookup_failed(self):
        with self.assertRaises(ValueError) as err:
            PathLookup(ignoredTopics=['bad'])

    def test_graph_settings(self):
        g = GraphSettings(edges=[EdgeSettings(name='Test', style=Style(color='red'), type='edge')],
                          pathLookup=PathLookup()).settings('v4.3')
        g['edges'][0].pop('id', None)
        self.assertEqual(g, {'edges': [{'name': 'Test', 'visible': True, 'grouped': True,
                                                         'style': {'color': '#f00', 'pattern': 'solid',
                                                                   'thicknessThresholds': [2, 4, 8]},
                                                         'type': 'edge', 'labels': ['protocols']}],
                                              'hiddenDeviceTypes': [], 'pathLookup':
                                                  {'ignoredTopics': [], 'colorDetectedLoops': True}})

    def test_graph_settings_failed(self):
        with self.assertRaises(ValueError) as err:
            GraphSettings(edges=[EdgeSettings(name='Test', style=Style(color='red'), type='edge')],
                          hiddenDeviceTypes=['bad'])

    def test_network_settings_hide_protocol(self):
        n = NetworkSettings()
        is_true = n.hide_protocol('xdp')
        self.assertFalse(n.settings('v4.3')['edges'][0]['children'][0]['visible'])
        self.assertTrue(is_true)

    def test_network_settings_hide_protocol_failed(self):
        n = NetworkSettings()
        with self.assertRaises(KeyError) as err:
           n.hide_protocol('bad_proto')

    def test_network_settings_ungroup_protocol(self):
        n = NetworkSettings()
        is_true = n.ungroup_protocol('xdp')
        n_settings = n.settings('v4.3')
        self.assertFalse(n_settings['edges'][0]['grouped'])
        self.assertFalse(n_settings['edges'][0]['children'][0]['grouped'])
        self.assertTrue(is_true)

    def test_network_settings_hide_group(self):
        n = NetworkSettings()
        is_true = n.hide_group('Layer 1')
        self.assertFalse(n.settings('v4.3')['edges'][0]['visible'])
        self.assertTrue(is_true)

    def test_network_settings_ungroup_group(self):
        n = NetworkSettings()
        is_true = n.ungroup_group('Layer 1')
        n_settings = n.settings('v4.3')
        self.assertFalse(n_settings['edges'][0]['grouped'])
        self.assertTrue(is_true)

    def test_network_settings_failed(self):
        n = NetworkSettings()
        with self.assertRaises(KeyError) as err:
            n.hide_group('Layer 7')
        with self.assertRaises(KeyError) as err:
            n.ungroup_group('Layer 7')

    def test_pathlookup_settings(self):
        self.assertIsInstance(PathLookupSettings(), PathLookupSettings)

    def test_overlay_snapshot(self):
        o = Overlay(snapshotToCompare='$prev').overlay('v4.3')
        self.assertEqual(o, {'type': 'compare', 'snapshotToCompare': '$prev'})

    def test_overlay_snapshot_id(self):
        o = Overlay(snapshotToCompare='6cf80812-18fa-4e99-9edc-a6143fab2876').overlay('v4.3')
        self.assertEqual(o, {'type': 'compare', 'snapshotToCompare': '6cf80812-18fa-4e99-9edc-a6143fab2876'})

    def test_overlay_snapshot_failed(self):
        with self.assertRaises(ValueError) as err:
            Overlay(snapshotToCompare='hello')

    def test_overlay_intent(self):
        o = Overlay(intentRuleId='nonRedundantEdges').overlay('v4.3')
        self.assertEqual(o, {'type': 'intent', 'intentRuleId': 'nonRedundantEdges'})

    def test_overlay_intent_id(self):
        o = Overlay(intentRuleId=1).overlay('v4.3')
        self.assertEqual(o, {'type': 'intent', 'intentRuleId': '1'})

    def test_overlay_intent_failed(self):
        with self.assertRaises(ValueError) as err:
            Overlay(intentRuleId='hello')
