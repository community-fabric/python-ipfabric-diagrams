import re
from copy import deepcopy
from ipaddress import IPv4Interface, IPv4Address
from typing import Optional, Union, List

from pydantic import BaseModel, validator, Field

from ipfabric_diagrams.input_models.constants import VALID_LAYOUTS

PORT_REGEX = re.compile(r"^\d*$|^\d*-\d*$")
ALL_NETWORK = "$main"


class Instance(BaseModel):
    rootId: str
    vlanId: int
    visible: bool = True
    grouped: bool = True


class STPInstances(BaseModel):
    isolate: bool = False
    instances: List[Instance]


class Technologies(BaseModel):
    expandDeviceGroups: Optional[List[str]] = Field(default_factory=list)
    stpInstances: Optional[STPInstances]

    def technologies_parameters(self) -> dict:
        params = dict(expandDeviceGroups=self.expandDeviceGroups)
        if self.stpInstances:
            params["stpInstances"] = dict(isolate=self.stpInstances.isolate, instances=list())
            for i in self.stpInstances.instances:
                params["stpInstances"]["instances"].append(vars(i))
        return params


class ICMP(BaseModel):
    type: int
    code: int


class OtherOptions(BaseModel):
    applications: Optional[str] = ".*"
    tracked: Optional[bool] = False


class EntryPoint(BaseModel):
    sn: str = Field(title="Serial Number", description="IP Fabric Unique Device Serial Number API column sn")
    iface: str = Field(
        title="Interface", description="Interface to use as entry point. This is the intName not nameOriginal."
    )
    hostname: str = Field(title="Hostname", description="Hostname of the Device")


class Algorithm(BaseModel):
    """Default is automatic. Adding entryPoints will change to userDefined."""

    vrf: Optional[str] = None
    entryPoints: Optional[List[EntryPoint]] = None

    @property
    def type(self):
        return "userDefined" if self.entryPoints else "automatic"

    def algorithm_parameters(self) -> dict:
        if self.entryPoints:
            return dict(type=self.type, entryPoints=[vars(e) for e in self.entryPoints])
        else:
            return dict(type=self.type, vrf=self.vrf) if self.vrf else dict(type=self.type)


class PathLookup(BaseModel):
    protocol: Optional[str] = Field("tcp", title="Protocol", description="Valid protocols are tcp, udp, or icmp.")
    srcPorts: Optional[Union[str, int]] = Field(
        "1024-65535",
        title="Source Ports",
        description="Source ports if protocol is tcp or udp. "
        "Can be comma separated, a range using -, or any combination.",
    )
    dstPorts: Optional[Union[str, int]] = Field(
        "80,443",
        title="Destination Ports",
        description="Destination ports if protocol is tcp or udp. "
        "Can be comma separated, a range using -, or any combination.",
    )
    tcpFlags: Optional[list] = Field(
        default_factory=list,
        title="TCP Flags",
        description="Optional additional flags if protocol = TCP. "
        "Valid flags are ['ack', 'fin', 'psh', 'rst', 'syn', 'urg']",
    )
    icmp: Optional[ICMP] = Field(
        ICMP(type=0, code=0),
        title="ICMP Packet",
        description="Default is Echo Reply (type=0, code=0). You can pass in an ICMP model from ipfabric_diagrams.icmp "
        "or specify your own values like {'type': 1, 'code': 2}.",
    )
    ttl: Optional[int] = Field(128, title="Time To Live", description="TTL value, default is 128.")
    fragmentOffset: Optional[int] = Field(
        0, title="Fragment Offset", description="Fragment Offset value, default is 0."
    )
    securedPath: Optional[bool] = True
    enableRegions: Optional[bool] = False
    srcRegions: Optional[str] = ".*"
    dstRegions: Optional[str] = ".*"
    otherOptions: Optional[OtherOptions] = Field(default_factory=OtherOptions)
    firstHopAlgorithm: Optional[Algorithm] = Field(default_factory=Algorithm)

    @validator("protocol")
    def _valid_protocols(cls, v):
        if v.lower() not in ["tcp", "udp", "icmp"]:
            raise ValueError(f'Protocol "{v}" not in ["tcp", "udp", "icmp"]')
        return v.lower()

    @validator("srcPorts", "dstPorts")
    def _check_ports(cls, v):
        ports = v.replace(" ", "").split(",")
        for p in ports:
            if not PORT_REGEX.match(p):
                raise ValueError(
                    f'Ports "{v}" is not in the valid syntax, examples: ["80", "80,443", "0-1024", "80,8000-8100,8443"]'
                )
            if "-" in p:
                pn = p.split("-")
                if int(pn[0]) >= int(pn[1]):
                    raise ValueError(f'Ports "{p}" is invalid. {pn[0]} must be smaller than {pn[1]}.')
        return str(",".join(ports))

    @validator("tcpFlags")
    def _valid_flags(cls, v):
        v = [f.lower() for f in v] if v else list()
        if all(f in ["ack", "fin", "psh", "rst", "syn", "urg"] for f in v):
            return v
        raise ValueError(f'TCP Flags "{v}" must be None or combination of ["ack", "fin", "psh", "rst", "syn", "urg"]')

    def _l4_options(self):
        if self.protocol == "icmp":
            return dict(type=self.icmp.type, code=self.icmp.code)
        elif self.protocol == "udp":
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
            enableRegions=self.enableRegions,
            srcRegions=self.srcRegions,
            dstRegions=self.dstRegions,
            l4Options=self._l4_options(),
            otherOptions=vars(self.otherOptions),
            firstHopAlgorithm=self.firstHopAlgorithm.algorithm_parameters(),
        )

    @staticmethod
    def swap_src_dst(parameters: dict):
        params = deepcopy(parameters)
        if params["protocol"] != "icmp":
            params["l4Options"]["srcPorts"], params["l4Options"]["dstPorts"] = (
                params["l4Options"]["dstPorts"],
                params["l4Options"]["srcPorts"],
            )
        params["srcRegions"], params["dstRegions"] = params["dstRegions"], params["srcRegions"]
        params["startingPoint"], params["destinationPoint"] = params["destinationPoint"], params["startingPoint"]
        return params


