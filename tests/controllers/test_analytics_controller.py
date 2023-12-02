import json
import unittest
from main import app, db
from app.models import PacketReturnStatus, Decision, Case, User, Role

from werkzeug.security import generate_password_hash


class TestAnalyticsRoutes(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True
        self.app_context = app.app_context()
        self.app_context.push()

        db.create_all()

        admin_role = Role(name='Admin')
        test_role = Role(name='Eligibility Supervisor')
        db.session.add(admin_role)
        db.session.add(test_role)
        db.session.commit()

        admin_user = User(name='Admin User',
                          email='admin@example.com', role=admin_role)
        admin_user.password = generate_password_hash("admin123")
        db.session.add(admin_user)
        db.session.commit()

        test_case = Case(customer_id = 1, first_name = 'Jhon', last_name = 'Doe', num_of_children = 4, outreach_date = '2023-05-14')
        db.session.add(test_case)
        db.session.commit()

        self.login_user('admin@example.com', "admin123")

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login_user(self, email, password):
        response = self.client.post('/user/login', data=dict(
            email=email,
            password=password
        ))
        return response

    def test_get_years(self):
        response = self.client.get('/analytics/get_years')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data.decode('utf-8'))
        self.assertListEqual(
            response_json["data"],
            ['2023'])
        
    def test_get_packets_sent_graph(self):
        response = self.client.get('/analytics/packets_sent?year=2023')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data.decode('utf-8'))

    def test_get_packets_return_graph(self):
        response = self.client.get('/analytics/packets_status?year=2023')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data.decode('utf-8'))

    def test_get_children_enrolled_graph(self):
        response = self.client.get('/analytics/children_enrolled?year=2023')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data.decode('utf-8'))

    def test_get_children_not_enrolled_enrolled(self):
        response = self.client.get('/analytics/children_not_enrolled?year=2023')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data.decode('utf-8'))
    
    def test_get_not_enrolled_reasons_graph(self):
        response = self.client.get('/analytics/children_not_enrolled_reasons?year=2023')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data.decode('utf-8'))

    def test_get_processing_time_graph(self):
        response = self.client.get('/analytics/processing_time?year=2023')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
