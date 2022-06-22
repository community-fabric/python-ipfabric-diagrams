from typing import Optional, List, Union, Dict
from uuid import UUID

from pydantic import BaseModel, Field

from ipfabric_diagrams.output_models.protocols import PROTOCOLS
from ipfabric_diagrams.output_models.trace import Trace


class Checks(BaseModel):
    green: int = Field(alias="0")
    blue: int = Field(alias="10")
    amber: int = Field(alias="20")
    red: int = Field(alias="30")


class Severity(Checks):
    pass


class Topics(BaseModel):
    acl: Checks = Field(alias="ACL")
    forwarding: Checks = Field(alias="FORWARDING")
    zonefw: Checks = Field(alias="ZONEFW")


class TrafficScore(BaseModel):
    accepted: int
    dropped: int
    forwarded: int
    total: int


class Label(BaseModel):
    type: str
    visible: bool
    text: str


class Labels(BaseModel):
    center: Optional[List[Label]] = None
    source: Optional[List[Label]] = None
    target: Optional[List[Label]] = None


class Node(BaseModel):
    path: Optional[str] = None
    boxId: Union[str, None]
    children: List
    graphType: str
    id: str
    label: str
    parentPath: Union[str, None]
    sn: str
    type: str
    stack: Optional[bool] = None


class Edge(BaseModel):
    direction: str
    source: str
    target: str
    edgeSettingsId: UUID
    id: str
    labels: Labels
    protocol: Optional[str] = ""


class NetworkEdge(Edge, BaseModel):
    circle: bool
    children: List[str]


class PathLookupEdge(Edge, BaseModel):
    nextEdgeIds: List[str]
    prevEdgeIds: List[str]
    packet: List[PROTOCOLS]
    severityInfo: Severity
    sourceIfaceName: Optional[str]
    targetIfaceName: Optional[str]
    trafficScore: TrafficScore
    nextEdge: Optional[list] = Field(default_factory=list)
    prevEdge: Optional[list] = Field(default_factory=list)


class EventsSummary(BaseModel):
    flags: list
    topics: Topics
    global_list: list = Field(alias="global")


class Traces(BaseModel):
    severityInfo: Checks
    sourcePacketId: str
    targetPacketId: str
    trace: List[Trace]


class Decision(BaseModel):
    traces: List[Traces]
    trafficIn: Optional[Dict[str, List[str]]] = Field(default_factory=dict)
    trafficOut: Optional[Dict[str, List[str]]] = Field(default_factory=dict)


class Check(BaseModel):
    exists: bool


class PathLookup(BaseModel):
    eventsSummary: EventsSummary
    decisions: Dict[str, Decision]
    passingTraffic: str
    check: Check


class GraphResult(BaseModel):
    nodes: Dict[str, Node]
    edges: Dict[str, Union[NetworkEdge, PathLookupEdge]]
    pathlookup: Optional[PathLookup] = None
