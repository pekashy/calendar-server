import datetime
import enum
import typing
from dataclasses import dataclass
from typing import List, Dict, Optional, Any


class DatetimePair(typing.NamedTuple):
    start_datetime: datetime.datetime
    end_datetime: datetime.datetime


class EventRepeatType(enum.Enum):
    SINGLE_EVENT = 'SINGLE_EVENT'
    REPEAT_DAILY = 'REPEAT_DAILY'
    REPEAT_WEEKLY = 'REPEAT_WEEKLY'
    REPEAT_MONTHLY = 'REPEAT_MONTHLY'
    REPEAT_YEARLY = 'REPEAT_YEARLY'
    REPEAT_WORKDAYS = 'REPEAT_WORKDAYS'
    REPEAT_CUSTOM = 'REPEAT_CUSTOM'


@dataclass
class Event:
    id: str
    created_by: str
    schedule_start: datetime.datetime
    repeat_type: EventRepeatType
    duration: datetime.timedelta
    invited: List[str]
    accepted: List[str]
    is_private: bool
    description: str
    custom_repeat_params: Optional[Dict[str, Any]]
