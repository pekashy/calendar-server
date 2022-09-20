import datetime
import typing


class DatetimeInterval:
    def __init__(self, start_datetime: datetime.datetime, end_datetime: datetime.datetime):
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.date = self.start_datetime.date()
        if self.start_datetime.date() != self.end_datetime.date():
            raise SchedulingError("Multi-date intervals are not supported!")

    def __eq__(self, other):
        return self.start_datetime == other.start_datetime and self.end_datetime == other.end_datetime


class TimeInterval(typing.NamedTuple):
    start_time: datetime.time
    end_time: datetime.time


class SchedulingError(Exception):
    pass


class SchedulingExpression:
    def __init__(self, start_datetime: datetime.datetime,
                 duration: datetime.timedelta = datetime.timedelta(days=0)):
        self.start_time = start_datetime.time()
        self.end_time = (start_datetime + duration).time()
        self.first_scheduled_date = start_datetime.date()
        if (start_datetime + duration).date() != self.first_scheduled_date:
            raise SchedulingError("Multi-date meetings are not supported!")

    def includes(self, date: datetime.date) -> bool:
        return self.first_scheduled_date <= date

    def intersects_interval(self, interval: DatetimeInterval) -> bool:
        return self.includes(interval.date) and (
            not (
                    (
                            self.start_time <= interval.start_datetime.time()
                            and self.end_time < interval.start_datetime.time()
                    )
                    or
                    (
                            self.start_time >= interval.end_datetime.time()
                            and self.end_time > interval.end_datetime.time()
                    )
            )
        )


class RepeatEveryDay(SchedulingExpression):
    pass


class RepeatEveryWeek(SchedulingExpression):
    def includes(self, date: datetime.date) -> bool:
        return self.first_scheduled_date.isoweekday() == date.isoweekday() and super().includes(date)


class RepeatEveryWorkDay(SchedulingExpression):
    def includes(self, date: datetime.date) -> bool:
        return self.first_scheduled_date.isoweekday() < 6 and super().includes(date)


class RepeatEveryYear(SchedulingExpression):
    def includes(self, date: datetime.date) -> bool:
        return (
                self.first_scheduled_date.day == date.day
                and self.first_scheduled_date.month == date.month
                and super().includes(date)
        )


class RepeatEveryMonthSameWeekSameDay(SchedulingExpression):
    def includes(self, date: datetime.date) -> bool:
        def get_week_of_the_month(date: datetime.date):
            month = date.month
            week = 0
            while date.month == month:
                week += 1
                date -= datetime.timedelta(days=7)

            return week

        return (
                self.first_scheduled_date.isoweekday() == date.isoweekday()
                and get_week_of_the_month(self.first_scheduled_date) == get_week_of_the_month(date)
                and super().includes(date)
        )


class NoRepeat(SchedulingExpression):
    def includes(self, date: datetime.date) -> bool:
        return self.first_scheduled_date == date


class DayConstrain:
    def is_restricts(self, day: datetime.date):
        return NotImplementedError


class HolidayConstrain(DayConstrain):
    def is_restricts(self, day: datetime.date):
        return day.isoweekday() > 5


class EventLink(typing.NamedTuple):
    id: str
    # datetime of initial scheduling. event can have more occurrences defined by recurring_info
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


class UserSchedule:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.events: typing.Dict[str, EventLink] = {}
        self.events_ordered: typing.List[str] = []  # kept ordered by start_time, non-overlapping
        self.date_constrains: typing.List[DayConstrain] = [HolidayConstrain()]  # TODO: allow to setup

    def schedule_event(self, event: EventLink):
        self.events_ordered.append(event.id)
        self.events[event.id] = event
        self.events_ordered.sort(key=lambda event_id: self.events[event_id].recurring_info.start_time)

    def is_event_occurring(self, event_id: str, date: datetime.date) -> bool:
        if event_id not in self.events:
            return False
        return self.events[event_id].occurs_at(date)

    def get_events_in_interval(self, interval: DatetimeInterval) -> typing.List[str]:
        return [event_id for event_id in self.events_ordered if
                self.events[event_id].intersects_interval(interval)]

    @staticmethod
    def _get_next_day_start_datetime(start_datetime: datetime.datetime):
        next_day_start_date = start_datetime.date() + datetime.timedelta(days=1)
        return datetime.datetime(year=next_day_start_date.year, month=next_day_start_date.month,
                                 day=next_day_start_date.day)

    def _get_events_datetimes_for_day(self, start_datetime: datetime.datetime) -> typing.List[DatetimeInterval]:
        events_datetimes = []
        next_date_datetime = self._get_next_day_start_datetime(start_datetime)
        day_interval = DatetimeInterval(start_datetime=start_datetime,
                                        end_datetime=next_date_datetime - datetime.timedelta(microseconds=1))
        for event in [self.events[event_id] for event_id in self.events_ordered if
                      self.events[event_id].intersects_interval(day_interval)]:
            events_datetimes.append(event.get_datetime_interval_for_date(start_datetime.date()))

        return events_datetimes

    def get_next_free_slot(self, start_datetime: datetime.datetime, min_duration: datetime.timedelta,
                           following_days_to_look: int = 7) -> typing.Optional[DatetimeInterval]:
        """
        We neither want to search for next slot in a year for a busy user,
        nor to in general validate if scheduling a meeting with given length is possible for user.
        So we will recursively call this fi
        """
        if following_days_to_look < 0:
            return None

        next_day_start_datetime = self._get_next_day_start_datetime(start_datetime)
        # Weekday or holiday day etc
        if any(constrain.is_restricts(start_datetime.date()) for constrain in self.date_constrains):
            return self.get_next_free_slot(start_datetime=next_day_start_datetime,
                                           min_duration=min_duration,
                                           following_days_to_look=following_days_to_look - 1)

        daily_events = self._get_events_datetimes_for_day(start_datetime=start_datetime)

        # Adding some sentinel events to respect day's interval borders
        if not daily_events:
            daily_events = [DatetimeInterval(start_datetime=start_datetime, end_datetime=start_datetime)]
        daily_events = daily_events + [
            DatetimeInterval(start_datetime=next_day_start_datetime - datetime.timedelta(microseconds=1),
                             end_datetime=next_day_start_datetime - datetime.timedelta(microseconds=1))]

        for i in range(1, len(daily_events)):
            last_event_end_datetime = daily_events[i - 1].end_datetime
            curr_event_start_datetime = daily_events[i].start_datetime

            free_interval = curr_event_start_datetime - last_event_end_datetime
            if free_interval >= min_duration:
                # TODO: Add time constrains
                return DatetimeInterval(start_datetime=last_event_end_datetime, end_datetime=curr_event_start_datetime)

        return self.get_next_free_slot(start_datetime=self._get_next_day_start_datetime(start_datetime),
                                       min_duration=min_duration,
                                       following_days_to_look=following_days_to_look - 1)
