import logging
from datetime import datetime

from flask import Blueprint, request, jsonify, render_template
from flask_login import current_user

from app import db
from app.decorators.login_decorator import requires_admin
from app.exceptions.validation import ValidationException
from app.helpers.user_helpers import validate_add_user_payload, validate_user_email, validate_role, send_mail
from app.models import User

import uuid

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin/users', methods=['GET'])
@requires_admin
def get_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_data = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role.name
        }
        user_list.append(user_data)

    logging.debug(user_list)
    return render_template('manage_users.html', user=current_user, users=user_list)


@admin_bp.route('/admin/users/<int:user_id>', methods=['GET'])
@requires_admin
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


@admin_bp.route('/admin/users', methods=['POST'])
@requires_admin
def add_user():
    try:
        data = request.get_json()
        logging.info(f"POST to /users: {data}")

        validate_add_user_payload(data)
        email = validate_user_email(data["email"])
        role = validate_role(data["role"])
        user_exists = db.session.query(User).filter(
            User.email == email).first()
        if user_exists:
            return jsonify({'message': f'User already exists with email: {data["email"]}'}), 400

        verification_code = str(uuid.uuid1())
        new_user = User(name=data.get('name'), email=email, role=role)
        new_user.created_on = datetime.utcnow()
        new_user.verification_code = verification_code

        try:
            db.session.add(new_user)
            db.session.commit()
            send_mail(request.base_url, email, verification_code)

            user_data = {
                'id': new_user.id,
                'name': new_user.name,
                'email': new_user.email,
                'role': new_user.role.name if new_user.role else None
            }
            return jsonify({'message': 'User added successfully', 'data': user_data}), 201
        except Exception as e:
            logging.error(e)
            db.session.rollback()
            return jsonify({'message': 'Failed to add user', 'error': str(e)}), 500
        finally:
            db.session.close()
    except ValidationException as ve:
        logging.error(ve)
        return jsonify({'message': str(ve)}), ve.status_code


@admin_bp.route('/admin/users/<int:user_id>', methods=['PUT'])
@requires_admin
def update_user(user_id):
    try:
        data = request.get_json()
        logging.info(
            f"PUT to /users with user id: {user_id} and data: {data}")

        validate_add_user_payload(data)
        email = validate_user_email(data["email"])
        role = validate_role(data["role"])
        name = data.get('name')

        user = User.query.get(user_id)
        if user is None:
            return jsonify({'message': 'User not found'}), 404

        if name != user.name:
            user.name = data['name']
        if email != user.email:
            user.email = email
        if role != user.role:
            user.role = role

        try:
            db.session.commit()
            user_data = {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'role': user.role.name if user.role else None
            }
            return jsonify({'message': 'User updated successfully', 'data': user_data}), 200
        except Exception as e:
            logging.error(e)
            db.session.rollback()
            return jsonify({'message': 'Failed to update user', 'error': str(e)}), 500
        finally:
            db.session.close()
    except ValidationException as ve:
        logging.error(ve)
        return jsonify({'message': str(ve)}), ve.status_code


@admin_bp.route('/admin/users/<int:user_id>', methods=['DELETE'])
@requires_admin
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
