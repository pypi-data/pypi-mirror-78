import socket

TCP_IP = '192.168.0.1'
# has probably always the same address
TCP_PORT = 9999
RECV_BYTE_SIZE = 2048


class TcpClient(object):
    """
    opens a socket for every object and close it after using
    an object of the class TcpClient can call the methods send or recv for TCP-communication
    """

    def __init__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.connect((TCP_IP, TCP_PORT))

    def __del__(self):
        self._socket.close()

    def send(self, encoded_message):
        self._socket.send(encoded_message)

    def recv(self):
        recv_bytes = self._socket.recv(RECV_BYTE_SIZE)
        return recv_bytes
