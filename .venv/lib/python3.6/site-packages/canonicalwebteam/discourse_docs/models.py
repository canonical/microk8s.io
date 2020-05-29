# Packages
from canonicalwebteam.http import CachedSession


class DiscourseAPI:
    """
    Retrieve information from a Discourse installation
    through its API
    """

    def __init__(
        self, base_url, session=CachedSession(fallback_cache_duration=300)
    ):
        """
        @param base_url: The Discourse URL (e.g. https://discourse.example.com)
        """

        self.base_url = base_url.rstrip("/")
        self.session = session

    def __del__(self):
        self.session.close()

    def get_topic(self, topic_id):
        """
        Retrieve topic object by path
        """

        response = self.session.get(f"{self.base_url}/t/{topic_id}.json")
        response.raise_for_status()

        return response.json()

    def get_topics_category(self, category_id, page=0):
        response = self.session.get(
            f"{self.base_url}/c/{category_id}.json?page={page}"
        )
        response.raise_for_status()

        return response.json()
