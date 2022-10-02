import datetime
import uuid

import pytest
import requests

import common
import schemas.event as event_schemas
import schemas.requests as requests_schemas
import schemas.responses as responses_schemas
from common import EventRepeatType
from typing import List

CREATE_EVENT_ENDPOINT = "http://0.0.0.0:8050/create_event"
GET_EVENT_ENDPOINT = "http://0.0.0.0:8050/event"
APPROVE_EVENT_ENDPOINT = "http://0.0.0.0:8050/approve_event"
USER_EVENTS_ENDPOINT = "http://0.0.0.0:8050/user_events"
FIRST_INTERVAL_ENDPOINT = "http://0.0.0.0:8050/find_interval"


@pytest.fixture
def default_event():
    return common.Event(
        id='event_' + str(uuid.uuid4()),
        created_by='user1_id',
        schedule_start=datetime.datetime(
            year=2022, month=1, day=1, hour=0, minute=0, second=0,
        ),
        duration=datetime.timedelta(hours=1),
        invited=['user1_id', 'user2_id'],
        accepted=['user1_id'],
        is_private=False,
        repeat_type=EventRepeatType.SINGLE_EVENT,
        description='Very important meeting',
        custom_repeat_params=None,
    )


@pytest.fixture
def create_event():
    def _method(event: common.Event):
        event_schema = event_schemas.get_schema_from_event(event)
        headers = {"Content-Type": "application/json"}
        create_event_request = requests_schemas.CreateEventRequest(event=event_schema)
        return requests.post(url=CREATE_EVENT_ENDPOINT,
                             data=create_event_request.to_json(),
                             headers=headers)

    return _method


@pytest.fixture
def get_event():
    def _method(event_id: str, user_id: str):
        headers = {"Content-Type": "application/json"}

        get_event_resp = requests.get(
            url=GET_EVENT_ENDPOINT,
            params=requests_schemas.GetEventRequest(event_id=event_id, user_id=user_id).to_dict(),
            headers=headers
        )
        if not 200 <= get_event_resp.status_code < 300:
            return get_event_resp.status_code, None
        returned_event_schema = responses_schemas.GetEventResponse.from_dict(get_event_resp.json()).event
        returned_event = event_schemas.get_event_from_schema(returned_event_schema)
        return get_event_resp.status_code, returned_event

    return _method


@pytest.fixture
def approve_event():
    def _method(event_id: str, user_id: str):
        headers = {"Content-Type": "application/json"}
        approve_event_req = requests_schemas.ApproveEventRequest(event_id=event_id, user_id=user_id)
        return requests.post(url=APPROVE_EVENT_ENDPOINT,
                             data=approve_event_req.to_json(),
                             headers=headers)

    return _method


@pytest.fixture
def user_events():
    def _method(user_id: str, interval_start: datetime.datetime, interval_duration: datetime.timedelta):
        headers = {"Content-Type": "application/json"}
        user_events_req = requests_schemas.UserEventsRequest(
            user_id=user_id,
            interval_start_time_iso=interval_start.isoformat(),
            interval_duration_sec=int(interval_duration.total_seconds()),
        )
        res = requests.get(url=USER_EVENTS_ENDPOINT,
                           params=user_events_req.to_dict(),
                           headers=headers)
        response: responses_schemas.GetUserEventsResponse = responses_schemas.GetUserEventsResponse.from_dict(
            res.json())
        return response.events_list

    return _method


@pytest.fixture
def first_free_interval():
    def _method(users: List[str], interval_start: datetime.datetime, interval_duration: datetime.timedelta,
                search_interval_duration: datetime.timedelta):
        headers = {"Content-Type": "application/json"}
        user_events_req = requests_schemas.FirstFreeIntervalRequest(
            user_ids=users,
            search_start_time_iso=interval_start.isoformat(),
            interval_duration_sec=int(interval_duration.total_seconds()),
            search_interval_duration_sec=int(search_interval_duration.total_seconds()),
        )
        res = requests.post(url=FIRST_INTERVAL_ENDPOINT,
                            data=user_events_req.to_json(),
                            headers=headers)
        response: responses_schemas.FirstFreeIntervalResponse = responses_schemas.FirstFreeIntervalResponse.from_dict(
            res.json())
        return datetime.datetime.fromisoformat(response.interval_start_time_iso)

    return _method
