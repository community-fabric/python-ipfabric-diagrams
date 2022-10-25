from typing import Optional, List, Union
from uuid import UUID

from pydantic import BaseModel, validator, Field
from pydantic.color import Color

from ipfabric_diagrams.input_models.constants import VALID_DEV_TYPES, DEFAULT_NETWORK, DEFAULT_PATHLOOKUP, \
    VALID_NET_PROTOCOLS, VALID_PROTOCOL_LABELS, VALID_PATH_PROTOCOLS


class Style(BaseModel):
    color: Color
    pattern: Optional[str] = 'solid'
    thicknessThresholds: Optional[List[int]] = [2, 4, 8]

    @validator("pattern")
    def _valid_patterns(cls, v):
        if v.lower() not in ["solid", "dashed", "dotted"]:
            raise ValueError(f'Pattern "{v}" not in ["solid", "dashed", "dotted"]')
        return v.lower()

    def style_settings(self) -> dict:
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

    def base_settings(self) -> dict:
        return dict(
            name=self.name,
            visible=self.visible,
            grouped=self.grouped,
            style=self.style.style_settings(),
            type=self.type
        )


class EdgeSettings(Setting, BaseModel):
    labels: List[str] = ['protocols']
    id: Optional[UUID] = None

    def settings(self) -> dict:
        base_settings = self.base_settings()
        base_settings['labels'] = self.labels
        return base_settings


class GroupSettings(Setting, BaseModel):
    label: str
    children: List[EdgeSettings]
    id: Optional[UUID] = None

    def settings(self) -> dict:
        base_settings = self.base_settings()
        base_settings.update(dict(
            children=[child.settings() for child in self.children],
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
    pathLookup: Optional[PathLookup] = None

    @validator('hiddenDeviceTypes')
    def _valid_dev_types(cls, v):
        if v and not all(d in VALID_DEV_TYPES for d in v):
            raise ValueError(f"Device Types '{v}' must be None or in {VALID_DEV_TYPES}.")
        return v


class NetworkSettings(GraphSettings):
    def __init__(self):
        edges = [GroupSettings(**edge) for edge in DEFAULT_NETWORK]
        super().__init__(edges=edges, hiddenDeviceTypes=['ap', 'fex', 'host', 'phone'])

    @staticmethod
    def _update_edge(children: List[EdgeSettings], name: str, attribute: str, bool_value=False):
        for edge in children:
            if edge.name.lower() == name:
                setattr(edge, attribute, bool_value)
                return True
        return False

    def _update_group(self, name: str, attribute: str, group: bool = False, bool_value=False):
        for edge in self.edges:
            if group and isinstance(edge, GroupSettings) and edge.name.lower() == name:
                setattr(edge, attribute, bool_value)
                return True
            elif not group:
                if isinstance(edge, GroupSettings) and self._update_edge(edge.children, name, attribute, bool_value):
                    return self._update_group(edge.name.lower(), 'grouped', True)
                elif isinstance(edge, EdgeSettings) and self._update_edge([edge], name, attribute, bool_value):
                    return True
        return False

    def hide_protocol(self, protocol_name: str, unhide: bool = False):
        if protocol_name.lower() in VALID_NET_PROTOCOLS:
            return self._update_group(VALID_NET_PROTOCOLS[protocol_name.lower()], attribute='visible', group=False,
                                      bool_value=unhide)
        else:
            raise KeyError(
                f"Protocol {protocol_name} does not exist.  Valid protocols are {VALID_NET_PROTOCOLS.values()}")

    def hide_all_protocols(self):
        for protocol_name in VALID_NET_PROTOCOLS.values():
            self._update_group(protocol_name, attribute='visible', group=False)

    def ungroup_protocol(self, protocol_name: str):
        if protocol_name.lower() in VALID_NET_PROTOCOLS:
            return self._update_group(VALID_NET_PROTOCOLS[protocol_name.lower()], attribute='grouped', group=False)
        else:
            raise KeyError(
                f"Protocol {protocol_name} does not exist.  Valid protocols are {VALID_NET_PROTOCOLS.values()}")

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

    @staticmethod
    def _proto_label(edge: EdgeSettings, protocol_name: str, label_name: str):
        if edge.name.lower() == protocol_name:
            proto = next(x for x in VALID_PROTOCOL_LABELS[protocol_name].labels if x == label_name)
            if proto.center:
                edge.labels[0] = proto.name
            else:
                edge.labels[1] = proto.name
            return True
        return False

    def change_label(self, protocol_name: str, label_name: str):
        protocol_name, label_name = protocol_name.lower(), label_name.lower()
        if protocol_name not in VALID_NET_PROTOCOLS:
            raise KeyError(
                f"Protocol {protocol_name} does not exist.  Valid protocols are {VALID_NET_PROTOCOLS.values()}")
        else:
            protocol_name = VALID_NET_PROTOCOLS[protocol_name]
        if label_name not in VALID_PROTOCOL_LABELS[protocol_name].labels:
            raise KeyError(f"Label {label_name} does not exist for protocol {protocol_name}.  "
                           f"Valid labels for {protocol_name} are {VALID_PROTOCOL_LABELS[protocol_name].labels}")
        for edge in self.edges:
            if isinstance(edge, GroupSettings):
                for child in edge.children:
                    if self._proto_label(child, protocol_name, label_name):
                        return True
            if self._proto_label(edge, protocol_name, label_name):
                return True
        return False

    def settings(self) -> dict:
        settings = dict(
            edges=[edge.settings() for edge in self.edges],
            hiddenDeviceTypes=self.hiddenDeviceTypes,
        )
        return settings


class PathLookupSettings(GraphSettings):
    def __init__(self):
        edges = [EdgeSettings(**edge) for edge in DEFAULT_PATHLOOKUP]
        super().__init__(edges=edges, pathLookup=PathLookup())

    @property
    def protocol_priority(self):
        return {edge.name.lower(): idx for idx, edge in enumerate(self.edges)}

    def increase_priority(self, protocol_name: str):
        if protocol_name.lower() not in VALID_PATH_PROTOCOLS:
            raise KeyError(f"Protocol {protocol_name} does not exist.  Valid protocols are {VALID_PATH_PROTOCOLS}")
        current = self.protocol_priority[protocol_name]
        if current != 0:
            self.edges[current], self.edges[current - 1] = self.edges[current - 1], self.edges[current]
        return True

    def decrease_priority(self, protocol_name: str):
        if protocol_name.lower() not in VALID_PATH_PROTOCOLS:
            raise KeyError(f"Protocol {protocol_name} does not exist.  Valid protocols are {VALID_PATH_PROTOCOLS}")
        current = self.protocol_priority[protocol_name]
        if current != len(self.edges) - 1:
            self.edges[current], self.edges[current + 1] = self.edges[current + 1], self.edges[current]
        return True

    def settings(self) -> dict:
        settings = dict(
            edges=[edge.settings() for edge in self.edges],
            pathLookup=vars(self.pathLookup),
        )
        return settings


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

    def overlay(self) -> dict:
        if self.snapshotToCompare:
            return dict(type=self.type, snapshotToCompare=self.snapshotToCompare)
        else:
            return dict(type=self.type, intentRuleId=self.intentRuleId)
