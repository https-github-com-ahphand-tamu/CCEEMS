import logging

from flask import Blueprint, render_template
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

    logging.debug(user_list)
    return render_template('users.html', users=[])
