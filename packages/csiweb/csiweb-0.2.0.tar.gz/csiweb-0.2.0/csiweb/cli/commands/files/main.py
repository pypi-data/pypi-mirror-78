# system modules
import logging
import re
import sys
import time
import json

# internal modules
from csiweb.cli.commands.main import cli

# external modules
import click


logger = logging.getLogger(__name__)


@cli.group(help="Access files on the datalogger", invoke_without_command=True)
@click.option(
    "-p",
    "--pattern",
    help="Regular expression to match the WHOLE path",
    default=".*",
    show_default="matches all files",
    show_envvar=True,
)
@click.pass_context
def files(ctx, pattern):
    """
    Access files on the datalogger
    """
    ctx.ensure_object(dict)
    client = ctx.obj["client"]

    def get_files(path="/"):
        for filejson in client.filesquery(path=path).json().get("files", []):
            filepath = filejson.get("path")
            if not filepath or filepath == path:
                continue
            if filejson.get("is_dir"):
                for p in get_files(path=filepath):
                    yield p
            else:
                yield filejson

    regex = re.compile(pattern, flags=re.IGNORECASE)
    ctx.obj["files"] = filter(
        lambda j: regex.search(j.get("path")), get_files()
    )

    if ctx.invoked_subcommand is None:
        for filejson in ctx.obj["files"]:
            click.echo(filejson.get("path"))
