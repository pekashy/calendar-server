import pytest

from scheduling.repeat_modes import *
from scheduling.user_schedule import UserSchedule, EventLink


@pytest.fixture
def schedule():
    return UserSchedule('some_user_id')


@pytest.fixture
def event_date():
    return datetime.datetime(year=2000, month=1, day=3)


def test_daily_recurring(schedule, event_date):
    event = EventLink(id='event_id',
                      recurring_info=RepeatEveryDay(start_datetime=event_date + datetime.timedelta(hours=4),
                                                    duration=datetime.timedelta(hours=5)))
    prev_interval = DatetimeInterval(start_datetime=event_date + datetime.timedelta(hours=1),
                                     end_datetime=event_date + datetime.timedelta(hours=2))
    left_intersect_interval = DatetimeInterval(start_datetime=event_date + datetime.timedelta(hours=1),
                                               end_datetime=event_date + datetime.timedelta(hours=5))
    inner_intersect_interval = DatetimeInterval(start_datetime=event_date + datetime.timedelta(hours=5),
                                                end_datetime=event_date + datetime.timedelta(hours=6))
    outer_intersect_interval = DatetimeInterval(start_datetime=event_date + datetime.timedelta(hours=3),
                                                end_datetime=event_date + datetime.timedelta(hours=10))
    right_intersect_interval = DatetimeInterval(start_datetime=event_date + datetime.timedelta(hours=6),
                                                end_datetime=event_date + datetime.timedelta(hours=10))
    right_interval = DatetimeInterval(start_datetime=event_date + datetime.timedelta(hours=11),
                                      end_datetime=event_date + datetime.timedelta(hours=12))

    prev_interval_next_day = DatetimeInterval(start_datetime=prev_interval.start_datetime + datetime.timedelta(days=1),
                                              end_datetime=prev_interval.end_datetime + datetime.timedelta(days=1))
    inner_intersect_interval_next_day = DatetimeInterval(
        start_datetime=inner_intersect_interval.start_datetime + datetime.timedelta(days=1),
        end_datetime=inner_intersect_interval.end_datetime + datetime.timedelta(days=1))
    outer_intersect_interval_next_day = DatetimeInterval(
        start_datetime=outer_intersect_interval.start_datetime + datetime.timedelta(days=1),
        end_datetime=outer_intersect_interval.end_datetime + datetime.timedelta(days=1))
    left_intersect_interval_next_day = DatetimeInterval(
        start_datetime=left_intersect_interval.start_datetime + datetime.timedelta(days=1),
        end_datetime=left_intersect_interval.end_datetime + datetime.timedelta(days=1))
    right_intersect_interval_next_day = DatetimeInterval(
        start_datetime=right_intersect_interval.start_datetime + datetime.timedelta(days=1),
        end_datetime=right_intersect_interval.end_datetime + datetime.timedelta(days=1))
    right_interval_next_day = DatetimeInterval(
        start_datetime=right_interval.start_datetime + datetime.timedelta(days=1),
        end_datetime=right_interval.end_datetime + datetime.timedelta(days=1))

    schedule.schedule_event(event)

    assert schedule.is_event_occurring('event_id', event_date.date())
    assert schedule.is_event_occurring('event_id', (event_date + datetime.timedelta(days=1)).date())
    assert schedule.get_events_in_interval(prev_interval) == []
    assert schedule.get_events_in_interval(left_intersect_interval) == ['event_id']
    assert schedule.get_events_in_interval(inner_intersect_interval) == ['event_id']
    assert schedule.get_events_in_interval(outer_intersect_interval) == ['event_id']
    assert schedule.get_events_in_interval(outer_intersect_interval) == ['event_id']
    assert schedule.get_events_in_interval(right_intersect_interval) == ['event_id']
    assert schedule.get_events_in_interval(right_interval) == []
    assert schedule.get_events_in_interval(prev_interval_next_day) == []
    assert schedule.get_events_in_interval(left_intersect_interval_next_day) == ['event_id']
    assert schedule.get_events_in_interval(inner_intersect_interval_next_day) == ['event_id']
    assert schedule.get_events_in_interval(outer_intersect_interval_next_day) == ['event_id']
    assert schedule.get_events_in_interval(outer_intersect_interval_next_day) == ['event_id']
    assert schedule.get_events_in_interval(right_intersect_interval_next_day) == ['event_id']
    assert schedule.get_events_in_interval(right_interval_next_day) == []


