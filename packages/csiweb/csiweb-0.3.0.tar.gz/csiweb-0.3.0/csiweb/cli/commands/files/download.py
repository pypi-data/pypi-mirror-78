# system modules
import logging
import os
import re

# internal modules
from csiweb.cli.commands.files.main import files

# external modules
import click
import requests
import tqdm

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
    "--overwrite",
    "--no-overwrite",
    is_flag=True,
    default=False,
    help="whether to also download file if size matches",
)
@click.option(
    "-n",
    "--dry-run",
    is_flag=True,
    help="don't actually download any files or modify any local files",
)
@click.pass_context
def download(ctx, directory, overwrite, dry_run):
    ctx.ensure_object(dict)
    client = ctx.obj["client"]
    ctx.obj["files"] = tuple(ctx.obj.get("files", tuple()))
    total_pbar = tqdm.tqdm(
        disable=None,
        unit="byte",
        unit_scale=True,
        desc="total",
        total=sum(j.get("size", 0) for j in ctx.obj.get("files", tuple())),
        position=1,
    )
    last_filesize = 0
    for filejson in ctx.obj.get("files", tuple()):
        total_pbar.update(last_filesize)
        last_filesize = filejson.get("size", 0)
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
            if overwrite:
                logger.warning(
                    "Overwriting file {}".format(repr(filepath_local))
                )
            else:
                fstat = os.stat(filepath_local)
                if fstat.st_size == filejson.get("size", 0):
                    logger.info(
                        "File {} exists and already has the expected size {},"
                        " skipping download".format(
                            repr(filepath_local), fstat.st_size
                        )
                    )
                    continue
                else:
                    logger.warning(
                        "File {} exists but has unexpected size {} "
                        "(should be {})".format(
                            repr(filepath_local),
                            fstat.st_size,
                            filejson.get("size", 0),
                        )
                    )
                    backup_filepath_local = filepath_local
                    correct_backup_exists = False
                    while os.path.exists(backup_filepath_local):
                        bak_fstat = os.stat(backup_filepath_local)
                        if bak_fstat.st_size == filejson.get("size", 0):
                            correct_backup_exists = True
                            break
                        m = re.fullmatch(
                            r"(?P<title>.*?)"
                            r"(?:-bak(?P<baknr>\d+))?\.(?P<ext>[^.]+)",
                            backup_filepath_local,
                        )
                        if m:
                            d = m.groupdict()
                            d["baknr_inc"] = (
                                int(d.get("baknr", 0)) + 1
                                if d.get("baknr")
                                else 1
                            )
                            backup_filepath_local = (
                                "{title}-bak{baknr_inc:03d}.{ext}".format(**d)
                            )
                        else:
                            backup_filepath_local += "-bak{:03d}".format(1)
                    if correct_backup_exists:
                        logger.warning(
                            "Backup {} of upstream file {} "
                            "has the right size, "
                            " so skipping download.".format(
                                repr(backup_filepath_local),
                                repr(filepath_local),
                            )
                        )
                        continue
                    else:
                        logger.warning(
                            "Downloading upstream "
                            "file {} to {} instead".format(
                                repr(filepath_local),
                                repr(backup_filepath_local),
                            )
                        )
                        filepath_local = backup_filepath_local
        if not dry_run:
            total_pbar.refresh()
            client.download_file(
                filepath, target=filepath_local, progresscb=total_pbar.update
            )
    total_pbar.close()
