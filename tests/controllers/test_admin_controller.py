import unittest
from main import app, db
from app.models import User, Role

from werkzeug.security import generate_password_hash


class TestAdminRoutes(unittest.TestCase):

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

        admin_user = User(name='Admin User', email='admin@example.com', role=admin_role)
        admin_user.password = generate_password_hash("admin123")
        db.session.add(admin_user)

        test_user = User(name='Test User', email='test1@example.com', role=test_role)
        test_user.password = generate_password_hash("user123")
        db.session.add(test_user)

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

    def test_get_users(self):
        response = self.client.get('/admin/users')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test User', response.data)

    def test_get_user_by_id(self):
        response = self.client.get('/admin/users/2')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test User', response.data)

    def test_get_user_by_id_nonexistent_user(self):
        response = self.client.get('/admin/users/999')
        self.assertEqual(response.status_code, 404)

    def test_add_user(self):
        data = {
            'name': 'New User',
            'email': 'newuser@example.com',
            'role': 'Admin'
        }
        response = self.client.post('/admin/users', json=data)
        self.assertEqual(response.status_code, 201)

    def test_add_user_with_invalid_email(self):
        data = {
            'name': 'New User',
            'email': 'invalid-email',
            'role': 'Admin'
        }
        response = self.client.post('/admin/users', json=data)
        self.assertEqual(response.status_code, 400)

    def test_add_user_with_duplicate_email(self):
        data = {
            'name': 'Test User',
            'email': 'test1@example.com',
            'role': 'Admin'
        }
        response = self.client.post('/admin/users', json=data)
        self.assertEqual(response.status_code, 400)

    def test_add_user_without_name(self):
        data = {
            'email': 'invalid-email',
            'role': 'Admin'
        }
        response = self.client.post('/admin/users', json=data)
        self.assertEqual(response.status_code, 400)

    def test_add_user_without_email(self):
        data = {
            'name': 'New User',
            'role': 'Admin'
        }
        response = self.client.post('/admin/users', json=data)
        self.assertEqual(response.status_code, 400)

    def test_add_user_without_role(self):
        data = {
            'name': 'New User',
            'email': 'newuser@example.com',
        }
        response = self.client.post('/admin/users', json=data)
        self.assertEqual(response.status_code, 400)

    def test_add_user_invalid_role(self):
        data = {
            'name': 'New User',
            'email': 'newuser@example.com',
            'role': 'invalid role'
        }
        response = self.client.post('/admin/users', json=data)
        self.assertEqual(response.status_code, 400)

    def test_update_user(self):
        data = {
            'name': 'Updated User',
            'email': 'updateduser@example.com',
            'role': 'Admin'
        }
        response = self.client.put('/admin/users/2', json=data)
        self.assertEqual(response.status_code, 200)
        updated_user = db.session.get(User, 2)
        self.assertEqual(updated_user.name, 'Updated User')

    def test_update_user_nonexistent(self):
        data = {
            'name': 'Updated User',
            'email': 'updateduser@example.com',
            'role': 'Admin'
        }
        response = self.client.put('/admin/users/3', json=data)
        self.assertEqual(response.status_code, 404)

    def test_update_user_without_name(self):
        data = {
            'email': 'updateduser@example.com',
            'role': 'Admin'
        }
        response = self.client.put('/admin/users/2', json=data)
        self.assertEqual(response.status_code, 400)

    def test_update_user_without_email(self):
        data = {
            'name': 'Updated User',
            'role': 'Admin'
        }
        response = self.client.put('/admin/users/2', json=data)
        self.assertEqual(response.status_code, 400)

    def test_update_user_without_invalid_email(self):
        data = {
            'name': 'Updated User',
            'email': 'invalid-email',
            'role': 'Admin'
        }
        response = self.client.put('/admin/users/2', json=data)
        self.assertEqual(response.status_code, 400)

    def test_update_user_without_role(self):
        data = {
            'name': 'Updated User',
            'email': 'updateduser@example.com',
        }
        response = self.client.put('/admin/users/2', json=data)
        self.assertEqual(response.status_code, 400)

    def test_delete_user(self):
        response = self.client.delete('/admin/users/2')
        self.assertEqual(response.status_code, 204)
        deleted_user = db.session.get(User, 2)
        self.assertIsNone(deleted_user)



if __name__ == '__main__':
    unittest.main()
