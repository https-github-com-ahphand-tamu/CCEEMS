from flask import Blueprint, request, jsonify, render_template
from app import db
from app.models import User

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

    # users_data = jsonify({'users': user_list})
    return render_template('users.html', users=user_list)
    # return jsonify({'users': user_list})


# Add a new user
@user_bp.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(name=data['name'], email=data['email'], role=data['role'])

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to add user', 'error': str(e)}), 500
    finally:
        db.session.close()

# Update an existing user
@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = User.query.get(user_id)

    if user is None:
        return jsonify({'message': 'User not found'}), 404

    user.name = data['name']
    user.email = data['email']
    user.role = data['role']

    try:
        db.session.commit()
        return jsonify({'message': 'User updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to update user', 'error': str(e)}), 500
    finally:
        db.session.close()

# Delete an existing user
@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query
