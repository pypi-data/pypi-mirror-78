from wifimeter.network.tcp import TcpClient
from wifimeter.util.coder import encode, decode
from wifimeter.util.model import SetTimeRequest, SetNetifRequest, NetifRefresher, SetAliasRequest, SetScheduleRequest
import json
import logging


def tcp_setup(wlan_type, wlan_name, alias, password):
    """
    Prepares the data before they can be send to the device
    :param wlan_type: a integer; 0 = without any security, 2 = WEP, 3 = WPA
    :param wlan_name: the name of the required wlan
    :param alias: device name
    :param password: wlan password
    """

    tcp = TcpClient()
    tcp_send(tcp, wlan_type, wlan_name, alias, password)


def tcp_send(tcp, wlan_type, wlan_name, alias, password):
    """
    Sends and receives the TCP-messages for the setup and checks its success
    :param tcp: an object of type TcpClient
    :param wlan_type: a integer; 0 = without security, 2 = WEP, 3 = WPA
    :param wlan_name: the name of the required wlan
    :param alias: device name
    :param password: wlan password
    """
    events = [SetTimeRequest(), SetAliasRequest(alias), NetifRefresher(),
              SetNetifRequest(wlan_name, password, wlan_type), SetScheduleRequest()]
    for req in events:
        tcp.send(encode(req.to_json()))
        decoded_response = json.loads(decode(tcp.recv()))
        logging.debug(decoded_response)
        if not req.validate_response(decoded_response):
            logging.info("invalid err_code")
