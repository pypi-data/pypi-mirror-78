from datetime import datetime


def iso8601_without_underscore(date=None):
    if date:
        iso8601 = date.replace(microsecond=0).isoformat()
    else:
        iso8601 = datetime.now().replace(microsecond=0).isoformat()
    return iso8601.replace('-', '')
