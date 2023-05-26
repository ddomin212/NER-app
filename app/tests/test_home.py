from app import app
import unittest
import os
import pytest

class TestHome(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_home_get(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'AIF Parser', response.data)

    def test_home_post_no_file(self):
        try:
            response = self.client.post('/')
            self.assertEqual(response.status_code, 400)
            self.assertIn(b'Bad Request', response.data)
        except Exception as e:
            pass

    @pytest.mark.skip(reason="Takes too long to run")
    def test_home_post_with_file(self):
        data = {'file': (open(os.path.join('app', 'tests', 'test.txt'), 'rb'), 'test.txt')}
        response = self.client.post('/', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Bing', response.data)

if __name__ == '__main__':
    unittest.main()