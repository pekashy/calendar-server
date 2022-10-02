import logging

import common
import schemas.event as event_schemas
import schemas.requests as requests_schemas
import schemas.responses as responses_schemas
from handlers.events_db import EventDB
import datetime

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

