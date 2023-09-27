import logging
from app import db
from flask import Blueprint, render_template, request, current_app
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
        if upload_file:
            if upload_file.filename.endswith('.csv'):
                df = pd.read_csv(upload_file)
            elif upload_file.filename.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(upload_file)
            else:
                return "Unsupported file format"
            df.to_sql(Request.__tablename__, current_app.db.engine, if_exists='append', index=False)
        return "Uploaded successfully!"

    return render_template('upload-new-requests.html')
