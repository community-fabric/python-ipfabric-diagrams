"""
multicast_diagram.py
"""
from ipfabric_diagrams import IPFDiagram, Multicast

if __name__ == '__main__':
    ipf = IPFDiagram()
    multi = Multicast(source='10.33.230.2', group='233.1.1.1', receiver='10.33.240.201', securedPath=False)
    json_data = ipf.diagram_json(multi)

    model_data = ipf.diagram_model(multi)

    ipf.close()
