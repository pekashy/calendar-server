import datetime
import enum
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import List, Optional

import datetime
import json


class datetime_encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date, datetime.timedelta)):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


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
    attendees: List[str]
    is_private: bool
    description: str


@dataclass_json
@dataclass
class EventSchema:
    id: str
    created_by: str
    schedule_start: str
    repeat_type: str
    duration_sec: int
    attendees: List[str]
    is_private: bool
    description: str


def get_event_from_schema(event_schema: EventSchema) -> Event:
    return Event(
        event_schema.id, event_schema.created_by,
        datetime.datetime.fromisoformat(event_schema.schedule_start),
        EventRepeatType(event_schema.repeat_type), datetime.timedelta(seconds=event_schema.duration_sec),
        event_schema.attendees, event_schema.is_private, event_schema.description
    )


@dataclass_json
@dataclass
class User:
    id: str
    timezone: Optional[str]
