"""
Generic collector code to run config file
"""
from typing import Dict

from tabulate import tabulate

from jocasta.inputs.serial_connector import SerialSensor

from jocasta.connectors import file_system, influx, io_adafruit

# io_adafruit, influx
from jocasta.command_line.setup import setup_config, convert_config_stanza
import click
import logging

from jocasta.validators import validate_temperature

LEVELS = {
    'critical': logging.CRITICAL,
    'error': logging.ERROR,
    'warn': logging.WARNING,
    'warning': logging.WARNING,
    'info': logging.INFO,
    'debug': logging.DEBUG,
}


@click.command()
@click.option('--port', '-p', type=click.Path(exists=True))
@click.option('--config-file', '-c', required=False, type=click.Path(exists=True))
@click.option('--log-level', '-l', default='error')
def main(port, config_file, log_level):

    level = LEVELS.get(log_level)
    logging.basicConfig(
        level=level,
        format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    logger = logging.getLogger(__name__)
    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    for logger in loggers:
        logger.setLevel(level)

    logger.debug('Starting...')
    sensor_reader = SerialSensor(port=port)

    reading = sensor_reader.read()

    if reading:
        logger.debug(f'Reading: {reading}')
        config = setup_config(ini_file=config_file)

        connectors: Dict = setup_connectors(config=config)

        display_table(reading)
        if 'temperature_ranges' in config:
            reading = validate_temperature(
                reading, convert_config_stanza(config['temperature_ranges'])
            )
        for name, connector in connectors.items():
            connector.send(data=reading)
    else:
        print('Unable to get reading.')


def setup_connectors(config):
    connectors = {}
    for name, section in config.items():
        args = convert_config_stanza(section)
        if name == 'file_system':
            connectors[name] = file_system.FileSystemConnector(**args)
        elif name == 'io_adafruit':
            connectors[name] = io_adafruit.IOAdafruitConnector(**args)
        elif name == 'influxdb':
            connectors[name] = influx.InfluxDBConnector(**args)
    return connectors


def display_table(reading: Dict):
    table_data = [
        [i.capitalize() for i in reading.keys()],
        [i for i in reading.values()],
    ]
    print(tabulate(table_data, tablefmt='fancy_grid'))


if __name__ == '__main__':
    main()
