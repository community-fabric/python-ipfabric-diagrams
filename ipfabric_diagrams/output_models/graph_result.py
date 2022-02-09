from typing import Optional, List, Union
from uuid import UUID

from pydantic import BaseModel

from ipfabric_diagrams.input_models.graph_settings import EdgeSettings


class Label(BaseModel):
    type: str
    visible: bool
    text: str


class Labels(BaseModel):
    center: List[Label]
    source: List[Label]
    target: List[Label]


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
    circle: bool
    edgeSettingsId: UUID
    children: List[str]
    id: str
    labels: Labels
    edgeSettings: Optional[EdgeSettings] = None
