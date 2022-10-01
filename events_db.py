import psycopg

import schemas
from schemas import Event
from typing import List


class EventDB:
    def __init__(self):
        self.connection = psycopg.connect(
            "host=calendar-data port=5433 dbname=calendardb user=usr password=pwd connect_timeout=10"
        )

    def save_event(self, event: Event):
        with self.connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO events (id, created_by, invited, accepted, schedule_start, '
                'duration, is_private, repeat_type, description) VALUES '
                '(%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (event.id, event.created_by, event.attendees, [event.created_by], event.schedule_start,
                 event.duration, event.is_private, event.repeat_type, event.description,)
            )
            self.connection.commit()

    def approve_event_invite(self, approving_user_id: str, event_id: str):
        pass

    def get_event(self, event_id: str) -> schemas.Event:
        pass

    def get_user_events(self, user_id: str) -> List[Event]:
        pass
