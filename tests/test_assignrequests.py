import unittest
from flask import Flask
from app import db, create_app
from app.models import User, Newrequest, Currentrequest
import json

class AssignControllerTestCase(unittest.TestCase):
    def setUp(self):
        # Create a test Flask app
        self.app = create_app()
        self.client = self.app.test_client()

        # Set up the test database
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_assign_request(self):
        # Create test data in the database (e.g., a new request and a user)
        with self.app.app_context():
            new_request = Newrequest(
                customer_id="12345",
                first_name="John",
                last_name="Doe",
                num_of_children=2,
                outreach_date="2023-10-20"
            )
            user = User(name="Test User", email="test@example.com", role="roleName")
            db.session.add(new_request)
            db.session.add(user)
            db.session.commit()

        # Send a POST request to the assign_request endpoint
        response = self.client.post('/assign_request/1', data={'user_id': 1})

        # Assert the response status code and content
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data['message'], 'Request assigned successfully')

        # Verify the assignment by checking the database
        with self.app.app_context():
            current_request = Currentrequest.query.first()
            self.assertIsNotNone(current_request)
            self.assertEqual(current_request.packet_return_status, "Waiting for Response")
            self.assertEqual(current_request.staff_initials, "")
            self.assertEqual(current_request.decision, "Waiting")
            self.assertIsNone(current_request.num_children_enrolled)
            self.assertIsNone(current_request.decision_date)
            self.assertEqual(current_request.not_enrolled_reason, "")

            # Verify that the new request was deleted
            new_request = Newrequest.query.first()
            self.assertIsNone(new_request)

if __name__ == '__main__':
    unittest.main()
