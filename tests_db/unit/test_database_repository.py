import pytest

from games import SqlAlchemyRepository
from games.domainmodel.model import User, Review, Game, Genre, Publisher


def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_user(User('dave', '12345e6789'))
    repo.add_user(User('martin', '12345e6789'))
    user = repo.get_user('dave')
    assert user.username == 'dave' and user.password == '12345e6789'


def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_user(User('fmercury', '8734gfe2058v'))
    user = repo.get_user('fmercury')
    assert user.username == 'fmercury' and user.password == '8734gfe2058v'


def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = repo.add_user(User('felicity', 'pleasE1234'))
    user = repo.get_user('prince')
    assert user is None


def test_repository_can_add_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User("Davy", "seaweed123")
    game = Game(89, "Boring Game 3")
    review = Review(user, game, 3, "This was boring.")
    repo.add_review(review)

    assert repo.get_first_review() == review


def test_repository_can_retrieve_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User("Davy", "seaweed123")
    game = Game(89, "Boring Game 3")
    review = Review(user, game, 3, "This was boring.")
    repo.add_review(review)

    assert review in repo.get_reviews_by_game_id(89)


def test_repository_can_retrieve_reviews_of_game(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    assert len(repo.get_reviews_by_game_id(800)) == 0


def test_repository_does_not_retrieve_a_review_when_there_are_no_reviews_for_a_given_game(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    reviews = repo.get_reviews_by_game_id(300)

    assert reviews == []


def test_repository_can_retrieve_genres(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    genres = repo.get_genres()
    assert genres is not None


def test_repository_can_get_first_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User("Davy", "seaweed123")
    game = Game(89, "Boring Game 3")
    review = Review(user, game, 3, "This was boring.")
    repo.add_review(review)

    assert repo.get_first_review() == review


def test_repository_can_get_last_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User("Davy", "seaweed123")
    game = Game(89, "Boring Game 3")
    review = Review(user, game, 3, "This was boring.")

    user1 = User("Nina", "apricOt456")
    game1 = Game(89, "Sleep Phones")
    review1 = Review(user1, game1, 3, "This put me to sleep.")
    repo.add_review(review1)

    assert repo.get_last_review() == review1


def test_repository_can_get_review_by_ids(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User("Martin", "Martin123")
    game = Game(123, "Amazing Game")
    review = Review(user, game, 5, "Fantastic Game!")
    repo.add_review(review)

    review_result = repo.get_reviews_by_game_id(123)
    assert review == review_result[0]

def test_repository_does_not_retrieve_review_for_non_existent_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    review_result = repo.get_reviews_by_game_id(999)

    assert review_result == []


def test_repository_returns_none_when_there_are_no_previous_reviews(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    result = repo.get_last_review()

    assert result is None

def test_repository_does_not_add_a_review_without_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    pass


def make_review():
    user = User("Davy", "seaweed123")
    game = Game(89, "Boring Game 3")
    review = Review(user, game, 3, "This was boring.")
    return review


def test_repository_can_add_genres(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    genre = Genre("Fantasy")
    repo.add_genre(genre)
    genre_list = repo.get_genres()
    assert genre in genre_list


def test_repository_search_for_games_by_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    game = Game(890, "My New Game")
    repo.add_game(game)

    fetched_game = repo.get_game(890)
    assert fetched_game == game


def test_repository_can_add_a_game(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    game1 = Game(890, "My New Game")

    repo.add_game(game1)
    game_list = repo.get_games()
    assert game1 in game_list


def test_repository_can_retrieve_a_game_on_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    game1 = Game(890, "My New Game")

    repo.add_game(game1)
    result_game = repo.get_game_by_id(890)
    assert game1 == result_game


def test_repository_can_retrieve_a_game_by_publisher():
    pass


def test_repository_can_retrieve_game_by_title(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    game = Game(3000, "The Quest for the Lost Ark")
    repo.add_game(game)

    result_games = repo.search_games_by_title("Lost Ark")
    assert game in result_games