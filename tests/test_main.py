import unittest
from main import app


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_home_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('Redirecting...</h1>\n<p>You should be redirected automatically to the target URL: <a href="/user/login">/user/login</a>.',
                      response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
