"""
unicast_diagram.py
"""
from ipfabric_diagrams import IPFDiagram, PathLookupSettings, Unicast

if __name__ == '__main__':
    ipf = IPFDiagram()
    uni = Unicast(startingPoint='10.241.1.203', destinationPoint='10.35.253.58')
    settings = PathLookupSettings()
    test = ipf.diagram_json(uni, graph_settings=settings)
