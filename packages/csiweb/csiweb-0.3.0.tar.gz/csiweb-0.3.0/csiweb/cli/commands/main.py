# system modules
import logging
import re

# internal modules
from csiweb.client import Client
from csiweb.client.fake import FakeClient
from csiweb import utils

# external modules
import click
import requests

logger = logging.getLogger(__name__)

interface, default_gateway = next(
    utils.default_gateway(wireless=True, ethernet=False), (None, None)
)


@click.group(
    help="Campbell Scientific CSI Web Server client",
    context_settings={
        "help_option_names": ["-h", "--help"],
        "auto_envvar_prefix": "CSIWEB",
    },
)
@click.option(
    "-v",
    "--verbose",
    "verbosity",
    help=(
        "increase the loglevel. "
        "Specifying this option more than 2 times "
        "enables all log messages. More than 3 times doesn't limit "
        "logging to only this package."
    ),
    show_envvar=True,
    count=True,
)
@click.option(
    "-q",
    "--quiet",
    "quietness",
    help="decrease the loglevel",
    show_envvar=True,
    count=True,
)
@click.option(
    "--simulate",
    help="simulate the CSI web server",
    is_flag=True,
    show_envvar=True,
)
@click.option(
    "--ip",
    "--host",
    "host",
    help="CSI web server hostname or IP. "
    + (
        "This option must be specified if no default gateway "
        "could be found on any wireless network interfaces and --simulate "
        "was not specified."
        if default_gateway is None
        else ""
    ),
    default=default_gateway,
    show_default="default gateway on {}: {}".format(
        interface, default_gateway
    ),
    show_envvar=True,
)
@click.option(
    "-p",
    "--port",
    help="Port to use",
    default=80,
    show_envvar=True,
)
@click.option(
    "-u",
    "--user",
    help="Username for authentication",
    show_envvar=True,
)
@click.option(
    "--password",
    help="Password for authentication",
    show_envvar=True,
)
@click.version_option(help="show version and exit")
@click.pass_context
def cli(ctx, quietness, verbosity, simulate, host, port, user, password):
    # set up logging
    loglevel_choices = dict(
        enumerate(
            (
                logging.CRITICAL + 1,
                logging.CRITICAL,
                logging.WARNING,
                logging.INFO,
                logging.DEBUG,
            ),
            -2,
        )
    )
    loglevel = loglevel_choices.get(
        min(
            max(loglevel_choices),
            max(min(loglevel_choices), verbosity - quietness),
        )
    )
    logging.basicConfig(
        level=loglevel,
        format="[%(asctime)s] %(levelname)-8s"
        + (" (%(name)s)" if verbosity >= 3 else "")
        + " %(message)s",
    )
    for n, l in logger.manager.loggerDict.items():
        if (
            not re.match(
                r"csiweb\." if verbosity >= 4 else r"csiweb.cli(?!\w)", n
            )
            and not verbosity > 4
        ):
            l.propagate = False
            if hasattr(l, "setLevel"):
                l.setLevel(logging.CRITICAL + 1)
    # start requests session
    ctx.ensure_object(dict)
    if simulate:
        client = FakeClient(host=host, port=port)
    elif host:
        client = Client(host=host, port=port, username=user, password=password)
    else:
        ctx.fail("Either specify --host/--ip or --simulate")
    ctx.obj["client"] = client
