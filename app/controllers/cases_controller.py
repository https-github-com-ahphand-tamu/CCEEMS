from flask import Blueprint, request, render_template, jsonify
from flask_login import current_user
from app.models import Case, User, PacketReturnStatus, Decision
from app import db
from datetime import datetime

assign = Blueprint('assign', __name__)


@assign.route('/cases', methods=['GET'])
def list_new_requests():
    # Query the new requests from the database, limiting to 50 per page
    cases = Case.query.all()
    users = User.query.all()
    return render_template('cases.html', cases=cases, users=users, PacketReturnStatus=PacketReturnStatus, Decision=Decision, currentDate=datetime.now().date())

@assign.route('/case/edit', methods=['POST'])
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

@assign.route('/assign_request/<int:request_id>', methods=['POST'])
def assign_request(request_id):
    user_id = request.form['user_id']
    case = Case.query.get(request_id)
    if case and User.query.get(user_id):
        try:
            case.assigned_to_user = int(user_id)
            db.session.commit()
            return jsonify({'message': 'Request assigned successfully'})
        except:
            # Return an error response with an appropriate status code
            return jsonify({'error': 'Error assigning request'}), 500
    return jsonify({'message': 'Invalid Case/User' + str(request_id)}), 400
