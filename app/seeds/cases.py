from app import db
from app.models import Case
import logging


def seed():
    my_case_1 = Case(customer_id="1", first_name="Tanmai", last_name="Harish", num_of_children=3,
                     outreach_date="2023-11-11")
    my_case_2 = Case(customer_id="2", first_name="John", last_name="Jonhnson", num_of_children=2,
                     outreach_date="2023-11-12")
    my_case_3 = Case(customer_id="3", first_name="Great", last_name="Khali", num_of_children=1,
                     outreach_date="2023-11-13")
    my_case_4 = Case(customer_id="4", first_name="Daehee", last_name="Han", num_of_children=4,
                     outreach_date="2023-11-14")
    my_case_5 = Case(customer_id="5", first_name="Ravi", last_name="Ashwin", num_of_children=5,
                     outreach_date="2023-11-15")
    my_case_6 = Case(customer_id="6", first_name="Rajesh", last_name="Jadhav", num_of_children=3,
                     outreach_date="2023-11-16")
    db.session.add(my_case_1)
    db.session.add(my_case_2)
    db.session.add(my_case_3)
    db.session.add(my_case_4)
    db.session.add(my_case_5)
    db.session.add(my_case_6)
    db.session.commit()

    logging.info("Cases seeded")
