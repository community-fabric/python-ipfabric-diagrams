from typing import Optional, List

from pydantic import BaseModel, Field
from typing_extensions import Literal


class MPLS(BaseModel):
    stack: List[str]
    type: Literal['mpls']


class Ethernet(BaseModel):
    src: Optional[str] = None
    dst: Optional[str] = None
    etherType: str
    type: Literal['ethernet']
    vlan: Optional[int] = None


class ESP(BaseModel):
    payload: str
    nextHeader: str
    type: Literal['esp']


class IP(BaseModel):
    src: List[str]
    dst: List[str]
    fragmentOffset: int = Field(alias='fragment offset')
    protocol: str
    ttl: int
    type: Literal['ip']
