"""Initialize Flask app."""
import os
from pathlib import Path

from flask import Flask

from games.adapters.datareader import database_repository
from games.adapters.memoryRepository import MemoryRepository, populate
from games.domainmodel.model import Game
from games.adapters.repository import AbstractRepository

import games.adapters.repository as repo
#from games.adapters.memoryRepository import populate
from games.adapters import memoryRepository
from games.adapters.datareader import repository_populate

from games.adapters.datareader.database_repository import SqlAlchemyRepository
from games.adapters.datareader.orm import metadata, map_model_to_tables

# imports from SQLAlchemy
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool


def create_app(test_config=None):
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    app.config.from_object('config.Config')

# database uri that should be used for the connection
    database_uri = 'sqlite:///games.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

    app.config['SQLALCHEMY_ECHO'] = True  # logs all SQL statements - useful for debugging

    data_path = Path('games') / 'adapters' / 'data'
    # database_echo = app.config['SQLALCHEMY_ECHO'] -> i don't think we need this line
    #database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool,
                                 #   echo=False)

   ## if app.config['TESTING'] == 'True' or len(database_engine.table_names()) == 0:
    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config[
            'TEST_DATA_PATH']  # Make sure to change TEST_DATA_PATH : games/tests/data and TESTING: True in .env for testing

    if app.config['REPOSITORY'] == 'memory':
        # Create the MemoryRepository implementation for a memory-based repository.
        repo.repo_instance = memoryRepository.MemoryRepository()
        # fill the content of the repository from the provided csv files (has to be done every time we start app!)
        database_mode = False
        repository_populate.populate(data_path, repo.repo_instance, database_mode)


    elif app.config['REPOSITORY'] == 'database':
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']
        database_echo = app.config['SQLALCHEMY_ECHO']
        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool,
                                        echo=database_echo)
        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
        repo.repo_instance = database_repository.SqlAlchemyRepository(session_factory)
        if app.config['TESTING'] == 'True':
            print("REPOPULATING DATABASE...")
            # For testing, or first-time use of the web application, reinitialise the database.
            clear_mappers()
            metadata.create_all(database_engine)  # Conditionally create database tables.
            for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
                database_engine.execute(table.delete())

            # Generate mappings that map domain model classes to the database tables.
            map_model_to_tables()

            database_mode = True
            repository_populate.populate(data_path, repo.repo_instance, database_mode)
            print("REPOPULATING DATABASE... FINISHED")




    else:
        # Solely generate mappings that map domain model classes to the database tables.
        map_model_to_tables()



    #
    # repo.repo_instance = MemoryRepository()
    # populate(data_path, repo.repo_instance)

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

        # Register a callback the makes sure that database sessions are associated with http requests
        # We reset the session inside the database repository before a new flask request is generated
        @app.before_request
        def before_flask_http_request_function():
            if isinstance(repo.repo_instance, database_repository.SqlAlchemyRepository):
                repo.repo_instance.reset_session()

        # Register a tear-down method that will be called after each request has been processed.
        @app.teardown_appcontext
        def shutdown_session(exception=None):
            if isinstance(repo.repo_instance, database_repository.SqlAlchemyRepository):
                repo.repo_instance.close_session()

    return app
