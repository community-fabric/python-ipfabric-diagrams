import importlib.resources
import json
from typing import Optional, List, Union
from uuid import uuid4

from pydantic import BaseModel, validator, Field

VALID_DEV_TYPES = ["aciLeaf", "aciSpine", "ap", "cloudInstance", "cloudTransitHub", "cloudInternetGw", "cloudNatGw",
                   "cloudRouter", "cloudVpnGw", "fex", "fw", "host", "l3switch", "lb", "nx7000", "phone", "router",
                   "securityManagement", "switch", "unknown", "vgw", "waas", "wlc"]
DEFAULT_NETWORK = json.loads(importlib.resources.read_text(__package__, "defaultGraphSettings.json"))
DEFAULT_PATHLOOKUP = json.loads(importlib.resources.read_text(__package__, "defaultPathLookupSettings.json"))


class Style(BaseModel):
    color: str
    pattern: str
    thicknessThresholds: Optional[list] = [2, 4, 8]


class EdgeSettings(BaseModel):
    name: str
    visible: bool = True
    grouped: bool = True
    labels: List[str] = ['protocols']
    style: Style
    type: str = 'protocol'

    def settings(self, version: str) -> dict:
        settings = vars(self)
        settings['style'] = vars(self.style)
        settings['id'] = str(uuid4())
        return settings


class GroupSettings(BaseModel):
    name: str
    visible: bool = True
    grouped: bool = True
    label: str
    style: Style
    children: List[EdgeSettings]
    type: str = 'group'

    def settings(self, version: str) -> dict:
        settings = vars(self)
        settings['style'] = vars(self.style)
        settings['children'] = [child.settings(version) for child in self.children]
        return settings


class PathLookup(BaseModel):
    ignoredTopics: Optional[List[str]] = Field(
        default_factory=list,
        description="List of topics to ignore.  Valid topics are in ['ACL', 'FORWARDING', 'ZONEFW'].")
    colorDetectedLoops: Optional[bool] = True

    @validator('ignoredTopics')
    def _valid_topics(cls, v):
        if v and not all(t in ['ACL', 'FORWARDING', 'ZONEFW'] for t in v):
            raise ValueError(f"Ignored Topics '{v}' must be None or in ['ACL', 'FORWARDING', 'ZONEFW'].")
        return v


class GraphSettings(BaseModel):
    edges: List[Union[GroupSettings, EdgeSettings]]
    hiddenDeviceTypes: Optional[List[str]] = Field(default_factory=list)
    pathLookup: PathLookup = Field(default_factory=PathLookup)

    @validator('hiddenDeviceTypes')
    def _valid_dev_types(cls, v):
        if v and not all(d in VALID_DEV_TYPES for d in v):
            raise ValueError(f"Device Types '{v}' must be None or in {VALID_DEV_TYPES}.")
        return v

    def settings(self, version: str) -> dict:
        return dict(
            edges=[edge.settings(version) for edge in self.edges],
            hiddenDeviceTypes=self.hiddenDeviceTypes,
            pathLookup=vars(self.pathLookup)
        )


class NetworkSettings(GraphSettings):
    def __init__(self):
        edges = [GroupSettings(**edge) for edge in DEFAULT_NETWORK]
        super().__init__(edges=edges, hiddenDeviceTypes=['ap', 'fex', 'host', 'phone'])


class PathLookupSettings(GraphSettings):
    def __init__(self):
        edges = [EdgeSettings(**edge) for edge in DEFAULT_PATHLOOKUP]
        super().__init__(edges=edges)
