import os
import unittest

from ipfabric import IPFClient
from pkg_resources import parse_version

condition = False if os.getenv('IPF_TOKEN', None) and os.getenv('IPF_URL', None) else True


@unittest.skipIf(condition, "IPF_URL and IPF_TOKEN not set")
class MyTestCase(unittest.TestCase):
    def test_site(self):
        ipf = IPFClient()
        if parse_version(ipf.os_version) < parse_version("4.3"):
            self.skipTest('IP Fabric version under 4.3')
        graph = ipf.graphs.site('$main')
        self.assertIsInstance(graph, dict)

    def test_picture(self):
        ipf = IPFClient()
        if parse_version(ipf.os_version) < parse_version("4.3"):
            self.skipTest('IP Fabric version under 4.3')
        ipf.graphs.style = 'png'
        graph = ipf.graphs.site('$main')
        self.assertIsInstance(graph, bytes)
        ipf.graphs.style = 'svg'
        graph = ipf.graphs.site('$main')
        self.assertIsInstance(graph, bytes)

    def test_h2gw(self):
        with self.assertRaises(ConnectionRefusedError) as err:
            IPFClient(token='BAD')

    def test_inventory(self):
        ipf = IPFClient()
        if parse_version(ipf.os_version) < parse_version("4.3"):
            self.skipTest('IP Fabric version under 4.3')
        host = ipf.fetch('tables/addressing/hosts', columns=["ip"], limit=1)[0]['ip']
        graph = ipf.graphs.host_to_gw(host)
        self.assertIsInstance(graph, dict)


if __name__ == '__main__':
    unittest.main()
