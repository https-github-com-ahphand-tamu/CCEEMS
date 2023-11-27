import unittest
from main import app, db
from app.models import User, Role

from werkzeug.security import generate_password_hash
import uuid


class TestApp(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True
        self.app_context = app.app_context()
        self.app_context.push()

        db.create_all()

        # Create a test user and role
        test_role = Role(name='Admin')
        test_user = User(name='Test User',
                         email="test@example.com", role=test_role)
        test_user.password = generate_password_hash("test123")
        test_user.verification_code=str(uuid.uuid1())
        db.session.add(test_role)
        db.session.add(test_user)
        db.session.commit()

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

    def test_home_route_unauthenticated(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertIn(
            'Redirecting...</h1>\n<p>You should be redirected automatically to the target URL: <a href="/user/login">/user/login</a>.',
            response.data.decode('utf-8'))

    def test_home_route_authenticated(self):
        response = self.login_user("test@example.com", "test123")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], "/")

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Home Page',
                      response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
