from .authentication import auth
from .user_management import user
from .autocomplete import autocomplete
from .movie import movie


def init_app(app):
    """Register blueprints

    Args:
        app (app): the unique instance app created in app/__init__.py
    """
    app.register_blueprint(auth)
    app.register_blueprint(user)
    app.register_blueprint(autocomplete)
    app.register_blueprint(movie)
