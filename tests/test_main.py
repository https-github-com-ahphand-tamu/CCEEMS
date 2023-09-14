import unittest
from main import CCEEMS

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = CCEEMS.test_client()

    def test_landing_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Childcare" in response.data.decode('utf-8'))

if __name__ == '__main__':
    unittest.main()
