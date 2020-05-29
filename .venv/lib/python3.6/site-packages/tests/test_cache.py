import json
import os
import shutil
import sys
import time
import unittest
import warnings
from unittest.mock import patch

import httpretty
import redis
import requests
from canonicalwebteam.http import CachedSession
from freezegun import freeze_time

from mockredis import mock_redis_client

file_cache_directory = ".testcache"


class MockRedisSingletons:
    def __init__(self):
        self.redis_clients = {}

    def mock_redis_client_singleton(self, connection_pool, *args, **kwargs):

        # A name has to passed into the connection pool, this will make sure
        # that different Redis instances can be mocked
        name = connection_pool.name

        if name not in self.redis_clients:
            self.redis_clients[name] = mock_redis_client()
            self.redis_clients[name].name = name
        return self.redis_clients[name]


class TestCachedSession(unittest.TestCase):
    mock_redis_singletons = MockRedisSingletons()

    def setUp(self):
        if not sys.warnoptions:
            warnings.simplefilter("ignore")

    def tearDown(self):
        if os.path.exists(file_cache_directory):
            shutil.rmtree(file_cache_directory)

    @httpretty.activate
    def test_custom_heuristic(self):
        def request_callback(request, uri, response_headers):
            return [200, response_headers, json.dumps({"epoch": time.time()})]

        httpretty.register_uri(
            httpretty.GET, "https://now.httpbin.org", body=request_callback
        )

        session = CachedSession(
            fallback_cache_duration=2,
            file_cache_directory=file_cache_directory,
        )

        # with a 2s retention, and a 1.1s time between requests, 2 of the
        # request should have the same epoch, where as the 3rd gets fresh data
        # the first requests gets send at t=0

        with freeze_time("2012-01-14 12:00:01") as freezer:
            response_1 = session.get("https://now.httpbin.org")
            freezer.tick()

            response_2 = session.get("https://now.httpbin.org")
            freezer.tick()

            response_3 = session.get("https://now.httpbin.org")

            self.assertEqual(response_1.text, response_2.text)
            self.assertNotEqual(response_2.text, response_3.text)

    @httpretty.activate
    def test_default_heuristic(self):
        def request_callback(request, uri, response_headers):
            return [200, response_headers, json.dumps({"epoch": time.time()})]

        httpretty.register_uri(
            httpretty.GET, "https://now.httpbin.org", body=request_callback
        )

        session = CachedSession(file_cache_directory=file_cache_directory)

        with freeze_time("2012-01-14 12:00:01") as freezer:

            response_1 = session.get("https://now.httpbin.org")
            freezer.tick()
            freezer.tick()

            response_2 = session.get("https://now.httpbin.org")
            freezer.tick()
            freezer.tick()
            freezer.tick()

            response_3 = session.get("https://now.httpbin.org")

            self.assertEqual(response_1.text, response_2.text)
            self.assertNotEqual(response_2.text, response_3.text)

    @httpretty.activate
    def test_cache_control_max_age_overwrites_custom_heuristic(self):
        def request_callback(request, uri, response_headers):
            return [200, response_headers, json.dumps({"epoch": time.time()})]

        httpretty.register_uri(
            httpretty.GET,
            "https://now.httpbin.org",
            body=request_callback,
            adding_headers={"Cache-Control": "max-age=2"},
        )

        session = CachedSession(file_cache_directory=file_cache_directory)

        with freeze_time("2012-01-14 12:00:01") as freezer:

            response_1 = session.get("https://now.httpbin.org")
            freezer.tick()
            response_2 = session.get("https://now.httpbin.org")
            freezer.tick()
            response_3 = session.get("https://now.httpbin.org")

            self.assertEqual(response_1.text, response_2.text)
            self.assertNotEqual(response_2.text, response_3.text)

    @httpretty.activate
    def test_cache_control_no_cache_overwrites_custom_heuristic(self):
        def request_callback(request, uri, response_headers):
            return [200, response_headers, json.dumps({"epoch": time.time()})]

        httpretty.register_uri(
            httpretty.GET,
            "https://now.httpbin.org",
            body=request_callback,
            adding_headers={"Cache-Control": "no-cache"},
        )
        session = CachedSession(file_cache_directory=file_cache_directory)

        # with no-cache set, no request should be cached,
        # thus all bodies are different
        response_1 = session.get("https://now.httpbin.org")
        response_2 = session.get("https://now.httpbin.org")
        response_3 = session.get("https://now.httpbin.org")

        self.assertNotEqual(response_1.text, response_2.text)
        self.assertNotEqual(response_2.text, response_3.text)

    @httpretty.activate
    def test_file_cache(self):
        def request_callback(request, uri, response_headers):
            return [200, response_headers, json.dumps({"epoch": time.time()})]

        httpretty.register_uri(
            httpretty.GET, "https://now.httpbin.org", body=request_callback
        )

        cache_dir_1 = ".test1"
        cache_dir_2 = ".test2"

        session_1 = CachedSession(
            file_cache_directory=cache_dir_1, fallback_cache_duration=2000
        )
        session_2 = CachedSession(file_cache_directory=cache_dir_2)

        resp_1 = session_1.get("https://now.httpbin.org")

        self.assertEqual(os.path.isdir(cache_dir_1), True)

        resp_2 = session_2.get("https://now.httpbin.org")

        self.assertEqual(os.path.isdir(cache_dir_2), True)
        self.assertNotEqual(resp_1.text, resp_2.text)

        shutil.rmtree(cache_dir_2)

        self.assertEqual(os.path.isdir(cache_dir_2), False)

        resp_3 = session_2.get("https://now.httpbin.org")

        self.assertEqual(os.path.isdir(cache_dir_2), True)
        self.assertNotEqual(resp_2.text, resp_3.text)

        session_3 = CachedSession(
            file_cache_directory=cache_dir_1, fallback_cache_duration=2000
        )

        resp_4 = session_3.get("https://now.httpbin.org")

        self.assertEqual(resp_1.text, resp_4.text)

        shutil.rmtree(cache_dir_1)
        shutil.rmtree(cache_dir_2)

    @httpretty.activate
    @patch("redis.Redis", mock_redis_singletons.mock_redis_client_singleton)
    def test_redis_cache(self):
        class FakeConnectionPool:
            def __init__(self, name):
                self.name = name

        # our mock will be called here. Passing a connection_pool with a name
        # makes sure that we can identify the different redis mocks

        redis_mock_1 = redis.Redis(
            connection_pool=FakeConnectionPool(name="test1")
        )
        redis_mock_2 = redis.Redis(
            connection_pool=FakeConnectionPool(name="test2")
        )

        self.assertNotEqual(redis_mock_1, redis_mock_2)

        def request_callback(request, uri, response_headers):
            return [200, response_headers, json.dumps({"epoch": time.time()})]

        httpretty.register_uri(
            httpretty.GET, "https://now.httpbin.org", body=request_callback
        )

        with freeze_time("2012-01-14 12:00:01") as freezer:
            session_1 = CachedSession(
                redis_connection=redis_mock_1, fallback_cache_duration=500
            )
            session_2 = CachedSession(
                redis_connection=redis_mock_2, fallback_cache_duration=1
            )

            resp_1 = session_1.get("https://now.httpbin.org")
            resp_2 = session_2.get("https://now.httpbin.org")

            self.assertNotEqual(resp_1.text, resp_2.text)

            freezer.tick()

            resp_3 = session_2.get("https://now.httpbin.org")

            self.assertNotEqual(resp_2.text, resp_3.text)

            session_3 = CachedSession(
                redis_connection=redis_mock_1, fallback_cache_duration=1
            )

            resp_4 = session_3.get("https://now.httpbin.org")

            self.assertEqual(resp_1.text, resp_4.text)

    def test_timeout_adapter(self):
        session = CachedSession(
            timeout=2, file_cache_directory=file_cache_directory
        )

        # this test can be inconsistent on multiple concurrent
        # runs due to the use of time.sleep
        with self.assertRaises(
            (
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ReadTimeout,
            )
        ):
            session.get("https://httpbin.org/delay/3")

        resp = session.get("https://httpbin.org/delay/1")

        self.assertIsNotNone(resp)


if __name__ == "__main__":
    unittest.main()
