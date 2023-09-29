import json
import logging
from behave import given, when, then
from flask import Flask
from app import db, create_app
from app.models import User, Role
from bs4 import BeautifulSoup
import random
import string
import os

os.environ['FLASK_ENV'] = 'test'
# Set up a Flask app for testing
app = create_app()

# Create a test client to interact with the app
client = app.test_client()

@given('the application is running')
def step_given_application_running(context):
    context.users = {}

@when('I access the "{endpoint}" endpoint')
def step_when_access_endpoint(context, endpoint):
    context.response = client.get(endpoint)
    context.data = context.response.data.decode()

@then(u'I should see user details')
def step_assert_user_details(context):
    # Parse the rendered HTML from the response
    soup = BeautifulSoup(context.response.data, 'html.parser')
    # Check if the table headers are present
    headers = soup.find_all('th')
    expected_headers = ['Name', 'Email', 'Role']
    for header in headers:
        assert header.text in expected_headers

    # Check if user data is present
    user_data = soup.find_all('tr', {'class': 'user-data'})

    for user, user_element in zip(context.users, user_data):
        # Replace with the actual data structure used in your context
        expected_name = user['name']
        expected_email = user['email']
        expected_role = user['role']

        # Find the corresponding data in the HTML
        user_cells = user_element.find_all('td')
        actual_name = user_cells[0].text.strip()
        actual_email = user_cells[1].text.strip()
        actual_role = user_cells[2].text.strip()

        # Make assertions
        assert actual_name == expected_name
        assert actual_email == expected_email
        assert actual_role == expected_role

    assert context.response.status_code == 200

@then('I should see that user\'s details')
def step_assert_user_details(context):
    logging.info(context.data)
    assert 'id' in context.data
    assert 'name' in context.data
    assert 'email' in context.data
    assert 'role' in context.data

@when('I send a POST request to "{endpoint}" with JSON')
def step_when_send_post_request(context, endpoint):
    json_data = json.loads(context.text)
    if json_data['email']:
        json_data['email'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)) + '@gmail.com'
    context.response = client.post(endpoint, json=json_data)
    context.data = json.loads(context.response.data.decode())
    logging.info(context.data)

@then('the response status code should be {status_code:d}')
def step_then_response_status_code(context, status_code):
    assert context.response.status_code == status_code

@then('the response should contain "{text}"')
def step_then_response_contains_text(context, text):
    logging.info(context.response.data.decode())
    assert text in context.data["message"]

@when('I send a PUT request to "{endpoint}" with JSON')
def step_when_send_put_request(context, endpoint):
    json_data = json.loads(context.text)
    context.response = client.put(endpoint, json=json_data)
    context.data = json.loads(context.response.data.decode())
    logging.info(context.data)

@when('I send a DELETE request to "{endpoint}"')
def step_when_send_delete_request(context, endpoint):
    context.response = client.delete(endpoint)
    context.data = json.loads(context.response.data.decode())

# Hooks to set up and tear down the test database
def before_scenario(context, scenario):
    with app.app_context():
        db.create_all()

def after_scenario(context, scenario):
    with app.app_context():
        db.session.remove()
        db.drop_all()