from behave import given, when, then
from flask import Flask
from app import create_app, db
from app.seeds import roles, users
import os
from app.models import Newrequest

os.environ['FLASK_ENV'] = 'test'
app = create_app()
client = app.test_client()

@given('I am on the "new-requests" page')
def step_given_i_am_on_new_requests_page(context):
    context.client = app.test_client()

@when('I view the list of new requests')
def step_when_i_view_list_of_new_requests(context):
    context.response = context.client.get('/new-requests')

@then('I should see a list of new requests with customer IDs, first names, and last names')
def step_then_i_should_see_list_of_new_requests(context):
    assert context.response.status_code == 200
    assert b"New Requests" in context.response.data
    assert b"ID" in context.response.data
    assert b"First Name" in context.response.data
    assert b"Last Name" in context.response.data
    # You can add more assertions to check for specific data in the response.

# Step Definitions for Scenario 2
@when('I click the "Assign" button for a new request')
def step_when_i_click_assign_button(context):
    context.response = context.client.get('/new-requests')

    # Extract request ID from the page
    request_id = 1  # Change this to a valid request ID
    context.request_id = request_id

@when('I select a user from the dropdown')
def step_when_i_select_user(context):
    context.data = {'user_id': '1'}  # Change '1' to a valid user ID

@when('I submit the assignment form')
def step_when_i_submit_assignment_form(context):
    context.response = context.client.post(f'/assign_request/{context.request_id}', data=context.data)

@then('I should see a success message')
def step_then_i_should_see_success_message(context):
    assert context.response.status_code == 200
    assert b"Request assigned successfully" in context.response.data

@given('create db')
def step(context):
    with app.app_context():
        db.create_all()
        roles.seed()
        users.seed()
        new_request_1 = Newrequest(
                customer_id="12345",
                first_name="John",
                last_name="Doe",
                num_of_children=2,
                outreach_date="2023-10-20"
            )
        new_request_2 = Newrequest(
            customer_id="67890",
            first_name="Jane",
            last_name="Smith",
            num_of_children=1,
            outreach_date="2023-10-21"
        )
        db.session.add(new_request_1)
        db.session.add(new_request_2)
        db.session.commit()

@given('purge db')
def step(context):
    with app.app_context():
        db.drop_all()