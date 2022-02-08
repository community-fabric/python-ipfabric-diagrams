"""
network_diagram.py
"""
from ipfabric_diagrams import IPFDiagram, Network, NetworkSettings

if __name__ == '__main__':
    ipf = IPFDiagram()

    net = Network(sites='MPLS', all_network=True)
    json_data = ipf.diagram_json(net, graph_settings=NetworkSettings())

    settings = NetworkSettings()
    settings.hide_protocol('xdp')
    png_data = ipf.diagram_png(net, graph_settings=settings)
    with open('network.png', 'wb') as f:
        f.write(png_data)

    settings = NetworkSettings()
    settings.ungroup_group('Layer 3')
    svg_data = ipf.diagram_svg(net, graph_settings=settings)
    with open('network.svg', 'wb') as f:
        f.write(svg_data)

    ipf.close()
