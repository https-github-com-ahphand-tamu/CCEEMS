from flask import Blueprint, request, render_template, jsonify
from flask_login import current_user
from app.models import Case, User, PacketReturnStatus, Decision
from app import db
from datetime import datetime
import logging

assign = Blueprint('assign', __name__)


@assign.route('/cases/', methods=['GET'])
def list_cases():
    cases = Case.query.all()
    users = User.query.all()
    return render_template('cases.html', user=current_user, cases=cases, users=users, PacketReturnStatus=PacketReturnStatus, Decision=Decision, currentDate=datetime.now().date())


@assign.route('/case/edit/', methods=['POST'])
def edit_case():
    data = request.json
    num_children_enrolled = data.get('numChildrenEnrolled')
    decision_date_str = data.get('decisionDate')
    packet_received_date_str = data.get('packetReceivedDate')
    case_id = data.get('caseId')
    case_to_edit = Case.query.filter_by(id=case_id).first()

    if not case_to_edit:
        return jsonify({"status": "Error", "message": "Case not found"}), 404

    outreach_date = case_to_edit.outreach_date
    isCaseLate = case_to_edit.packet_return_status == PacketReturnStatus.WAITING and (
        datetime.now().date() - outreach_date).days > 15

    if isCaseLate:
        if data.get('packetReturnStatus') != PacketReturnStatus.RETURNED.name:
            case_to_edit.packet_return_status = data.get('packetReturnStatus')
        else:
            return jsonify({"status": "Error", "message": "Late case package status can\'t be made returned"}), 400
    else:
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
                packet_received_date_str, '%Y-%m-%d') if packet_received_date_str and packet_received_date_str.lower() != 'none' else None
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


@assign.route('/case/assign/', methods=['POST'])
def assign_request():
    try:
        data = request.json
        user_id = data.get('user_id')
        case_id = data.get('case_id')
        logging.info(f"ASSIGN={data}, user_id={user_id}, case_id={case_id}")
        case = Case.query.get(int(case_id))
        user = User.query.get(int(user_id))
        logging.info(f"ASSIGN={data}, case={case}, user={user}")

        if case and user:
            if case.packet_return_status != PacketReturnStatus.RETURNED:
                return jsonify({'status': 'error', 'message': "Cannot assign case who\'s package is not received"}), 400
            case.assigned_to_user = user.id
            case.staff_initials = user.name
            try:
                db.session.commit()
                return jsonify({'status': 'error', 'message': 'Case assigned successfully'}), 200
            except Exception as e:
                return jsonify({'status': 'error', 'message': 'Error assigning case', 'exception': str(e)}), 500
        return jsonify({'status': 'error', 'message': 'Invalid Case/User'}), 400
    except:
        return jsonify({'status': "error", "message": "user_id/case_id should be numbers in payload"}), 400
