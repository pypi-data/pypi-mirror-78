import json

from influxdb import InfluxDBClient
import logging
import platform
from typing import Dict, List

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

logger = logging.getLogger(__name__)


class InfluxDBConnector(object):
    def __init__(self, database, password, username, host=None, port=None):

        if not host:
            host = 'localhost'

        if not port:
            port = 8086

        self.influx_client = InfluxDBClient(host, port, username, password, database)

    def send(self, data: Dict, hostname: str = None) -> None:
        """
        Send the data over to the Influx server.
        """
        json_payload = _build_payload(data, hostname=hostname)
        logger.info('Sending payload to InfluxDB server')
        logger.info(json.dumps(json_payload, indent=2))
        self.influx_client.write_points(json_payload)
        logger.info('Payload sent')


def _build_payload(data: Dict, hostname: str = None) -> List:
    """
    Break out each reading into measurements that Influx will understand.
    """
    logger.info('Building payload for Influxdb')
    payload_values = []

    # location isn't a measurement we want to log.
    location = data.pop('location', 'unset location')

    if not hostname:
        hostname = platform.node()

    for name, value in data.items():
        payload = {
            'measurement': name,
            'tags': {'host': hostname, 'location': location},
            'fields': {'value': float(value)},
        }
        payload_values.append(payload)

    return payload_values
