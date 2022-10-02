from dataclasses import dataclass

from dataclasses_json import dataclass_json

import schemas.event as event_schemas


@dataclass_json
@dataclass
class CreateEventRequest:
    event: event_schemas.EventSchema


@dataclass_json
@dataclass
class ApproveEventRequest:
    event_id: str
    user_id: str


@dataclass_json
@dataclass
class GetEventRequest:
    event_id: str
    user_id: str


@dataclass_json
@dataclass
class UserEventsRequest:
    user_id: str
    interval_start_time_iso: str
    interval_duration_sec: int
