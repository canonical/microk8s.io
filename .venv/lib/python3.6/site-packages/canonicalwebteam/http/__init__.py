# Core packages
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

# Third-party packages
import requests
from cachecontrol import CacheControlAdapter
from cachecontrol.caches import FileCache
from cachecontrol.caches.redis_cache import RedisCache
from canonicalwebteam.http.heuristics import ExpiresAfterIfNoCacheControl
from requests import adapters, Session

try:
    # If prometheus is available, set up metric counters

    import prometheus_client

    TIMEOUT_COUNTER = prometheus_client.Counter(
        "feed_timeouts", "A counter of timed out requests", ["domain"]
    )
    CONNECTION_FAILED_COUNTER = prometheus_client.Counter(
        "feed_connection_failures",
        "A counter of requests which failed to connect",
        ["domain"],
    )
    LATENCY_HISTOGRAM = prometheus_client.Histogram(
        "feed_latency_seconds",
        "Feed requests retrieved",
        ["domain", "code"],
        buckets=[0.25, 0.5, 0.75, 1, 2, 3],
    )
except ImportError:
    TIMEOUT_COUNTER = None
    CONNECTION_FAILED_COUNTER = None
    LATENCY_HISTOGRAM = None


class TimeoutHTTPAdapter(adapters.HTTPAdapter):
    """
    A simple extension to the HTTPAdapter to add a 'timeout' parameter
    """

    def __init__(self, timeout=None, *args, **kwargs):
        self.timeout = timeout
        super(TimeoutHTTPAdapter, self).__init__(*args, **kwargs)

    def send(self, *args, **kwargs):
        kwargs["timeout"] = self.timeout
        return super(TimeoutHTTPAdapter, self).send(*args, **kwargs)


class BaseSession(Session):
    """
    A base session interface to implement common functionality:

    - timeout: Set timeout for outgoing requests
    - headers: Additional headers to add to all outgoing requests
    """

    def __init__(self, timeout=(0.5, 3), headers={}, *args, **kwargs):
        super(BaseSession, self).__init__(*args, **kwargs)

        self.mount("http://", TimeoutHTTPAdapter(timeout=timeout))
        self.mount("https://", TimeoutHTTPAdapter(timeout=timeout))

        self.headers.update(headers)

    def request(self, method, url, **kwargs):
        domain = urlparse(url).netloc

        try:
            request = super(BaseSession, self).request(
                method=method, url=url, **kwargs
            )
        except requests.exceptions.Timeout as timeout_error:
            if TIMEOUT_COUNTER:
                TIMEOUT_COUNTER.labels(domain=domain).inc()

            raise timeout_error
        except requests.exceptions.ConnectionError as connection_error:
            if CONNECTION_FAILED_COUNTER:
                CONNECTION_FAILED_COUNTER.labels(domain=domain).inc()

            raise connection_error

        if LATENCY_HISTOGRAM:
            LATENCY_HISTOGRAM.labels(
                domain=domain, code=request.status_code
            ).observe(request.elapsed.total_seconds())

        return request


class UncachedSession(BaseSession, Session):
    """
    A session object for making HTTP requests directly, using the default
    settings from BaseSession
    """

    pass


class CacheAdapterWithTimeout(CacheControlAdapter):
    """
    A combination of the CacheControl and Timeout adapter
    to provide both functionalities.
    """

    def __init__(self, heuristic, cache, timeout=None, *args, **kwargs):
        self.timeout = timeout
        super(CacheAdapterWithTimeout, self).__init__(
            cache=cache, heuristic=heuristic, *args, **kwargs
        )

    def send(self, *args, **kwargs):
        kwargs["timeout"] = self.timeout
        return super(CacheAdapterWithTimeout, self).send(*args, **kwargs)


class CachedSession(BaseSession, Session):
    """
     A session object that implements CacheControl functionality with
     our default settings from BaseSession.

     The session respects cache control headers to manage the caching strategy
     and saves responses in a file or redis cache.
     If CacheControl headers are not provided a custom duration time
     for caching can be passed as a fallback strategy.

     :param redis_connection_pool: Port of your Redis instance
     :param file_cache_directory: Name for the directory to store cache on
     :param fallback_cache_duration: Duration in seconds for fallback caching
         retention when no CacheControl headers are set
     :param timeout: Set the timeout for outgoing requests
     """

    def __init__(
        self,
        redis_connection=None,
        fallback_cache_duration=5,
        file_cache_directory=".webcache",
        timeout=(0.5, 3),
        *args,
        **kwargs
    ):
        super(CachedSession, self).__init__(*args, **kwargs)

        heuristic = ExpiresAfterIfNoCacheControl(
            seconds=fallback_cache_duration
        )
        cache = FileCache(file_cache_directory)

        if redis_connection:
            cache = RedisCache(redis_connection)

        adapter = CacheAdapterWithTimeout(
            heuristic=heuristic, cache=cache, timeout=timeout
        )

        self.mount("http://", adapter)
        self.mount("https://", adapter)
