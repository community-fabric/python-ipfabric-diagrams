import importlib.resources
import json
import unittest
from unittest.mock import patch, MagicMock

from ipfabric_diagrams.graphs import IPFDiagram
from ipfabric_diagrams.input_models.graph_parameters import Network, Unicast
from ipfabric_diagrams.input_models.graph_settings import NetworkSettings, Overlay
from ipfabric_diagrams.output_models.graph_result import GraphResult


class Graph(unittest.TestCase):
    @patch("ipfabric_diagrams.graphs.IPFDiagram.__init__", return_value=None)
    def setUp(self, mock_init):
        self.graph = IPFDiagram()
        self.graph.attribute_filters = None
        snapshot = MagicMock()
        snapshot.loaded = True
        snapshot.disabled_graph_cache = None
        self.graph.snapshots = {"$last": snapshot, "$prev": snapshot}
        self.graph._snapshot_id = "$last"

    @patch("ipfabric_diagrams.graphs.IPFDiagram._query")
    def test_diagram_json(self, mock_query):
        mock_query.return_value = {"data": None}
        test = self.graph.diagram_json(Network())
        self.assertEqual(test, {"data": None})

    @patch("ipfabric_diagrams.graphs.IPFDiagram._query")
    def test_diagram_svg(self, mock_query):
        mock_query.return_value = b"test"
        test = self.graph.diagram_svg(Network())
        self.assertEqual(test, b"test")

    @patch("ipfabric_diagrams.graphs.IPFDiagram._query")
    def test_diagram_png(self, mock_query):
        mock_query.return_value = b"test"
        test = self.graph.diagram_png(Network())
        self.assertEqual(test, b"test")

    @patch("ipfabric_diagrams.graphs.IPFabricAPI.post")
    def test_query(self, mock_post):
        mock_post().json.return_value = {"data": None}
        test = self.graph._query({})
        self.assertEqual(test, {"data": None})

    @patch("ipfabric_diagrams.graphs.IPFabricAPI.post")
    def test_query_settings(self, mock_post):
        mock_post().json.return_value = {"data": None}
        test = self.graph._query({}, graph_settings=NetworkSettings())
        self.assertEqual(test, {"data": None})

    @patch("ipfabric_diagrams.graphs.IPFabricAPI.post")
    def test_query_overlay(self, mock_post):
        mock_post().json.return_value = {"data": None}
        test = self.graph._query({}, overlay=Overlay(snapshotToCompare="$last"))
        self.assertEqual(test, {"data": None})

    def test_query_overlay_invalid(self):
        with self.assertRaises(ValueError) as err:
            self.graph._query({}, overlay=Overlay(snapshotToCompare="$lastLocked"))

    @patch("ipfabric_diagrams.graphs.IPFDiagram.diagram_json")
    def test_pathlookup(self, mock_json):
        mock_json.return_value = json.loads(
            importlib.resources.read_text("tests.unittests", "pathlookup.json")
        )
        model = self.graph.diagram_model(Unicast(startingPoint='10.241.1.203', destinationPoint='10.35.253.58'))
        self.assertIsInstance(model, GraphResult)

    @patch("ipfabric_diagrams.graphs.IPFDiagram.diagram_json")
    def test_network(self, mock_json):
        mock_json.return_value = json.loads(
            importlib.resources.read_text("tests.unittests", "network.json")
        )
        model = self.graph.diagram_model(Network())
        self.assertIsInstance(model, GraphResult)
