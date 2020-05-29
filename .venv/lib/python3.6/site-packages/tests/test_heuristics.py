# Standard library
import unittest
import time
from datetime import datetime, timedelta

# Local modules
from canonicalwebteam.http import heuristics


class TestHeuristics(unittest.TestCase):
    def test_custom_heuristic(self):
        today = datetime.utcnow()
        one_day_delta = timedelta(days=1)
        tomorrow = today + one_day_delta

        self.assertEqual(
            tomorrow, heuristics.expire_after(one_day_delta, today)
        )

    def test_datetime_to_header_string(self):
        expected_result = "Thu, 01 Dec 1994 16:00:00 " + time.tzname[0]
        date = datetime.strptime(expected_result, "%a, %d %b %Y %H:%M:%S %Z")
        function_result = heuristics.datetime_to_HTTP_date(date)

        self.assertEqual(expected_result, function_result)

    def test_cache_directives_in_headers(self):
        headers = {}

        self.assertEqual(
            heuristics.cache_directives_in_headers(headers), False
        )

        headers = {"expires": "1"}

        self.assertEqual(heuristics.cache_directives_in_headers(headers), True)

        headers = {"pragma": "no-cache"}

        self.assertEqual(heuristics.cache_directives_in_headers(headers), True)

        headers = {"cache-control": "yeah"}

        self.assertEqual(heuristics.cache_directives_in_headers(headers), True)
