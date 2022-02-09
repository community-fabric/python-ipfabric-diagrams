from typing import Optional, List, Union
from uuid import UUID

from pydantic import BaseModel, Field

from ipfabric_diagrams.input_models.graph_settings import EdgeSettings


class Severity(BaseModel):
    green: int = Field(alias='0')
    blue: int = Field(alias='10')
    amber: int = Field(alias='20')
    red: int = Field(alias='30')


class TrafficScore(BaseModel):
    accepted: int
    dropped: int
    forwarded: int
    total: int


class Packet(BaseModel):
    dst: Union[List[str], str]
    src: Union[List[str], str]
    type: str
    protocol: Optional[str] = None
    etherType: Optional[str] = None
    ttl: Optional[int] = None
    fragmentOffest: Optional[int] = Field(alias='fragment offset')
    flags: Optional[List[str]] = None


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
    edgeSettings: Optional[EdgeSettings] = None


class NetworkEdge(Edge, BaseModel):
    circle: bool
    children: List[str]


class PathLookupEdge(Edge, BaseModel):
    nextEdgeIds: List[str]
    prevEdgeIds: List[str]
    packet: List[Packet]
    severityInfo: Severity
    sourceIfaceName: Optional[str]
    targetIfaceName: Optional[str]
    trafficScore: TrafficScore
    nextEdge: Optional[list] = Field(default_factory=list)
    prevEdge: Optional[list] = Field(default_factory=list)
