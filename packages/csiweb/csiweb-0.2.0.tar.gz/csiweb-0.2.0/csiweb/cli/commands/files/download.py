# system modules
import logging
import os

# internal modules
from csiweb.cli.commands.files.main import files

# external modules
import click
import requests


logger = logging.getLogger(__name__)


@files.command(help="Download selected files")
@click.option(
    "-d",
    "--directory",
    help="output directory",
    default=os.getcwd(),
    show_default="current directory",
    show_envvar=True,
)
@click.option(
    "-f", "--force", is_flag=True, help="also download file if size matches"
)
@click.option(
    "--progress/--no-progress",
    is_flag=True,
    default=True,
    help="Whether to display a progress bar",
)
@click.option(
    "-n",
    "--dry-run",
    is_flag=True,
    help="don't actually download any files or modify any local files",
)
@click.pass_context
def download(ctx, directory, force, progress, dry_run):
    ctx.ensure_object(dict)
    client = ctx.obj["client"]
    for filejson in ctx.obj.get("files", tuple()):
        filepath = filejson.get("path")
        if not filepath:
            continue
        filepath_local = os.path.join(directory, filepath)
        filedir_local, filename_local = os.path.split(filepath_local)
        if not os.path.exists(filedir_local):
            logger.info(
                "Creating output directory {}".format(repr(filedir_local))
            )
            if not dry_run:
                os.makedirs(filedir_local)
        logger.info(
            "Downloading {} to {}".format(
                client.fileurl(filepath),
                os.path.join(filedir_local, filename_local),
            )
        )
        if os.path.exists(filepath_local):
            if not force:
                fstat = os.stat(filepath_local)
                if fstat.st_size == filejson.get("size", 0):
                    logger.info(
                        "File {} exists and already has the expected size {},"
                        " skipping download".format(
                            repr(filepath_local), fstat.st_size
                        )
                    )
                    continue
        if not dry_run:
            client.download_file(
                filepath, target=filepath_local, progress=progress
            )
