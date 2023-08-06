# system modules
import os
import logging
from collections import OrderedDict
from urllib.parse import urlunsplit

# internal modules
from csiweb import utils

# external modules
import attr
import tqdm
import requests


logger = logging.getLogger(__name__)


@attr.s
class Client:
    host = attr.ib(
        default=next(
            utils.default_gateway(wireless=True, ethernet=False),
            (None, "192.168.67.1"),
        )[-1]
    )
    port = attr.ib(default=80)
    username = attr.ib(default=None)
    password = attr.ib(default=None)
    timeout = attr.ib(converter=int, type=int, default=5)

    @property
    def session(self):
        try:
            return self._session
        except AttributeError:
            self._session = requests.sessions.Session()
            if self.username and self.password:
                self._session.auth = requests.auth.HTTPBasicAuth(
                    self.username, self.password
                )
        return self._session

    def command(self, cmd, path="/", params={}, **kwargs):
        # We use an OrderedDict because the server needs the first
        # parameter to be "command" for some reason...
        p = OrderedDict()
        p.update(command=cmd)
        p.update(params)
        p.update(kwargs)
        url = urlunsplit(
            ("http", ":".join(map(str, (self.host, self.port))), path, "", "")
        )
        return self.session.get(url, params=p, timeout=self.timeout)

    def dataquery(self, params={}, **kwargs):
        default_params = {
            "mode": "most-recent",
            "format": "json",
            "uri": "dl:Public",
            "p1": 25,
        }
        p = default_params.copy()
        p.update(params)
        p.update(kwargs)
        logger.info("Requesting data")
        return self.command("dataquery", params=p)

    def filesquery(self, path="/", params={}, **kwargs):
        default_params = {"format": "json"}
        p = default_params.copy()
        p.update(params)
        p.update(kwargs)
        logger.info("Requesting file list")
        return self.command("ListFiles", path, params=p)

    def fileurl(self, path):
        return urlunsplit(
            ("http", ":".join(map(str, (self.host, self.port))), path, "", "")
        )

    def download_file(self, path, target, progresscb=lambda b: None):
        url = self.fileurl(path)
        logger.info("Downloading {} to {}".format(url, target))
        with self.session.get(url, stream=True, timeout=self.timeout) as r:
            if r.status_code != requests.codes.ALL_GOOD:
                logger.warning(
                    "Error {} downloading file {}. "
                    "Downloading content anyway.".format(r.status_code, path)
                )
            with open(target, "wb") as f:
                expected_size = int(r.headers.get("Content-Length", 0))
                with tqdm.tqdm(
                    disable=None,
                    unit="byte",
                    unit_scale=True,
                    desc=path,
                    total=expected_size,
                    position=0,
                ) as pbar:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                        pbar.update(len(chunk))
                        if progresscb:
                            progresscb(len(chunk))
            fstat = os.stat(target)
            if fstat.st_size != expected_size:
                logger.warning(
                    "Downloaded file {} has size {} "
                    "but should have been {}!".format(
                        repr(target), fstat.st_size, expected_size
                    )
                )

    def get_recent_data(self):
        response = self.dataquery().json()
        logger.debug("JSON response: {}".format(response))
        for field, value in zip(
            response.get("head", {}).get("fields", tuple()),
            response.get("data", tuple({}))[0].get("vals", tuple()),
        ):
            topic, unit = field.get("name", "?"), field.get("units")
            message = value if unit is None else (value, unit)
            yield topic, message
