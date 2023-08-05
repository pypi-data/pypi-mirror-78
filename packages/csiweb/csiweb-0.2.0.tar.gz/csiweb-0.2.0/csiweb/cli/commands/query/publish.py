# system modules
import logging
import random
import itertools
import types
import time
import re
from urllib.parse import urlparse, parse_qs, ParseResult

# internal modules
from csiweb.cli.commands.query.main import query

# external modules
import click
from paho.mqtt.client import Client as MQTTClient

logger = logging.getLogger(__name__)


class Url(click.ParamType):
    name = "url"

    def __init__(self, scheme):
        self.scheme = scheme

    def convert(self, value, param, ctx):
        if value is None or isinstance(value, ParseResult):
            return value
        return urlparse(
            value
            if value.startswith("{}://".format(self.scheme))
            else "{}://{}".format(self.scheme, value),
            scheme=self.scheme,
        )


@query.command(help="Publish data from the CSI web server via MQTT")
@click.option(
    "--host",
    "--broker",
    "-b",
    "brokers",
    help=" ".join(
        re.split(
            r"\s+",
            """
add another MQTT broker to publish the data to. Supports
user:pass@host:port/TOPIC?OPTIONS format, where TOPIC is a topic pattern like
/topic/subtopic/{quantity} where {quantity} will be substituted with the field
name (e.g. T_probe,H2O_mixratio, etc.). OPTIONS (separated by an ampersand &)
can be used to rename quantities to custom names, e.g.
CO2_mixratio=co2&H20_probe=watervapour would rename CO2_mixratio and H20_probe
accordingly. With message=PATTERN the message pattern can be specified. {value}
and {unit} in the PATTERN will be substituted accordingly.  Of multiple
message=PATTERN pairs, the first that works will be used.  With
only=QUANTITY1,QUANTITY2,... or not=QUANTITY3,QUANTITY3,...  the quantities to
publish can be specified.  With interval=SECONDS, the minimum interval between
publishments to the broker can be specified.  This option can be specified
multiple times.
""",
        )
    ),
    type=Url(scheme="mqtt"),
    multiple=True,
    default=list(
        map(
            urlparse,
            (
                "mqtt://localhost:1883/csiweb/{quantity}?"
                "message={value}%20{unit}&message={value}",
            ),
        )
    ),
    show_envvar=True,
)
@click.pass_context
def publish(ctx, brokers):
    ctx.ensure_object(dict)
    query_data = ctx.obj.get("query-data-callback")
    if not query_data:
        ctx.fail("No query-data callback...")

    def broker2client(spec):
        client = MQTTClient("csiweb-{}".format(random.randint(1, 2 ** 16 - 1)))
        client.username_pw_set(spec.username, spec.password)
        client._topic_template = (
            re.sub(r"^/", "", spec.path) if spec.path else "csiweb/{quantity}"
        )
        params = parse_qs(spec.query or "")
        client._message_templates = params.pop(
            "message", ("{value} {unit}", "{value}")
        )

        def topic(client, **kwargs):
            return client._topic_template.format(**kwargs)

        def message(client, **kwargs):
            for template in client._message_templates:
                try:
                    yield template.format(**kwargs)
                except (ValueError, KeyError, TypeError):
                    continue

        client.topic = types.MethodType(topic, client)
        client.message = types.MethodType(message, client)
        client._publish_interval = max(
            map(float, params.pop("interval", tuple())), default=0
        )
        client._only = set(
            itertools.chain.from_iterable(
                map(
                    lambda x: re.split(r"\s*,\s*", x),
                    params.pop("only", tuple()),
                )
            )
        )
        client._not = set(
            itertools.chain.from_iterable(
                map(
                    lambda x: re.split(r"\s*,\s*", x),
                    params.pop("not", tuple()),
                )
            )
        )
        client._rename_mapping = {k: v[-1] for k, v in params.items()}
        client.connect_async(spec.hostname, spec.port or 1883)
        return client

    def start_client(client):
        logger.info(
            "Starting MQTT client {client._client_id} connecting to "
            "broker {client._host}:{client._port}...".format(client=client)
        )

        def on_connect(client, userdata, flags, rc):
            if rc:
                logger.error(
                    "Client {client._client_id} couldn't connect to "
                    "{client._host}:{client._port}: result code {rc}".format(
                        rc=rc, client=client
                    )
                )
            else:
                logger.info(
                    "Client {client._client_id} now connected to "
                    "{client._host}:{client._port}".format(client=client)
                )

        client.on_connect = on_connect
        client._last_publishment = 0
        client.loop_start()
        return client

    clients = tuple(map(start_client, map(broker2client, brokers)))

    for queried_data in map(tuple, query_data()):
        for client in filter(
            lambda c: (time.time() - getattr(c, "_last_publishment", 0))
            > getattr(c, "_publish_interval", 0),
            clients,
        ):
            for quantity, data in filter(
                lambda qd: (
                    ((qd[0] in client._only) if client._only else True)
                    and qd[0] not in client._not
                ),
                queried_data,
            ):
                quantity = client._rename_mapping.get(quantity, quantity)
                try:
                    data_iter = iter(
                        (data,) if isinstance(data, str) else data
                    )
                except TypeError:
                    data_iter = iter((data,))
                data_info = dict(
                    filter(
                        lambda x: x[1] is not None,
                        map(
                            lambda x: (x, next(data_iter, None)),
                            ("value", "unit"),
                        ),
                    )
                )
                topic = client.topic(quantity=quantity)
                message = next(client.message(**data_info), data)
                logger.debug(
                    "Publishing {topic} = {message} to "
                    "broker {client._host}:{client._port}".format(
                        topic=topic, message=message, client=client
                    )
                )
                client.publish(topic, message)
            client._last_publishment = time.time()
