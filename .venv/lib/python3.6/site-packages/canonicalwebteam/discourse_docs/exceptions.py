class PathNotFoundError(Exception):
    """
    The URL path wasn't recognised
    """

    def __init__(self, path, *args, message=None, **kwargs):
        self.path = path

        if not message:
            message = f"Path {path} not found"

        super().__init__(message, *args, **kwargs)


class RedirectFoundError(Exception):
    """
    If we encounter redirects from Discourse, we need to take action
    """

    def __init__(self, path, target_url, *args, message=None, **kwargs):
        self.path = path
        self.target_url = target_url

        if not message:
            message = f"Path {path} has moved to {target_url}"

        super().__init__(*args, **kwargs)
