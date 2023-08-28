import unittest
from webapp.app import app


class TestRoutes(unittest.TestCase):
    def setUp(self):
        """
        Set up Flask app for testing
        """
        app.testing = True
        self.client = app.test_client()

    def test_homepage(self):
        """
        When given the index URL,
        we should return a 200 status code
        """

        self.assertEqual(self.client.get("/").status_code, 200)

    def test_features(self):
        """
        When given the /features URL,
        we should return a 200 status code
        """

        self.assertEqual(self.client.get("/features").status_code, 200)

    def test_compare(self):
        """
        When given the /compare URL,
        we should return a 200 status code
        """

        self.assertEqual(self.client.get("/compare").status_code, 200)

    def test_tutorials(self):
        """
        When given the /tutorials URL,
        we should return a 200 status code
        """

        self.assertEqual(self.client.get("/tutorials").status_code, 200)

    def test_docs(self):
        """
        When given the /docs URL,
        we should return a 200 status code
        """

        self.assertEqual(self.client.get("/docs").status_code, 200)

    def test_resources(self):
        """
        When given the /resources URL,
        we should return a 200 status code
        """

        self.assertEqual(self.client.get("/resources").status_code, 200)

    def test_contact_us(self):
        """
        When given the /contact-us URL,
        we should return a 200 status code
        """

        self.assertEqual(self.client.get("/contact-us").status_code, 200)

    def test_not_found(self):
        """
        When given a non-existent URL,
        we should return a 404 status code
        """

        self.assertEqual(self.client.get("/not-found-url").status_code, 404)


if __name__ == "__main__":
    unittest.main()
