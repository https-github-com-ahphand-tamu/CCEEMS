# features/steps/assign_case_steps.py

from behave import given, when, then

@given('there is a case with packet return status "RETURNED"')
def create_returned_case(context):
    # Assuming you have logic to create a case with packet return status "RETURNED"
    context.returned_case_id = context.returned_case.id  # Replace with the actual case ID

@given('there is a case with packet return status "WAITING"')
def create_waiting_case(context):
    # Assuming you have logic to create a case with packet return status "WAITING"
    context.waiting_case_id = context.waiting_case.id  # Replace with the actual case ID

@given('there is a user')
def create_user(context):
    # Assuming you have logic to create a user
    context.user_id = 1  # Replace with the actual user ID

@when('the user assigns the case to the user')
def assign_case_to_user(context):
    # Assuming you have logic to assign the case to the user
    context.response = context.client.post('/case/assign/', json={'user_id': context.user_id, 'case_id': context.returned_case_id})

@then('the case should be assigned successfully')
def check_assignment_success(context):
    assert context.response.status_code == 200
    assert 'Case assigned successfully' in context.response.json['message']

@when('the user tries to assign the case to the user')
def try_to_assign_case(context):
    # Assuming you have logic to try to assign the case to the user
    context.response = context.client.post('/case/assign/', json={'user_id': context.user_id, 'case_id': context.waiting_case_id})

@then('an error should be displayed indicating the case can\'t be assigned')
def check_assignment_error(context):
    assert context.response.status_code == 400
    assert 'Cannot assign case who\'s package is not received' in context.response.json['message']

@given('there is an invalid case ID or user ID')
def set_invalid_ids(context):
    context.invalid_case_id = 999  # Replace with an invalid case ID
    context.invalid_user_id = 999  # Replace with an invalid user ID

@then('an error should be displayed indicating an invalid case or user')
def check_invalid_assignment_error(context):
    assert context.response.status_code == 400
    assert 'Invalid Case/User' in context.response.json['message']
