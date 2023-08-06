import base64
import unittest

from wifimeter.util.coder import decode, encode


class TestCoder(unittest.TestCase):
    def setUp(self):
        self.message = "{\"system\":{\"get_sysinfo\":null},\"emeter\":{\"get_realtime\":null}}"
        self.byte_array = base64.b64decode("0PKB+Iv/mvfV75S20bTAn+yV5o/hh+jK8J7rh+uWupj9kPWB5Ja0jvXX"
                                           "sNWh/ozpiOSQ+ZTx0+mH8p7yj/I=")

    def test_encode_decode_twice(self):
        result_byte_array = encode(self.message)
        result_after_encode_and_decode = decode(result_byte_array)
        result_byte_array = encode(result_after_encode_and_decode)
        result_after_2_encode_and_decode = decode(result_byte_array)
        self.assertEquals(self.message, result_after_2_encode_and_decode)

    def test_encode(self):
        self.assertEquals(self.byte_array, encode(self.message))

    def test_decode(self):
        self.assertEquals(self.message, decode(self.byte_array))
