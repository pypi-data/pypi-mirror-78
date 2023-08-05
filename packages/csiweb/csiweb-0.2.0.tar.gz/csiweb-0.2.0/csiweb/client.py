# system modules
import logging
from collections import OrderedDict
from urllib.parse import urlunsplit

# internal modules
from csiweb import utils

# external modules
import attr
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
    timeout = attr.ib(converter=int, type=int, default=5)

    @property
    def session(self):
        try:
            return self._session
        except AttributeError:
            self._session = requests.sessions.Session()
        return self._session

    def command(self, cmd, params={}, **kwargs):
        """"""
        # We use an OrderedDict because the server needs the first
        # parameter to be "command" for some reason...
        p = OrderedDict()
        p.update(command=cmd)
        p.update(params)
        p.update(kwargs)
        url = urlunsplit(("http", self.host, "", "", ""))
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
