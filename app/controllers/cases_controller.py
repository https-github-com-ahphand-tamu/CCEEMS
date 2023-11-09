from flask import Blueprint, request, render_template, jsonify
from flask_login import current_user
from app.models import Case, User, PacketReturnStatus, Decision
from app import db
import logging

assign = Blueprint('assign', __name__)


@assign.route('/cases', methods=['GET'])
def list_new_requests():
    # Query the new requests from the database, limiting to 50 per page
    cases = Case.query.all()
    users = User.query.all()
    print(users)
    return render_template('cases.html', cases=cases, users=users)


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
