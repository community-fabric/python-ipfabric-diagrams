import unittest
from unittest.mock import patch

from ipfabric_diagrams.graph_parameters import Network
from ipfabric_diagrams.graph_settings import NetworkSettings, Overlay
from ipfabric_diagrams.graphs import IPFDiagram


class Models(unittest.TestCase):
    @patch('ipfabric_diagrams.graphs.IPFabricAPI.__init__', return_value=None)
    def setUp(self, mock_ipf) -> None:
        self.graph = IPFDiagram()
        self.graph.snapshots = {'$last': None, '$prev': None}
        self.graph._snapshot_id = '$last'
        self.graph.os_version = 'v4.3.0'

    @patch('ipfabric_diagrams.graphs.IPFDiagram._query')
    def test_diagram_json(self, mock_query):
        mock_query.return_value = {'data': None}
        test = self.graph.diagram_json(Network())
        self.assertEqual(test, {'data': None})

    @patch('ipfabric_diagrams.graphs.IPFDiagram._query')
    def test_diagram_svg(self, mock_query):
        mock_query.return_value = b'test'
        test = self.graph.diagram_svg(Network())
        self.assertEqual(test, b'test')

    @patch('ipfabric_diagrams.graphs.IPFDiagram._query')
    def test_diagram_png(self, mock_query):
        mock_query.return_value = b'test'
        test = self.graph.diagram_png(Network())
        self.assertEqual(test, b'test')

    @patch('ipfabric_diagrams.graphs.IPFabricAPI.post')
    def test_query(self, mock_post):
        mock_post().json.return_value = {'data': None}
        test = self.graph._query({})
        self.assertEqual(test, {'data': None})

    @patch('ipfabric_diagrams.graphs.IPFabricAPI.post')
    def test_query_settings(self, mock_post):
        mock_post().json.return_value = {'data': None}
        test = self.graph._query({}, graph_settings=NetworkSettings())
        self.assertEqual(test, {'data': None})

    @patch('ipfabric_diagrams.graphs.IPFabricAPI.post')
    def test_query_overlay(self, mock_post):
        mock_post().json.return_value = {'data': None}
        test = self.graph._query({}, overlay=Overlay(snapshotToCompare='$last'))
        self.assertEqual(test, {'data': None})

    def test_query_overlay_invalid(self):
        with self.assertRaises(ValueError) as err:
            self.graph._query({}, overlay=Overlay(snapshotToCompare='$lastLocked'))
