from app import db
from flask import Blueprint, render_template, request, jsonify, abort, current_app
from app.models import Currentrequest
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.fields import DateField
from flask import redirect, url_for

# from wtforms.ext.sqlalchemy.fields import QuerySelectField

my_req_bp = Blueprint('my-requests', __name__)

class RequestForm(FlaskForm):
    id = IntegerField('ID')
    customer_id = StringField('Customer ID')
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    num_of_children = IntegerField('Number of Children')
    outreach_date = DateField('Outreach Date')
    packet_return_status = StringField('Packet Return Status')
    packet_received_date = DateField('Packet Received Date')
    staff_initials = StringField('Staff Initials')
    decision = StringField('Decision')
    num_children_enrolled = IntegerField('Number of Children Enrolled')
    decision_date = DateField('Decision Date')
    not_enrolled_reason = StringField('Not Enrolled Reason')
    submit = SubmitField('Save Changes')

@my_req_bp.route('/my-requests', methods=['GET', 'POST'])
def view_requests():
    requests_data = Currentrequest.query.order_by(Currentrequest.id).all()

    forms = []

    for request_data in requests_data:
        form = RequestForm(obj=request_data)
        forms.append((request_data.id, form))

    return render_template('my_requests.html', forms=forms)

@my_req_bp.route('/my-requests/<int:request_id>', methods=['POST'])
def update_request(request_id):
    request_data = Currentrequest.query.get_or_404(request_id)
    form = RequestForm(obj=request_data)

    if form.validate_on_submit():
        form.populate_obj(request_data)
        db.session.commit()
        print(f"Updating request {request_id} with data: {form.data}")

    # Redirect to avoid form resubmission on page refresh
    return redirect(url_for('my-requests.view_requests'))

