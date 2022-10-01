import datetime
from dataclasses import dataclass
from dataclasses_json import dataclass_json

import common

from typing import List, Optional


@dataclass_json
@dataclass
class Event:
    id: str
    created_by: str
    start_time: datetime.datetime
    duration: datetime.timedelta
    attendees: List[str]
    is_private: bool
    repeat_type:  common.EventRepeatType
    description: str


@dataclass_json
@dataclass
class User:
    id: str
    timezone: Optional[str]
