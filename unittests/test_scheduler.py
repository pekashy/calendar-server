import datetime

import pytest

from common import DatetimePair, EventRepeatType
from common import Event
from scheduler.scheduler import Scheduler


@pytest.fixture
def event_date():
    return datetime.datetime(year=2000, month=1, day=3)


def test_scheduler(event_date):
    scheduler = Scheduler()
    user1 = 'user1_id'
    event1 = Event(schedule_start=event_date, duration=datetime.timedelta(hours=1),
                   repeat_type=EventRepeatType.SINGLE_EVENT, id='event1_id',
                   invited=['user1_id'], created_by='user1_id', is_private=False,
                   description='Some Event', accepted=['user1_id'], custom_repeat_params=None)  # 00 to 01
    event2 = Event(schedule_start=event_date + datetime.timedelta(hours=2), duration=datetime.timedelta(hours=2),
                   repeat_type=EventRepeatType.SINGLE_EVENT, id='event2_id',
                   invited=['user1_id'], created_by='user1_id', is_private=False,
                   description='Some Event', accepted=['user1_id'], custom_repeat_params=None)  # 02 to 04
    event3 = Event(schedule_start=event_date + datetime.timedelta(hours=5), duration=datetime.timedelta(hours=2),
                   repeat_type=EventRepeatType.SINGLE_EVENT, id='event3_id',
                   invited=['user1_id'], created_by='user1_id', is_private=False,
                   description='Some Event', accepted=['user1_id'], custom_repeat_params=None)  # 05 to 07
    scheduler.schedule_events(user1, [event1, event2, event3])
    available_slot = scheduler.get_next_available_slot_for_users(users=[user1], start_time=event_date,
                                                                 search_time_interval=datetime.timedelta(days=1),
                                                                 interval_duration=datetime.timedelta(minutes=30))

    assert available_slot == DatetimePair(start_datetime=event_date + datetime.timedelta(hours=1),  # 01 to 0130
                                          end_datetime=event_date + datetime.timedelta(hours=1, minutes=30))
    user2 = 'user2_id'
    event4 = Event(schedule_start=event_date, duration=datetime.timedelta(hours=4),
                   repeat_type=EventRepeatType.SINGLE_EVENT, id='event4_id',
                   invited=['user2_id'], created_by='user2_id', is_private=False,
                   description='Some Event', accepted=['user1_id'], custom_repeat_params=None)  # 00 to 04
    scheduler.schedule_events(user2, [event4])
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
