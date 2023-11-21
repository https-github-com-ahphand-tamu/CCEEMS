from werkzeug.security import generate_password_hash

from app import db
from app.models import User, Role, Case
import logging


def seed():
    # admin_role = Role.query.filter_by(name="Admin").first()
    # logging.info("ADMIN ROLE: " + str(admin_role))
    # user1 = User(name='Test1', email="test1@tamu.edu", role=admin_role)
    # user1.password = generate_password_hash("Password@123")
    # db.session.add(user1)
    # db.session.commit()

    # eligibility_supervisor_role = Role.query.filter_by(
    #     name="Eligibility Supervisor").first()
    # user2 = User(name='Test2', email="test2@tamu.edu",
    #              role=eligibility_supervisor_role)
    # user2.password = generate_password_hash("Password@456")
    # db.session.add(user2)
    # db.session.commit()

    my_case_1 = Case(customer_id="111111",first_name="Atharva",last_name="Phand",num_of_children=3,outreach_date="2023-11-11")
    my_case_2 = Case(customer_id="111221",first_name="Ath",last_name="Phan",num_of_children=3,outreach_date="2023-11-12")
    my_case_3 = Case(customer_id="33331",first_name="Arva",last_name="Phad",num_of_children=3,outreach_date="2023-11-13")
    my_case_4 = Case(customer_id="444411",first_name="Aa",last_name="Phnd",num_of_children=3,outreach_date="2023-11-14")
    my_case_5 = Case(customer_id="555511",first_name="Arva",last_name="Pand",num_of_children=3,outreach_date="2023-11-15")
    my_case_6 = Case(customer_id="6755511",first_name="harva",last_name="hand",num_of_children=3,outreach_date="2023-11-16")
    db.session.add(my_case_1)
    db.session.add(my_case_2)
    db.session.add(my_case_3)
    db.session.add(my_case_4)
    db.session.add(my_case_5)
    db.session.add(my_case_6)
    db.session.commit()

    logging.info("Users seeded")
