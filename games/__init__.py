"""Initialize Flask app."""

from flask import Flask, render_template
from games.domainmodel.model import Game


def create_app():
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    # Build the application - these steps require an application context.
    with app.app_context():
        # Register blueprints.
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .games import games
        app.register_blueprint(games.games_blueprint)

    return app
