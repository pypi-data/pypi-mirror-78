from wifimeter.util.model import JSONResponse, EMeterData
import sys


def output_interface(raw_bytes):
    """
    Prints the measurement on screen
    :param raw_bytes: byteArray from the WlanMeter
    """
    response = JSONResponse.from_encoded(raw_bytes)
    measurement = EMeterData.from_json(response.json)
    print("{}, {}, {}, {}, {}, {}".format(measurement.date, measurement.current, measurement.total,
                                          measurement.power, measurement.voltage, measurement.err_code))


class Unbuffered(object):
    """
    Unbuffered stdout to allow working with the output easily (grep, more,...)
    http://stackoverflow.com/questions/107705/disable-output-buffering
    """

    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        # TODO: "python -m wifimeter measure | grep TestPlug" throws BrokenPipeError in ctrl+c
        self.stream.write(data)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


sys.stdout = Unbuffered(sys.stdout)
