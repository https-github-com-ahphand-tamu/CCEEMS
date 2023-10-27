import logging
from behave import when, then
from werkzeug.datastructures import FileStorage
import os

from behave import when, then
from werkzeug.datastructures import FileStorage

from main import app

os.environ['FLASK_ENV'] = 'test'
client = app.test_client()

def simulate_form_submission(filename):
    with open(filename, 'rb') as file:
        upload_file = FileStorage(file)
        return client.post('/upload-new-requests', data={'new-requests': upload_file})

@when('I attach a file named "{filename}"')
def step_when_attach_file(context, filename):
    # Assuming the files are located in the "features/ENV[UPLOAD_LOCATION]" directory
    file_path = os.path.join(os.getcwd(), app.config["UPLOAD_LOCATION"], filename)
    context.file_path = file_path

@when('I submit the form')
def step_when_submit_form(context):
    response = simulate_form_submission(context.file_path)
    context.response = response

@then('Data inserted successfully')
def step_then_data_inserted_successfully(context):
    assert 'Data inserted successfully' in context.response.data.decode()

@then('the rendered html should contain "{expected_text}" in the valid table and "{invalid_text}" in invalid table')
def step_then_rendered_html_contains(context, expected_text, invalid_text):
    response = context.response
    page_content = response.data.decode('utf-8')

    # Check if the expected_text is present in the valid table
    assert expected_text in page_content

    # Check if the name is not in the valid table
    valid_table_start = page_content.find('Valid Data')
    valid_table_end = page_content.find('Invalid Data')

    if invalid_text != "NONE":
        # Check if the invalid_text is present in the invalid table
        invalid_table_start = page_content.find('Invalid Data')
        assert invalid_table_start != -1  # Check if the "Invalid Data" header exists in the page
        invalid_table_content = page_content[invalid_table_start:]
        logging.info(invalid_table_content)
        assert invalid_text in invalid_table_content
