import unittest
from app import app
from unittest.mock import patch, MagicMock
from werkzeug.datastructures import FileStorage

class TestExport(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    @patch('os.path.exists')
    def test_export_with_file(self, mock_path_exists):
        response = self.app.get('/api/export')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Content_Types', response.data)

    @patch('app.os.path.exists')
    def test_export_without_file(self, mock_path_exists):
        mock_path_exists.return_value = False
        response = self.app.get('/api/export')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Did not recieve', response.data)

if __name__ == '__main__':
    unittest.main()