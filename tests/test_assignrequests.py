import unittest
from flask import Flask
from app import db, create_app
from app.models import User, Newrequest, Currentrequest, PacketReturnStatus, Decision
import json
from app.seeds import roles, users

class AssignControllerTestCase(unittest.TestCase):
    def setUp(self):
        # Create a test Flask app
        self.app = create_app()
        self.client = self.app.test_client()

        # Set up the test database
        with self.app.app_context():
            db.create_all()
            roles.seed()
            users.seed()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_list_new_requests(self):
        # Create test data in the database (e.g., new requests)
        with self.app.app_context():
            new_request_1 = Newrequest(
                customer_id="12345",
                first_name="John",
                last_name="Doe",
                num_of_children=2,
                outreach_date="2023-10-20"
            )
            new_request_2 = Newrequest(
                customer_id="67890",
                first_name="Jane",
                last_name="Smith",
                num_of_children=1,
                outreach_date="2023-10-21"
            )
            db.session.add(new_request_1)
            db.session.add(new_request_2)
            db.session.commit()

        # Send a GET request to the list_new_requests endpoint
        response = self.client.get('/new-requests')

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Assert the presence of data in the response (you may need to customize this based on your template)
        data = response.get_data(as_text=True)
        self.assertIn("John", data)
        self.assertIn("Doe", data)
        self.assertIn("12345", data)  # Check for the customer_id

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
            # user = User(name="Test User", email="test@example.com", role="admin")
            db.session.add(new_request)
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
            print(current_request.packet_return_status)
            self.assertEqual(current_request.packet_return_status, PacketReturnStatus.WAITING)
            self.assertEqual(current_request.staff_initials, "")
            self.assertEqual(current_request.decision, Decision.WAITING)
            self.assertIsNone(current_request.num_children_enrolled)
            self.assertIsNone(current_request.decision_date)
            self.assertEqual(current_request.not_enrolled_reason, "")

            # Verify that the new request was deleted
            new_request = Newrequest.query.first()
            self.assertIsNone(new_request)

if __name__ == '__main__':
    unittest.main()
