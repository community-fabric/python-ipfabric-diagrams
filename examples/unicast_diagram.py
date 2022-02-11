"""
unicast_diagram.py
"""
from ipfabric_diagrams import IPFDiagram, PathLookupSettings, Unicast, Algorithm, EntryPoint, OtherOptions

if __name__ == '__main__':
    ipf = IPFDiagram()
    uni = Unicast(
        startingPoint='10.241.1.203',
        destinationPoint='10.35.253.58',
        protocol='tcp',
        tcpFlags=['syn'],
        srcPorts='1024-10000',
        dstPorts='80,443',
        ttl=64,
        fragmentOffset=100
    )

    json_data = ipf.diagram_json(uni)
    model_data = ipf.diagram_model(uni)

    settings = PathLookupSettings()
    settings.increase_priority("ethernet")
    settings.decrease_priority("vxlan")
    print(settings.protocol_priority)
    png_data = ipf.diagram_png(uni, graph_settings=settings)
    with open('unicast.png', 'wb') as f:
        f.write(png_data)

    svg_data = ipf.diagram_svg(uni, graph_settings=settings)
    with open('unicast.svg', 'wb') as f:
        f.write(svg_data)

    uni = Unicast(
        startingPoint='8.8.8.8',
        destinationPoint='10.35.253.58',
        protocol='udp',
        srcPorts='53',
        dstPorts='1025-10000',
        firstHopAlgorithm=Algorithm(entryPoints=[
            EntryPoint(sn="9AMSST2E75V", iface="GigabitEthernet0/0", hostname="L35FW1"),
            EntryPoint(sn="9AJR4UMXS30", iface="GigabitEthernet0/0", hostname="L35FW2")
        ]),
        otherOptions=OtherOptions(applications="(dns)")
    )
    model_data = ipf.diagram_model(uni)
    png_data = ipf.diagram_png(uni)
    with open('unicast-entry.png', 'wb') as f:
        f.write(png_data)

    ipf.close()
