import unittest
from unittest.mock import patch
from app import app


class TestExport(unittest.TestCase):
    """
    A class that contains unit tests for the export route of the Flask application.
    """

    def setUp(self):
        """
        Sets up the test environment. This is called before any tests are run so we don't have to worry about it
        """
        app.config["TESTING"] = True
        self.app = app.test_client()

    @patch("os.path.exists")
    def test_export_with_file(self):
        """
        Test exporting a file with a file name.
        """
        response = self.app.get("/api/export")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Content_Types", response.data)

    @patch("app.os.path.exists")
    def test_export_without_file(self, mock_path_exists):
        """
        Test export without file.

        @param mock_path_exists - Function that returns True if the path exists
        """
        mock_path_exists.return_value = False
        response = self.app.get("/api/export")
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Did not recieve", response.data)


# Unittest. main. This is a convenience method for unittest. main
if __name__ == "__main__":
    unittest.main()
