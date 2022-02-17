"""
network_diagram.py
"""
from ipfabric_diagrams import IPFDiagram, Network, NetworkSettings, VALID_NET_PROTOCOLS, Layout


if __name__ == '__main__':
    ipf = IPFDiagram()

    net = Network(sites=['MPLS', 'LAB01'], all_network=True)
    json_data = ipf.diagram_json(net)
    model_data = ipf.diagram_model(net)
    with open('tmp/network.png', 'wb') as f:
        f.write(ipf.diagram_png(net))

    settings = NetworkSettings()
    settings.hide_protocol('xdp')
    png_data = ipf.diagram_png(net, graph_settings=settings)
    with open('tmp/network.png', 'wb') as f:
        f.write(png_data)

    settings.ungroup_group('Layer 3')
    svg_data = ipf.diagram_svg(net, graph_settings=settings)
    with open('tmp/network.svg', 'wb') as f:
        f.write(svg_data)

    settings = NetworkSettings()
    for proto in VALID_NET_PROTOCOLS:
        settings.ungroup_protocol(proto)
    settings.hide_group('Layer 1')
    settings.hide_group('Layer 2')
    settings.hide_protocol('rib')
    settings.hide_protocol('ldp')
    settings.hide_protocol('ebgp')
    settings.change_label('ospf', 'subnet')
    mpls = Network(sites='MPLS', layouts=[Layout(path='MPLS', layout='radial')])
    graph_result = ipf.diagram_model(mpls, graph_settings=settings)
    svg_data = ipf.diagram_svg(mpls, graph_settings=settings)
    with open('tmp/network_edited.svg', 'wb') as f:
        f.write(svg_data)

    ipf.close()
