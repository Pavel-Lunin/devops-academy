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


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("layers")
    net = commands.add_parser("subnet")
    net.add_argument("interface", help="IPv4/prefix, author example only")
    args = parser.parse_args(argv)
    try:
        result = layers() if args.command == "layers" else subnet(args.interface)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
