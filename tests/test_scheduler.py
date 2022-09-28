import datetime
import pytest

from scheduler import Scheduler
from common import Event, DatetimePair, EventRepeatType


@pytest.fixture
def event_date():
    return datetime.datetime(year=2000, month=1, day=3)


def test_scheduler(event_date):
    scheduler = Scheduler()
    user1 = 'user1_id'
    event1 = Event(schedule_start=event_date, duration=datetime.timedelta(hours=1),
                   repeat_type=EventRepeatType.SINGLE_MEETING, id='event1_id')  # 00 to 01
    event2 = Event(schedule_start=event_date + datetime.timedelta(hours=2), duration=datetime.timedelta(hours=2),
                   repeat_type=EventRepeatType.SINGLE_MEETING, id='event2_id')  # 02 to 04
    event3 = Event(schedule_start=event_date + datetime.timedelta(hours=5), duration=datetime.timedelta(hours=2),
                   repeat_type=EventRepeatType.SINGLE_MEETING, id='event3_id')  # 05 to 07
    scheduler.schedule_event(user1, event1)
    scheduler.schedule_event(user1, event2)
    scheduler.schedule_event(user1, event3)
    available_slot = scheduler.get_next_available_slot_for_users(users=[user1], start_time=event_date,
                                                                 search_time_interval=datetime.timedelta(days=1),
                                                                 interval_duration=datetime.timedelta(minutes=30))

    assert available_slot == DatetimePair(start_datetime=event_date + datetime.timedelta(hours=1),  # 01 to 0130
                                          end_datetime=event_date + datetime.timedelta(hours=1, minutes=30))
    user2 = 'user2_id'
    event4 = Event(schedule_start=event_date, duration=datetime.timedelta(hours=4),
                   repeat_type=EventRepeatType.SINGLE_MEETING, id='event4_id')  # 00 to 04
    scheduler.schedule_event(user2, event4)
    available_slot = scheduler.get_next_available_slot_for_users(users=[user1, user2], start_time=event_date,
                                                                 search_time_interval=datetime.timedelta(days=1),
                                                                 interval_duration=datetime.timedelta(minutes=30))
    assert available_slot == DatetimePair(start_datetime=event_date + datetime.timedelta(hours=4),  # 04 to 0430
                                          end_datetime=event_date + datetime.timedelta(hours=4, minutes=30))

    available_slot = scheduler.get_next_available_slot_for_users(users=[user1, user2], start_time=event_date,
                                                                 search_time_interval=datetime.timedelta(days=1),
                                                                 interval_duration=datetime.timedelta(hours=2))
    assert available_slot == DatetimePair(start_datetime=event_date + datetime.timedelta(hours=7),  # 07 to 09
                                          end_datetime=event_date + datetime.timedelta(hours=9))

    available_slot = scheduler.get_next_available_slot_for_users(users=[user1, user2], start_time=event_date,
                                                                 search_time_interval=datetime.timedelta(days=1),
                                                                 interval_duration=datetime.timedelta(hours=20))
    assert not available_slot
