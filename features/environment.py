from flask import Flask
from app import create_app, db,seeds
import os

os.environ['FLASK_ENV'] = 'test'
app = create_app()
client = app.test_client()

def step(context):
    # Establish a connection to the test database
    with app.app_context():
        db.create_all()
        seeds.users()
        seeds.roles()

def after_all(context):
    # Drop the test database and close the database session
    with app.app_context():
        db.drop_all()
