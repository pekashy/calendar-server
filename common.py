import datetime
import enum
import typing


class EventRepeatType(enum.Enum):
    SINGLE_MEETING = 'SINGLE_MEETING'
    REPEAT_DAILY = 'REPEAT_DAILY'
    REPEAT_WEEKLY = 'REPEAT_WEEKLY'
    REPEAT_MONTHLY = 'REPEAT_MONTHLY'
    REPEAT_YEARLY = 'REPEAT_YEARLY'
    REPEAT_WORKDAYS = 'REPEAT_WORKDAYS'
    REPEAT_CUSTOM = 'REPEAT_CUSTOM'


class Event(typing.NamedTuple):
    id: str
    repeat_type: EventRepeatType
    schedule_start: datetime.datetime
    duration: datetime.timedelta


class DatetimePair(typing.NamedTuple):
    start_datetime: datetime.datetime
    end_datetime: datetime.datetime
