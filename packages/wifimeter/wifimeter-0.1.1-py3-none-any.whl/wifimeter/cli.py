from getpass import getpass

import click
import logging
from wifimeter.network.threads import UDPSendThread, UDPRecvThread
from wifimeter.network.udp import UdpClient
from wifimeter.util.coder import encode
from wifimeter.util.model import MeasurementRequest, RelayStateRequest
from wifimeter.util.setup import tcp_setup
import timeout_decorator
import signal


@click.group()
def cli():
    pass


@cli.command()
@click.option('--state', prompt='State (0=OFF / 1=ON )', type=click.Choice(['0', '1']))
def switch(state):
    """
    Switch device ON/OFF
    """
    message_str = RelayStateRequest(int(state)).to_json()
    udp = UdpClient()
    udp.send(encode(message_str))


@cli.command()
def measure():
    """
    Receives readings every second
    """
    print("alias, timestamp, current, total, power, voltage, err_code")
    message_str = MeasurementRequest(None).to_json()
    socket_object = UdpClient()
    s = UDPSendThread(message_str, socket_object)
    r = UDPRecvThread(socket_object)
    s.start()
    r.start()

    def handler(signal, frame):
        for t in [s, r]:
            t.stop()
            t.join(1)
        socket_object.close()
        exit(0)

    signal.signal(signal.SIGINT, handler)

    while True:
        signal.pause()


@cli.command()
@click.option('-a', '--alias')
@click.option('-n', '--wlan-name')
@click.option('-p', '--password')
@click.option('-t', '--wlan-type', type=click.Choice(['0', '1', '2', '3']), help='0 = without any security, 2 = WEP, 3 = WPA')
@click.option('-l', '--log-level', default='DEBUG')
@timeout_decorator.timeout(35)
def setup(wlan_type, wlan_name, alias, password, log_level):
    """
    Setup device (alias, WLAN)
    """
    if alias is None:
        alias = click.prompt('Alias')
    if wlan_name is None:
        wlan_name = click.prompt("Wlan_name")
    if wlan_type is None:
        wlan_type = click.prompt("Wlan-type", type=click.Choice(['0', '1', '2', '3']))
    if wlan_type != '0' and password is None:
        password = getpass()
    setup_logging(log_level)
    wlan_type = int(wlan_type)
    tcp_setup(wlan_type, wlan_name, alias, password)


def setup_logging(log_level):
    """
    Set logging level
    :param log_level: possible choices 'DEBUG', 'WARNING', 'INFO'...
    """
    ext_logger = logging.getLogger("py.warnings")
    logging.captureWarnings(True)
    level = getattr(logging, log_level)
    logging.basicConfig(format="[%(asctime)s] %(levelname)s %(filename)s: %(message)s", level=level)
    if level <= logging.DEBUG:
        ext_logger.setLevel(logging.WARNING)



