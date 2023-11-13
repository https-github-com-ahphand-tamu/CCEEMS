import json
import unittest
from main import app, db
from app.models import User, Role

from werkzeug.security import generate_password_hash


class TestRoleRoutes(unittest.TestCase):

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

    def test_get_roles(self):
        response = self.client.get('/roles')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data.decode('utf-8'))
        self.assertListEqual(
            response_json["data"],
            [{'id': 1, 'name': 'Admin'}, {'id': 2, 'name': 'Eligibility Supervisor'}])


if __name__ == '__main__':
    unittest.main()
