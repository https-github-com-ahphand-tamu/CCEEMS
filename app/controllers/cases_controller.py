from flask import Blueprint, request, render_template, jsonify
from flask_login import current_user
from app.models import Case, User, PacketReturnStatus, Decision
from app import db
from datetime import datetime

assign = Blueprint('assign', __name__)

@assign.route('/cases/', methods=['GET'])
def list_cases():
    cases = Case.query.all()
    users = User.query.all()
    return render_template('cases.html', cases=cases, users=users, PacketReturnStatus=PacketReturnStatus, Decision=Decision, currentDate=datetime.now().date())

@assign.route('/case/edit/', methods=['POST'])
def edit_case():
    data = request.json

    num_children_enrolled_str = data.get('numChildrenEnrolled')
    decision_date_str = data.get('decisionDate')
    packet_received_date_str = data.get('packetReceivedDate')

    try:
        num_children_enrolled = int(num_children_enrolled_str) if num_children_enrolled_str else None
    except ValueError as e:
        return jsonify({"status": "Error", "message": "no. of children enrolled must be integer"}), 400

    try:
        decision_date = datetime.strptime(decision_date_str, '%Y-%m-%d' ) if decision_date_str or decision_date_str == 'None' else None
        packet_received_date = datetime.strptime(packet_received_date_str, '%Y-%m-%d') if packet_received_date_str or decision_date_str == 'None' else None
    except (ValueError, TypeError) as _:
        decision_date = None
        packet_received_date = None

    case_id = data.get('caseId')
    case_to_edit = Case.query.filter_by(id=case_id).first()

    if not case_to_edit:
        return jsonify({"status": "Error", "message": "Case not found"}), 404

    isCaseLate = case_to_edit.packet_return_status == PacketReturnStatus.WAITING.name and datetime.now().date() - outreach_date > 15

    if isCaseLate and data.get('packetReturnStatus') != PacketReturnStatus.RETURNED:
        case_to_edit = data.get('packetReturnStatus')
    else:
        outreach_date = case_to_edit.outreach_date
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

@assign.route('/case/assign/', methods=['POST'])
def assign_request():
    user_id = request.form['user_id']
    case_id = int(request.form['case_id']);
    case = Case.query.get(case_id)
    user = User.query.get(int(user_id))
    if case and user:
        if case.packet_return_status != PacketReturnStatus.RETURNED:
            return jsonify({'status': 'error', 'message': "Cannot assign case who\'s package is not received"}), 400
        case.assigned_to_user = user.id
        case.staff_initials = user.name
        try:
            db.session.commit()
            return jsonify({'status': 'error','message': 'Case assigned successfully'}), 200
        except Exception as e:
            return jsonify({'status': 'error','message': 'Error assigning request ' + str(e)}), 500
    return jsonify({'status': 'error','message': 'Invalid Case/User'}), 400
