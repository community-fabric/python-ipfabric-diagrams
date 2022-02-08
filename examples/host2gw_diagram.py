"""
unicast_diagram.py
"""
from ipfabric_diagrams import IPFDiagram, PathLookupSettings, Host2GW

if __name__ == '__main__':
    ipf = IPFDiagram()
    uni = Host2GW(startingPoint='10.241.1.203')
    settings = PathLookupSettings()
    test = ipf.diagram_json(uni, graph_settings=settings)
