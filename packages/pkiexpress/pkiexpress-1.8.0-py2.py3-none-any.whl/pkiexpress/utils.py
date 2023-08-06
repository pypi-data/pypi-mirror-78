import base64
from datetime import datetime
import sys


def _base64_encode_string(value):
    """

    This method is just a wrapper that handle the incompatibility between the
    standard_b64encode() method on versions 2 and 3 of Python. On Python 2, a
    string is returned, but on Python 3, a bytes-class instance is returned.

    """
    value_base64 = base64.standard_b64encode(value)
    if type(value_base64) is str:
        return value_base64
    elif type(value_base64) is bytes or type(value_base64) is bytearray:
        return value_base64.decode('ascii')

def _convert_datetime_from_service(date_string):
    # In Python 2.7
    if sys.version_info[0] == 2:
        # Delete 7th digit of millisecond and UTC timezone
        date_string = date_string[:date_string.find('.')+7]
        date_format = "%Y-%m-%dT%H:%M:%S.%f"

    # In Python 3
    else:
        utc_position = date_string.find('+')
        if utc_position == -1:
            utc_position = date_string.rfind('-')

        # Delete 7th digit of millisecond when it exists
        millisecond_len = utc_position - date_string.find('.')
        if millisecond_len > 7:
            date_string = date_string[:date_string.find('.')+7]+date_string[utc_position:]

        date_format = "%Y-%m-%dT%H:%M:%S.%f%z"

    return datetime.strptime(date_string, date_format)