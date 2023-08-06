"""
Module for sending data to https://io.adafruit.com/, checkout
https://io.adafruit.com/api/docs/ for more information on the adafruit service.

Example ~/.config/jocasta_config.ini:

[io_adafruit]
username = username
key = api_key_from_adafruit_site

# names of the feeds configured on io.adafruit.com
feeds = office.office-temperature,office.office-light,office.office-humidity

# measurements reported locally.
measurements = temperature,light,humidity

"""


from Adafruit_IO import Client
import logging


logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

logger = logging.getLogger(__name__)


class IOAdafruitConnector(object):
    def __init__(self, key: str, username: str, feeds: str, measurements: str) -> None:
        self.aio = Client(username=username, key=key)
        self.feeds = feeds
        self.measurement_mapping = dict(zip(feeds.split(','), measurements.split(',')))

    def send(self, data):
        """
        Update Adafruit feeds.
        """
        for adafruit_feed, measurement_name in self.measurement_mapping.items():
            logger.info(f'Sending {measurement_name} to AdaFruit.')
            self.aio.send_data(adafruit_feed, data[measurement_name])
