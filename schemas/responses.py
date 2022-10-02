from dataclasses import dataclass
from typing import Optional, Any, Tuple, List

from dataclasses_json import dataclass_json

import schemas.event as event_schemas


@dataclass_json
@dataclass
class Response:
    pass


ServerResponse = Tuple[Any, int, dict[str, str]]


def make_response(status: Optional[int] = 200, data: Optional[Response] = None) -> ServerResponse:
    data_str = ""
    if data:
        data_str = data.to_json()
    return data_str, status, {'ContentType': 'application/json'}


@dataclass_json
@dataclass
class OkResponse(Response):
    message: Optional[str]


@dataclass_json
@dataclass
class BadResponse(Response):
    error_code: str
    message: Optional[str]


@dataclass_json
@dataclass
class GetEventResponse(Response):
    event: Optional[event_schemas.EventSchema]


@dataclass_json
@dataclass
class GetUserEventsResponse(Response):
    events_list: List[str]


@dataclass_json
@dataclass
class FirstFreeIntervalResponse(Response):
    interval_start_time_iso: str

