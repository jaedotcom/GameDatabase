import pytest

import datetime

from sqlalchemy.exc import IntegrityError

from games.domainmodel.model import User, Review, Game


def insert_user(empty_session, values=None):
    new_name = "Andrew"
    new_password = "1234"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                          {'username': new_name, 'password': new_password})
    row = empty_session.execute('SELECT id from users where user_name = :user_name',
                                {'username': new_name}).fetchone()
    return row[0]


def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                              {'username': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT id from users'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_review(empty_session):
    empty_session.execute(
        'INSERT INTO reviews (id, user_id, game_id, rating, comment) VALUES '
        '(:id, "50", '
        '"70", '
        '"9999999", '
        '"5")'
    )
    row = empty_session.execute('SELECT id from reviews').fetchone()
    return row[0]


def make_review():
    review = Review(
        make_user(),
        make_game(),
        3,
        "This game sucks, I hate it. AVOID! "
    )
    return review


def make_game():
    game = Game(999999, "Test_game_PEOW")
    return game


def make_user():
    user = User("Andrew", "111")
    return user


def test_loading_of_users(empty_session):
    users = list()
    users.append(("andrew", "Testing1234"))
    users.append(("cindy", "Testing1111"))
    insert_users(empty_session, users)

    expected = [
        User("andrew", "Testing1234"),
        User("cindy", "Testing1111")
    ]
    assert empty_session.query(User).all() == expected


def test_saving_of_users(empty_session):
    user = User("andrew", "Password123")
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT username, password FROM users'))
    assert rows == [("andrew", "Password123")]


def test_saving_of_users_with_common_user_name(empty_session):
    user1 = User("andrew", "Testing1234")
    empty_session.add(user1)
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user2 = User("andrew", "Error456")
        empty_session.add(user2)
        empty_session.commit()


def test_loading_of_game(empty_session):
    game = Game(999999, "Test_game_PEOW")
    empty_session.add(game)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT game_title FROM games'))
    assert rows == [("Test_game_PEOW",)]


def test_saving_of_review(empty_session):
    game = Game(999999, "Test_game_PEOW")
    user1 = User("andrew", "Testing1234")
    review = Review(user1, game, 4, "so lost")
    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT rating FROM reviews'))
    assert rows == [(4,)]


