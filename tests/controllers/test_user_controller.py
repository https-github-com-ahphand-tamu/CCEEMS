import mock
import unittest

from main import app, db
from app.models import User, Role

from werkzeug.security import generate_password_hash
import uuid


class TestUserRoutes(unittest.TestCase):

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
        test_user.verification_code = uuid.uuid1()
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

    def set_password(self, email, password, repassword):
        response = self.client.post('/users/updatePassword', data=dict(
            email=email,
            password=password
        ))
        return response

    def test_get_login_auth_unauthenticated(self):
        response = self.client.get("/user/login")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Login', response.data.decode('utf-8'))

    def test_post_login_auth_with_correct_credentials(self):
        response = self.login_user("test@example.com", "test123")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], "/")

    def test_get_login_auth_authenticated(self):
        response = self.login_user("test@example.com", "test123")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], "/")

        response2 = self.client.get("/user/login")
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(response2.headers['Location'], "/")

    def test_login_auth_user_does_not_exist(self):
        response = self.login_user("nouser@example.com", "no-user")
        self.assertIn(b'Incorrect Password', response.data)
        self.assertEqual(response.status_code, 200)

    def test_login_auth_with_incorrect_password(self):
        response = self.login_user("test@example.com", "not-right-password")
        self.assertIn(b'Incorrect Password', response.data)
        self.assertEqual(response.status_code, 200)

    def test_login_auth_with_no_email(self):
        response = self.client.post('/user/login', data=dict(
            password="test123"
        ))
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            b'Missing required fields (email, password)', response.data)

    def test_login_auth_with_no_password(self):
        response = self.client.post('/user/login', data=dict(
            email="test@example.com"
        ))
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            b'Missing required fields (email, password)', response.data)

    def test_logout_user(self):
        response = self.login_user("test@example.com", "test123")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], "/")

        self.client.post("/user/logout")

        response3 = self.client.get("/")
        self.assertEqual(response3.status_code, 302)
        self.assertEqual(response3.headers['Location'], "/user/login")

    def test_get_user_by_id(self):
        self.login_user("test@example.com", "test123")
        response = self.client.get('/user/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test User', response.data)

    def test_get_user_by_id_unauthorizd_id(self):
        self.login_user("test@example.com", "test123")
        response = self.client.get('/user/2')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], "/")

    def test_get_user_by_id_nonexistent_user(self):
        self.login_user("test@example.com", "test123")
        response = self.client.get('/user/999')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], "/")

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
        self.assertEqual(response.headers['Location'], "/")

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

    def test_update_password_with_invalid_user(self):
        self.login_user("test@example.com", "test123")

        response = self.client.post("/user/updatePassword?user=123456", data={
            "email": "test3@tamu.edu",
            "password": "password",
            "re-password": "password"
        })
        self.assertEqual(response.status_code, 404)

    def test_update_password_with_existing_user(self):
        self.login_user("test@example.com", "test123")
        test_user = db.session.query(User).filter(
            User.email == "test@example.com").first()
        response = self.client.post(f"/user/updatePassword?user={test_user.verification_code}", data={
            "email": "test@example.com",
            "password": "password",
            "re-password": "password"
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn("User already verified", response.text)

    def test_update_password_with_invalid_string_length(self):
        self.login_user("test@example.com", "test123")
        
        response = self.client.post('/admin/users', json={
            "name": "Test User3",
            "email": "test3@tamu.edu",
            "role": "Admin"
        })

        test_user = db.session.query(User).filter(
            User.email == "test3@tamu.edu").first()
        verification_code = uuid.uuid1()
        test_user.verification_code = verification_code
        db.session.commit()
        response = self.client.post(f"/user/updatePassword?user={verification_code}", data={
            "email": "test3@tamu.edu",
            "password": "abcd",
            "re-password": "abcd"
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Password Must be at least 8 characters long", response.text)

    def test_update_password_with_password_mismatch(self):
        self.login_user("test@example.com", "test123")

        self.client.post('/admin/users', json={
            "name": "Test User3",
            "email": "test3@tamu.edu",
            "role": "Admin"
        })

        test_user = db.session.query(User).filter(
            User.email == "test3@tamu.edu").first()
        verification_code = uuid.uuid1()
        test_user.verification_code = verification_code
        db.session.commit()

        response = self.client.post(f"/user/updatePassword?user={verification_code}", data={
            "email": "test3@tamu.edu",
            "password": "abcd1234567",
            "re-password": "abcdsdsdvdsd"
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn("Both the passwords should match", response.text)

    def test_update_user_with_database_error(self):
        self.login_user("test@example.com", "test123")
        data = {
            'name': 'Updated User',
            'email': 'updateduser@example.com',
            'role': 'Admin'
        }

        with mock.patch('app.db.session.commit', side_effect=Exception('Simulated database error')):
            response = self.client.put('/user/1', json=data)

        self.assertEqual(response.status_code, 500)
        self.assertIn(b'Failed to update user', response.data)


if __name__ == '__main__':
    unittest.main()
