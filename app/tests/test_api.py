import unittest
from app import app
import json
from unittest.mock import patch
from revChatGPT.typings import AuthenticationError

class TestGptModal(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        
    @patch('app.functions.ai_helpers.get_response')
    def test_gpt_modal_with_data(self, mock_get_response):
        data = {'name': 'Theodore Roosevelt', 'tags': "PERSON"}
        try:
            response = self.app.post('/api/gpt-modal', data=json.dumps(data), content_type='application/json')
            mock_get_response.return_value = ('test response', 'test img_url')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'response', response.data)
            self.assertIn(b'img_url', response.data)
        except AuthenticationError as e:
            pass

    def test_gpt_modal_without_data(self):
        response = self.app.post('/api/gpt-modal')
        print(response)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Bad Request', response.data)

if __name__ == '__main__':
    unittest.main()