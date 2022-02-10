from typing import Optional, List, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, validator, Field
from pydantic.color import Color

from ipfabric_diagrams.input_models.constants import VALID_DEV_TYPES, DEFAULT_NETWORK, DEFAULT_PATHLOOKUP, \
    VALID_NET_PROTOCOLS


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
        return dict(
            color=self.color.as_hex(),
            pattern=self.pattern,
            thicknessThresholds=self.thicknessThresholds
        )


class Setting(BaseModel):
    name: str
    visible: bool = True
    grouped: bool = True
    style: Style
    type: str

    def base_settings(self, version: str) -> dict:
        return dict(
            name=self.name,
            visible=self.visible,
            grouped=self.grouped,
            style=self.style.style_settings(version),
            type=self.type
        )


class EdgeSettings(Setting, BaseModel):
    labels: List[str] = ['protocols']
    id: Optional[UUID] = None

    def settings(self, version: str) -> dict:
        base_settings = self.base_settings(version)
        base_settings['labels'] = self.labels
        base_settings['id'] = str(uuid4())  # TODO Remove when IPF does not require
        return base_settings


class GroupSettings(Setting, BaseModel):
    label: str
    children: List[EdgeSettings]
    id: Optional[UUID] = None

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

    @staticmethod
    def _update_edge(children: List[EdgeSettings], name: str, attribute: str):
        for edge in children:
            if edge.name.lower() == name:
                setattr(edge, attribute, False)
                return True
        return False

    def _update_group(self, name: str, attribute: str, group: bool = False):
        for edge in self.edges:
            if group and isinstance(edge, GroupSettings) and edge.name.lower() == name:
                setattr(edge, attribute, False)
                return True
            elif not group:
                if isinstance(edge, GroupSettings) and self._update_edge(edge.children, name, attribute):
                    return self._update_group(edge.name.lower(), 'grouped', True)
                elif isinstance(edge, EdgeSettings) and self._update_edge([edge], name, attribute):
                    return True
        return False

    def hide_protocol(self, protocol_name: str):
        if protocol_name.lower() in VALID_NET_PROTOCOLS:
            return self._update_group(protocol_name.lower(), attribute='visible', group=False)
        else:
            raise KeyError(f"Protocol {protocol_name} does not exist.  Valid protocols are {VALID_NET_PROTOCOLS}")

    def ungroup_protocol(self, protocol_name: str):
        return self._update_group(protocol_name.lower(), attribute='grouped', group=False)
        # TODO Uncomment
        # if protocol_name.lower() in VALID_NET_PROTOCOLS:
        #     return self._update_group(protocol_name.lower(), attribute='grouped', group=False)
        # else:
        #     raise KeyError(f"Protocol {protocol_name} does not exist.  Valid protocols are {VALID_NET_PROTOCOLS}")

    def hide_group(self, group_name: str):
        group_names = [g.name.lower() for g in self.edges if isinstance(g, GroupSettings)]
        if group_name.lower() in group_names:
            return self._update_group(group_name.lower(), attribute='visible', group=True)
        else:
            raise KeyError(f"Group {group_name} does not exist.  Valid groups are {group_names}")

    def ungroup_group(self, group_name: str):
        group_names = [g.name.lower() for g in self.edges if isinstance(g, GroupSettings)]
        if group_name.lower() in group_names:
            return self._update_group(group_name.lower(), attribute='grouped', group=True)
        else:
            raise KeyError(f"Group {group_name} does not exist.  Valid groups are {group_names}")


class PathLookupSettings(GraphSettings):
    def __init__(self):
        edges = [EdgeSettings(**edge) for edge in DEFAULT_PATHLOOKUP]
        super().__init__(edges=edges)

    @property
    def protocol_priority(self):
        return [edge.name for edge in self.edges]


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
        if v and v in ["nonRedundantEdges", "singlePointsOfFailure"]:
            return v
        try:
            int(v)
            return str(v)
        except ValueError:
            raise ValueError(f'"{v}" is not an Intent Rule ID or in ["nonRedundantEdges", "singlePointsOfFailure"]')

    @property
    def type(self):
        return "compare" if self.snapshotToCompare else "intent"

    def overlay(self, version: str) -> dict:
        if self.snapshotToCompare:
            return dict(type=self.type, snapshotToCompare=self.snapshotToCompare)
        else:
            return dict(type=self.type, intentRuleId=self.intentRuleId)
