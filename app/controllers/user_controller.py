import logging
import re
from datetime import datetime

from flask import Blueprint, redirect, request, jsonify, render_template
from werkzeug.security import check_password_hash

from app import db
from app.exceptions.validation import ValidationException
from app.models import User, Role

user_bp = Blueprint('user', __name__)


@user_bp.route('/users/login', methods=['POST'])
def login_auth():
    if request.method == 'POST':
        emailid = request.form['email']
        user_password = request.form['password']
        user = User.query.filter_by(email=emailid).first()
        if check_password_hash(user.password, user_password):
            return redirect('/index')
        else:
            return render_template('Login.html', incorrect_password=True)


@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_data = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role
        }
        user_list.append(user_data)

    logging.debug(user_list)
    return render_template('users.html', users=user_list)


@user_bp.route('/users/<int:user_id>', methods=['GET'])
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


@user_bp.route('/users', methods=['POST'])
def add_user():
    try:
        data = request.get_json()
        logging.debug(f"POST to /users: {data}")

        validate_user_payload(data)
        email = validate_user_email(data["email"])
        role = validate_role(data["role"])

        user_exists = db.session.query(User).filter(User.email == email).first()
        if user_exists:
            return jsonify({'message': f'User already exists with email: {data["email"]}'}), 400

        new_user = User(name=data.get('name'), email=email, role=role)
        new_user.created_on = datetime.utcnow()

        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'User added successfully'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Failed to add user', 'error': str(e)}), 500
        finally:
            db.session.close()
    except ValidationException as ve:
        return jsonify({'message': str(ve)}), ve.status_code


@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.get_json()
        logging.debug(f"PUT to /users with user id: {user_id} and data: {data}")

        validate_user_payload(data)
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


@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = db.session.get(User, user_id)

    if user is None:
        return jsonify({'message': 'User not found'}), 404

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to delete user', 'error': str(e)}), 500
    finally:
        db.session.close()


def validate_user_payload(data):
    if 'name' not in data or 'email' not in data or 'role' not in data:
        raise ValidationException('Missing required fields (name, email, role)', 400)


def validate_role(role_name):
    role = Role.query.filter_by(name=role_name).first()
    if not role:
        message = f"Role '{role_name}' does not exist"
        logging.info(message)
        raise ValidationException(message, 400)
    return role


def validate_user_email(email):
    sanitized_email = sanitize_email(email)
    if not is_valid_email(sanitized_email):
        raise ValidationException(f'Invalid email address: {sanitized_email}', 400)
    return sanitized_email


def sanitize_email(email):
    sanitized_email = email.strip()
    return sanitized_email


def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+$'
    return bool(re.match(pattern, email))
