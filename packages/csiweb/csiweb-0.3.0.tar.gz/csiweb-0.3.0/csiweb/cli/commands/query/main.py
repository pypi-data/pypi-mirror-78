# system modules
import logging
import sys
import time
import json

# internal modules
from csiweb.cli.commands.main import cli

# external modules
import click


logger = logging.getLogger(__name__)


@cli.group(
    help="Poll data from the CSI web server", invoke_without_command=True
)
@click.option(
    "-i",
    "--interval",
    "interval",
    help="Interval between queries in seconds",
    type=click.IntRange(min=1, clamp=True),
    default=None,
    show_envvar=True,
)
@click.option(
    "--drop-unit",
    "-U",
    "units_to_drop",
    help="Drop a given unit",
    multiple=True,
    default=["adimensional", "fraction"],
)
@click.pass_context
def query(ctx, interval, units_to_drop):
    """
    Query CSI web serverdata
    """
    ctx.ensure_object(dict)
    client = ctx.obj["client"]

    def drop_units(tm):
        topic, message = tm
        try:
            it = iter((message,) if isinstance(message, str) else message)
        except TypeError:
            it = iter((message,))
        value, unit = map(lambda x: next(it, None), range(2))
        return (
            topic,
            value
            if (unit is None or unit in units_to_drop)
            else (value, unit),
        )

    def query_data():
        time_last_query = 0
        while True:
            if time.time() - time_last_query > (
                0 if interval is None else interval
            ):
                queried_data = tuple(client.get_recent_data())
                yield map(drop_units, queried_data)
                time_last_query = time.time()
            if interval is None:
                break
            time.sleep(0.5)

    ctx.obj["query-data-callback"] = query_data
    if ctx.invoked_subcommand is None:
        for queried_data in map(dict, query_data()):
            click.echo(json.dumps(queried_data, indent=4, sort_keys=True))
