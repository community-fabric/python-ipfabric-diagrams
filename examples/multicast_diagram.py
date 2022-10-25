"""
multicast_diagram.py
"""
from ipfabric_diagrams import IPFDiagram, Multicast

if __name__ == '__main__':
    ipf = IPFDiagram(snapshot_id='$prev')
    multi = Multicast(source='10.33.230.2', group='232.1.1.1', receiver='10.33.255.109', securedPath=False)
    json_data = ipf.diagram_json(multi)

    model_data = ipf.diagram_model(multi)

    png_data = ipf.diagram_png(multi)
    with open('tmp/multicast.png', 'wb') as f:
        f.write(png_data)

    ipf.close()
