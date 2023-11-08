from functools import wraps

from flask import abort, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user

from app.helpers.user_helpers import get_role_from_user


def requires_login(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        current_app.logger.info(f"Request to {request.path}")
        # Check if the user is authenticated
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))

        # Check the URL to determine if it has an /admin prefix
        is_admin_route = request.path.startswith('/admin')

        # If it's an admin route, return without user_id check
        if is_admin_route:
            return func(*args, **kwargs)

        # If it's not an admin route,
        # check if the user_id from the path parameter matches the ID of the currently logged-in user
        user_id = kwargs.get('user_id')
        if user_id and current_user.id != user_id:
            flash('You do not have permission to view this user\'s profile.', 'danger')
            return redirect('/')

        current_app.logger.debug(f"User {user_id} is trying to login")
        return func(*args, **kwargs)
    return login_required(decorated_view)


def requires_admin(func):
    @wraps(func)
    @login_required
    def decorated_view(*args, **kwargs):
        current_app.logger.debug(
            f"User {current_user.email} is trying to access an admin route")
        role = get_role_from_user(current_user)
        if role.name == "Admin":
            return func(*args, **kwargs)
        else:
            current_app.logger.debug(
                f"User {current_user.email} is not an admin, so forbidden from accessing the route")
            abort(403)
    return decorated_view
