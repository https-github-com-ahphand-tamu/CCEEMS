import os
import logging
from behave import given, when, then
from flask import Flask
from app import create_app, db
from werkzeug.datastructures import FileStorage
from bs4 import BeautifulSoup

os.environ['FLASK_ENV'] = 'test'
app = create_app()
client = app.test_client()

def simulate_form_submission(filename):
    with open(filename, 'rb') as file:
        upload_file = FileStorage(file)
        return client.post('/upload-new-requests', data={'new-requests': upload_file})

@when('I attach a file named "{filename}"')
def step_when_attach_file(context, filename):
    # Assuming the files are located in the "features/files" directory
    file_path = os.path.join(os.getcwd(), 'features', 'files', filename)
    context.file_path = file_path

@when('I submit the form')
def step_when_submit_form(context):
    response = simulate_form_submission(context.file_path)
    context.response = response

@then('Data inserted successfully')
def step_then_data_inserted_successfully(context):
    assert 'Data inserted successfully' in context.response.data.decode()

@then('the rendered html should contain "{expected_text}"')
def step_then_rendered_html_contains(context, expected_text):
    response = context.response
    logging.info(response)
    # Check if the response is HTML
    assert response.content_type == 'text/html; charset=utf-8'
    # Parse the rendered HTML from the response
    soup = BeautifulSoup(response.data, 'html.parser')
    # Find all occurrences of the expected text
    found_text = soup.find(text=expected_text)
    # Check if the expected text is found in the HTML
    assert found_text is not None
