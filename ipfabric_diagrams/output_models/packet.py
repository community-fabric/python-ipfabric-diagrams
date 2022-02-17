from typing import List, Union

from pydantic import BaseModel, Field
from typing_extensions import Annotated
from typing_extensions import Literal

from ipfabric_diagrams.output_models.protocols import MPLS, Ethernet, ESP, IP


class Transport(BaseModel):
    src: List[str]
    dst: List[str]


class TCP(Transport, BaseModel):
    flags: List[str]
    type: Literal['tcp']


class UDP(Transport, BaseModel):
    type: Literal['udp']


class ICMP(BaseModel):
    icmpCode: int
    icmpType: int
    type: Literal['icmp']


PACKET = Annotated[Union[ICMP, UDP, TCP, Ethernet, IP, MPLS, ESP], Field(discriminator='type')]
