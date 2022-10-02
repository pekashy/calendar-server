from dataclasses import dataclass

from dataclasses_json import dataclass_json

import schemas.event as event_schemas


@dataclass_json
@dataclass
class CreateEventRequest:
    event: event_schemas.EventSchema


@dataclass_json
@dataclass
class GetEventRequest:
    event_id: str
