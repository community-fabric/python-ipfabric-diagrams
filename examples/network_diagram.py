"""
network_diagram.py
"""
from ipfabric_diagrams import IPFDiagram, Network, NetworkSettings, VALID_NET_PROTOCOLS


if __name__ == '__main__':
    ipf = IPFDiagram()

    net = Network(sites=['MPLS', 'LAB01'], all_network=True)
    json_data = ipf.diagram_json(net)

    settings = NetworkSettings()
    settings.hide_protocol('xdp')
    png_data = ipf.diagram_png(net, graph_settings=settings)
    with open('network.png', 'wb') as f:
        f.write(png_data)

    settings.ungroup_group('Layer 3')
    svg_data = ipf.diagram_svg(net, graph_settings=settings)
    with open('network.svg', 'wb') as f:
        f.write(svg_data)

    settings = NetworkSettings()
    for proto in VALID_NET_PROTOCOLS:
        settings.ungroup_protocol(proto)
    edges, nodes = ipf.diagram_model(Network(sites='MPLS'), graph_settings=settings)

    ipf.close()
