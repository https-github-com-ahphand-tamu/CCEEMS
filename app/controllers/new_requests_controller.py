import logging
from app import db
from flask import Blueprint, render_template, request, jsonify, abort
from app.models import Request
import os
from werkzeug.utils import secure_filename
import pandas as pd
from flask import current_app

upload_new_req_bp = Blueprint('new-requests', __name__)


@upload_new_req_bp.route('/upload-new-requests', methods=['GET','POST'])
def upload_new_requests():  
    if request.method == 'POST':
        try:
            upload_file = request.files['new-requests']
            saved_file_name = os.path.join(current_app.config['UPLOAD_LOCATION'], secure_filename(upload_file.filename))
            upload_file.save(saved_file_name)
            return populateDatabase(upload_file)
        except Exception as e:
            logging.info("No file selected")
            return jsonify({'message': 'No file selected', 'error': str(e)}), 404
    return render_template('upload-new-requests.html')

def populateDatabase(upload_file):
    try:
        if upload_file.filename.endswith('.csv'):
            df = pd.read_csv(upload_file)
        elif upload_file.filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(upload_file)
        else:
            try:
                logging.info("Unsupported file format")
                abort(501, "Unsupported file format")
            except Exception as e:
                return jsonify({'message': 'Unsupported file format', 'error': str(e)}), 501
        df.rename(columns={'Outreach_Date': 'outreach_date'}, inplace=True)
        df = df.iloc[:, :5]
        logging.debug(f"POST to /upload-new-requests: {df}")
    
        df.to_sql(Request.__tablename__, db.engine, if_exists='append', index=False)
        db.session.commit()
        return render_template('upload-new-requests.html', data_inserted=True)
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to add new requests', 'error': str(e)}), 500
    finally:
        db.session.close()
