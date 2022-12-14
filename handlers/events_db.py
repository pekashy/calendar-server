import datetime
import logging
from typing import List, Optional, Sequence

import psycopg
from dateutil import parser

import common
import schemas.event
from common import Event
from schemas.event import UserSchema


def _parse_event(event_columns: Sequence[str]) -> Event:
    # TODO: Implement type correction with psycopg
    event_duration_time = parser.parse(event_columns[3])
    event_duration = datetime.timedelta(hours=event_duration_time.hour, minutes=event_duration_time.minute,
                                        seconds=event_duration_time.second)
    event_start_time = parser.parse(event_columns[2])
    invited = event_columns[7][1:-1].split(',')
    accepted = event_columns[8][1:-1].split(',')
    is_private = event_columns[4] == 't'
    return Event(
        id=event_columns[0],
        created_by=event_columns[1],
        schedule_start=event_start_time,
        duration=event_duration,
        is_private=is_private,
        repeat_type=common.EventRepeatType(event_columns[5]),
        description=event_columns[6],
        invited=invited,
        accepted=accepted,
        custom_repeat_params=(
            schemas.event.CustomRepeatsParamsSchema.from_json(event_columns[9]) if event_columns[9] else None
        ),
    )


class EventDB:
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.connection = None

    def connect(self):
        self.connection = psycopg.connect(
            'host=calendar-data port=5433 dbname=calendardb user=usr password=pwd connect_timeout=10'
        )

    def save_event(self, event: Event):
        with self.connection.cursor() as cursor:
            self.logger.info(f'Saving event `{event.id}`')
            cursor.execute(
                'INSERT INTO events (id, created_by, invited, accepted, schedule_start, '
                'duration, is_private, repeat_type, description, custom_repeats_params) VALUES '
                '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) '
                'ON CONFLICT ON CONSTRAINT events_pkey DO NOTHING ',
                (event.id, event.created_by, event.invited, [event.created_by], event.schedule_start,
                 event.duration, event.is_private, event.repeat_type, event.description, event.custom_repeat_params,)
            )
            self.connection.commit()

    def approve_event_invite(self, approving_user_id: str, event_id: str):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "UPDATE events "
                "SET accepted = array_append(accepted, (%s)) "
                "WHERE id=(%s) AND NOT (%s)=ANY(accepted)",
                (approving_user_id, event_id, approving_user_id,)
            )
            self.connection.commit()

    def get_event(self, event_id: str) -> Optional[Event]:
        with self.connection.cursor() as cursor:
            cursor.execute(
                'SELECT (id, created_by, schedule_start, duration, '
                'is_private, repeat_type, description, invited, accepted, custom_repeats_params) '
                'FROM events WHERE (%s)=id', (event_id,)
            )
            cursor_resp = cursor.fetchone()
            self.logger.debug(f'Retrieved event `{cursor_resp}`')
            if cursor_resp:
                event_data = cursor_resp[0]
                return _parse_event(event_data)

        return None

    def get_user_events(self, user_id: str) -> List[Event]:
        res = []
        self.logger.info(f'Start fetching')
        with self.connection.cursor() as cursor:
            cursor.execute(
                'SELECT (id, created_by, schedule_start, duration, '
                'is_private, repeat_type, description, invited, accepted, custom_repeats_params) '
                'FROM events WHERE (%s)=ANY(accepted)', (user_id,)
            )
            cursor_resp = cursor.fetchall()
            self.logger.info(f'Fetched events for user {user_id}: `{cursor_resp}`')
            res.extend([_parse_event(event_columns=event[0]) for event in cursor_resp])
        return res

    def add_user(self, user: UserSchema):
        with self.connection.cursor() as cursor:
            self.logger.info(f'Saving user `{user.id}`')
            cursor.execute(
                'INSERT INTO users (name, timezone) VALUES '
                '(%s, %s) '
                'ON CONFLICT ON CONSTRAINT users_pkey DO NOTHING ',
                (user.id, user.timezone,)
            )
            self.connection.commit()
