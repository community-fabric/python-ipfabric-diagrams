"""
multicast_diagram.py
"""
from ipfabric_diagrams import IPFDiagram, PathLookupSettings, Multicast

if __name__ == '__main__':
    ipf = IPFDiagram()
    multi = Multicast(source='10.241.1.203', group='10.35.253.58', receiver='10.1.1.1')
    settings = PathLookupSettings()
    test = ipf.diagram_json(multi, graph_settings=settings)
