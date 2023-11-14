import unittest
from flask import Flask
from app import db, create_app
from app.models import PacketReturnStatus, Decision, Case
from app.seeds import roles, users

class CaseControllerTestCase(unittest.TestCase):
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

    def test_list_cases(self):
        # Add some test data
        with self.app.app_context():
            response = self.client.get('/cases/')
            self.assertEqual(response.status_code, 200)
    
    def test_invalid_num_children_enrolled(self):
        # Add some test data
        with self.app.app_context():
            test_case = Case(
                customer_id='123',
                first_name='John',
                last_name='Doe',
                num_of_children=2,
                outreach_date='2023-01-01',
                packet_return_status=PacketReturnStatus.WAITING,
                decision=Decision.WAITING
            )
            db.session.add(test_case)
            db.session.commit()

            # Test: Edit case with invalid numChildrenEnrolled
            invalid_num_children_data = {
                'caseId': test_case.id,
                'numChildrenEnrolled': 'invalid',
                'decisionDate': '2023-01-10',
                'packetReceivedDate': '2023-01-15',
                'packetReturnStatus': PacketReturnStatus.RETURNED.name,
                'decision': Decision.ENROLLED.name,
                'notEnrolledReason': None
            }
            response = self.client.post('/case/edit/', json=invalid_num_children_data, content_type='application/json')
            self.assertEqual(response.status_code, 400)
            self.assertIn('no. of children enrolled must be integer', response.json['message'])

    def test_case_not_found(self):
        # Test: Edit case with non-existent caseId
        non_existent_case_data = {
            'caseId': 9999,  # Assuming this ID does not exist
            'numChildrenEnrolled': 3,
            'decisionDate': '2023-01-10',
            'packetReceivedDate': '2023-01-15',
            'packetReturnStatus': PacketReturnStatus.RETURNED.name,
            'decision': Decision.ENROLLED.name,
            'notEnrolledReason': None
        }
        response = self.client.post('/case/edit/', json=non_existent_case_data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Case not found', response.json['message'])

    def test_decision_date_before_outreach_date(self):
        # Add some test data
        with self.app.app_context():
            test_case = Case(
                customer_id='123',
                first_name='John',
                last_name='Doe',
                num_of_children=2,
                outreach_date='2023-01-01',
                packet_return_status=PacketReturnStatus.WAITING,
                decision=Decision.WAITING
            )
            db.session.add(test_case)
            db.session.commit()

            # Test: Edit case with decision date before outreach date
            invalid_decision_date_data = {
                'caseId': test_case.id,
                'numChildrenEnrolled': 3,
                'decisionDate': '2022-12-25',  # Assuming this date is before outreach_date
                'packetReceivedDate': '2023-01-15',
                'packetReturnStatus': PacketReturnStatus.RETURNED.name,
                'decision': Decision.ENROLLED.name,
                'notEnrolledReason': None
            }
            response = self.client.post('/case/edit/', json=invalid_decision_date_data, content_type='application/json')
            self.assertEqual(response.status_code, 400)
            self.assertIn('Decision date cannot be before outreach date', response.json['message'])

if __name__ == '__main__':
    unittest.main()
