import importlib.resources
import json
from typing import Optional, List, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, validator, Field
from pydantic.color import Color

VALID_DEV_TYPES = ["aciLeaf", "aciSpine", "ap", "cloudInstance", "cloudTransitHub", "cloudInternetGw", "cloudNatGw",
                   "cloudRouter", "cloudVpnGw", "fex", "fw", "host", "l3switch", "lb", "nx7000", "phone", "router",
                   "securityManagement", "switch", "unknown", "vgw", "waas", "wlc"]
DEFAULT_NETWORK = json.loads(
    importlib.resources.read_text("ipfabric_diagrams.factory_defaults", "networkSettings.json")
)
DEFAULT_PATHLOOKUP = json.loads(
    importlib.resources.read_text("ipfabric_diagrams.factory_defaults", "pathLookupSettings.json")
)


class Style(BaseModel):
    color: Color
    pattern: Optional[str] = 'solid'
    thicknessThresholds: Optional[List[int]] = [2, 4, 8]

    @validator("pattern")
    def _valid_patterns(cls, v):
        if v.lower() not in ["solid", "dashed", "dotted"]:
            raise ValueError(f'Pattern "{v}" not in ["solid", "dashed", "dotted"]')
        return v.lower()

    def style_settings(self, version: str) -> dict:
        settings = vars(self)
        settings['color'] = self.color.as_hex()
        return settings


class Setting(BaseModel):
    name: str
    visible: bool = True
    grouped: bool = True
    style: Style
    type: str

    def base_settings(self, version: str) -> dict:
        settings = vars(self)
        settings['style'] = self.style.style_settings(version)
        return settings


class EdgeSettings(Setting, BaseModel):
    labels: List[str] = ['protocols']

    def settings(self, version: str) -> dict:
        base_settings = self.base_settings(version)
        base_settings['labels'] = self.labels
        base_settings['id'] = str(uuid4())  # TODO Remove when IPF does not require
        return base_settings


class GroupSettings(Setting, BaseModel):
    label: str
    children: List[EdgeSettings]

    def settings(self, version: str) -> dict:
        base_settings = self.base_settings(version)
        base_settings.update(dict(
            children=[child.settings(version) for child in self.children],
            label=self.label
        ))
        return base_settings


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

    def _update_protocol(self, protocol_name: str, proto_attr: str, value: bool = False):
        for edge in self.edges:
            if isinstance(edge, EdgeSettings) and edge.name == protocol_name:
                setattr(edge, proto_attr, value)
                return True
            if isinstance(edge, GroupSettings):
                for child in edge.children:
                    if child.name == protocol_name:
                        setattr(edge, proto_attr, value)
                        edge.grouped = False
                        return True
        return False

    def hide_protocol(self, protocol_name: str, unhide: bool = False):
        return self._update_protocol(protocol_name.lower(), 'visible', unhide)

    def ungroup_protocol(self, protocol_name: str, grouped: bool = False):
        return self._update_protocol(protocol_name.lower(), 'grouped', grouped)

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

    def hide_group(self, group_name: str, unhide: bool = False):
        for edge in self.edges:
            if isinstance(edge, GroupSettings) and edge.name == group_name.lower():
                edge.visible = unhide
                return True
        return False

    def ungroup_group(self, group_name: str, group: bool = False):
        for edge in self.edges:
            if isinstance(edge, GroupSettings) and edge.name == group_name.lower():
                edge.grouped = group
                return True
        return False


class PathLookupSettings(GraphSettings):
    def __init__(self):
        edges = [EdgeSettings(**edge) for edge in DEFAULT_PATHLOOKUP]
        super().__init__(edges=edges)


class Overlay(BaseModel):
    """Set snapshotToCompare or intentRuleId, not both."""
    snapshotToCompare: Optional[Union[UUID, str]] = Field(None, description="Snapshot ID to compare.")
    intentRuleId: Optional[Union[int, str]] = Field(
        None,
        description="Intent Rule ID to overlay. Also valid: ['nonRedundantEdges', 'singlePointsOfFailure']",
    )

    @validator("snapshotToCompare")
    def _valid_snapshot(cls, v):
        if v and v in ["$last", "$prev", "$lastLocked"]:
            return v
        elif v and isinstance(v, UUID):
            return str(v)
        raise ValueError(f'"{v}" is not a Snapshot ID or in ["$last", "$prev", "$lastLocked"]')

    @validator("intentRuleId")
    def _valid_intentrule(cls, v):
        if v and (isinstance(v, int) or v in ["nonRedundantEdges", "singlePointsOfFailure"]):
            return str(v)
        raise ValueError(f'"{v}" is not an Intent Rule ID or in ["nonRedundantEdges", "singlePointsOfFailure"]')

    @property
    def type(self):
        return "compare" if self.snapshotToCompare else "intent"

    def overlay(self, version: str) -> dict:
        if self.snapshotToCompare:
            return dict(type=self.type, snapshotToCompare=self.snapshotToCompare)
        else:
            return dict(type=self.type, intentRuleId=self.intentRuleId)
