# system modules
import csv
import operator
import socket
import re
import struct

# internal modules

# external modules


def walk(d, b=tuple()):
    """
    Generator recursing into a nested dictionary

    Args:
        d (dict): the arbitraryly-nested dictionary to recurse into
        b (flat tuple): tuple of layers to prepend. You should not need to
            specify this as it is used to store the recursion state.

    Yields:
        layers, deepestelement: tuple of recursed layers and the deepest
            element
    """
    if hasattr(d, "items"):
        for k, v in d.items():
            for m in walk(v, b + (k,)):
                yield m
    elif isinstance(d, str):
        yield (b, d)
    else:
        try:
            for i in iter(d):
                for i in walk(i, b):
                    yield i
        except TypeError:
            yield (b, d)


def default_gateway(wireless=True, ethernet=False):
    """
    Generator parsing ``/proc/net/route`` and yielding the default gateway as
    string.

    Args:
        wireless (bool, optional): whether to include wireless interfaces (i.e.
            interface names starting with ``w``)
        ethernet (bool, optional): whether to include ethernet interfaces (i.e.
            interface names starting with ``e``)

    Yields:
        str, str: the interface name and the :any:`struct.ntoa`-formatted IP
            address

    .. note::

        Adapted from https://stackoverflow.com/a/6556951
    """
    with open("/proc/net/route") as fh:
        parser = csv.DictReader(map(lambda l: re.sub(r"\s+", ",", l), fh))
        for route in parser:
            try:
                iface = route["Iface"]
                destination, flags, gateway = map(
                    lambda k: int(route[k], 16),
                    ("Destination", "Flags", "Gateway"),
                )
                if (
                    iface.startswith("w")
                    and not wireless
                    or iface.startswith("e")
                    and not ethernet
                ):
                    continue
                if destination or not flags & 0b10:
                    continue
                yield iface, socket.inet_ntoa(struct.pack("<L", gateway))
            except (AttributeError, ValueError, TypeError, KeyError):
                continue
