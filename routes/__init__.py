from .authentication import auth
from .user_management import user


def init_app(app):
    """Register blueprints

    Args:
        app (app): the unique instance app created in app/__init__.py
    """
    app.register_blueprint(auth)
    app.register_blueprint(user)
