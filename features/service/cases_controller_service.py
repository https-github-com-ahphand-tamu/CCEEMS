from app import db
from app.seeds import users, roles
from app.models import Case, PacketReturnStatus, Decision
from datetime import datetime

def setup_feature(context, app):
    with app.app_context():
        app.logger.info("Seeding database in cases controller")
        db.create_all()
        roles.seed()
        users.seed()
        returned_case = Case(
            customer_id='789',
            first_name='Alice',
            last_name='Smith',
            num_of_children=3,
            outreach_date=datetime.now().date(),
            packet_return_status=PacketReturnStatus.RETURNED,
            decision=Decision.WAITING
        )
        waiting_case = Case(
            customer_id='123',
            first_name='Qwedsa',
            last_name='Asdf',
            num_of_children=3,
            outreach_date=datetime.now().date(),
            packet_return_status=PacketReturnStatus.WAITING,
            decision=Decision.WAITING
        )
        db.session.add(returned_case)
        db.session.add(waiting_case)
        db.session.commit()
        context.returned_case_id = returned_case.id
        context.waiting_case_id  = waiting_case.id

def teardown_feature(context, app):
    with app.app_context():
        app.logger.info("Dropping all tables in cases controller")
        db.drop_all()