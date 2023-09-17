"""Initialize Flask app."""
import os
from flask import Flask
from games.domainmodel.model import Game
from games.adapters.repository import AbstractRepository

import games.adapters.repository as repo
from games.adapters.memoryRepository import populate
from games.adapters.memoryRepository import MemoryRepository


def create_app():
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    repo.repo_instance = MemoryRepository()
    populate(repo.repo_instance)

    # Build the application - these steps require an application context.
    with app.app_context():
        # Register blueprints.
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .games import games
        app.register_blueprint(games.games_bp)

        from .descriptions import descriptions
        app.register_blueprint(descriptions.descriptions_blueprint)

        from .genreBar import genreBar
        app.register_blueprint(genreBar.genreBar_blueprint)

        from .searchresults import search
        app.register_blueprint(search.search_bp)

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        from .profile import profile
        app.register_blueprint(profile.profile_blueprint)

    return app
