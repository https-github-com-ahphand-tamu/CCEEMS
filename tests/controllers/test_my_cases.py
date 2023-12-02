import unittest
from datetime import datetime
from main import app, db
from app.models import User, Role, Case, PacketReturnStatus, Decision

from werkzeug.security import generate_password_hash


class TestMyCasesRoutes(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True
        self.app_context = app.app_context()
        self.app_context.push()

        db.create_all()

        admin_role = Role(name='Admin')
        db.session.add(admin_role)
        db.session.commit()

        admin_user = User(name='Admin User',
                          email='admin@example.com', role=admin_role)
        admin_user.password = generate_password_hash("admin123")
        db.session.add(admin_user)

        test_case = Case(
            customer_id='123',
            first_name='John',
            last_name='Doe',
            num_of_children=2,
            outreach_date=datetime.now()
        )
        db.session.add(test_case)

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

    def test_view_cases(self):
        response = self.client.get('/my_cases')
        self.assertEqual(response.status_code, 200)

    # def test_view_cases_unauthorized(self):
    #     # Logout to simulate unauthorized access
    #     self.client.get('/user/logout')
    #     response = self.client.get('/my_cases')
    #     self.assertEqual(response.status_code, 302)

    def test_edit_case(self):
        # Create a test case for the user
        test_case = Case(customer_id='234', first_name='John', last_name='Doe',
                         num_of_children=2, outreach_date=datetime(1995, 1, 2))
        db.session.add(test_case)
        db.session.commit()

        response = self.client.post('/my_cases/edit/', json={
            'caseId': test_case.id,
            'numChildrenEnrolled': 2,
            'decisionDate': '2023-01-01',
            'packetReceivedDate': '2023-01-02',
            'packetReturnStatus': PacketReturnStatus.RETURNED.name,
            'decision': Decision.ENROLLED.name,
            'notEnrolledReason': 'Not interested'
        })
        self.assertEqual(response.status_code, 200)

        updated_case = Case.query.get(test_case.id)
        self.assertEqual(updated_case.num_children_enrolled, 2)
        self.assertEqual(updated_case.decision_date,
                         datetime(2023, 1, 1).date())
        self.assertEqual(updated_case.packet_received_date,
                         datetime(2023, 1, 2).date())
        self.assertEqual(updated_case.packet_return_status,
                         PacketReturnStatus.RETURNED)
        self.assertEqual(updated_case.decision, Decision.ENROLLED)
        self.assertEqual(updated_case.not_enrolled_reason, 'Not interested')

    def test_edit_case_invalid_data(self):
        response = self.client.post('/my_cases/edit/', json={
            'caseId': 999,
            'numChildrenEnrolled': 'invalid',
            'decisionDate': 'invalid-date',
            'packetReceivedDate': 'invalid-date',
            'packetReturnStatus': PacketReturnStatus.RETURNED.name,
            'decision': Decision.ENROLLED.name,
            'notEnrolledReason': 'Not interested'
        })
        self.assertEqual(response.status_code, 404)  # Case not found

    def test_edit_case_validation_error(self):
        test_case = Case(customer_id='345', first_name='John', last_name='Doe',
                         num_of_children=2, outreach_date=datetime(1995, 1, 2))
        db.session.add(test_case)
        db.session.commit()

        response = self.client.post('/my_cases/edit/', json={
            'caseId': test_case.id,
            'numChildrenEnrolled': 'invalid',
            'decisionDate': 'invalid-date',
            'packetReceivedDate': 'invalid-date',
            'packetReturnStatus': PacketReturnStatus.RETURNED.name,
            'decision': Decision.ENROLLED.name,
            'notEnrolledReason': 'Not interested'
        })
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
