import abc
from typing import List
from games.domainmodel.model import Game, Genre, User, Review

repo_instance = None


class RepositoryException(Exception):
    def __init__(self, message=None):
        print(f'RepositoryException: {message}')


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add_game(self, game: Game):
        """Add a game to repository list of aames"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_games(self) -> List[Game]:
        """Returns list of games"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_games(self):
        """Returns no. of games in repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_genres(self) -> List[Genre]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        raise NotImplementedError

    @abc.abstractmethod
    def get_games_by_genre(self, genre_name: str) -> List[Game]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user: User):
        """ Adds a user to the repository """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name) -> User:
        """ Returns the User named user_name from the repository.

        If there is no User with the given user_name, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review) -> Review:
        raise NotImplementedError

    @abc.abstractmethod
    def get_game_by_id(self, game_id) -> Game:
        raise NotImplementedError

    @abc.abstractmethod
    def get_reviews_by_game_id(self, game_id) -> Game:
        raise NotImplementedError

    @abc.abstractmethod
    def get_last_review(self) -> Review:
        raise NotImplementedError

    @abc.abstractmethod
    def get_first_review(self) -> Review:
        raise NotImplementedError

