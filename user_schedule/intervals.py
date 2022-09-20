import datetime
import typing


class SchedulingError(Exception):
    pass


class DatetimeInterval:
    def __init__(self, start_datetime: datetime.datetime, end_datetime: datetime.datetime):
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.date = self.start_datetime.date()
        if self.start_datetime.date() != self.end_datetime.date():
            raise SchedulingError("Multi-date intervals are not supported!")

    def __eq__(self, other):
        return self.start_datetime == other.start_datetime and self.end_datetime == other.end_datetime


class TimeInterval(typing.NamedTuple):
    start_time: datetime.time
    end_time: datetime.time