class Multicast(PathLookup, BaseModel):
    group: Union[IPv4Address, str]
    source: Union[IPv4Address, str]
    receiver: Optional[Union[IPv4Address, str]] = None

    @validator("group", "source", "receiver")
    def _valid_ip(cls, v):
        if v and not isinstance(v, IPv4Address):
            raise ValueError(f'IP "{v}" not a valid IP Address')
        return v

    def parameters(self):
        parameters = self.base_parameters()
        parameters.update(
            dict(
                pathLookupType="multicast",
                group=str(self.group),
                source=str(self.source),
            )
        )
        if self.receiver:
            parameters["receiver"] = str(self.receiver)
        return parameters


class Unicast(PathLookup, BaseModel):
    startingPoint: Union[IPv4Interface, str] = Field(title="Source IP Address or Subnet")
    destinationPoint: Union[IPv4Interface, str] = Field(title="Destination IP Address or Subnet")

    @validator("startingPoint", "destinationPoint")
    def _valid_ip(cls, v):
        if not isinstance(v, IPv4Interface):
            raise ValueError(f'IP "{v}" not a valid IP Address or Subnet')
        return v

    def parameters(self, swap: bool = False):
        parameters = self.base_parameters()
        parameters.update(
            dict(
                pathLookupType="unicast",
                networkMode=self._check_subnets(),
                startingPoint=self.startingPoint.with_prefixlen,
                destinationPoint=self.destinationPoint.with_prefixlen,
            )
        )
        return self.swap_src_dst(parameters) if swap else parameters

    def _check_subnets(self) -> bool:
        """
        Checks for valid IP Addresses or Subnet
        :param ips: ip addresses
        :return: True if a subnet is found to set to networkMode, False if only hosts
        """
        masks = {ip.network.prefixlen for ip in [self.startingPoint, self.destinationPoint]}
        return True if masks != {32} else False


class Host2GW(BaseModel):
    startingPoint: Union[IPv4Address, str]
    vrf: Optional[str] = None

    @validator("startingPoint")
    def _valid_ip(cls, v):
        if v and not isinstance(v, IPv4Address):
            raise ValueError(f'IP "{v}" not a valid IP Address')
        return v

    def parameters(self):
        parameters = dict(
            pathLookupType="hostToDefaultGW",
            type="pathLookup",
            groupBy="siteName",
            startingPoint=str(self.startingPoint),
        )
        if self.vrf:
            parameters["vrf"] = self.vrf
        return parameters


class Layout(BaseModel):
    path: str
    layout: str

    @validator("layout")
    def _valid_layout(cls, v):
        if v and v not in VALID_LAYOUTS:
            raise ValueError(f'Layout "{v}" is not in the valid layouts of {VALID_LAYOUTS}')
        return v


class Network(BaseModel):
    sites: Optional[Union[str, List[str]]] = [ALL_NETWORK]
    all_network: Optional[bool] = Field(False, description="Show all sites as clouds, UI option 'All Network'")
    layouts: Optional[List[Layout]] = None
    technologies: Optional[Technologies] = None

    @validator("sites")
    def _format_paths(cls, v):
        if isinstance(v, str):
            return [v]
        return v

    def parameters(self):
        parameters = dict(type="topology", groupBy="siteName", paths=self.sites.copy())
        if self.all_network and ALL_NETWORK not in parameters["paths"]:
            parameters["paths"].append(ALL_NETWORK)
        if self.layouts:
            parameters["layouts"] = [vars(l) for l in self.layouts]
        if self.technologies:
            parameters["technologies"] = self.technologies.technologies_parameters()
        return parameters
