import ipaddress
import unittest
from unittest.mock import patch

from ipfabric_diagrams.graphs import IPFPath


@unittest.skipIf(True, "skipping tests")
class Models(unittest.TestCase):
    @patch('ipfabric.api.IPFabricAPI')
    def setUp(self, mock_ipf) -> None:
        self.graph = IPFPath()

    def test_style(self):
        self.graph.style = 'png'
        self.assertEqual(self.graph.style, 'png')

    def test_invalid_style(self):
        with self.assertRaises(ValueError) as err:
            self.graph.style = 'bad'

    def test_query(self):
        self.graph.post().json.return_value = dict(test="hello")
        self.graph.post().content = b'Hello'
        self.assertEqual(self.graph._query({}), dict(test="hello"))
        self.graph.style = 'png'
        self.assertEqual(self.graph._query({}), b'Hello')
        self.graph.style = 'svg'
        self.assertEqual(self.graph._query({}), b'Hello')

    @patch('ipfabric_diagrams.graphs.IPFPath._query')
    def test_site(self, query):
        query.return_value = True
        self.assertTrue(self.graph.site('ip', overlay=dict(test=1)))

    @patch('ipfabric_diagrams.graphs.IPFPath.check_subnets')
    @patch('ipfabric_diagrams.graphs.IPFPath._query')
    def test_host_to_gw(self, query, subnets):
        query.return_value = True
        self.assertTrue(self.graph.host_to_gw('ip'))

    def test_check_subnets(self):
        self.assertTrue(self.graph.check_subnets('10.0.0.0/24'))
        self.assertFalse(self.graph.check_subnets('10.0.0.1'))

    def test_check_subnets_failed(self):
        with self.assertRaises(ipaddress.AddressValueError) as err:
            self.graph.check_subnets('bad ip')