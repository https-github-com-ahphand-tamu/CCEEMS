from flask import Blueprint, request, render_template, jsonify
from flask_login import current_user
from app.models import Case, User, PacketReturnStatus, Decision
from app import db
import logging

assign = Blueprint('assign', __name__)


@assign.route('/cases', methods=['GET'])
def list_new_requests():
    # Query the new requests from the database, limiting to 50 per page
    new_requests = Case.query.all()
    users = User.query.all()
    logging.info("USERS: ", users)
    return render_template('new-requests-page.html', new_requests=new_requests, user=current_user)


@assign.route('/assign_request/<int:request_id>', methods=['POST'])
def assign_request(request_id):
    # Get the user ID and other assignment details from the form
    user_id = request.form['user_id']
    # Move the request from new_requests to current_requests
    new_request = Case.query.get(request_id)
    if new_request:
        current_request = Case(
            customer_id=new_request.customer_id,
            first_name=new_request.first_name,
            last_name=new_request.last_name,
            num_of_children=new_request.num_of_children,
            outreach_date=new_request.outreach_date,
            packet_return_status=PacketReturnStatus.WAITING,  # Set an initial status
            packet_received_date=None,  # Set to None as it may be updated later
            staff_initials="",  # Set to an appropriate value
            decision=Decision.WAITING,  # Set an initial decision status
            num_children_enrolled=None,  # Set to None initially
            decision_date=None,  # Set to None initially
            not_enrolled_reason=""  # Set to an appropriate value
        )

        try:
            db.session.add(current_request)
            db.session.delete(new_request)
            db.session.commit()
            return jsonify({'message': 'Request assigned successfully'})
        except:
            # Return an error response with an appropriate status code
            return jsonify({'error': 'Error assigning request'}), 500
    return jsonify({'message': 'No new request found with id: ' + str(request_id)})
