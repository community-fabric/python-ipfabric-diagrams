import importlib.resources
import json


VALID_DEV_TYPES = ["aciLeaf", "aciSpine", "ap", "cloudInstance", "cloudTransitHub", "cloudInternetGw", "cloudNatGw",
                   "cloudRouter", "cloudVpnGw", "fex", "fw", "host", "l3switch", "lb", "nx7000", "phone", "router",
                   "securityManagement", "switch", "unknown", "vgw", "waas", "wlc"]
DEFAULT_NETWORK = json.loads(
    importlib.resources.read_text("ipfabric_diagrams.input_models.factory_defaults", "networkSettings.json")
)
DEFAULT_PATHLOOKUP = json.loads(
    importlib.resources.read_text("ipfabric_diagrams.input_models.factory_defaults", "pathLookupSettings.json")
)