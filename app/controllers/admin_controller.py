from datetime import datetime

from flask import Blueprint, request, jsonify, render_template, current_app

from app import db
from app.decorators.login_decorator import requires_admin
from app.exceptions.validation import ValidationException
from app.helpers.user_helpers import validate_user_payload, validate_user_email, validate_role
from app.models import User

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
            'role': user.role
        }
        user_list.append(user_data)

    current_app.logger.debug(user_list)
    return render_template('users.html', users=user_list)


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
        current_app.logger.debug(f"POST to /users: {data}")

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


@admin_bp.route('/admin/users/<int:user_id>', methods=['PUT'])
@requires_admin
def update_user(user_id):
    try:
        data = request.get_json()
        current_app.logger.debug(f"PUT to /users with user id: {user_id} and data: {data}")

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
