from datetime import datetime
from enum import Enum

from flask_login import UserMixin
from sqlalchemy import DateTime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import UniqueConstraint

from app import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    password = db.Column(db.String(128), nullable=True)
    created_on = db.Column(DateTime, default=datetime.utcnow)
    modified_on = db.Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    verified_on = db.Column(DateTime)
    last_login = db.Column(DateTime)

    role = db.relationship('Role', backref=db.backref('users', lazy=True))
    user_cases = db.relationship('Case', backref=db.backref('cases', lazy=True))

    def __init__(self, name, email, role):
        self.name = name
        self.email = email
        self.role = role
        self.password = ""

    def __repr__(self):
        return f'<User {self.name}>'

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Role {self.name}>'


class PacketReturnStatus(Enum):
    RETURNED = "Returned"
    NOT_RETURNED = "Not Returned"
    WAITING = "Waiting for Response"


class Decision(Enum):
    ENROLLED = "Enrolled"
    NOT_ENROLLED = "Not Enrolled"
    WAITING = "Waiting for Response"


class Case(db.Model):
    __tablename__ = 'cases'
    __table_args__ = (
        UniqueConstraint('customer_id', name='_customer_id_uc'),  # Add a unique constraint to customer_id
    )

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.String(80), unique=False, nullable=False)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    num_of_children = db.Column(db.Integer, unique=False, nullable=False)
    outreach_date = db.Column(db.Date, unique=False, nullable=False)
    packet_return_status = db.Column(db.Enum(PacketReturnStatus), nullable=False, server_default=PacketReturnStatus.WAITING.name)
    packet_received_date = db.Column(db.Date, unique=False, nullable=True)
    staff_initials = db.Column(db.String(80), unique=False, nullable=True)
    decision = db.Column(db.Enum(Decision), nullable=False, server_default=Decision.WAITING.name)
    num_children_enrolled = db.Column(db.Integer, unique=False, nullable=True)
    decision_date = db.Column(db.Date, unique=False, nullable=True)
    not_enrolled_reason = db.Column(db.String(80), unique=False, nullable=True)
    assigned_to_user = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, customer_id, first_name, last_name, num_of_children, outreach_date, packet_return_status=None,
                 packet_received_date=None, staff_initials=None, decision=None, num_children_enrolled=None,
                 decision_date=None, not_enrolled_reason=None, assigned_to_user=None):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.num_of_children = num_of_children
        self.outreach_date = outreach_date
        self.packet_return_status = packet_return_status or PacketReturnStatus.WAITING
        self.packet_received_date = packet_received_date or None
        self.staff_initials = staff_initials
        self.decision = decision or Decision.WAITING
        self.num_children_enrolled = num_children_enrolled
        self.decision_date = decision_date or None
        self.not_enrolled_reason = not_enrolled_reason
        self.assigned_to_user = assigned_to_user

    def __str__(self):
        return f"Case(id={self.id}, customer_id={self.customer_id}, first_name={self.first_name}, " \
               f"last_name={self.last_name}, num_of_children={self.num_of_children}, " \
               f"outreach_date={self.outreach_date}, packet_return_status={self.packet_return_status}, " \
               f"packet_received_date={self.packet_received_date}, staff_initials={self.staff_initials}, " \
               f"decision={self.decision}, num_children_enrolled={self.num_children_enrolled}, " \
               f"decision_date={self.decision_date}, not_enrolled_reason={self.not_enrolled_reason}, " \
               f"assigned_to_user={self.assigned_to_user})"
