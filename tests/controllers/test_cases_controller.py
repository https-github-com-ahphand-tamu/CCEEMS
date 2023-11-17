import unittest
from app import db, create_app
from app.models import PacketReturnStatus, Decision, Case
from app.seeds import roles, users
from datetime import datetime, timedelta

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
                outreach_date=datetime.now().date(),
                packet_return_status=PacketReturnStatus.WAITING,
                decision=Decision.WAITING
            )
            db.session.add(test_case)
            db.session.commit()

            # Test: Edit case with invalid numChildrenEnrolled
            invalid_num_children_data = {
                'caseId': test_case.id,
                'numChildrenEnrolled': 'invalid',
                'decisionDate': str(datetime.now().date() + timedelta(5)),
                'packetReceivedDate': str(datetime.now().date() - timedelta(5)),
                'packetReturnStatus': PacketReturnStatus.WAITING.name,
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

    def test_decision_and_package_date_before_outreach_date(self):
        with self.app.app_context():
            test_case = Case(
                customer_id='123',
                first_name='John',
                last_name='Doe',
                num_of_children=2,
                outreach_date=datetime.now().date(),
                packet_return_status=PacketReturnStatus.WAITING,
                decision=Decision.WAITING
            )
            db.session.add(test_case)
            db.session.commit()

            # Test: Edit case with decision date before outreach date
            invalid_decision_date_data = {
                'caseId': test_case.id,
                'numChildrenEnrolled': 3,
                'decisionDate': str(datetime.now().date() - timedelta(5)),
                'packetReceivedDate': '2023-01-15',
                'packetReturnStatus': PacketReturnStatus.RETURNED.name,
                'decision': Decision.ENROLLED.name,
                'notEnrolledReason': None
            }
            response = self.client.post('/case/edit/', json=invalid_decision_date_data, content_type='application/json')
            self.assertEqual(response.status_code, 400)
            self.assertIn('Decision date cannot be before outreach date', response.json['message'])
            
            invalid_decision_date_data = {
                'caseId': test_case.id,
                'numChildrenEnrolled': 3,
                'decisionDate': str(datetime.now().date() + timedelta(5)),
                'packetReceivedDate': str(datetime.now().date() - timedelta(5)),
                'packetReturnStatus': PacketReturnStatus.RETURNED.name,
                'decision': Decision.ENROLLED.name,
                'notEnrolledReason': None
            }
            response = self.client.post('/case/edit/', json=invalid_decision_date_data, content_type='application/json')
            self.assertEqual(response.status_code, 400)
            self.assertIn('Packet received date cannot be before outreach date', response.json['message'])

    def test_late_case(self):
        with self.app.app_context():
            # Assuming a case with outreach date more than 15 days ago
            late_case = Case(
                customer_id='456',
                first_name='Jane',
                last_name='Doe',
                num_of_children=1,
                outreach_date=datetime.now().date() - timedelta(days=20),
                packet_return_status=PacketReturnStatus.WAITING,
                decision=Decision.WAITING
            )
            db.session.add(late_case)
            db.session.commit()

            # Test: Attempt to edit a late case to packetReturnStatus to RETURNED
            invalid_late_case_data = {
                'caseId': late_case.id,
                'numChildrenEnrolled': 1,
                'decisionDate': str(datetime.now().date() - timedelta(days=5)),
                'packetReceivedDate': '2023-01-15',
                'packetReturnStatus': PacketReturnStatus.RETURNED.name,
                'decision': Decision.ENROLLED.name,
                'notEnrolledReason': None
            }
            response = self.client.post('/case/edit/', json=invalid_late_case_data, content_type='application/json')
            self.assertEqual(response.status_code, 400)
            self.assertIn("Late case package status can't be made returned", response.json['message'])

    def test_assign_case_before_returned(self):
        with self.app.app_context():
            case_to_assign = Case(
                customer_id='789',
                first_name='Alice',
                last_name='Smith',
                num_of_children=3,
                outreach_date=datetime.now().date(),
                packet_return_status=PacketReturnStatus.WAITING,
                decision=Decision.WAITING
            )
            db.session.add(case_to_assign)
            db.session.commit()

            # Test: Attempt to assign a case to a user before packagereturnstatus is set to RETURNED
            invalid_assign_case_data = {
                'case_id': case_to_assign.id,
                'user_id': 1  # Assuming user ID 1
            }
            response = self.client.post('/case/assign/', json=invalid_assign_case_data, content_type='application/json')
            self.assertEqual(response.status_code, 400)
            self.assertIn("Cannot assign case who\'s package is not received", response.json['message'])
    
    def test_assign_user_happy_path(self):
        with self.app.app_context():
            # Add a test case
            test_case = Case(
                customer_id='123',
                first_name='John',
                last_name='Doe',
                num_of_children=2,
                outreach_date=datetime.now().date(),
                packet_return_status=PacketReturnStatus.RETURNED,
                decision=Decision.ENROLLED
            )
            db.session.add(test_case)
            db.session.commit()

            # Assign the case to the user
            assign_data = {
                'case_id': test_case.id,
                'user_id': 1
            }
            response = self.client.post('/case/assign/', json=assign_data, content_type='application/json')
            self.assertEqual(response.status_code, 200)

            # Query the database to check if the assignment is correct
            assigned_case = Case.query.filter_by(id=test_case.id).first()
            self.assertIsNotNone(assigned_case)
            self.assertEqual(assigned_case.assigned_to_user, 1)
    
    def test_edit_case_happy_path(self):
        with self.app.app_context():
            # Add a test case
            test_case = Case(
                customer_id='123',
                first_name='John',
                last_name='Doe',
                num_of_children=2,
                outreach_date=datetime.now().date(),
                packet_return_status=PacketReturnStatus.WAITING,
                decision=Decision.WAITING
            )
            db.session.add(test_case)
            db.session.commit()

            # Edit the test case
            edit_data = {
                'caseId': test_case.id,
                'numChildrenEnrolled': 3,
                'decisionDate': str(datetime.now().date() + timedelta(5)),
                'packetReceivedDate': str(datetime.now().date() + timedelta(10)),
                'packetReturnStatus': PacketReturnStatus.RETURNED.name,
                'decision': Decision.ENROLLED.name,
                'notEnrolledReason': 'Not interested'
            }
            response = self.client.post('/case/edit/', json=edit_data, content_type='application/json')
            self.assertEqual(response.status_code, 200)

            # Query the database to check if the case details are edited and saved correctly
            edited_case = Case.query.filter_by(id=test_case.id).first()
            self.assertIsNotNone(edited_case)
            self.assertEqual(edited_case.num_children_enrolled, 3)
            self.assertEqual(str(edited_case.decision_date), edit_data['decisionDate'])
            self.assertEqual(str(edited_case.packet_received_date), edit_data['packetReceivedDate'])
            self.assertEqual(edited_case.packet_return_status, PacketReturnStatus.RETURNED)
            self.assertEqual(edited_case.decision, Decision.ENROLLED)
            self.assertEqual(edited_case.not_enrolled_reason, 'Not interested')

    def test_invalid_dates(self):
        with self.app.app_context():
            # Add a test case
            test_case = Case(
                customer_id='123',
                first_name='John',
                last_name='Doe',
                num_of_children=10,
                outreach_date=datetime.now().date(),
                packet_return_status=PacketReturnStatus.WAITING,
                decision=Decision.WAITING,
                num_children_enrolled=2
            )
            db.session.add(test_case)
            db.session.commit()

            # Test: Attempt to edit case with invalid package/decision dates
            invalid_dates_data = {
                'caseId': test_case.id,
                'numChildrenEnrolled': '3',
                'decisionDate': 'invalid_date',
                'packetReceivedDate': 'invalid_date',
                'packetReturnStatus': PacketReturnStatus.RETURNED.name,
                'decision': Decision.ENROLLED.name,
                'notEnrolledReason': 'Not interested'
            }
            response = self.client.post('/case/edit/', json=invalid_dates_data, content_type='application/json')
            self.assertEqual(response.status_code, 400)
            self.assertIn("Decision/Package dates must be valid dates", response.json['message'])
            
            # Query the database to check if the case details remain unchanged
            unchanged_case = Case.query.filter_by(id=test_case.id).first()
            self.assertIsNotNone(unchanged_case)
            self.assertEqual(unchanged_case.num_children_enrolled, 2)
            self.assertEqual(unchanged_case.packet_return_status, PacketReturnStatus.WAITING)
            self.assertEqual(unchanged_case.decision, Decision.WAITING)
            self.assertIsNone(unchanged_case.not_enrolled_reason)

    def test_assign_user_invalid_payload(self):
        with self.app.app_context():
            # Add a test case
            test_case = Case(
                customer_id='123',
                first_name='John',
                last_name='Doe',
                num_of_children=2,
                outreach_date=datetime.now().date(),
                packet_return_status=PacketReturnStatus.WAITING,
                decision=Decision.WAITING
            )
            db.session.add(test_case)
            db.session.commit()

            # Test 1: Attempt to assign without caseId or assignedToUser in the payload
            invalid_payload_data = {}
            response = self.client.post('/case/assign/', json=invalid_payload_data, content_type='application/json')
            self.assertEqual(response.status_code, 400)
            self.assertIn("user_id/case_id should be numbers in payload", response.json['message'])

            # Test 2: Attempt to assign with invalid caseId or assignedToUser in the payload
            invalid_data = {
                'case_id': 999,
                'user_id': 999
            }
            response = self.client.post('/case/assign/', json=invalid_data, content_type='application/json')
            self.assertEqual(response.status_code, 400)
            self.assertIn("Invalid Case/User", response.json['message'])

            # Query the database to ensure the case is not assigned
            unassigned_case = Case.query.filter_by(id=test_case.id).first()
            self.assertIsNotNone(unassigned_case)
            self.assertIsNone(unassigned_case.assigned_to_user)

if __name__ == '__main__':
    unittest.main()