import os
import re

class Config:
    uri = os.getenv("DATABASE_URL")
    # For compatability with heroku
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_LOCATION = r'./files/'