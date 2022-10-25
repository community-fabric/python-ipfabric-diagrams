import importlib.resources
import json
from typing import List

from pydantic import BaseModel


class Label(BaseModel):
    name: str
    center: bool = False

    def __str__(self):
        return self.name.lower()

    def __eq__(self, other):
        return self.name.lower() == other.lower()


class Protocol(BaseModel):
    name: str
    labels: List[Label]

    def __eq__(self, other):
        return self.name == other.lower()


PROTOCOL = Label(name="protocol", center=True)
INT_NAME = Label(name="intName", center=False)
IP_ADDR = Label(name="ipAddress", center=False)
SUBNET = Label(name="subnet", center=True)
AS = Label(name="as", center=False)
VALID_PROTOCOL_LABELS = dict(
    dgw=Protocol(name="dgw", labels=[PROTOCOL, INT_NAME, IP_ADDR, SUBNET]),
    dgwIpv6=Protocol(name="dgwIpv6", labels=[PROTOCOL, INT_NAME, IP_ADDR, SUBNET]),
    ebgp=Protocol(name="ebgp", labels=[PROTOCOL, IP_ADDR, AS, Label(name="prefix", center=False)]),
    eigrp=Protocol(name="eigrp", labels=[PROTOCOL, INT_NAME, IP_ADDR, SUBNET, AS]),
    fex=Protocol(name="fex", labels=[PROTOCOL, INT_NAME]),
    ibgp=Protocol(name="ibgp", labels=[PROTOCOL, IP_ADDR, AS, Label(name="prefix", center=False)]),
    isis=Protocol(name="isis", labels=[PROTOCOL, INT_NAME, IP_ADDR, SUBNET]),
    ldp=Protocol(name="ldp", labels=[PROTOCOL, INT_NAME, IP_ADDR, SUBNET]),
    ospf=Protocol(
        name="ospf",
        labels=[
            PROTOCOL,
            INT_NAME,
            IP_ADDR,
            SUBNET,
            Label(name="area", center=False),
            Label(name="cost", center=False),
        ],
    ),
    ospfv3=Protocol(
        name="ospfv3",
        labels=[
            PROTOCOL,
            INT_NAME,
            IP_ADDR,
            SUBNET,
            Label(name="area", center=False),
            Label(name="cost", center=False),
        ],
    ),
    pim=Protocol(name="pim", labels=[PROTOCOL, INT_NAME, IP_ADDR, SUBNET]),
    rib=Protocol(name="rib", labels=[PROTOCOL, INT_NAME, IP_ADDR, SUBNET]),
    ribIpv6=Protocol(name="ribIpv6", labels=[PROTOCOL, INT_NAME, IP_ADDR, SUBNET]),
    rip=Protocol(name="rip", labels=[PROTOCOL, INT_NAME, IP_ADDR, SUBNET]),
    rsvp=Protocol(name="rsvp", labels=[PROTOCOL, INT_NAME, IP_ADDR, SUBNET]),
    stp=Protocol(name="stp", labels=[PROTOCOL, INT_NAME, Label(name="media", center=False)]),
    vxlan=Protocol(name="vxlan", labels=[PROTOCOL, INT_NAME, IP_ADDR, SUBNET]),
    wired=Protocol(name="wired", labels=[PROTOCOL, INT_NAME]),
    wireless=Protocol(name="wireless", labels=[PROTOCOL, INT_NAME]),
    xdp=Protocol(name="xdp", labels=[PROTOCOL, INT_NAME]),
)

VALID_NET_PROTOCOLS = {p.lower(): p for p in VALID_PROTOCOL_LABELS.keys()}

VALID_DEV_TYPES = [
    "aciLeaf",
    "aciSpine",
    "ap",
    "cloud",
    "cloudInstance",
    "cloudInternetGw",
    "cloudLoadBalancer",
    "cloudNatGw",
    "cloudRouter",
    "cloudTransitHub",
    "cloudVpnGw",
    "fex",
    "fw",
    "host",
    "l3switch",
    "lb",
    "nx7000",
    "phone",
    "router",
    "securityManagement",
    "switch",
    "transit",
    "unknown",
    "vgw",
    "waas",
    "wlc",
]

VALID_PATH_PROTOCOLS = ["capwap", "esp", "ethernet", "ethernetVlan", "gre", "ip", "loop", "mpls", "tcp", "udp", "vxlan"]

DEFAULT_NETWORK = json.loads(
    importlib.resources.read_text("ipfabric_diagrams.input_models.factory_defaults", "networkSettings.json")
)
DEFAULT_PATHLOOKUP = json.loads(
    importlib.resources.read_text("ipfabric_diagrams.input_models.factory_defaults", "pathLookupSettings.json")
)

VALID_LAYOUTS = ["circular", "downwardTree", "hierarchical", "radial", "universal", "upwardTree"]
