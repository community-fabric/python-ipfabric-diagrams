"""
network_diagram.py
"""
from ipfabric_diagrams import IPFDiagram, Network, NetworkSettings

if __name__ == '__main__':
    ipf = IPFDiagram()

    net = Network(sites='MPLS')
    network = ipf.diagram_json(net, graph_settings=NetworkSettings())
