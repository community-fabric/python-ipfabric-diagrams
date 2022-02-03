from typing import Optional, List

from pydantic import BaseModel, validator, Field

VALID_DEV_TYPES = ["aciLeaf", "aciSpine", "ap", "cloudInstance", "cloudTransitHub", "cloudInternetGw", "cloudNatGw",
                   "cloudRouter", "cloudVpnGw", "fex", "fw", "host", "l3switch", "lb", "nx7000", "phone", "router",
                   "securityManagement", "switch", "unknown", "vgw", "waas", "wlc"]


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
    edges: Optional[list] = Field(default_factory=list)
    hiddenDeviceTypes: Optional[List[str]] = Field(default_factory=list)
    pathLookup: Optional[PathLookup] = Field(default_factory=PathLookup)

    @validator('hiddenDeviceTypes')
    def _valid_dev_types(cls, v):
        if v and not all(d in VALID_DEV_TYPES for d in v):
            raise ValueError(f"Device Types '{v}' must be None or in {VALID_DEV_TYPES}.")
        return v

    def setting(self, version: str) -> dict:
        return dict(
            edges=self.edges,
            hiddenDeviceTypes=self.hiddenDeviceTypes,
            pathLookup=vars(self.pathLookup)
        )
