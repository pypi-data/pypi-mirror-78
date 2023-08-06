from typing import Dict
import logging

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

logger = logging.getLogger(__name__)


def validate_temperature(reading: Dict, valid_range: Dict) -> Dict:
    """
    Remove any fields that fall outside like values.
    The ds18b20 returns -127.0 when not connected.

    If a reading has `temperature` in the name, it will be checked, if it falls outside
    the correct range delete it.

>>> validate_temperature({'temperature': '-127.0', 'light': '100'}, \
{'maximum': '50', 'minimum': '-5'})
{'light': 100}
>>> validate_temperature({'temperature': '25.0', 'light': '100'}, \
{'maximum': '50', 'minimum': '-5'})
{'temperature': 25.0, 'light': 100}
>>> validate_temperature({'temperature': '75.0', 'light': '100'}, \
{'maximum': '50', 'minimum': '-5'})
{'light': 100}
    """
    cleaned_data = {}
    for name, value in reading.items():

        try:
            value = float(value)
            max_value = float(valid_range['maximum'])
            min_value = float(valid_range['minimum'])

            if 'temperature' in name:
                if value == -127.0:
                    logger.error(
                        'Invalid reading from ds18b20 sensor of -127.0 '
                        'Please ensure the sensor is connected correctly.'
                    )
                    continue
                elif not value <= max_value or value < min_value:
                    logger.error(
                        f'Reading {value} is outside the configured range '
                        f'{min_value} -> {max_value}'
                    )
                    continue
        except ValueError:
            # bypass any plain text fields
            pass
        cleaned_data[name] = value

    return cleaned_data


if __name__ == "__main__":
    import doctest

    doctest.testmod()
