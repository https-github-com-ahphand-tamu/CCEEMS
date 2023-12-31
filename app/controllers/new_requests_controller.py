import os
from datetime import datetime

import pandas as pd
from flask import Blueprint, render_template, request, jsonify, abort, current_app
from flask_login import current_user
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert
from werkzeug.utils import secure_filename

from app import db
from app.decorators.login_decorator import requires_admin
from app.models import Case

upload_new_req_bp = Blueprint('new-requests', __name__)


@requires_admin
@upload_new_req_bp.route('/upload-new-requests', methods=['GET', 'POST'])
def upload_new_requests():
    if request.method == 'POST':
        try:
            upload_file = request.files['new-requests']
            if len(upload_file.filename) > 0:
                file_path = os.path.join(
                    current_app.config['UPLOAD_LOCATION'], secure_filename(upload_file.filename))
                return populateDatabase(upload_file, file_path)
            else:
                abort(404, "No file selected")
        except Exception as e:
            current_app.logger.info("No file selected")
            return jsonify({'message': 'No file selected', 'error': str(e)}), 404
    else:
        return render_template('upload-new-requests-page.html', valid_present=False, valid_data=pd.DataFrame(),
                               invalid_present=False, invalid_data=pd.DataFrame(), user=current_user)


def populateDatabase(upload_file, file_path):
    current_app.logger.debug("Populating database")
    try:
        if upload_file.filename.endswith('.csv'):
            upload_file.save(file_path)
            df = pd.read_csv(file_path, sep=",")
        elif upload_file.filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(upload_file)
        else:
            try:
                current_app.logger.info("Unsupported file format")
                abort(501, "Unsupported file format")
            except Exception as e:
                return jsonify({'message': 'Unsupported file format', 'error': str(e)}), 501

        #df = df.iloc[:, :5]
        df.rename(columns={'Outreach_Date': 'outreach_date'}, inplace=True)
        valid_data, invalid_data = validateData(df)

        current_app.logger.debug(f"POST to /upload-new-requests: {df}")
        insert_stmt = insert(Case).values(
            valid_data.to_dict(orient='records'))
        on_conflict_stmt = insert_stmt.on_conflict_do_update(
            index_elements=['customer_id'],
            set_={
                'first_name': insert_stmt.excluded.first_name,
                'last_name': insert_stmt.excluded.last_name,
                'num_of_children': insert_stmt.excluded.num_of_children,
                'outreach_date': insert_stmt.excluded.outreach_date
            }
        )

        reset_query = """
            UPDATE cases
            SET id = new_id
            FROM (SELECT id, ROW_NUMBER() OVER (ORDER BY id) as new_id FROM cases) as subquery
            WHERE cases.id = subquery.id;
        """

        db.session.execute(on_conflict_stmt)
        db.session.execute(text(reset_query))
        db.session.commit()

        if (invalid_data.empty):
            return render_template('upload-new-requests-page.html', valid_present=True, valid_data=valid_data,
                                   invalid_present=False, invalid_data=invalid_data, user=current_user)
        elif (valid_data.empty):
            return render_template('upload-new-requests-page.html', valid_present=False, valid_data=[],
                                   invalid_present=True,
                                   invalid_data=invalid_data, user=current_user)
        return render_template('upload-new-requests-page.html', valid_present=True, valid_data=valid_data,
                               invalid_present=True, invalid_data=invalid_data, user=current_user)

    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify({'message': 'Failed to add new requests', 'error': str(e)}), 500
    finally:
        db.session.close()


def validateData(data):
    invalid_rows = []
    valid_rows = []

    # Check if all required columns are present in the DataFrame
    required_columns = ['customer_id', 'first_name',
                        'last_name', 'num_of_children', 'outreach_date']
    if not set(required_columns).issubset(data.columns):
        invalid_rows.append(data)
        invalid_df = pd.DataFrame(invalid_rows)
        invalid_df = invalid_df.reset_index(drop=True)
        return pd.DataFrame(), invalid_df

    # Check each row for validation
    for index, row in data.iterrows():
        validation_errors = []

        # Check if 'customer_id' contains digits only and does not start from 0
        if not str(row['customer_id']).isdigit() or str(row['customer_id'])[0] == '0':
            validation_errors.append(
                "Invalid value in customer_id. Must contain digits only and not start from 0.")

        # Check if 'num_of_children' is a non-negative integer
        if not str(row['num_of_children']).isdigit() or int(row['num_of_children']) < 0:
            validation_errors.append(
                "Invalid value in num_of_children. Must be a non-negative integer.")

        # Check if 'Outreach_Date' is a valid date and not in the future
        try:
            outreach_date = pd.to_datetime(row['outreach_date'])
            if outreach_date > datetime.now():
                validation_errors.append(
                    "Invalid date in Outreach_Date. Cannot be in the future.")
        except ValueError:
            validation_errors.append("Invalid date format in Outreach_Date.")

        if validation_errors:
            row_with_error = row.copy()
            row_with_error['validation_error'] = ', '.join(validation_errors)
            invalid_rows.append(row_with_error)
        else:
            valid_rows.append(row)

    # Convert rows to DataFrames
    valid_df = pd.DataFrame(valid_rows)
    # Use reset_index to ignore the original index
    valid_df = valid_df.reset_index(drop=True)

    if invalid_rows:
        invalid_df = pd.DataFrame(invalid_rows)
        invalid_df = invalid_df.reset_index(drop=True)
    else:
        invalid_df = pd.DataFrame()

    return valid_df, invalid_df
