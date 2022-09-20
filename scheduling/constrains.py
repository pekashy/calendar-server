import datetime


class DayConstrain:
    def is_restricts(self, day: datetime.date):
        return NotImplementedError


class HolidayConstrain(DayConstrain):
    def is_restricts(self, day: datetime.date):
        return day.isoweekday() > 5
