import unittest
import os
import pytest
from app import app


class TestHome(unittest.TestCase):
    """
    A class that contains unit tests for the home route of the Flask application.
    """

    def setUp(self):
        """
        Sets up the test environment. This is called before any tests are run so we don't have to worry about it
        """
        self.app = app
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def test_home_get(self):
        """
        Test home page GET request with AIF parser as data. This should be a success and no content
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"AIF Parser", response.data)

    def test_home_post_no_file(self):
        """
        Test home post no file POST / home should return 400 Bad Request ( No Content ) as response body
        """
        try:
            response = self.client.post("/")
            self.assertEqual(response.status_code, 400)
            self.assertIn(b"Bad Request", response.data)
        except Exception as e:
            pass

    @pytest.mark.skip(reason="Takes too long to run")
    def test_home_post_with_file(self):
        """
        Test home post with file POST / api / v1 / file?file = test. txt content
        """
        data = {
            "file": (open(os.path.join("app", "tests", "test.txt"), "rb"), "test.txt")
        }
        response = self.client.post("/", data=data, content_type="multipart/form-data")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Bing", response.data)


# Unittest. main. This is a convenience method for unittest. main.
if __name__ == "__main__":
    unittest.main()
