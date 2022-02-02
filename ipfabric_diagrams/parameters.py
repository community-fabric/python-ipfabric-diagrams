import re
from ipaddress import IPv4Interface, IPv4Address
from typing import Optional, Union, List

from pydantic import BaseModel, validator, Field

PORT_REGEX = re.compile(r"^\d*$|^\d*-\d*$")


class ICMP(BaseModel):
    type: int
    code: int


class Options(BaseModel):
    applications: Optional[str] = '.*'
    tracked: Optional[bool] = False


class EntryPoint(BaseModel):
    sn: str
    iface: str


class Algorithm(BaseModel):
    type: str = 'automatic'
    vrf: Optional[str] = None
    entryPoints: Optional[List[EntryPoint]] = None

    @validator('type')
    def valid_types(cls, v):
        if v not in ['automatic', 'userDefined']:
            raise ValueError(f'Type "{v}" not in ["automatic", "userDefined"]')
        return v

    def algorithm_parameters(self):
        if self.type == 'automatic':
            return dict(type=self.type, vrf=self.vrf) if self.vrf else dict(type=self.type)
        else:
            return dict(type=self.type, entryPoints=[vars(e) for e in self.entryPoints])


class PathLookup(BaseModel):
    protocol: Optional[str] = 'tcp'
    srcPorts: Optional[Union[str, int]] = '1024-65535'
    dstPorts: Optional[Union[str, int]] = '80,443'
    tcpFlags: Optional[list] = None
    icmp: Optional[ICMP] = ICMP(type=0, code=0)
    ttl: Optional[int] = 128
    fragmentOffset: Optional[int] = 0
    securedPath: Optional[bool] = True
    srcRegions: Optional[str] = '.*'
    dstRegions: Optional[str] = '.*'
    otherOptions: Optional[Options] = Field(default_factory=Options)
    firstHopAlgorithm: Optional[Algorithm] = Field(default_factory=Algorithm)

    @validator('protocol')
    def valid_protocols(cls, v):
        if v.lower() not in ['tcp', 'udp', 'icmp']:
            raise ValueError(f'Protocol "{v}" not in ["tcp", "udp", "icmp"]')
        return v.lower()

    @validator('srcPorts', 'dstPorts')
    def check_ports(cls, v):
        ports = v.replace(" ", "").split(",")
        for p in ports:
            if not PORT_REGEX.match(p):
                raise ValueError(
                    f'Ports "{v}" is not in the valid syntax, examples: ["80", "80,443", "0-1024", "80,8000-8100,8443"]'
                )
        return str(",".join(ports))

    @validator('tcpFlags')
    def valid_flags(cls, v):
        v = [f.lower() for f in v] if v else list()
        if all(f in ["ack", "fin", "psh", "rst", "syn", "urg"] for f in v):
            return v
        raise ValueError(f'TCP Flags "{v}" must be None or combination of ["ack", "fin", "psh", "rst", "syn", "urg"]')

    def _l4_options(self):
        if self.protocol == 'icmp':
            return dict(type=self.icmp.type, code=self.icmp.code)
        elif self.protocol == 'udp':
            return dict(srcPorts=self.srcPorts, dstPorts=self.dstPorts)
        else:
            return dict(srcPorts=self.srcPorts, dstPorts=self.dstPorts, flags=self.tcpFlags)

    def base_parameters(self) -> dict:
        return dict(
            type="pathLookup",
            groupBy="siteName",
            protocol=self.protocol,
            ttl=self.ttl,
            fragmentOffset=self.fragmentOffset,
            securedPath=self.securedPath,
            srcRegions=self.srcRegions,
            dstRegions=self.dstRegions,
            l4Options=self._l4_options(),
            otherOptions=vars(self.otherOptions),
            firstHopAlgorithm=vars(self.firstHopAlgorithm)
        )


class Multicast(PathLookup, BaseModel):
    group: Union[IPv4Address, str]
    source: Union[IPv4Address, str]
    receiver: Optional[Union[IPv4Address, str]] = None

    @validator('group', 'source', 'receiver')
    def valid_ip(cls, v):
        if v and not isinstance(v, IPv4Address):
            raise ValueError(f'IP "{v}" not a valid IP Address')
        return v

    def parameters(self):
        parameters = self.base_parameters()
        parameters.update(dict(
            pathLookupType="multicast",
            group=str(self.group),
            source=str(self.source),

        ))
        if self.receiver:
            parameters['receiver'] = str(self.receiver)
        return parameters


class Unicast(PathLookup, BaseModel):
    startingPoint: Union[IPv4Interface, str]
    destinationPoint: Union[IPv4Interface, str]

    @validator('startingPoint', 'destinationPoint')
    def valid_ip(cls, v):
        if not isinstance(v, IPv4Interface):
            raise ValueError(f'IP "{v}" not a valid IP Address or Subnet')
        return v

    def parameters(self):
        parameters = self.base_parameters()
        parameters.update(dict(
            pathLookupType="unicast",
            networkMode=self._check_subnets(),
            startingPoint=self.startingPoint.with_prefixlen,
            destinationPoint=self.destinationPoint.with_prefixlen
        ))
        return parameters

    def _check_subnets(self) -> bool:
        """
        Checks for valid IP Addresses or Subnet
        :param ips: ip addresses
        :return: True if a subnet is found to set to networkMode, False if only hosts
        """
        masks = {ip.network.prefixlen for ip in [self.startingPoint, self.destinationPoint]}
        return True if masks != {32} else False
