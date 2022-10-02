import datetime

import requests

import common
import schemas.event as event_schemas
import schemas.requests as requests_schemas
import schemas.responses as responses_schemas
from common import EventRepeatType

CREATE_EVENT_ENDPOINT = "http://0.0.0.0:8050/create_event"
GET_EVENT_ENDPOINT = "http://0.0.0.0:8050/event"


def test_create_event():
    event = common.Event(
        id='event1_id',
        created_by='user1_id',
        schedule_start=datetime.datetime(
            year=2022, month=1, day=1, hour=1, minute=1, second=1, tzinfo=datetime.timezone.utc,
        ),
        duration=datetime.timedelta(hours=1),
        invited=['user1_id', 'user2_id'],
        accepted=['user1_id'],
        is_private=False,
        repeat_type=EventRepeatType.SINGLE_EVENT,
        description='Very important meeting',
        custom_repeat_params=None,
    )
    event_schema = event_schemas.get_schema_from_event(event)
    headers = {"Content-Type": "application/json"}
    create_event_request = requests_schemas.CreateEventRequest(event=event_schema)
    create_resp = requests.post(url=CREATE_EVENT_ENDPOINT,
                                data=create_event_request.to_json(),
                                headers=headers)

    assert create_resp.status_code == 200

    get_event_resp = requests.get(
        url=GET_EVENT_ENDPOINT,
        params={'id': event.id},
        headers=headers
    )

    assert get_event_resp.status_code == 200
    returned_event_schema = responses_schemas.GetEventResponse.from_dict(get_event_resp.json()).event
    returned_event = event_schemas.get_event_from_schema(returned_event_schema)

    assert returned_event == event

    get_event_resp = requests.get(
        url=GET_EVENT_ENDPOINT,
        params={'id': 'no_such_id'},
        headers=headers
    )

    assert get_event_resp.status_code == 404