def test_single_event(schedule, event_date):
    event = EventLink(id='event_id',
                      recurring_info=NoRepeat(start_datetime=event_date + datetime.timedelta(hours=4),
                                              duration=datetime.timedelta(hours=5)))
    prev_interval = DatetimeInterval(start_datetime=event_date + datetime.timedelta(hours=1),
                                     end_datetime=event_date + datetime.timedelta(hours=2))
    left_intersect_interval = DatetimeInterval(start_datetime=event_date + datetime.timedelta(hours=1),
                                               end_datetime=event_date + datetime.timedelta(hours=5))
    inner_intersect_interval = DatetimeInterval(start_datetime=event_date + datetime.timedelta(hours=5),
                                                end_datetime=event_date + datetime.timedelta(hours=6))
    outer_intersect_interval = DatetimeInterval(start_datetime=event_date + datetime.timedelta(hours=3),
                                                end_datetime=event_date + datetime.timedelta(hours=10))
    right_intersect_interval = DatetimeInterval(start_datetime=event_date + datetime.timedelta(hours=6),
                                                end_datetime=event_date + datetime.timedelta(hours=10))
    right_interval = DatetimeInterval(start_datetime=event_date + datetime.timedelta(hours=11),
                                      end_datetime=event_date + datetime.timedelta(hours=12))

    prev_interval_next_day = DatetimeInterval(start_datetime=prev_interval.start_datetime + datetime.timedelta(days=1),
                                              end_datetime=prev_interval.end_datetime + datetime.timedelta(days=1))
    inner_intersect_interval_next_day = DatetimeInterval(
        start_datetime=inner_intersect_interval.start_datetime + datetime.timedelta(days=1),
        end_datetime=inner_intersect_interval.end_datetime + datetime.timedelta(days=1))
    outer_intersect_interval_next_day = DatetimeInterval(
        start_datetime=outer_intersect_interval.start_datetime + datetime.timedelta(days=1),
        end_datetime=outer_intersect_interval.end_datetime + datetime.timedelta(days=1))
    left_intersect_interval_next_day = DatetimeInterval(
        start_datetime=left_intersect_interval.start_datetime + datetime.timedelta(days=1),
        end_datetime=left_intersect_interval.end_datetime + datetime.timedelta(days=1))
    right_intersect_interval_next_day = DatetimeInterval(
        start_datetime=right_intersect_interval.start_datetime + datetime.timedelta(days=1),
        end_datetime=right_intersect_interval.end_datetime + datetime.timedelta(days=1))
    right_interval_next_day = DatetimeInterval(
        start_datetime=right_interval.start_datetime + datetime.timedelta(days=1),
        end_datetime=right_interval.end_datetime + datetime.timedelta(days=1))

    schedule.schedule_event(event)

    assert schedule.is_event_occurring('event_id', event_date.date())
    assert not schedule.is_event_occurring('event_id', (event_date + datetime.timedelta(days=1)).date())
    assert schedule.get_events_in_interval(prev_interval) == []
    assert schedule.get_events_in_interval(left_intersect_interval) == ['event_id']
    assert schedule.get_events_in_interval(inner_intersect_interval) == ['event_id']
    assert schedule.get_events_in_interval(outer_intersect_interval) == ['event_id']
    assert schedule.get_events_in_interval(outer_intersect_interval) == ['event_id']
    assert schedule.get_events_in_interval(right_intersect_interval) == ['event_id']
    assert schedule.get_events_in_interval(right_interval) == []
    assert schedule.get_events_in_interval(prev_interval_next_day) == []
    assert schedule.get_events_in_interval(left_intersect_interval_next_day) == []
    assert schedule.get_events_in_interval(inner_intersect_interval_next_day) == []
    assert schedule.get_events_in_interval(outer_intersect_interval_next_day) == []
    assert schedule.get_events_in_interval(outer_intersect_interval_next_day) == []
    assert schedule.get_events_in_interval(right_intersect_interval_next_day) == []
    assert schedule.get_events_in_interval(right_interval_next_day) == []


def test_weekly_repeat(schedule, event_date):
    event = EventLink(id='event_id',
                      recurring_info=RepeatEveryWeek(start_datetime=event_date, duration=datetime.timedelta(hours=1)))
    schedule.schedule_event(event)

    assert not schedule.is_event_occurring('event_id', (event_date + datetime.timedelta(days=2)).date())
    assert schedule.is_event_occurring('event_id', (event_date + datetime.timedelta(weeks=1)).date())


