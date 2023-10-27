from flask import Blueprint, redirect, request, jsonify, render_template, current_app
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash

from app import db
from app.decorators.login_decorator import requires_login
from app.exceptions.validation import ValidationException
from app.helpers.user_helpers import validate_add_user_payload, validate_user_email, validate_role
from app.models import User

user_bp = Blueprint('user', __name__)


@user_bp.route('/user/login', methods=['POST'])
def login_auth():
    data = request.form
    if 'email' not in data or 'password' not in data:
        return jsonify({'message': 'Missing required fields (email, password)'}), 400
    email_id = data["email"]
    user_password = data['password']
    user = User.query.filter_by(email=email_id).first()
    if not user:
        current_app.logger.error(f"User with email {email_id} does not exists")
        return render_template('Login.html', incorrect_password=True)
    elif check_password_hash(user.password, user_password):
        login_user(user)
        current_app.logger.info(f"User with email: {email_id} and role: {user.role.name} is successfully logged in!")
        current_app.logger.debug(f"Current user: {current_user}")
        return redirect('/index')
    else:
        current_app.logger.error(f"Invalid credentials for user: {email_id}")
        return render_template('Login.html', incorrect_password=True)


@user_bp.route('/user/logout', methods=['POST'])
@requires_login
def logout():
    current_app.logger.info(f"Logging out user: {current_user.email}")
    logout_user()
    return


@user_bp.route('/user/<int:user_id>', methods=['GET'])
@requires_login
def get_user_by_id(user_id):
    user = db.session.get(User, user_id)

    if user is None:
        return jsonify({'message': 'User not found'}), 404

    user_data = {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'role': user.role.name if user.role else None
    }

    return jsonify(user_data), 200


@user_bp.route('/user/<int:user_id>', methods=['PUT'])
@requires_login
def update_user(user_id):
    try:
        data = request.get_json()
        current_app.logger.debug(
            f"PUT to /users with user id: {user_id} and data: {data}")

        validate_add_user_payload(data)
        email = validate_user_email(data["email"])
        role = validate_role(data["role"])

        user = db.session.get(User, user_id)
        if user is None:
            return jsonify({'message': 'User not found'}), 404

        user.name = data.get('name')
        user.email = email
        user.role = role

        try:
            db.session.commit()
            return jsonify({'message': 'User updated successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Failed to update user', 'error': str(e)}), 500
        finally:
            db.session.close()
    except ValidationException as ve:
        return jsonify({'message': str(ve)}), ve.status_code
