import pytest
import os.path
from typing import List
from games.adapters.datareader.csvdatareader import GameFileCSVReader
from games.domainmodel.model import Publisher, Genre, Game, Review, User
from datetime import datetime
from games.adapters.repository import AbstractRepository
from games.authentication import services as auth_services


class MemoryRepository(AbstractRepository):

    def __init__(self):
        self.__reviews = list()
        self.__games = list()
        self.__genres = list()
        self.__games_by_genre = dict()
        self.__users = list()

    def add_user(self, user: User):
        for already_user in self.__users:
            if already_user.username == user.username:
                return "Username already taken."
        self.__users.append(user)

    def get_user(self, user_name) -> User:
        return next((user for user in self.__users if user.username == user_name), None)

    def add_game(self, game: Game):
        self.__games.append(game)
        for genre_name in game.genres:
            if genre_name not in self.__games_by_genre:
                self.__games_by_genre[genre_name] = []
            self.__games_by_genre[genre_name].append(game)

    def get_games(self) -> List[Game]:
        return self.__games

    def get_game_by_id(self, game_id) -> Game | None:
        for game in self.__games:
            if game.game_id == game_id:
                return game
        return None

    def get_number_of_games(self):
        return len(self.__games)

    def get_genres(self) -> List[Genre]:
        return self.__genres

    def add_genre(self, genre: Genre):
        self.__genres.append(genre)

    def get_games_by_genre(self, genre_name: str) -> List[Game]:
        return self.__games_by_genre.get(genre_name, [])

    def add_review(self, review: Review) -> Review:
        self.__reviews.append(review)
        return review

    def get_reviews_by_game_id(self, game_id) -> List[Review]:
        return [review for review in self.__reviews if review.game_id == game_id]

    def get_last_review(self) -> Review | None:
        if not self.__reviews:
            return None

        last_review = self.__reviews[-1]
        return last_review

    def get_first_review(self) -> Review | None:
        if not self.__reviews:
            return None

        first_review = self.__reviews[0]
        return first_review



    def populate(repo: AbstractRepository):

        dir_name = os.path.dirname(os.path.abspath(__file__))
        games_file_name = os.path.join(dir_name, "data/games.csv")
        reader = GameFileCSVReader(games_file_name)
        reader.read_csv_file()
        games = reader.dataset_of_games
        genres = reader.dataset_of_genres

        for game in games:
            repo.add_game(game)

        for genre in genres:
            repo.add_genre(genre)

class TestService:

    @pytest.fixture
    def repo(self):
        return MemoryRepository()

    def test_get_existing_game(self, repo):
        repo.add_game(Game(1, "life..."))
        game_id = 1
        game = repo.get_game(game_id)
        assert game is not None

    def test_get_pagination(self, repo):
        for i in range(1, 21):
            repo.add_game(Game(i, f"Game {i}"))

        page_number = 2
        page_size = 10
        games = repo.get_paginated_games(page_number, page_size)
        assert len(games) == page_size
        start_index = (page_number - 1) * page_size
        end_index = start_index + page_size
        expected_games = repo.get_games()[start_index:end_index]
        assert games == expected_games

    def test_search_by_genre(self, repo):
        genre = "Action"
        game1 = Game(1, "Game 1")
        repo.add_game(game1)
        repo.add_game(Game(2, "Game 2"))
        games = repo.get_games_by_genre(genre)
        assert all(game.genre == genre for game in games)

    def test_non_existing_search_key_raises_exception(self, repo):
        with pytest.raises(ValueError):
            invalid_search_key = 5434535
            repo.get_games_by_search_key(invalid_search_key)

    def test_publisher_init(repo):
        publisher1 = Publisher("Publisher A")
        assert repr(publisher1) == "<Publisher Publisher A>"
        assert publisher1.publisher_name == "Publisher A"

        publisher2 = Publisher("")
        assert publisher2.publisher_name is None

        publisher3 = Publisher(123)
        assert publisher3.publisher_name is None

        publisher4 = Publisher(" Wild Rooster   ")
        assert publisher4.publisher_name == "Wild Rooster"

        publisher4.publisher_name = "Century Game"
        assert repr(publisher4) == "<Publisher Century Game>"

    def test_game_init(repo):
        genre = Genre("Action")
        game = Game(1010, "Game Title")
        game.add_genre(genre)
        assert repr(game) == "<Game 1010, Game Title>"
        assert game.title == "Game Title"
        assert repr(game.genres[0]) == '<Genre Action>'

    def test_game_title_validation(repo):
        publisher = Publisher("Publisher A")
        genre = Genre("Action")

        with pytest.raises(ValueError):
            game = Game('', "")

        with pytest.raises(ValueError):
            game = Game('', genre)

        with pytest.raises(ValueError):
            game = Game('', publisher)

        with pytest.raises(ValueError):
            game = Game(-10, 0)

        with pytest.raises(ValueError):
            game = Game(publisher, genre)

    def test_game_release_date_validation(repo):
        game = Game(12345678, "God I hate writing tests, Amen")

        with pytest.raises(ValueError):
            game.release_date = "Dec 44, 0000"

        game.release_date = "Oct 21, 2008"

        expected_date = datetime.strptime("Oct 21, 2008", "%b %d, %Y")
        assert str(game.release_date) == 'Oct 21, 2008'
        assert expected_date == datetime(2008, 10, 21, 0, 0)

    def test_genre_init(repo):
        genre1 = Genre("Adventure")
        assert repr(genre1) == "<Genre Adventure>"
        assert genre1.genre_name == "Adventure"

        genre2 = Genre("")
        assert genre2.genre_name is None

        genre3 = Genre(123)
        assert genre3.genre_name is None

        genre4 = Genre("  Role-Playing  ")
        assert genre4.genre_name == "Role-Playing"

        with pytest.raises(AttributeError):
            genre4.genre_name = "RPG"

    def test_can_add_user(repo):
        new_user_name = 'jz'
        new_password = 'abcd1A23'

        auth_services.add_user(new_user_name, new_password, repo)

        user_as_dict = auth_services.get_user(new_user_name, repo)
        assert user_as_dict['user_name'] == new_user_name

        # Check that password has been encrypted.
        assert user_as_dict['password'].startswith('pbkdf2:sha256:')