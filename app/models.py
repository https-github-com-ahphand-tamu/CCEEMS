from app import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    role = db.relationship('Role', backref=db.backref('users', lazy=True))

    def __init__(self, name, email, role):
        self.name = name
        self.email = email
        self.role = role

    def __repr__(self):
        return f'<User {self.name}>'


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Role {self.name}>'


class Request(db.Model):
    __tablename__ = 'new-requests'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.String(80), unique=False, nullable=False)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    num_of_children = db.Column(db.Integer, nullable=False)

    def __init__(self, customer_id, first_name, last_name, num_of_children):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.num_of_children = num_of_children
