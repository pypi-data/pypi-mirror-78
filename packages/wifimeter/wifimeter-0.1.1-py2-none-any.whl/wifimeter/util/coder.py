CODING_START_CHAR = 171

try:
    from itertools import izip
except ImportError:
    izip = zip


def decode(recv_bytes):
    """
    decodes the received byte_array to a string
    :param recv_bytes: byte_array; received from the device
    """
    recv_bytes = bytearray(recv_bytes)
    first_symbol = chr(CODING_START_CHAR)
    first_symbol = chr(recv_bytes[0] ^ ord(first_symbol))
    decoded_array = [chr(x ^ y) for x, y in izip(recv_bytes, recv_bytes[1:])]
    return first_symbol + "".join(decoded_array)


def encode(message_str):
    """
    encodes the message to a byte_array
    :param message_str: string in format json
    """
    ord_array = map(ord, message_str)
    message_byte = [CODING_START_CHAR]
    for c, s in izip(message_byte, ord_array):
        message_byte.append(c ^ s)
    return bytearray(message_byte[1:])
