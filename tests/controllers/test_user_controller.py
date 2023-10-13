import unittest
from main import app, db
from app.models import User, Role

from werkzeug.security import generate_password_hash


class TestUserRoutes(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True
        self.app_context = app.app_context()
        self.app_context.push()

        db.create_all()

        # Create a test user and role
        test_role = Role(name='Admin')
        test_user = User(name='Test User', email="test@example.com", role=test_role)
        test_user.password = generate_password_hash("test123")
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

    def test_login_auth_with_correct_credentials(self):
        response = self.login_user("test@example.com", "test123")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], "/index")

    def test_login_auth_user_does_not_exist(self):
        response = self.login_user("nouser@example.com", "no-user")
        self.assertIn(b'Incorrect Password', response.data)
        self.assertEqual(response.status_code, 200)

    def test_login_auth_with_incorrect_password(self):
        response = self.login_user("test@example.com", "not-right-password")
        self.assertIn(b'Incorrect Password', response.data)
        self.assertEqual(response.status_code, 200)

    def test_get_user_by_id(self):
        self.login_user("test@example.com", "test123")
        response = self.client.get('/user/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test User', response.data)

    def test_get_user_by_id_unauthorizd_id(self):
        self.login_user("test@example.com", "test123")
        response = self.client.get('/user/2')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], "/index")

    def test_get_user_by_id_nonexistent_user(self):
        self.login_user("test@example.com", "test123")
        response = self.client.get('/user/999')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], "/index")

    def test_update_user(self):
        self.login_user("test@example.com", "test123")
        data = {
            'name': 'Updated User',
            'email': 'updateduser@example.com',
            'role': 'Admin'
        }
        response = self.client.put('/user/1', json=data)
        self.assertEqual(response.status_code, 200)
        updated_user = db.session.get(User, 1)
        self.assertEqual(updated_user.name, 'Updated User')

    def test_update_user_nonexistent(self):
        self.login_user("test@example.com", "test123")
        data = {
            'name': 'Updated User',
            'email': 'updateduser@example.com',
            'role': 'Admin'
        }
        response = self.client.put('/user/2', json=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], "/index")

    def test_update_user_without_name(self):
        self.login_user("test@example.com", "test123")
        data = {
            'email': 'updateduser@example.com',
            'role': 'Admin'
        }
        response = self.client.put('/user/1', json=data)
        self.assertEqual(response.status_code, 400)

    def test_update_user_without_email(self):
        self.login_user("test@example.com", "test123")
        data = {
            'name': 'Updated User',
            'role': 'Admin'
        }
        response = self.client.put('/user/1', json=data)
        self.assertEqual(response.status_code, 400)

    def test_update_user_without_invalid_email(self):
        self.login_user("test@example.com", "test123")
        data = {
            'name': 'Updated User',
            'email': 'invalid-email',
            'role': 'Admin'
        }
        response = self.client.put('/user/1', json=data)
        self.assertEqual(response.status_code, 400)

    def test_update_user_without_role(self):
        self.login_user("test@example.com", "test123")
        data = {
            'name': 'Updated User',
            'email': 'updateduser@example.com',
        }
        response = self.client.put('/user/1', json=data)
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
