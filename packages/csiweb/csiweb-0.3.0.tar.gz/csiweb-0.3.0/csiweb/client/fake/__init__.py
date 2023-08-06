# system modules
import logging
from unittest.mock import Mock
import pkg_resources
from functools import partial
import re
import os

# internal modules
from csiweb.client import Client

# external modules
import attr
from requests.models import Response

logger = logging.getLogger(__name__)


@attr.s
class FakeClient(Client):
    """
    Class faking a :any:`Client` for simulation purposes.
    """

    @property
    def session(self):
        raise NotImplemented(
            "{cls.__name__} FAKEs the client, thus no session!".format(
                cls=type(self)
            )
        )

    @staticmethod
    def sanitize(fname):
        return re.sub(r"-+", "-", re.sub(r"\W+", "-", fname))

    @staticmethod
    def dict2str(d):
        return "-".join(
            map(lambda x: "-".join(map(str, x)), sorted(d.items()))
        )

    def response_filename(self, cmd, params={}, **kwargs):
        params = params.copy()
        params.update(kwargs)

        def p2s(p=params):
            return self.sanitize(self.dict2str(p)).lower()

        specs = []
        specs.append("{}.dat".format(p2s({**params, **{"command": cmd}})))
        specs.append("{}-{}.dat".format(cmd, p2s()))
        fmt = params.pop("format", "dat")
        specs.append("{}.{}".format(p2s({**params, **{"command": cmd}}), fmt))
        specs.append("{}-{}.{}".format(cmd, p2s(), fmt))
        return filter(
            os.path.exists,
            filter(
                bool,
                map(partial(pkg_resources.resource_filename, __name__), specs),
            ),
        )

    def command(self, cmd, params={}, **kwargs):
        logger.info(
            "Got {} command request with params {}".format(
                cmd, {**params, **kwargs}
            )
        )
        response_filename = next(
            self.response_filename(cmd, params=params, **kwargs), None
        )
        response = Response()
        if response_filename:
            logger.info(
                "answering with file {}".format(repr(response_filename))
            )
            response.code = "ok"
            response.status_code = 200
            with open(response_filename, "rb") as fh:
                response._content = fh.read()
        else:
            logger.warning("no file found for request")
            response.code = "not-found"
            response.error_code = "not-found"
            response.status_code = 404
        return response
