import unittest

from ipfabric_diagrams.graph_parameters import *
from ipfabric_diagrams.icmp import *


class GraphParam(unittest.TestCase):
    def test_icmp(self):
        icmp = ICMP(type=1, code=0)
        self.assertIsInstance(icmp, ICMP)

    def test_icmp_type(self):
        self.assertIsInstance(NEED_AUTHORIZATION, ICMP)

    def test_entry_point(self):
        ep = EntryPoint(sn="SERIAL", iface="eth0")
        self.assertIsInstance(ep, EntryPoint)

    def test_algorithm(self):
        alg = Algorithm(vrf="mgmt")
        param = alg.algorithm_parameters("v4.3.0")
        self.assertEqual(param, {"type": "automatic", "vrf": "mgmt"})

    def test_algorithm_entry(self):
        alg = Algorithm(entryPoints=[EntryPoint(sn="SERIAL", iface="eth0")])
        param = alg.algorithm_parameters("v4.3.0")
        self.assertEqual(param, {"type": "userDefined", "entryPoints": [{"sn": "SERIAL", "iface": "eth0"}]})

    def test_pathlookup(self):
        bp = PathLookup(protocol="tcp", tcpFlags=["syn"], dstPorts="80,443").base_parameters("v4.3")
        self.assertEqual(
            bp,
            {
                "type": "pathLookup",
                "groupBy": "siteName",
                "protocol": "tcp",
                "ttl": 128,
                "fragmentOffset": 0,
                "securedPath": True,
                "srcRegions": ".*",
                "dstRegions": ".*",
                "l4Options": {"srcPorts": "1024-65535", "dstPorts": "80,443", "flags": ["syn"]},
                "otherOptions": {"applications": ".*", "tracked": False},
                "firstHopAlgorithm": {"type": "automatic"},
            },
        )

    def test_pathlookup_validators(self):
        with self.assertRaises(ValueError) as err:
            PathLookup(srcPorts="hello")
        with self.assertRaises(ValueError) as err:
            PathLookup(protocol="test")
        with self.assertRaises(ValueError) as err:
            PathLookup(tcpFlags=["bad"])

    def test_pathlookup_l4(self):
        pl = PathLookup(protocol="udp")
        self.assertEqual(pl._l4_options(), {"srcPorts": "1024-65535", "dstPorts": "80,443"})
        pl.protocol = "icmp"
        self.assertEqual(pl._l4_options(), {"type": 0, "code": 0})

    def test_multicast(self):
        m = Multicast(source="1.1.1.1", group="2.2.2.2", receiver="3.3.3.3").parameters("v4.3")
        self.assertEqual(
            m,
            {
                "type": "pathLookup",
                "groupBy": "siteName",
                "protocol": "tcp",
                "ttl": 128,
                "fragmentOffset": 0,
                "securedPath": True,
                "srcRegions": ".*",
                "dstRegions": ".*",
                "l4Options": {"srcPorts": "1024-65535", "dstPorts": "80,443", "flags": []},
                "otherOptions": {"applications": ".*", "tracked": False},
                "firstHopAlgorithm": {"type": "automatic"},
                "pathLookupType": "multicast",
                "group": "2.2.2.2",
                "source": "1.1.1.1",
                "receiver": "3.3.3.3",
            },
        )

    def test_multicast_failed(self):
        with self.assertRaises(ValueError) as err:
            Multicast(source="1.1.1.1", group="2.2.2.2", receiver="3.3.3.3/24")

    def test_unicast(self):
        u = Unicast(startingPoint="1.1.1.1", destinationPoint="2.2.2.2").parameters("v4.3")
        self.assertEqual(
            u,
            {
                "type": "pathLookup",
                "groupBy": "siteName",
                "protocol": "tcp",
                "ttl": 128,
                "fragmentOffset": 0,
                "securedPath": True,
                "srcRegions": ".*",
                "dstRegions": ".*",
                "l4Options": {"srcPorts": "1024-65535", "dstPorts": "80,443", "flags": []},
                "otherOptions": {"applications": ".*", "tracked": False},
                "firstHopAlgorithm": {"type": "automatic"},
                "pathLookupType": "unicast",
                "networkMode": False,
                "startingPoint": "1.1.1.1/32",
                "destinationPoint": "2.2.2.2/32",
            },
        )

    def test_unicast_failed(self):
        with self.assertRaises(ValueError) as err:
            Unicast(startingPoint="1.1.1.1", destinationPoint="hello")

    def test_host2gw(self):
        h = Host2GW(startingPoint="1.1.1.1", vrf="mgmt").parameters("v4.3")
        self.assertEqual(
            h,
            {
                "pathLookupType": "hostToDefaultGW",
                "type": "pathLookup",
                "groupBy": "siteName",
                "startingPoint": "1.1.1.1",
                "vrf": "mgmt",
            },
        )

    def test_host2gw_failed(self):
        with self.assertRaises(ValueError) as err:
            Host2GW(startingPoint="3.3.3.3/24")

    def test_network(self):
        n = Network(sites="L1", all_network=True).parameters("v4,3")
        self.assertEqual(n, {"type": "topology", "groupBy": "siteName", "paths": ["L1", "$main"]})
