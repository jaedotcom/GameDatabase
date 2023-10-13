import pytest
import os.path
from sqlalchemy import select, inspect
from games.adapters.datareader.orm import metadata

def test_database_populate_inspect_table_names(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    print(inspector.get_table_names())
    assert all(element in inspector.get_table_names() for element in ['game_genres', 'publishers', 'games', 'genres', 'users', 'reviews', 'user_game_favourites'])


def test_database_populate_select_all_genres(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_genres_table = inspector.get_table_names()[3]

    with database_engine.connect() as connection:
        # query for records in table tags
        select_statement = select([metadata.tables[name_of_genres_table]])
        result = connection.execute(select_statement)

        all_genre_names = []
        for row in result:
            all_genre_names.append(row['tag_name'])
#add all genres in???
        assert all_genre_names == ['New Zealand', 'Health', 'World', 'Politics']


def test_database_populate_select_all_users(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[4]

    with database_engine.connect() as connection:
        # query for records in table users
        select_statement = select([metadata.tables[name_of_users_table]])
        result = connection.execute(select_statement)

        all_users = []
        for row in result:
            all_users.append(row['user_name'])

        assert all_users == ['thorke', 'fmercury']


def test_database_populate_select_all_reviews(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_comments_table = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        # query for records in table comments
        select_statement = select([metadata.tables[name_of_comments_table]])
        result = connection.execute(select_statement)

        all_comments = []
        for row in result:
            all_comments.append((row['id'], row['user_id'], row['article_id'], row['comment']))

        assert all_comments == [(1, 2, 1, 'Oh no, COVID-19 has hit New Zealand'),
                                (2, 1, 1, 'Yeah Freddie, bad news')]


def test_database_populate_select_all_publishers(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_articles_table = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        # query for records in table articles
        select_statement = select([metadata.tables[name_of_articles_table]])
        result = connection.execute(select_statement)

        all_articles = []
        for row in result:
            all_articles.append((row['id'], row['title']))

        nr_articles = len(all_articles)
        assert nr_articles == 6

        assert all_publishers[0] == (1, 'Coronavirus: First case of virus in New Zealand')


def test_database_populate_select_all_games(database_engine):
    inspector = inspect(database_engine)
    games_table_name = inspector.get_table_names()[1]
    print(games_table_name)

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[games_table_name]])
        result = connection.execute(select_statement)

        game_details = []
        for row in result:
            game_details.append((row['game_id'], row['game_title']))

        number_of_games = len(game_details)
        assert number_of_games == 800

        assert game_details[0] == (7940, 'Call of Duty® 4: Modern Warfare®')


