from flask import Blueprint, jsonify, current_app

from app.models import Role
from app.decorators.login_decorator import requires_admin

role_bp = Blueprint('role', __name__)


@requires_admin
@role_bp.route('/roles', methods=['GET'])
def get_roles():
    roles = Role.query.all()
    roles_dict = [{'id': role.id, 'name': role.name} for role in roles]
    current_app.logger.debug(roles_dict)
    return jsonify({
        'message': 'success',
        'data': roles_dict
    }), 200
