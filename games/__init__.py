"""Initialize Flask app."""
import os
from pathlib import Path

from flask import Flask
from games.domainmodel.model import Game
from games.adapters.repository import AbstractRepository

import games.adapters.repository as repo
from games.adapters.memoryRepository import populate
from games.adapters.memoryRepository import MemoryRepository


def create_app(test_config=None):
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)
    app.config.from_object('config.Config')
    data_path = Path('games') / 'adapters' / 'data'
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH'] # Make sure to change TEST_DATA_PATH : games/tests/data and TESTING: True in .env for testing

    repo.repo_instance = MemoryRepository()
    populate(data_path, repo.repo_instance)

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

        from .reviews import reviews
        app.register_blueprint(reviews.reviews_blueprint)

        from .forms import forms
        app.register_blueprint(forms.forms_blueprint)

    return app
