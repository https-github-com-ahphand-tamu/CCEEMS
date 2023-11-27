from flask import render_template, redirect
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
import logging
from app import create_app, db
from app.models import User, Case
from sqlalchemy import create_engine, text

from config import getUri

import os

app = create_app()
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view = "/user/login"
login_manager.init_app(app)

logging.basicConfig(level=logging.DEBUG)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    if current_user.is_authenticated:
        month_data = [0] * 12
        return_status_data = [0] * 3
        children_enrolled_data = [0] * 12
        children_not_enrolled_data = [0] * 12
        not_enrolled_reasons_count = [0] * 15
        not_enrolled_reasons = ["Does not meet employment/activity requirement", "Fee too high", "No Child Care Slots",
                                "No longer in Dallas County", "No longer needing services", "No packet received",
                                "No Provider Choice", "Not a Priority", "Not working/training", "On leave/STD",
                                "Over the income guidelines", "Unable to Reach Client", "Under participation requirement",
                                "Verification Docs Needed", "Other"
                                ]
        not_enrolled_reasons_dict = dict(
            map(lambda i, j: (i, j), not_enrolled_reasons, not_enrolled_reasons_count))
        processing_time = [0] * 5

        query_for_sent_packets = """
        select extract(month from outreach_date) as month, count(id) from cases group by month;
        """

        quey_for_packet_return_status = """
         select count(id) from cases group by packet_return_status order by packet_return_status asc;
        """

        query_for_children_enrolled = """
         select extract(month from outreach_date) as month, sum(num_children_enrolled) from cases group by month;
        """

        query_for_children_not_enrolled = """
         select extract(month from outreach_date) as month, sum(num_of_children)-sum(num_children_enrolled) from cases group by month;
        """

        query_for_not_enrolled_reason = """
         select not_enrolled_reason, count(id) from cases group by not_enrolled_reason having not_enrolled_reason <> '' order by not_enrolled_reason asc;
        """

        query_for_processing_time = """
         select CASE
                WHEN decision_date - outreach_date > 0 AND decision_date - outreach_date < 10 THEN 1
                WHEN decision_date - outreach_date > 10 AND decision_date - outreach_date < 20 THEN 2
                WHEN decision_date - outreach_date > 20 AND decision_date - outreach_date < 30 THEN 3
                WHEN decision_date - outreach_date > 30 THEN 4
                WHEN decision_date - outreach_date is NULL THEN 5
                END Processing_Time, count(id) from cases group by Processing_Time order by processing_time asc
                ;
        """
        
        with db.engine.connect() as connection:
            result_sent_packets = connection.execute(
                text(query_for_sent_packets))
            for row in result_sent_packets:
                month_data[int(row[0]) - 1] = row[1]

            result_packet_return_status = connection.execute(
                text(quey_for_packet_return_status))

            i = 0
            for row in result_packet_return_status:
                return_status_data[i] = row[0]
                i += 1

            result_children_enrolled = connection.execute(
                text(query_for_children_enrolled))
            for row in result_children_enrolled:
                children_enrolled_data[int(row[0]) - 1] = row[1]

            result_children_not_enrolled = connection.execute(
                text(query_for_children_not_enrolled))
            for row in result_children_not_enrolled:
                children_not_enrolled_data[int(row[0]) - 1] = row[1]

            result_not_enrolled_reason = connection.execute(
                text(query_for_not_enrolled_reason))
            for row in result_not_enrolled_reason:
                not_enrolled_reasons_dict[str(row[0])] = row[1]

            result_processing_time = connection.execute(
                text(query_for_processing_time))
            for row in result_processing_time:
                processing_time[int(row[0]) - 1] = row[1]

        return render_template('home.html', user=current_user, sent_data=month_data,
                               returned_data=return_status_data, children_enrolled=children_enrolled_data,
                               children_not_enrolled=children_not_enrolled_data, not_enrolled_reasons=list(
                                   not_enrolled_reasons_dict.values()),
                               processing_time=processing_time)
    else:
        return redirect('/user/login')


if __name__ == '__main__':
    app.run(debug=True)
