import datetime
import logging
from typing import List

import schemas.requests as requests_schemas
import schemas.responses as responses_schemas
import user_schedule.factory
from handlers.events_db import EventDB
from user_schedule.intervals import DatetimeInterval
from user_schedule.user_schedule import UserSchedule


class UserHandler:
    def __init__(self, logger: logging.Logger, db: EventDB):
        self.logger = logger
        self.events_db = db

    def approve_event(
            self,
            approve_request: requests_schemas.ApproveEventRequest,
    ) -> responses_schemas.ServerResponse:
        event_id = approve_request.event_id
        user_id = approve_request.user_id
        event = self.events_db.get_event(event_id)
        if not event:
            return responses_schemas.make_response(
                data=responses_schemas.BadResponse(error_code='not_found', message='Event was not found'),
                status=404
            )
        if user_id not in event.invited:
            return responses_schemas.make_response(
                data=responses_schemas.BadResponse(
                    error_code='permission_denied',
                    message='User was not invited to event, unable to approve'
                ),
                status=403
            )
        if user_id in event.accepted:
            return responses_schemas.make_response(
                data=responses_schemas.OkResponse(message='Event Approved')
            )
        self.events_db.approve_event_invite(approving_user_id=user_id, event_id=event_id)
        return responses_schemas.make_response(
            data=responses_schemas.OkResponse(message='Event Approved')
        )

    def user_events(
            self,
            user_events_request: requests_schemas.UserEventsRequest,
    ) -> responses_schemas.ServerResponse:
        user_id = user_events_request.user_id
        start_time = datetime.datetime.fromisoformat(user_events_request.interval_start_time_iso)
        search_interval = DatetimeInterval(
            start_datetime=start_time,
            end_datetime=start_time + datetime.timedelta(seconds=user_events_request.interval_duration_sec)
        )
        scheduled_events: UserSchedule = user_schedule.factory.create_user_schedule(
            events_base=self.events_db,
            user_id=user_id
        )
        events_in_interval: List[str] = scheduled_events.get_events_in_interval(search_interval)
        return responses_schemas.make_response(
            data=responses_schemas.GetUserEventsResponse(events_list=events_in_interval)
        )
