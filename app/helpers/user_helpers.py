import re

from flask import current_app

from app.exceptions.validation import ValidationException
from app.models import Role, User


def validate_user_payload(data):
    if 'name' not in data or 'email' not in data or 'role' not in data:
        raise ValidationException('Missing required fields (name, email, role)', 400)


def validate_role(role_name):
    role = Role.query.filter_by(name=role_name).first()
    if not role:
        message = f"Role '{role_name}' does not exist"
        current_app.logger.info(message)
        raise ValidationException(message, 400)
    return role


def get_role_from_user(user: User):
    role = Role.query.filter_by(id=user.role.id).first()
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
