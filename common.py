import datetime
import typing


class DatetimePair(typing.NamedTuple):
    start_datetime: datetime.datetime
    end_datetime: datetime.datetime
