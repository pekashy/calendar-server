import logging

import common
import schemas.event as event_schemas
import schemas.requests as requests_schemas
import schemas.responses as responses_schemas
from handlers.events_db import EventDB
from user_schedule.intervals import DatetimeInterval
import datetime
from scheduler.scheduler import Scheduler
from scheduler import factory

from typing import List


def _ensure_event_users_lists_guarantees(event: common.Event):
    if event.created_by not in event.invited:
        event.invited.append(event.created_by)
    if event.created_by not in event.accepted:
        event.accepted.append(event.created_by)


class EventHandler:
    def __init__(self, logger: logging.Logger, db: EventDB):
        self.logger = logger
        self.events_db = db

    def create_event(self, creation_request: requests_schemas.CreateEventRequest) -> responses_schemas.ServerResponse:
        event_schema = creation_request.event
        event = event_schemas.get_event_from_schema(event_schema)
        _ensure_event_users_lists_guarantees(event)
        self.events_db.save_event(event)
        return responses_schemas.make_response(
            data=responses_schemas.OkResponse(message='Event Created')
        )

    def event_info(self, get_event_info_request: requests_schemas.GetEventRequest) -> responses_schemas.ServerResponse:
        event_id = get_event_info_request.event_id
        user_id = get_event_info_request.user_id
        event: common.Event = self.events_db.get_event(event_id)
        if not event:
            return responses_schemas.make_response(
                data=responses_schemas.BadResponse(error_code='not_found', message='Event was not found'),
                status=404
            )
        event_schema = event_schemas.get_schema_from_event(event)
        if event.is_private and user_id not in event.invited:
            event_schema = event_schemas.hide_private_fields(event_schema)
        return responses_schemas.make_response(
            data=responses_schemas.GetEventResponse(event=event_schema),
        )

    def free_interval(
            self,
            get_free_interval_request: requests_schemas.FirstFreeIntervalRequest,
    ) -> responses_schemas.ServerResponse:
        users: List[str] = get_free_interval_request.user_ids
        start_time = datetime.datetime.fromisoformat(get_free_interval_request.search_start_time_iso)
        interval_duration = datetime.timedelta(seconds=get_free_interval_request.interval_duration_sec)
        search_interval_duration = datetime.timedelta(seconds=get_free_interval_request.search_interval_duration_sec)
        self.logger.info(f'Start fetching {users}')
        scheduler: Scheduler = factory.create_scheduler(
            events_base=self.events_db,
            user_list=users
        )

        next_free_interval: common.DatetimePair = scheduler.get_next_available_slot_for_users(
            users=users,
            start_time=start_time,
            search_time_interval=search_interval_duration,
            interval_duration=interval_duration
        )
        if not next_free_interval:
            return responses_schemas.make_response(
                data=responses_schemas.BadResponse(error_code='not_found',
                                                   message='Free interval for given users was not found'),
                status=404,
            )

        return responses_schemas.make_response(
            data=responses_schemas.FirstFreeIntervalResponse(
                interval_start_time_iso=next_free_interval.start_datetime.isoformat())
        )
