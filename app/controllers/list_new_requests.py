from flask import Blueprint, current_app
from app.models import Newrequest, Currentrequest
from app import db

assign = Blueprint('assign', __name__)

from flask import render_template, request

@assign.route('/new-requests', methods=['GET'])
def list_new_requests():
    # Query the new requests from the database, limiting to 50 per page
    # page = request.args.get('page', 1, type=int)
    # per_page = 50
    # new_requests = Newrequest.query.paginate(page, per_page, error_out=False)
    new_requests = Newrequest.query.all()
    current_app.logger.info(new_requests)
    print(new_requests)
    return render_template('new-requests.html', new_requests=new_requests)

@assign.route('/assign_request/<int:request_id>', methods=['POST'])
def assign_request(request_id):
    # Get the user ID and other assignment details from the form
    user_id = request.form['user_id']
    # Add more assignment logic here

    # Move the request from new_requests to current_requests
    new_request = Newrequest.query.get(request_id)
    if new_request:
        current_request = Currentrequest(
            customer_id=new_request.customer_id,
            first_name=new_request.first_name,
            last_name=new_request.last_name,
        )
        db.session.add(current_request)
        db.session.delete(new_request)
        db.session.commit()