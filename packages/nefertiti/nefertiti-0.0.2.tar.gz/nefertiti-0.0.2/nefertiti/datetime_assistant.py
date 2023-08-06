import datetime

import dateutil.parser
from pytz import timezone


CST_TZ = timezone('Asia/Shanghai')
UTC_TZ = timezone('UTC')


def datetime_to_string(_datetime, format='%Y-%m-%d %H:%M:%S'):
    """datetime to string"""
    return _datetime.strftime(format) if _datetime else None


def string_to_datetime(datetime_str):
    """string to datetime"""
    try:
        return dateutil.parser.parse(datetime_str)
    except:
        return None


def date_to_datetime(_date):
    """datetime.date to datetime.datetime"""
    return datetime.datetime(_date.year, _date.month, _date.day, 0, 0, 0, 0)


def get_epoch_milli(_datetime=None, is_utc=False):
    """datetime to int"""
    if not _datetime:
        _datetime = datetime.datetime.now()
        is_utc = False
    if is_utc:
        _datetime = _datetime.replace(tzinfo=UTC_TZ)
    return int(_datetime.timestamp() * 1000)


def epoch_milli_to_datetime(ts, return_utc=False):
    """将timestamp转化成datetime

    注意: 如果return_utc=True, 则返回的datetime为UTC时区的时间, 但是它不含有时区信息. 如果直接操作它. python会给他指定本地时区为默认时区!
    """
    if return_utc:
        return datetime.datetime.utcfromtimestamp(ts / 1000)
    return datetime.datetime.fromtimestamp(ts / 1000)
