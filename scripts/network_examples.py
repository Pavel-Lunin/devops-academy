"""Offline author examples. No sockets, subprocesses, files, or lab answers."""
import argparse
import ipaddress
import json


def layers():
    return {"Ethernet": {"IPv4": {"TCP": {"data": "example"}}}}


def subnet(value):
    interface = ipaddress.IPv4Interface(value)
    network = interface.network
    # Avoid materializing huge lists of addresses; /0 is also safe.
    special = network.prefixlen >= 31
    first = network.network_address if special else network.network_address + 1
    last = network.broadcast_address if special else network.broadcast_address - 1
    return {
        "address": str(interface.ip), "network": str(network),
        "netmask": str(network.netmask), "last_address": str(network.broadcast_address),
        "first_host": str(first), "last_host": str(last),
        "host_count": network.num_addresses if special else network.num_addresses - 2,
    }


def choose_route(destination, routes):
    """One-table IPv4 model; no policy routing, metrics, ECMP, or host changes."""
    address = ipaddress.IPv4Address(destination)
    matches = []
    for prefix, gateway, interface in routes:
        network = ipaddress.IPv4Network(prefix)
        if gateway is not None:
            ipaddress.IPv4Address(gateway)
        if not interface:
            raise ValueError("interface is required")
        if address in network:
            matches.append((network, gateway, interface))
    if not matches:
        return None
    longest = max(item[0].prefixlen for item in matches)
    best = [item for item in matches if item[0].prefixlen == longest]
    if len(best) != 1:
        raise ValueError("equal prefixes are outside this model")
    network, gateway, interface = best[0]
    return {"prefix": str(network), "next_hop": gateway or str(address),
            "interface": interface, "direct": gateway is None}


def route_example():
    return choose_route("198.51.100.13", [
        ("192.0.2.0/24", None, "e0"),
        ("198.51.100.0/25", "192.0.2.2", "e0"),
        ("0.0.0.0/0", "192.0.2.1", "e0"),
    ])


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("layers")
    commands.add_parser("route")
    net = commands.add_parser("subnet")
    net.add_argument("interface", help="IPv4/prefix, author example only")
    args = parser.parse_args(argv)
    try:
        if args.command == "layers":
            result = layers()
        elif args.command == "route":
            result = route_example()
        else:
            result = subnet(args.interface)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
