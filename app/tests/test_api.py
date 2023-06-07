import unittest
import json
from unittest.mock import patch
from revChatGPT.typings import AuthenticationError
from app import app


class TestGptModal(unittest.TestCase):
    """
    A class that contains unit tests for the GPT API of the Flask application.
    """

    def setUp(self):
        """
        Sets up the test environment. This is called
        before any tests are run so we don't have to worry about it
        """
        app.config["TESTING"] = True
        self.app = app.test_client()

    @patch("app.functions.app_helpers.get_response")
    def test_gpt_modal_with_data(self, mock_get_response):
        """
        Test gpt modals with data. The data should be encoded as JSON and passed to the request.

        @param mock_get_response - mock get response to use
        """
        data = {"name": "Theodore Roosevelt", "tags": "PERSON"}
        try:
            response = self.app.post(
                "/api/gpt-modal", data=json.dumps(data), content_type="application/json"
            )
            mock_get_response.return_value = ("test response", "test img_url")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"response", response.data)
            self.assertIn(b"img_url", response.data)
        except AuthenticationError:
            pass

    def test_gpt_modal_without_data(self):
        """
        Test gpt - modal without data returns 400 Bad Request ( not valid GPT request ) for non
        """
        response = self.app.post("/api/gpt-modal")
        print(response)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Bad Request", response.data)


# Unittest. main. This is a convenience method for unittest. main
if __name__ == "__main__":
    unittest.main()
