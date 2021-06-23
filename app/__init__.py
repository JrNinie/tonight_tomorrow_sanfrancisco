from flask import Flask
import os
import models
import routes


def create_app():
    """Construct the core flask application

    This allows to create only one instance named app
    by using basic factory pattern,
    and to define some config for app.

    Returns:
        app: unique instance of flask app for whole project
    """

    app = Flask(__name__)

    # Register the right config for app
    current_flask_env = os.getenv("FLASK_ENV").lower()
    if current_flask_env == "production":
        app.config.from_object("config.ProductionConfig")
    elif current_flask_env == "development":
        app.config.from_object("config.DevelopmentConfig")
    elif current_flask_env == "testing":
        app.config.from_object("config.TestingConfig")
    else:
        return {"Message": "The config is incorrect."}

    models.init_app(app)
    routes.init_app(app)

    return app
