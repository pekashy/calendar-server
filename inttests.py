import pytest

import requests
import datetime
from schemas import EventSchema, EventRepeatType

CREATE_EVENT_ENDPOINT = "http://0.0.0.0:8050/create_event"


def test_create_event():
    event = EventSchema(
        id='event1_id',
        created_by='user1_id',
        schedule_start=datetime.datetime(
            year=2022, month=1, day=1, hour=1, minute=1, second=1
        ).isoformat(),
        duration_sec=datetime.timedelta(hours=1).seconds,
        attendees=['user2_id'],
        is_private=False,
        repeat_type=EventRepeatType.SINGLE_EVENT,
        description='Very important meeting',
    )
    headers = {"Content-Type": "application/json"}
    requests.post(url=CREATE_EVENT_ENDPOINT,
                  data=event.to_json(),
                  headers=headers)
