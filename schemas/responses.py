from dataclasses import dataclass
from typing import Optional, Any

from dataclasses_json import dataclass_json

import schemas.event as event_schemas


def make_response(status: Optional[int] = 200, data: Optional[Any] = None) -> tuple[Any, int, dict[str, str]]:
    data_str = ""
    if data:
        data_str = data.to_json()
    return data_str, status, {'ContentType': 'application/json'}


@dataclass_json
@dataclass
class OkResponse:
    message: Optional[str]


@dataclass_json
@dataclass
class BadResponse:
    error_code: str
    message: Optional[str]


@dataclass_json
@dataclass
class GetEventResponse:
    event: Optional[event_schemas.EventSchema]
