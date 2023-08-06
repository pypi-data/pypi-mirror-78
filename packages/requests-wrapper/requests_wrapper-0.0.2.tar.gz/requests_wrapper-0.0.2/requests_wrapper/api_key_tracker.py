from datetime import datetime
from typing import Union


class ApiKeyTracker:
    def __init__(self,
                 api_key: str,
                 call_limit_per_second: Union[float, int]):
        self.value = api_key
        self.call_limit_per_second = call_limit_per_second
        self.call_count = 0
        self.last_called_time: Union[datetime, None] = None

    def log_call(self) -> None:
        self.last_called_time = datetime.now()
        self.call_count += 1

    def get_time_in_seconds_till_available(self) -> float:
        if self.last_called_time is None or not self.call_limit_per_second:
            return 0.

        time_delta = (1 / self.call_limit_per_second) - (datetime.now() -
                                                         self.last_called_time).total_seconds()
        if time_delta > 0:
            return time_delta
        else:
            return 0.
