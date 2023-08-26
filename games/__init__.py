"""Initialize Flask app."""

from flask import Flask, render_template
from games.domainmodel.model import Game
from games.adapters.repository import AbstractRepository

import games.adapters.repository as repo
from games.adapters.memoryRepository import populate
from games.adapters.memoryRepository import MemoryRepository


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
        app.register_blueprint(games.games_bp)

        from .descriptions import descriptions
        app.register_blueprint(descriptions.descriptions_blueprint)

    repo.repo_instance = MemoryRepository()
    populate(repo.repo_instance)

    return app
