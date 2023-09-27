import logging
import re

from datetime import datetime
from flask import Blueprint, request, jsonify, render_template

from app import db
from app.models import User, Role

user_bp = Blueprint('user', __name__)


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
    user = User.query.get(user_id)

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
    data = request.get_json()
    logging.debug(f"POST to /users: {data}")

    if 'name' not in data or 'email' not in data or 'role' not in data:
        return jsonify({'message': 'Missing required fields (name, email, role)'}), 400

    email = sanitize_email(data['email'])
    if not is_valid_email(email):
        return jsonify({'message': f'Invalid email address: {data["email"]}'}), 400

    # Check if the role already exists in the database
    role_name = data.get('role')
    role = Role.query.filter_by(name=role_name).first()
    if not role:
        message = f"Role '{role_name}' does not exist"
        logging.info(message)
        return jsonify({'message': message}), 400

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


@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    logging.debug(f"PUT to /users with user id: {user_id} and data: {data}")

    if 'name' not in data or 'email' not in data or 'role' not in data:
        return jsonify({'message': 'Missing required fields (name, email, role)'}), 400

    email = sanitize_email(data['email'])
    if not is_valid_email(email):
        return jsonify({'message': f'Invalid email address: {data["email"]}'}), 400

    user = User.query.get(user_id)
    if user is None:
        return jsonify({'message': 'User not found'}), 404

    user.name = data.get('name')
    user.email = email
    role_name = data.get('role')
    if role_name:
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            message = f"Role '{role_name}' does not exist"
            logging.info(message)
            return jsonify({'message': message}), 400
        user.role = role

    try:
        db.session.commit()
        return jsonify({'message': 'User updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to update user', 'error': str(e)}), 500
    finally:
        db.session.close()


@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)

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


def sanitize_email(email):
    sanitized_email = email.strip()
    return sanitized_email


def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+$'
    return bool(re.match(pattern, email))
