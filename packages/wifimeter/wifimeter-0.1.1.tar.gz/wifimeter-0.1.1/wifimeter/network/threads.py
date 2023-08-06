import threading
import time

from wifimeter.util.coder import encode
from wifimeter.util.output import output_interface


class UDPSendThread(threading.Thread):
    """
    Sends the message for a measurement request
    :param message_str: message as a json-string; can be send after encoding to the device
    :param socket_object: a object from type UdpClient with an open socket inside
    """
    def __init__(self, message_str, socket_object):
        self._message_str = message_str
        self._udp = socket_object
        super(UDPSendThread, self).__init__()
        self._running = False

    def run(self):
        self._running = True
        while self._running:
            next_send = time.time() + 1
            self.send()
            next_send -= time.time()  # ToDo: not perfect, but it works (probably send a request on every full second)
            time.sleep(next_send)

    def send(self):
        self._udp.send(encode(self._message_str))

    def stop(self):
        self._running = False


class UDPRecvThread(threading.Thread):
    """
    Receives a byte_array from the device on the open socket
    :param socket_object: a object from type UdpClient with an open socket inside
    """
    def __init__(self, socket_object):
        self._udp = socket_object
        super(UDPRecvThread, self).__init__()
        self._running = False

    def run(self):
        self._running = True
        while self._running:
            self.recv()

    def recv(self):
        raw_bytes = self._udp.recv()
        if raw_bytes is not None:
            output_interface(raw_bytes)

    def stop(self):
        self._running = False
