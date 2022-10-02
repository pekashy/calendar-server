from scheduler.scheduler import Scheduler
from handlers import events_db
from typing import List


def create_scheduler(events_base: events_db.EventDB, user_list: List[str]):
    scheduler = Scheduler()
    for user in user_list:
        user_events = events_base.get_user_events(user)
        scheduler.schedule_events(user_id=user, events=user_events)

    return scheduler
