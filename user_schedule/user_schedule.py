import datetime
import typing

import common
import user_schedule.repeat_modes as repeats
from user_schedule.constrains import DayConstrain, HolidayConstrain
from user_schedule.intervals import TimeInterval, DatetimeInterval
from user_schedule.repeat_modes import SchedulingExpression


class ScheduleElement(typing.NamedTuple):
    id: str
    # datetime of initial user_schedule. event can have more occurrences defined by recurring_info
    recurring_info: SchedulingExpression

    def occurs_at(self, date: datetime.date) -> bool:
        return self.recurring_info.includes(date)

    def intersects_interval(self, interval: DatetimeInterval) -> bool:
        return self.recurring_info.intersects_interval(interval)

    def _get_times_interval(self) -> TimeInterval:
        return TimeInterval(start_time=self.recurring_info.start_time,
                            end_time=self.recurring_info.end_time)

    def get_datetime_interval_for_date(self, date: datetime.date):
        time_info = self._get_times_interval()
        start_datetime_event = datetime.datetime(year=date.year, month=date.month,
                                                 day=date.day, hour=time_info.start_time.hour,
                                                 minute=time_info.start_time.minute,
                                                 second=time_info.start_time.second,
                                                 microsecond=time_info.start_time.microsecond)
        end_datetime_event = datetime.datetime(year=date.year, month=date.month,
                                               day=date.day, hour=time_info.end_time.hour,
                                               minute=time_info.end_time.minute, second=time_info.end_time.second,
                                               microsecond=time_info.end_time.microsecond)

        return DatetimeInterval(start_datetime=start_datetime_event, end_datetime=end_datetime_event)


def _create_schedule_element(event: common.Event) -> ScheduleElement:
    return ScheduleElement(id=event.id, recurring_info=repeats.get_repeat_mode(event=event))


def _get_next_day_start_datetime(start_datetime: datetime.datetime):
    next_day_start_date = start_datetime.date() + datetime.timedelta(days=1)
    return datetime.datetime(year=next_day_start_date.year, month=next_day_start_date.month,
                             day=next_day_start_date.day)


class UserSchedule:
    def __init__(self):
        self.events: typing.Dict[str, ScheduleElement] = {}
        self.events_ordered: typing.List[str] = []  # kept ordered by start_time, non-overlapping
        self.date_constrains: typing.List[DayConstrain] = [HolidayConstrain()]  # TODO: allow to setup

    def schedule_events(self, events: typing.List[common.Event]):
        self.events.update({event.id: _create_schedule_element(event=event) for event in events})
        self.events_ordered.extend([event.id for event in events])
        self.events_ordered.sort(key=lambda event_id: self.events[event_id].recurring_info.start_time)

    def is_event_occurring(self, event_id: str, date: datetime.date) -> bool:
        if event_id not in self.events:
            return False
        return self.events[event_id].occurs_at(date)

    def get_events_in_interval(self, interval: DatetimeInterval) -> typing.List[str]:
        return [event_id for event_id in self.events_ordered if
                self.events[event_id].intersects_interval(interval)]

    def get_events_datetimes_for_day(self, start_datetime: datetime.datetime) -> typing.List[DatetimeInterval]:
        events_datetimes = []
        next_date_datetime = _get_next_day_start_datetime(start_datetime)
        day_interval = DatetimeInterval(start_datetime=start_datetime,
                                        end_datetime=next_date_datetime - datetime.timedelta(microseconds=1))
        for event in [self.events[event_id] for event_id in self.events_ordered if
                      self.events[event_id].intersects_interval(day_interval)]:
            events_datetimes.append(event.get_datetime_interval_for_date(start_datetime.date()))

        return events_datetimes
