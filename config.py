import os

class BaseConfig:
    uri = os.getenv("DATABASE_URL")
    # For compatibility with Heroku
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_LOCATION = r'./files/'

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False

class TestConfig():
    uri = "sqlite:///default.db"
    SQLALCHEMY_DATABASE_URI = uri
    TESTING = True
    UPLOAD_LOCATION = r'features/testUploadFiles/'