import datetime
from dataclasses import dataclass
from typing import List, Optional, Dict, Any

from dataclasses_json import dataclass_json

import common


@dataclass_json
@dataclass
class EventSchema:
    id: str
    created_by: str
    schedule_start: str
    repeat_type: str
    duration_sec: int
    invited: List[str]
    accepted: List[str]
    is_private: bool
    description: str
    custom_repeat_params: Optional[Dict[str, Any]]


def get_event_from_schema(event_schema: EventSchema) -> common.Event:
    return common.Event(
        id=event_schema.id, created_by=event_schema.created_by,
        schedule_start=datetime.datetime.fromisoformat(event_schema.schedule_start),
        repeat_type=common.EventRepeatType(event_schema.repeat_type),
        duration=datetime.timedelta(seconds=event_schema.duration_sec),
        invited=event_schema.invited, accepted=event_schema.accepted, is_private=event_schema.is_private,
        description=event_schema.description,
        custom_repeat_params=event_schema.custom_repeat_params
    )


def get_schema_from_event(event: common.Event) -> EventSchema:
    return EventSchema(id=event.id, created_by=event.created_by, schedule_start=event.schedule_start.isoformat(),
                       duration_sec=event.duration.seconds,
                       invited=event.invited, accepted=event.accepted, is_private=event.is_private,
                       description=event.description,
                       custom_repeat_params=event.custom_repeat_params, repeat_type=event.repeat_type.value)


@dataclass_json
@dataclass
class UserSchema:
    id: str
    timezone: Optional[str]
