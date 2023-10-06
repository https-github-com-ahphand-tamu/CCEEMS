import unittest
from main import app, db
from app.models import User, Role


class TestUserRoutes(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.app_context = app.app_context()
        self.app_context.push()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Use a separate test database
        db.create_all()

        # Create a test user and role
        test_role = Role(name='test_role')
        test_user = User(name='Test User', email='test@example.com', role=test_role)
        db.session.add(test_role)
        db.session.add(test_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # def test_login_auth_with_correct_credentials(self):
    #     response = self.app.post('/users/login', data={'email': 'test@example.com', 'password': 'your_password'})
    #     self.assertEqual(response.status_code, 302)
    #
    # def test_login_auth_with_incorrect_password(self):
    #     response = self.app.post('/users/login', data={'email': 'test@example.com', 'password': 'wrong_password'})
    #     self.assertIn(b'incorrect_password', response.data)
    #     self.assertEqual(response.status_code, 200)

    def test_get_users(self):
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test User', response.data)

    def test_get_user_by_id(self):
        response = self.app.get('/users/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test User', response.data)

    def test_get_user_by_id_nonexistent_user(self):
        response = self.app.get('/users/999')
        self.assertEqual(response.status_code, 404)

    def test_add_user(self):
        data = {
            'name': 'New User',
            'email': 'newuser@example.com',
            'role': 'test_role'
        }
        response = self.app.post('/users', json=data)
        self.assertEqual(response.status_code, 201)

    def test_add_user_with_invalid_email(self):
        data = {
            'name': 'New User',
            'email': 'invalid-email',
            'role': 'test_role'
        }
        response = self.app.post('/users', json=data)
        self.assertEqual(response.status_code, 400)

    def test_add_user_without_name(self):
        data = {
            'email': 'invalid-email',
            'role': 'test_role'
        }
        response = self.app.post('/users', json=data)
        self.assertEqual(response.status_code, 400)

    def test_add_user_without_email(self):
        data = {
            'name': 'New User',
            'role': 'test_role'
        }
        response = self.app.post('/users', json=data)
        self.assertEqual(response.status_code, 400)

    def test_add_user_without_role(self):
        data = {
            'name': 'New User',
            'email': 'newuser@example.com',
        }
        response = self.app.post('/users', json=data)
        self.assertEqual(response.status_code, 400)

    def test_add_user_invalid_role(self):
        data = {
            'name': 'New User',
            'email': 'newuser@example.com',
            'role': 'invalid role'
        }
        response = self.app.post('/users', json=data)
        self.assertEqual(response.status_code, 400)

    def test_update_user(self):
        data = {
            'name': 'Updated User',
            'email': 'updateduser@example.com',
            'role': 'test_role'
        }
        response = self.app.put('/users/1', json=data)
        self.assertEqual(response.status_code, 200)
        updated_user = db.session.get(User, 1)
        self.assertEqual(updated_user.name, 'Updated User')

    def test_update_user_nonexistent(self):
        data = {
            'name': 'Updated User',
            'email': 'updateduser@example.com',
            'role': 'test_role'
        }
        response = self.app.put('/users/2', json=data)
        self.assertEqual(response.status_code, 404)

    def test_update_user_without_name(self):
        data = {
            'email': 'updateduser@example.com',
            'role': 'test_role'
        }
        response = self.app.put('/users/1', json=data)
        self.assertEqual(response.status_code, 400)

    def test_update_user_without_email(self):
        data = {
            'name': 'Updated User',
            'role': 'test_role'
        }
        response = self.app.put('/users/1', json=data)
        self.assertEqual(response.status_code, 400)

    def test_update_user_without_invalid_email(self):
        data = {
            'name': 'Updated User',
            'email': 'invalid-email',
            'role': 'test_role'
        }
        response = self.app.put('/users/1', json=data)
        self.assertEqual(response.status_code, 400)

    def test_update_user_without_role(self):
        data = {
            'name': 'Updated User',
            'email': 'updateduser@example.com',
        }
        response = self.app.put('/users/1', json=data)
        self.assertEqual(response.status_code, 400)

    def test_delete_user(self):
        response = self.app.delete('/users/1')
        self.assertEqual(response.status_code, 204)
        deleted_user = db.session.get(User, 1)
        self.assertIsNone(deleted_user)


if __name__ == '__main__':
    unittest.main()
