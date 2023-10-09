from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Text, Float, ForeignKey
)
from sqlalchemy.orm import mapper, relationship


from games.domainmodel.model import Game, Publisher, Genre, User, Review

metadata = MetaData()


game_genres_table = Table(
    'game_genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True ),
    Column('game_id', ForeignKey('games.game_id')),
    Column('genre_name', ForeignKey('genres.genre_name'))
)

publishers_table = Table(
    'publishers', metadata,
    # Column('publisher_id', Integer, primary_key=True),
    Column('name', String(255), primary_key=True)
)

games_table = Table(
    'games', metadata,
    Column('game_id', Integer, primary_key=True),
    Column('game_title', String(50), nullable=False),
    Column('game_price', Float, nullable=False),
    Column('release_date', String(50), nullable=False),
    Column('game_description', String(255), nullable=True),
    Column('game_image_url', String(255), nullable=True),
    Column('game_website_url', String(255), nullable=True),
    Column('publisher_name', ForeignKey('publishers.name')),
    # Column('user_reviews', ForeignKey('user_reviews.user_reviews_id')),
)

genres_table = Table(
    'genres', metadata,
    Column('genre_name', String(64), primary_key=True),
)

# users_table = Table(
#     'users', metadata,
#     Column('user_id', Integer, primary_key=True, autoincrement=True),
#     Column('user_name', String(64), nullable=False),
# )

# reviews_table = Table(
#     'reviews', metadata,
#     Column('review_id', Integer, primary_key=True, autoincrement=True),
#     Column('review_text', String(1024), nullable=False),
#     Column('rating', Integer, nullable=False),
#     Column('user_id', ForeignKey('users.user_id')),
#     # Column('game_id', ForeignKey('games.game_id')),
# )
#
# user_reviews_table = Table(
#     'user_reviews', metadata,
#     Column('user_reviews_id', Integer, primary_key=True, autoincrement=True),
#     Column('user_id', ForeignKey('users.user_id')),
#     Column('review_id', ForeignKey('reviews.review_id')),
#     Column('game_id', ForeignKey('games.game_id')),
# )


def map_model_to_tables():
    # mapper(User, users_table, properties={
    #     '_User__user_name': users_table.c.user_name,
    #     '_User__reviews': relationship(Review),
    #     # '_User__games': relationship(Game, secondary=user_reviews_table),
    # })
    #
    # mapper(Review, reviews_table, properties={
    #     '_Review__user': relationship(User),
    #     # '_Review__game': relationship(Game),
    # })

    mapper(Genre, genres_table, properties={
        '_Genre__genre_name': genres_table.c.genre_name,
    })

    mapper(Publisher, publishers_table, properties={
        '_Publisher__publisher_name': publishers_table.c.name,
    })

    mapper(Game, games_table, properties={
        '_Game__game_id': games_table.c.game_id,
        '_Game__game_title': games_table.c.game_title,
        '_Game__price': games_table.c.game_price,
        '_Game__release_date': games_table.c.release_date,
        '_Game__description': games_table.c.game_description,
        '_Game__image_url': games_table.c.game_image_url,
        '_Game__website_url': games_table.c.game_website_url,
        '_Game__publisher': relationship(Publisher),
         '_Game__genres': relationship(Genre, secondary=game_genres_table),
        # '_Game__reviews': relationship(Review, secondary=user_reviews_table),
        # '_Game__users': relationship(User, secondary=user_reviews_table),
    })