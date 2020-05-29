from datetime import datetime, timedelta

from cachecontrol.heuristics import BaseHeuristic


def expire_after(delta, date=None):
    date = date or datetime.utcnow()
    return date + delta


def datetime_to_HTTP_date(date_and_time):
    """
    Returns a HTTP-date as defined in rfc7234 section 5.3
    for a datetime object"""

    return datetime.astimezone(date_and_time).strftime(
        "%a, %d %b %Y %H:%M:%S %Z"
    )


def cache_directives_in_headers(headers):
    """
    Checks if cache controls are set in response headers
    """
    cache_control = "cache-control" in headers
    pragma = "pragma" in headers and "no-cache" in headers["pragma"]
    expires = "expires" in headers

    return expires or pragma or cache_control


class ExpiresAfterIfNoCacheControl(BaseHeuristic):
    """
    Cache **all** requests for a defined time period.
    """

    def __init__(self, **kw):
        self.delta = timedelta(**kw)

    def update_headers(self, response):
        """
        If no caching controls are present,
        a default expires header will be set
        """
        if cache_directives_in_headers(response.headers):
            return

        expires = expire_after(self.delta)

        return {
            "expires": datetime_to_HTTP_date(expires),
            "cache-control": "public",
        }

    def warning(self, response):
        """
        Adds a warning to the response as defined in rfc7234 section 5.5
        :param response: The response object to be manipulated.
        """
        template = "110 - Automatically cached for %s. Response might be stale"
        return template % self.delta

    def apply(self, response):
        """
        Applies the heuristic to the response
        """
        updated_headers = self.update_headers(response)

        if updated_headers:
            response.headers.update(updated_headers)
            warning_header_value = self.warning(response)
            if warning_header_value is not None:
                response.headers.update({"Warning": warning_header_value})

        return response
