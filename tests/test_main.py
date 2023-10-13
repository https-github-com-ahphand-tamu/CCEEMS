import unittest
from main import app


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_home_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Login Page", response.data.decode('utf-8'))

if __name__ == '__main__':
    unittest.main()
