from handlers import events_db
from user_schedule.user_schedule import UserSchedule


def create_user_schedule(events_base: events_db.EventDB, user_id: str) -> UserSchedule:
    schedule = UserSchedule()
    user_events = events_base.get_user_events(user_id)
    schedule.schedule_events(user_events)
    return schedule
