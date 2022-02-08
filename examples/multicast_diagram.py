"""
multicast_diagram.py
"""
from ipfabric_diagrams import IPFDiagram, PathLookupSettings, Multicast

if __name__ == '__main__':
    ipf = IPFDiagram()
    uni = Multicast(source='10.241.1.203', group='10.35.253.58')
    settings = PathLookupSettings()
    test = ipf.diagram_json(uni, graph_settings=settings)
