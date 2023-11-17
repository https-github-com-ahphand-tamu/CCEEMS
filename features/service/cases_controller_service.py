from app import db
from app.seeds import users, roles


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
        context.returned_case = returned_case
        context.waiting_case = waiting_case
        db.session.commit()

def teardown_feature(context, app):
    with app.app_context():
        app.logger.info("Dropping all tables in cases controller")
        db.drop_all()