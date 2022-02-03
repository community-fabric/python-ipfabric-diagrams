from typing import Optional, Union
from urllib.parse import urljoin

from ipfabric.api import IPFabricAPI

from ipfabric_diagrams.parameters import Unicast, Multicast, Host2GW, Network


class IPFPath(IPFabricAPI):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.base_url = urljoin(str(self.base_url), '/graphs')

    def _query(self, parameters: dict, snapshot_id: str = None, image: str = None):
        """
        Submits a query, does no formating on the parameters.  Use for copy/pasting from the webpage.
        :param parameters: dict: Dictionary to submit in POST.
        :return: list: List of Dictionary objects.
        """
        url = image or '/'
        res = self.post(url, json=dict(parameters=parameters, snapshot=snapshot_id or self.snapshot_id))
        res.raise_for_status()
        return res.content if image else res.json()

    def json(self, parameter: Union[Unicast, Multicast, Host2GW, Network], snapshot_id: str = None):
        return self._query(parameter.parameters(self.os_version), snapshot_id=snapshot_id)

    def svg(self, parameter: Union[Unicast, Multicast, Host2GW, Network], snapshot_id: str = None):
        return self._query(parameter.parameters(self.os_version), snapshot_id=snapshot_id, image='svg')

    def png(self, parameter: Union[Unicast, Multicast, Host2GW, Network], snapshot_id: str = None):
        return self._query(parameter.parameters(self.os_version), snapshot_id=snapshot_id, image='png')

    def site(
        self,
        site_name: Union[str, list],
        snapshot_id: Optional[str] = None,
        overlay: dict = None,
    ):
        """
        Returns a diagram for a site or sites
        :param site_name: Union[str, list]: A single site name or a list of site names
        :param snapshot_id: str: Optional Snapshot ID
        :param overlay: dict: Optional Overlay dictionary
        :return:
        """
        payload = {
            "parameters": {
                "groupBy": "siteName",
                "layouts": [],
                "paths": [site_name] if isinstance(site_name, str) else site_name,
                "type": "topology",
            },
            "snapshot": snapshot_id or self.snapshot_id,
        }
        if overlay:
            payload["overlay"] = overlay
        return self._query(payload)
