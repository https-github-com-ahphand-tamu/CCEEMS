import unittest
from main import CCEMS

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = CCEMS.test_client()

    def test_landing_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Childcare" in response.data.decode('utf-8'))

if __name__ == '__main__':
    unittest.main()
