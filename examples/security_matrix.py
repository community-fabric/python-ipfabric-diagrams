"""
security_matrix.py

Project started 26/6/22 DF
Aim: to output a security matrix of subnet-to-subnet connectivity from the latest IPF snapshot
Requires: Rich, ipfabric_diagrams

Takes a list of source IPs/subnets and a list of destination IPs/subnets and for a specific combination of protocol
and ports, tests both the reachability and the applicable security policy, and outputs those results in a Rich table.
"""

from rich.console import Console
from rich.progress import Progress
from rich.table import Table

from ipfabric_diagrams import IPFDiagram, Unicast


def is_reachable(instance, src_ip, dst_ip, prot, src_ports='1025-10000', dst_ports='80'):
    """ takes an IPFDiagram instance and data about the flow to be tested and returns a structure representing
        whether there is a forwarding path from src to dst and that security policy allows the flow - valid values are
        'all', 'part' or 'none' - and if failing a description of the failure point """

    # default the returning values
    failure_desc = ''

    # assemble the request and submit
    path_to_request = Unicast(startingPoint=src_ip, destinationPoint=dst_ip, protocol=prot, srcPorts=src_ports,
                              dstPorts=dst_ports)
    output_json = instance.diagram_json(path_to_request)

    # if pathlookup indicates no forwarding issues and no blocking policy then set return values
    if output_json['pathlookup']['passingTraffic'] == 'all':
        forwards_ok = 'all'
        allowed = 'all'
    else:
        # otherwise grab failure counts
        forwarding_errors = output_json['pathlookup']['eventsSummary']['topics']['FORWARDING']
        acl_errors = output_json['pathlookup']['eventsSummary']['topics']['ACL']
        zonefw_errors = output_json['pathlookup']['eventsSummary']['topics']['ZONEFW']

        # no forwarding errors occurred if all counts are zero
        if forwarding_errors == {'0': 0, '10': 0, '20': 0, '30': 0}:
            forwards_ok = 'all'
        # otherwise all traffic blocked if there are no green/amber/blue counts
        elif forwarding_errors['0'] + forwarding_errors['10'] + forwarding_errors['20'] == 0:
            forwards_ok = 'none'
        # and if there are green/amber/blue then we can assume partial forwarding
        else:
            # breakpoint()
            forwards_ok = 'part'

        # if no traffic allowed to be forwarded, then security policy is irrelevant
        if forwards_ok != 'none':
            # otherwise use the "part" or "all" from the pathlookup
            allowed = output_json['pathlookup']['passingTraffic']

            # and catch the security policy that is failing some/all of the traffic
            if acl_errors != {'0': 0, '10': 0, '20': 0, '30': 0}:
                failure_desc += '+ACL'
            if zonefw_errors != {'0': 0, '10': 0, '20': 0, '30': 0}:
                failure_desc += '+ZONEFW'
        else:
            allowed = 'n/a'

    # assemble JSON for return
    return {'forwarding': forwards_ok, 'allowed_by_policy': allowed, 'failure_description': failure_desc}


def reachability_matrix(ipfd, src_list, dst_list, prot, src_ports, dst_ports):
    """ takes an IPF Diagram instance, and checks reachability from a list of sources to a list of destinations for a
        given protocol and ports. Returns a list of list of results - first item is the list of tested destinations then
        each subsequent item is a list of results for a given source """

    with Progress(transient=True) as progress:
        tasks = len(src_list) * len(dst_list)
        bar = progress.add_task('Working', total=tasks)

        # Initialize first row
        output_matrix = [['src_addr', 'protocol', 'src_port']]

        # then add column headings for destinations
        for dest in dst_list:
            output_matrix[0].append(dest + ' :' + dst_ports)

        # Loop through sources and test to each destination
        for source in src_list:
            # create temporary row
            temp_row = [source, prot, src_ports]

            # Loop through destinations and test reachbility from source to dest
            for dest in dst_list:
                temp_row.append(is_reachable(ipfd, source, dest, prot, src_ports, dst_ports))
                progress.update(bar, advance=1)

            # append the temp row to the final output.
            output_matrix.append(temp_row)

    return output_matrix


def print_matrix(reach_matrix, title='Reachability Matrix'):
    """ takes the output of the reachabilityMatrix function and outputs it as a Rich Text table using Will McGugan's
        Rich project """

    # start assembling the table
    out_table = Table(title='\n' + title)

    # iterate and create columns
    for column in reach_matrix[0]:
        out_table.add_column(column, justify='center')

    # for each group of reachability tests, build a list of cells for the table
    for row in reach_matrix[1:]:
        # grab the data about the sources
        build_row = [row[0], row[1], row[2]]

        # then the reachability and security success or otherwise for each destination
        for col in row[3:]:
            cell = ''
            if col['forwarding'] == 'all':
                cell = '[green]:heavy_check_mark:'
            elif col['forwarding'] == 'part':
                cell = '[gold]O'
            elif col['forwarding'] == 'none':
                cell = '[red]X'
            if col['allowed_by_policy'] == 'all':
                cell += ' [green]:heavy_check_mark:'
            elif col['allowed_by_policy'] == 'part':
                cell += ' [gold]O'
            elif col['allowed_by_policy'] == 'none':
                cell += ' [red]X'
            build_row.append(cell)

        # add it to the table
        out_table.add_row(*build_row)

    # then output the table itself
    console = Console()
    console.print(out_table)

    return True


if __name__ == "__main__":
    # Open session to IP Fabric instance
    # ipfd=IPFDiagram(base_url='https://ipfinstance.domain/',token='API token',verify=False)
    ipfd = IPFDiagram(verify=False, snapshot_id='$last')

    # Can now call isReachable directly eg
    # print(isReachable(ipfd,'10.48.132.19','10.66.124.110','tcp','1024-10000','80'))

    src_list = ['10.48.132.19', '10.47.116.102', '10.35.123.191', '10.34.250.3', '10.10.10.10', '10.36.135.0/24']
    dst_list = ['10.66.123.0/24', '10.66.124.0/24', '10.66.126.0/24', '8.8.8.8', '10.193.132.193']
    result = reachability_matrix(ipfd, src_list, dst_list, 'tcp', '1024-10000', '80')
    print_matrix(result, title="Test Matrix")
