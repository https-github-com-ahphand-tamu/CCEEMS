import logging
from app import db
from flask import Blueprint, render_template, request, current_app, jsonify
from app.models import Request
import os
from werkzeug.utils import secure_filename

from config import Config
import pandas as pd

upload_new_req_bp = Blueprint('new-requests', __name__)


@upload_new_req_bp.route('/upload-new-requests', methods=['GET','POST'])
def upload_new_requests():
    if request.method == 'POST':
        upload_file = request.files['new-requests']
        upload_file.save(os.path.join(Config.UPLOAD_LOCATION, secure_filename(upload_file.filename)))
        return populateDatabase(upload_file)
        

    return render_template('upload-new-requests.html')

def populateDatabase(upload_file):
    if not upload_file:
        return "No file uploaded"
    try:
        if upload_file.filename.endswith('.csv'):
            df = pd.read_csv(upload_file)
        elif upload_file.filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(upload_file)
        else:
            return "Unsupported file format"
        df.rename(columns={'Outreach_Date': 'outreach_date'}, inplace=True)
        df = df.iloc[:, :5]  # Selects all rows and the first 5 columns
        print(df)
    
        df.to_sql(Request.__tablename__, db.engine, if_exists='append', index=False)
        db.session.commit()

        return "Data inserted successfully"
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to add new requests', 'error': str(e)}), 500
    finally:
        db.session.close()
