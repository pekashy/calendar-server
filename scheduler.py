import datetime
from typing import Dict, List, Optional

import common
import user_schedule.intervals
from common import Event
from user_schedule.user_schedule import UserSchedule


class Scheduler:
    def __init__(self):
        self.user_schedules: Dict[str, UserSchedule] = {}

    def schedule_event(self, user_id: str, event: Event):
        if user_id not in self.user_schedules:
            self.user_schedules[user_id] = UserSchedule()

        self.user_schedules[user_id].schedule_event(event)

    def get_next_available_slot_for_users(self, users: List[str], start_time: datetime.datetime,
                                          search_time_interval: datetime.timedelta,
                                          interval_duration: datetime.timedelta) -> Optional[common.DatetimePair]:
        assert users
        search_start = start_time
        search_end = None
        while search_start - start_time <= search_time_interval:
            for user_id in users:
                if user_id not in self.user_schedules:
                    self.user_schedules[user_id] = UserSchedule()

                user_interval: user_schedule.intervals.DatetimeInterval = self.user_schedules[
                    user_id].get_next_free_slot(
                    start_datetime=search_start,
                    min_duration=interval_duration,
                    following_days_to_look=0)
                if not user_interval:
                    search_start += interval_duration
                    search_end = None
                    break

                search_start = max(search_start, user_interval.start_datetime)
                search_end = min(search_end, user_interval.end_datetime) if search_end else user_interval.end_datetime

                if search_end - search_start < interval_duration:
                    search_start += interval_duration
                    search_end = None
                    break

            if search_end:
                return common.DatetimePair(start_datetime=search_start, end_datetime=search_end)

        return None
