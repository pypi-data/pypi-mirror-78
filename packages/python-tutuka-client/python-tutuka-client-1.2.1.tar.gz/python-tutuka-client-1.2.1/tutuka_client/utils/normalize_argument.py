from datetime import datetime

from tutuka_client.utils import iso8601_without_underscore


def checksum_normalize(argument):
    if isinstance(argument, str):
        return argument
    if isinstance(argument, (int, float)):
        return str(argument)
    if isinstance(argument, datetime):
        return iso8601_without_underscore(argument)
    raise Exception('cant normalize argument')


def date_time_normalize(argument):
    if isinstance(argument, datetime):
        return argument.isoformat()
    return argument
