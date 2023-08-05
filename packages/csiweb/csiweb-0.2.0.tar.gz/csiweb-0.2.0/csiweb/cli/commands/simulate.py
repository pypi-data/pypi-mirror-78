# system modules
import logging
import sys
import time
import json
from collections import OrderedDict
from urllib.parse import urlunsplit

# internal modules
from csiweb.cli.commands.main import cli

# external modules
import requests
import click


logger = logging.getLogger(__name__)


@cli.group(invoke_without_command=True)
@click.option(
    "--ip",
    "--host",
    "csiweb_host",
    help="CSI web server hostname or IP",
    default="192.168.67.1",
    show_envvar=True,
)
@click.option(
    "-i",
    "--interval",
    "query_interval",
    help="Interval between queries in seconds",
    type=click.IntRange(min=1, clamp=True),
    default=None,
    show_envvar=True,
)
@click.pass_context
def query(ctx, csiweb_host, query_interval):
    """
    Query CSI web server data
    """
    ctx.ensure_object(dict)

    def query_data_single():
        url = urlunsplit(("http", csiweb_host, "tables.html", "", ""))
        with requests.session() as session:
            server_response = session.get(
                url,
                # We use an OrderedDict because the server needs the first
                # parameter to be "command" for some reason...
                params=OrderedDict(
                    (
                        ("command", "DataQuery"),
                        ("mode", "most-recent"),
                        ("format", "json"),
                        ("uri", "dl:Public"),
                        ("p1", 25),
                    ),
                    timeout=5,
                ),
            )
            response = server_response.json()
        for field, value in zip(
            response["head"]["fields"], response["data"][0]["vals"]
        ):
            topic = field["name"]
            message = (
                value if "units" not in field else (value, field["units"])
            )
            yield topic, message

    def query_data():
        while True:
            yield query_data_single()
            if query_interval is None:
                break
            else:
                time.sleep(query_interval)

    ctx.obj["query-data"] = query_data
    if ctx.invoked_subcommand is None:
        for queried_data in map(dict, query_data()):
            click.echo(json.dumps(queried_data, indent=4, sort_keys=True))
