from typing import Union

from ipfabric.api import IPFabricAPI

from ipfabric_diagrams.input_models.graph_parameters import Unicast, Multicast, Host2GW, Network
from ipfabric_diagrams.input_models.graph_settings import NetworkSettings, PathLookupSettings, GraphSettings, Overlay, \
    GroupSettings
from ipfabric_diagrams.output_models.graph_result import Edge, Node

GRAPHS_URL = "graphs/"


class IPFDiagram(IPFabricAPI):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _query(
        self,
        parameters: dict,
        snapshot_id: str = None,
        overlay: Overlay = None,
        image: str = None,
        graph_settings: Union[NetworkSettings, PathLookupSettings, GraphSettings] = None,
    ):
        """
        Submits a query, does no formating on the parameters.  Use for copy/pasting from the webpage.
        :param parameters: dict: Dictionary to submit in POST.
        :return: list: List of Dictionary objects.
        """
        url = GRAPHS_URL + image if image else GRAPHS_URL
        payload = dict(parameters=parameters, snapshot=snapshot_id or self.snapshot_id)
        if overlay:
            if overlay.type == "compare" and overlay.snapshotToCompare not in self.snapshots:
                raise ValueError(f"Snapshot {overlay.snapshotToCompare} not found in IP Fabric.")
            payload["overlay"] = overlay.overlay(self.os_version)
        if graph_settings:
            payload["settings"] = graph_settings.settings(self.os_version)
        res = self.post(url, json=payload)
        res.raise_for_status()
        return res.content if image else res.json()

    def diagram_json(
        self,
        parameters: Union[Unicast, Multicast, Host2GW, Network],
        snapshot_id: str = None,
        overlay: Overlay = None,
        graph_settings: Union[NetworkSettings, PathLookupSettings, GraphSettings] = None,
    ) -> dict:
        return self._query(
            parameters.parameters(self.os_version),
            snapshot_id=snapshot_id,
            overlay=overlay,
            graph_settings=graph_settings,
        )

    def diagram_svg(
        self,
        parameters: Union[Unicast, Multicast, Host2GW, Network],
        snapshot_id: str = None,
        overlay: Overlay = None,
        graph_settings: Union[NetworkSettings, PathLookupSettings, GraphSettings] = None,
    ) -> bytes:
        return self._query(
            parameters.parameters(self.os_version),
            snapshot_id=snapshot_id,
            overlay=overlay,
            image="svg",
            graph_settings=graph_settings,
        )

    def diagram_png(
        self,
        parameters: Union[Unicast, Multicast, Host2GW, Network],
        snapshot_id: str = None,
        overlay: Overlay = None,
        graph_settings: Union[NetworkSettings, PathLookupSettings, GraphSettings] = None,
    ) -> bytes:
        return self._query(
            parameters.parameters(self.os_version),
            snapshot_id=snapshot_id,
            overlay=overlay,
            image="png",
            graph_settings=graph_settings,
        )

    def diagram_model(
            self,
            parameters: Union[Unicast, Multicast, Host2GW, Network],
            snapshot_id: str = None,
            overlay: Overlay = None,
            graph_settings: Union[NetworkSettings, PathLookupSettings, GraphSettings] = None,
    ):
        json_data = self.diagram_json(parameters, snapshot_id, overlay, graph_settings)
        if isinstance(parameters, Network):
            return self._diagram_network(json_data)

    @staticmethod
    def _diagram_network(json_data: dict) -> (dict, dict):
        net_settings = GraphSettings(**json_data['graphResult']['settings'])
        edge_type = dict()
        for edge in net_settings.edges:
            edge_type[edge.id] = edge
            if isinstance(edge, GroupSettings):
                for child in edge.children:
                    edge_type[child.id] = child

        edges, nodes = dict(), dict()
        for node_id, node in json_data['graphResult']['graphData']['nodes'].items():
            nodes[node_id] = Node(**node)
        for edge_id, edge_json in json_data['graphResult']['graphData']['edges'].items():
            edge = Edge(**edge_json)
            edge.edgeSettings = edge_type[edge.edgeSettingsId]
            if edge.source:
                edge.source = nodes[edge.source]
            if edge.target:
                edge.target = nodes[edge.target]
            edges[edge_id] = edge

        return edges, nodes
