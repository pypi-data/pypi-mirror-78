import json
from datetime import datetime
from time import tzname
import pytz
from wifimeter.util.coder import decode, encode


class JsonSerializer(object):
    """
    Converts all self.variable of its childes to Json-keys and their values to values in Json
    """
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, separators=(',', ':'), sort_keys=True)


class SetTimeRequest(JsonSerializer):
    """
    Sets the current time in format json. This entry can be sent to the device for its setup
    """
    def __init__(self):
        date = datetime.now(tz=pytz.timezone(tzname[0]))
        self.time = {
            'set_timezone': {
                'year': date.year,
                'month': date.month,
                'mday': date.day,
                'hour': date.hour,
                'min': date.minute,
                'sec': date.second,
                'index': 0
            }
        }

    @staticmethod
    def validate_response(response):
        """
        Checks the response of the device
        :param response: json-string
        """
        try:
            return response['time']['set_timezone']['err_code'] == 0
        except KeyError:
            return False


class SetAliasRequest(JsonSerializer):
    """
    Sets the alias in format json. This entry can be sent to the device for its setup
    """
    def __init__(self, alias):
        self.system = {
            'set_dev_alias': {
                'alias': alias
            }
        }

    @staticmethod
    def validate_response(response):
        """
        Checks the response of the device
        :param response: json-string
        """
        try:
            return response['system']['set_dev_alias']['err_code'] == 0
        except KeyError:
            return False


class SetScheduleRequest(JsonSerializer):
    """
    Resets the schedule (format json). This entry can be sent to the device for its setup
    """
    def __init__(self):
        self.schedule = {
            'get_next_action': None
        }

    @staticmethod
    def validate_response(response):
        """
        Checks the response of the device
        :param response: json-string
        """
        try:
            return response['schedule']['get_next_action']['err_code'] == 0
        except KeyError:
            return False


class SetNetifRequest(JsonSerializer):
    """
    Sets the wlan-name, password and type in format json. This entry can be sent to the device for its setup
    """
    def __init__(self, ssid, password, key_type):
        self.netif = {
            'set_stainfo': {
                'ssid': ssid,
                'password': password,
                'key_type': key_type
            }
        }

    @staticmethod
    def validate_response(response):
        """
        Checks the response of the device
        :param response: json-string
        """
        try:
            return response['netif']['set_stainfo']['err_code'] == 0
        except KeyError:
            return False


class NetifRefresher(JsonSerializer):
    """
    Write a refresh for the wlan in format json. This entry can be sent to the device for its setup
    """
    def __init__(self):
        self.netif = {
            'get_scaninfo': {
                'refresh': 0
            }
        }

    @staticmethod
    def validate_response(response):
        """
        Checks the response of the device
        :param response: json-string
        """
        try:
            return response['netif']['get_scaninfo']['err_code'] == 0
        except KeyError:
            return False


class MeasurementRequest(JsonSerializer):
    """
    Writes a json entry which can be sent to the device to get measurement
    """
    def __init__(self, state):
        self.system = {
                'get_sysinfo': state
        }
        self.emeter = JsonSerializer()
        self.emeter.get_realtime = None
        super(MeasurementRequest, self).__init__()


class RelayStateRequest(JsonSerializer):
    """
    Writes a json entry which can be sent to the device to get the current state of the device
    """
    def __init__(self, state):
        self.system = {
                'set_relay_state': {
                    'state': state
                }
        }
        super(RelayStateRequest, self).__init__()


class EMeterData(object):
    """
    Gets a Json-String and manages the single measurement.
    With the @property-functions is it possible to get the values
    """

    def __init__(self, date, current, total, power, voltage, err_code, alias):
        self._date = date
        self._current = current
        self._total = total
        self._power = power
        self._voltage = voltage
        self._err_code = err_code
        self._alias = alias

    @staticmethod
    def from_json(json_str):
        date = datetime.now(tz=pytz.timezone(tzname[0]))
        json_str = json.loads(json_str)
        measurement = json_str['emeter']['get_realtime']
        alias = json_str['system']['get_sysinfo']['alias']
        return EMeterData(alias,
                          date,
                          measurement['current'],
                          measurement['total'],
                          measurement['power'],
                          measurement['voltage'],
                          measurement['err_code'])

    @property
    def date(self):
        return self._date

    @property
    def current(self):
        return self._current

    @property
    def total(self):
        return self._total

    @property
    def power(self):
        return self._power

    @property
    def voltage(self):
        return self._voltage

    @property
    def err_code(self):
        return self._err_code

    @property
    def alias(self):
        return self._alias


class JSONResponse(object):
    def __init__(self, decoded_str):
        self._decoded_str = decoded_str

    @staticmethod
    def from_encoded(recv_bytes):
        return JSONResponse(decode(recv_bytes))

    @property
    def json(self):
        return self._decoded_str


class JSONRequest(object):
    def __init__(self, encoded_bytes):
        self._encoded_bytes = encoded_bytes

    @staticmethod
    def from_decoded(message_str):
        return JSONRequest(encode(message_str))

    @property
    def byte_array(self):
        return self._encoded_bytes
