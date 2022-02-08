"""
unicast_diagram.py
"""
from ipfabric_diagrams import IPFDiagram, PathLookupSettings, Host2GW

if __name__ == '__main__':
    ipf = IPFDiagram()
    h2g = Host2GW(startingPoint='10.241.1.203')
    json_data = ipf.diagram_json(h2g)

    settings = PathLookupSettings()
    png_data = ipf.diagram_png(h2g, graph_settings=settings)
    with open('host2gw.png', 'wb') as f:
        f.write(png_data)

    svg_data = ipf.diagram_svg(h2g)
    with open('host2gw.svg', 'wb') as f:
        f.write(svg_data)
