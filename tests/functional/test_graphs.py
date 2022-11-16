import os
import unittest

from httpx import HTTPStatusError
from ipfabric import IPFClient

from ipfabric_diagrams import IPFDiagram, Network, Host2GW, Unicast

os.environ["IPF_VERIFY"] = "false"

condition = False if os.getenv('IPF_TOKEN', None) and os.getenv('IPF_URL', None) else True


@unittest.skipIf(condition, "IPF_URL and IPF_TOKEN not set")
class MyTestCase(unittest.TestCase):
    def test_site(self):
        ipf = IPFDiagram(timeout=15)
        graph = ipf.diagram_json(Network())
        self.assertIsInstance(graph, dict)

    def test_picture(self):
        ipf = IPFDiagram(timeout=15)
        graph = ipf.diagram_png(Network())
        self.assertIsInstance(graph, bytes)
        graph = ipf.diagram_svg(Network())
        self.assertIsInstance(graph, bytes)

    def test_bad_token(self):
        with self.assertRaises(HTTPStatusError) as err:
            IPFDiagram(token='BAD')

    def test_host2gw(self):
        ipf = IPFDiagram(timeout=15)
        host = IPFClient().fetch('tables/addressing/hosts', columns=["ip"], limit=1)[0]['ip']
        graph = ipf.diagram_json(Host2GW(startingPoint=host))
        self.assertIsInstance(graph, dict)

    def test_unicast(self):
        ipf = IPFDiagram(timeout=15)
        hosts = IPFClient().fetch('tables/addressing/hosts', columns=["ip"], limit=2)
        graph = ipf.diagram_json(Unicast(startingPoint=hosts[0]['ip'], destinationPoint=hosts[1]['ip']))
        self.assertIsInstance(graph, dict)


if __name__ == '__main__':
    unittest.main()