def test_repeat_every_work_day(schedule, event_date):
    event = EventLink(id='event_id',
                      recurring_info=RepeatEveryWorkDay(start_datetime=datetime.datetime(year=2022, month=9, day=20),
                                                        duration=datetime.timedelta(hours=1)))
    schedule.schedule_event(event)

    assert not schedule.is_event_occurring('event_id', datetime.date(year=2022, month=9, day=24))
    assert schedule.is_event_occurring('event_id', datetime.date(year=2022, month=9, day=26))


def test_repeat_every_year(schedule, event_date):
    event = EventLink(id='event_id',
                      recurring_info=RepeatEveryWorkDay(start_datetime=datetime.datetime(year=2022, month=9, day=20),
                                                        duration=datetime.timedelta(hours=1)))
    schedule.schedule_event(event)

    assert not schedule.is_event_occurring('event_id', datetime.date(year=2022, month=9, day=24))
    assert not schedule.is_event_occurring('event_id', datetime.date(year=2021, month=9, day=20))
    assert schedule.is_event_occurring('event_id', datetime.date(year=2023, month=9, day=20))


def test_repeat_every_month_same_week_same_day(schedule, event_date):
    event = EventLink(id='event_id',
                      recurring_info=RepeatEveryMonthSameWeekSameDay(
                          start_datetime=datetime.datetime(year=2022, month=9, day=20),
                          duration=datetime.timedelta(hours=1)))

    schedule.schedule_event(event)

    assert not schedule.is_event_occurring('event_id', datetime.date(year=2022, month=9, day=24))
    assert not schedule.is_event_occurring('event_id', datetime.date(year=2021, month=9, day=20))
    assert schedule.is_event_occurring('event_id', datetime.date(year=2022, month=10, day=18))


def test_find_intervals(schedule, event_date):
    event1 = EventLink(id='event_id1',
                       recurring_info=RepeatEveryDay(start_datetime=event_date,
                                                     duration=datetime.timedelta(hours=1)))
    schedule.schedule_event(event1)
    event2 = EventLink(id='event_id2',
                       recurring_info=NoRepeat(start_datetime=event_date + datetime.timedelta(hours=2),
                                               duration=datetime.timedelta(hours=1)))
    schedule.schedule_event(event2)

    event3 = EventLink(id='event_id3',
                       recurring_info=RepeatEveryDay(start_datetime=event_date + datetime.timedelta(hours=5),
                                                     duration=datetime.timedelta(hours=18)))
    schedule.schedule_event(event3)

    first_1h_interval = schedule.get_next_free_slot(start_datetime=event_date, min_duration=datetime.timedelta(hours=1))
    second_interval_for_1h = schedule.get_next_free_slot(start_datetime=first_1h_interval.end_datetime,
                                                         min_duration=datetime.timedelta(hours=1))
    interval_for_2h = schedule.get_next_free_slot(start_datetime=event_date, min_duration=datetime.timedelta(hours=2))
    interval_for_4h = schedule.get_next_free_slot(start_datetime=event_date, min_duration=datetime.timedelta(hours=4))
    interval_for_6h = schedule.get_next_free_slot(start_datetime=event_date, min_duration=datetime.timedelta(hours=6))
    interval_for_4h_same_day = schedule.get_next_free_slot(start_datetime=event_date,
                                                           min_duration=datetime.timedelta(hours=4),
                                                           following_days_to_look=0)

    assert first_1h_interval == DatetimeInterval(start_datetime=event_date + datetime.timedelta(hours=1),
                                                 end_datetime=event_date + datetime.timedelta(hours=2))
    assert second_interval_for_1h == DatetimeInterval(start_datetime=event_date + datetime.timedelta(hours=3),
                                                      end_datetime=event_date + datetime.timedelta(hours=5))
    assert interval_for_2h == DatetimeInterval(start_datetime=event_date + datetime.timedelta(hours=3),
                                               end_datetime=event_date + datetime.timedelta(hours=5))
    assert interval_for_4h == DatetimeInterval(start_datetime=event_date + datetime.timedelta(days=1, hours=1),
                                               end_datetime=event_date + datetime.timedelta(days=1, hours=5))
    assert not interval_for_6h
    assert not interval_for_4h_same_day
