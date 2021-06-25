import os


class Config:
    """Base config"""

    # Secret key to generate token
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Configure/connextion database
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    FLASK_DEBUG = os.getenv("FLASK_DEBUG")
    FLASK_RUN_PORT = os.getenv("FLASK_RUN_PORT")
    FLASK_RUN_HOST = os.getenv("FLASK_RUN_HOST")


class DevelopmentConfig(Config):
    # Add different config for dev if necessary
    pass


class TestingConfig(Config):
    # Add different config for test if necessary
    pass


class ProductionConfig(Config):
    # Add other different config for prod if necessary
    FLASK_DEBUG = 0
