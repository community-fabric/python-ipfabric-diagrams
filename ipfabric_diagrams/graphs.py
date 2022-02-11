from typing import Union

from ipfabric.api import IPFabricAPI

from ipfabric_diagrams.input_models.graph_parameters import Unicast, Multicast, Host2GW, Network
from ipfabric_diagrams.input_models.graph_settings import (
    NetworkSettings,
    PathLookupSettings,
    GraphSettings,
    Overlay,
    GroupSettings,
)
from ipfabric_diagrams.output_models.graph_result import NetworkEdge, Node, PathLookupEdge, GraphResult, PathLookup

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
    ) -> GraphResult:
        json_data = self.diagram_json(parameters, snapshot_id, overlay, graph_settings)
        edge_setting_dict = self._diagram_edge_settings(json_data["graphResult"]["settings"])
        if isinstance(parameters, Network):
            return self._diagram_network(json_data, edge_setting_dict)
        else:
            return self._diagram_pathlookup(json_data, edge_setting_dict)

    @staticmethod
    def _diagram_network(json_data: dict, edge_setting_dict: dict, pathlookup: bool = False) -> GraphResult:
        edges, nodes = dict(), dict()
        for node_id, node in json_data["graphResult"]["graphData"]["nodes"].items():
            nodes[node_id] = Node(**node)
        for edge_id, edge_json in json_data["graphResult"]["graphData"]["edges"].items():
            edge = PathLookupEdge(**edge_json) if pathlookup else NetworkEdge(**edge_json)
            edge.edgeSettings = edge_setting_dict[edge.edgeSettingsId]
            if edge.source:
                edge.source = nodes[edge.source]
            if edge.target:
                edge.target = nodes[edge.target]
            edges[edge_id] = edge

        return GraphResult(edges=edges, nodes=nodes)

    def _diagram_pathlookup(self, json_data: dict, edge_setting_dict: dict) -> GraphResult:
        graph_result = self._diagram_network(json_data, edge_setting_dict, pathlookup=True)

        for edge_id, edge in graph_result.edges.items():
            for prev_id in edge.prevEdgeIds:
                edge.prevEdge.append(graph_result.edges[prev_id])
            for next_id in edge.nextEdgeIds:
                edge.nextEdge.append(graph_result.edges[next_id] if next_id in graph_result.edges else next_id)

        graph_result.pathlookup = PathLookup(**json_data["pathlookup"])
        return graph_result

    @staticmethod
    def _diagram_edge_settings(graph_settings: dict) -> dict:
        net_settings = GraphSettings(**graph_settings)
        edge_setting_dict = dict()
        for edge in net_settings.edges:
            edge_setting_dict[edge.id] = edge
            if isinstance(edge, GroupSettings):
                for child in edge.children:
                    edge_setting_dict[child.id] = child
        return edge_setting_dict
