from datetime import datetime
from sqlalchemy import DateTime, Column, Integer, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from app import db
from enum import Enum


class User(db.Model):
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

    def __init__(self, name, email, role):
        self.name = name
        self.email = email
        self.role = role
        self.password = generate_password_hash("Password@123")

    def __repr__(self):
        return f'<User {self.name}>'

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


class Newrequest(db.Model):
    __tablename__ = 'new_requests'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    num_of_children = db.Column(db.Integer, nullable=False)
    outreach_date = db.Column(db.Date, nullable=False)

    def __init__(self, customer_id, first_name, last_name, num_of_children, outreach_date):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.num_of_children = num_of_children
        self.outreach_date = outreach_date


class PacketReturnStatus(Enum):
    RETURNED = "Returned"
    NOT_RETURNED = "Not Returned"
    WAITING = "Waiting for Response"


class Decision(Enum):
    ENROLLED = "Enrolled"
    NOT_ENROLLED = "Not Enrolled"
    WAITING = "Waiting for Response"


class Currentrequest(db.Model):
    __tablename__ = 'current_requests'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.String(80), unique=False, nullable=False)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    num_of_children = db.Column(db.Integer, unique=False, nullable=False)
    outreach_date = db.Column(db.Date, unique=False, nullable=False)
    packet_return_status = db.Column(
        db.Enum(PacketReturnStatus), nullable=False)
    packet_received_date = db.Column(db.Date, unique=False, nullable=True)
    staff_initials = db.Column(db.String(80), unique=False, nullable=False)
    decision = db.Column(db.Enum(Decision), nullable=False)
    num_children_enrolled = db.Column(db.Integer, unique=False, nullable=True)
    decision_date = db.Column(db.Date, unique=False, nullable=True)
    not_enrolled_reason = db.Column(db.String(80), unique=False, nullable=True)

    def __init__(self, customer_id, first_name, last_name, num_of_children, outreach_date, packet_return_status, packet_received_date, staff_initials, decision, num_children_enrolled, decision_date, not_enrolled_reason):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.num_of_children = num_of_children
        self.outreach_date = outreach_date
        self.packet_return_status = packet_return_status
        self.packet_received_date = packet_received_date
        self.staff_initials = staff_initials
        self.decision = decision
        self.num_children_enrolled = num_children_enrolled
        self.decision_date = decision_date
        self.not_enrolled_reason = not_enrolled_reason
