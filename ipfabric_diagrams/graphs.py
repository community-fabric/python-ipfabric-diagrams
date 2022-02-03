from typing import Union
from urllib.parse import urljoin

from ipfabric.api import IPFabricAPI

from ipfabric_diagrams.graph_parameters import Unicast, Multicast, Host2GW, Network, Overlay
from ipfabric_diagrams.graph_settings import NetworkSettings, PathLookupSettings, GraphSettings


class IPFDiagram(IPFabricAPI):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.base_url = urljoin(str(self.base_url), "/graphs")

    def _query(
        self,
        parameters: dict,
        snapshot_id: str = None,
        overlay: Overlay = None,
        image: str = None,
        settings: Union[NetworkSettings, PathLookupSettings, GraphSettings] = None,
    ):
        """
        Submits a query, does no formating on the parameters.  Use for copy/pasting from the webpage.
        :param parameters: dict: Dictionary to submit in POST.
        :return: list: List of Dictionary objects.
        """
        url = image or "/"
        payload = dict(parameters=parameters, snapshot=snapshot_id or self.snapshot_id)
        if overlay:
            if overlay.type == "compare" and overlay.snapshotToCompare not in self.snapshots:
                raise ValueError(f"Snapshot {overlay.snapshotToCompare} not found in IP Fabric.")
            payload["overlay"] = overlay.overlay(self.os_version)
        if settings:
            payload['settings'] = settings.settings(self.os_version)
        res = self.post(url, json=payload)
        res.raise_for_status()
        return res.content if image else res.json()

    def json(
        self,
        parameters: Union[Unicast, Multicast, Host2GW, Network],
        snapshot_id: str = None,
        overlay: Overlay = None,
        settings: Union[NetworkSettings, PathLookupSettings, GraphSettings] = None,
    ):
        return self._query(
            parameters.parameters(self.os_version), snapshot_id=snapshot_id, overlay=overlay, settings=settings
        )

    def svg(
        self,
        parameters: Union[Unicast, Multicast, Host2GW, Network],
        snapshot_id: str = None,
        overlay: Overlay = None,
        settings: Union[NetworkSettings, PathLookupSettings, GraphSettings] = None,
    ):
        return self._query(
            parameters.parameters(self.os_version),
            snapshot_id=snapshot_id,
            overlay=overlay,
            image="svg",
            settings=settings,
        )

    def png(
        self,
        parameters: Union[Unicast, Multicast, Host2GW, Network],
        snapshot_id: str = None,
        overlay: Overlay = None,
        settings: Union[NetworkSettings, PathLookupSettings, GraphSettings] = None,
    ):
        return self._query(
            parameters.parameters(self.os_version),
            snapshot_id=snapshot_id,
            overlay=overlay,
            image="png",
            settings=settings,
        )
