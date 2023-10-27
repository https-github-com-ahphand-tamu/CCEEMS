from app import db
from flask import Blueprint, render_template, request, jsonify, abort, current_app
from app.models import Newrequest
import os
from werkzeug.utils import secure_filename
import pandas as pd
from flask import current_app
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert

upload_new_req_bp = Blueprint('new-requests', __name__)


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
    return render_template('upload-new-requests-page.html', valid_present=False, valid_data=pd.DataFrame(),
                           invalid_present=False, invalid_data=pd.DataFrame())


def populateDatabase(upload_file, file_path):
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

        df = df.iloc[:, :5]
        df.rename(columns={'Outreach_Date': 'outreach_date'}, inplace=True)
        valid_data, invalid_data = validateData(df)

        current_app.logger.debug(f"POST to /upload-new-requests: {df}")

        # for index, row in valid_data.iterrows():
        #     customer_id = str(row['customer_id'])
        #     existing_data = db.session.query(Newrequest).filter_by(customer_id=customer_id).first()
        #     if existing_data:
        #         # Update existing row
        #         existing_data.first_name = row['first_name']
        #         existing_data.last_name = row['last_name']
        #         existing_data.num_of_children = row['num_of_children']
        #         existing_data.outreach_date = row['outreach_date']
        #     else:
        #         # Insert a new row
        #         new_request = Newrequest(**row)
        #         db.session.add(new_request)

        # valid_data.to_sql(Newrequest.__tablename__, db.engine, if_exists='append', index=False)

        # remove_duplicates_query = """
        # WITH CTE AS (
        #     SELECT
        #         customer_id,
        #         MIN(id) AS min_id
        #     FROM
        #         new_requests
        #     GROUP BY
        #         customer_id
        # )
        # DELETE FROM
        #     new_requests
        # WHERE
        #     (customer_id, id) NOT IN (SELECT customer_id, min_id FROM CTE);

        # ALTER SEQUENCE new_requests_id_seq RESTART WITH 1;
        # """
        insert_stmt = insert(Newrequest).values(
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
            UPDATE new_requests
            SET id = new_id
            FROM (SELECT id, ROW_NUMBER() OVER (ORDER BY id) as new_id FROM new_requests) as subquery
            WHERE new_requests.id = subquery.id;
        """

        db.session.execute(on_conflict_stmt)
        db.session.execute(text(reset_query))
        db.session.commit()

        if (invalid_data.empty):
            return render_template('upload-new-requests-page.html', valid_present=True, valid_data=valid_data,
                                   invalid_present=False, invalid_data=invalid_data)
        elif (valid_data.empty):
            return render_template('upload-new-requests-page.html', valid_present=False, valid_data=[], invalid_present=True,
                                   invalid_data=invalid_data)
        return render_template('upload-new-requests-page.html', valid_present=True, valid_data=valid_data,
                               invalid_present=True, invalid_data=invalid_data)

    except Exception as e:
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
