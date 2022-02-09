import importlib.resources
import json

VALID_DEV_TYPES = ["aciLeaf", "aciSpine", "ap", "cloudInstance", "cloudTransitHub", "cloudInternetGw", "cloudNatGw",
                   "cloudRouter", "cloudVpnGw", "fex", "fw", "host", "l3switch", "lb", "nx7000", "phone", "router",
                   "securityManagement", "switch", "unknown", "vgw", "waas", "wlc"]
VALID_PATH_PROTOCOLS = []
VALID_PROTOCOL_LABELS = {
    "dgw": None,
    "ebgp": None,
    "eigrp": None,
    "fex": None, "ibgp": None, "isis": None, "ldp": None, "ospf": None,
    "ospfv3": None, "pim": None, "rib": None, "rip": None, "stp": None, "vxlan": None, "wired": None, "wireless": None,
    "xdp": None
}
VALID_NET_PROTOCOLS = VALID_PROTOCOL_LABELS.keys()

DEFAULT_NETWORK = json.loads(
    importlib.resources.read_text("ipfabric_diagrams.input_models.factory_defaults", "networkSettings.json")
)
DEFAULT_PATHLOOKUP = json.loads(
    importlib.resources.read_text("ipfabric_diagrams.input_models.factory_defaults", "pathLookupSettings.json")
)
