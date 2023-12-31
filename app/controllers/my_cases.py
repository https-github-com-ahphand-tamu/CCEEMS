from datetime import datetime

from flask import jsonify
from flask import request, Blueprint, render_template
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.fields import DateField

from app import db
from app.decorators.login_decorator import requires_login
from app.models import Case

my_req_bp = Blueprint('my-cases', __name__)


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


@requires_login
@my_req_bp.route('/my_cases', methods=['GET'])
def view_cases():
    cases = current_user.user_cases
    return render_template('my_cases.html', cases=cases, user=current_user)


@requires_login
@my_req_bp.route('/my_cases/edit/', methods=['POST'])
def edit_case():
    data = request.json
    num_children_enrolled = data.get('numChildrenEnrolled')

    print(num_children_enrolled)
    decision_date_str = data.get('decisionDate')
    packet_received_date_str = data.get('packetReceivedDate')
    case_id = data.get('caseId')
    case_to_edit = Case.query.filter_by(id=case_id).first()

    if not case_to_edit:
        return jsonify({"status": "Error", "message": "Case not found"}), 404

    outreach_date = case_to_edit.outreach_date
    if num_children_enrolled != "":
        try:
            int(num_children_enrolled)
        except:
            return jsonify({"status": "Error", "message": "no. of children enrolled must be integer"}), 400
    num_children_enrolled = int(
        num_children_enrolled) if num_children_enrolled != "" else 0

    try:
        decision_date = datetime.strptime(
            decision_date_str, '%Y-%m-%d') if decision_date_str and decision_date_str.lower() != 'none' else None
        packet_received_date = datetime.strptime(
            packet_received_date_str,
            '%Y-%m-%d') if packet_received_date_str and packet_received_date_str.lower() != 'none' else None
    except ValueError as e:
        return jsonify({"status": "Error", "message": "Decision/Package dates must be valid dates"}), 400
    print(decision_date, packet_received_date)
    # Validate that decision and packet_received_date are not before outreach_date
    if decision_date and decision_date.date() < outreach_date:
        return jsonify({"status": "Error", "message": "Decision date cannot be before outreach date"}), 400

    if packet_received_date and packet_received_date.date() < outreach_date:
        return jsonify({"status": "Error", "message": "Packet received date cannot be before outreach date"}), 400

    # Get the case ID from the data
    case_to_edit.packet_return_status = data.get('packetReturnStatus')
    case_to_edit.packet_received_date = data.get('packetReceivedDate')
    case_to_edit.decision = data.get('decision')
    case_to_edit.num_children_enrolled = num_children_enrolled
    case_to_edit.decision_date = decision_date
    case_to_edit.not_enrolled_reason = data.get('notEnrolledReason')

    try:
        db.session.commit()
        return jsonify({"status": "OK"}), 200
    except Exception as e:
        return jsonify({"status": "Error", "message": e}), 400
