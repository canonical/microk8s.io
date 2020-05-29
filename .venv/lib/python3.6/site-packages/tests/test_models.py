import unittest
import httpretty

from canonicalwebteam.discourse_docs.models import DiscourseAPI
from tests.fixtures.forum_mock import register_uris


class TestDiscourseAPI(unittest.TestCase):
    def setUp(self):
        httpretty.enable()
        register_uris()

        self.api = DiscourseAPI(base_url="https://discourse.example.com")

    def test_get_topic(self):
        """
        Check the DiscourseAPI object can get a topic by its ID
        """

        topic = self.api.get_topic(34)

        self.assertEqual(topic["id"], 34)
        self.assertEqual(topic["title"], "An index page")


if __name__ == "__main__":
    unittest.main()
