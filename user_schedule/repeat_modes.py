import datetime

import common
from user_schedule.intervals import DatetimeInterval, SchedulingError


class SchedulingExpression:
    def __init__(self, start_datetime: datetime.datetime, duration: datetime.timedelta):
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
        return date.isoweekday() < 6 and super().includes(date)


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


class CustomRepeat(SchedulingExpression):
    def includes(self, date: datetime.date) -> bool:
        raise NotImplementedError('TODO: Implement free-form repeat conditions')


def get_repeat_mode(event: common.Event) -> SchedulingExpression:
    event_repeat_mode_constructor = {common.EventRepeatType.REPEAT_DAILY: RepeatEveryDay,
                                     common.EventRepeatType.SINGLE_EVENT: NoRepeat,
                                     common.EventRepeatType.REPEAT_WORKDAYS: RepeatEveryWorkDay,
                                     common.EventRepeatType.REPEAT_MONTHLY: RepeatEveryMonthSameWeekSameDay,
                                     common.EventRepeatType.REPEAT_WEEKLY: RepeatEveryWeek,
                                     common.EventRepeatType.REPEAT_YEARLY: RepeatEveryYear,
                                     common.EventRepeatType.REPEAT_CUSTOM: CustomRepeat,
                                     }[event.repeat_type]

    return event_repeat_mode_constructor(start_datetime=event.schedule_start, duration=event.duration)
