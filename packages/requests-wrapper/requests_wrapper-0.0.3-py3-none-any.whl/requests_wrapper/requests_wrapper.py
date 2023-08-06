import logging
import time
from typing import List

import requests
from requests import Response
from requests_wrapper.api_key_tracker import ApiKeyTracker

logger = logging.getLogger(__name__)


class RequestsWrapper:
    def __init__(self,
                 api_keys: List[str],
                 api_key_header: str = "Authorization",
                 call_limit_per_second: float = 0
                 ):
        self._api_key_trackers: List[ApiKeyTracker] = []
        self._api_key_header = api_key_header
        for api_key in api_keys:
            api_key_tracker = ApiKeyTracker(api_key,
                                            call_limit_per_second)
            self._api_key_trackers.append(api_key_tracker)

    def _get_least_used_key_index(self):
        call_counts = [x.call_count for x in self._api_key_trackers]
        index_min = call_counts.index(min(call_counts))
        return index_min

    def call(self,
             http_method: str,
             **kwargs) -> Response:
        call_key_index = self._get_least_used_key_index()
        sleep_time = self._api_key_trackers[call_key_index].get_time_in_seconds_till_available()

        print(f"sleeping for {sleep_time} seconds before using api_key {call_key_index}")
        time.sleep(sleep_time)

        http_request_function = getattr(requests, http_method)

        if "headers" not in kwargs.keys():
            kwargs["headers"] = dict()
        kwargs["headers"][self._api_key_header] = self._api_key_trackers[call_key_index].value

        response = http_request_function(**kwargs)
        logger.info(f"request call made using api_key {call_key_index}")

        self._api_key_trackers[call_key_index].log_call()
        return response
