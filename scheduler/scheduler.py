import datetime
import heapq
from typing import Dict, List, Optional

import common
import user_schedule.intervals
from common import Event
from user_schedule.user_schedule import UserSchedule


class Scheduler:
    def __init__(self):
        self.user_schedules: Dict[str, UserSchedule] = {}

    def schedule_events(self, user_id: str, events: List[Event]):
        if user_id not in self.user_schedules:
            self.user_schedules[user_id] = UserSchedule()

        self.user_schedules[user_id].schedule_events(events)

    def get_next_available_slot_for_users(self, users: List[str], start_time: datetime.datetime,
                                          search_time_interval: datetime.timedelta,
                                          interval_duration: datetime.timedelta) -> Optional[common.DatetimePair]:
        assert users
        intervals = []

        for user_id in users:
            if user_id not in self.user_schedules:
                self.user_schedules[user_id] = UserSchedule()

            users_events: List[user_schedule.intervals.DatetimeInterval] = self.user_schedules[
                user_id].get_events_datetimes_for_day(
                start_datetime=start_time)
            intervals.extend([event for event in users_events])
        end_time = start_time + search_time_interval
        # Sentinel end interval
        intervals.append(user_schedule.intervals.DatetimeInterval(start_datetime=end_time, end_datetime=end_time))
        heapq.heapify(intervals)
        last_event_end = start_time
        while last_event_end - start_time <= search_time_interval and intervals:
            event = heapq.heappop(intervals)
            if event.start_datetime - last_event_end >= interval_duration:
                return common.DatetimePair(start_datetime=last_event_end,
                                           end_datetime=last_event_end + interval_duration)
            last_event_end = max(last_event_end, event.end_datetime)

        return None
